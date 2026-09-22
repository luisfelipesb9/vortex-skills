---
name: agent-architect
description: >
  Use esta skill SEMPRE que o usuario quiser criar, planejar, arquitetar ou iniciar qualquer projeto
  de agente de IA. Triggers incluem: quero criar um agente, vamos construir um bot, preciso de um
  agente de IA, como estruturar um agente, planejamento de agente, novo agente, chatbot com IA,
  automacao com LLM, agent com n8n, agent com langchain, qualquer mencao a construir ou planejar
  algo com LLMs, agentes ou AI agents. A skill conduz o usuario por um processo guiado baseado no
  Roteiro de IA Agentica 2026 (9 camadas), classificando o projeto por porte e budget, recomendando
  ferramentas com estimativas de custo reais, e gerando ao final um Checklist de Decisoes e um
  README tecnico completo como arquivos .md. Nao espere a palavra agente - sinais como quero
  automatizar com IA, bot que faz X, pipeline de LLM tambem ativam esta skill.
---

# Agent Architect

Skill para planejar arquitetura de agentes de IA com base no **Roteiro de IA Agêntica 2026** — 9 camadas, do que é obrigatório ao que é opcional, com ferramentas e custos reais.

---

## Objetivo

Guiar o usuário por um processo estruturado de tomada de decisão para:
1. Entender o contexto e porte do projeto
2. Percorrer as 9 camadas do roteiro
3. Recomendar as ferramentas certas com base em custo e cenário
4. Gerar um **Checklist de Decisões** + **README técnico** como arquivos `.md`

---

## Fase 1 — Contexto do Projeto

Antes de qualquer coisa, envie ao usuário as perguntas abaixo em uma única mensagem. **Aguarde todas as respostas antes de avançar.**

```
Para montar a arquitetura certa, preciso entender o projeto:

1. O que o agente vai fazer? (função principal, tarefa específica)
2. Para quem? (uso interno, cliente final, B2C, B2B?)
3. Budget mensal estimado de infraestrutura? (em R$ ou USD)
4. Prazo para ter o MVP rodando?
5. Vai precisar de memória entre sessões? (lembrar de conversas anteriores)
6. Vai interagir com sistemas externos? (APIs, WhatsApp, CRM, banco de dados...) — quais?
7. É um agente único ou múltiplos agentes colaborando?
8. Stack que já usa ou prefere? (ex: Python, n8n, Supabase...)
```

---

## Fase 2 — Classificação do Projeto

Com base nas respostas, classifique e **informe o usuário** em qual porte o projeto se encaixa:

| Porte | Budget Infra/mês | Perfil |
|-------|-----------------|--------|
| 🟢 **MVP** | Até ~R$300 / USD 60 | Validação, projeto pessoal, freelancer |
| 🟡 **Médio** | R$300–1.500 / USD 60–300 | PMEs, clientes de agência, produção real |
| 🔴 **Enterprise** | Acima de R$1.500 / USD 300 | Escala, multi-tenant, missão crítica |

---

## Fase 3 — Percurso pelas 9 Camadas

Para cada camada, siga este padrão:

1. **Anuncie a camada** com número e nome
2. **Explique em 1–2 linhas** o que ela resolve
3. **Diga se é obrigatória ou opcional** para este projeto específico (use o contexto coletado)
4. **Apresente as opções de ferramenta** com custo estimado (dados em `references/ferramentas-custo.md`)
5. **Faça uma recomendação direta** com base no porte — não dê 10 opções, dê 1 principal e no máximo 1 alternativa
6. **Confirme a decisão** com o usuário ou avance se for óbvio
7. **Registre internamente** a decisão para usar no output final

> Pode agrupar camadas relacionadas em uma mensagem quando fizer sentido para agilizar o fluxo.

### Ordem e Prioridade das Camadas

```
✅ SEMPRE OBRIGATÓRIAS (independente de porte ou caso de uso):
  01 — Segurança & Governança
  02 — Monitoramento & Avaliação
  07 — LLMs & APIs
  08 — Conceitos de IA & Agentes (decisão arquitetural)
  09 — Programação & Prompting

⚡ DEPENDE DO CASO DE USO:
  03 — Conhecimento & RAG          → obrigatório se o agente precisa consultar documentos/base de conhecimento
  04 — Gerenciamento de Memória    → obrigatório se precisa lembrar entre sessões
  05 — Orquestração & Automação    → obrigatório se multi-agente ou workflow complexo; opcional para agente único simples
  06 — Uso de Ferramentas          → obrigatório se interage com sistemas externos; opcional se agente é apenas conversacional
```

> ⚠️ **NUNCA pule as camadas 01 e 02.** Segurança e monitoramento ignorados no início viram incidentes em produção. Deixe isso claro ao usuário se ele tentar pular.

Para detalhes técnicos de cada camada (funcionalidades, trade-offs, recomendações por porte), leia `references/camadas.md`.

Para tabela de preços e comparativos de ferramentas, consulte `references/ferramentas-custo.md`.

---

## Fase 4 — Geração dos Outputs

Após percorrer todas as camadas, gere automaticamente os dois arquivos abaixo como `.md`.

Use os templates em `assets/checklist-template.md` e `assets/readme-template.md` como base — preencha com as decisões reais tomadas durante a conversa.

**A) `checklist-[nome-do-agente].md`**
Checklist de todas as decisões tomadas por camada, com ferramentas escolhidas e custos.

**B) `README-[nome-do-agente].md`**
Documento técnico completo: visão geral, arquitetura, stack, estrutura de pastas, como rodar, variáveis de ambiente, custos estimados e roadmap.

Salve os dois arquivos no diretório de trabalho atual (ou na pasta que o usuário indicar) e informe os caminhos ao usuário ao final.

---

## Diretrizes de Comunicação

- **Idioma:** sempre Português
- **Público:** contexto técnico — pode usar RAG, embeddings, RBAC, vector store, MCP, etc. sem explicar do zero
- **Tom:** direto e objetivo. Recomendações claras, não listas intermináveis de possibilidades
- **Status visual:** use ✅ Obrigatório | ⚡ Opcional | 🔧 Ferramenta | 💰 Custo | ⚠️ Atenção
- **Trade-offs:** quando houver custo vs. qualidade, explicite brevemente e recomende
- **Dúvidas do usuário:** se não souber responder algo (ex: "não sei o budget"), ajude a estimar com base no contexto
- **Ritmo:** avance camada por camada, confirmando decisões. Não despeje tudo de uma vez.

---

## Referências

| Arquivo | Quando Ler |
|---------|-----------|
| `references/camadas.md` | Detalhes técnicos, funcionalidades e recomendações por porte de cada camada |
| `references/ferramentas-custo.md` | Preços, planos gratuitos e pagos de todas as ferramentas |
| `assets/checklist-template.md` | Template base para o checklist de decisões |
| `assets/readme-template.md` | Template base para o README técnico |
