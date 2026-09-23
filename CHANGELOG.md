# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento semântico.

## [1.0.2] — 2026-09-23

### Corrigido

- **O gate de fronteiras não rodava.** Os hooks passavam `--nivel
  ${user_config.VORTEX_NIVEL_FRONTEIRAS}`, e o runtime trata interpolação irresolvível como erro
  **fatal**: numa instalação sem configurar, o hook nem era lançado. O `default` do schema é
  pré-preenchimento de diálogo, não valor materializado. A flag saiu; o nível agora é resolvido
  pelo próprio script (`.vortex/config.json` > env > default), que é onde a defesa sempre esteve.
- **Os testes gravavam no log de produção.** `CLAUDE_PLUGIN_DATA` não era isolado, então
  `log_erro` escrevia em `~/.claude/vortex-skills/erros.jsonl` e o `/vortex-doutor` reportava
  entradas de teste como erro real — o que produziu um diagnóstico errado. Isolado, com teste que
  afirma que o caminho de produção não é tocado.

### Adicionado

- **`/vortex-doutor` agora prova que cada gate está vivo**, não só que está configurado. Ele invoca
  cada hook com entrada sintética de resposta conhecida (`git merge main` tem que ser negado) e
  reporta `ativo` ou `FALHOU — <motivo>`. Sem isso, gate morto e gate que liberou produzem o mesmo
  silêncio — que foi exatamente como o de fronteiras passou uma instalação inteira sem rodar.

## [1.0.1] — 2026-09-23

### Corrigido

- **Nenhum dos 15 agentes carregava.** A estrutura `agents/<nome>/<nome>.md`, herdada do
  repositório original, não é lida por um plugin: agente de plugin carrega só de `agents/*.md` no
  nível raiz. `claude plugin details` reportava `Agents (0)`. Só a instalação real revelou isso —
  sete ciclos de leitura estática não revelaram.
- `commands/vortex-fluxo.md` e `commands/vortex-plano.md` colidiam com as skills de mesmo nome.
  Skill e command dividem namespace; uma skill já é invocável como `/nome`. Os dois commands foram
  removidos e as skills passaram a aceitar argumento.

### Alterado

- Renomeado de `jet-skills` para `vortex-skills` em todo o sistema: caminhos, nome do plugin, chaves
  de configuração (`VORTEX_NIVEL_*`), diretório de artefatos (`.vortex/sdd/`) e o prefixo das
  mensagens de gate (`[VORTEX/<gate>]`). A atribuição MIT a Jesse Vincent no NOTICE não mudou.

## [1.0.0] — 2026-09-22

Primeira versão como plugin do Claude Code. Antes disso a distribuição era `cp -r` de pastas soltas.

### Adicionado

- **Plugin instalável** com `.claude-plugin/plugin.json` e marketplace próprio. Instalação e
  atualização em um comando, com 8 chaves de configuração por projeto.
- **Três gates que rodam como hooks**, todos determinísticos e fail-open:
  - `fronteiras` — nega merge, force-push, push em branch protegida, `gh pr merge` e `reset --hard`
    contra remoto; pergunta antes de deploy de produção, secrets, DNS, terraform, kubectl e ações
    financeiras.
  - `contexto` — reinjeta o ledger e os commits recentes no início de sessão e após compactação.
  - `ledger` — nega redespachar task que o ledger já marca como concluída.
- **10 slash commands**: `/vortex-feature`, `/vortex-plano`, `/vortex-executar`, `/vortex-diff`, `/vortex-ledger`,
  `/vortex-verificar`, `/vortex-pr`, `/vortex-nivel`, `/vortex-doutor`, `/vortex-fluxo`.
- **Passo de abertura de PR** na `vortex-subagentes`. O sistema convergia para "entrega via PR" e
  nenhum agente tinha esse passo — a execução terminava com commits numa branch e parava.
- **`docs/RUNBOOK.md`** e a skill `vortex-fluxo`: como operar o time, encontrável no momento da dúvida.
- **`DESIGN.md`** — contrato da superfície visual (cores por time no picker, prefixo `[VORTEX/<gate>]`,
  severidade com marcador de largura fixa), cobrado por teste.
- **`doutor.py`** — validador de frontmatter. Existe porque `claude plugin validate` só confere a
  presença do bloco: ele aceita `effort` inválido, `maxTurns` negativo e `permissionMode`
  perigoso sem reclamar.
- **75 testes** em stdlib puro, escritos antes da implementação e verificados contra sabotagem.
- **CI** com três gates: testes, validação de frontmatter e `plugin validate`.

### Alterado

- Os 15 agentes migrados de 4 campos de frontmatter para os campos nativos do Claude Code:
  `effort`, `memory`, `skills` (pré-carga), `maxTurns`, `disallowedTools`, `color`, `displayName`,
  `background`, `omitClaudeMd`.
- **Roteamento por especialidade**: cada tarefa do plano declara o campo `Agente`. Antes, o
  cabeçalho injetado em todo plano mandava usar sempre o generalista, e 4 dos 15 agentes nunca
  recebiam trabalho.
- Contrato de status unificado em pt-BR: `CONCLUIDO`, `CONCLUIDO_COM_RESSALVAS`, `FALTA_CONTEXTO`,
  `BLOQUEADO`. A skill descrevia quatro status que o agente nunca emitiu.
- Artefatos unificados sob `.vortex/sdd/` — specs, planos e ledger versionados de propósito; briefs,
  relatórios e diffs fora do histórico.
- `vortex-tdd` deixa de prometer invariante que a mecânica não entrega, e passa a declarar o que é
  cobrado por máquina, o que é do revisor e o que depende do agente.
- Descriptions dos agentes reduzidas de até 77 para no máximo 25 palavras — é o que renderiza no
  picker, lado a lado com as outras catorze.

### Corrigido

- `vortex-maestro` não tinha `Bash` nem `Write` e portanto **não conseguia executar a skill que
  orquestra**: não gerava arquivo de diff nem escrevia o ledger.
- `vortex-designer` carregava 21 ferramentas MCP com namespace fixo que não resolve fora do ambiente
  de origem — o agente subia sem nenhuma ferramenta de Figma, em silêncio.
- O gate de fronteiras negava `git push -u origin feat/main-nav`, porque a palavra protegida casava
  dentro do nome da branch. Push de branch é pré-requisito do PR.
- O mesmo gate negava `git merge-base`, que é leitura pura.
- `vortex-copywriter`, `vortex-trafego` e `vortex-seo` eram mandados a seguir o guia de marca do cliente e
  não tinham `Grep`/`Glob` para encontrá-lo.

### Removido

- A skill `agent-architect`, que não participava do funil e cujos dados de custo exigem ciclo de
  atualização próprio. Íntegra no histórico: `git show db12f21:skills/agent-architect/SKILL.md`.
- As 25 instruções de instalação duplicadas em 22 arquivos.

### Conhecido

- `VORTEX_NIVEL_TDD` e `VORTEX_NIVEL_VERIFICACAO` estão declarados e **não fazem nada** — o aparato que os
  implementaria fica para a v2. `/vortex-nivel` recusa alterá-los, e o `/vortex-doutor` os reporta como
  `off`.
- O enforcement cobre o caminho do agente, não o commit que o humano faz no próprio terminal.
