"""Reancoragem do ledger — SessionStart e PostCompact.

A skill `jet-subagentes` diz, com todas as letras, que o erro mais caro ja
observado foi um controlador redespachando tasks ja concluidas depois de uma
compactacao. A causa e simples: memoria de conversa nao sobrevive a
compactacao. Disco sobrevive.

Este hook le o ledger e o git log e devolve isso como contexto, nos dois
momentos em que a memoria acabou de ser perdida ou ainda nao existe. Ele
**nunca bloqueia nada** — so injeta. E o hook de menor risco e maior retorno
do plugin.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comum

# "Task 3: concluída", "- Task 3: concluida", "* Task 3 : CONCLUÍDA"
CONCLUIDA = re.compile(r"^\s*[-*]?\s*Task\s+([\d.]+)\s*:?\s*[^\n]*\bconclu[ií]d", re.I | re.M)


def tasks_concluidas(ledger):
    return CONCLUIDA.findall(ledger or "")


def _caminho_ledger(raiz):
    import os
    rel = os.environ.get("JET_LEDGER_PATH") or ".jet/sdd/progress.md"
    return Path(raiz) / rel


def _git_log(raiz):
    """Commits recentes. Lista fixa de argumentos, sem shell, sem interpolacao."""
    try:
        r = subprocess.run(
            ["git", "-C", str(raiz), "log", "--oneline", "-15"],
            capture_output=True, text=True, timeout=3,
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception as e:
        _comum.log_erro("git_log", e)
        return ""


def montar(raiz, evento):
    """Texto de reancoragem, ou None quando nao ha ledger neste projeto."""
    ledger_p = _caminho_ledger(raiz)
    if not ledger_p.is_file():
        return None

    ledger = ledger_p.read_text(encoding="utf-8")
    feitas = tasks_concluidas(ledger)
    momento = "Sessao iniciada" if evento == "SessionStart" else "Contexto compactado"

    linhas = [f"[JET/ledger] {momento}. Estado real do trabalho, lido do disco:", ""]
    if feitas:
        linhas.append(f"Tasks ja CONCLUIDAS: {', '.join(feitas)}.")
        linhas.append(
            "Nao redespache nenhuma delas. Retome na primeira task nao marcada no ledger. "
            "Os commits abaixo existem no git mesmo que voce nao lembre de te-los criado."
        )
    else:
        linhas.append("Nenhuma task marcada como concluida ainda.")
    linhas += ["", f"Ledger ({ledger_p}):", ledger.strip()]

    log = _git_log(raiz)
    if log:
        linhas += ["", "Commits recentes:", log]
    return "\n".join(linhas)


def responder(entrada):
    entrada = entrada or {}
    # O ledger e contexto do controlador. Um subagente recebe o brief da task
    # dele e nada mais — reancorar ali so poluiria o contexto isolado que a
    # jet-subagentes cuida de montar.
    if entrada.get("agent_id"):
        return None
    evento = entrada.get("hook_event_name") or "SessionStart"
    texto = montar(_comum.raiz_projeto(entrada), evento)
    if not texto:
        return None
    return _comum.saida_contexto(evento, texto)


if __name__ == "__main__":
    _comum.executar(responder)
