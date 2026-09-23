---
description: Diagnostico do Vortex Skills — comando de teste detectado, niveis efetivos dos gates, validacao dos frontmatters de agente e erros de hook.
argument-hint: "[--agentes]"
allowed-tools: Bash(python3 -S "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/doutor.py"*), Read
disable-model-invocation: false
---

Rode o diagnostico e apresente o resultado ao usuario.

```bash
python3 -S "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/doutor.py" $ARGUMENTS
```

Depois de rodar:

- Reproduza a saida como veio. Ela ja esta formatada; nao reescreva em prosa.
- Se houver **erro**, explique a consequencia concreta em uma linha cada e ofereca a correcao. Os dois mais comuns:
  - `tools` com namespace MCP fixo → o agente carrega **sem** aquelas ferramentas, em silencio. Corrija removendo a lista e herdando do ambiente.
  - `permissionMode` perigoso → desarma o gate humano e anula o `ask` das fronteiras. Nunca deixe passar.
- Se houver so **avisos**, diga que nada esta quebrado e o que cada um custa na pratica.
- Se `comando teste` vier vazio, diga que os gates que dependem de suite ficam inativos neste projeto por decisao de desenho — nao e falha — e que `.vortex/config.json` com `{"test_command": "..."}` corrige se a deteccao errou.

Para ajustar a severidade de um gate neste projeto, o caminho e `.vortex/config.json`:

```json
{ "niveis": { "fronteiras": "warn" } }
```
