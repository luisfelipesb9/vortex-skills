# Detalhes das 9 Camadas — Roteiro de IA Agêntica 2026

---

## Camada 01 — Segurança & Governança ✅ SEMPRE OBRIGATÓRIA

> Confiança, controle e proteção

**O que resolve:** Define quem pode fazer o quê e protege o agente contra manipulação, vazamento de dados e acesso indevido.

**Por que nunca pular:** Segurança negligenciada no início vira incidente em produção — prompt injection, exposição de secrets, acesso não autorizado. O custo de corrigir depois é ordens de magnitude maior.

**Funcionalidades:**
- Proteção contra injeção de prompt
- Gerenciamento de chaves de API (secrets)
- Autenticação de usuário
- Controle de acesso baseado em papéis (RBAC)
- Filtragem de saída (output guardrails)
- Privacidade de dados & conformidade (LGPD, GDPR)

**Decisões a tomar:**
- Como usuários vão se autenticar?
- Onde ficam as chaves de API? (.env / secrets manager / vault)
- Precisa de RBAC? (diferentes usuários com diferentes permissões)
- Precisa de guardrails de output? (filtrar respostas do LLM antes de exibir)

**Recomendação por porte:**
- 🟢 MVP: JWT simples + variáveis de ambiente (.env) + sanitização de input no código. Custo: R$0
- 🟡 Médio: Auth0 (free até 7.500 MAU) + Doppler para secrets ($10/mês time). Custo: ~R$50/mês
- 🔴 Enterprise: Okta + HashiCorp Vault + Permit.io para RBAC granular. Custo: ~R$200+/mês

---

## Camada 02 — Monitoramento & Avaliação ✅ SEMPRE OBRIGATÓRIA

> Mensurar, avaliar e otimizar

**O que resolve:** Garante visibilidade do que o agente está fazendo em tempo real. Sem isso, você não sabe quando ele alucina, trava ou produz resultados ruins.

**Por que nunca pular:** Um agente sem monitoramento é uma caixa preta em produção. Você só descobre o problema quando o cliente reclama.

**Funcionalidades:**
- Métricas de avaliação de agentes (latência, tokens, custo por request)
- Feedback humano no circuito — HITL (Human-in-the-Loop)
- Registro e rastreamento (logging / tracing)
- Loops de autoavaliação
- Testes de equipe vermelha (red team / adversarial testing)

**Decisões a tomar:**
- Qual nível de rastreamento você precisa? (logs simples vs. tracing completo)
- Precisa de HITL? (humano aprovando/corrigindo antes de ações)
- Vai usar dashboard visual ou só logs?

**Recomendação por porte:**
- 🟢 MVP: Logs estruturados em console/arquivo + LangSmith free (3k traces/mês). Custo: R$0
- 🟡 Médio: LangSmith Developer ($39/mês ≈ R$200) ou Grafana + Prometheus self-hosted (gratuito, só infra). Custo: R$0–R$200/mês
- 🔴 Enterprise: LangSmith Enterprise + OpenTelemetry + Grafana Cloud. Custo: R$500+/mês

---

## Camada 03 — Conhecimento & RAG ⚡ CONDICIONAL

> Dados que os agentes entendem

**Quando é obrigatório:** O agente precisa consultar documentos, PDFs, base de conhecimento interna, catálogo de produtos, histórico de atendimento, ou qualquer informação que não está no treinamento do LLM.

**Quando é opcional/desnecessário:** Agente puramente conversacional que usa apenas o conhecimento do LLM + dados passados no prompt.

**Funcionalidades:**
- RAG (Retrieval-Augmented Generation) — buscar contexto relevante antes de gerar resposta
- Modelos de embeddings (transformar texto em vetores)
- Carregamento e processamento de dados personalizados
- Indexação de documentos
- Refinamento de consultas (query rewriting)
- Busca híbrida (semântica + keyword)

**Decisões a tomar:**
- Qual é a fonte de dados? (PDFs, banco de dados, notion, site, planilhas...)
- Com que frequência os dados mudam? (tempo real vs. batch)
- Volume de documentos? (pequeno = Chroma local | grande = Pinecone/Weaviate)
- Precisa de busca híbrida ou semântica pura basta?

**Recomendação por porte:**
- 🟢 MVP: Chroma (local, gratuito) + LlamaIndex ou LangChain. Custo: R$0
- 🟡 Médio: Weaviate Cloud (free até 1M vetores) ou Qdrant Cloud + LangChain. Custo: R$0–R$130/mês
- 🔴 Enterprise: Pinecone Starter+ ($70/mês ≈ R$350) ou Weaviate dedicado. Custo: R$350+/mês

**Trade-off chave:** Chroma/FAISS são gratuitos mas locais — não escalam facilmente. Pinecone escala mas tem custo. Weaviate/Qdrant são o meio-termo.

---

## Camada 04 — Gerenciamento de Memória ⚡ CONDICIONAL

> Memória que permite evolução dos agentes

**Quando é obrigatório:** Chatbots de atendimento, assistentes pessoais, agentes que precisam lembrar do usuário entre conversas, agentes que aprendem com o tempo.

**Quando é opcional:** Agentes de tarefa única (ex: "analise este PDF e retorne um relatório") que não precisam de contexto histórico.

**Tipos de memória:**
- **Curto prazo:** dentro da sessão atual (contexto do LLM)
- **Longo prazo:** entre sessões (banco de dados / vector store)
- **Episódica:** registros de eventos passados específicos
- **Semântica:** conhecimento geral acumulado

**Funcionalidades:**
- Armazenamento vetorial de memórias
- Gatilhos baseados em eventos (salvar memória quando X acontece)
- Validações & guardrails de memória
- Loops & fluxos condicionais baseados em memória
- Gerenciamento DAG (Directed Acyclic Graph) de dependências

**Recomendação por porte:**
- 🟢 MVP: PostgreSQL/SQLite para memória estruturada + resumo de contexto injetado no prompt. Custo: R$0
- 🟡 Médio: Chroma ou Qdrant para memória vetorial + Redis para cache de sessão. Custo: R$0–R$80/mês
- 🔴 Enterprise: Pinecone + Redis Enterprise + pipeline de memória episódica customizado. Custo: R$500+/mês

---

## Camada 05 — Orquestração & Automação ⚡ CONDICIONAL

> Agentes que agem com inteligência

**Quando é obrigatório:** Múltiplos agentes colaborando, workflows com múltiplos passos, automações complexas com condicionais e ramificações.

**Quando é opcional:** Agente único e simples com fluxo linear — pode ser orquestrado direto no código.

**Funcionalidades:**
- Coordenação de múltiplos agentes
- Definição de papéis e responsabilidades por agente
- Fluxos condicionais e ramificações
- Handoffs entre agentes
- Triggers e webhooks
- Estado persistente entre etapas

**Ferramentas e seus perfis:**

| Ferramenta | Melhor para | Tipo |
|-----------|------------|------|
| **n8n** | Workflows visuais + integrações SaaS | Low-code, self-hosted ou cloud |
| **Make** | Integrações SaaS para não-devs | No-code, cloud |
| **Zapier** | Maior biblioteca de integrações | No-code, cloud |
| **LangGraph** | Agentes com estado complexo e fluxos condicionais | Code, open-source |
| **CrewAI** | Multi-agente com papéis definidos | Code, open-source |
| **AutoGen** | Multi-agente robusto (Microsoft) | Code, open-source |
| **Semantic Kernel** | Stack Microsoft (.NET/Python) | Code, open-source |
| **LangChain** | Base universal para pipelines LLM | Code, open-source |

**Recomendação por porte:**
- 🟢 MVP: n8n self-hosted + LangGraph ou CrewAI. Custo: R$0 (só infra)
- 🟡 Médio: n8n Cloud ($20/mês ≈ R$100) + CrewAI ou LangGraph. Custo: ~R$100/mês
- 🔴 Enterprise: LangGraph + n8n Cloud Business ($50/mês ≈ R$250) + AgentOps para monitoramento. Custo: R$400+/mês

**Trade-off chave:** n8n self-hosted = gratuito mas você gerencia o servidor. n8n Cloud = pago mas zero manutenção.

---

## Camada 06 — Uso de Ferramentas & Integração ⚡ CONDICIONAL

> Execução no mundo real

**Quando é obrigatório:** Sempre que o agente precisar interagir com sistemas externos (APIs, arquivos, banco de dados, web, WhatsApp, CRM, etc.).

**Quando é opcional:** Agente puramente conversacional sem integrações externas.

**Funcionalidades:**
- System de uso de ferramentas (tool calling / function calling)
- Chamadas a APIs externas (REST, GraphQL, webhooks)
- Leitura e escrita de arquivos
- Interpretador de código & calculadora
- Execução de código Python em sandbox
- Navegação na web (browser use)
- Busca e recuperação em tempo real

**Protocolo recomendado:**
- **MCP (Model Context Protocol):** padrão moderno para conectar agentes a ferramentas — use sempre que possível
- **Function Calling nativo:** suportado por OpenAI, Anthropic, Google — mais simples para casos básicos
- **A2A (Agent-to-Agent):** para comunicação entre agentes diferentes

**Custo:** Depende das APIs externas. Exemplos:
- WhatsApp Business API: ~$0.05–0.15/conversa (~R$0.25–0.75)
- Twilio SMS: ~$0.0075/mensagem
- APIs internas: custo de infra apenas

**Recomendação:** Defina as ferramentas como funções com schemas claros + use MCP quando disponível. Documente todos os endpoints externos com rate limits e custos.

---

## Camada 07 — LLMs & APIs ✅ SEMPRE OBRIGATÓRIA

> Modelos como motor

**O que resolve:** O cérebro do agente — o modelo que processa, raciocina e gera respostas.

**Funcionalidades:**
- Autenticação de APIs (API keys, OAuth)
- Rate limiting e retry logic
- Function calling / tool use
- Parsing e validação de saída estruturada
- Encadeamento de prompts via API
- Roteamento por complexidade de tarefa (modelos baratos para triagem, caros para raciocínio)

**Consulte `references/ferramentas-custo.md`** para tabela completa de modelos com preços atualizados.

**Recomendação por porte:**
- 🟢 MVP: **Claude 3.5 Haiku** (melhor custo-qualidade para tarefas simples) ou **DeepSeek V3** (absurdamente barato). Custo: R$5–50/mês
- 🟡 Médio: **Claude 3.5 Sonnet** para tarefas gerais + Haiku para triagem (roteamento). Custo: R$50–500/mês
- 🔴 Enterprise: **Claude Opus 4** ou **GPT-4o** + roteamento inteligente por complexidade. Custo: R$500+/mês

**Trade-off chave:** Modelos melhores custam mais por token. Para escala, implemente roteamento: tarefas simples vão para modelos baratos, tarefas complexas vão para modelos caros. Reduz custo em 60–80%.

---

## Camada 08 — Conceitos de IA & Agentes ✅ OBRIGATÓRIA (decisão de arquitetura)

> Blueprint estratégico

**O que resolve:** As decisões arquiteturais fundamentais que definem como o agente vai pensar, agir e se organizar. Feita no início; difícil de mudar depois.

**Decisões desta camada:**

**1. Tipo de agente:**
- **Semi-autônomo:** Pede confirmação humana antes de ações críticas. Mais seguro, mais lento.
- **Autônomo:** Age por conta própria dentro de políticas definidas. Mais ágil, mais risco.

**2. Arquitetura:**
- **ReAct (Reason + Act):** O agente raciocina sobre o que fazer, age, observa o resultado, repete. Mais previsível e fácil de debugar. ✅ Recomendado para MVP
- **Plan-and-Execute:** Planeja todos os passos antes de agir. Melhor para tarefas complexas com dependências.
- **CAMEL:** Dois agentes (usuário + assistente) simulando diálogo para resolver tarefas. Criativo.
- **AutoGPT / BabyAGI:** Agente com objetivos de longo prazo e auto-geração de subtarefas. Poderoso mas imprevisível.

**3. Protocolo:**
- **MCP (Model Context Protocol):** padrão moderno para agentes interagirem com ferramentas e contexto
- **A2A (Agent-to-Agent):** protocolo para comunicação entre agentes diferentes

**4. Políticas de decisão:**
- Quando o agente age autonomamente?
- Quando ele pausa e pede confirmação humana?
- O que acontece em caso de erro ou incerteza?

**5. Colaboração multiagente:**
- Hierarquia: agente orquestrador + subagentes especializados
- Comunicação entre agentes: mensagens, estado compartilhado, handoffs

**Recomendação por porte:**
- 🟢 MVP: ReAct simples, semi-autônomo, sem MCP (function calling básico)
- 🟡 Médio: ReAct ou Plan-and-Execute, MCP para padronizar ferramentas
- 🔴 Enterprise: Multi-agente com papéis definidos, MCP + A2A, políticas de decisão explícitas

---

## Camada 09 — Programação & Prompting ✅ SEMPRE OBRIGATÓRIA

> A base que transforma intenção em comportamento confiável

**O que resolve:** A fundação técnica — como o código é escrito e como os prompts são estruturados para que o agente se comporte de forma previsível e confiável.

**Funcionalidades:**
- Requisições de API (HTTP/JSON, autenticação, retry)
- Manipulação de arquivos e dados
- Programação assíncrona (async/await)
- Web scraping quando necessário
- Engenharia de prompts (system prompt, few-shot, CoT)
- Gerenciamento de contexto (janela de contexto, compressão)
- Cadeia de pensamento (Chain of Thought — CoT)
- Prompting multiagente

**Linguagens:**
- **Python:** Melhor ecossistema para IA. Recomendado para backend e pipelines. ✅ Padrão
- **TypeScript:** Ideal para agentes web, integrações com frontend, Vercel Edge Functions
- **Shell:** Scripts de automação, CI/CD, infraestrutura

**Boas práticas de prompting por porte:**
- 🟢 MVP: System prompt direto, instrução clara, exemplos simples. Itere rápido.
- 🟡 Médio: Few-shot examples, CoT para raciocínio, output estruturado (JSON schema)
- 🔴 Enterprise: DSPy para otimização automática de prompts, versionamento de prompts, A/B testing de prompts

**Custo:** R$0 — é tempo de desenvolvimento.
