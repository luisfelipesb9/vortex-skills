---
name: jet-subagentes
description: Use ao executar um plano de implementação com tasks majoritariamente independentes, na mesma sessão. Gatilhos: "executa esse plano", "vamos implementar as tasks", "roda o plano com subagentes", ou qualquer situação em que exista um plano de implementação pronto e as tasks não sejam fortemente acopladas entre si.
---

# JET — Desenvolvimento Orientado por Subagentes

Executa um plano despachando um subagente implementador novo por task (o
`jet-implementador`), seguido de uma revisão por task (spec + qualidade,
feita pelo `jet-revisor`), e termina com uma revisão ampla de toda a branch.

**Por que subagentes:** você delega tasks a agentes especializados com
contexto isolado. Ao construir cuidadosamente as instruções e o contexto de
cada um, eles ficam focados e têm mais chance de acertar. Eles nunca devem
herdar o histórico da sua sessão — você monta exatamente o que cada um
precisa. Isso também preserva o seu próprio contexto para o trabalho de
coordenação.

**Princípio central:** subagente novo por task + revisão por task (spec +
qualidade) + revisão ampla no final = alta qualidade, iteração rápida.

**Narração:** entre chamadas de ferramenta, narre no máximo uma linha curta
— o ledger de progresso e os resultados das ferramentas já carregam o
registro.

**Execução contínua:** não pare para confirmar com o humano entre tasks.
Execute todas as tasks do plano sem interromper. Os únicos motivos válidos
para parar são: status BLOQUEADO que você não consegue resolver, ambiguidade
que realmente impede o progresso, ou todas as tasks concluídas. Perguntas
tipo "posso continuar?" e resumos de progresso a cada task desperdiçam o
tempo de quem pediu a execução do plano — execute.

## Quando usar

- Existe um plano de implementação escrito (produzido, por exemplo, pela
  skill `jet-plano`).
- As tasks do plano são majoritariamente independentes entre si (não
  fortemente acopladas).
- Você vai continuar na mesma sessão (sem trocar de sessão/terminal).

Se não há plano ainda, use `jet-brainstorm` e depois `jet-plano` antes de
chegar aqui. Se as tasks são fortemente acopladas (uma depende do estado
interno da outra de forma inseparável), execute manualmente em vez de
paralelizar por subagentes.

## O processo

Para cada task, nesta ordem:

1. Despachar um subagente **implementador** (por padrão, o agent
   `jet-implementador`) com o brief da task.
2. Se o implementador fizer perguntas, responda com contexto completo e
   redespache — não empurre ele para implementar na dúvida.
3. O implementador implementa em TDD, testa, faz commit e se autorrevisa,
   reportando um dos quatro status (ver "Tratando o status do
   implementador" abaixo).
4. Assim que o status for CONCLUIDO (ou CONCLUIDO_COM_RESSALVAS resolvido), monte o
   diff da task e despache o subagente **revisor** (o agent `jet-revisor`)
   com esse diff.
5. O revisor devolve dois vereditos: **conformidade com o spec** e
   **qualidade de código/segurança**. Se qualquer um vier reprovado,
   despache um subagente de correção (pode ser o mesmo implementador) para
   os achados Crítico/Importante e repita a revisão.
6. Só marque a task como concluída (na todo list e no ledger de progresso)
   quando ambos os vereditos vierem aprovados.
7. Passe para a próxima task.

Depois de todas as tasks concluídas, despache uma revisão final de toda a
branch (escopo mais amplo que a revisão por task, olhando o diff completo
contra a base) usando o `jet-revisor` com o range completo, e então siga
para a integração (merge/PR) conforme o fluxo do projeto.

## Pré-voo: revisão do plano antes de começar

Antes de despachar a Task 1, leia o plano inteiro uma vez procurando
conflitos:

- tasks que se contradizem entre si ou com as Restrições Globais do plano;
- qualquer coisa que o plano exija explicitamente mas que a revisão de
  qualidade trataria como defeito (ex.: um teste que não afirma nada,
  duplicação verbatim de um bloco de lógica).

Apresente tudo que encontrar ao humano em uma única pergunta em lote — cada
achado ao lado do trecho do plano que o originou, perguntando qual deve
prevalecer — antes de começar a execução, não uma interrupção por achado no
meio do plano. Se a varredura estiver limpa, siga sem comentário. O loop de
revisão por task continua sendo a rede de segurança para conflitos que só
aparecem durante a implementação.

## Seleção de modelo

Use o modelo menos poderoso que dá conta de cada papel, para economizar
custo e ganhar velocidade.

- **Tasks mecânicas** (funções isoladas, spec clara, 1-2 arquivos): modelo
  rápido e barato.
- **Tasks de integração/julgamento** (coordenação multi-arquivo, padrões,
  debugging): modelo padrão.
- **Tasks de arquitetura/design**, incluindo a **revisão final de branch**:
  o modelo mais capaz disponível.
- **Revisões por task**: escolha o modelo pelo mesmo critério, escalado ao
  tamanho, complexidade e risco do diff. Um diff pequeno e mecânico não
  precisa do modelo mais caro; uma mudança sutil de concorrência precisa.

**Sempre especifique o modelo explicitamente ao despachar um subagente.**
Se você omitir, ele herda o modelo da sua sessão — em geral o mais caro —
o que anula essa economia silenciosamente.

**Número de turnos pesa mais que preço por token.** Tempo de parede e custo
de contexto escalam com quantos turnos o subagente gasta, e modelos baratos
costumam gastar 2-3x mais turnos em trabalho multi-etapa — saindo mais caro
no total. Use um modelo intermediário como piso para revisores e para
implementadores que trabalham a partir de descrição em prosa. Quando o
texto da task já contém o código completo a escrever, a implementação é
transcrição + teste: aí sim use o nível mais barato. Correções mecânicas de
um arquivo só também cabem no nível mais barato.

## Tratando o status do implementador

O `jet-implementador` reporta um dos quatro status:

- **CONCLUIDO:** monte o pacote de revisão (commit list + diff da task, veja
  "Como entregar artefatos" abaixo) e despache o `jet-revisor`.
- **CONCLUIDO_COM_RESSALVAS:** a task foi concluída mas o implementador sinalizou
  dúvidas. Leia as preocupações antes de seguir. Se forem sobre
  corretude/escopo, resolva antes da revisão. Se forem só observações (ex.:
  "esse arquivo está ficando grande"), registre e siga para a revisão.
- **FALTA_CONTEXTO:** falta informação que não foi fornecida. Forneça o
  contexto que falta e redespache.
- **BLOQUEADO:** o implementador não consegue concluir. Avalie o bloqueio:
  1. Se é falta de contexto, forneça mais contexto e redespache no mesmo
     modelo.
  2. Se a task exige mais raciocínio, redespache com um modelo mais capaz.
  3. Se a task é grande demais, quebre em pedaços menores.
  4. Se o problema é o próprio plano, escale para o humano.

**Nunca** ignore uma escalada nem force o mesmo modelo a tentar de novo sem
mudar nada. Se o implementador disse que travou, alguma coisa precisa
mudar.

## Tratando itens "⚠️ não dá para verificar pelo diff" do revisor

O `jet-revisor` pode reportar itens que exigem contexto que não está no
diff (requisito que vive em código não alterado, ou que atravessa várias
tasks). Isso não bloqueia o resto da revisão, mas você precisa resolver
cada item pessoalmente antes de marcar a task como concluída — você é
quem tem o plano e o contexto entre tasks que o revisor não tem. Se
confirmar que é uma lacuna real, trate como reprovação de spec: devolva ao
implementador e reabra a revisão.

## Como montar o pedido de revisão

Revisões por task são gates com escopo de uma task. A revisão ampla
acontece uma vez, no final, sobre toda a branch. Ao preparar o pedido para
o `jet-revisor`:

- Não adicione instruções abertas tipo "confira todos os usos" ou "rode
  testes de race se for útil" sem um motivo concreto e específico da task.
- Não peça ao revisor para rerrodar testes que o implementador já rodou no
  mesmo código — o relatório do implementador já carrega essa evidência.
- Não pré-julgue achados pelo revisor — nunca instrua o revisor a ignorar
  ou não sinalizar algo. Se você acha que um achado seria falso positivo,
  deixe o revisor levantar e resolva no loop de revisão. Se o texto que
  você está escrevendo contém "não sinalize", "não trate X como defeito",
  "no máximo Menor" ou "o plano escolheu" — pare: você está pré-julgando,
  geralmente para poupar a si mesmo de um loop de revisão.
- O bloco de restrições globais que você entrega ao revisor é a lente de
  atenção dele. Copie os requisitos vinculantes literalmente da seção de
  Restrições Globais do plano ou do spec: valores exatos, formatos exatos,
  e as relações declaradas entre componentes ("mesmo layout de X", "casa
  com Y"). O próprio revisor já sabe as regras de processo (YAGNI, higiene
  de teste, método de revisão) — o bloco de restrições é para o que ESTE
  projeto exige.
- Entregue ao revisor o diff da task como arquivo — não cole o diff inteiro
  na conversa. Gere o diff (por exemplo, `git log --oneline`, `git diff
  --stat` e `git diff -U10` para o range da task, redirecionado para um
  arquivo com nome único) e passe o caminho do arquivo ao revisor. Isso
  mantém o output fora do seu próprio contexto e dá ao revisor a lista de
  commits, o resumo e o diff completo com contexto em uma única leitura.
  Use como base a revisão de commit registrada antes de despachar o
  implementador — nunca `HEAD~1`, que trunca silenciosamente tasks com
  múltiplos commits.
- Um pedido de despacho descreve uma task, não o histórico da sessão. Não
  cole resumos acumulados de tasks anteriores ("estado após as Tasks 1-3")
  em despachos posteriores. Um subagente novo precisa da sua task, das
  interfaces que ela toca e das restrições globais. Nada além disso.
- Despache um subagente de correção para achados Crítico e Importante.
  Registre achados Menores no ledger de progresso conforme avança, e
  aponte a revisão final de branch para essa lista, para que ela triagem o
  que precisa ser corrigido antes do merge. Uma lista consolidada que
  ninguém lê é um descarte silencioso.
- Um achado rotulado "mandado pelo plano" — ou qualquer achado que conflite
  com o que o texto do plano exige — é decisão do humano, como qualquer
  contradição de plano: apresente o achado e o texto do plano, pergunte
  qual prevalece. Não descarte o achado só porque o plano manda, e não
  despache uma correção que contraria o plano sem perguntar.
- Todo despacho de correção carrega o mesmo contrato do implementador: o
  subagente de correção roda de novo os testes que cobrem a mudança e
  reporta os resultados. Nomeie os arquivos de teste relevantes no
  despacho — uma correção de uma linha não precisa da suíte inteira. Antes
  de redespachar o revisor, confirme que o relatório de correção contém os
  testes cobertos, o comando rodado e o output; só então despache a
  re-revisão.
- Se a revisão final de branch retornar achados, despache UM subagente de
  correção com a lista completa — não um corretor por achado. Corretores
  por achado individual reconstroem contexto e rerrodam suítes a cada vez;
  isso pode custar mais que todas as tasks somadas.

## Como entregar artefatos (briefs, diffs, relatórios)

Tudo que você cola num pedido de despacho — e tudo que um subagente
devolve na resposta — fica residente no seu contexto pelo resto da sessão
e é relido a cada turno seguinte. Entregue artefatos como arquivos:

- **Brief da task:** antes de despachar um implementador, extraia o texto
  completo da task do plano para um arquivo com nome único (ex.:
  `task-N-brief.md`) e componha o despacho para que o brief seja a fonte
  única dos requisitos. Seu despacho deve conter: (1) uma linha sobre onde
  essa task se encaixa no projeto; (2) o caminho do brief, apresentado como
  "leia isso primeiro — são os seus requisitos, com os valores exatos a
  usar"; (3) interfaces e decisões de tasks anteriores que o brief não pode
  saber; (4) sua resolução de qualquer ambiguidade que você notou no
  brief; (5) o caminho do arquivo de relatório e o contrato de relatório.
  Valores exatos (números, strings mágicas, assinaturas, casos de teste)
  aparecem só no brief.
- **Arquivo de relatório:** nomeie o relatório do implementador a partir do
  brief (brief `task-N-brief.md` → relatório `task-N-report.md`) e informe
  o caminho no despacho. O implementador escreve o relatório completo lá e
  retorna na resposta só o status, os commits, um resumo de uma linha dos
  testes e as preocupações.
- **Entradas do revisor:** o `jet-revisor` recebe três caminhos — o mesmo
  brief, o arquivo de relatório e o pacote de diff — mais as restrições
  globais que vinculam a task.
- Despachos de correção anexam o relatório de correção (com resultados de
  teste) ao mesmo arquivo de relatório e retornam um resumo curto;
  re-revisões leem o arquivo atualizado.

## Progresso durável (ledger)

Memória de conversa não sobrevive a compactação. Controladores que
perderam o rumo já rechamaram sequências inteiras de tasks já concluídas —
o erro mais caro observado. Rastreie o progresso num arquivo de ledger, não
só na todo list.

- No início da execução, verifique se já existe um ledger de progresso
  (ex.: `.jet/sdd/progress.md` na raiz do projeto). Tasks lá marcadas como
  concluídas estão CONCLUIDO — não redespache; retome na primeira task não
  marcada.
- Quando a revisão de uma task vier limpa, adicione uma linha ao ledger na
  mesma mensagem em que você faz o resto da contabilidade: `Task N:
  concluída (commits <base7>..<head7>, revisão limpa)`.
- O ledger é o seu mapa de recuperação: os commits que ele nomeia existem
  no git mesmo quando seu contexto não lembra mais de tê-los criado. Depois
  de uma compactação, confie no ledger e no `git log`, não na sua memória.
- Operações destrutivas de limpeza do repositório podem apagar o ledger se
  ele estiver fora do controle de versão; se isso acontecer, reconstrua a
  partir do `git log`.

## Exemplo de fluxo

```
Você: Vou usar Desenvolvimento Orientado por Subagentes para executar este plano.

[Lê o plano uma vez: .jet/sdd/plans/feature-plano.md]
[Cria todos para todas as tasks]

Task 1: Script de instalação do hook

[Extrai o brief da Task 1; despacha jet-implementador com brief + caminho
 de relatório + contexto]

Implementador: "Antes de começar - o hook deve ser instalado a nível de
usuário ou de sistema?"

Você: "Nível de usuário (~/.config/jet/hooks/)"

Implementador: "Entendido. Implementando agora..."
[Depois] Implementador:
  - Implementou o comando install-hook
  - Adicionou testes, 5/5 passando
  - Autorrevisão: percebeu que faltava a flag --force, adicionou
  - Fez commit

[Monta o pacote de diff, despacha jet-revisor com o caminho]
jet-revisor: Spec ✅ - todos os requisitos atendidos, nada extra.
  Pontos fortes: boa cobertura de teste, limpo. Problemas: nenhum.
  Qualidade da task: Aprovada.

[Marca Task 1 concluída]

Task 2: Modos de recuperação

[Extrai o brief da Task 2; despacha jet-implementador com brief + caminho
 de relatório + contexto]

Implementador: [Sem perguntas, segue direto]
Implementador:
  - Adicionou modos verify/repair
  - 8/8 testes passando
  - Autorrevisão: tudo certo
  - Fez commit

[Monta o pacote de diff, despacha jet-revisor com o caminho]
jet-revisor: Spec ❌:
  - Faltando: relatório de progresso (spec pede "reportar a cada 100 itens")
  - Extra: adicionou flag --json (não pedida)
  Problemas (Importante): número mágico (100)

[Despacha subagente de correção com todos os achados]
Corretor: Removeu --json, adicionou relatório de progresso, extraiu
  constante PROGRESS_INTERVAL

[jet-revisor revisa de novo]
jet-revisor: Spec ✅. Qualidade da task: Aprovada.

[Marca Task 2 concluída]

...

[Depois de todas as tasks]
[Despacha revisão final de toda a branch com jet-revisor]
Revisor final: todos os requisitos atendidos, pronto para merge

Concluído!
```

## Vantagens

**vs. execução manual:**
- Subagentes seguem TDD naturalmente (ver `jet-tdd`).
- Contexto novo por task (sem confusão acumulada).
- Seguro para paralelizar (subagentes não interferem entre si).
- O subagente pode perguntar (antes E durante o trabalho).

**Ganhos de eficiência:**
- O controlador cura exatamente o contexto necessário; artefatos volumosos
  viajam como arquivos, não como texto colado.
- O subagente recebe a informação completa de uma vez.
- Perguntas surgem antes do trabalho começar (não depois).

**Gates de qualidade:**
- A autorrevisão pega problemas antes da entrega.
- A revisão por task carrega dois vereditos: conformidade com o spec e
  qualidade de código.
- Os loops de revisão garantem que as correções realmente funcionam.
- Conformidade com spec evita construir a mais ou a menos.
- Qualidade de código garante que a implementação está bem construída.

**Custo:**
- Mais invocações de subagente (implementador + revisor por task).
- O controlador faz mais preparo (extrair todas as tasks com antecedência).
- Loops de revisão adicionam iterações.
- Mas pega problemas cedo (mais barato que debugar depois).

## Sinais de alerta

**Nunca:**
- Comece implementação na branch principal sem consentimento explícito do
  humano.
- Pule a revisão por task, ou aceite um relatório sem os dois vereditos
  (conformidade com spec E qualidade da task são ambos obrigatórios).
- Siga em frente com problemas não corrigidos.
- Despache múltiplos subagentes de implementação em paralelo (geram
  conflito).
- Faça um subagente ler o plano inteiro (entregue o brief da task dele,
  não o plano completo).
- Pule o contexto de cena (o subagente precisa entender onde a task se
  encaixa).
- Ignore perguntas do subagente (responda antes de deixá-lo seguir).
- Aceite "está quase lá" em conformidade com spec (revisor achou problema
  de spec = não está pronto).
- Pule loops de revisão (revisor achou problema = implementador corrige =
  revisa de novo).
- Deixe a autorrevisão do implementador substituir a revisão real (ambas
  são necessárias).
- Diga ao revisor o que não sinalizar, ou pré-classifique a severidade de
  um achado no despacho ("trate como Menor no máximo") — o código de
  exemplo do plano é um ponto de partida, não evidência de que suas
  fraquezas foram escolhidas de propósito.
- Despache um revisor sem um arquivo de diff — gere primeiro e nomeie o
  caminho no pedido.
- Avance para a próxima task enquanto a revisão tiver problemas abertos de
  Crítico/Importante.
- Redespache uma task que o ledger de progresso já marca como concluída —
  confira o ledger (e o `git log`) depois de qualquer compactação ou
  retomada.

**Se o subagente fizer perguntas:**
- Responda de forma clara e completa.
- Forneça contexto adicional se necessário.
- Não apresse a implementação.

**Se o revisor encontrar problemas:**
- O implementador (mesmo subagente) corrige.
- O revisor revisa de novo.
- Repita até aprovar.
- Não pule a re-revisão.

**Se o subagente falhar na task:**
- Despache um subagente de correção com instruções específicas.
- Não tente corrigir manualmente (isso polui o contexto do controlador).

## Integração com outras skills e agents

- **`jet-brainstorm`** — explora intenção e requisitos antes de existir
  qualquer plano.
- **`jet-plano`** — produz o plano de implementação que esta skill executa.
- **`jet-verificacao`** — aplique a mentalidade de evidência antes de
  afirmar antes de qualquer alegação de "pronto", tanto sua quanto a dos
  subagentes.
- **Agent `jet-implementador`** — implementador padrão por task, segue TDD
  (`jet-tdd`).
- **Agent `jet-revisor`** — revisor por task (spec + qualidade) e da
  revisão final de branch.
