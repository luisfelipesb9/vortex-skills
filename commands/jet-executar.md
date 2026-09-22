---
description: Executa um plano de implementacao com a skill jet-subagentes, conduzido pelo jet-maestro.
argument-hint: "<caminho-do-plano.md>"
agent: jet-maestro
context: fork
---

Execute o plano em `$ARGUMENTS` seguindo a skill `jet-subagentes`.

Antes de despachar a Task 1:

1. Leia o ledger (`/jet-ledger status`). Task já marcada como concluída **não** é redespachada.
2. Leia o plano inteiro uma vez procurando conflitos entre tasks ou com as Restrições Globais. Se achar, apresente tudo ao humano em uma pergunta só, antes de começar.

Depois, para cada task: extraia o brief para arquivo, despache o agente do campo `Agente` da task (sem campo: `jet-implementador`), monte o pacote de diff com `/jet-diff`, despache o `jet-revisor`, e só marque a task no ledger quando os dois vereditos vierem aprovados.

Roda em contexto forkado para o loop autônomo não poluir a sessão do humano.
