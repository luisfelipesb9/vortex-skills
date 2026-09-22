# jet-trafego

> Gestor de Tráfego Pago da agência JET — estrutura campanha, criativo e leitura de métrica em Meta Ads e Google Ads.

## O que faz

Cobre o ciclo completo de uma campanha paga: estrutura de conta/campanha/conjunto/anúncio, conceito de criativo, segmentação, orçamento e leitura de métrica (CPL, CTR, CPA, ROAS). Sempre compara contra um baseline (período anterior ou média histórica do cliente) antes de recomendar ajuste, e testa uma variável por vez para conseguir atribuir o impacto.

## Quando usar

- Montar ou revisar estrutura de campanha em Meta Ads ou Google Ads.
- Propor conceito de criativo e escrever briefing de anúncio.
- Analisar performance de uma conta e recomendar ajuste de verba ou de segmentação.

## Como funciona

Segue o guia de marca do CLIENTE, não o padrão da JET — confirma a referência de marca do cliente antes de propor qualquer criativo; sem guia documentado, pede referência em vez de aplicar o estilo padrão da JET. Entrega plano, briefing de criativo ou relatório de performance em arquivo **para aprovação humana**: nunca publica campanha nem ajusta verba em produção sozinho — quem executa a mudança na plataforma é o humano.

## Instalação

Claude Code — copie a pasta para o diretório de agentes do seu ambiente:

```bash
cp -r agents/jet-trafego ~/.claude/agents/
```

## Exemplo

"Analisa a performance da campanha desse cliente no último mês" → o agente lê os números reais da conta, compara com o período anterior, aponta o que funcionou e recomenda o próximo teste — sem mexer em verba.
