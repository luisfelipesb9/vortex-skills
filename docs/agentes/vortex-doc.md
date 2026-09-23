# vortex-doc

> Escreve e atualiza documentação de engenharia — ADR, README, PRD, runbooks — no padrão e no tom do repositório.

## O que faz

Registra decisões e documenta entregas seguindo os templates e convenções já existentes no repositório (ou o padrão MADR quando não houver template próprio). Escreve sempre em pt-BR, sem placeholders soltos e sem links quebrados.

## Quando usar

- Para registrar uma decisão de arquitetura ou técnica como ADR.
- Para escrever ou atualizar README, PRD ou runbook de um projeto.
- Depois de uma entrega, para deixar documentado o que foi feito e por quê.

## Como funciona

1. Antes de escrever, lê o template do repositório e um exemplo recente do mesmo tipo de documento, e espelha estrutura, cabeçalho e estilo.
2. Para ADR, segue MADR: numeração sequencial sem reutilizar, status inicial `Proposto`, índice atualizado.
3. Escreve sem placeholders/TBD e só com links relativos que resolvem de fato.
4. Ao final, reporta quais arquivos foram criados ou atualizados e um resumo curto do que mudou e por quê.

**Fronteira:** só docs — não implementa código nem faz merge; entrega via commit convencional com trailer.

## Exemplo

"Documenta a decisão de trocar de fila de mensagens" → o vortex-doc lê o template de ADR do repositório, cria o próximo ADR numerado com status `Proposto`, atualiza o índice e reporta o arquivo criado.
