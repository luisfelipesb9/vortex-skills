---
name: jet-plano
description: "Skill do sistema de agentes da JET. Use quando você tiver um spec ou requisitos definidos para uma tarefa multi-etapas, antes de tocar em código. Transforma o design aprovado (saída da jet-brainstorm) em um plano de implementação bite-sized, testável e pronto para execução por subagentes. Gatilhos: 'temos o spec, agora precisamos do plano', 'como vamos dividir isso em tarefas', 'gera o plano de implementação'."
---

# JET Plano — Escrevendo Planos de Implementação

## Visão geral

Escreva planos de implementação completos assumindo que quem vai executar não tem nenhum contexto prévio da base de código e bom senso questionável. Documente tudo que essa pessoa/agente precisa saber: quais arquivos tocar em cada tarefa, código, testes, docs a consultar, como testar. Entregue o plano inteiro como tarefas mordíveis (bite-sized). DRY. YAGNI. TDD. Commits frequentes.

Assuma que quem executa é um desenvolvedor competente, mas que não conhece nosso stack nem o domínio do problema. Assuma que não domina bem o design de testes.

**Anuncie no início:** "Estou usando a skill jet-plano para criar o plano de implementação."

**Salve os planos em:** `docs/aios-jet/plans/YYYY-MM-DD-<nome-da-feature>.md`
- (Preferências do usuário sobre local do plano sobrescrevem esse padrão)

## Checagem de escopo

Se o spec cobre múltiplos subsistemas independentes, ele já deveria ter sido quebrado em subprojetos durante o brainstorm (skill `jet-brainstorm`). Se não foi, sugira quebrar isto em planos separados — um por subsistema. Cada plano deve produzir software funcional e testável por si só.

## Estrutura de arquivos

Antes de definir as tarefas, mapeie quais arquivos serão criados ou modificados e qual a responsabilidade de cada um. É aqui que as decisões de decomposição ficam travadas.

- Desenhe unidades com fronteiras claras e interfaces bem definidas. Cada arquivo deve ter uma responsabilidade clara.
- Agentes raciocinam melhor sobre código que cabe no contexto de uma vez, e as edições ficam mais confiáveis quando os arquivos são focados. Prefira arquivos menores e focados a arquivos grandes que fazem coisa demais.
- Arquivos que mudam juntos devem morar juntos. Divida por responsabilidade, não por camada técnica.
- Em bases de código existentes, siga os padrões já estabelecidos. Se a base usa arquivos grandes, não reestruture unilateralmente — mas se um arquivo que você está modificando cresceu demais, incluir uma divisão no plano é razoável.

Essa estrutura informa a decomposição das tarefas. Cada tarefa deve produzir mudanças autocontidas que fazem sentido de forma independente.

## Dimensionamento das tarefas

Uma tarefa é a menor unidade que carrega seu próprio ciclo de teste e que vale um gate de revisão por um revisor com olhos frescos (skill `jet-revisor`). Ao desenhar as fronteiras das tarefas: dobre setup, configuração, scaffolding e passos de documentação dentro da tarefa cujo entregável precisa deles; só divida onde um revisor poderia rejeitar significativamente uma tarefa e aprovar a vizinha. Cada tarefa termina com um entregável testável de forma independente.

## Granularidade bite-sized

**Cada passo é uma ação (2-5 minutos):**
- "Escrever o teste que falha" — passo
- "Rodar para garantir que falha" — passo
- "Implementar o código mínimo para o teste passar" — passo
- "Rodar os testes e garantir que passam" — passo
- "Commit" — passo

## Cabeçalho do documento de plano

**Todo plano DEVE começar com este cabeçalho:**

```markdown
# Plano de Implementação: [Nome da Feature]

> **Para quem for executar:** SUB-SKILL OBRIGATÓRIA: use a skill `jet-subagentes` para implementar este plano tarefa por tarefa, com um agente `jet-implementador` por tarefa e revisão via `jet-revisor` entre tarefas. Passos usam sintaxe de checkbox (`- [ ]`) para rastreamento.

**Objetivo:** [Uma frase descrevendo o que isso constrói]

**Arquitetura:** [2-3 frases sobre a abordagem]

**Stack técnica:** [Principais tecnologias/bibliotecas]

## Restrições globais

[Os requisitos de escopo do projeto vindos do spec — versões mínimas, limites
de dependências, regras de nomenclatura e copy, requisitos de plataforma —
uma linha cada, com valores exatos copiados literalmente do spec. Os
requisitos de toda tarefa incluem implicitamente esta seção.]

---
```

## Estrutura de tarefa

````markdown
### Tarefa N: [Nome do Componente]

**Arquivos:**
- Criar: `caminho/exato/para/arquivo.py`
- Modificar: `caminho/exato/para/existente.py:123-145`
- Teste: `tests/caminho/exato/para/test.py`

**Interfaces:**
- Consome: [o que esta tarefa usa de tarefas anteriores — assinaturas exatas]
- Produz: [o que tarefas posteriores vão depender — nomes exatos de funções,
  tipos de parâmetro e retorno. Quem implementa uma tarefa vê só a própria
  tarefa; este bloco é como ele aprende os nomes e tipos usados pelas
  tarefas vizinhas.]

- [ ] **Passo 1: Escrever o teste que falha**

```python
def test_comportamento_especifico():
    resultado = funcao(entrada)
    assert resultado == esperado
```

- [ ] **Passo 2: Rodar o teste para confirmar que falha**

Rodar: `pytest tests/caminho/test.py::test_nome -v`
Esperado: FAIL com "função não definida"

- [ ] **Passo 3: Escrever a implementação mínima**

```python
def funcao(entrada):
    return esperado
```

- [ ] **Passo 4: Rodar o teste para confirmar que passa**

Rodar: `pytest tests/caminho/test.py::test_nome -v`
Esperado: PASS

- [ ] **Passo 5: Commit**

```bash
git add tests/caminho/test.py src/caminho/arquivo.py
git commit -m "feat: adiciona comportamento específico"
```
````

Use TDD (skill `jet-tdd`) como referência para o ciclo RED → GREEN → commit em cada tarefa.

## Sem placeholders

Todo passo precisa conter o conteúdo real que quem implementa precisa. Isso são **falhas de plano** — nunca escreva:
- "TBD", "TODO", "implementar depois", "preencher detalhes"
- "Adicionar tratamento de erro apropriado" / "adicionar validação" / "tratar casos extremos"
- "Escrever testes para o que foi feito acima" (sem o código do teste de fato)
- "Similar à Tarefa N" (repita o código — quem implementa pode estar lendo as tarefas fora de ordem)
- Passos que descrevem o que fazer sem mostrar como (blocos de código são obrigatórios em passos de código)
- Referências a tipos, funções ou métodos não definidos em nenhuma tarefa

## Lembretes

- Caminhos de arquivo exatos sempre
- Código completo em cada passo — se um passo muda código, mostre o código
- Comandos exatos com output esperado
- DRY, YAGNI, TDD, commits frequentes

## Autorrevisão

Depois de escrever o plano completo, releia o spec com olhos frescos e confira o plano contra ele. Isto é um checklist que você mesmo roda — não é um dispatch de subagente.

**1. Cobertura do spec:** Percorra cada seção/requisito do spec. Dá para apontar uma tarefa que a implementa? Liste as lacunas.

**2. Varredura de placeholder:** Busque no plano os sinais de alerta da seção "Sem placeholders" acima. Corrija.

**3. Consistência de tipos:** Os tipos, assinaturas de método e nomes de propriedade usados em tarefas posteriores batem com o que foi definido nas tarefas anteriores? Uma função chamada `limparCamadas()` na Tarefa 3 mas `limparCamadasCompleto()` na Tarefa 7 é um bug.

Se encontrar problemas, corrija inline. Não precisa revisar de novo — só corrija e siga em frente. Se encontrar um requisito do spec sem tarefa correspondente, adicione a tarefa.

## Entrega para execução

Depois de salvar o plano, ofereça o próximo passo:

**"Plano completo e salvo em `docs/aios-jet/plans/<arquivo>.md`. Próximo passo: execução."**

- **SUB-SKILL OBRIGATÓRIA:** invoque a skill `jet-subagentes`
- Ela despacha um agente `jet-implementador` fresco por tarefa (ciclo TDD via `jet-tdd`), com revisão de `jet-revisor` entre tarefas
- Ao final de cada tarefa (ou do plano completo, conforme o fluxo de `jet-subagentes`), rode a skill `jet-verificacao` antes de declarar qualquer coisa como concluída — evidência antes de afirmação
