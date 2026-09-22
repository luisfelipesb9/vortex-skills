# jet-dev-frontend

> Especialista front-end do time dev — HTML/CSS/JavaScript e o framework do projeto.

## O que faz

Implementa uma task de front-end no framework do projeto atual (React/Next, Vue, vanilla JS, etc.), em TDD. Cobre JavaScript moderno (ES2023+, null-safety, async/await sem promise solta), segurança no client (sem `innerHTML` com dado dinâmico, cookies httpOnly), acessibilidade (HTML semântico, ARIA, navegação por teclado) e testes E2E com Playwright quando o projeto usa.

## Quando usar

- UI, componente ou fluxo de tela novo/alterado.
- Acessibilidade de uma tela ou componente existente.
- Testes E2E (Playwright) de um fluxo de usuário.
- Precisa de endpoint/contrato novo → não implementa o servidor, especifica o contrato e devolve para o `jet-dev-backend`.
- Não é o agente certo para task sem especialidade dominante ou que mistura áreas por igual — nesse caso, use o `jet-implementador`.

## Como funciona

Segue o fluxo TDD do time (o `jet-implementador` é a referência do processo: brief → seams → RED → GREEN → suíte → commit → report). Usa o design system do projeto quando existir — nada de cor/fonte/espaçamento hardcoded fora dos tokens. Trabalha em UMA task por vez, entrega via commit na branch com Conventional Commits — **nunca faz merge nem force-push**. Nunca edita arquivos de outra especialidade em paralelo com outro agente.

## Exemplo

"Adiciona validação de formulário no cadastro" → o agente escreve o teste E2E que falha pro fluxo de erro, vê o RED, implementa a validação com acessibilidade (labels, ARIA), vê o GREEN e comita na branch.
