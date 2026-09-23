---
description: Executa um plano de implementacao com a skill vortex-subagentes, conduzido pelo vortex-maestro.
argument-hint: "<caminho-do-plano.md>"
agent: vortex-maestro
context: fork
---

Execute o plano em `$ARGUMENTS` seguindo a skill `vortex-subagentes`.

Antes de despachar a Task 1:

1. Leia o ledger (`/vortex-ledger status`). Task já marcada como concluída **não** é redespachada.
2. Leia o plano inteiro uma vez procurando conflitos entre tasks ou com as Restrições Globais. Se achar, apresente tudo ao humano em uma pergunta só, antes de começar.

Depois, para cada task: extraia o brief para arquivo, despache o agente do campo `Agente` da task (sem campo: `vortex-implementador`), monte o pacote de diff com `/vortex-diff`, despache o `vortex-revisor`, e só marque a task no ledger quando os dois vereditos vierem aprovados.

Roda em contexto forkado para o loop autônomo não poluir a sessão do humano.
