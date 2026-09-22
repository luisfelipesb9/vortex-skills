# jet-revisor

> Revisa o diff de uma task em dois eixos — conformidade com o spec e qualidade/segurança — e devolve vereditos com evidência.

## O que faz

Revisa o diff de UMA task contra o spec original e contra um baseline de qualidade e segurança (padrões de código, OWASP, testes). Devolve dois vereditos independentes — spec e qualidade — cada um com findings classificados por severidade, `file:line`, impacto e remediação sugerida. Não corrige nada: aponta.

## Quando usar

- Como gate por task, antes de abrir PR ou de seguir para a próxima etapa do plano.
- Quando você quer confirmar se o que foi implementado é o que o spec pediu (nem menos, nem "a mais" fora do escopo).
- Para checar qualidade de código e segurança (injection, IDOR, segredo commitado, XSS) num diff específico.

## Como funciona

1. Confirma que entendeu a intenção da task em uma frase; se não conseguir, devolve pedindo esclarecimento em vez de revisar às cegas.
2. Valida o diff (ref existe, não é ruído de main) antes de começar.
3. Avalia conformidade com o spec primeiro (faltando, extra/scope creep, mal-entendido) — não faz sentido julgar qualidade de código que resolve a coisa errada.
4. Avalia qualidade (smells, design, testes) e segurança (baseline OWASP) do que foi implementado.
5. Reporta dois vereditos separados (spec e qualidade), cada um com findings priorizados e pelo menos uma força específica.

**Fronteira de segurança:** somente leitura — não altera a árvore de arquivos, não aprova nem mergeia. É um gate consultivo: quem decide seguir ou não é o humano ou o próximo passo do fluxo.

## Instalação

Claude Code — copie a pasta para o diretório de agentes do seu ambiente:

```bash
cp -r agents/jet-revisor ~/.claude/agents/
```

## Exemplo

"Revisa o diff da task 3 antes de eu abrir o PR" → o revisor confirma a intenção da task, roda a comparação de spec, depois qualidade e segurança, e devolve os dois vereditos com findings acionáveis — sem tocar em nenhum arquivo.
