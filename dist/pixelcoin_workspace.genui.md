# Emblema Alquímico de Compressão Máxima, Puxers Quantitativos & LottieMCP

**Sinal Principal:** Mar de informações de investimento condensado em 52 Puxers Quantitativos e 1 Emblema Alquímico com Ressonância Lógico-Estética R_LE = 0.85.

- **Ação Prioritária:** Cada Puxer Monetário (🜃 Terra / 🜄 Aqua) = R$ 250; cada Puxer Experimental (🜂 Ignis) = 5% ΔIncerteza; 6 templates LottieMCP prontos para parametrização via JSON.
- **Anomalia / Gargalo:** Equilíbrio harmônico entre Valor Realizado (15 puxers 🜃) e Capital Comprometido (8 puxers 🜄) aproxima-se da razão áurea φ = 1.618.
- **Transparência Epistemológica:** Transparência Epistemológica: Das 18 dimensões avaliadas nos gráficos radiais do portfólio, 14 baseiam-se em evidências empíricas observadas nos repositórios/entrevistas e 4 são estimativas explícitas que exigem experimentos de validação.

:::genui
version: "0.1"
id: "ui-spec-71cd77a5e33b"
mode: "interactive"
intent: "curate_investment_sea_and_compile_alchemical_emblem"
surface: "workspace"
layout: "capital-workbench"
state_scope: "workspace"
windows:
  - id: "alchemical-emblem"
    title: "Emblema Alquímico & Puxers"
    component: "alchemical.emblem"
    source: "portfolio.alchemical_emblem"
    span: 6
    priority: 1
  - id: "portfolio"
    title: "Mosaico do Portfólio"
    component: "portfolio.mosaic"
    source: "portfolio.opportunities"
    span: 6
    priority: 2
  - id: "decision"
    title: "Matriz de Decisão & Experimentos"
    component: "decision.matrix"
    source: "portfolio.ranked_experiments"
    span: 7
    priority: 1
  - id: "radial-profile"
    title: "Perfil Radial (6 Dimensões)"
    component: "chart.radial"
    source: "selection.opportunity_profile"
    span: 5
    priority: 2
  - id: "asset-graph"
    title: "Grafo de Ativos & Direitos SPDX"
    component: "graph.knowledge"
    source: "portfolio.asset_graph"
    span: 6
    priority: 2
  - id: "capital-flow"
    title: "Fluxo de Capital em Movimento"
    component: "capital.flow"
    source: "capital.flows"
    span: 6
    priority: 3
  - id: "evidence"
    title: "Inspeção de Evidências & Rastreabilidade"
    component: "evidence.inspector"
    source: "selection.evidence_and_rights"
    span: 8
    priority: 1
  - id: "next-actions"
    title: "Fila de Tarefas Executáveis"
    component: "task.queue"
    source: "plan.next_actions"
    span: 4
    priority: 2
links:
  - from: "portfolio.selection"
    to: "decision.selection"
    event: "selection.changed"
  - from: "decision.selection"
    to: "radial-profile.target"
    event: "selection.changed"
  - from: "asset-graph.selection"
    to: "evidence.target"
    event: "selection.changed"
  - from: "alchemical-emblem.lottie_params"
    to: "portfolio.filter"
    event: "lottie.parameterized"
actions:
  - id: "opportunity.simulate"
    label: "Simular Alocação de Orçamento"
    kind: "invoke"
    permission: "capital:simulate"
    confirmation: "none"
  - id: "lottie.parameterize"
    label: "Parametrizar Infográfico Lottie via JSON"
    kind: "invoke"
    permission: "lottie:parameterize"
    confirmation: "none"
  - id: "rights.audit"
    label: "Aprovar Limpeza de Licenças SPDX"
    kind: "mutate"
    permission: "rights:audit"
    confirmation: "required"
  - id: "treasury.allocate"
    label: "Confirmar Alocação e Registrar Experimento"
    kind: "mutate"
    permission: "capital:allocate"
    confirmation: "required"
fallback:
  mode: "markdown"
  summary: "Mar de informações de investimento condensado em 52 Puxers Quantitativos e 1 Emblema Alquímico com Ressonância Lógico-Estética R_LE = 0.85."
provenance:
  show_sources: true
  show_as_of: true
  distinguish_observed_estimated_simulated: true
:::
