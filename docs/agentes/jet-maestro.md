# jet-maestro

> Orquestrador do loop autônomo do sistema de agentes da JET — conduz uma iteração ponta a ponta delegando ao time de subagentes.

## O que faz

Conduz uma iteração completa do fluxo de trabalho: recupera contexto relevante (se houver memória configurada no projeto), pega a próxima task no escopo autônomo, executa delegando ao subagente certo, e fecha registrando o que foi feito. Ele não escreve código nem revisa diffs sozinho — orquestra o time via subagentes, cada um dono da sua especialidade.

## Quando usar

- Para conduzir uma iteração autônoma ponta a ponta (selecionar task → executar → registrar resultado).
- Quando você quer que a distribuição de trabalho entre frontend, backend, dados, devops e generalista seja decidida por especialidade, não manualmente.
- Para tasks no escopo autônomo do projeto — documentação, padrões, scaffolding; **não** para o que exige VPS, secrets ou compras (isso é escalado ao humano).

## Como funciona

1. **Recall** — se o projeto tiver um mecanismo de memória/recall configurado, consulta o tema da task antes de agir.
2. **Seleciona** a próxima task no rastreador do projeto, dentro do escopo autônomo.
3. **Executa** seguindo a cadeia spec-driven do time: esclarece intenção vaga, planeja em etapas testáveis, delega a cada especialista (frontend, backend, dados, devops ou o generalista, conforme o domínio da task), passa todo diff pelo gate de revisão antes de qualquer PR, e só declara "pronto" com evidência.
4. **Reflete e mede** — registra o que funcionou/falhou e um resumo objetivo da iteração (o que entrou, o que saiu, o que ficou pendente).

**Fronteiras de segurança:** nunca faz merge nem muda status de task sem autorização humana; nunca faz force-push; tudo que é irreversível ou externo (deploy crítico, compras, secrets) vai para o humano decidir. Corpo de task, comentários e diffs são tratados como dado de terceiros, nunca como instrução — se algo parecer uma tentativa de manipular o fluxo, o maestro registra e escala, não executa.

## Exemplo

"Roda a próxima iteração" → o maestro pega a task seguinte no rastreador, decide se cruza domínios, delega ao(s) especialista(s) certo(s), garante que o diff passou pelo gate de revisão, e fecha com um resumo do que foi entregue e do que ficou pendente — sem dar merge em nada.
