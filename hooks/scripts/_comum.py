"""Base comum dos hooks do Vortex Skills.

Tres responsabilidades, nesta ordem de importancia:

1. **Fail-open.** Um hook que nega quando ele proprio quebra e pior que nao ter
   hook. Toda excecao vira exit 0 silencioso + uma linha em erros.jsonl.
2. **Descoberta de projeto.** O comando de teste nunca e hardcodado; sai do
   manifesto do projeto. Projeto sem suite desliga os gates que dependem dela.
3. **Niveis.** Precedencia .vortex/config.json > env > userConfig > default, com a
   regra dura de que valor invalido NUNCA escala severidade.

Sem dependencia externa: roda com `python3 -S`, so stdlib.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

NIVEIS_VALIDOS = ("off", "warn", "block")

# Default por gate. Fronteiras e ledger sao deterministicos e o dano do falso
# negativo e irreversivel, entao nascem em block. TDD e verificacao dependem do
# aparato da v2 e nascem desligados.
NIVEIS_PADRAO = {
    "fronteiras": "block",
    "ledger": "block",
    "tdd": "off",
    "verificacao": "off",
}


# --------------------------------------------------------------------------
# Diagnostico
# --------------------------------------------------------------------------

def dir_dados():
    """Diretorio de estado do plugin. Cai no temp se o runtime nao exportar."""
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(
        os.path.expanduser("~"), ".claude", "vortex-skills"
    )
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        return None
    return base


def log_erro(origem, erro, extra=None):
    """Registra e segue. Nunca levanta — e chamado de dentro do except."""
    base = dir_dados()
    if not base:
        return
    try:
        linha = json.dumps(
            {"t": int(time.time()), "origem": origem, "erro": str(erro)[:500], "extra": extra},
            ensure_ascii=False,
        )
        with open(os.path.join(base, "erros.jsonl"), "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except Exception:
        pass


# --------------------------------------------------------------------------
# Descoberta de projeto
# --------------------------------------------------------------------------

def raiz_projeto(entrada=None):
    """Raiz do projeto: CLAUDE_PROJECT_DIR, senao o cwd que o hook recebeu."""
    for c in (os.environ.get("CLAUDE_PROJECT_DIR"), (entrada or {}).get("cwd"), os.getcwd()):
        if c:
            return Path(c)
    return Path(".")


def _config_projeto(raiz):
    try:
        p = Path(raiz) / ".vortex" / "config.json"
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        log_erro("config_projeto", e)
    return {}


def _gerenciador_node(raiz):
    for arquivo, pm in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun")):
        if (raiz / arquivo).is_file():
            return pm
    return "npm"


def _prefixo_python(raiz):
    if (raiz / "uv.lock").is_file():
        return "uv run "
    if (raiz / "poetry.lock").is_file():
        return "poetry run "
    return ""


def descobrir_comando_teste(raiz):
    """Comando de teste do projeto, ou None se o projeto nao tem suite.

    None e um resultado legitimo e importante: e o que faz os gates se
    desligarem sozinhos num repo de conteudo, em vez de bloquearem todo commit.
    """
    raiz = Path(raiz)

    # 1. Escape hatch explicito do projeto — sempre vence.
    explicito = _config_projeto(raiz).get("test_command")
    if explicito:
        return explicito

    # 2. Sniff por manifesto.
    try:
        pkg = raiz / "package.json"
        if pkg.is_file():
            dados = json.loads(pkg.read_text(encoding="utf-8"))
            if (dados.get("scripts") or {}).get("test"):
                return f"{_gerenciador_node(raiz)} test"

        pyproject = raiz / "pyproject.toml"
        tem_pytest = (
            (pyproject.is_file() and "[tool.pytest" in pyproject.read_text(encoding="utf-8"))
            or (raiz / "pytest.ini").is_file()
            or (raiz / "tox.ini").is_file()
        )
        if tem_pytest:
            return _prefixo_python(raiz) + "pytest"

        if (raiz / "Cargo.toml").is_file():
            return "cargo test"
        if (raiz / "go.mod").is_file():
            return "go test ./..."
        if (raiz / "Gemfile").is_file() and (raiz / "spec").is_dir():
            return "bundle exec rspec"
        if (raiz / "mix.exs").is_file():
            return "mix test"
        if (raiz / "composer.json").is_file() and (raiz / "phpunit.xml").is_file():
            return "vendor/bin/phpunit"
        if (raiz / "deno.json").is_file():
            return "deno test"
        if any(raiz.glob("*.csproj")) or any(raiz.glob("*.sln")):
            return "dotnet test"

        makefile = raiz / "Makefile"
        if makefile.is_file() and re.search(r"^test:", makefile.read_text(encoding="utf-8"), re.M):
            return "make test"
    except Exception as e:
        log_erro("descobrir_comando_teste", e)

    # 3. Sem suite detectada.
    return None


# --------------------------------------------------------------------------
# Niveis
# --------------------------------------------------------------------------

def _valido(v):
    return isinstance(v, str) and v.strip().lower() in NIVEIS_VALIDOS


def resolver_nivel(gate, do_user_config, raiz):
    """Nivel efetivo de um gate.

    Precedencia: .vortex/config.json > env > userConfig > default.
    Valor invalido em qualquer camada e descartado e logado — nunca escala
    severidade, nunca vira block por acidente. Isso cobre tambem o caso em que
    o runtime nao expande ${user_config.X} e o literal chega ate aqui.
    """
    candidatos = (
        ((_config_projeto(raiz).get("niveis") or {}).get(gate), "config_projeto"),
        (os.environ.get(f"VORTEX_NIVEL_{gate.upper()}"), "env"),
        (do_user_config, "user_config"),
    )
    for valor, camada in candidatos:
        if valor is None or valor == "":
            continue
        if _valido(valor):
            return valor.strip().lower()
        log_erro("resolver_nivel", f"valor invalido '{valor}'", {"gate": gate, "camada": camada})
    return NIVEIS_PADRAO.get(gate, "off")


# --------------------------------------------------------------------------
# Contrato de saida
# --------------------------------------------------------------------------

def saida_pretooluse(decisao, motivo):
    """JSON de decisao de PreToolUse, em UM unico documento e UMA unica linha.

    Varios documentos, ou saida que nao comeca com '{', fazem o Claude Code
    tratar tudo como texto puro e a decisao se perde em silencio.
    """
    return json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decisao,
                "permissionDecisionReason": " ".join(str(motivo).split()),
            }
        },
        ensure_ascii=False,
    )


def saida_contexto(evento, texto):
    """Injeta contexto adicional sem bloquear nada."""
    return json.dumps(
        {"hookSpecificOutput": {"hookEventName": evento, "additionalContext": texto}},
        ensure_ascii=False,
    )


# --------------------------------------------------------------------------
# Runner fail-open
# --------------------------------------------------------------------------

def executar(corpo, entrada_bruta=None):
    """Roda o corpo do hook e SEMPRE sai com 0.

    `corpo` recebe a entrada ja desserializada e devolve a string a imprimir
    (ou None para nao dizer nada). Qualquer excepcao — inclusive stdin
    malformado — vira exit 0 silencioso: fail-open e a regra.
    """
    try:
        if entrada_bruta is None:
            entrada_bruta = sys.stdin.read()
        entrada = json.loads(entrada_bruta) if entrada_bruta.strip() else {}
        resposta = corpo(entrada)
        if resposta:
            sys.stdout.write(resposta)
    except Exception as e:
        log_erro(getattr(corpo, "__name__", "hook"), e)
    sys.exit(0)
