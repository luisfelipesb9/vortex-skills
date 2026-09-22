"""Validador de frontmatter dos agentes JET + diagnostico do enforcement.

Existe porque `claude plugin validate` so confere a PRESENCA do bloco de
frontmatter. Verificado empiricamente no Claude Code 2.1.273: ele aceita sem
reclamar `effort: altissimo`, `maxTurns: -5`, `color: roxo-neon` e
`permissionMode: bypassPermissions`. Este script cobra os valores.

Uso:
    python3 -S doutor.py            # diagnostico completo
    python3 -S doutor.py --agentes  # so a varredura de frontmatter
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comum

EFFORTS = ("low", "medium", "high", "xhigh", "max")
CORES = ("red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta")
MODOS_PERIGOSOS = ("bypassPermissions", "dontAsk", "auto")
MODOS_VALIDOS = ("default", "acceptEdits", "plan") + MODOS_PERIGOSOS
MAX_PALAVRAS_DESCRICAO = 25


def _achado(nivel, campo, mensagem, arquivo=None):
    return {"nivel": nivel, "campo": campo, "mensagem": mensagem, "arquivo": str(arquivo or "")}


def ler_frontmatter(caminho):
    """Devolve o dict do frontmatter, ou None se o arquivo nao tem bloco.

    Parser deliberadamente raso: chave: valor no topo do arquivo. Sem YAML,
    porque o plugin roda com `python3 -S` e nao pode depender de pyyaml.
    """
    try:
        texto = Path(caminho).read_text(encoding="utf-8")
    except Exception:
        return None
    if not texto.startswith("---"):
        return None
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return None
    campos = {}
    for linha in partes[1].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", linha)
        if m:
            campos[m.group(1)] = m.group(2).strip()
    return campos


def _tools_como_lista(bruto):
    """Aceita as duas formas: array YAML e string separada por virgula."""
    bruto = (bruto or "").strip()
    if not bruto:
        return []
    if bruto.startswith("["):
        return [t.strip().strip('"').strip("'") for t in bruto[1:-1].split(",") if t.strip()]
    return [t.strip() for t in bruto.split(",") if t.strip()]


def validar_agente(caminho):
    """Achados de UM arquivo de agente. Lista vazia = limpo."""
    caminho = Path(caminho)
    campos = ler_frontmatter(caminho)

    # Sem frontmatter, ou frontmatter sem `name`: e documentacao co-locada.
    # O proprio loader do Claude Code ignora esses arquivos em silencio.
    if not campos or "name" not in campos:
        return []

    achados = []
    nome = campos["name"].strip()

    if nome != caminho.stem:
        achados.append(_achado(
            "erro", "name",
            f"name '{nome}' diverge do arquivo '{caminho.stem}.md'", caminho))

    desc = campos.get("description", "").strip()
    if not desc:
        achados.append(_achado("erro", "description", "description ausente — o agente nao carrega", caminho))
    elif len(desc.split()) > MAX_PALAVRAS_DESCRICAO:
        achados.append(_achado(
            "aviso", "description",
            f"{len(desc.split())} palavras (max {MAX_PALAVRAS_DESCRICAO}) — "
            "isso renderiza no picker de agentes; mova o detalhe para o corpo", caminho))

    if "effort" in campos:
        v = campos["effort"].strip()
        if v not in EFFORTS and not v.isdigit():
            achados.append(_achado(
                "erro", "effort", f"'{v}' invalido — use {'|'.join(EFFORTS)} ou inteiro", caminho))

    if "maxTurns" in campos:
        v = campos["maxTurns"].strip()
        if not (v.lstrip("-").isdigit() and int(v) > 0):
            achados.append(_achado("erro", "maxTurns", f"'{v}' precisa ser inteiro positivo", caminho))

    if "color" in campos:
        v = campos["color"].strip()
        if v not in CORES:
            achados.append(_achado("erro", "color", f"'{v}' fora da paleta ({', '.join(CORES)})", caminho))

    if "permissionMode" in campos:
        v = campos["permissionMode"].strip()
        if v in MODOS_PERIGOSOS:
            achados.append(_achado(
                "erro", "permissionMode",
                f"'{v}' desarma o gate humano e anula o `ask` das fronteiras", caminho))
        elif v not in MODOS_VALIDOS:
            achados.append(_achado("erro", "permissionMode", f"'{v}' invalido", caminho))

    tools = _tools_como_lista(campos.get("tools"))
    mcp = [t for t in tools if t.startswith("mcp__")]
    if mcp:
        achados.append(_achado(
            "erro", "tools",
            f"{len(mcp)} tool(s) MCP com namespace fixo ({mcp[0]}...) — o namespace depende "
            "de quem instalou o servidor, entao isso nao resolve fora do ambiente de origem", caminho))
    if "Task" in tools:
        achados.append(_achado(
            "aviso", "tools", "'Task' e o nome legado; o tool de delegacao hoje e 'Agent'", caminho))

    return achados


def varrer_agentes(raiz):
    """Valida todos os agentes sob `raiz` e cobra unicidade de `name`."""
    raiz = Path(raiz)
    achados, vistos = [], {}
    for caminho in sorted(raiz.rglob("*.md")):
        achados.extend(validar_agente(caminho))
        campos = ler_frontmatter(caminho)
        if campos and "name" in campos:
            nome = campos["name"].strip()
            if nome in vistos:
                achados.append(_achado(
                    "erro", "name",
                    f"name '{nome}' duplicado (tambem em {vistos[nome]}) — "
                    "um dos dois e descartado em silencio", caminho))
            vistos[nome] = caminho.name
    return achados


# --------------------------------------------------------------------------
# Relatorio
# --------------------------------------------------------------------------

# Contrato de saida — DESIGN.md secao 2. Largura fixa para alinhar em coluna:
# o olho aprende onde olhar e para de ler a linha inteira. Sem emoji, sem cor
# ANSI — o terminal do leitor ja tem tema, competir com ele e ruido.
MARCA = {"erro": "ERRO ", "aviso": "aviso"}


def cabecalho(gate, resumo):
    """Abertura de toda mensagem de gate: quem esta falando, e o veredito."""
    return f"[JET/{gate}] {resumo}"


def linha_gate(nivel, arquivo, campo, mensagem):
    """Uma linha de achado, alinhada em coluna."""
    return f"{MARCA[nivel]} {arquivo:<26} {campo}: {mensagem}"


def relatorio(raiz_plugin, raiz_projeto):
    linhas = [cabecalho("doutor", "diagnostico do enforcement"), ""]

    linhas.append("Projeto")
    cmd = _comum.descobrir_comando_teste(raiz_projeto)
    linhas.append(f"  raiz            {raiz_projeto}")
    linhas.append(f"  comando teste   {cmd or 'nenhum detectado — gates de suite ficam inativos'}")
    linhas.append("")

    linhas.append("Niveis efetivos")
    for gate in ("fronteiras", "ledger", "tdd", "verificacao"):
        linhas.append(f"  {gate:<14}  {_comum.resolver_nivel(gate, None, raiz_projeto)}")
    linhas.append("")

    dir_agentes = Path(raiz_plugin) / "agents"
    achados = varrer_agentes(dir_agentes) if dir_agentes.is_dir() else []
    total = len(list(dir_agentes.rglob("*.md"))) if dir_agentes.is_dir() else 0
    erros = [a for a in achados if a["nivel"] == "erro"]
    linhas.append(f"Agentes ({total} arquivos varridos)")
    if not achados:
        linhas.append("  todos os frontmatters validos")
    else:
        for a in achados:
            arq = Path(a["arquivo"]).name
            linhas.append("  " + linha_gate(a['nivel'], arq, a['campo'], a['mensagem']))
    linhas.append("")

    base = _comum.dir_dados()
    erros_log = Path(base) / "erros.jsonl" if base else None
    if erros_log and erros_log.is_file():
        recentes = erros_log.read_text(encoding="utf-8").strip().splitlines()[-5:]
        linhas.append(f"Erros de hook ({len(recentes)} mais recentes)")
        linhas.extend(f"  {l[:150]}" for l in recentes)
    else:
        linhas.append("Erros de hook: nenhum registrado")

    linhas.append("")
    linhas.append("Fluxo de operacao: /jet-fluxo")

    return "\n".join(linhas), len(erros)


def main():
    raiz_plugin = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).resolve().parents[2]))
    raiz_proj = _comum.raiz_projeto()

    if "--agentes" in sys.argv:
        achados = varrer_agentes(raiz_plugin / "agents")
        if "--json" in sys.argv:
            print(json.dumps(achados, ensure_ascii=False, indent=2))
        else:
            for a in achados:
                print(linha_gate(a['nivel'], Path(a['arquivo']).name, a['campo'], a['mensagem']))
            erros = len([a for a in achados if a["nivel"] == "erro"])
            print("\n" + cabecalho("doutor", f"{len(achados)} achado(s), {erros} erro(s)"))
        return 1 if any(a["nivel"] == "erro" for a in achados) else 0

    texto, erros = relatorio(raiz_plugin, raiz_proj)
    print(texto)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
