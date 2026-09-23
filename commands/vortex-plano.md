---
description: Transforma um spec aprovado em plano de implementacao bite-sized pela skill vortex-plano.
argument-hint: "[caminho-do-spec.md]"
when_to_use: Quando ja existe um spec aprovado e o proximo passo e o plano — tipicamente automatico depois do brainstorm, mas necessario quando a sessao foi interrompida entre as duas etapas.
---

Invoque a skill `vortex-plano` para o spec em **$ARGUMENTS** (sem argumento: o spec mais recente em `.vortex/sdd/specs/`).

Normalmente você não precisa deste comando — o estado terminal da `vortex-brainstorm` já é invocar a `vortex-plano`. Ele existe para o caso em que a sessão foi interrompida entre as duas etapas e o spec já está aprovado em disco.

**Antes de planejar, confirme que o spec foi de fato aprovado pelo humano.** Spec escrito não é spec aprovado; planejar sobre um design não validado só empurra o retrabalho para a Task 7.
