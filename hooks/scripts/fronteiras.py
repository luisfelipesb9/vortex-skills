"""Gate de fronteiras de seguranca — PreToolUse em Bash.

Materializa em mecanica as regras que os 15 agentes repetem em prosa: nunca
faz merge, nunca force-push, acao irreversivel/externa para no humano.

**O que isto garante e o que nao garante.** E uma tabela de regex sobre a
string do comando: guardrail contra um modelo cooperativo e descuidado, que e
o caso real. NAO e sandbox e nao segura um modelo adversarial — `git $(echo
bWVyZ2U= | base64 -d)` passa. A fronteira de verdade continua sendo o sistema
de permissao do Claude Code somado ao `ask` chegando num humano.

Nenhum LLM no caminho: a decisao e uma tabela, nao um julgamento, e este hook
roda em toda chamada de Bash da sessao.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comum

# Isento antes de tudo: nao e execucao real, ou e recuperacao.
ISENTO = [
    re.compile(r"--dry-run\b"),
    re.compile(r"\bgit\s+merge\s+--abort\b"),
    re.compile(r"\b(echo|printf|cat|grep|rg)\b[^|;&]*\bgit\s+(merge|push)\b"),
]

# Irreversivel e explicitamente proibido pelo metodo do time: nega.
NEGAR = [
    (re.compile(r"\bgit\s+(-C\s+\S+\s+)?merge(?![-\w])"), "merge",
     "O time entrega via PR; merge e gate humano. Abra o PR (gh pr create) e pare."),
    (re.compile(r"\bgit\b[^;&|]*\bpush\b[^;&|]*(--force\b|--force-with-lease\b|\s-f\b)"), "force-push",
     "Force-push reescreve historico compartilhado. Se precisa mesmo, e decisao do humano."),
    (re.compile(r"\bgit\b[^;&|]*\bpush\b[^;&|]*(?<![\w/-])(main|master|prod|producao)(?![\w/-])"),
     "push em branch protegida",
     "Entregue numa branch de feature e abra o PR (gh pr create)."),
    (re.compile(r"\bgh\s+pr\s+merge\b"), "merge de PR",
     "Quem aprova e mergeia o PR e o humano."),
    (re.compile(r"\bgit\s+reset\s+--hard\b[^;&|]*\borigin/"), "reset --hard contra remoto",
     "Isso descarta trabalho local sem recuperacao. Confirme com o humano."),
]

# Irreversivel ou externo: pergunta, nao decide sozinho.
PERGUNTAR = [
    (re.compile(r"\b(vercel|netlify|flyctl|fly|railway|wrangler)\b[^;&|]*(--prod\b|--production\b|\bdeploy\b)"),
     "deploy de producao"),
    (re.compile(r"\bterraform\s+(apply|destroy)\b"), "mudanca de infraestrutura"),
    (re.compile(r"\bkubectl\s+(delete|apply|rollout)\b"), "mudanca em cluster"),
    (re.compile(r"\b(aws|gcloud|az)\b[^;&|]*\b(rm|delete|terminate|destroy)\b"), "recurso de nuvem"),
    (re.compile(r"\b(doppler|vault|op|gh\s+secret)\b[^;&|]*\b(set|write|put|create|delete)\b"), "secrets"),
    (re.compile(r"\b(cloudflare|route53|namecheap)\b|\bdns\b[^;&|]*\b(create|update|delete)\b"), "DNS"),
    (re.compile(r"\bstripe\b[^;&|]*\b(charge|payment|subscription|refund)\b"), "acao financeira"),
    # Remocao destrutiva so fora da arvore de trabalho: `rm -rf node_modules`
    # e limpeza rotineira e nunca pode travar.
    (re.compile(r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*\s+(/|~|\$HOME|\*)"), "remocao destrutiva"),
    (re.compile(r"\bdocker\s+system\s+prune\b"), "prune destrutivo"),
]

COMO_DESLIGAR = 'Reduzir a aviso neste projeto: .vortex/config.json -> {"niveis":{"fronteiras":"warn"}}'


def avaliar(comando, nivel):
    """Devolve (decisao, motivo). decisao em allow|ask|deny."""
    if nivel == "off" or not comando:
        return "allow", ""

    if any(rx.search(comando) for rx in ISENTO):
        return "allow", ""

    for rx, rotulo, remediacao in NEGAR:
        if rx.search(comando):
            # Em `warn` o gate rebaixa para `ask`: o humano decide em vez de so
            # ser impedido. Nunca vira allow silencioso.
            decisao = "deny" if nivel == "block" else "ask"
            verbo = "Bloqueado" if decisao == "deny" else "Confirmar"
            return decisao, f"[VORTEX/fronteiras] {verbo}: {rotulo}. {remediacao} {COMO_DESLIGAR}"

    for rx, rotulo in PERGUNTAR:
        if rx.search(comando):
            if nivel == "warn":
                return "allow", ""
            return "ask", (
                f"[VORTEX/fronteiras] Acao irreversivel ou externa: {rotulo}. "
                f"Confirme se e isso mesmo antes de seguir. {COMO_DESLIGAR}")

    return "allow", ""


def responder(entrada, nivel):
    """String JSON a imprimir, ou None quando nao ha nada a dizer."""
    if (entrada or {}).get("tool_name") != "Bash":
        return None
    comando = ((entrada or {}).get("tool_input") or {}).get("command") or ""
    decisao, motivo = avaliar(comando, nivel)
    if decisao == "allow":
        return None
    return _comum.saida_pretooluse(decisao, motivo)


def corpo(entrada):
    raiz = _comum.raiz_projeto(entrada)
    arg = None
    if "--nivel" in sys.argv:
        arg = sys.argv[sys.argv.index("--nivel") + 1]
    return responder(entrada, _comum.resolver_nivel("fronteiras", arg, raiz))


if __name__ == "__main__":
    _comum.executar(corpo)
