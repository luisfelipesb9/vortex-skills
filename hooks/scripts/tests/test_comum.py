"""Testes de _comum.py — descoberta de projeto, niveis e saida de hook.

Roda sem dependencia externa:  python3 -m unittest discover -s hooks/scripts/tests
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _comum  # noqa: E402


class TestDescobrirComandoTeste(unittest.TestCase):
    """O hook nunca pode hardcodar `npm test` — ele descobre pelo manifesto."""

    def projeto(self, arquivos):
        d = Path(tempfile.mkdtemp())
        for nome, conteudo in arquivos.items():
            p = d / nome
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(conteudo)
        return d

    def test_node_com_script_test_usa_o_package_manager_do_lockfile(self):
        d = self.projeto({
            "package.json": json.dumps({"scripts": {"test": "vitest"}}),
            "pnpm-lock.yaml": "",
        })
        self.assertEqual(_comum.descobrir_comando_teste(d), "pnpm test")

    def test_node_sem_lockfile_cai_para_npm(self):
        d = self.projeto({"package.json": json.dumps({"scripts": {"test": "jest"}})})
        self.assertEqual(_comum.descobrir_comando_teste(d), "npm test")

    def test_node_sem_script_test_nao_conta_como_suite(self):
        d = self.projeto({"package.json": json.dumps({"scripts": {"build": "tsc"}})})
        self.assertIsNone(_comum.descobrir_comando_teste(d))

    def test_python_com_pytest_configurado(self):
        d = self.projeto({"pyproject.toml": "[tool.pytest.ini_options]\n"})
        self.assertEqual(_comum.descobrir_comando_teste(d), "pytest")

    def test_python_com_uv_lock_prefixa_uv_run(self):
        d = self.projeto({"pyproject.toml": "[tool.pytest.ini_options]\n", "uv.lock": ""})
        self.assertEqual(_comum.descobrir_comando_teste(d), "uv run pytest")

    def test_go_e_rust(self):
        self.assertEqual(_comum.descobrir_comando_teste(self.projeto({"go.mod": "module x"})), "go test ./...")
        self.assertEqual(_comum.descobrir_comando_teste(self.projeto({"Cargo.toml": "[package]"})), "cargo test")

    def test_config_do_projeto_sempre_vence_o_sniff(self):
        d = self.projeto({
            "package.json": json.dumps({"scripts": {"test": "jest"}}),
            ".jet/config.json": json.dumps({"test_command": "make prova"}),
        })
        self.assertEqual(_comum.descobrir_comando_teste(d), "make prova")

    def test_projeto_sem_suite_devolve_none(self):
        """Repo de conteudo/documentacao: os gates precisam se desligar sozinhos."""
        d = self.projeto({"README.md": "# doc", "notas.md": "texto"})
        self.assertIsNone(_comum.descobrir_comando_teste(d))


class TestNivel(unittest.TestCase):
    """Precedencia: .jet/config.json > env > argumento (userConfig) > default."""

    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        for k in list(os.environ):
            if k.startswith("JET_NIVEL_"):
                del os.environ[k]

    def test_default_quando_nada_definido(self):
        self.assertEqual(_comum.resolver_nivel("fronteiras", None, self.d), "block")
        self.assertEqual(_comum.resolver_nivel("tdd", None, self.d), "off")

    def test_argumento_vence_o_default(self):
        self.assertEqual(_comum.resolver_nivel("fronteiras", "warn", self.d), "warn")

    def test_env_vence_o_argumento(self):
        os.environ["JET_NIVEL_FRONTEIRAS"] = "off"
        self.assertEqual(_comum.resolver_nivel("fronteiras", "block", self.d), "off")

    def test_config_do_projeto_vence_tudo(self):
        os.environ["JET_NIVEL_FRONTEIRAS"] = "off"
        (self.d / ".jet").mkdir(parents=True, exist_ok=True)
        (self.d / ".jet/config.json").write_text(json.dumps({"niveis": {"fronteiras": "warn"}}))
        self.assertEqual(_comum.resolver_nivel("fronteiras", "block", self.d), "warn")

    def test_valor_invalido_nunca_escala_severidade(self):
        """Um valor errado cai no default; nunca vira block por acidente."""
        self.assertEqual(_comum.resolver_nivel("tdd", "bloqueia-tudo", self.d), "off")

    def test_placeholder_nao_substituido_cai_no_default(self):
        """Se o runtime nao expandir ${user_config.X}, o literal chega no script."""
        self.assertEqual(_comum.resolver_nivel("fronteiras", "${user_config.JET_NIVEL_FRONTEIRAS}", self.d), "block")


class TestSaidaDeHook(unittest.TestCase):
    """O contrato de saida do PreToolUse, exatamente como o Claude Code espera."""

    def test_negar_produz_permission_decision_deny(self):
        s = json.loads(_comum.saida_pretooluse("deny", "motivo"))
        self.assertEqual(s["hookSpecificOutput"]["hookEventName"], "PreToolUse")
        self.assertEqual(s["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(s["hookSpecificOutput"]["permissionDecisionReason"], "motivo")

    def test_perguntar_produz_ask(self):
        s = json.loads(_comum.saida_pretooluse("ask", "confirma?"))
        self.assertEqual(s["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_saida_e_um_unico_documento_json(self):
        """Varios documentos JSON fazem o Claude Code tratar a saida como texto puro."""
        bruto = _comum.saida_pretooluse("deny", 'motivo com "aspas" e \n quebra')
        json.loads(bruto)
        self.assertEqual(bruto.count("\n"), 0)


class TestFailOpen(unittest.TestCase):
    """Um hook que nega quando ele proprio quebra e pior que nao ter hook."""

    def test_excecao_no_corpo_nao_bloqueia_e_sai_zero(self):
        def explode(_entrada):
            raise RuntimeError("bug no script")

        with self.assertRaises(SystemExit) as ctx:
            _comum.executar(explode, entrada_bruta='{"tool_name":"Bash"}')
        self.assertEqual(ctx.exception.code, 0)

    def test_stdin_invalido_nao_bloqueia(self):
        with self.assertRaises(SystemExit) as ctx:
            _comum.executar(lambda e: None, entrada_bruta="isso nao e json")
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
