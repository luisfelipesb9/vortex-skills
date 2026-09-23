# vortex-verificacao

> Skill que exige evidência de verificação fresca antes de qualquer alegação de "pronto".

## O que faz

Bloqueia qualquer alegação de conclusão, correção ou sucesso — própria ou de um subagente — até que o comando que prova essa alegação tenha rodado nesta mensagem e o output tenha sido lido de fato. Cobre testes, build, linter, correção de bug e checagem de requisito contra o relatório de um subagente, com tabelas de falhas comuns e racionalizações a evitar.

## Quando usar

- Antes de fazer commit, abrir PR, marcar uma task como concluída no rastreador, ou confiar no relatório de um subagente.
- Em qualquer variação de "terminei", "deve funcionar agora", "os testes passam", "corrigi o bug", "pronto para merge".
- Antes de qualquer expressão de satisfação ("ótimo!", "perfeito!") — a satisfação vem depois de rodar o comando que prova a alegação, nunca antes.

## Como funciona

1. Identifica qual comando prova a alegação específica sendo feita (teste, build, linter, diff do VCS).
2. Roda esse comando completo, fresco, sem atalho e sem reaproveitar rodada anterior.
3. Lê o output completo — código de saída, contagem de falhas, mensagens de erro.
4. Compara o output com a alegação: se não confirma, declara o estado real e a lacuna encontrada.
5. Só então faz a alegação, sempre acompanhada da evidência que a sustenta.

## Exemplo

Um subagente reporta "task concluída, testes passam" → a skill exige rodar o comando de teste de novo e conferir o diff do VCS antes de aceitar o relatório como fato.
