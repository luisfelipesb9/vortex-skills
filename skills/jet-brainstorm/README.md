# jet-brainstorm

> Skill que transforma uma ideia em design aprovado pelo usuário, antes de qualquer linha de código.

## O que faz

Conduz, em diálogo natural, a passagem de uma ideia solta para um spec de design pronto para virar plano de implementação. Explora o contexto do projeto, faz perguntas de esclarecimento uma de cada vez, propõe 2-3 abordagens com trade-offs e valida o design em seções com o usuário antes de escrever o spec final.

## Quando usar

- "quero criar/adicionar/mudar algo no produto", "vamos construir uma feature".
- Início de qualquer projeto ou pedido de mudança de comportamento — inclusive os que parecem simples (uma lista de tarefas, uma função utilitária, uma mudança de config).
- Sempre ANTES de qualquer trabalho criativo: criar features, construir componentes, adicionar funcionalidade.

## Como funciona

1. Explora o contexto atual do projeto (arquivos, docs, commits recentes).
2. Faz perguntas de esclarecimento uma de cada vez, buscando propósito, restrições e critérios de sucesso.
3. Propõe 2-3 abordagens com trade-offs e uma recomendação clara.
4. Apresenta o design em seções proporcionais à complexidade, pedindo validação a cada uma.
5. Escreve o spec em arquivo, faz commit e roda uma autorrevisão (placeholders, contradições, ambiguidade, escopo).
6. Pede que o usuário revise o spec escrito — só segue adiante com aprovação explícita.
7. Estado terminal: invoca a skill `jet-plano`. Nenhuma skill de implementação é acionada antes da aprovação do usuário.

## Instalação

Claude Code — copie a pasta para o diretório de skills do seu ambiente:

```bash
cp -r skills/jet-brainstorm ~/.claude/skills/
```

## Exemplo

"Quero adicionar um sistema de notificações por e-mail" → a skill explora o projeto, faz perguntas uma de cada vez, propõe abordagens, escreve e commita o spec, pede a revisão do usuário e só então aciona a `jet-plano`.
