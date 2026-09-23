# vortex-subagentes

> Skill que executa um plano de implementação despachando um subagente por tarefa, com revisão em cada gate.

## O que faz

Executa um plano de implementação tarefa por tarefa, despachando um subagente implementador novo (contexto isolado, sem herdar o histórico da sessão) para cada uma, seguido de uma revisão de spec + qualidade antes de avançar para a próxima. Termina com uma revisão ampla de toda a branch antes da integração. Escolhe o modelo pelo tamanho e risco de cada tarefa — o mais barato para trabalho mecânico, o mais capaz para arquitetura e revisão final.

## Quando usar

- "executa esse plano", "vamos implementar as tasks", "roda o plano com subagentes".
- Existe um plano de implementação pronto (por exemplo, produzido pela `vortex-plano`) com tarefas majoritariamente independentes entre si, na mesma sessão.

## Como funciona

1. Lê o plano inteiro uma vez, checando conflitos e contradições com as Restrições Globais antes de despachar a primeira tarefa (pré-voo).
2. Para cada tarefa: extrai o brief para um arquivo próprio e despacha o `vortex-implementador` com o brief + contexto — nunca o plano inteiro.
3. Trata o status devolvido (CONCLUIDO, CONCLUIDO_COM_RESSALVAS, FALTA_CONTEXTO ou BLOQUEADO) antes de seguir adiante.
4. Monta o diff da tarefa e despacha o `vortex-revisor`, que devolve dois vereditos — conformidade com o spec e qualidade de código/segurança.
5. Se algum veredito reprovar, despacha uma correção e revisa de novo; só marca a tarefa concluída no ledger de progresso quando os dois vierem aprovados.
6. Estado terminal: depois de todas as tarefas, despacha uma revisão final de toda a branch e segue para a integração conforme o fluxo do projeto — nunca inicia implementação na branch principal sem consentimento explícito do humano, e nunca mergeia sozinha.

## Exemplo

"Roda o plano de notificações com subagentes" → a skill despacha um `vortex-implementador` por tarefa, revisa cada diff com `vortex-revisor`, resolve os achados e fecha com uma revisão final de toda a branch antes do merge.
