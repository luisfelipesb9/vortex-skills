"""Testes de contexto.py — reancoragem do ledger em SessionStart e PostCompact.

A vortex-subagentes diz que o erro mais caro observado foi controlador
redespachando tasks ja concluidas depois de uma compactacao. Memoria de
conversa nao sobrevive a compactacao; disco sobrevive. Este hook reancora.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contexto  # noqa: E402

LEDGER = """# Progresso

Task 1: concluída (commits a1b2c3d..e4f5g6h, revisão limpa)
Task 2: concluída (commits e4f5g6h..i7j8k9l, revisão limpa)
Task 3: em andamento
Task 4: não iniciada
"""


class TestLerLedger(unittest.TestCase):
    def projeto(self, ledger=LEDGER, caminho=".vortex/sdd/progress.md"):
        d = Path(tempfile.mkdtemp())
        if ledger is not None:
            p = d / caminho
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(ledger, encoding="utf-8")
        return d

    def test_lista_as_tasks_concluidas(self):
        self.assertEqual(contexto.tasks_concluidas(LEDGER), ["1", "2"])

    def test_task_em_andamento_nao_conta_como_concluida(self):
        self.assertNotIn("3", contexto.tasks_concluidas(LEDGER))

    def test_ledger_vazio_ou_ausente_nao_quebra(self):
        self.assertEqual(contexto.tasks_concluidas(""), [])
        self.assertIsNone(contexto.montar(self.projeto(ledger=None), "SessionStart"))

    def test_reconhece_variacoes_de_escrita(self):
        for linha in ("Task 5: concluída", "- Task 5: concluida", "* Task 5 : CONCLUÍDA"):
            self.assertIn("5", contexto.tasks_concluidas(linha), linha)


class TestMontarContexto(unittest.TestCase):
    def projeto(self):
        d = Path(tempfile.mkdtemp())
        p = d / ".vortex/sdd/progress.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(LEDGER, encoding="utf-8")
        return d

    def test_diz_quais_tasks_nao_redespachar(self):
        texto = contexto.montar(self.projeto(), "SessionStart")
        self.assertIn("1", texto)
        self.assertIn("2", texto)
        self.assertIn("nao redespache", texto.lower().replace("ã", "a").replace("ç", "c"))

    def test_segue_o_contrato_de_saida(self):
        self.assertTrue(contexto.montar(self.projeto(), "SessionStart").startswith("[VORTEX/ledger]"))

    def test_saida_json_e_do_evento_certo(self):
        for evento in ("SessionStart", "PostCompact"):
            bruto = contexto.responder({"hook_event_name": evento, "cwd": str(self.projeto())})
            dados = json.loads(bruto)
            self.assertEqual(dados["hookSpecificOutput"]["hookEventName"], evento)
            self.assertIn("additionalContext", dados["hookSpecificOutput"])

    def test_nunca_bloqueia(self):
        """Este hook so injeta contexto. Nao existe caminho que impeca nada."""
        fonte = Path(contexto.__file__).read_text(encoding="utf-8")
        for proibido in ('"deny"', '"block"', '"decision"', "permissionDecision"):
            self.assertNotIn(proibido, fonte, f"{proibido} num hook que deveria so injetar")

    def test_subagente_nao_recebe_reancoragem(self):
        """O ledger e contexto do controlador; subagente recebe o brief dele."""
        entrada = {"hook_event_name": "SessionStart", "cwd": str(self.projeto()), "agent_id": "ag_7f"}
        self.assertIsNone(contexto.responder(entrada))


if __name__ == "__main__":
    unittest.main()
