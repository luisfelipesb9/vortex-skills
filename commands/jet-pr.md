---
description: Abre o PR de entrega de uma branch, com o corpo montado a partir do spec, do plano, do ledger e da revisao final.
argument-hint: "[base-branch]"
allowed-tools: Bash(git push:*), Bash(git log:*), Bash(git status:*), Bash(git rev-parse:*), Bash(git symbolic-ref:*), Bash(gh auth status:*), Bash(gh pr create:*), Bash(gh pr view:*), Read, Write
when_to_use: Quando a execucao de um plano terminou e a branch precisa virar PR — tipicamente depois de /jet-executar, que para antes deste passo por rodar em contexto forkado.
---

Abra o PR de entrega desta branch. Siga a seção **Fechamento — abrir o PR** da skill `jet-subagentes` — este comando é a reentrada manual do mesmo procedimento, não um caminho paralelo.

**Pré-checagens, nesta ordem. Aborte com o motivo em uma linha se alguma falhar:**

1. A branch atual não é a default (`git symbolic-ref refs/remotes/origin/HEAD`). Se for, pare: o trabalho deveria estar numa branch de feature.
2. `git status` limpo. Mudança não commitada não entra no PR e some do relato.
3. `gh auth status` ok.
4. Ledger (`.jet/sdd/progress.md`) sem task não marcada. Se houver, **avise quais e pergunte** antes de seguir — PR parcial é uma decisão legítima, mas tem que ser consciente.
5. A revisão final de branch aconteceu. Se não houver registro dela, despache o `jet-revisor` com o range completo antes de abrir.

**Depois:** `git push -u origin <branch>`, monte o corpo a partir do que está em disco (spec, plano, linhas do ledger com os ranges de commit, vereditos da revisão final, Menores não corrigidos, comando de teste e resultado da última verificação), mostre ao humano, e só então `gh pr create`.

Registre `PR aberto: <url>` como última linha do ledger.

Nunca `gh pr merge` — o gate de fronteiras nega, e o merge é do humano.
