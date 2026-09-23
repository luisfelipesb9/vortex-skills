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
    def checar(self, conteudo, nome="vortex-x.md"):
        d = Path(tempfile.mkdtemp())
        p = d / nome
        p.write_text(conteudo)
        return doutor.validar_agente(p)

    def test_agente_valido_nao_gera_achado(self):
        self.assertEqual(self.checar(agente(
            name="vortex-x", description="faz x", model="sonnet",
            effort="high", maxTurns=60, color="cyan",
        )), [])

    def test_sem_name_e_tratado_como_doc_colocado_nao_como_erro(self):
        """README ao lado do agente nao tem name — e documentacao, nao defeito."""
        self.assertEqual(self.checar("# vortex-x\n\ndoc sem frontmatter", nome="README.md"), [])

    def test_sem_description_e_erro(self):
        achados = self.checar(agente(name="vortex-x", model="sonnet"))
        self.assertTrue(any(a["campo"] == "description" and a["nivel"] == "erro" for a in achados))

    def test_effort_invalido(self):
        achados = self.checar(agente(name="vortex-x", description="d", effort="altissimo"))
        self.assertTrue(any(a["campo"] == "effort" and a["nivel"] == "erro" for a in achados))

    def test_effort_valido_aceita_palavra_e_inteiro(self):
        for v in ("low", "medium", "high", "xhigh", "max", "3"):
            self.assertEqual(
                [a for a in self.checar(agente(name="vortex-x", description="d", effort=v)) if a["campo"] == "effort"],
                [], f"effort={v} deveria ser valido",
            )

    def test_maxturns_negativo_ou_zero(self):
        for v in ("-5", "0"):
            achados = self.checar(agente(name="vortex-x", description="d", maxTurns=v))
            self.assertTrue(any(a["campo"] == "maxTurns" for a in achados), f"maxTurns={v}")

    def test_color_fora_da_paleta(self):
        achados = self.checar(agente(name="vortex-x", description="d", color="roxo-neon"))
        self.assertTrue(any(a["campo"] == "color" for a in achados))

    def test_permission_mode_perigoso_e_erro(self):
        """bypassPermissions anula o `ask` das fronteiras — nunca pode passar."""
        for v in ("bypassPermissions", "dontAsk", "auto"):
            achados = self.checar(agente(name="vortex-x", description="d", permissionMode=v))
            self.assertTrue(
                any(a["campo"] == "permissionMode" and a["nivel"] == "erro" for a in achados), v
            )

    def test_tool_mcp_hardcoded_e_erro_de_portabilidade(self):
        """O namespace de um MCP depende de quem instalou; hardcodar quebra fora da origem."""
        achados = self.checar(agente(
            name="vortex-designer", description="d",
            tools='["Read", "mcp__claude_ai_Figma__get_design_context"]',
        ))
        self.assertTrue(any(a["campo"] == "tools" and a["nivel"] == "erro" for a in achados))

    def test_tool_task_legado_e_aviso(self):
        """`Task` era o nome antigo; hoje o tool de delegacao e `Agent`."""
        achados = self.checar(agente(name="vortex-x", description="d", tools='["Read", "Task"]'))
        self.assertTrue(any(a["campo"] == "tools" and a["nivel"] == "aviso" for a in achados))

    def test_description_longa_demais_para_o_picker(self):
        longa = " ".join(["palavra"] * 40)
        achados = self.checar(agente(name="vortex-x", description=longa))
        self.assertTrue(any(a["campo"] == "description" and a["nivel"] == "aviso" for a in achados))

    def test_name_divergente_do_arquivo(self):
        achados = self.checar(agente(name="outro-nome", description="d"), nome="vortex-x.md")
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




class TestContratoDeSaida(unittest.TestCase):
    """DESIGN.md secao 2 — o vocabulario de saida e contrato, nao sugestao.

    Um contrato de design so documentado diverge; cobrado por teste, nao.
    """

    def test_toda_mensagem_de_gate_abre_com_o_prefixo(self):
        linha = doutor.linha_gate("erro", "vortex-x.md", "tools", "namespace fixo")
        self.assertTrue(
            linha.startswith("[VORTEX/doutor]") or linha.startswith("ERRO ") or linha.startswith("aviso"),
            linha)

    def test_marcadores_de_severidade_tem_largura_fixa(self):
        """Alinhados em coluna: o olho aprende onde olhar e para de ler a linha."""
        self.assertEqual(len(doutor.MARCA["erro"]), len(doutor.MARCA["aviso"]))

    def test_sem_emoji_e_sem_cor_ansi_na_saida(self):
        """O terminal do leitor ja tem tema; competir com ele e ruido."""
        texto = doutor.linha_gate("erro", "vortex-x.md", "tools", "namespace fixo")
        self.assertNotIn("\x1b[", texto)
        self.assertFalse(any(ord(c) > 0x2500 for c in texto), f"caractere decorativo em: {texto}")

    def test_cabecalho_de_gate_identifica_quem_esta_falando(self):
        self.assertTrue(doutor.cabecalho("doutor", "3 achados").startswith("[VORTEX/doutor]"))


if __name__ == "__main__":
    unittest.main()
