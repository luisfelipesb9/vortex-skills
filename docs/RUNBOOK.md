# RUNBOOK — operando o time

Como um humano conduz este time no dia a dia. Tudo aqui descreve o que os arquivos fazem hoje;
onde algo é convenção e não mecanismo, está dito.

---

## 0. O que é garantido por máquina e o que é convenção

Confundir as duas colunas é o jeito mais rápido de se machucar com este plugin.

| Garantido por máquina | Convenção — o modelo pode furar |
|---|---|
| Merge, force-push, push em branch protegida, `gh pr merge` e `reset --hard origin/*` são **negados** | Passar por design antes de codar |
| Deploy de produção, secrets, DNS, terraform, kubectl e Stripe **perguntam** antes de rodar | Um implementador por vez |
| Redespachar task que o ledger marca como concluída é **negado** | Revisão em dois eixos por task |
| Ledger e commits recentes são **reinjetados** no início de sessão e após compactação | Teste escrito antes do código |
| `jet-revisor` **não consegue** escrever arquivo; implementadores **não conseguem** delegar | O teste ter falhado pelo motivo certo |
| Frontmatter inválido **reprova** no CI | |

A coluna da direita é o método. Os gates são o **piso**; o `jet-revisor` é o **teto**. Nenhum dos
dois sozinho fecha.

**Nada disso cobre o commit que você faz no seu terminal.** Isto é enforcement do caminho do
agente, não do repositório. Se quiser cobrir o humano também, a resposta é um `pre-commit` de git —
complementar, não substituto.

---

## 1. Setup

```bash
/plugin marketplace add wearejet/jet-skills
```

```bash
/plugin install jet-skills
```

O Claude Code pergunta 8 chaves de configuração. **Aceite os defaults**, com duas ressalvas:

- `JET_NIVEL_TDD` e `JET_NIVEL_VERIFICACAO` estão marcados "(v2)" e **não fazem nada**. `off` é o
  valor honesto. O `/jet-nivel` recusa alterá-los de propósito.
- `JET_DOCS_PATH` e `JET_LEDGER_PATH`: hoje o maestro e os hooks os respeitam, mas as skills ainda
  hardcodam `.jet/sdd/…`. **Não mude esses dois** por enquanto, ou seus artefatos vão para dois
  lugares diferentes.

Confira que ficou de pé:

```bash
/jet-doutor
```

Leia os quatro blocos. `comando teste` vindo vazio num projeto que **tem** suíte significa que a
detecção errou — corrija com `.jet/config.json` → `{"test_command": "pytest -q"}`. Num projeto sem
suíte, vazio é o resultado certo: os gates que dependem dela se desligam sozinhos.

**Pré-requisitos do projeto:** repositório git com remote, `gh auth status` ok (o fluxo termina em
PR), e trabalhe numa branch de feature — push em `main`/`master`/`prod` é negado. Branch *chamada*
`feat/main-nav` funciona normalmente.

### O que o sistema cria no seu repo

| Caminho | Versionado | Quem escreve |
|---|---|---|
| `.jet/sdd/specs/AAAA-MM-DD-<topico>-design.md` | sim | `jet-brainstorm` |
| `.jet/sdd/plans/AAAA-MM-DD-<feature>.md` | sim | `jet-plano` |
| `.jet/sdd/progress.md` — o ledger | **sim, é o mapa de recuperação** | controlador |
| `.jet/sdd/tasks/task-N-brief.md` e `-report.md` | não | controlador e implementador |
| `.jet/sdd/diffs/<task>.diff` | não | `/jet-diff` |
| `.jet/config.json` | sim | `/jet-nivel` |

O ledger é versionado de propósito: ele só serve se sobreviver a uma limpeza do repositório.

---

## 2. Fluxo A — feature nova

### Etapa 1 · Design *(você presente o tempo todo)*

```bash
/jet-feature exportação de relatório em CSV no painel
```

Digitar a ideia em linguagem natural também funciona — a skill auto-invoca. O comando existe porque
auto-invocação depende da sua frase casar com a descrição, e o HARD-GATE (nada de implementação
antes de design aprovado) só vale se a skill realmente carregar.

Ele explora o repositório, faz **uma pergunta por vez**, propõe 2-3 abordagens com trade-offs — e
despacha o `jet-pesquisador` quando a escolha depende de fato externo (maturidade de biblioteca,
comportamento de API de terceiro, custo), para que as fontes brutas não fiquem residentes no seu
contexto.

**Dois gates seus, e os dois são duros:**

1. Aprovação **após cada seção** do design.
2. Revisão do **spec escrito e commitado**. Ele para e pede. **Abra o arquivo** — é a última vez que
   mudar de ideia é barato.

Espere 10–30 turnos. Não responda "tanto faz": ambiguidade resolvida aqui custa uma pergunta;
descoberta na Task 7 custa um redespacho. Se o pedido for grande demais, ele para e propõe
decompor — aceite, cada subprojeto ganha seu próprio ciclo.

### Etapa 2 · Plano *(automático)*

Você não digita nada: o estado terminal do brainstorm é invocar a `jet-plano`. Se a sessão caiu
entre as duas etapas, `/jet-plano <caminho-do-spec>` retoma.

**Não há gate obrigatório, mas leia o plano.** Três coisas, dois minutos:

- toda tarefa tem caminhos exatos e **código real** em cada passo de código — "adicionar tratamento
  de erro apropriado" é falha de plano declarada, não instrução;
- os nomes de função e tipo batem entre tarefas vizinhas;
- toda tarefa tem o campo **Agente**, e ele bate com os arquivos que ela lista.

Esse campo é o que decide quem implementa. Corrigi-lo aqui custa uma linha; corrigir depois custa um
redespacho.

### Etapa 3 · Execução

| | `executa esse plano` | `/jet-executar <plano.md>` |
|---|---|---|
| Conduz | a própria sessão | `jet-maestro`, em contexto forkado |
| Seu contexto | enche | fica limpo |
| Você vê | tudo, ao vivo | o relatório final |
| Use quando | ≤3 tasks, ou quer acompanhar | >3 tasks |

Ele faz o pré-voo — lê o plano inteiro e, se achar contradições, faz **uma pergunta em lote**.
Responda. Depois disso **ele não te interrompe**, por regra explícita.

Por task: extrai o brief → despacha o agente do campo `Agente` (TDD: RED com falha significativa →
GREEN → suíte uma vez → commit) → monta o diff → despacha o `jet-revisor` → dois vereditos separados
→ linha no ledger só com ambos limpos.

Espere 2–6 despachos por task; um plano de 6 tasks passa de 40–80 turnos. Task que não fecha em três
ciclos de revisão é sinal de plano ruim, não de implementador ruim.

### Etapa 4 · Entrega

Revisão final de toda a branch, triagem dos achados Menores, verificação fresca, push e PR.

- **Na sua sessão:** ele mostra título, base e corpo do PR, pede **uma** confirmação, abre, e grava
  `PR aberto: <url>` no ledger.
- **Em `/jet-executar`:** o maestro roda forkado, onde a pergunta não chega a você. Ele para e
  devolve `Branch <x> pronta, revisão final limpa, N Menores pendentes. Rode /jet-pr para abrir.`

```bash
/jet-pr
```

**Merge é seu, no GitHub.** Nenhum agente faz, e o gate nega — isso não é bug.

### Retomada no meio de uma feature

1. Abra a sessão. O hook imprime `[JET/ledger]` com as tasks concluídas e os commits recentes.
   **Confie nisso, não na sua memória.**
2. `/jet-ledger status` — cruza ledger com `git log` e aponta divergência.
3. `/jet-executar <mesmo plano>` — tasks marcadas são puladas, e agora isso é mecânico: redespachar
   uma task concluída é negado.

---

## 3. Fluxo B — bugfix

Diferente do A em três pontos: a entrada é **sintoma + repro**, não ideia; não há spec nem plano; e
o artefato central é o **teste de regressão**.

Despache direto, com o sintoma como você o viveu:

> `use o jet-dev-backend: /export devolve 500 quando o filtro de data vem vazio — repro: POST com {"from": null}`

Especialista quando o domínio é óbvio, `jet-implementador` quando não é.

Ele é obrigado a construir um **loop de feedback antes de qualquer hipótese** — um sinal pass/fail
que fica vermelho neste bug. Sem loop, ele para e reporta em vez de chutar. E vale a **regra dos 3
fixes**: três tentativas falhas significam problema arquitetural, e ele para.

**Onde você entra:** confirmar a repro — se ele não consegue reproduzir, não deixe ele "consertar",
porque ou a repro está errada ou o bug é outro. E se a regra dos 3 fixes disparar, **volte para o
Fluxo A**: isso é design, não bug.

Antes de aceitar: `/jet-verificar`. Vale também passar pelo revisor — custa um despacho, e ele trata
o relatório do implementador como alegação não verificada.

**Quando um bugfix vira Fluxo A:** toca três ou mais subsistemas, exige mudança de schema, ou a causa
raiz é a ausência de um seam para testar.

---

## 4. Fluxo C — entrega de agência

**Não há loop, ledger, gate nem delegação automática deste lado — e isso é desenho, não lacuna.**
A peça de agência não tem oráculo mecânico: não existe `npm test` para "essa copy está no tom da
marca". O gate final é a aprovação do cliente, que é justamente aquilo pelo qual a agência é paga.
Automatizar o handoff só adiantaria trabalho que o gate humano pode descartar.

**Ponto de entrada, sempre o mesmo:**

> `use o jet-gestor-projetos: <o pedido do cliente, cru, como chegou>`

Ele faz uma pergunta de esclarecimento se o pedido for vago e devolve tarefas no formato
`- [ ] <o quê> — dono: <agente> — prazo: <data> — pronto quando: <critério>`.

**Esse arquivo é o ledger da agência. Versione.** É o que sobrevive à compactação.

Ele **nomeia** o dono; **você despacha**:

| Entrega | Cadeia |
|---|---|
| Campanha | `jet-trafego` (estrutura + briefing de criativo) → `jet-copywriter` (texto fino) → você aprova → você publica |
| Artigo | `jet-seo` (keyword, intenção, brief com H1/H2/H3, cluster) → `jet-copywriter` (versão final quando o tom é comercial) |
| Relatório | `jet-analista-dados` — exige fonte e período antes de analisar, e recusa inventar número |
| Layout | `jet-designer` → handoff para `jet-dev-frontend` quando virar código |
| Site ou sistema | o gestor define escopo e prazo; você troca para o Fluxo A |

**A armadilha cara deste lado é a marca.** O `jet-copywriter` distingue vozes que são opostas entre
si. **Diga de qual marca é a peça na primeira linha do despacho**, e aponte o caminho do guia se ele
existir — copywriter, tráfego e SEO rodam sem o CLAUDE.md do projeto de propósito (convenção de
repositório não é guia de marca de cliente), então dar o caminho economiza uma busca.

Os cinco fecham com estado: o que entregaram, o caminho do arquivo, a fonte e a data do dado, e a
lacuna que ficou por falta de insumo. **Lacuna reportada é o mecanismo deste lado** — não há suíte
para pegar um número inventado.

---

## 5. Fluxo D — retomada após compactação ou sessão nova

O hook roda sozinho no início de sessão e após compactação, e injeta:

```
[JET/ledger] Contexto compactado. Estado real do trabalho, lido do disco:

Tasks ja CONCLUIDAS: 1, 2, 3.
Nao redespache nenhuma delas. Retome na primeira task nao marcada no ledger.
```

Ele só roda na thread principal — um subagente recebe o brief dele e nada mais, de propósito.

**O que você faz:**

1. `/jet-ledger status` — concluídas, a próxima, e divergências entre ledger e git.
2. `/jet-ledger proxima` — uma linha, se você só quer saber onde parou.
3. Ledger sumiu? `/jet-ledger reconstruir` refaz a partir do `git log` e **marca como inferidas** as
   linhas que não deu para deduzir. Leia essas antes de confiar.

**Ledger discorda do git? O git ganha, sempre.** Nunca reescreva o ledger de memória.

---

## 6. Quando **não** usar o pipeline

| Situação | O que fazer |
|---|---|
| Typo, string, bump de versão, formatação | Edite. O pipeline custa dezenas de turnos por uma linha |
| Protótipo descartável | Diga **"protótipo descartável"** explicitamente — a `jet-tdd` se exclui, e o revisor vai exigir que ele seja deletado depois. Não deixe spike virar produção por omissão |
| Exploração ("como funciona X aqui?") | Leia direto. Pesquisa externa vai para o `jet-pesquisador`, que escreve em arquivo |
| Código gerado ou config puro | Fora do escopo da `jet-tdd` por descrição própria |
| Tasks fortemente acopladas | Execute manualmente — subagente em contexto isolado não compartilha estado |
| Uma task só, domínio óbvio | Despache o especialista com o requisito e rode `/jet-verificar` |
| Repo sem remote ou sem `gh` | O passo de PR não se aplica. Se você trabalha direto na main, `/jet-nivel fronteiras warn` rebaixa negar→perguntar |

**Regra de bolso:** o pipeline se paga com 3+ tasks, ou quando errar o design custa mais que 30
turnos de design. Abaixo disso, é cerimônia.

---

## 7. Tabela de decisão

| Quero… | Uso |
|---|---|
| Começar uma feature | `/jet-feature <ideia>` |
| Retomar do spec para o plano | `/jet-plano <spec.md>` |
| Executar um plano acompanhando | `executa esse plano` |
| Executar sem sujar meu contexto | `/jet-executar <plano.md>` |
| Corrigir um bug | despacho direto ao especialista, com sintoma e repro |
| Saber onde parei | `/jet-ledger status` |
| Provar que os testes passam | `/jet-verificar` |
| Montar o diff de uma task | `/jet-diff <base-ref> <task>` |
| Revisar um diff | despachar `jet-revisor` com brief, report e caminho do diff |
| Abrir o PR | `/jet-pr` |
| Fazer merge | **você, no GitHub** |
| Saber se o plugin está de pé | `/jet-doutor` |
| Afrouxar ou apertar um gate | `/jet-nivel fronteiras warn` |
| Pesquisa externa profunda | despachar `jet-pesquisador` |
| ADR, README, runbook | despachar `jet-doc` — sob demanda, fora do pipeline |
| Layout, wireframe, protótipo | despachar `jet-designer` |
| Pedido de cliente virando tarefas | despachar `jet-gestor-projetos` |

---

## 8. Troubleshooting

### 1 · Editou código sem perguntar nada
A auto-invocação não disparou — sua frase não casou com a descrição da skill. Interrompa e diga
`use a skill jet-brainstorm`, e **descarte o que ele escreveu**: código sem spec não tem contra o
que ser revisado. Prevenção: use `/jet-feature`.

### 2 · Um gate bloqueou
Leia o rótulo antes de reagir. `merge`, `push em branch protegida`, `force-push`, `merge de PR` →
**está funcionando**, faça no GitHub. `Acao irreversivel ou externa` → é pergunta, não bloqueio:
confirme se é isso mesmo. Escape: `/jet-nivel fronteiras warn` rebaixa negar→perguntar; `off`
desliga tudo, e aí você sabe o que está abrindo mão.

### 3 · `[JET/ledger] Bloqueado: redespacho da Task N`
O ledger diz que essa task está pronta. Confira com `/jet-ledger status`. Se o trabalho realmente
precisa ser refeito, **edite o ledger primeiro** — remover a linha é a declaração consciente de que
você está reabrindo. O gate existe porque redespachar após compactação é o erro mais caro que este
sistema já cometeu.

### 4 · O agente errado pegou a task
O campo `Agente` do plano está errado. Interrompa **antes** da linha entrar no ledger, corrija o
campo e redespache. O agente errado é instruído a reclamar sozinho (`FALTA_CONTEXTO`) — se ele não
reclamou e o trabalho está bom, deixe: o gate de revisão é o mesmo para todos.

### 5 · Ledger divergiu do git
Dois casos, tratamento oposto. **Linha de task concluída cujos commits não existem** → a alegação é
falsa, remova a linha e reexecute. **Commits que o ledger não registra** → trabalho feito e não
contabilizado: gere o diff, passe pelo revisor, e só então escreva a linha.

### 6 · "Suíte verde" e a suíte está vermelha
Relatório de subagente é **alegação**, não evidência. `/jet-verificar` roda o comando no **seu**
contexto, completo, sem filtro — evidência em outro contexto não é evidência. Falhou? A task não
está pronta: remova a linha do ledger, despache correção **com o output da falha colado**, nomeie os
arquivos de teste relevantes, e exija comando + output no relatório antes de re-revisar.

### 7 · Parou no meio, sem status
Provável teto de `maxTurns` — implementador 60, especialistas 80, revisor 40, maestro 200. O que ele
commitou existe: `git log --oneline` e `/jet-ledger status`, e redespache só o pedaço que falta.
Bateu no teto duas vezes na mesma task? A task é grande demais — quebre em duas no plano.

### 8 · `/jet-doutor` mostra ERRO no frontmatter
`tools` com namespace MCP fixo significa que aquele agente carrega **sem** aquelas ferramentas, em
silêncio — remova a lista e deixe herdar do ambiente. `permissionMode` perigoso desarma o gate
humano e anula as perguntas das fronteiras: nunca deixe passar.
