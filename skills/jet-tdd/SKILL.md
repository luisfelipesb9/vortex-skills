---
name: jet-tdd
description: Use ao implementar qualquer feature ou bugfix, antes de escrever código de implementação. Gatilhos: "implementa isso", "corrige esse bug", "adiciona essa funcionalidade", início de qualquer task de código do time de agentes da JET (jet-implementador, jet-dev-backend, jet-dev-frontend, jet-dev-dados). Não usar em protótipos descartáveis, código gerado ou arquivos de configuração puros — nesses casos, confirme antes com o humano.
---

# jet-tdd — Test-Driven Development do time de agentes da JET

## Visão geral

Escreva o teste primeiro. Veja-o falhar pelo motivo certo. Escreva o código mínimo para passar. Refatore. Commit.

**Princípio central:** se você não viu o teste falhar, não sabe se ele testa a coisa certa.

**Violar a letra da regra é violar o espírito da regra.** Não existe "TDD só no espírito".

Esta skill é o padrão de execução de código de qualquer task do time de agentes da JET. Ela vem **pré-carregada** no frontmatter de `jet-implementador`, `jet-dev-backend`, `jet-dev-frontend` e `jet-dev-dados` (campo `skills:`) — eles não escolhem carregá-la, ela já está no contexto quando a task começa. `jet-revisor` cobra evidência de que o ciclo abaixo foi seguido; `jet-subagentes` é quem despacha a task que aciona esta skill.

## O que é cobrado por máquina e o que depende de você

Ser honesto sobre essa fronteira não enfraquece a disciplina — é o que a torna confiável. Um repositório que promete invariante e entrega heurística destrói a confiança também na parte que **é** dura.

| | Quem garante |
|---|---|
| A skill estar carregada quando você começa a task | **Mecânica** — `skills:` no frontmatter do agente |
| Você não conseguir delegar a task para outro agente | **Mecânica** — `disallowedTools: ["Agent"]` |
| Merge, force-push e push em branch protegida | **Mecânica** — hook de fronteiras, nega antes de executar |
| Teste escrito **antes** do código de produção | **Você.** Nenhum script observa isso hoje |
| O teste ter falhado **pelo motivo certo** | **Você.** É julgamento semântico, não mecanizável |
| O teste que falhou cobrir **este** código | **Você.** Provar isso exigiria cobertura por teste a cada ciclo |
| Teste sem asserção real, tautológico ou acoplado à implementação | **`jet-revisor`**, na revisão por task |

Os gates mecânicos são o **piso**; o `jet-revisor` é o **teto**. Nenhum dos dois sozinho fecha — e no meio, entre um e outro, está a disciplina que esta skill descreve. É por isso que ela é escrita como lei e não como sugestão.

## Quando usar

**Sempre:**
- Feature nova
- Correção de bug
- Refatoração
- Qualquer mudança de comportamento

**Exceções (confirme com o humano antes de pular):**
- Protótipo descartável
- Código gerado automaticamente
- Arquivos de configuração puros (sem lógica)

Se você está pensando "pulo o TDD só dessa vez" — pare. Isso é racionalização, não é uma exceção legítima.

## A Lei de Ferro

```
NENHUM CÓDIGO DE PRODUÇÃO SEM UM TESTE QUE FALHE PRIMEIRO
```

Escreveu código antes do teste? Apague. Comece de novo.

**Sem exceções:**
- Não guarde "como referência"
- Não "adapte" o código enquanto escreve o teste
- Não olhe para ele
- Apagar significa apagar — implemente do zero, a partir dos testes

## O ciclo RED → GREEN → REFACTOR → commit

```
RED (teste falha) → verificar que falhou pelo motivo certo
   → GREEN (implementação mínima) → verificar que passou, tudo verde
      → REFACTOR (limpar, mantendo verde) → commit
         → próximo teste (RED de novo)
```

### RED — escreva o teste que falha

Escreva um teste mínimo mostrando o que deveria acontecer. Uma coisa só, nome claro, código real (mock só se for inevitável).

**Bom exemplo:**
```typescript
test('refaz operação falha 3 vezes antes de desistir', async () => {
  let tentativas = 0;
  const operacao = () => {
    tentativas++;
    if (tentativas < 3) throw new Error('falhou');
    return 'sucesso';
  };

  const resultado = await retryOperation(operacao);

  expect(resultado).toBe('sucesso');
  expect(tentativas).toBe(3);
});
```
Nome claro, testa comportamento real, uma coisa só.

**Ruim (evite):**
```typescript
test('retry funciona', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('sucesso');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Nome vago, testa o mock e não o código real.

### Verificar RED — assista falhar

**Obrigatório. Nunca pule esta etapa.**

Rode o comando de teste do projeto (ex.: `npm test caminho/do/teste.test.ts`, `pytest caminho/do/teste.py`) e confirme:
- O teste falha (não dá erro de execução/typo)
- A mensagem de falha é a esperada
- Falha porque a funcionalidade ainda não existe — não por erro de digitação

Teste passou de primeira? Você está testando comportamento que já existe — corrija o teste.
Teste deu erro (não falha)? Corrija o erro e rode de novo até falhar corretamente.

### GREEN — implementação mínima

Escreva o código mais simples possível para passar o teste. Não adicione recursos, não refatore outra coisa, não "melhore" além do que o teste pede — isso é over-engineering e quebra o ciclo.

**Bom exemplo:**
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('inalcançável');
}
```

**Ruim (evite, YAGNI):**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: { maxRetries?: number; backoff?: 'linear' | 'exponential'; onRetry?: (n: number) => void }
): Promise<T> {
  // ninguém pediu isso ainda
}
```

### Verificar GREEN — assista passar

**Obrigatório.** Rode a suíte de novo e confirme:
- O teste passa
- Os outros testes continuam passando
- Saída limpa (sem erros, sem warnings)

Teste falhou? Corrija o código, não o teste.
Outro teste quebrou? Corrija agora, antes de seguir.

### REFACTOR — limpe

Só depois de verde:
- Remova duplicação
- Melhore nomes
- Extraia helpers

Mantenha os testes verdes. Não adicione comportamento novo nesta etapa.

### Commit

Feche o ciclo com um commit da task (Conventional Commits, conforme o padrão do repo do projeto). Depois, volte ao início: próximo teste que falha, para a próxima fatia de comportamento.

## O que faz um bom teste

| Qualidade | Bom | Ruim |
|---|---|---|
| **Mínimo** | Uma coisa só. Se o nome tem "e", divida. | `test('valida email e domínio e espaços')` |
| **Claro** | Nome descreve o comportamento | `test('teste1')` |
| **Mostra intenção** | Demonstra a API desejada | Esconde o que o código deveria fazer |

Teste comportamento, não implementação: valide entradas e saídas observáveis, não detalhes internos que podem mudar num refactor sem quebrar o comportamento.

## Higiene de teste — evite

- **Asserts vazios ou triviais** (`expect(true).toBe(true)`, teste sem nenhum `expect`) — não provam nada
- **Testar o mock em vez do código real** — se o teste só verifica que um mock foi chamado, ele não valida comportamento
- **Setup gigante escondendo o que está sendo testado** — se o teste precisa de 30 linhas de setup, o design provavelmente está complicado demais
- **Testes que dependem de ordem de execução ou de estado global** — cada teste deve poder rodar isolado
- **Métodos "só para teste" na classe de produção** — se a única razão de existir é o teste, o design está errado; prefira injeção de dependência

## Por que a ordem importa

**"Escrevo os testes depois para verificar que funciona"** — testes escritos depois passam de primeira. Passar de primeira não prova nada: pode estar testando a coisa errada, pode estar testando a implementação em vez do comportamento, pode estar deixando casos de borda passar batido. Você nunca viu o teste pegar o bug.

**"Já testei manualmente todos os casos"** — teste manual é ad-hoc: sem registro do que foi testado, não roda de novo quando o código muda, fácil esquecer casos sob pressão.

**"Apagar X horas de trabalho é desperdício"** — falácia do custo afundado. O tempo já foi gasto; a escolha agora é: apagar e reescrever com TDD (mais confiança) ou manter sem teste real (dívida técnica disfarçada de economia).

**"TDD é dogmático, ser pragmático é adaptar"** — TDD É pragmático: acha bug antes do commit, previne regressão, documenta comportamento, permite refatorar com segurança. "Atalho pragmático" costuma significar debugar em produção depois — isso é mais lento, não mais rápido.

## Racionalizações comuns

| Desculpa | Realidade |
|---|---|
| "Simples demais para testar" | Código simples também quebra. O teste leva 30 segundos. |
| "Testo depois" | Teste que passa de primeira não prova nada. |
| "Testar depois cumpre o mesmo objetivo" | Depois responde "o que isso faz?". Antes responde "o que isso deveria fazer?". |
| "Já testei manualmente" | Ad-hoc não é sistemático. Sem registro, não repete. |
| "Apagar X horas é desperdício" | Custo afundado. Manter código sem teste é a dívida real. |
| "Guardo como referência e escrevo o teste depois" | Você vai adaptar o código existente — isso é testar depois. Apagar é apagar. |
| "Preciso explorar antes" | Tudo bem. Descarte a exploração e comece do zero com TDD. |
| "Teste difícil = design confuso" | Ouça o teste. Difícil de testar é difícil de usar — simplifique a interface. |

## Sinais de alerta — pare e recomece

- Código escrito antes do teste
- Teste escrito depois da implementação
- Teste passa de primeira, sem nunca ter falhado
- Você não consegue explicar por que o teste falhou
- Testes "adicionados depois, no fim"
- Qualquer racionalização do tipo "só dessa vez"

**Qualquer um desses sinais significa: apague o código, comece de novo com TDD.**

## Exemplo — correção de bug

**Bug:** e-mail vazio é aceito no formulário.

**RED**
```typescript
test('rejeita email vazio', async () => {
  const resultado = await submitForm({ email: '' });
  expect(resultado.error).toBe('Email obrigatório');
});
```

**Verificar RED**
```
FAIL: esperado 'Email obrigatório', recebido undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email obrigatório' };
  }
  // ...
}
```

**Verificar GREEN** — suíte passa, saída limpa.

**REFACTOR** — se houver mais campos obrigatórios, extraia a validação para um helper reutilizável, mantendo os testes verdes.

## Checklist de verificação

Antes de marcar a task como concluída:

- [ ] Toda função/método novo tem teste
- [ ] Vi cada teste falhar antes de implementar
- [ ] Cada teste falhou pelo motivo certo (funcionalidade ausente, não erro de digitação)
- [ ] Escrevi o código mínimo para passar cada teste
- [ ] Todos os testes passam
- [ ] Saída limpa (sem erros, sem warnings)
- [ ] Testes usam código real (mock só se inevitável)
- [ ] Casos de borda e de erro estão cobertos

Não consegue marcar todos os itens? Você pulou o TDD. Volte e refaça.

## Quando travar

| Problema | Solução |
|---|---|
| Não sei como testar | Escreva a API desejada primeiro. Escreva o assert antes do resto. Pergunte ao humano se travar. |
| Teste ficou complicado demais | O design está complicado. Simplifique a interface. |
| Preciso mockar tudo | Código acoplado demais. Use injeção de dependência. |
| Setup de teste enorme | Extraia helpers. Se ainda estiver complexo, simplifique o design. |

## Integração com debugging

Bug encontrado? Escreva um teste que falhe reproduzindo o bug. Siga o ciclo RED → GREEN → REFACTOR normalmente. O teste prova a correção e previne regressão. Nunca corrija um bug sem um teste que o reproduza primeiro.

## Regra final

```
Código de produção → existe teste e ele falhou primeiro
Caso contrário → não é TDD
```

Sem exceções sem autorização explícita do humano responsável pela task.
