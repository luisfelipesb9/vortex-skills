# jet-plano

> Skill que transforma um spec aprovado em plano de implementação bite-sized, pronto para execução por subagentes.

## O que faz

Pega o design/spec aprovado (saída da `jet-brainstorm`) e escreve um plano de implementação completo — arquivos exatos a tocar, código de teste, comandos e critérios de sucesso — assumindo que quem executa não conhece a base de código. Divide o trabalho em tarefas pequenas (bite-sized), cada uma com seu próprio ciclo TDD e commit, sem placeholders nem passos vagos.

## Quando usar

- "temos o spec, agora precisamos do plano", "como vamos dividir isso em tarefas", "gera o plano de implementação".
- Você tem um spec ou requisitos definidos para uma tarefa multi-etapas, antes de tocar em código.

## Como funciona

1. Confere se o spec cobre mais de um subsistema independente — se sim, sugere quebrar em planos separados (um por subsistema).
2. Mapeia a estrutura de arquivos: o que será criado ou modificado e a responsabilidade de cada um.
3. Decompõe o trabalho em tarefas bite-sized, cada uma com passos de 2-5 minutos (teste que falha → rodar → implementar → rodar → commit).
4. Escreve o plano completo com o cabeçalho obrigatório apontando para `jet-subagentes`, sem placeholders ("TBD", "tratar depois", "similar à Tarefa N").
5. Roda uma autorrevisão contra o spec — cobertura de requisito, varredura de placeholder, consistência de tipos/nomes entre tarefas — e corrige inline.
6. Estado terminal: entrega o plano salvo em arquivo e recomenda a skill `jet-subagentes` para a execução.

## Instalação

Claude Code — copie a pasta para o diretório de skills do seu ambiente:

```bash
cp -r skills/jet-plano ~/.claude/skills/
```

## Exemplo

"Temos o spec do sistema de notificações, vamos gerar o plano" → a skill mapeia os arquivos, quebra o trabalho em tarefas com teste e commit já definidos, e entrega o plano pronto para a `jet-subagentes` executar.
