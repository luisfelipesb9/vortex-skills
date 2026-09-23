# vortex-fluxo

> Skill meta: responde como operar o time, não executa trabalho de produto.

## O que faz

Entrega a tabela de decisão ("quero X → uso Y"), a separação entre o que é garantido por máquina e o
que é convenção, e os sintomas mais comuns com a ação correspondente. Para o detalhe narrado —
setup, feature nova, bugfix, entrega de agência, retomada após compactação — ela aponta para o
[RUNBOOK](../RUNBOOK.md).

## Quando usar

- "como eu uso isso?", "qual o próximo passo?", "o que faço agora?"
- "por que esse gate bloqueou?", "travou, e agora?"
- "qual agente eu chamo para X?"

## Quando **não** usar

Ela nunca executa trabalho de produto, e a própria descrição redireciona: feature ou mudança de
comportamento é `vortex-brainstorm` (ou `/vortex-feature`); bug é despacho direto ao especialista; entrega
de agência começa no `vortex-gestor-projetos`.

Essa fronteira é deliberada. Uma skill que responde "como uso isso" tem descrição perigosamente
próxima da que responde "quero criar isso" — se ela roubar a invocação da `vortex-brainstorm`, o
HARD-GATE de design deixa de ser aplicado.

## Exemplo

"O Claude travou dizendo `[VORTEX/ledger] Bloqueado: redespacho da Task 3`, o que eu faço?" → explica
que o ledger marca a task como concluída, manda conferir com `/vortex-ledger status`, e diz que reabrir
a task exige editar o ledger primeiro — porque remover a linha é a declaração consciente de que o
trabalho vai ser refeito.
