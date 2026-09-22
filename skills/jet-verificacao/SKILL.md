---
name: jet-verificacao
description: Use sempre antes de afirmar que um trabalho está completo, corrigido ou passando — antes de fazer commit, abrir PR, marcar uma task como concluída no rastreador ou confiar no relatório de um subagente. Gatilhos — "terminei", "deve funcionar agora", "os testes passam", "corrigi o bug", "pronto para merge", ou qualquer variação de satisfação ("ótimo!", "perfeito!") antes de rodar o comando que prova a alegação.
---

# JET — Verificação Antes de Declarar Concluído

## Visão geral

Afirmar que um trabalho está completo sem verificação é desonestidade, não
eficiência.

**Princípio central:** evidência antes da alegação, sempre.

**Violar a letra desta regra é violar o espírito desta regra.**

## A lei inegociável

```
NENHUMA ALEGAÇÃO DE CONCLUSÃO SEM EVIDÊNCIA DE VERIFICAÇÃO FRESCA
```

Se você não rodou o comando de verificação nesta mensagem, não pode alegar
que ele passa.

## A função-gate

```
ANTES de alegar qualquer status ou expressar satisfação:

1. IDENTIFICAR: qual comando prova essa alegação?
2. RODAR: executar o comando COMPLETO (fresco, sem atalho)
3. LER: o output completo, checar o código de saída, contar falhas
4. VERIFICAR: o output confirma a alegação?
   - Se NÃO: declare o status real, com a evidência
   - Se SIM: declare a alegação COM a evidência
5. SÓ ENTÃO: faça a alegação

Pular qualquer passo = mentir, não verificar
```

## Falhas comuns

| Alegação | Exige | Não é suficiente |
|---|---|---|
| Testes passam | Output do comando de teste: 0 falhas | Rodada anterior, "deveria passar" |
| Linter limpo | Output do linter: 0 erros | Checagem parcial, extrapolação |
| Build passa | Comando de build: exit 0 | Linter passando, logs parecem bons |
| Bug corrigido | Teste do sintoma original: passa | Código mudou, presumiu-se corrigido |
| Teste de regressão funciona | Ciclo red-green verificado | Teste passa uma vez |
| Subagente concluiu | Diff do VCS mostra as mudanças | Subagente reportou "sucesso" |
| Requisitos atendidos | Checklist linha a linha | Testes passando |

## Sinais de alerta — PARE

- Usar "deveria", "provavelmente", "parece que".
- Expressar satisfação antes de verificar ("Ótimo!", "Perfeito!", "Pronto!"
  etc.).
- Estar prestes a fazer commit/push/PR sem verificação.
- Confiar no relatório de sucesso de um subagente sem checar independente.
- Confiar em verificação parcial.
- Pensar "só dessa vez".
- Estar cansado e só querer que o trabalho acabe.
- **QUALQUER formulação que implique sucesso sem ter rodado a verificação.**

## Prevenção de racionalização

| Desculpa | Realidade |
|---|---|
| "Deve funcionar agora" | RODE a verificação |
| "Estou confiante" | Confiança ≠ evidência |
| "Só dessa vez" | Sem exceções |
| "O linter passou" | Linter ≠ compilador |
| "O subagente disse que deu certo" | Verifique de forma independente |
| "Estou cansado" | Cansaço não é desculpa |
| "Uma checagem parcial já basta" | Parcial não prova nada |
| "Com outras palavras a regra não se aplica" | Espírito acima da letra |

## Padrões-chave

**Testes:**
```
✅ [Roda o comando de teste] [Vê: 34/34 passando] "Todos os testes passam"
❌ "Deve passar agora" / "Parece correto"
```

**Testes de regressão (TDD Red-Green):**
```
✅ Escreve → Roda (passa) → Reverte a correção → Roda (TEM que falhar) →
   Restaura → Roda (passa)
❌ "Escrevi um teste de regressão" (sem verificação red-green)
```

**Build:**
```
✅ [Roda o build] [Vê: exit 0] "O build passa"
❌ "O linter passou" (linter não checa compilação)
```

**Requisitos:**
```
✅ Relê o plano/spec → Cria checklist → Verifica item a item →
   Reporta lacunas ou conclusão
❌ "Os testes passam, fase concluída"
```

**Delegação a subagente:**
```
✅ Subagente reporta sucesso → Confere o diff do VCS → Verifica as
   mudanças → Reporta o estado real
❌ Confiar no relatório do subagente sem checar
```

## Por que isso importa

Quando uma alegação de "pronto" se revela falsa depois — em revisão, em
produção, ou na mão do cliente — o custo não é só o retrabalho: é a
confiança quebrada com quem confiou na alegação. Funções não definidas
sobem para produção. Requisitos faltando saem como se estivessem
completos. Tempo se perde no ciclo alegação falsa → correção → redirecionamento.
Honestidade sobre o estado real do trabalho é inegociável — é isso que
sustenta a confiança de continuar delegando trabalho sem reconferir tudo do
zero.

## Quando aplicar

**SEMPRE antes de:**
- Qualquer variação de alegação de sucesso/conclusão.
- Qualquer expressão de satisfação.
- Qualquer afirmação positiva sobre o estado do trabalho.
- Fazer commit, abrir PR, marcar task como concluída.
- Passar para a próxima task.
- Delegar a um subagente e aceitar o relatório dele como fato.

**A regra se aplica a:**
- Frases exatas.
- Paráfrases e sinônimos.
- Implicações de sucesso.
- QUALQUER comunicação que sugira conclusão/correção.

## Como isso se conecta ao fluxo de subagentes (`jet-subagentes`)

Ao usar `jet-subagentes`, cada gate desse fluxo é um ponto de aplicação
desta skill:

- O relatório "CONCLUIDO" de um `jet-implementador` não é evidência — é uma
  alegação. A evidência é o diff no git e o output de teste que o
  relatório cita; confira que ambos existem antes de despachar o
  `jet-revisor`.
- Os dois vereditos do `jet-revisor` (spec + qualidade) só valem se ele de
  fato leu o diff — não aceite um relatório de revisão que não referencia
  linhas ou arquivos concretos.
- Marcar uma task como concluída no ledger de progresso é uma alegação de
  conclusão: só escreva a linha do ledger depois que a re-revisão vier
  limpa, nunca antes, "para adiantar".

## Conclusão

**Sem atalhos para verificação.**

Rode o comando. Leia o output. SÓ ENTÃO alegue o resultado.

Isso não é negociável.
