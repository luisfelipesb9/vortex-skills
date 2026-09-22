"""Gate de integridade do ledger — PreToolUse em Agent.

Impede redespachar uma task que o ledger ja marca como concluida. A
`jet-subagentes` chama isso de "o erro mais caro observado": um controlador
que, depois de uma compactacao, rechama sequencias inteiras de tasks ja
feitas.

O `contexto.py` ja reancora o ledger em SessionStart e PostCompact — mas
reancorar e **conselho**, e o repo diz que esse conselho ja foi ignorado e
custou caro. A diferenca entre conselho e mecanismo sao estas ~80 linhas.

**Duas regras de desenho:**

1. *Nunca adivinha.* Sem numero de task explicito no despacho, libera. Um
   gate que chuta trava trabalho legitimo, e falso positivo aqui e caro: o
   humano perde a capacidade de despachar.
2. *O brief tem precedencia sobre a prosa.* Um brief da Task 5 cujo texto
   menciona "consome o que a Task 3 produziu" e um despacho da 5, nao da 3.

**Fora de escopo, deliberado:** detectar implementadores em paralelo. Isso
exigiria lockfile com TTL, e lock preso bloqueia TODO despacho — o modo de
falha que `_comum.py` proibe em caixa alta. Continua sendo um "Nunca"
explicito na skill.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comum
import contexto  # reusa tasks_concluidas(): uma fonte de verdade so

# Quem implementa. O revisor fica de fora de proposito: re-revisar uma task
# concluida e legitimo e acontece no fluxo normal.
IMPLEMENTADORES = {
    "jet-implementador",
    "jet-dev-backend",
    "jet-dev-frontend",
    "jet-dev-dados",
    "jet-dev-devops",
}

# `task-3-brief.md`, `task_3_brief`, `task 3 brief`. O brief e nomeado pelo
# controlador com numero canonico, entao o numero viaja por construcao.
BRIEF = re.compile(r"task[-_\s]?(\d+(?:\.\d+)?)[-_\s]?brief", re.I)
PROSA = re.compile(r"\bTask\s+(\d+(?:\.\d+)?)\b", re.I)


def numero_da_task(prompt, subagent_type):
    """(numero, aplicavel). Aplicavel = este despacho e de implementacao."""
    prompt = prompt or ""

    m = BRIEF.search(prompt)
    if m:
        # Brief nomeado: e despacho de implementacao por definicao, e o numero
        # e o do brief — nao o de qualquer task citada no corpo.
        return m.group(1), True

    m = PROSA.search(prompt)
    if m and subagent_type in IMPLEMENTADORES:
        return m.group(1), True

    return None, False


def responder(entrada, nivel):
    entrada = entrada or {}
    if entrada.get("tool_name") not in ("Agent", "Task"):
        return None
    if nivel == "off":
        return None

    entradas = entrada.get("tool_input") or {}
    numero, aplicavel = numero_da_task(entradas.get("prompt"), entradas.get("subagent_type"))
    if not aplicavel or numero is None:
        return None

    raiz = _comum.raiz_projeto(entrada)
    ledger_p = contexto._caminho_ledger(raiz)
    try:
        ledger = ledger_p.read_text(encoding="utf-8")
    except Exception:
        # Ledger ausente ou ilegivel: projeto novo, ou disco com problema.
        # Fail-open — nao e trabalho deste gate adivinhar estado.
        return None

    if numero not in contexto.tasks_concluidas(ledger):
        return None

    decisao = "deny" if nivel == "block" else "ask"
    verbo = "Bloqueado" if decisao == "deny" else "Confirmar"
    return _comum.saida_pretooluse(decisao, (
        f"[JET/ledger] {verbo}: redespacho da Task {numero}. "
        f"O ledger marca a Task {numero} como concluida ({ledger_p}). "
        "Retome na primeira task nao marcada, ou reabra a task editando o ledger antes. "
        'Reduzir a aviso neste projeto: .jet/config.json -> {"niveis":{"ledger":"warn"}}'
    ))


def corpo(entrada):
    raiz = _comum.raiz_projeto(entrada)
    arg = None
    if "--nivel" in sys.argv:
        arg = sys.argv[sys.argv.index("--nivel") + 1]
    return responder(entrada, _comum.resolver_nivel("ledger", arg, raiz))


if __name__ == "__main__":
    _comum.executar(corpo)
