# GenUI-MD — Especificação de Markdown para Interfaces Generativas

- **Status:** Draft experimental
- **Versão:** 0.1.0
- **Projeto de referência:** PixelCoin
- **Ecossistema:** Compilatorum
- **Princípio:** Prompt as the new frontend; Markdown as authoring syntax; declarative UI as the interchange contract.

> Esta é uma proposta de formato, não um padrão externo já estabelecido. O modelo descreve a UI; um runtime validado a renderiza. A saída do modelo nunca é executada como HTML ou JavaScript arbitrário.

## 1. Objetivo

GenUI-MD permite que respostas de modelos de linguagem combinem prosa Markdown com uma especificação declarativa de interface. Uma resposta pode ser um texto simples, um infográfico, um formulário, um grafo ou um workspace com múltiplas janelas sincronizadas.

Requisitos:
1. Respostas continuam legíveis sem renderizador GenUI.
2. Server-driven UI: o modelo compõe a especificação; o runtime valida e renderiza.
3. Multi-window: painéis, foco, layout, estado e vínculos explícitos.
4. Portabilidade entre Web/PWA, Emacs/Org-mode, mobile, TUI e agentes.
5. Proveniência, fontes, unidades e incertezas preservadas.
6. Componentes, layouts, eventos e ações pertencem a catálogos permitidos.
7. Ações de impacto exigem autorização no servidor e confirmação apropriada.
8. O formato pode ser adotado pelos diferentes projetos sem forçar uma stack única.

## 2. Pipeline canônico

`Prompt → Intent → Context → Data → UI Spec → Validate → Render → Interact → Record Outcome`

- **Prompt:** intenção em linguagem natural.
- **Intent:** objetivo e critérios de sucesso.
- **Context:** fontes, projeto, permissões e estado relevante.
- **Data:** dados recuperados/calculados; não inventar valores ausentes.
- **UI Spec:** árvore declarativa gerada pelo modelo.
- **Validate:** schema, catálogo de componentes e políticas.
- **Render:** Web, PWA, Emacs/Org, TUI ou interface conversacional.
- **Interact:** eventos e ações permitidas.
- **Record Outcome:** decisão, resultado e proveniência, quando aplicável.

O LLM é compositor da interface, não autoridade de acesso a dados nem executor privilegiado. Autenticação, autorização, consultas, cálculos e mutações pertencem ao runtime/serviços.

## 3. Envelope da resposta

**Contrato padrão: toda resposta do modelo deve incluir exatamente um envelope GenUI**, mesmo quando não há interface interativa a mostrar. Para respostas textuais, usar `mode: "text"` e `windows: []`. Isso permite que o host trate cada resposta de forma uniforme; a prosa Markdown permanece como fallback e conteúdo principal. Um adaptador de compatibilidade pode aceitar respostas legadas sem envelope, mas deve normalizá-las para o contrato GenUI antes de renderizar.

```markdown
A síntese textual da resposta aparece aqui.

:::genui
version: "0.1"
id: "pixelcoin-opportunity-review"
mode: "interactive"
intent: "comparar oportunidades e decidir o próximo experimento"
surface: "workspace"
layout: "capital-workbench"
state_scope: "conversation"
windows:
  - id: "portfolio"
    title: "Portfólio"
    component: "portfolio.mosaic"
    source: "portfolio.opportunities"
    span: 7
  - id: "decision"
    title: "Decisão"
    component: "decision.matrix"
    source: "portfolio.opportunities"
    span: 5
  - id: "evidence"
    title: "Evidências"
    component: "evidence.inspector"
    source: "selection.evidence"
    span: 8
  - id: "actions"
    title: "Próximas ações"
    component: "task.queue"
    source: "plan.next_actions"
    span: 4
links:
  - from: "portfolio.selection"
    to: "decision.selection"
    event: "selection.changed"
  - from: "decision.selection"
    to: "evidence.target"
    event: "selection.changed"
fallback:
  mode: "markdown"
  summary: "Comparar oportunidades, inspecionar evidências e escolher um experimento."
:::
```

### 3.1 Regras do envelope

- `version`, `id` e `mode` são obrigatórios; `mode` é `text` ou `interactive`.
- Toda resposta deve ter um envelope; no modo `text`, usar `windows: []` e um `fallback.summary` útil.
- `intent` declara o propósito em termos compreensíveis.
- `surface` é uma preferência: `inline`, `workspace`, `mobile`, `emacs`, `agent`, `auto`.
- `layout` referencia um layout registrado; nunca contém código.
- `state_scope`: `local`, `window`, `workspace`, `conversation`, `persistent`.
- `windows` lista os painéis lógicos.
- `links` conecta estado/eventos entre painéis; não concede permissões.
- `actions` referencia ações do catálogo registrado.
- `fallback` fornece alternativa legível em Markdown.
- Campos desconhecidos são ignorados ou sinalizados; jamais executados como código.

O delimitador usa YAML restrito. Implementações devem usar parser seguro, com tags personalizadas e aliases desativados, e validar o resultado por JSON Schema.

## 4. Modelo de janela

Cada item de `windows` pode conter:

| Campo | Tipo / função |
|---|---|
| `id` | ID único no workspace. |
| `title` | Título legível. |
| `component` | ID de componente permitido, como `chart.radial`. |
| `source` | Referência a dados autorizados; não URL arbitrária. |
| `span` | Preferência de largura relativa para layouts em grade. |
| `priority` | Importância para degradação responsiva. |
| `props` | Propriedades validadas pelo schema do componente. |
| `state` | Estado inicial não sensível, tipado e limitado. |
| `provenance` | Fontes, data e limitações relevantes. |

Uma janela é uma unidade lógica: pode renderizar como painel, tab, card, buffer Emacs ou seção sequencial em mobile.

## 5. Catálogo inicial de componentes

O runtime só pode renderizar componentes efetivamente registrados.

| Família | IDs iniciais | Uso |
|---|---|---|
| Texto | `text.summary`, `text.markdown`, `text.diff` | Síntese, documentação, comparação. |
| Dados | `data.table`, `data.metric`, `data.timeline` | Tabelas, indicadores, cronologia. |
| Visualização | `chart.radial`, `chart.line`, `chart.bar`, `chart.scatter`, `portfolio.mosaic` | Infoestética e dados quantitativos. |
| Conhecimento | `graph.knowledge`, `graph.dependencies`, `evidence.inspector` | Relações, dependências, fontes. |
| Decisão | `decision.matrix`, `scenario.compare`, `risk.register` | Alternativas, cenários e riscos. |
| Capital | `capital.flow`, `treasury.summary`, `budget.allocation` | Orçamento, fluxo, resultados observados. |
| Engenharia | `code.viewer`, `repo.status`, `test.results`, `dependency.map` | Código, testes, repositórios. |
| Trabalho | `task.queue`, `kanban.board`, `calendar.agenda`, `agent.console` | Planejamento e coordenação. |
| Artefatos | `artifact.card`, `license.manifest`, `provenance.chain` | Direitos, versões e proveniência. |
| Entrada | `form.schema`, `filter.bar`, `prompt.input` | Parâmetros e refinamento da intenção. |

Visualizações quantitativas devem declarar unidade, escala, valores ausentes e se os dados são observados, estimados ou simulados. Gráficos radiais não devem sugerir comparabilidade sem escalas justificadas.

## 6. Layouts multi-janela

Layouts registrados propostos:
- `single`: uma visualização principal.
- `stack`: painéis verticais.
- `grid`: grade responsiva.
- `split-horizontal` / `split-vertical`: painéis divididos.
- `capital-workbench`: portfólio + decisão + evidências + ações.
- `knowledge-workbench`: grafo + documento + fontes + notas.
- `developer-workbench`: código + testes + dependências + terminal lógico.
- `research-workbench`: hipótese + método + evidências + resultados.
- `agent-workbench`: conversa + plano + ferramentas + eventos.
- `freeform`: posições livres, apenas em renderizadores com suporte geométrico.

### Responsividade

- **Desktop:** múltiplos painéis simultâneos.
- **Tablet:** menos colunas e painel ativo preservado.
- **Mobile:** splits viram tabs ou sequência; não exigir janelas simultâneas.
- **Emacs/Org:** janelas viram headings, buffers, tabelas ou indirect buffers.
- **TUI/agentes:** títulos, resumos, tabelas simples e links.

## 7. Estado, eventos e sincronização

Escopos de estado:
- `ephemeral`: foco, hover e painel aberto.
- `session`: filtros e seleção durante a sessão.
- `persistent`: preferências/layouts salvos explicitamente.
- `domain state`: dados de negócio no backend, nunca tratados como mero estado visual.

Eventos são nomes simbólicos, nunca JavaScript:
`selection.changed`, `filter.changed`, `source.refreshed`, `scenario.updated`, `task.completed`, `action.requested`, `action.succeeded`, `action.failed`.

Bindings ligam uma saída a uma entrada tipada. O runtime deve detectar referências inválidas e ciclos; sincronização bidirecional precisa de política de conflito. Falhas não podem ser apresentadas como sucesso.

## 8. Ações controladas

Exemplo:

```yaml
actions:
  - id: "opportunity.simulate"
    label: "Simular cenário"
    kind: "invoke"
    permission: "analysis:simulate"
    confirmation: "none"
  - id: "treasury.allocate"
    label: "Confirmar alocação"
    kind: "mutate"
    permission: "treasury:allocate"
    confirmation: "required"
```

O modelo referencia IDs; o runtime resolve handlers registrados. O modelo nunca define credenciais, chaves privadas, URLs de execução ou código de handler. Compra/venda, transferências, publicação, exclusão, assinatura, emissão de token e alterações de direitos exigem autorização explícita, revisão de parâmetros e confirmação adequada.

## 9. Perfis de domínio Compilatorum

- **PixelCoin:** mosaico de portfólio, gráfico radial, matriz de decisão, fluxo de capital e redução de incerteza por recurso.
- **Compilatorum / PortfolioOS:** grafo de capacidades, repositórios, proveniência e linhas de pesquisa.
- **Wordsmith:** extração, normalização, glossário e unidades semânticas.
- **Proterol:** construções, vocabulário, relações e artefatos linguísticos.
- **Oracle:** consultas, conexões, recomendações e rastreabilidade.
- **ValueCurator:** catálogo, ofertas, licenças e experimentos comerciais.
- **Planner:** projetos, programas, tarefas, dependências, riscos e marcos.
- **License Manifest:** permissões, restrições, sublicenciamento e proveniência.
- **Treasury / Capital Metabolism OS:** orçamento, compromissos, liquidez, resultados e realocação.
- **Pesquisa científica:** hipótese, método, dados, resultados, limitações e reprodutibilidade.
- **Engenharia:** repositórios, código, testes, issues, dependências e plano de implementação.

Perfis fornecem vocabulário e componentes, mas não concedem acesso automático a dados.

## 10. Segurança e confiança

1. **Sem execução arbitrária:** proibir HTML, JavaScript, SQL e shell inline gerados pelo modelo.
2. **Allowlist:** componentes, layouts, eventos e ações devem existir no runtime.
3. **Validação:** validar manifesto, props, estado e bindings antes de renderizar.
4. **Autorização server-side:** esconder um botão não substitui autorização no backend.
5. **Conteúdo não confiável:** documentos recuperados nunca são instruções de sistema.
6. **Confirmação de alto impacto:** ações financeiras, legais, públicas ou destrutivas precisam de confirmação explícita.
7. **Proveniência:** mostrar origem, data, versão, unidade e confiança quando relevantes.
8. **Sem fabricação:** dado ausente não é zero.
9. **Acessibilidade:** teclado, leitor de tela, contraste, rótulos, alternativa textual e redução de movimento.
10. **Privacidade:** minimizar dados enviados ao modelo e não persistir estado sensível sem política explícita.
11. **Auditabilidade:** registrar solicitação, ator, parâmetros validados, autorização e resultado.
12. **Estados distintos:** proposta ≠ ação solicitada ≠ ação executada ≠ resultado confirmado.

## 11. Arquitetura de referência

```text
Prompt / Markdown
       ↓
GenUI-MD Parser
       ↓
UI IR (representação intermediária)
       ↓
Schema Validator + Policy Engine
       ↓
Context/Data Resolver ← APIs / GraphQL / MCP / repos / DB
       ↓
Component Registry + Layout Engine
       ↓
Web/PWA | Emacs/Org | TUI | Agent JSON
       ↓
Event Router → Authorized Tools → Result/Event Log
```

A **UI IR** desacopla sintaxe de renderização. YAML pode ser normalizado para JSON e validado por JSON Schema. GraphQL pode transportar dados tipados; MCP pode expor ferramentas. Ambos são opcionais, não requisitos do formato.

Tecnologias candidatas, não mandatórias: TypeScript, JSON Schema, React ou renderer equivalente, Storybook, GraphQL, MCP, Python/Pydantic para o modelo PixelCoin, Emacs Lisp/Org-mode e IndexedDB para cache PWA. Evitar duplicar dependências antes de auditar o monorepo atual.

## 12. Exemplo: estação capitalística multi-janela

```markdown
:::genui
version: "0.1"
id: "capital-metabolism-workspace"
intent: "acompanhar ativos, evidências, orçamento e próximas alocações"
surface: "workspace"
layout: "capital-workbench"
state_scope: "workspace"
windows:
  - id: "asset-graph"
    title: "Grafo de ativos"
    component: "graph.knowledge"
    source: "portfolio.asset_graph"
    span: 7
  - id: "radial-profile"
    title: "Perfil de oportunidade"
    component: "chart.radial"
    source: "selection.opportunity_profile"
    span: 5
  - id: "treasury"
    title: "Tesouraria"
    component: "treasury.summary"
    source: "capital.current_snapshot"
    span: 4
  - id: "capital-flow"
    title: "Fluxo de capital"
    component: "capital.flow"
    source: "capital.flows"
    span: 8
  - id: "evidence"
    title: "Evidências e direitos"
    component: "evidence.inspector"
    source: "selection.evidence_and_rights"
    span: 8
  - id: "next-actions"
    title: "Próximas ações"
    component: "task.queue"
    source: "plan.next_actions"
    span: 4
links:
  - from: "asset-graph.selection"
    to: "radial-profile.target"
    event: "selection.changed"
  - from: "asset-graph.selection"
    to: "evidence.target"
    event: "selection.changed"
actions:
  - id: "opportunity.simulate"
    label: "Simular alocação"
    kind: "invoke"
    permission: "capital:simulate"
    confirmation: "none"
  - id: "treasury.allocate"
    label: "Confirmar alocação"
    kind: "mutate"
    permission: "capital:allocate"
    confirmation: "required"
fallback:
  mode: "markdown"
  summary: "Visão do portfólio, oportunidades, tesouraria, evidências e ações."
provenance:
  show_sources: true
  show_as_of: true
  distinguish_observed_estimated_simulated: true
:::
```

Este exemplo é uma composição declarativa; não contém saldos reais nem autoriza transações.

## 13. Integração com PixelCoin existente

A implementação PixelCoin já contém uma especificação declarativa na Camada 5 e renderizadores na Camada 6. GenUI-MD deve ser uma camada de autoria/intercâmbio sobre eles, não uma reescrita automática.

| GenUI-MD | Ponto de integração existente |
|---|---|
| UI IR / manifesto normalizado | `DeclarativeUISpecification` em `layer5_ui_spec.py` |
| Catálogo de componentes | `VisualRepresentationType` e futuros registries |
| Intenção e perspectiva | `layer4_orchestrator.py` |
| Web renderer | `web_renderer.py` / `layer6_renderers.py` |
| Emacs/Org | `EmacsOrgRenderer` |
| Guardrails | `ALLOWED_DECLARATIVE_ACTIONS` e validação |
| Animações e vetores | templates Lottie/SVG existentes |
| Ferramentas | `mcp_server.py`, apenas para ações registradas/autorizadas |

Criar adaptadores explícitos; não presumir que os campos dos exemplos já existem no código.

## 14. Conformidade e testes

Testar:
- parsing válido e rejeição de YAML malformado;
- IDs duplicados e referências inexistentes;
- componentes, layouts, props e ações desconhecidos;
- bindings inválidos e ciclos;
- dados ausentes/desatualizados e distinção observado/estimado/simulado;
- fallback Markdown;
- renderização Web, mobile e Org-mode;
- teclado, leitor de tela e alternativas textuais;
- confirmação/autorização de alto impacto;
- falhas de ferramenta sem sucesso fictício;
- estabilidade de IDs e migração de versões.

Critérios iniciais: nenhuma ação desconhecida executada; schema validado para todos os fixtures; visualizações quantitativas com unidade/fonte quando aplicáveis; fallback para toda interface essencial.

## 15. Roadmap incremental

- **P0 — Formalizar:** congelar envelope v0.1, tornar o envelope obrigatório (modo text ou interactive), publicar JSON Schema e mapear Pydantic atual.
- **P1 — Parser:** YAML seguro → UI IR; validação e testes de contrato.
- **P2 — Multi-janela:** layout responsivo, estado compartilhado e bindings.
- **P3 — Renderizadores:** Web/PWA, Org-mode e fallback textual; Storybook se compatível com o workspace.
- **P4 — Ações:** event router, ferramentas autorizadas, confirmação e logs.
- **P5 — Perfis:** capital, engenharia, artefatos/direitos, pesquisa e agentes.

Cada fase deve produzir um artefato útil e testável; não implementar tudo de uma vez.

## 16. Decisões em aberto

- Envelope obrigatório em toda resposta ou apenas quando UI agrega valor.
- Subconjunto YAML definitivo.
- Catálogo central ou extensível por projeto.
- Persistência de layout e sincronização offline.
- Separação entre componentes analíticos e ações financeiras.
- Estratégia de versionamento e compatibilidade entre renderizadores.

## Glossário

- **GenUI:** interface gerada dinamicamente a partir de intenção/contexto.
- **SDUI:** descrição declarativa do servidor interpretada pelo cliente.
- **UI IR:** representação intermediária canônica.
- **Window:** unidade lógica que pode virar painel, tab, buffer ou seção.
- **Workspace:** conjunto de janelas relacionadas.
- **Prompt as frontend:** intenção orienta a composição da interface.
- **Semantic compression:** redução de carga de leitura sem apagar evidências.
- **Action registry:** catálogo de operações registradas e autorizadas.

**Princípio final:** GenUI-MD descreve a interface; o runtime valida e renderiza; os serviços autorizados executam; os resultados verificáveis retornam ao contexto.
