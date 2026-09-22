---
description: Gera o pacote de diff de uma task (log + stat + diff -U10) em arquivo e devolve so o caminho.
argument-hint: "<base-ref> [nome-da-task]"
allowed-tools: Bash(git log:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(mkdir:*), Write
context: fork
---

Gere o pacote de revisão de uma task em `.jet/sdd/diffs/<task>.diff` e devolva **apenas o caminho**.

```bash
mkdir -p .jet/sdd/diffs
{ git log --oneline "$1..HEAD"; echo; git diff --stat "$1...HEAD"; echo; git diff -U10 "$1...HEAD"; } > .jet/sdd/diffs/${2:-task}.diff
```

Valide antes: que `$1` resolve (`git rev-parse`) e que o diff não está vazio. Use three-dot (`base...HEAD`), contra o merge-base — two-dot traz ruído da main.

Este comando roda em contexto forkado de propósito: o `git diff -U10` inteiro **não** encosta no contexto de quem pediu. É esse o ponto. O revisor recebe o caminho, não o conteúdo.

Nunca use `HEAD~1` como base: trunca silenciosamente qualquer task com mais de um commit.
