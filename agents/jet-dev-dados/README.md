# jet-dev-dados

> Especialista de dados do time dev — PostgreSQL: schema, migrações, índices e performance de query.

## O que faz

Implementa uma task de dados — mudança de schema, migração ou tuning de query lenta — sempre com baseline medido antes e depois (`EXPLAIN ANALYZE`, `pg_stat_statements`). Cobre leitura de plano de execução, desenho de índice (composto, parcial, de expressão, BRIN, GIN), SQL set-based e manutenção (autovacuum, `ANALYZE`).

## Quando usar

- Mudança de schema ou índice.
- Query lenta que precisa de tuning com medição antes/depois.
- Migração de banco versionada.
- O código de aplicação que consome o schema é do `jet-dev-backend` — este agente entrega schema/query/índice e o contrato, não reescreve o serviço.
- Não é o agente certo para task sem especialidade dominante ou que mistura áreas por igual — nesse caso, use o `jet-implementador`.

## Como funciona

Testes de banco rodam contra Postgres real (testcontainers ou equivalente), nunca mock. Toda otimização segue: baseline → uma mudança por vez → nova medição → documentar antes/depois. Trabalha em UMA task por vez, entrega via commit na branch com Conventional Commits — **nunca faz merge nem force-push**. Migração destrutiva (`DROP`, `TRUNCATE`, mudança de tipo com perda de dado) contra dado real: o agente interrompe e pede aprovação humana antes de aplicar — não é reversível como um commit.

## Instalação

Claude Code — copie a pasta para o diretório de agentes do seu ambiente:

```bash
cp -r agents/jet-dev-dados ~/.claude/agents/
```

## Exemplo

"A listagem de pedidos está lenta" → o agente captura o `EXPLAIN ANALYZE` atual, identifica o Seq Scan, cria o índice direcionado, mede de novo e documenta o ganho antes de comitar.
