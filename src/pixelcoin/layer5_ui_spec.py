"""
Camada 5 — Especificação Declarativa de UI, Compressão Semântica e Guardrails

Define o modelo de interface semântica compartilhado entre Web, Emacs, Mobile e Agentes:
- 5 Representações Infoestéticas:
  1. Gráfico Radial (`radial_profile`)
  2. Grafo de Relações e Sinergias (`knowledge_graph`)
  3. Mosaico do Portfólio (`portfolio_mosaic`)
  4. Matriz de Decisão (`decision_matrix`)
  5. Fluxo de Capital em Movimento (`capital_flow`)
- Regra da Compressão Semântica em 3 níveis (Visão Instantânea, Inspeção, Rastreabilidade)
- 4 Regras de Controle / Guardrails da Seção 7 (Dados antes da estética, Explicabilidade, Ações autorizadas, Separação entre análise e execução)
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class VisualRepresentationType(str, Enum):
    RADIAL_PROFILE = "radial_profile"        # 1. Gráfico radial — perfil de uma oportunidade
    KNOWLEDGE_GRAPH = "knowledge_graph"      # 2. Grafo — relações e sinergias
    PORTFOLIO_MOSAIC = "portfolio_mosaic"    # 3. Mosaico — o panorama do portfólio
    DECISION_MATRIX = "decision_matrix"      # 4. Matriz de decisão — prioridade e incerteza
    CAPITAL_FLOW = "capital_flow"            # 5. Fluxo — capital em movimento
    ALCHEMICAL_EMBLEM = "alchemical_emblem"  # 6. Emblema Alquímico (Puxers + Vetor + Lottie)


class PersonaPerspective(str, Enum):
    EXECUTIVE = "executiva"      # Privilegia síntese, alocação, ROI e decisões
    DEVELOPER = "desenvolvedor"  # Privilegia repositórios, dependências, licenças SPDX e arquitetura
    SCIENTIFIC = "cientifica"    # Privilegia hipóteses, métodos, evidências, incertezas e equações


ALLOWED_DECLARATIVE_ACTIONS = {
    "select_opportunity",
    "simulate_allocation",
    "prioritize_experiment",
    "register_experiment_result",
    "audit_artifact_rights",
    "switch_representation",
    "switch_perspective",
    "export_org_report",
    "parameterize_lottie_template",
}

FORBIDDEN_UNCONTROLLED_OPERATIONS = {
    "transfer_funds_autonomous",
    "buy_market_asset_autonomous",
    "mint_speculative_token_autonomous",
    "eval_arbitrary_js",
}


class PixelCoinGuardrailError(Exception):
    """Exceção disparada quando uma regra da Seção 7 é violada."""


class MetricIndicator(BaseModel):
    """Unidade visual elementar ("Pixel" de decisão) com fonte ou marcação explícita de estimativa."""

    indicator_id: str
    label: str
    value: Any
    unit: str = ""
    is_estimate: bool = Field(
        ...,
        description="Regra 1 (Dados antes da estética): True se estimativa; False apenas se houver dado observado",
    )
    source_refs: List[str] = Field(
        default_factory=list,
        description="IDs de fontes na Camada 1 que sustentam este indicador",
    )
    semantic_meaning: str = Field(
        ..., description="Consequência ou significado deste indicador para a decisão"
    )

    @model_validator(mode="after")
    def validate_data_before_aesthetics(self) -> "MetricIndicator":
        # Regra 1: Todo indicador deve ter uma fonte ou ser explicitamente identificado como estimativa
        if not self.is_estimate and not self.source_refs:
            raise PixelCoinGuardrailError(
                f"Violação da Regra 1 (Dados antes da estética): O indicador '{self.indicator_id}' "
                "está marcado como dado observado (is_estimate=False), mas não possui fontes (source_refs)."
            )
        return self


class InstantViewLayer(BaseModel):
    """Nível 1 da Compressão Semântica: Visão instantânea (o sinal principal, a prioridade ou a anomalia)."""

    headline_signal: str = Field(..., description="Sinal principal em uma frase direta")
    top_priority_action: str = Field(..., description="Ação prioritária recomendada agora")
    detected_anomaly_or_bottleneck: str = Field(
        ..., description="Anomalia, bloqueio de direitos ou gargalo que exige atenção"
    )


class InspectionLayer(BaseModel):
    """Nível 2 da Compressão Semântica: Inspeção (fatores que explicam a representação)."""

    causal_factors: List[str] = Field(..., description="Fatores que explicam por que a recomendação aparece assim")
    observed_vs_estimated_breakdown: str = Field(
        ...,
        description="Transparência explícita sobre quantas dimensões/métricas são observadas vs. estimadas",
    )
    decision_criteria_used: List[str] = Field(..., description="Critérios explícitos de priorização aplicados")
    alternative_scenarios: List[str] = Field(default_factory=list, description="Cenários alternativos comparados")


class TraceabilityLayer(BaseModel):
    """Nível 3 da Compressão Semântica: Rastreabilidade (fontes, premissas, versões, incertezas e dados originais)."""

    source_records: List[Dict[str, str]] = Field(
        ..., description="Fontes primárias com ID, título, URI e hash SHA-256"
    )
    assumptions: List[str] = Field(..., description="Premissas assumidas na análise")
    uncertainties: List[str] = Field(..., description="Incertezas remanescentes que precisam de validação")
    schema_version: str = "pixelcoin-ui-spec/1.0.0"


class SemanticCompressionTriad(BaseModel):
    """Estrutura obrigatória dos 3 níveis da Regra da Compressão Semântica."""

    instant_view: InstantViewLayer
    inspection: InspectionLayer
    traceability: TraceabilityLayer


class DeclarativeActionSpec(BaseModel):
    """Ação declarativa permitida na Especificação de UI (Camada 5)."""

    action_id: str
    action_type: str = Field(..., description="Deve pertencer a ALLOWED_DECLARATIVE_ACTIONS")
    label: str
    target_id: str
    execution_mode: str = Field(
        default="simulation",
        description="simulation | authorized_mutation (Regra 4: separação entre análise e execução)",
    )
    requires_human_approval: bool = Field(
        default=True,
        description="Operações que registram decisões ou alteram estado exigem confirmação explícita",
    )
    parameters: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_authorized_action(self) -> "DeclarativeActionSpec":
        if self.action_type in FORBIDDEN_UNCONTROLLED_OPERATIONS:
            raise PixelCoinGuardrailError(
                f"Violação da Regra 3/4: Operação financeira autônoma ou código arbitrário proibido: '{self.action_type}'."
            )
        if self.action_type not in ALLOWED_DECLARATIVE_ACTIONS:
            raise PixelCoinGuardrailError(
                f"Violação da Regra 3 (Ações autorizadas): Ação '{self.action_type}' não faz parte do conjunto permitido."
            )
        return self


class DeclarativeUISpecification(BaseModel):
    """
    Especificação declarativa completa da UI gerada pela Camada 4 (Server-Driven / Generative UI)
    e consumida pelos renderizadores da Camada 6 (Web, Emacs, Mobile, Agentes).
    """

    spec_id: str
    prompt: str
    interpreted_intent: str
    perspective: PersonaPerspective = PersonaPerspective.EXECUTIVE
    primary_representation: VisualRepresentationType
    available_representations: List[VisualRepresentationType] = Field(
        default_factory=lambda: [
            VisualRepresentationType.RADIAL_PROFILE,
            VisualRepresentationType.KNOWLEDGE_GRAPH,
            VisualRepresentationType.PORTFOLIO_MOSAIC,
            VisualRepresentationType.DECISION_MATRIX,
            VisualRepresentationType.CAPITAL_FLOW,
            VisualRepresentationType.ALCHEMICAL_EMBLEM,
        ]
    )
    title: str
    subtitle: str
    semantic_compression: SemanticCompressionTriad
    indicators: List[MetricIndicator]
    visual_payloads: Dict[str, Any] = Field(
        ...,
        description="Dados estruturados para as 5 representações infoestéticas (radial, graph, mosaic, matrix, flow) e catálogos/planos",
    )
    allowed_actions: List[DeclarativeActionSpec]
    guardrail_attestation: Dict[str, Any] = Field(
        default_factory=lambda: {
            "data_before_aesthetics": True,
            "explainability_3_levels": True,
            "authorized_actions_only": True,
            "analysis_execution_separated": True,
            "arbitrary_js_execution": False,
        }
    )

    @model_validator(mode="after")
    def validate_guardrails(self) -> "DeclarativeUISpecification":
        if not self.semantic_compression.instant_view.headline_signal:
            raise PixelCoinGuardrailError("Violação da Regra 2 (Explicabilidade): Visão instantânea vazia.")
        if not self.semantic_compression.traceability.source_records:
            raise PixelCoinGuardrailError(
                "Violação da Regra 2 (Rastreabilidade): A especificação deve referenciar pelo menos uma fonte verificável."
            )
        return self
