"""Testes de gate_despacho.py — impede redespachar task ja concluida.

A `vortex-subagentes` chama isso de "o erro mais caro observado": um controlador
que, depois de uma compactacao, rechama sequencias inteiras de tasks ja
feitas. O `contexto.py` ja reancora o ledger, mas reancorar e conselho; este
gate e mecanismo.

O caso mais importante da matriz e o 10: o brief tem precedencia sobre a
prosa. Um brief da Task 5 cujo texto menciona "consome o que a Task 3
produziu" NAO pode ser bloqueado por causa da Task 3.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gate_despacho  # noqa: E402


def setUpModule():
    """Isola o log de erros do diretorio de producao (ver test_comum)."""
    os.environ["CLAUDE_PLUGIN_DATA"] = tempfile.mkdtemp(prefix="vortex-testes-")

LEDGER = """# Progresso

Task 1: concluída (commits aaa1111..bbb2222, revisão limpa)
Task 3: concluída (commits bbb2222..ccc3333, revisão limpa)
Task 4: em andamento
"""


def projeto(ledger=LEDGER):
    d = Path(tempfile.mkdtemp())
    if ledger is not None:
        p = d / ".vortex/sdd/progress.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(ledger, encoding="utf-8")
    return d


def despacho(prompt, subagent_type="vortex-implementador", tool_name="Agent", raiz=None):
    return {
        "tool_name": tool_name,
        "tool_input": {"prompt": prompt, "subagent_type": subagent_type},
        "cwd": str(raiz or projeto()),
        "hook_event_name": "PreToolUse",
    }


def decidir(entrada, nivel="block"):
    bruto = gate_despacho.responder(entrada, nivel)
    if bruto is None:
        return "allow"
    return json.loads(bruto)["hookSpecificOutput"]["permissionDecision"]


class TestMatriz(unittest.TestCase):
    def test_01_tool_que_nao_e_despacho_e_ignorada(self):
        e = despacho("qualquer coisa")
        e["tool_name"] = "Bash"
        self.assertIsNone(gate_despacho.responder(e, "block"))

    def test_02_ledger_ausente_libera(self):
        r = projeto(ledger=None)
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-3-brief.md", raiz=r)), "allow")

    def test_03_redespacho_de_task_concluida_e_negado(self):
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-3-brief.md")), "deny")

    def test_04_nivel_warn_pergunta(self):
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-3-brief.md"), "warn"), "ask")

    def test_05_nivel_off_libera(self):
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-3-brief.md"), "off"), "allow")

    def test_06_task_nao_concluida_passa(self):
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-4-brief.md")), "allow")

    def test_07_revisor_sobre_task_concluida_passa(self):
        """Re-revisao e legitima: o gate e sobre implementacao, nao sobre leitura."""
        self.assertEqual(decidir(despacho("revise task-3", subagent_type="vortex-revisor")), "allow")

    def test_08_especialista_tambem_e_implementador(self):
        self.assertEqual(
            decidir(despacho("leia .vortex/sdd/tasks/task-3-brief.md", subagent_type="vortex-dev-frontend")),
            "deny")

    def test_09_prompt_sem_numero_de_task_passa(self):
        """Nunca adivinha. Sem sinal explicito, libera."""
        self.assertEqual(decidir(despacho("implemente o que discutimos")), "allow")

    def test_10_brief_tem_precedencia_sobre_a_prosa(self):
        """O falso positivo critico: citar uma task concluida como dependencia."""
        p = ("leia .vortex/sdd/tasks/task-5-brief.md — ela consome o que a Task 3 produziu "
             "e estende o comportamento da Task 1")
        self.assertEqual(decidir(despacho(p)), "allow")

    def test_11_fronteira_de_numero(self):
        """Ledger tem Task 1; Task 10 e outra task."""
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-10-brief.md")), "allow")

    def test_12_subtask_nao_e_a_task_pai(self):
        r = projeto("Task 3.2: concluída (commits x..y, revisão limpa)\n")
        self.assertEqual(decidir(despacho("leia .vortex/sdd/tasks/task-3-brief.md", raiz=r)), "allow")

    def test_13_prosa_sem_brief_ainda_vale_para_implementador(self):
        self.assertEqual(decidir(despacho("refaça a Task 3 por favor")), "deny")

    def test_14_ledger_ilegivel_libera(self):
        d = Path(tempfile.mkdtemp())
        p = d / ".vortex/sdd/progress.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"\xff\xfe binario invalido")
        self.assertEqual(decidir(despacho("leia task-3-brief.md", raiz=d)), "allow")

    def test_15_entrada_vazia_nao_quebra(self):
        self.assertIsNone(gate_despacho.responder({}, "block"))
        self.assertIsNone(gate_despacho.responder({"tool_name": "Agent"}, "block"))


class TestMensagem(unittest.TestCase):
    def test_segue_o_contrato_de_saida(self):
        bruto = gate_despacho.responder(despacho("leia .vortex/sdd/tasks/task-3-brief.md"), "block")
        motivo = json.loads(bruto)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertTrue(motivo.startswith("[VORTEX/ledger]"), motivo)
        self.assertIn("3", motivo)
        self.assertIn(".vortex/config.json", motivo)

    def test_saida_e_um_unico_documento_de_uma_linha(self):
        bruto = gate_despacho.responder(despacho("leia .vortex/sdd/tasks/task-3-brief.md"), "block")
        json.loads(bruto)
        self.assertEqual(bruto.count("\n"), 0)

    def test_reusa_o_parser_do_contexto(self):
        """Duas fontes de verdade sobre 'o que e uma task concluida' divergem."""
        fonte = Path(gate_despacho.__file__).read_text(encoding="utf-8")
        self.assertIn("contexto", fonte)


if __name__ == "__main__":
    unittest.main()
