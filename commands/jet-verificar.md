---
description: Roda o comando de teste detectado, mais lint e typecheck, e imprime o output cru como evidencia.
allowed-tools: Bash
---

Descubra o comando de teste do projeto e rode-o. Rode também lint e typecheck, se o projeto tiver.

```bash
python3 -S "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/doutor.py" | grep 'comando teste'
```

Depois rode o comando que ele reportou, **completo, sem filtrar**, e apresente o output cru.

Este comando **não** roda em contexto forkado, e isso é deliberado: o ponto inteiro é a evidência ficar no contexto onde a alegação vai ser feita. Evidência em outro contexto não é evidência.

Ao final, diga o estado real — quantos passaram, quantos falharam, exit code. Se falhou, não suavize: `jet-verificacao` existe exatamente para esse momento.
