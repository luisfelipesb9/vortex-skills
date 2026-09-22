---
description: Le o ledger de progresso e cruza com o git log — diz qual e a proxima task nao concluida.
argument-hint: "[status|proxima|reconstruir]"
allowed-tools: Read, Bash(git log:*), Bash(git rev-parse:*), Bash(cat:*), Write
when_to_use: Depois de uma compactacao, ao retomar uma sessao, ou antes de despachar qualquer task de um plano.
---

Ledger em `.jet/sdd/progress.md` (ou o caminho em `JET_LEDGER_PATH`).

**`status`** (padrao) — leia o ledger e `git log --oneline -20`. Reporte: tasks concluídas, a próxima não marcada, e qualquer divergência entre ledger e git (linha de task concluída cujo range de commits não existe, ou commits de task que o ledger não registra).

**`proxima`** — responda só com a próxima task não marcada. Uma linha.

**`reconstruir`** — o ledger sumiu ou está incompleto. Reconstrua a partir do `git log`: cada commit que fecha uma task vira uma linha `Task N: concluída (commits <base7>..<head7>, revisão limpa)`. Onde não der para inferir o número da task, escreva o que dá e **marque a linha como inferida** — nunca invente um range de commits.

Regra que não se quebra: task marcada como concluída **está** concluída. Não redespache. Se o humano quer reabrir, ele pede e o ledger é editado primeiro.
