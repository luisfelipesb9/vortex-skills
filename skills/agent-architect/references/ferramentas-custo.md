# Referência de Ferramentas e Custos

> Estimativas atualizadas para 2026. Preços em USD e BRL (câmbio ~R$5,00).
> Confirme na documentação oficial antes de usar em proposta comercial.

---

## 🤖 LLMs & APIs

| Modelo | Input (1M tokens) | Output (1M tokens) | R$/mês estimado (uso médio) | Melhor para |
|--------|-------------------|---------------------|------------------------------|------------|
| **Claude 3.5 Haiku** | ~$0.80 | ~$4.00 | R$10–80 | MVP, triagem, tarefas simples |
| **Claude 3.5 Sonnet** | ~$3.00 | ~$15.00 | R$50–500 | Uso geral, melhor equilíbrio |
| **Claude Opus 4** | ~$15.00 | ~$75.00 | R$500+ | Raciocínio complexo, Enterprise |
| **GPT-4o mini** | ~$0.15 | ~$0.60 | R$5–30 | Muito barato, triagem rápida |
| **GPT-4o** | ~$2.50 | ~$10.00 | R$50–400 | Multimodal, function calling robusto |
| **Gemini 1.5 Flash** | ~$0.075 | ~$0.30 | R$5–25 | O mais barato do Google |
| **Gemini 1.5 Pro** | ~$3.50 | ~$10.50 | R$50–400 | Contexto longo (1M tokens) |
| **DeepSeek V3** | ~$0.14 | ~$0.28 | R$3–20 | Excelente qualidade por preço baixíssimo |
| **Mistral Large** | ~$2.00 | ~$6.00 | R$40–200 | Compliance GDPR europeu |
| **LLaMA 3 (self-hosted)** | Custo de GPU | Custo de GPU | R$300+ (infra) | Controle total, dados sensíveis |
| **OpenRouter** | Varia | Varia | Varia | Agregador com fallback automático |

**💡 Dica de custo:** Para escala, implemente **roteamento por complexidade** — GPT-4o mini ou Haiku para triagem, modelos maiores só para tarefas complexas. Reduz custo em 60–80%.

---

## 🔒 Autenticação & Segurança

| Ferramenta | Plano Gratuito | Plano Pago | Ideal para |
|------------|---------------|------------|------------|
| **JWT + .env** | Gratuito | — | MVP simples, uso interno |
| **Auth0** | Até 7.500 MAU | A partir de $23/mês (R$115) | MVP → Médio, login social |
| **Supabase Auth** | 50k MAU no free | $25/mês (R$125) | Se já usa Supabase |
| **Clerk** | 10k MAU | A partir de $25/mês (R$125) | DX excelente, Next.js |
| **Okta** | Não | A partir de $2/usuário/mês | Enterprise |
| **Permit.io** | Até 1.000 tenants | Custom | RBAC granular |
| **Doppler** | Gratuito (pessoal) | $10/mês (R$50) time | Secrets management simples |
| **HashiCorp Vault** | Open-source (self-hosted) | $0.03/secret/hora (Cloud) | Secrets Enterprise |

---

## 📊 Monitoramento & Avaliação

| Ferramenta | Plano Gratuito | Plano Pago | Ideal para |
|------------|---------------|------------|------------|
| **LangSmith** | 3.000 traces/mês | $39/mês (R$195) Developer | Agentes LangChain/LangGraph |
| **AgentOps** | Free tier | Custom | Monitoramento específico para agentes |
| **Prometheus** | Open-source | — | Métricas custom (requer infra) |
| **Grafana** | Open-source / Cloud free | $29/mês (R$145) | Dashboards visuais |
| **OpenTelemetry** | Open-source | — | Tracing padronizado, multi-provider |
| **Datadog** | 14 dias trial | A partir de $31/mês (R$155) | Enterprise, observabilidade completa |

---

## 🗄️ Vector Stores (Conhecimento & Memória)

| Ferramenta | Plano Gratuito | Plano Pago | Notas |
|------------|---------------|------------|-------|
| **Chroma** | Open-source (local) | — | Melhor para MVP local. Não escala facilmente. |
| **FAISS** | Open-source (Meta) | — | Muito performático, sem servidor, sem UI |
| **Qdrant** | Open-source + Cloud free | Cloud a partir de $0 | Melhor alternativa open-source ao Pinecone |
| **Weaviate** | Cloud free (1M vetores) | A partir de $25/mês (R$125) | Busca híbrida nativa, boa DX |
| **Pinecone** | 1 índice, 100k vetores | $70/mês (R$350) Starter | Mais maduro, melhor para Enterprise |
| **Supabase pgvector** | No free tier | $25/mês (R$125) | Se já usa Supabase — simplifica stack |

**Trade-off:**
- 🟢 MVP → Chroma (local) ou Qdrant (cloud free)
- 🟡 Médio → Weaviate Cloud ou Qdrant Cloud
- 🔴 Enterprise → Pinecone ou Weaviate dedicado

---

## ⚙️ Orquestração & Automação

| Ferramenta | Gratuito | Pago | Tipo | Notas |
|-----------|---------|------|------|-------|
| **n8n** | Self-hosted ∞ | Cloud $20/mês (R$100) | Low-code | Melhor para workflows visuais + integrações |
| **Make** | 1.000 ops/mês | A partir de $9/mês (R$45) | No-code | Fácil para não-devs, muitas integrações |
| **Zapier** | 100 tarefas/mês | A partir de $19.99/mês (R$100) | No-code | Maior biblioteca de integrações SaaS |
| **LangGraph** | Open-source | — | Code | Agentes com estado complexo e fluxos condicionais |
| **CrewAI** | Open-source | — | Code | Multi-agente com papéis. Fácil de começar. |
| **AutoGen** | Open-source | — | Code | Multi-agente robusto (Microsoft) |
| **Semantic Kernel** | Open-source | — | Code | Stack Microsoft (.NET / Python) |
| **LangChain** | Open-source | — | Code | Base universal. Mais verboso mas muito flexível. |
| **Haystack** | Open-source | — | Code | Foco em NLP e RAG |

---

## 🗃️ Bancos de Dados & Infraestrutura

| Serviço | Gratuito | Pago | Notas |
|---------|---------|------|-------|
| **Supabase** | 500MB, 2 projetos | $25/mês (R$125) | PostgreSQL + Auth + Storage + Realtime |
| **PostgreSQL self-hosted** | Gratuito | Custo de infra | Controle total |
| **Redis** | Open-source | Cloud: $5/mês (R$25) | Cache de sessão, memória de curto prazo |
| **MongoDB Atlas** | 512MB free | A partir de $9/mês (R$45) | Documentos, flexível |
| **Railway** | $5 crédito/mês | ~$5–20/mês (R$25–100) | Backend fácil de fazer deploy |
| **Render** | Free tier (dorme) | A partir de $7/mês (R$35) | Alternativa ao Railway |
| **Fly.io** | Free tier | A partir de $3/mês (R$15) | Containers globais, barato |
| **Vercel** | Free tier | $20/mês (R$100) Pro | Frontend + Edge Functions + AI SDK |
| **Hostinger VPS** | — | R$50–150/mês | Opção já usada pela JET Digital |
| **AWS Lambda** | 1M requests/mês grátis | $0.20/1M requests | Serverless, pay-per-use |

---

## 🔗 Integrações Externas Comuns

| Integração | Custo |
|-----------|-------|
| WhatsApp Business API (via Meta) | ~$0.05–0.15/conversa (~R$0.25–0.75) |
| WhatsApp via WABA + provider | Varia por provider (~R$0.10–0.30/msg) |
| Twilio SMS | ~$0.0075/mensagem |
| SendGrid Email | 100 emails/dia grátis, $19.95/mês (R$100) |
| Resend Email | 3.000 emails/mês grátis, $20/mês (R$100) |
| Stripe Pagamentos | 2.5% + R$0.37 por transação (Brasil) |
| ASAAS Pagamentos | 2.49% boleto, 2.99% cartão |
| Mercado Pago | 4.99% + R$0.49 por transação |

---

## 📦 Frameworks RAG

| Ferramenta | Custo | Melhor para |
|-----------|-------|------------|
| **LangChain** | Open-source | Ecossistema amplo, muitas integrações |
| **LlamaIndex** | Open-source | RAG especializado, indexação avançada |
| **Haystack** | Open-source | NLP avançado, pipelines modulares |

---

## 💡 Estimativas de Custo Total por Porte

### 🟢 MVP (até R$300/mês)
| Componente | Ferramenta | Custo |
|-----------|-----------|-------|
| LLM | Claude 3.5 Haiku ou DeepSeek | R$20–50 |
| Auth | JWT + .env | R$0 |
| Monitoramento | LangSmith free | R$0 |
| Vector store | Chroma local | R$0 |
| Orquestração | n8n self-hosted + CrewAI | R$0 (só infra) |
| Infra | Hostinger VPS / Railway | R$50–100 |
| **TOTAL ESTIMADO** | | **R$70–150/mês** |

### 🟡 Médio (R$300–1.500/mês)
| Componente | Ferramenta | Custo |
|-----------|-----------|-------|
| LLM | Claude 3.5 Sonnet | R$100–500 |
| Auth | Auth0 free + Doppler | R$50 |
| Monitoramento | LangSmith Developer | R$195 |
| Vector store | Weaviate Cloud ou Qdrant | R$0–125 |
| Orquestração | n8n Cloud | R$100 |
| Infra | VPS + Supabase | R$125–200 |
| **TOTAL ESTIMADO** | | **R$570–1.170/mês** |

### 🔴 Enterprise (acima de R$1.500/mês)
| Componente | Ferramenta | Custo |
|-----------|-----------|-------|
| LLM | Claude Opus 4 + roteamento | R$500–2.000 |
| Auth | Okta + Vault | R$300+ |
| Monitoramento | LangSmith Enterprise + Datadog | R$700+ |
| Vector store | Pinecone Enterprise | R$350+ |
| Orquestração | n8n Cloud Business | R$250 |
| Infra | AWS/GCP + Supabase | R$500+ |
| **TOTAL ESTIMADO** | | **R$2.600+/mês** |
