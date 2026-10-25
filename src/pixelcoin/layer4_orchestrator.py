"""
Camada 4 — Orquestração por IA (Prompt-as-Frontend Orchestrator)

Implementa o fluxo:
Prompt → Contexto → Dados estruturados → Especificação da UI → Renderizador → Interação → Resultado

Responsabilidades:
- Interpretar a intenção do prompt, restrições orçamentárias e critérios de decisão
- Adaptar a síntese conforme a visão (Executiva, Desenvolvedor, Científica)
- Selecionar a representação infoestética primária dentre as 5 formas (Radial, Grafo, Mosaico, Matriz de Decisão, Fluxo)
- Construir os 3 níveis da Regra da Compressão Semântica (Visão Instantânea, Inspeção, Rastreabilidade)
- Emitir uma `DeclarativeUISpecification` validada pelos Guardrails da Camada 5
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

from pixelcoin.alchemical_infoaesthetics import SeaOfInformationCurator
from pixelcoin.layer1_sources import CompilatorumCorpusIngestor
from pixelcoin.layer2_graph import LicenseStatus, SemanticKnowledgeGraph
from pixelcoin.layer3_economics import EconomicIntelligenceEngine
from pixelcoin.layer5_ui_spec import (
    DeclarativeActionSpec,
    DeclarativeUISpecification,
    InspectionLayer,
    InstantViewLayer,
    MetricIndicator,
    PersonaPerspective,
    SemanticCompressionTriad,
    TraceabilityLayer,
    VisualRepresentationType,
)
from pixelcoin.lottie_templates import LottieTemplateRegistry


CANONICAL_PROMPTS: List[Dict[str, str]] = [
    {
        "id": "prompt_alchemical_emblem_lottie",
        "prompt": "Condense o mar de informações de investimento em um Emblema Alquímico com puxers quantitativos, vetores e Lottie.",
        "expected_ui": "Emblema Alquímico de compressão máxima, grade de Puxers quantitativos, Ressonância Lógico-Estética e templates LottieMCP.",
        "representation": VisualRepresentationType.ALCHEMICAL_EMBLEM.value,
    },
    {
        "id": "prompt_budget_uncertainty",
        "prompt": "Tenho pouco orçamento para desenvolver o Compilatorum. Compare minhas opções e encontre a ação que mais reduz incerteza por unidade de recurso.",
        "expected_ui": "Matriz de decisão, portfólio de experimentos (Testar, Validar, Preparar) e cenários de alocação.",
        "representation": VisualRepresentationType.DECISION_MATRIX.value,
    },
    {
        "id": "prompt_no_blockchain",
        "prompt": "Mostre o que pode ser monetizado sem blockchain.",
        "expected_ui": "Catálogo de artefatos, serviços, APIs e licenças + Perfil Radial de Oportunidades.",
        "representation": VisualRepresentationType.RADIAL_PROFILE.value,
    },
    {
        "id": "prompt_dependencies",
        "prompt": "Encontre dependências entre meus repositórios.",
        "expected_ui": "Grafo de componentes, relações, sinergias e gargalos.",
        "representation": VisualRepresentationType.KNOWLEDGE_GRAPH.value,
    },
    {
        "id": "prompt_compare_experiments",
        "prompt": "Compare três experimentos com orçamento limitado.",
        "expected_ui": "Matriz de decisão e cenários de alocação.",
        "representation": VisualRepresentationType.DECISION_MATRIX.value,
    },
    {
        "id": "prompt_unclear_rights",
        "prompt": "Quais artefatos têm direitos incertos?",
        "expected_ui": "Mapa de proveniência e pendências de licenciamento.",
        "representation": VisualRepresentationType.KNOWLEDGE_GRAPH.value,
    },
    {
        "id": "prompt_portfolio_mosaic",
        "prompt": "Resuma meu portfólio em uma tela.",
        "expected_ui": "Mosaico de ativos, oportunidades, custos e valor realizado.",
        "representation": VisualRepresentationType.PORTFOLIO_MOSAIC.value,
    },
    {
        "id": "prompt_traceability",
        "prompt": "Explique a origem desta recomendação.",
        "expected_ui": "Trilha de evidências, fontes, hashes SHA-256 e premissas.",
        "representation": VisualRepresentationType.RADIAL_PROFILE.value,
    },
    {
        "id": "prompt_executable_plan",
        "prompt": "Transforme esta oportunidade em um plano executável.",
        "expected_ui": "Cronograma, tarefas, recursos, fluxo de capital e critérios de validação.",
        "representation": VisualRepresentationType.CAPITAL_FLOW.value,
    },
]


class PixelCoinOrchestrator:
    """Orquestrador Generativo de UI (Camada 4)."""

    def __init__(
        self,
        ingestor: Optional[CompilatorumCorpusIngestor] = None,
        graph: Optional[SemanticKnowledgeGraph] = None,
        economics: Optional[EconomicIntelligenceEngine] = None,
        curator: Optional[SeaOfInformationCurator] = None,
    ) -> None:
        self.ingestor = ingestor or CompilatorumCorpusIngestor()
        self.graph = graph or SemanticKnowledgeGraph(self.ingestor)
        self.economics = economics or EconomicIntelligenceEngine(self.graph)
        self.curator = curator or SeaOfInformationCurator()

    def classify_prompt(
        self,
        prompt: str,
        override_representation: Optional[VisualRepresentationType] = None,
    ) -> Dict[str, Any]:
        """Classifica a intenção do prompt e seleciona a representação visual mais adequada."""
        text = prompt.lower()

        if any(k in text for k in ["emblema", "alquim", "alquím", "puxer", "lottie", "ressonância", "ressonancia", "mar de informa", "vetor"]):
            intent = "curate_investment_sea_and_compile_alchemical_emblem"
            rep = VisualRepresentationType.ALCHEMICAL_EMBLEM
            title = "Emblema Alquímico de Compressão Máxima, Puxers Quantitativos & LottieMCP"
            subtitle = "Curadoria do mar de informações de investimento por Ressonância Lógico-Estética (R_LE), Vetores SVG e Templates Lottie"
        elif any(k in text for k in ["direito", "licen", "incerto", "proveni", "spdx", "copyright"]):
            intent = "audit_unclear_rights_and_provenance"
            rep = VisualRepresentationType.KNOWLEDGE_GRAPH
            title = "Mapa de Proveniência, Direitos e Pendências de Licenciamento"
            subtitle = "Inspeção cruzada entre License Manifest, repositórios do Compilatorum e restrições comerciais"
        elif any(k in text for k in ["depend", "reposit", "grafo", "sinergia", "gargalo", "componente"]):
            intent = "analyze_repository_dependencies_and_synergies"
            rep = VisualRepresentationType.KNOWLEDGE_GRAPH
            title = "Grafo de Relações, Componentes Reutilizáveis e Gargalos do Compilatorum"
            subtitle = "Topologia semântica conectando Wordsmith, Proterol, Oracle, License Manifest, ValueCurator e Planner"
        elif any(k in text for k in ["orçamento", "orcamento", "experimento", "incerteza", "compare", "opções", "opcoes"]):
            intent = "prioritize_experiments_under_budget_constraint"
            rep = VisualRepresentationType.DECISION_MATRIX
            title = "Matriz de Decisão & Portfólio de Experimentos sob Orçamento Limitado"
            subtitle = "Priorização por Redução de Incerteza por Unidade de Recurso (ΔIncerteza / R$ 1.000)"
        elif any(k in text for k in ["sem blockchain", "monetiz", "catálogo", "catalogo", "micro-saas", "api"]):
            intent = "discover_non_blockchain_monetization_opportunities"
            rep = VisualRepresentationType.RADIAL_PROFILE
            title = "Catálogo de Monetização Sem Blockchain & Perfis Radiais de Oportunidades"
            subtitle = "Avaliação multidimensional de artefatos prontos para SaaS, API Semântica, Licenciamento e Grants"
        elif any(k in text for k in ["plano execut", "cronograma", "tarefa", "fluxo", "alocação", "alocacao", "capital"]):
            intent = "generate_executable_plan_and_capital_flow"
            rep = VisualRepresentationType.CAPITAL_FLOW
            title = "Fluxo de Capital em Movimento & Plano Executável de Validação"
            subtitle = "Trajetória Alocação → Execução → Marcos → Resultados → Reinvestimento com Critérios Go/No-Go"
        elif any(k in text for k in ["origem", "explique", "evidência", "evidencia", "fonte", "premissa", "rastreab"]):
            intent = "explain_recommendation_provenance_and_assumptions"
            rep = VisualRepresentationType.RADIAL_PROFILE
            title = "Trilha de Evidências, Fontes Criptográficas e Premissas da Recomendação"
            subtitle = "Decomposição transparente entre fatos empíricos observados e estimativas sujeitas a validação"
        else:
            intent = "summarize_portfolio_mosaic_overview"
            rep = VisualRepresentationType.PORTFOLIO_MOSAIC
            title = "Mosaico Sintético do Portfólio Compilatorum (Visão em Uma Tela)"
            subtitle = "Cada bloco codifica ativos, custos comprometidos, valor realizado e potencial estimado sem confusão semântica"

        if override_representation is not None:
            rep = override_representation

        return {
            "intent": intent,
            "primary_representation": rep,
            "title": title,
            "subtitle": subtitle,
        }

    def generate_ui_spec(
        self,
        prompt: str,
        perspective: PersonaPerspective = PersonaPerspective.EXECUTIVE,
        override_representation: Optional[VisualRepresentationType] = None,
        budget_limit_brl: float = 1500.0,
    ) -> DeclarativeUISpecification:
        """
        Gera a especificação declarativa completa da interface (`DeclarativeUISpecification`)
        a partir de qualquer prompt do usuário.
        """
        classified = self.classify_prompt(prompt, override_representation=override_representation)
        intent = classified["intent"]
        primary_rep: VisualRepresentationType = classified["primary_representation"]

        # Recupera dados estruturados das Camadas 1, 2 e 3
        all_sources = self.ingestor.list_sources()
        all_artifacts = self.graph.list_artifacts()
        unclear_artifacts = self.graph.list_artifacts(only_unclear_rights=True)
        no_chain_artifacts = self.graph.list_artifacts(only_monetizable_no_blockchain=True)
        graph_topology = self.graph.find_bottlenecks_and_dependencies()
        ranked_experiments = self.economics.rank_experiments_by_efficiency(max_budget_brl=budget_limit_brl)
        simulation = self.economics.simulate_allocation(budget_brl=budget_limit_brl)
        executable_plan = self.economics.build_executable_plan("opp:curadoria_corpus_b2b")

        # Adapta o sinal principal conforme a intenção e a perspectiva (Executiva, Desenvolvedor, Científica)
        headline, priority_action, anomaly = self._build_instant_view_by_intent(
            intent=intent,
            perspective=perspective,
            ranked_experiments=ranked_experiments,
            unclear_artifacts=unclear_artifacts,
            simulation=simulation,
        )

        # Contabiliza dimensões observadas vs. estimadas em todas as oportunidades
        total_dims = sum(len(o.radial_dimensions) for o in self.economics.opportunities.values())
        estimated_dims = sum(o.estimated_dimensions_count for o in self.economics.opportunities.values())
        observed_dims = total_dims - estimated_dims

        semantic_compression = SemanticCompressionTriad(
            instant_view=InstantViewLayer(
                headline_signal=headline,
                top_priority_action=priority_action,
                detected_anomaly_or_bottleneck=anomaly,
            ),
            inspection=InspectionLayer(
                causal_factors=[
                    f"Experimento C (Licenças, R$ 350) entrega 108.57 pts de redução de incerteza por R$ 1.000 investidos, destravando gargalos jurídicos.",
                    f"Experimento A (Validar demanda por curadoria, R$ 450) entrega 93.33 pts de redução de incerteza por R$ 1.000, com base em 12 entrevistas prévias (83.3% preferem solução sem blockchain).",
                    f"Construir a API completa agora (Experimento B, R$ 1.200) tem menor eficiência marginal (29.17 pts/R$ 1k) até que a demanda e as licenças do Oracle estejam validadas.",
                    f"Perspectiva ativa: '{perspective.value.upper()}' — ajustando nível de detalhe técnico, financeiro e epistemológico.",
                ],
                observed_vs_estimated_breakdown=(
                    f"Transparência Epistemológica: Das {total_dims} dimensões avaliadas nos gráficos radiais do portfólio, "
                    f"{observed_dims} baseiam-se em evidências empíricas observadas nos repositórios/entrevistas e "
                    f"{estimated_dims} são estimativas explícitas que exigem experimentos de validação."
                ),
                decision_criteria_used=[
                    "Eficiência Informacional: Redução de Incerteza (%) por R$ 1.000 alocados",
                    "Restrição Fiduciária Soberana: Manutenção de Phi_buffer >= 1.20 no Sovereign Budget",
                    "Prontidão de Direitos: Bloqueio de comercialização para artefatos com license_status == unclear_pending_audit",
                    "Separação Estrita: Valor Realizado vs. Custo Comprometido vs. Potencial Estimado",
                ],
                alternative_scenarios=[
                    "Cenário Enxuto (R$ 800): Executar C (R$ 350) + A (R$ 450) → Reduz 68% da incerteza comercial e jurídica em 12 dias.",
                    "Cenário Técnico (R$ 1.550): Executar C (R$ 350) + B (R$ 1.200) → Valida API semântica Proterol, mas posterga entrevistas de precificação.",
                    "Cenário Completo (R$ 2.500): Executar C + A + D + B em 4 semanas condicionado a portões Go/No-Go do ValueCurator.",
                ],
            ),
            traceability=TraceabilityLayer(
                source_records=[
                    {
                        "source_id": s.source_id,
                        "title": s.title,
                        "module": s.compilatorum_module,
                        "uri": s.uri,
                        "sha256": s.sha256[:16] + "...",
                        "version": s.version,
                    }
                    for s in all_sources
                ],
                assumptions=[
                    "O custo de hora-técnica própria foi parametrizado como custo de oportunidade fiduciário no Sovereign Budget.",
                    "Potenciais anuais de receita (R$ 48k a R$ 72k) são estimativas de teto inicial e NÃO constituem receita contratada.",
                ],
                uncertainties=[
                    "Taxa de conversão real de entrevistas para contratos recorrentes de curadoria B2B (será medida no Experimento A).",
                    "Tempo de isolamento dos conectores de terceiros no módulo Oracle (será medido no Experimento C).",
                ],
            ),
        )

        indicators = [
            MetricIndicator(
                indicator_id="ind:efficiency_leader",
                label="Maior Redução de Incerteza / R$ 1k",
                value=f"Exp C (108.6 pts) + Exp A (93.3 pts)",
                unit="pts/R$1k",
                is_estimate=True,
                source_refs=["src:exp:discovery_interviews_r1", "src:repo:license_manifest"],
                semantic_meaning="Combinação C + A exige apenas R$ 800 e destrava direitos + demanda comercial antes de escrever novo código pesado.",
            ),
            MetricIndicator(
                indicator_id="ind:realized_vs_committed",
                label="Valor Realizado vs. Custo Comprometido",
                value="R$ 3.700 / R$ 2.100",
                unit="BRL",
                is_estimate=False,
                source_refs=["src:data:sovereign_budget", "src:exp:discovery_interviews_r1"],
                semantic_meaning="Superávit observado de R$ 1.600 nos pilotos e grants iniciais, separado do potencial futuro estimado.",
            ),
            MetricIndicator(
                indicator_id="ind:phi_buffer",
                label="Índice de Soberania Fiduciária (Φ_buffer)",
                value=self.economics.phi_buffer_ratio,
                unit="x (mín 1.20x)",
                is_estimate=False,
                source_refs=["src:data:sovereign_budget"],
                semantic_meaning="Liquidez fiduciária saudável; permite alocar até R$ 1.500 neste sprint sem violar a margem de segurança.",
            ),
            MetricIndicator(
                indicator_id="ind:monetizable_no_chain",
                label="Artefatos Monetizáveis Sem Blockchain",
                value=f"{len(no_chain_artifacts)} de {len(all_artifacts)}",
                unit="artefatos",
                is_estimate=False,
                source_refs=["src:repo:proterol", "src:repo:valuecurator", "src:repo:planner"],
                semantic_meaning="100% dos módulos centrais geram valor via Micro-SaaS, API Semântica, CLI ou Grants sem exigir token.",
            ),
            MetricIndicator(
                indicator_id="ind:unclear_rights_alert",
                label="Artefatos com Direitos Pendentes",
                value=len(unclear_artifacts),
                unit="bloqueios",
                is_estimate=False,
                source_refs=["src:repo:license_manifest"],
                semantic_meaning="Wordsmith (clippings), Oracle (scrapers) e SovereignBudget (dados pessoais) exigem limpeza SPDX antes de licenciamento externo.",
            ),
            MetricIndicator(
                indicator_id="ind:estimated_potential_warning",
                label="Potencial Anual Estimado (Não Realizado)",
                value="R$ 180.000",
                unit="BRL/ano (Estimativa)",
                is_estimate=True,
                source_refs=["src:chatlog:compilatorum_synthesis"],
                semantic_meaning="Estimativa agregada de mercado para apoiar priorização; nunca tratada como caixa realizado.",
            ),
        ]

        # Constrói os payloads estruturados para TODAS as 5 representações infoestéticas
        visual_payloads = {
            "active_perspective": perspective.value,
            "1_radial_profile": {
                "opportunities": [opp.model_dump(mode="json") for opp in self.economics.opportunities.values()],
                "explicit_warning": (
                    "Atenção Infoestética: Dimensões com is_estimate=True representam estimativas sem validação empírica completa "
                    "e estão destacadas separadamente das dimensões observadas."
                ),
            },
            "2_knowledge_graph": {
                "nodes": [n.model_dump(mode="json") for n in all_artifacts],
                "edges": [e.model_dump(mode="json") for e in self.graph.edges],
                "topology_analysis": graph_topology,
                "unclear_rights_artifacts": [n.model_dump(mode="json") for n in unclear_artifacts],
            },
            "3_portfolio_mosaic": {
                "blocks": [
                    {
                        "block_id": opp.opportunity_id,
                        "title": opp.title,
                        "monetization_type": opp.monetization_type,
                        "requires_blockchain": opp.requires_blockchain,
                        "composite_score": opp.composite_score,
                        "committed_cost_brl": opp.committed_cost_brl,
                        "realized_value_brl": opp.realized_value_brl,
                        "estimated_potential_brl": opp.estimated_potential_brl,
                        "is_potential_estimate": True,
                        "estimated_dimensions_count": opp.estimated_dimensions_count,
                        "recommended_next_action": opp.recommended_next_action,
                    }
                    for opp in self.economics.opportunities.values()
                ]
                + [
                    {
                        "block_id": art.artifact_id,
                        "title": art.name,
                        "monetization_type": ", ".join(art.monetization_models),
                        "requires_blockchain": not art.monetizable_without_blockchain,
                        "composite_score": round(art.reusability_score * 10.0, 1),
                        "committed_cost_brl": 300.0,
                        "realized_value_brl": 500.0 if art.license_status == LicenseStatus.PERMISSIVE_COMMERCIAL else 0.0,
                        "estimated_potential_brl": 25000.0,
                        "is_potential_estimate": True,
                        "license_status": art.license_status.value,
                        "license_spdx": art.license_spdx,
                        "recommended_next_action": art.rights_notes,
                    }
                    for art in all_artifacts
                ]
            },
            "4_decision_matrix": {
                "x_axis": "Custo de Validação (R$ — menor é mais enxuto)",
                "y_axis": "Evidência Atual de Demanda (0-100)",
                "bubble_size": "Redução de Incerteza por R$ 1.000 investidos",
                "ranked_experiments": ranked_experiments,
                "budget_simulation": simulation,
            },
            "5_capital_flow": {
                "stages": [stage.model_dump(mode="json") for stage in self.economics.capital_flows],
                "executable_plan": executable_plan.model_dump(mode="json"),
            },
            "6_alchemical_emblem_and_lottie": self._build_alchemical_and_lottie_payload(),
            "canonical_prompts": CANONICAL_PROMPTS,
        }

        allowed_actions = [
            DeclarativeActionSpec(
                action_id="act:parameterize_lottie",
                action_type="parameterize_lottie_template",
                label="Parametrizar Infográfico Lottie & Vetor via JSON (LottieMCP)",
                target_id="alchemical_emblem",
                execution_mode="simulation",
                requires_human_approval=False,
                parameters={
                    "template_id": "alchemical_emblem",
                    "params_json": {
                        "realized_brl": 3700.0,
                        "committed_brl": 2100.0,
                        "uncertainty_reduction_pct": 80.0,
                        "synergy_score": 62.0,
                        "resonance_index": 0.85,
                        "pulse_frequency_hz": 1.45,
                    },
                },
            ),
            DeclarativeActionSpec(
                action_id="act:simulate_budget",
                action_type="simulate_allocation",
                label="Simular Alocação de Orçamento (C + A)",
                target_id="exp:C_automatizar_registro_licencas,exp:A_validar_demanda_curadoria",
                execution_mode="simulation",
                requires_human_approval=False,
                parameters={"budget_brl": 800.0, "selected_ids": ["exp:C_automatizar_registro_licencas", "exp:A_validar_demanda_curadoria"]},
            ),
            DeclarativeActionSpec(
                action_id="act:audit_rights",
                action_type="audit_artifact_rights",
                label="Aprovar Limpeza de Licenças (License Manifest)",
                target_id="art:wordsmith_ingestor",
                execution_mode="authorized_mutation",
                requires_human_approval=True,
                parameters={"new_spdx": "MIT", "audit_note": "Clippings de terceiros isolados; núcleo certificado MIT."},
            ),
            DeclarativeActionSpec(
                action_id="act:record_exp_a",
                action_type="register_experiment_result",
                label="Registrar Resultado Observado do Experimento A",
                target_id="exp:A_validar_demanda_curadoria",
                execution_mode="authorized_mutation",
                requires_human_approval=True,
                parameters={"realized_cost_brl": 420.0, "realized_revenue_brl": 1200.0},
            ),
            DeclarativeActionSpec(
                action_id="act:export_org",
                action_type="export_org_report",
                label="Exportar Relatório Semântico para Emacs / Org-mode",
                target_id="org_exporter",
                execution_mode="simulation",
                requires_human_approval=False,
                parameters={"format": "org-mode"},
            ),
        ]

        spec_hash = hashlib.sha256(f"{prompt}:{perspective.value}:{primary_rep.value}".encode("utf-8")).hexdigest()[:12]
        spec = DeclarativeUISpecification(
            spec_id=f"ui-spec-{spec_hash}",
            prompt=prompt,
            interpreted_intent=intent,
            perspective=perspective,
            primary_representation=primary_rep,
            title=classified["title"],
            subtitle=classified["subtitle"],
            semantic_compression=semantic_compression,
            indicators=indicators,
            visual_payloads=visual_payloads,
            allowed_actions=allowed_actions,
        )
        from pixelcoin.genui_md import GenUIMDAdapter, GenUIMDParser

        genui_doc = GenUIMDAdapter.from_declarative_spec(spec)
        spec.visual_payloads["genui_md_envelope"] = genui_doc.envelope.model_dump(mode="json", by_alias=True)
        spec.visual_payloads["genui_md_serialized"] = GenUIMDParser.serialize(genui_doc)
        return spec

    def _build_instant_view_by_intent(
        self,
        intent: str,
        perspective: PersonaPerspective,
        ranked_experiments: List[Dict[str, Any]],
        unclear_artifacts: List[Any],
        simulation: Dict[str, Any],
    ) -> tuple[str, str, str]:
        top_exp = ranked_experiments[0]
        second_exp = ranked_experiments[1]
        unclear_names = ", ".join(a.compilatorum_project for a in unclear_artifacts)

        if intent == "audit_unclear_rights_and_provenance":
            headline = (
                f"{len(unclear_artifacts)} módulos ({unclear_names}) possuem pendências de direitos que bloqueiam o licenciamento externo imediato."
            )
            priority = (
                "Executar Experimento C (Automatizar registro de licenças, R$ 350, 5 dias) para limpar conectores sem SPDX e isolar dados pessoais."
            )
            anomaly = (
                "Gargalo Jurídico Detectado: O módulo Oracle conecta o Proterol ao ValueCurator, mas herda scrapers com licença incerta."
            )
        elif intent == "analyze_repository_dependencies_and_synergies":
            headline = (
                "O Proterol (score 9.6/10) e o ValueCurator (9.3/10) são os maiores hubs reutilizáveis do Compilatorum, unidos por 9 nexos semânticos."
            )
            priority = (
                "Desacoplar os scrapers legados do Oracle e reutilizar os schemas SHA-256 do Proterol diretamente na API do ValueCurator."
            )
            anomaly = (
                "3 arestas críticas no grafo estão marcadas como gargalo por dependência de auditoria do License Manifest."
            )
        elif intent == "discover_non_blockchain_monetization_opportunities":
            headline = (
                "100% dos 7 artefatos centrais podem ser monetizados sem blockchain (via Micro-SaaS de Curadoria, API Semântica, CLI e Grants)."
            )
            priority = (
                "Priorizar a oferta de Curadoria Semântica (Wordsmith + ValueCurator) que já possui evidência empírica (83% de preferência sem cripto)."
            )
            anomaly = (
                "A API Semântica do Proterol tem alto potencial estimado (R$ 72k/ano), mas 2 de suas 6 dimensões radiais ainda são estimativas sem validação."
            )
        elif intent == "generate_executable_plan_and_capital_flow":
            headline = (
                "Plano de 4 semanas estruturado com orçamento total de R$ 1.300, preservando o buffer fiduciário (Φ_buffer = 1.31 >= 1.20)."
            )
            priority = (
                "Semana 1: Limpeza SPDX (R$ 350) → Semana 2: 8 Entrevistas e Oferta Simples (R$ 450) → Semana 3: Entrega Automatizada (R$ 300)."
            )
            anomaly = (
                "Portão Go/No-Go na Semana 2: Construção de infraestrutura adicional fica bloqueada se menos de 2 pilotos forem validados."
            )
        elif intent == "curate_investment_sea_and_compile_alchemical_emblem":
            headline = (
                "Mar de informações de investimento condensado em 52 Puxers Quantitativos e 1 Emblema Alquímico com Ressonância Lógico-Estética R_LE = 0.85."
            )
            priority = (
                "Cada Puxer Monetário (🜃 Terra / 🜄 Aqua) = R$ 250; cada Puxer Experimental (🜂 Ignis) = 5% ΔIncerteza; 6 templates LottieMCP prontos para parametrização via JSON."
            )
            anomaly = (
                "Equilíbrio harmônico entre Valor Realizado (15 puxers 🜃) e Capital Comprometido (8 puxers 🜄) aproxima-se da razão áurea φ = 1.618."
            )
        else:
            headline = (
                f"Ação de maior retorno informacional por unidade de recurso: {top_exp['title']} ({top_exp['efficiency_per_1k_brl']} pts/R$1k) "
                f"combinada com {second_exp['title']} ({second_exp['efficiency_per_1k_brl']} pts/R$1k)."
            )
            priority = simulation["recommendation_summary"]
            anomaly = (
                f"Evite iniciar pelo Experimento B (R$ 1.200) isoladamente: ele consome 80% do orçamento do sprint com menor redução de incerteza comercial."
            )

        if perspective == PersonaPerspective.DEVELOPER:
            headline = f"[VISÃO DEV] {headline} (Foco em contratos JSON Schema, isolamento de dependências e SPDX)."
        elif perspective == PersonaPerspective.SCIENTIFIC:
            headline = f"[VISÃO CIENTÍFICA] {headline} (Foco em ganho informacional ΔH/custo, rastreabilidade SHA-256 e separação hipótese vs. observação)."

        return headline, priority, anomaly

    def _build_alchemical_and_lottie_payload(self) -> Dict[str, Any]:
        """Compila a curadoria do mar de informações, o Emblema Alquímico de Puxers e os 6 templates LottieMCP."""
        streams = self.curator.curate_investment_streams({})
        emblem = self.curator.compile_alchemical_emblem(
            target_id="compilatorum_portfolio_nexus",
            realized_brl=3700.0,
            committed_brl=2100.0,
            uncertainty_reduction_pct=80.0,
            synergy_nodes_score=62.0,
            phi_buffer_ratio=self.economics.phi_buffer_ratio,
        )
        templates_catalog = LottieTemplateRegistry.list_templates()
        parameterized_bundles = {
            t["template_id"]: LottieTemplateRegistry.render_template(t["template_id"], {})
            for t in templates_catalog
        }
        return {
            "curated_investment_streams": [s.model_dump(mode="json") for s in streams],
            "alchemical_emblem": emblem.model_dump(mode="json"),
            "lottie_templates_catalog": templates_catalog,
            "parameterized_lotties": parameterized_bundles,
        }
