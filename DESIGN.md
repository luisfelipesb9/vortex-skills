# DESIGN — o terminal é a interface

Este plugin não tem tela, e não deveria ter. Sua interface é o picker de agentes, o texto que os
gates imprimem, os relatórios que os agentes devolvem e o README. Este documento é o contrato
dessas superfícies: se algo que o sistema imprime não segue o que está aqui, é bug de design.

**A regra que ordena todas as outras:** um marcador por eixo de informação. Nada decorativo.
Quem lê isso está no meio de uma tarefa, não navegando por prazer.

---

## 1. Identidade dos agentes

A cor agrupa por time. Quem abre o picker com 15 agentes precisa achar o certo numa passada de
olho — é a única informação que a cor carrega, e ela não carrega mais nenhuma.

| Time | Cores | Agentes |
|---|---|---|
| **Dev** (frios) | `blue` `cyan` `purple` `green` `magenta` | implementador, dev-backend, dev-frontend, dev-dados, dev-devops |
| **Processo** (sinal) | `yellow` `red` `cyan` `blue` | maestro, revisor, pesquisador, doc |
| **Agência** (quentes) | `orange` `red` `yellow` `pink` `magenta` `purple` | copywriter, tráfego, seo, analista-dados, gestor-projetos, designer |

Dentro de um time, cores distintas. Entre times elas se repetem — o time já está separado pelo
contexto em que você chama o agente.

**`description` — no máximo 25 palavras.** É o que renderiza no picker, lado a lado com as outras
catorze. Ela responde *quando eu chamo este agente* e *o que o distingue do vizinho*. Tudo que for
"como ele trabalha" pertence ao corpo do agente, que só carrega depois que ele é escolhido.
O validador (`doutor.py`) reprova acima de 25.

**`displayName`** — o nome curto, sem prefixo `vortex-`. "Revisor", não "vortex-revisor".

---

## 2. Vocabulário de saída

O humano lê isso dezenas de vezes por dia. Formato estável vale mais que formato bonito: o olho
aprende onde olhar e para de ler a linha inteira.

### Toda mensagem de gate

```
[VORTEX/<gate>] <veredito em uma linha>
<contexto factual, uma informação por linha, alinhado>
<o que fazer agora — imperativo, concreto>
<como desligar, quando aplicável>
```

`<gate>` é `fronteiras`, `ledger`, `tdd`, `verificacao` ou `doutor`. O prefixo existe para o leitor
saber, antes de ler o resto, **quem** está falando e se aquilo é do plugin ou do projeto.

Exemplo real, do gate de fronteiras:

```
[VORTEX/fronteiras] Bloqueado: merge.
O time entrega via PR; merge é gate humano.
Abra o PR (`gh pr create`) e pare.
Desativar neste projeto: .vortex/config.json → {"niveis":{"fronteiras":"warn"}}
```

### Severidade — três níveis, um marcador cada

| Nível | Marca | Quando |
|---|---|---|
| Erro | `ERRO ` | Quebra algo agora. Exige ação. |
| Aviso | `aviso` | Custa alguma coisa, não quebra. |
| Nada | *(sem marca)* | Informação. |

Alinhados em coluna, largura fixa, minúsculas exceto `ERRO`. **Sem emoji, sem cor ANSI, sem
caixa desenhada.** O terminal do leitor já tem tema; competir com ele é ruído. A exceção é o
`✓`/`✘` de um resultado binário e único, nunca em lista.

### Veredito do `vortex-revisor` — dois eixos, nunca fundidos

Código pode passar num eixo e falhar no outro; fundir os dois esconde exatamente a informação que
importa. Os dois aparecem sempre, mesmo quando ambos passam.

```
Spec        ✓ todos os requisitos atendidos, nada extra
Qualidade   ✘ 1 importante, 2 menores

  IMPORTANTE  src/retry.ts:34   número mágico (3) sem constante nomeada
  menor       src/retry.ts:12   nome `doIt` não descreve o comportamento
```

`file:line` sempre — é o que torna o achado clicável e acionável.

### `statusMessage` de hook

Minúsculas, sem ponto final, no máximo 4 palavras, verbo no gerúndio ou substantivo:
`Vortex: fronteiras`, `Vortex: lendo ledger`. Isso pisca por milissegundos; frase completa ali é ruído.

### Relatório de agente

Fecha com **estado, não com narrativa**: o que entregou, onde ficou o arquivo, o que falta.
Nada de "espero que ajude", nada de recapitular o que já está no diff.

---

## 3. README e página do sistema

O README é a vitrine. Ordem obrigatória: **o que é** (uma frase que alguém repete para um colega),
**mostrar funcionando** (asciinema ou GIF, antes de qualquer tabela — é a única coisa que vende
ferramenta de dev), **como instalar**, **o que cada peça faz**, **o que é garantido por máquina e
o que é convenção**, atribuição.

A página do sistema é **gerada a partir dos frontmatters**, nunca escrita à mão. Documentação
paralela diverge do código em semanas; documentação derivada não pode divergir.

---

## 4. Idioma

Tudo em **pt-BR**: agentes, skills, mensagens de gate, commits, documentação.

Os identificadores que o Claude Code interpreta ficam como o runtime espera (`PreToolUse`,
`permissionDecision`, `disallowedTools`). Os que **nós** definimos são pt-BR — daí
`CONCLUIDO_COM_RESSALVAS` e não `DONE_WITH_CONCERNS`. A fronteira é: se o runtime lê, é dele; se só
nós lemos, é nosso.
