"""Gera o mapa do sistema a partir dos frontmatters.

A pagina visual e DERIVADA, nunca escrita a mao: documentacao paralela diverge
do codigo em semanas; documentacao gerada nao pode divergir.

    python3 -S tools/gerar-mapa.py > mapa.json
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "hooks/scripts"))
from doutor import ler_frontmatter  # noqa: E402

TIMES = {
    "vortex-implementador": "dev", "vortex-dev-backend": "dev", "vortex-dev-frontend": "dev",
    "vortex-dev-dados": "dev", "vortex-dev-devops": "dev",
    "vortex-maestro": "processo", "vortex-revisor": "processo",
    "vortex-pesquisador": "processo", "vortex-doc": "processo",
    "vortex-copywriter": "agencia", "vortex-trafego": "agencia", "vortex-seo": "agencia",
    "vortex-analista-dados": "agencia", "vortex-gestor-projetos": "agencia", "vortex-designer": "agencia",
}


def lista(bruto):
    bruto = (bruto or "").strip()
    if not bruto:
        return []
    if bruto == '"*"':
        return ["*"]
    if bruto.startswith("["):
        return [t.strip().strip('"').strip("'") for t in bruto[1:-1].split(",") if t.strip()]
    return [t.strip() for t in bruto.split(",") if t.strip()]


def agentes():
    saida = []
    for f in sorted((RAIZ / "agents").glob("*.md")):
        c = ler_frontmatter(f)
        if not c or "name" not in c:
            continue
        saida.append({
            "nome": c["name"], "titulo": c.get("displayName", c["name"]),
            "descricao": c.get("description", ""),
            "time": TIMES.get(c["name"], "processo"),
            "modelo": c.get("model", "—"), "esforco": c.get("effort", "—"),
            "cor": c.get("color", "cyan"),
            "turnos": int(c["maxTurns"]) if c.get("maxTurns", "").isdigit() else None,
            "memoria": c.get("memory") == "project",
            "background": c.get("background") == "true",
            "semClaudeMd": c.get("omitClaudeMd") == "true",
            "ferramentas": lista(c.get("tools")),
            "proibido": lista(c.get("disallowedTools")),
            "skills": lista(c.get("skills")),
        })
    return saida


def skills():
    saida = []
    for f in sorted((RAIZ / "skills").glob("*/SKILL.md")):
        c = ler_frontmatter(f) or {}
        d = (c.get("description") or "").strip().strip('"')
        saida.append({"nome": c.get("name", f.parent.name),
                      "descricao": d.split("Gatilhos")[0].strip(" .—-"),
                      "linhas": len(f.read_text(encoding="utf-8").splitlines())})
    return saida


def comandos():
    saida = []
    for f in sorted((RAIZ / "commands").glob("*.md")):
        c = ler_frontmatter(f) or {}
        saida.append({"nome": "/" + f.stem,
                      "descricao": (c.get("description") or "").strip(),
                      "args": (c.get("argument-hint") or "").strip().strip('"'),
                      "fork": c.get("context") == "fork"})
    return saida


def gates():
    h = json.loads((RAIZ / "hooks/hooks.json").read_text(encoding="utf-8"))
    saida = []
    for evento, grupos in h["hooks"].items():
        for g in grupos:
            script = Path(g["hooks"][0]["args"][1]).name
            saida.append({"evento": evento, "matcher": g.get("matcher"),
                          "script": script, "rotulo": g["hooks"][0].get("statusMessage", "")})
    return saida


if __name__ == "__main__":
    _ag = agentes()
    if not _ag:
        sys.exit("gerar-mapa: zero agentes lidos — o glob nao bate com a estrutura de agents/")
    json.dump({"agentes": _ag, "skills": skills(),
               "comandos": comandos(), "gates": gates()},
              sys.stdout, ensure_ascii=False, indent=2)
