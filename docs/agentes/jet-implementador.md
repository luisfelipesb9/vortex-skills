# jet-implementador

> Generalista do time dev — implementa uma task de um plano de implementação em TDD, sem especialidade fixa.

## O que faz

Implementa exatamente uma task a partir de um brief: identifica o seam (interface pública) onde o comportamento vai ser testado, escreve o teste que falha, vê o RED com mensagem significativa, implementa o mínimo, vê o GREEN, roda a suíte inteira e comita. Também segue uma disciplina de diagnóstico de bugs — hipóteses ranqueadas, um probe por vez, regra dos 3 fixes.

## Quando usar

- Task multi-área sem dominância clara (não é claramente frontend, backend, dados ou devops).
- Task fora das quatro especialidades do time.
- Bugfix que precisa de repro e diagnóstico sistemático antes da correção.
- Se a task for claramente de uma especialidade (UI/DS → `jet-dev-frontend`; backend/API → `jet-dev-backend`; SQL/dados → `jet-dev-dados`; infra/CI/deploy → `jet-dev-devops`), sinaliza ao orquestrador antes de começar em vez de tocar a task genericamente.

## Como funciona

Fluxo fixo por task: brief → seam → RED → GREEN → verificação (typecheck/lint contínuo, suíte completa uma vez antes de comitar) → auto-revisão → report (status, commits, resumo dos testes, ressalvas). Trabalha em UMA task por vez, entrega via commit na branch com Conventional Commits e trailer `Co-Authored-By` — **nunca faz merge nem force-push**. Não constrói além da task (YAGNI); se travar, reporta BLOQUEADO/FALTA_CONTEXTO em vez de adivinhar.

## Exemplo

"Implementa a task 3 do plano: exportar relatório em CSV" → o agente lê o brief, escreve o teste que falha pro seam de exportação, vê o RED, implementa o mínimo, vê o GREEN, roda a suíte e comita — sem mergear.
