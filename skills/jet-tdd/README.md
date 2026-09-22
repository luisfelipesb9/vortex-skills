# jet-tdd

> Skill que impõe o ciclo RED → GREEN → REFACTOR → commit em qualquer mudança de código.

## O que faz

Define o padrão de Test-Driven Development do time de agentes da JET: teste primeiro, ver falhar pelo motivo certo, implementação mínima para passar, refactor mantendo tudo verde, commit. Traz exemplos de bom/mau teste, uma tabela de racionalizações comuns para pular TDD ("é simples demais", "testo depois") e um checklist de verificação antes de fechar a tarefa.

## Quando usar

- "implementa isso", "corrige esse bug", "adiciona essa funcionalidade".
- Início de qualquer tarefa de código do time de agentes da JET (`jet-implementador`, `jet-dev-backend`, `jet-dev-frontend`, `jet-dev-dados`).
- Não usar em protótipos descartáveis, código gerado automaticamente ou arquivos de configuração puros — nesses casos, confirme antes com o humano.

## Como funciona

1. **RED** — escreve um teste mínimo que descreve o comportamento esperado, com nome claro e código real (mock só se inevitável).
2. **Verificar RED** — roda o teste e confirma que falha pelo motivo certo, não por erro de digitação.
3. **GREEN** — escreve o código mais simples possível para passar, sem adicionar nada que o teste não pede.
4. **Verificar GREEN** — roda a suíte inteira e confirma saída limpa, sem quebrar outros testes.
5. **REFACTOR** — limpa duplicação e nomes mantendo os testes verdes, sem introduzir comportamento novo.
6. **Commit** — fecha o ciclo com Conventional Commits e volta ao passo 1 para a próxima fatia de comportamento.

## Instalação

Claude Code — copie a pasta para o diretório de skills do seu ambiente:

```bash
cp -r skills/jet-tdd ~/.claude/skills/
```

## Exemplo

"Corrige o bug do e-mail vazio aceito no formulário" → a skill escreve um teste que falha reproduzindo o bug, vê o RED, implementa a validação mínima, vê o GREEN e só então comita.
