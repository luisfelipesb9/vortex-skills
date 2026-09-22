# agent-architect

> Guia estruturado para planejar a arquitetura de um agente de IA, camada por camada, com recomendação de ferramentas e custo real.

## O que faz

Conduz o usuário por um roteiro de 9 camadas (segurança, monitoramento, memória, ferramentas, prompting etc.) para desenhar um agente de IA do zero. Classifica o projeto por porte (MVP/Médio/Enterprise) e budget, recomenda uma ferramenta principal por camada — nunca uma lista extensa de opções — com custo estimado. Ao final, gera dois arquivos `.md`: um checklist de decisões e um README técnico completo do agente planejado.

## Quando usar

- "quero criar um agente", "vamos construir um bot", "preciso de um agente de IA".
- "como estruturar um agente", "planejamento de agente", "novo agente", "chatbot com IA".
- "automação com LLM", "agent com n8n", "agent com langchain".
- Qualquer menção a construir ou planejar algo com LLMs, agentes ou AI agents — mesmo sem usar a palavra "agente" (ex.: "bot que faz X", "pipeline de LLM").

## Como funciona

1. Faz uma rodada de perguntas de contexto — o que o agente faz, para quem, budget mensal, prazo, se precisa de memória, se interage com sistemas externos, stack preferida.
2. Classifica o projeto por porte (MVP, Médio ou Enterprise) com base nas respostas.
3. Percorre as 9 camadas do roteiro uma a uma: diz o que é obrigatório ou opcional para aquele projeto e recomenda 1 ferramenta principal (no máximo 1 alternativa), consultando `references/camadas.md` e `references/ferramentas-custo.md`.
4. Ao final, gera o checklist de decisões e o README técnico como arquivos `.md`, usando os templates de `assets/checklist-template.md` e `assets/readme-template.md` preenchidos com as decisões reais da conversa.

## Exemplo

"Quero montar um bot de atendimento no WhatsApp com n8n" → a skill pergunta o contexto do projeto, classifica o porte, percorre as camadas recomendando ferramentas com custo, e fecha entregando `checklist-<nome>.md` e `README-<nome>.md`.
