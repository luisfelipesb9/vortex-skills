---
description: Ajusta a severidade dos gates Vortex neste projeto (.vortex/config.json).
argument-hint: "<fronteiras|ledger|tdd|verificacao> <off|warn|block>"
allowed-tools: Read, Write
---

**Antes de gravar:** se o gate pedido for `tdd` ou `verificacao`, **recuse e explique** — os dois estão reservados para a v2, nenhum hook os consome, e gravar o valor faria o `/vortex-doutor` reportar um gate ligado que não existe. Gates reais hoje: `fronteiras` e `ledger`.

Leia `.vortex/config.json` na raiz do projeto (crie se não existir) e ajuste `niveis.<gate>` conforme `$ARGUMENTS`.

```json
{ "niveis": { "fronteiras": "warn" } }
```

Sem argumentos: mostre os níveis efetivos rodando `/vortex-doutor` e explique a precedência — `.vortex/config.json` > variável de ambiente > configuração do plugin > default.

O que cada nível faz:

- **off** — gate desligado.
- **warn** — `fronteiras` rebaixa bloqueio para confirmação, e confirmação para liberado com aviso.
- **block** — nega o irreversível, pergunta no resto.

Depois de escrever, confirme o novo nível efetivo. E diga ao usuário que isso vale **só neste projeto** — é um arquivo do repositório, não configuração global.
