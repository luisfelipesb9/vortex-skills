# ✅ Checklist de Decisões — [Nome do Agente]

> **Gerado em:** [DATA]
> **Porte do projeto:** [🟢 MVP / 🟡 Médio / 🔴 Enterprise]
> **Budget estimado:** [BUDGET/mês]
> **Gerado com:** Agent Architect — JET Digital

---

## 📋 Contexto do Projeto

| Campo | Valor |
|-------|-------|
| **Função principal** | [DESCRIÇÃO DO QUE O AGENTE FAZ] |
| **Público-alvo** | [QUEM USA] |
| **Prazo para MVP** | [PRAZO] |
| **Stack preferida** | [TECNOLOGIAS] |
| **Memória entre sessões** | [SIM / NÃO] |
| **Integrações necessárias** | [LISTA DE SISTEMAS EXTERNOS] |
| **Tipo de agente** | [SINGLE AGENT / MULTI-AGENT] |

---

## 🗂️ Decisões por Camada

### Camada 01 — Segurança & Governança ✅ Obrigatória

- [ ] **Método de autenticação:** [JWT / Auth0 / Okta / Supabase Auth / Clerk]
- [ ] **Gerenciamento de secrets:** [.env / Doppler / HashiCorp Vault]
- [ ] **RBAC necessário:** [SIM — Ferramenta: X / NÃO]
- [ ] **Proteção contra prompt injection:** [Sanitização manual / Guardrails / Ferramenta X]
- [ ] **Filtragem de output:** [SIM / NÃO]
- [ ] **Conformidade:** [LGPD / GDPR / Nenhuma exigência formal]
- **Ferramenta(s) escolhida(s):** [FERRAMENTA] — 💰 Custo: [CUSTO/mês]

---

### Camada 02 — Monitoramento & Avaliação ✅ Obrigatória

- [ ] **Ferramenta de observabilidade:** [LangSmith / Grafana+Prometheus / AgentOps / Logs simples]
- [ ] **Estratégia de logging:** [Console / Arquivo / Banco de dados / Serviço externo]
- [ ] **HITL (humano no circuito):** [SIM / NÃO]
- [ ] **Métricas a rastrear:** [Latência / Custo por request / Taxa de erro / Satisfação]
- [ ] **Red team / testes adversariais:** [Planejado / Não planejado]
- **Ferramenta(s) escolhida(s):** [FERRAMENTA] — 💰 Custo: [CUSTO/mês]

---

### Camada 03 — Conhecimento & RAG ⚡ [Obrigatório / Opcional]

- [ ] **RAG necessário:** [SIM / NÃO] — *Se NÃO, pule esta camada*
- [ ] **Fonte(s) de dados:** [PDFs / Banco de dados / Notion / Site / Planilhas / Outro]
- [ ] **Frequência de atualização dos dados:** [Tempo real / Diária / Semanal / Estática]
- [ ] **Volume estimado de documentos:** [Pequeno <1k / Médio 1k–100k / Grande 100k+]
- [ ] **Estratégia de busca:** [Semântica / Híbrida (semântica + keyword)]
- [ ] **Framework RAG:** [LangChain / LlamaIndex / Haystack]
- [ ] **Vector store:** [Chroma / FAISS / Qdrant / Weaviate / Pinecone / pgvector]
- **Ferramenta(s) escolhida(s):** [FERRAMENTA] — 💰 Custo: [CUSTO/mês]

---

### Camada 04 — Gerenciamento de Memória ⚡ [Obrigatório / Opcional]

- [ ] **Memória entre sessões necessária:** [SIM / NÃO] — *Se NÃO, pule esta camada*
- [ ] **Tipo de memória:** [Curto prazo / Longo prazo / Ambos / Episódica]
- [ ] **O que será memorizado:** [Preferências do usuário / Histórico de conversas / Outro]
- [ ] **Solução de armazenamento:** [PostgreSQL / Redis / Vector store / Outro]
- [ ] **Guardrails de memória:** [SIM / NÃO]
- **Ferramenta(s) escolhida(s):** [FERRAMENTA] — 💰 Custo: [CUSTO/mês]

---

### Camada 05 — Orquestração & Automação ⚡ [Obrigatório / Opcional]

- [ ] **Single ou multi-agente:** [SINGLE / MULTI]
- [ ] **Fluxo principal mapeado:** [SIM / NÃO — descrever aqui se sim]
- [ ] **Ferramenta de orquestração:** [n8n / Make / LangGraph / CrewAI / AutoGen / Código próprio]
- [ ] **Hospedagem da orquestração:** [Self-hosted / Cloud]
- [ ] **Papéis dos agentes (se multi):** [Descrever]
- **Ferramenta(s) escolhida(s):** [FERRAMENTA] — 💰 Custo: [CUSTO/mês]

---

### Camada 06 — Uso de Ferramentas & Integração ⚡ [Obrigatório / Opcional]

- [ ] **Integrações necessárias:** [LISTA]
- [ ] **Protocolo de tool use:** [MCP / Function Calling nativo / A2A / Webhook]
- [ ] **Execução de código:** [SIM / NÃO]
- [ ] **Navegação na web:** [SIM / NÃO]
- [ ] **Leitura/escrita de arquivos:** [SIM / NÃO]
- **Custo estimado das integrações externas:** [CUSTO/mês]

---

### Camada 07 — LLMs & APIs ✅ Obrigatória

- [ ] **Modelo principal:** [MODELO] — 💰 Custo estimado: [CUSTO/1M tokens]
- [ ] **Modelo de fallback / triagem:** [MODELO] — 💰 Custo: [CUSTO/1M tokens]
- [ ] **Provider:** [Anthropic / OpenAI / Google / OpenRouter / Self-hosted]
- [ ] **Roteamento por complexidade:** [SIM / NÃO]
- [ ] **Output estruturado (JSON schema):** [SIM / NÃO]
- [ ] **Rate limiting e retry implementados:** [SIM / NÃO]
- **Custo estimado mensal de LLM:** [CUSTO/mês]

---

### Camada 08 — Conceitos de IA & Agentes ✅ Obrigatória

- [ ] **Tipo de agente:** [Semi-autônomo / Autônomo]
- [ ] **Arquitetura:** [ReAct / Plan-and-Execute / CAMEL / AutoGPT / Custom]
- [ ] **Protocolo:** [MCP / A2A / Function Calling / Nenhum]
- [ ] **Política de decisão autônoma:** [Definir quando age sem pedir confirmação]
- [ ] **Política de escalamento humano:** [Definir quando pausa e aguarda input]
- [ ] **Decomposição de metas:** [SIM — estratégia: X / NÃO]
- [ ] **Colaboração multiagente:** [SIM — hierarquia: X / NÃO]

---

### Camada 09 — Programação & Prompting ✅ Obrigatória

- [ ] **Linguagem principal:** [Python / TypeScript / Outro]
- [ ] **Linguagem secundária (se houver):** [LINGUAGEM]
- [ ] **Estratégia de prompting:** [Simples / Few-shot / CoT / DSPy]
- [ ] **Gerenciamento de contexto:** [Janela completa / Compressão / Sumarização]
- [ ] **Versionamento de prompts:** [SIM / NÃO]
- [ ] **Testes de prompts planejados:** [SIM / NÃO]

---

## 💰 Resumo de Custos

| Categoria | Ferramenta | Custo/mês (R$) |
|-----------|-----------|---------------|
| LLM | [MODELO] | R$ [VALOR] |
| Segurança | [FERRAMENTA] | R$ [VALOR] |
| Monitoramento | [FERRAMENTA] | R$ [VALOR] |
| Conhecimento/RAG | [FERRAMENTA] | R$ [VALOR] |
| Memória | [FERRAMENTA] | R$ [VALOR] |
| Orquestração | [FERRAMENTA] | R$ [VALOR] |
| Infraestrutura | [SERVIÇO] | R$ [VALOR] |
| Integrações externas | [APIS] | R$ [VALOR] |
| **TOTAL ESTIMADO** | | **R$ [TOTAL]** |

---

## ⚠️ Riscos Identificados

- [ ] [RISCO 1 — ex: Custo de LLM pode escalar rápido com volume de usuários]
- [ ] [RISCO 2 — ex: Dependência de API externa sem SLA garantido]
- [ ] [RISCO 3]

---

## 📌 Próximos Passos

1. [ ] [PASSO 1 — ex: Configurar ambiente de desenvolvimento e .env]
2. [ ] [PASSO 2 — ex: Implementar autenticação e logging antes de qualquer outra coisa]
3. [ ] [PASSO 3 — ex: Construir pipeline RAG com dados de teste]
4. [ ] [PASSO 4 — ex: MVP funcional para validação interna]
5. [ ] [PASSO 5 — ex: Deploy e monitoramento em produção]

---

*Gerado com Agent Architect — JET Digital*
