"""Testes de doutor.py — o validador real dos frontmatters de agente.

`claude plugin validate` so confere a PRESENCA do bloco de frontmatter; ele
aceita effort invalido, maxTurns negativo, color inexistente e
permissionMode perigoso sem reclamar. Este modulo e quem cobra os valores.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import doutor  # noqa: E402


def agente(**campos):
    linhas = ["---"]
    for k, v in campos.items():
        linhas.append(f"{k}: {v}")
    linhas += ["---", "", "corpo do agente"]
    return "\n".join(linhas)


class TestValidarAgente(unittest.TestCase):
    def checar(self, conteudo, nome="jet-x.md"):
        d = Path(tempfile.mkdtemp())
        p = d / nome
        p.write_text(conteudo)
        return doutor.validar_agente(p)

    def test_agente_valido_nao_gera_achado(self):
        self.assertEqual(self.checar(agente(
            name="jet-x", description="faz x", model="sonnet",
            effort="high", maxTurns=60, color="cyan",
        )), [])

    def test_sem_name_e_tratado_como_doc_colocado_nao_como_erro(self):
        """README ao lado do agente nao tem name — e documentacao, nao defeito."""
        self.assertEqual(self.checar("# jet-x\n\ndoc sem frontmatter", nome="README.md"), [])

    def test_sem_description_e_erro(self):
        achados = self.checar(agente(name="jet-x", model="sonnet"))
        self.assertTrue(any(a["campo"] == "description" and a["nivel"] == "erro" for a in achados))

    def test_effort_invalido(self):
        achados = self.checar(agente(name="jet-x", description="d", effort="altissimo"))
        self.assertTrue(any(a["campo"] == "effort" and a["nivel"] == "erro" for a in achados))

    def test_effort_valido_aceita_palavra_e_inteiro(self):
        for v in ("low", "medium", "high", "xhigh", "max", "3"):
            self.assertEqual(
                [a for a in self.checar(agente(name="jet-x", description="d", effort=v)) if a["campo"] == "effort"],
                [], f"effort={v} deveria ser valido",
            )

    def test_maxturns_negativo_ou_zero(self):
        for v in ("-5", "0"):
            achados = self.checar(agente(name="jet-x", description="d", maxTurns=v))
            self.assertTrue(any(a["campo"] == "maxTurns" for a in achados), f"maxTurns={v}")

    def test_color_fora_da_paleta(self):
        achados = self.checar(agente(name="jet-x", description="d", color="roxo-neon"))
        self.assertTrue(any(a["campo"] == "color" for a in achados))

    def test_permission_mode_perigoso_e_erro(self):
        """bypassPermissions anula o `ask` das fronteiras — nunca pode passar."""
        for v in ("bypassPermissions", "dontAsk", "auto"):
            achados = self.checar(agente(name="jet-x", description="d", permissionMode=v))
            self.assertTrue(
                any(a["campo"] == "permissionMode" and a["nivel"] == "erro" for a in achados), v
            )

    def test_tool_mcp_hardcoded_e_erro_de_portabilidade(self):
        """O namespace de um MCP depende de quem instalou; hardcodar quebra fora da origem."""
        achados = self.checar(agente(
            name="jet-designer", description="d",
            tools='["Read", "mcp__claude_ai_Figma__get_design_context"]',
        ))
        self.assertTrue(any(a["campo"] == "tools" and a["nivel"] == "erro" for a in achados))

    def test_tool_task_legado_e_aviso(self):
        """`Task` era o nome antigo; hoje o tool de delegacao e `Agent`."""
        achados = self.checar(agente(name="jet-x", description="d", tools='["Read", "Task"]'))
        self.assertTrue(any(a["campo"] == "tools" and a["nivel"] == "aviso" for a in achados))

    def test_description_longa_demais_para_o_picker(self):
        longa = " ".join(["palavra"] * 40)
        achados = self.checar(agente(name="jet-x", description=longa))
        self.assertTrue(any(a["campo"] == "description" and a["nivel"] == "aviso" for a in achados))

    def test_name_divergente_do_arquivo(self):
        achados = self.checar(agente(name="outro-nome", description="d"), nome="jet-x.md")
        self.assertTrue(any(a["campo"] == "name" for a in achados))


class TestVarrerDiretorio(unittest.TestCase):
    def test_detecta_name_duplicado_entre_arquivos(self):
        d = Path(tempfile.mkdtemp())
        for sub in ("a", "b"):
            (d / sub).mkdir()
            (d / sub / f"{sub}.md").write_text(agente(name="mesmo", description="d"))
        achados = doutor.varrer_agentes(d)
        self.assertTrue(any(a["campo"] == "name" and "duplicad" in a["mensagem"] for a in achados))

    def test_diretorio_sem_agentes_nao_quebra(self):
        self.assertEqual(doutor.varrer_agentes(Path(tempfile.mkdtemp())), [])


if __name__ == "__main__":
    unittest.main()
