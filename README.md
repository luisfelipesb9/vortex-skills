# JET Skills

> O sistema de agentes que a JET Digital usa para tocar projetos de dev e de agência com Claude Code — não uma coleção de prompts soltos, mas um time com papéis, fronteiras e um método de trabalho comum.

A JET não escreve um prompt novo a cada tarefa. Construiu um **time fixo de agentes especializados** — cada um com escopo claro, ferramentas certas e guardrails de segurança — e um punhado de **skills de processo** que garantem que qualquer um deles trabalhe do mesmo jeito: explora antes de decidir, planeja antes de codar, testa antes de implementar, verifica antes de dizer "pronto".

Este repositório publica esse sistema inteiro como um plugin do Claude Code: 15 agentes, 6 skills de processo, 10 slash commands e 3 gates que rodam como hooks.

---

## O time

15 agentes, agrupados por onde atuam. Cada um entrega em arquivo/commit — nenhum publica em produção nem faz merge sozinho.

### Dev

| Agente | O que faz |
|---|---|
| [`jet-dev-backend`](docs/agentes/jet-dev-backend.md) | Lógica de servidor, APIs e serviços — TDD do início ao fim, na stack de backend do projeto. |
| [`jet-dev-frontend`](docs/agentes/jet-dev-frontend.md) | HTML/CSS/JavaScript e o framework do projeto — UI, acessibilidade e testes E2E, em TDD. |
| [`jet-dev-dados`](docs/agentes/jet-dev-dados.md) | PostgreSQL: schema, migrações, índices e performance de query, sempre com baseline medido antes/depois. |
| [`jet-dev-devops`](docs/agentes/jet-dev-devops.md) | Containers, CI/CD e deploy — infra como código, rollback documentado antes de qualquer deploy. |
| [`jet-implementador`](docs/agentes/jet-implementador.md) | Generalista do time dev — implementa uma task de um plano em TDD, sem especialidade fixa. |

### Agência

| Agente | O que faz |
|---|---|
| [`jet-copywriter`](docs/agentes/jet-copywriter.md) | Copy de anúncio, página, e-mail e CTA — ângulo de persuasão e tom de voz por marca. |
| [`jet-trafego`](docs/agentes/jet-trafego.md) | Estrutura de campanha, criativos, segmentação e leitura de métrica em Meta Ads e Google Ads. |
| [`jet-seo`](docs/agentes/jet-seo.md) | Pesquisa de keyword, briefs de artigo, clusters de conteúdo e otimização on-page. |
| [`jet-designer`](docs/agentes/jet-designer.md) | Layout, wireframes, protótipos navegáveis, Figma e design system. |
| [`jet-analista-dados`](docs/agentes/jet-analista-dados.md) | Dashboards, GA4 e relatório de performance traduzido em insight de negócio. |
| [`jet-gestor-projetos`](docs/agentes/jet-gestor-projetos.md) | Transforma pedido de cliente em tarefas com dono e prazo, acompanha status e destrava bloqueio. |

### Processo

| Agente | O que faz |
|---|---|
| [`jet-maestro`](docs/agentes/jet-maestro.md) | Orquestra o loop autônomo do time — pega a próxima task, delega ao especialista certo, registra o resultado. |
| [`jet-revisor`](docs/agentes/jet-revisor.md) | Revisa o diff de uma task em dois eixos — conformidade com o spec e qualidade/segurança — só leitura. |
| [`jet-pesquisador`](docs/agentes/jet-pesquisador.md) | Deep research multi-fonte na web, verificado de forma adversarial, com relatório citado. |
| [`jet-doc`](docs/agentes/jet-doc.md) | Escreve e atualiza documentação de engenharia — ADR, README, PRD, runbooks. |

---

## As skills de processo

6 skills que qualquer agente (ou o próprio Claude Code) invoca durante o trabalho — é o que faz o time inteiro seguir o mesmo método.

| Skill | O que faz |
|---|---|
| [`agent-architect`](docs/skills/agent-architect.md) | Guia estruturado para planejar a arquitetura de um agente de IA, camada por camada, com custo estimado. |
| [`jet-brainstorm`](docs/skills/jet-brainstorm.md) | Transforma uma ideia solta em design aprovado pelo usuário, antes de qualquer linha de código. |
| [`jet-plano`](docs/skills/jet-plano.md) | Transforma um spec aprovado em plano de implementação bite-sized, pronto para execução por subagentes. |
| [`jet-subagentes`](docs/skills/jet-subagentes.md) | Executa um plano despachando um subagente por tarefa, com revisão em cada gate. |
| [`jet-tdd`](docs/skills/jet-tdd.md) | Impõe o ciclo RED → GREEN → REFACTOR → commit em qualquer mudança de código. |
| [`jet-verificacao`](docs/skills/jet-verificacao.md) | Exige evidência de verificação fresca — comando rodado e output lido — antes de qualquer alegação de "pronto". |

Fora dessa tabela existe a [`jet-fluxo`](docs/skills/jet-fluxo.md) — ela não participa do trabalho,
ela explica o trabalho: responde "como eu uso isso", "por que esse gate bloqueou", "qual o próximo
passo". É o runbook em forma de skill.

---

## Como o sistema se encaixa

Uma feature não vira código direto. Ela passa por um funil de skills, com o `jet-maestro` orquestrando a entrega entre os agentes:

```mermaid
flowchart LR
    I[Ideia / pedido] --> B(jet-brainstorm)
    B --> P(jet-plano)
    P --> S(jet-subagentes)
    S --> T(jet-tdd)
    T --> V(jet-verificacao)
    V --> R(jet-revisor)
    R --> M[Pronto para merge]

    O{{jet-maestro}} -. orquestra .-> S
    O -. orquestra .-> T
    O -. orquestra .-> V
    O -. orquestra .-> R
```

Na prática: `jet-brainstorm` converge a ideia num design aprovado; `jet-plano` quebra o design em tasks bite-sized; `jet-subagentes` despacha um agente especialista por task; cada task roda em `jet-tdd` (RED → GREEN → REFACTOR); `jet-verificacao` bloqueia qualquer "terminei" sem evidência fresca; e `jet-revisor` audita o diff antes de seguir. O `jet-maestro` é quem fecha o loop sozinho quando o trabalho é autônomo — sem ele, o time roda sob comando direto do humano, um agente de cada vez.

---

## Como instalar

É um plugin do Claude Code. Dois comandos, e atualizar depois é `/plugin update`:

```bash
/plugin marketplace add wearejet/jet-skills
```

```bash
/plugin install jet-skills
```

Na instalação o Claude Code pergunta a severidade de cada gate e os caminhos do projeto — todos
têm default razoável, pode aceitar tudo e ajustar depois com `/jet-doutor`.

Para conferir que ficou de pé:

```bash
/jet-doutor
```

Cada agente e cada skill tem uma página em [`docs/`](docs/) com o que faz, quando usar e um
exemplo.

## Como operar

O fluxo completo — setup, feature nova, bugfix, entrega de agência, retomada após compactação,
quando **não** usar o pipeline, e troubleshooting — está em **[`docs/RUNBOOK.md`](docs/RUNBOOK.md)**.

Dentro de uma sessão você não precisa procurar: pergunte ("como eu uso isso?", "por que esse gate
bloqueou?") e a skill `jet-fluxo` responde. Ou rode `/jet-fluxo` direto.

---

## O que vem a seguir

A JET construiu o **Nexo** para orquestrar esse time num canvas só — [em breve](https://wearejet.digital).

---

## Sobre a JET

Desenvolvido e mantido pela [JET Digital](https://wearejet.digital) — estúdio de tecnologia e growth especializado em web design, inteligência comercial, SEO & GEO, performance e sistemas.

Parte deste conteúdo é adaptação de um toolkit de terceiros; a atribuição completa (origem, licença e o que é original da JET) está no [`NOTICE`](./NOTICE).

---

*Feito em Criciúma, SC.*
