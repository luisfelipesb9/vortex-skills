---
name: jet-fluxo
description: "Use quando a pergunta for sobre COMO OPERAR o plugin jet-skills: qual comando rodar, em que ordem, por que um gate bloqueou, como retomar depois de uma compactação, qual agente chamar para quê, o que é garantido por máquina e o que é convenção. Gatilhos: 'como uso isso', 'qual o próximo passo', 'travou o gate', 'o que faço agora', 'qual agente chamo'. NUNCA use para executar trabalho de produto — para criar, mudar ou corrigir software a skill é jet-brainstorm, e para operar uma entrega de agência o ponto de entrada é o jet-gestor-projetos."
---

# jet-fluxo — como operar o time

Responda pela tabela que couber. Detalhe completo, com os fluxos narrados passo a passo:
`${CLAUDE_PLUGIN_ROOT}/docs/RUNBOOK.md` — leia antes de responder qualquer coisa que não esteja
nas tabelas abaixo.

**Se a pergunta for sobre construir alguma coisa, e não sobre operar o plugin, você é a skill
errada.** Feature ou mudança de comportamento → `jet-brainstorm` (ou `/jet-feature`). Bug →
despacho direto ao especialista. Entrega de agência → `jet-gestor-projetos`.

## Tabela de decisão

| Quero… | Uso |
|---|---|
| Começar uma feature | `/jet-feature <ideia>` |
| Retomar do spec para o plano | `/jet-plano <spec.md>` |
| Executar um plano acompanhando | `executa esse plano` |
| Executar sem sujar meu contexto | `/jet-executar <plano.md>` |
| Corrigir um bug | despacho direto ao especialista, com sintoma e repro |
| Saber onde parei | `/jet-ledger status` |
| Provar que os testes passam | `/jet-verificar` |
| Montar o diff de uma task | `/jet-diff <base-ref> <task>` |
| Abrir o PR | `/jet-pr` |
| Fazer merge | **o humano, no GitHub** — nenhum agente faz |
| Saber se o plugin está de pé | `/jet-doutor` |
| Afrouxar ou apertar um gate | `/jet-nivel fronteiras warn` |
| Pesquisa externa profunda | despachar `jet-pesquisador` |
| ADR, README, runbook | despachar `jet-doc` |
| Layout, wireframe, protótipo | despachar `jet-designer` |
| Pedido de cliente virando tarefas | despachar `jet-gestor-projetos` |

## Garantido por máquina × convenção

| Máquina | Convenção |
|---|---|
| Merge, force-push, push em branch protegida e `gh pr merge` são negados | Passar por design antes de codar |
| Deploy, secrets, DNS, terraform e Stripe perguntam antes | Um implementador por vez |
| Redespachar task concluída no ledger é negado | Teste escrito antes do código |
| Ledger é reinjetado no início de sessão e após compactação | O teste ter falhado pelo motivo certo |
| Revisor não escreve arquivo; implementador não delega | Revisão em dois eixos por task |

Os gates são o piso; o `jet-revisor` é o teto. E **nada disso cobre o commit que o humano faz no
próprio terminal**.

## Sintomas mais comuns

| Sintoma | Causa e ação |
|---|---|
| Editou código sem perguntar nada | Auto-invocação falhou. Interrompa, `use a skill jet-brainstorm`, descarte o que ele escreveu |
| `[JET/fronteiras] Bloqueado: merge` | Está funcionando. Merge é no GitHub |
| `[JET/ledger] Bloqueado: redespacho` | O ledger diz que a task está pronta. Confira com `/jet-ledger status`; para reabrir, edite o ledger primeiro |
| Agente errado pegou a task | Campo `Agente` do plano errado. Corrija e redespache antes de entrar no ledger |
| Ledger diverge do git | O git ganha, sempre. Nunca reescreva o ledger de memória |
| "Suíte verde" e está vermelha | Relatório de subagente é alegação. `/jet-verificar` no seu contexto |
| Parou no meio, sem status | Teto de `maxTurns`. `git log` + `/jet-ledger status`, redespache só o que falta |

Sintoma que não está aqui: leia a seção 8 do RUNBOOK.
