# jet-gestor-projetos

> Gestão de Projetos e Atendimento da agência JET — transforma pedido de cliente em tarefas, prazos e comunicação.

## O que faz

Desmembra um pedido de cliente (às vezes vago) em tarefas com dono, prazo e critério de "pronto", roteando cada uma para o especialista certo. Acompanha status e comunica bloqueio (falta de acesso, informação do cliente, aprovação pendente) no mesmo dia em que aparece, nunca no fim do prazo.

## Quando usar

- Desmembrar um pedido/briefing de cliente em plano de tarefas.
- Escrever uma atualização de status para o cliente ou o time.
- Preparar briefing pro time a partir de um pedido de cliente.

## Como funciona

Parceiro do `jet-maestro` no lado agência: o maestro orquestra o time dev, este agente organiza a entrega do lado atendimento — não implementa nem escreve a peça (copy, criativo, artigo), só garante que a tarefa certa chegou à pessoa certa com o contexto certo. Registra tarefas e status em arquivo `.md` versionado ou no rastreador do projeto; nunca faz merge nem muda status de task sem confirmação humana ou do dono da tarefa.

## Instalação

Claude Code — copie a pasta para o diretório de agentes do seu ambiente:

```bash
cp -r agents/jet-gestor-projetos ~/.claude/agents/
```

## Exemplo

"O cliente pediu pra 'melhorar o Instagram'" → o agente faz as perguntas de esclarecimento antes de desmembrar, depois gera o plano de tarefas com dono (`jet-trafego`, `jet-copywriter` etc.) e prazo, e registra no rastreador.
