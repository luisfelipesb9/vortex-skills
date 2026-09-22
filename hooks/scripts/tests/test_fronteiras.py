"""Testes de fronteiras.py — o unico gate da v1 que bloqueia.

A matriz abaixo e o contrato. Falso positivo aqui trava trabalho legitimo;
falso negativo deixa passar acao irreversivel. Os dois custam, e por isso
cada caso esta escrito explicitamente em vez de coberto por regra geral.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fronteiras  # noqa: E402


def decidir(comando, nivel="block"):
    return fronteiras.avaliar(comando, nivel)


class TestNegar(unittest.TestCase):
    """O repo diz 'nunca faz merge', nao 'pergunte antes de fazer merge'."""

    CASOS = [
        ("git merge main", "merge"),
        ("git merge --no-ff feature/x", "merge"),
        ("cd subdir && git merge x", "merge em comando composto"),
        ("git -C pacote merge main", "merge com -C"),
        ("git push --force origin feature", "force-push"),
        ("git push -f origin feature", "force-push com -f"),
        ("git push --force-with-lease origin main", "force-push com lease"),
        ("git push origin main", "push em branch protegida"),
        ("git push origin master", "push em master"),
        ("gh pr merge 42 --squash", "merge de PR"),
        ("git reset --hard origin/main", "reset --hard contra remoto"),
    ]

    def test_casos_negados(self):
        for comando, rotulo in self.CASOS:
            with self.subTest(rotulo):
                self.assertEqual(decidir(comando)[0], "deny", comando)


class TestPerguntar(unittest.TestCase):
    """Irreversivel ou externo para no humano — `ask` entrega a decisao a ele."""

    CASOS = [
        ("vercel --prod", "deploy de producao"),
        ("flyctl deploy", "deploy"),
        ("terraform apply", "mudanca de infra"),
        ("terraform destroy -auto-approve", "destruicao de infra"),
        ("kubectl delete pod meu-pod", "mudanca em cluster"),
        ("gh secret set API_KEY", "secrets"),
        ("aws s3 rm s3://bucket --recursive", "recurso de nuvem"),
        ("rm -rf ~/projetos", "remocao destrutiva"),
        ("docker system prune -a", "prune destrutivo"),
    ]

    def test_casos_perguntados(self):
        for comando, rotulo in self.CASOS:
            with self.subTest(rotulo):
                self.assertEqual(decidir(comando)[0], "ask", comando)


class TestLiberar(unittest.TestCase):
    """Falso positivo trava trabalho legitimo — estes TEM que passar."""

    CASOS = [
        ("git merge --abort", "abortar merge e recuperacao, nao merge"),
        ("git push origin feature/nova-tela", "push em branch de feature"),
        ("git push -u origin minha-branch", "push com upstream"),
        ("git status", "leitura"),
        ("git log --oneline -20", "leitura"),
        ("git diff --cached", "leitura"),
        ('echo "nunca use git merge aqui"', "mencao em echo"),
        ("terraform plan", "plan nao aplica"),
        ("kubectl get pods", "leitura de cluster"),
        ("npm test", "suite de teste"),
        ("rm -rf node_modules", "limpeza local comum"),
        ("rm -rf ./build", "limpeza de artefato"),
        ("gh pr create --fill", "abrir PR e o caminho desejado"),
        ("git commit -m 'feat: x'", "commit"),
    ]

    def test_casos_liberados(self):
        for comando, rotulo in self.CASOS:
            with self.subTest(rotulo):
                self.assertEqual(decidir(comando)[0], "allow", comando)


class TestNiveis(unittest.TestCase):
    def test_off_libera_tudo(self):
        self.assertEqual(decidir("git push --force origin main", "off")[0], "allow")

    def test_warn_rebaixa_deny_para_ask_e_ask_para_allow(self):
        self.assertEqual(decidir("git merge main", "warn")[0], "ask")
        self.assertEqual(decidir("vercel --prod", "warn")[0], "allow")


class TestMensagem(unittest.TestCase):
    def test_segue_o_contrato_de_saida_do_design(self):
        _, motivo = decidir("git merge main")
        self.assertTrue(motivo.startswith("[JET/fronteiras]"), motivo)

    def test_diz_o_que_fazer_e_como_desligar(self):
        _, motivo = decidir("git merge main")
        self.assertIn("gh pr create", motivo)
        self.assertIn(".jet/config.json", motivo)

    def test_saida_json_e_um_unico_documento_de_uma_linha(self):
        bruto = fronteiras.responder({"tool_name": "Bash", "tool_input": {"command": "git merge main"}}, "block")
        json.loads(bruto)
        self.assertEqual(bruto.count("\n"), 0)

    def test_comando_liberado_nao_produz_saida(self):
        """Silencio e a resposta certa: o hook so fala quando tem algo a dizer."""
        self.assertIsNone(
            fronteiras.responder({"tool_name": "Bash", "tool_input": {"command": "git status"}}, "block"))


class TestRobustez(unittest.TestCase):
    def test_entrada_sem_comando_nao_quebra(self):
        self.assertIsNone(fronteiras.responder({"tool_name": "Bash", "tool_input": {}}, "block"))
        self.assertIsNone(fronteiras.responder({}, "block"))

    def test_conteudo_do_comando_nunca_e_executado(self):
        """O script faz regex sobre entrada de terceiros. Zero eval, zero shell."""
        fonte = Path(fronteiras.__file__).read_text(encoding="utf-8")
        for proibido in ("eval(", "exec(", "shell=True", "os.system", "subprocess"):
            self.assertNotIn(proibido, fonte, f"{proibido} no caminho de dados nao-confiaveis")


if __name__ == "__main__":
    unittest.main()
