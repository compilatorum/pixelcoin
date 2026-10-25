"""
Camada 3 — Inteligência Econômica (Economic Intelligence Layer)

Transforma informação curada do Compilatorum em decisões de alocação de recursos:
- Perfis Radiais de Oportunidades (6 dimensões explícitas com distinção entre evidência observada e estimativa)
- Portfólio de Experimentos (Testar, Validar, Preparar, Financiar) e cálculo de Redução de Incerteza por Unidade de Recurso
- Mosaico do Portfólio (separando estritamente Valor Realizado, Custo Comprometido e Potencial Estimado)
- Matriz de Decisão (Evidência de Demanda vs. Custo de Validação)
- Fluxo de Capital em Movimento (Previsto, Comprometido, Realizado)
- Planos Executáveis com Cronograma, Tarefas, Recursos e Critérios de Validação
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from pixelcoin.layer2_graph import SemanticKnowledgeGraph


class ExperimentTag(str, Enum):
    TESTAR = "Testar"
    VALIDAR = "Validar"
    PREPARAR = "Preparar"
    FINANCIAR = "Financiar"


class RadialDimensionScore(BaseModel):
    """Pontuação de uma dimensão no Gráfico Radial com rastreabilidade explícita."""

    dimension_key: str = Field(..., description="evidence | utility | feasibility | risk_control | rights_clarity | commercial_readiness")
    label: str = Field(..., description="Nome legível da dimensão")
    score: float = Field(..., ge=0.0, le=100.0, description="Nota de 0 a 100")
    scale_criteria: str = Field(..., description="Critério explícito da escala para evitar notas arbitrárias")
    is_estimate: bool = Field(
        ...,
        description="True se esta dimensão foi estimada sem evidência empírica direta; False se sustentada por evidência observada",
    )
    basis_explanation: str = Field(..., description="Explicação do porquê desta nota e qual a evidência/premissa")
    source_id: str = Field(..., description="ID da fonte na Camada 1 que sustenta ou contextualiza a nota")


class OpportunityProfile(BaseModel):
    """Ficha completa de uma oportunidade comercial ou de licenciamento do Compilatorum."""

    opportunity_id: str
    title: str
    subtitle: str
    related_artifact_ids: List[str]
    monetization_type: str = Field(..., description="Ex: Micro-SaaS, API Semântica, Licenciamento B2B, Grant Científico")
    requires_blockchain: bool = False
    radial_dimensions: List[RadialDimensionScore]
    committed_cost_brl: float = Field(..., ge=0.0, description="Custo já comprometido/gasto (observado)")
    realized_value_brl: float = Field(..., ge=0.0, description="Valor financeiro já realizado/recebido (observado)")
    estimated_potential_brl: float = Field(..., ge=0.0, description="Potencial anual estimado (explicitamente marcado como estimativa)")
    key_risks: List[str]
    recommended_next_action: str

    @property
    def estimated_dimensions_count(self) -> int:
        return sum(1 for d in self.radial_dimensions if d.is_estimate)

    @property
    def composite_score(self) -> float:
        if not self.radial_dimensions:
            return 0.0
        return round(sum(d.score for d in self.radial_dimensions) / len(self.radial_dimensions), 1)


class ExperimentOption(BaseModel):
    """Experimento de validação ou preparação com relação custo vs. redução de incerteza."""

    experiment_id: str
    code: str = Field(..., description="Código curto: A, B, C, D")
    title: str
    subtitle: str
    tag: ExperimentTag
    objective: str
    related_opportunity_id: str
    related_artifact_ids: List[str]
    cost_brl: float = Field(..., gt=0.0, description="Custo estimado de execução em R$")
    duration_days: int = Field(..., gt=0, description="Duração estimada em dias")
    uncertainty_reduction_pct: float = Field(
        ..., ge=0.0, le=100.0, description="Redução esperada de incerteza crítica (0 a 100%)"
    )
    demand_evidence_score: float = Field(
        ..., ge=0.0, le=100.0, description="Evidência atual de demanda antes do experimento (0 a 100)"
    )
    is_cost_estimate: bool = True
    validation_criteria: List[str]
    source_ids: List[str]
    status: str = Field(default="pending", description="pending | simulated | approved | completed")
    recorded_outcome: Optional[str] = None

    @property
    def uncertainty_reduction_per_1k_brl(self) -> float:
        """Retorna quantos pontos percentuais de incerteza são reduzidos por R$ 1.000 investidos."""
        return round((self.uncertainty_reduction_pct / self.cost_brl) * 1000.0, 2)


class CapitalFlowStage(BaseModel):
    """Estágio do fluxo de capital em movimento (Seção 2.5)."""

    stage_id: str
    stage_name: str = Field(..., description="Alocação | Execução | Marcos | Resultados | Reinvestimento")
    description: str
    planned_brl: float = Field(..., ge=0.0, description="Valor previsto em R$")
    committed_brl: float = Field(..., ge=0.0, description="Valor comprometido em R$")
    realized_brl: float = Field(..., ge=0.0, description="Valor efetivamente realizado em R$")
    linked_items: List[str]
    source_id: str


class ExecutableTask(BaseModel):
    """Tarefa dentro de um plano executável derivado de uma oportunidade."""

    task_id: str
    week: str
    title: str
    owner_module: str
    resource_brl: float
    deliverable: str
    validation_metric: str


class ExecutableActionPlan(BaseModel):
    """Plano executável gerado para transformar uma oportunidade em ação."""

    plan_id: str
    opportunity_id: str
    title: str
    total_budget_brl: float
    duration_weeks: int
    tasks: List[ExecutableTask]
    go_no_go_criteria: List[str]
    risk_mitigations: List[str]


class EconomicIntelligenceEngine:
    """
    Camada 3: Motor de Inteligência Econômica do PixelCoin.
    Avalia oportunidades, compara experimentos sob restrição orçamentária,
    separa valor realizado de potencial estimado e rastreia o fluxo de capital.
    """

    def __init__(self, graph: Optional[SemanticKnowledgeGraph] = None) -> None:
        self.graph = graph or SemanticKnowledgeGraph()
        self.available_budget_brl: float = 4500.0
        self.phi_buffer_ratio: float = 1.34
        self.phi_buffer_min: float = 1.20
        self.opportunities: Dict[str, OpportunityProfile] = {}
        self.experiments: Dict[str, ExperimentOption] = {}
        self.capital_flows: List[CapitalFlowStage] = []
        self.decision_log: List[Dict[str, Any]] = []
        self._init_economic_models()

    def _init_economic_models(self) -> None:
        opps = [
            OpportunityProfile(
                opportunity_id="opp:curadoria_corpus_b2b",
                title="Oferta de Curadoria Semântica & Higienização de Corpus (Wordsmith + ValueCurator)",
                subtitle="Serviço productizado e Micro-SaaS para transformar chatlogs, docs e repositórios dispersos em bases acionáveis",
                related_artifact_ids=["art:wordsmith_ingestor", "art:valuecurator_core", "art:license_manifest"],
                monetization_type="Serviço Productizado / Micro-SaaS (Sem Blockchain)",
                requires_blockchain=False,
                committed_cost_brl=650.0,
                realized_value_brl=1200.0,
                estimated_potential_brl=48000.0,
                radial_dimensions=[
                    RadialDimensionScore(
                        dimension_key="evidence",
                        label="Evidência de Demanda",
                        score=84.0,
                        scale_criteria="0=Sem entrevistas, 50=Interesse verbal, 80+=Entrevistas documentadas + piloto pago",
                        is_estimate=False,
                        basis_explanation="Rodada E0 com 12 entrevistas mostrou que 10/12 pagariam por síntese acionável sem blockchain.",
                        source_id="src:exp:discovery_interviews_r1",
                    ),
                    RadialDimensionScore(
                        dimension_key="utility",
                        label="Utilidade Prática",
                        score=90.0,
                        scale_criteria="Redução mensurável de trabalho manual repetitivo de organização de conhecimento",
                        is_estimate=False,
                        basis_explanation="Wordsmith já processou 1.87MB de logs reais reduzindo triagem manual de dias para minutos.",
                        source_id="src:repo:wordsmith",
                    ),
                    RadialDimensionScore(
                        dimension_key="feasibility",
                        label="Viabilidade Técnica",
                        score=88.0,
                        scale_criteria="Disponibilidade de código funcional e testes no workspace",
                        is_estimate=False,
                        basis_explanation="Pipeline Python + SQLite + Discovery UI já operacionais localmente.",
                        source_id="src:repo:valuecurator",
                    ),
                    RadialDimensionScore(
                        dimension_key="risk_control",
                        label="Segurança / Baixo Risco",
                        score=82.0,
                        scale_criteria="Inverso da exposição financeira e operacional (100 = risco mínimo)",
                        is_estimate=False,
                        basis_explanation="Baixo custo de validação (R$ 450) preserva folga no Phi_buffer (1.34 >= 1.20).",
                        source_id="src:data:sovereign_budget",
                    ),
                    RadialDimensionScore(
                        dimension_key="rights_clarity",
                        label="Clareza dos Direitos",
                        score=68.0,
                        scale_criteria="100=SPDX limpo em toda a cadeia; <75=Requer higienização de datasets de terceiros",
                        is_estimate=False,
                        basis_explanation="Motor é MIT/Apache-2.0, mas templates de exemplos do Wordsmith contêm clippings pendentes de limpeza.",
                        source_id="src:repo:license_manifest",
                    ),
                    RadialDimensionScore(
                        dimension_key="commercial_readiness",
                        label="Prontidão Comercial",
                        score=76.0,
                        scale_criteria="Existência de página de oferta, contrato de serviço e precificação validada",
                        is_estimate=True,
                        basis_explanation="Estimativa: falta validar preço recorrente mensal em teste de oferta simples com 5 compradores.",
                        source_id="src:chatlog:compilatorum_synthesis",
                    ),
                ],
                key_risks=[
                    "Escopo de curadoria virar consultoria manual se não limitar formatos de entrada (JSONL/Markdown/Git)",
                    "Necessidade de separar clippings pessoais do pacote distribuível",
                ],
                recommended_next_action="Executar Experimento A (Validar demanda por curadoria com 5 entrevistas e oferta simples por R$ 450).",
            ),
            OpportunityProfile(
                opportunity_id="opp:api_semantica_proterol",
                title="API Semântica & SDK de Ontologia Executável (Proterol + Oracle)",
                subtitle="Licenciamento técnico e API para transformar repositórios e especificações em grafos tipados com provas SHA-256",
                related_artifact_ids=["art:proterol_engine", "art:oracle_associative", "art:license_manifest"],
                monetization_type="API SaaS B2D / Licenciamento Dual (Sem Blockchain)",
                requires_blockchain=False,
                committed_cost_brl=950.0,
                realized_value_brl=0.0,
                estimated_potential_brl=72000.0,
                radial_dimensions=[
                    RadialDimensionScore(
                        dimension_key="evidence",
                        label="Evidência de Demanda",
                        score=58.0,
                        scale_criteria="0=Sem entrevistas, 50=Hipótese validada internamente, 80+=Clientes externos testando",
                        is_estimate=True,
                        basis_explanation="Estimativa baseada em hipótese de chatlog (redução de 65% no onboarding); ainda sem benchmark externo pago.",
                        source_id="src:chatlog:compilatorum_synthesis",
                    ),
                    RadialDimensionScore(
                        dimension_key="utility",
                        label="Utilidade Prática",
                        score=86.0,
                        scale_criteria="Capacidade de reutilização transversal entre projetos e agentes",
                        is_estimate=False,
                        basis_explanation="Proterol já compila genes semânticos e provas verificáveis usados por outros módulos.",
                        source_id="src:repo:proterol",
                    ),
                    RadialDimensionScore(
                        dimension_key="feasibility",
                        label="Viabilidade Técnica",
                        score=92.0,
                        scale_criteria="Maturidade do compilador e cobertura de testes automatizados",
                        is_estimate=False,
                        basis_explanation="Compilador Proterol v1.0.0 completo em Python com suíte pytest passando 100%.",
                        source_id="src:repo:proterol",
                    ),
                    RadialDimensionScore(
                        dimension_key="risk_control",
                        label="Segurança / Baixo Risco",
                        score=70.0,
                        scale_criteria="Risco de construir API pública antes de confirmar integração com o Oracle",
                        is_estimate=False,
                        basis_explanation="Custo de prototipação de API (R$ 1.200) consome 26% do orçamento livre de experimentos.",
                        source_id="src:data:sovereign_budget",
                    ),
                    RadialDimensionScore(
                        dimension_key="rights_clarity",
                        label="Clareza dos Direitos",
                        score=95.0,
                        scale_criteria="Clareza de licença do núcleo Proterol (MIT)",
                        is_estimate=False,
                        basis_explanation="Núcleo Proterol é 100% MIT autoral; contudo, acoplamento com scrapers do Oracle exige isolamento.",
                        source_id="src:repo:proterol",
                    ),
                    RadialDimensionScore(
                        dimension_key="commercial_readiness",
                        label="Prontidão Comercial",
                        score=54.0,
                        scale_criteria="Existência de documentação de integração rápida, billing e SLA",
                        is_estimate=True,
                        basis_explanation="Estimativa: requer empacotamento REST/MCP e avaliação de latência em repositórios de terceiros.",
                        source_id="src:chatlog:compilatorum_synthesis",
                    ),
                ],
                key_risks=[
                    "Risco de sobre-engenharia caso a API seja construída sem validar o caso de uso mais urgente dos desenvolvedores",
                    "Dependência indireta do módulo Oracle que possui conectores com licença pendente",
                ],
                recommended_next_action="Executar Experimento B (Protótipo enxuto da API semântica focado em 1 endpoint de inspeção de repositório).",
            ),
            OpportunityProfile(
                opportunity_id="opp:governaut_grants_automation",
                title="Copiloto de Submissão a Grants & Governança Orientada por Evidências (Planner + Governaut OS)",
                subtitle="Uso interno e licenciamento para captar grants científicos/tecnológicos e estruturar propostas auditáveis",
                related_artifact_ids=["art:planner_governaut", "art:valuecurator_core", "art:proterol_engine"],
                monetization_type="Captação de Grants + Assinatura B2B/DAO",
                requires_blockchain=False,
                committed_cost_brl=500.0,
                realized_value_brl=2500.0,
                estimated_potential_brl=60000.0,
                radial_dimensions=[
                    RadialDimensionScore(
                        dimension_key="evidence",
                        label="Evidência de Demanda",
                        score=78.0,
                        scale_criteria="Histórico de submissões e validação do pipeline L0-L5",
                        is_estimate=False,
                        basis_explanation="Pipeline completo já utilizado em submissões reais e auditorias de propostas.",
                        source_id="src:repo:planner",
                    ),
                    RadialDimensionScore(
                        dimension_key="utility",
                        label="Utilidade Prática",
                        score=88.0,
                        scale_criteria="Economia de horas na redação e auditoria de propostas técnicas",
                        is_estimate=False,
                        basis_explanation="Orquestrador automatiza desde roteamento de intenção até revisão crítica por 3 personas.",
                        source_id="src:repo:planner",
                    ),
                    RadialDimensionScore(
                        dimension_key="feasibility",
                        label="Viabilidade Técnica",
                        score=94.0,
                        scale_criteria="Sistema operacional e servidor HTTP JSON prontos",
                        is_estimate=False,
                        basis_explanation="Governaut OS v0.1.0 possui CLI, API HTTP e guardrails testados.",
                        source_id="src:repo:planner",
                    ),
                    RadialDimensionScore(
                        dimension_key="risk_control",
                        label="Segurança / Baixo Risco",
                        score=89.0,
                        scale_criteria="Presença de guardrails Human-in-the-Loop e custo marginal baixo",
                        is_estimate=False,
                        basis_explanation="EthicsGuard, CitationGuard e HumanInTheLoopGate impedem ações autônomas de risco.",
                        source_id="src:repo:planner",
                    ),
                    RadialDimensionScore(
                        dimension_key="rights_clarity",
                        label="Clareza dos Direitos",
                        score=96.0,
                        scale_criteria="Licenciamento MIT limpo",
                        is_estimate=False,
                        basis_explanation="Repositório Governaut OS possui direitos claros e sem dependências restritivas.",
                        source_id="src:repo:planner",
                    ),
                    RadialDimensionScore(
                        dimension_key="commercial_readiness",
                        label="Prontidão Comercial",
                        score=72.0,
                        scale_criteria="Adaptação para editais de subvenção (FAPESP/FINEP/Open Source Grants)",
                        is_estimate=True,
                        basis_explanation="Estimativa: templates para editais tradicionais fora de Web3 ainda precisam de ajuste fino.",
                        source_id="src:repo:planner",
                    ),
                ],
                key_risks=[
                    "Ciclo de aprovação de grants demora de 30 a 90 dias para liquidação em caixa",
                ],
                recommended_next_action="Combinar com o Experimento C (Auditoria de licenças) para submeter o dossiê técnico completo a 2 grants.",
            ),
        ]
        for opp in opps:
            self.opportunities[opp.opportunity_id] = opp

        exps = [
            ExperimentOption(
                experiment_id="exp:A_validar_demanda_curadoria",
                code="A",
                title="A. Validar demanda por curadoria",
                subtitle="Entrevistas e teste de uma oferta simples",
                tag=ExperimentTag.TESTAR,
                objective="Descobrir se existe um comprador imediato e qual problema específico ele pagaria para resolver com o Wordsmith + ValueCurator.",
                related_opportunity_id="opp:curadoria_corpus_b2b",
                related_artifact_ids=["art:wordsmith_ingestor", "art:valuecurator_core"],
                cost_brl=450.0,
                duration_days=7,
                uncertainty_reduction_pct=42.0,
                demand_evidence_score=84.0,
                is_cost_estimate=True,
                validation_criteria=[
                    "Realizar 8 entrevistas estruturadas usando o roteiro científico do ValueCurator (/interview)",
                    "Apresentar página de oferta de diagnóstico de corpus por R$ 600 e obter pelo menos 2 pré-reservas",
                    "Registrar objeções reais sobre formatos de dados e confidencialidade",
                ],
                source_ids=["src:exp:discovery_interviews_r1", "src:repo:valuecurator", "src:data:sovereign_budget"],
            ),
            ExperimentOption(
                experiment_id="exp:B_construir_api_semantica",
                code="B",
                title="B. Construir uma API semântica",
                subtitle="Protótipo técnico e avaliação de reutilização",
                tag=ExperimentTag.VALIDAR,
                objective="Medir se a capacidade técnica do compilador Proterol + Oracle pode ser transformada em uma oferta utilizável por terceiros.",
                related_opportunity_id="opp:api_semantica_proterol",
                related_artifact_ids=["art:proterol_engine", "art:oracle_associative"],
                cost_brl=1200.0,
                duration_days=14,
                uncertainty_reduction_pct=35.0,
                demand_evidence_score=58.0,
                is_cost_estimate=True,
                validation_criteria=[
                    "Expor endpoint REST/MCP determinístico que recebe um repositório e devolve o grafo semântico JSON-LD",
                    "Testar reutilização em 3 projetos reais do Compilatorum com tempo de resposta < 2s",
                    "Medir se 3 desenvolvedores externos conseguem integrar o SDK em menos de 15 minutos",
                ],
                source_ids=["src:repo:proterol", "src:repo:oracle", "src:chatlog:compilatorum_synthesis"],
            ),
            ExperimentOption(
                experiment_id="exp:C_automatizar_registro_licencas",
                code="C",
                title="C. Automatizar o registro de licenças",
                subtitle="Manifestos, direitos e proveniência",
                tag=ExperimentTag.PREPARAR,
                objective="Esclarecer direitos pendentes e tornar os artefatos (Wordsmith, Oracle, SovereignBudget) aptos à exploração comercial segura.",
                related_opportunity_id="opp:curadoria_corpus_b2b",
                related_artifact_ids=["art:license_manifest", "art:wordsmith_ingestor", "art:oracle_associative"],
                cost_brl=350.0,
                duration_days=5,
                uncertainty_reduction_pct=38.0,
                demand_evidence_score=76.0,
                is_cost_estimate=True,
                validation_criteria=[
                    "Gerar arquivo LICENSE_MANIFEST.json assinado com SHA-256 para todos os 7 módulos do Compilatorum",
                    "Isolar clippings de terceiros do Wordsmith e substituir scrapers sem SPDX no Oracle por conectores MIT",
                    "Zerar o contador de gargalos jurídicos na Camada 2 antes de assinar contratos B2B",
                ],
                source_ids=["src:repo:license_manifest", "src:repo:wordsmith", "src:repo:oracle"],
            ),
            ExperimentOption(
                experiment_id="exp:D_submeter_grant_compilatorum",
                code="D",
                title="D. Submeter dossiê técnico a Grant de P&D Open-Source",
                subtitle="Empacotamento de provas empíricas e submissão não-dilutiva",
                tag=ExperimentTag.FINANCIAR,
                objective="Mobilizar financiamento não-dilutivo para o ecossistema Compilatorum usando o histórico de provas do Proterol e Governaut OS.",
                related_opportunity_id="opp:governaut_grants_automation",
                related_artifact_ids=["art:planner_governaut", "art:proterol_engine"],
                cost_brl=500.0,
                duration_days=10,
                uncertainty_reduction_pct=30.0,
                demand_evidence_score=78.0,
                is_cost_estimate=True,
                validation_criteria=[
                    "Gerar dossiê técnico verificável combinando Proterol Codex + Governaut OS",
                    "Submeter a 2 programas de grant de infraestrutura aberta com orçamento detalhado",
                ],
                source_ids=["src:repo:planner", "src:repo:proterol"],
            ),
        ]
        for exp in exps:
            self.experiments[exp.experiment_id] = exp

        self.capital_flows = [
            CapitalFlowStage(
                stage_id="flow:1_alocacao",
                stage_name="1. Alocação (Orçamento Soberano)",
                description="Reserva de capital de experimentação respeitando a restrição fiduciária Phi_buffer >= 1.20 no Sovereign Budget.",
                planned_brl=4500.0,
                committed_brl=2100.0,
                realized_brl=2100.0,
                linked_items=["art:sovereign_budget_thermo"],
                source_id="src:data:sovereign_budget",
            ),
            CapitalFlowStage(
                stage_id="flow:2_execucao",
                stage_name="2. Execução de Experimentos",
                description="Mobilização de recursos nos experimentos priorizados (C: Licenças R$ 350, A: Curadoria R$ 450, B: API R$ 1.200).",
                planned_brl=2500.0,
                committed_brl=800.0,
                realized_brl=650.0,
                linked_items=["exp:C_automatizar_registro_licencas", "exp:A_validar_demanda_curadoria", "exp:B_construir_api_semantica"],
                source_id="src:exp:discovery_interviews_r1",
            ),
            CapitalFlowStage(
                stage_id="flow:3_marcos",
                stage_name="3. Marcos de Validação (Evidence Gates)",
                description="Portões determinísticos do ValueCurator que liberam ou pausam a próxima tranche conforme a evidência observada.",
                planned_brl=2000.0,
                committed_brl=1300.0,
                realized_brl=950.0,
                linked_items=["art:valuecurator_core", "art:license_manifest"],
                source_id="src:repo:valuecurator",
            ),
            CapitalFlowStage(
                stage_id="flow:4_resultados",
                stage_name="4. Resultados & Receita Validada",
                description="Retorno observado de pilotos de curadoria e grants iniciais versus potencial anual estimado.",
                planned_brl=12000.0,
                committed_brl=3700.0,
                realized_brl=3700.0,
                linked_items=["opp:curadoria_corpus_b2b", "opp:governaut_grants_automation"],
                source_id="src:exp:discovery_interviews_r1",
            ),
            CapitalFlowStage(
                stage_id="flow:5_reinvestimento",
                stage_name="5. Reinvestimento no Compilatorum",
                description="Realocação dos excedentes validados de volta na infraestrutura semântica (Proterol + PixelCoin).",
                planned_brl=3000.0,
                committed_brl=1100.0,
                realized_brl=1100.0,
                linked_items=["art:proterol_engine", "art:planner_governaut"],
                source_id="src:data:sovereign_budget",
            ),
        ]

    def rank_experiments_by_efficiency(self, max_budget_brl: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Ordena os experimentos pela maior redução de incerteza por unidade de recurso
        (Delta Incerteza / R$ 1.000), respeitando um teto orçamentário opcional.
        """
        budget = max_budget_brl if max_budget_brl is not None else self.available_budget_brl
        sorted_exps = sorted(
            self.experiments.values(),
            key=lambda e: e.uncertainty_reduction_per_1k_brl,
            reverse=True,
        )
        cumulative_cost = 0.0
        ranked: List[Dict[str, Any]] = []
        for rank_idx, exp in enumerate(sorted_exps, start=1):
            fits_budget = (cumulative_cost + exp.cost_brl) <= budget
            if fits_budget:
                cumulative_cost += exp.cost_brl
            ranked.append(
                {
                    "rank": rank_idx,
                    "experiment_id": exp.experiment_id,
                    "code": exp.code,
                    "title": exp.title,
                    "subtitle": exp.subtitle,
                    "tag": exp.tag.value,
                    "objective": exp.objective,
                    "cost_brl": exp.cost_brl,
                    "duration_days": exp.duration_days,
                    "uncertainty_reduction_pct": exp.uncertainty_reduction_pct,
                    "efficiency_per_1k_brl": exp.uncertainty_reduction_per_1k_brl,
                    "demand_evidence_score": exp.demand_evidence_score,
                    "fits_in_budget": fits_budget,
                    "cumulative_cost_if_selected_brl": round(cumulative_cost, 2) if fits_budget else None,
                    "validation_criteria": exp.validation_criteria,
                    "source_ids": exp.source_ids,
                    "status": exp.status,
                }
            )
        return ranked

    def simulate_allocation(self, budget_brl: float, selected_experiment_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Simula uma alocação de recursos (Modo Simulação — separação estrita entre análise e execução).
        Verifica se o orçamento proposto preserva a inequação de soberania cambial Phi_buffer >= 1.20.
        """
        if selected_experiment_ids:
            chosen = [self.experiments[eid] for eid in selected_experiment_ids if eid in self.experiments]
        else:
            ranked = self.rank_experiments_by_efficiency(max_budget_brl=budget_brl)
            chosen = [self.experiments[r["experiment_id"]] for r in ranked if r["fits_in_budget"]]

        total_cost = sum(e.cost_brl for e in chosen)
        # Simula impacto no Phi_buffer (cada R$ 1.000 acima de R$ 1.500 reduz Phi_buffer em 0.05)
        simulated_phi = round(self.phi_buffer_ratio - max(0.0, (total_cost - 500.0) / 1000.0) * 0.04, 3)
        respects_sovereign_buffer = simulated_phi >= self.phi_buffer_min and total_cost <= self.available_budget_brl

        combined_uncertainty_reduction = round(
            min(95.0, sum(e.uncertainty_reduction_pct * 0.85 for e in chosen)), 1
        )
        return {
            "mode": "simulation_only",
            "financial_execution_performed": False,
            "input_budget_brl": budget_brl,
            "total_simulated_cost_brl": total_cost,
            "remaining_budget_brl": round(budget_brl - total_cost, 2),
            "simulated_phi_buffer": simulated_phi,
            "phi_buffer_minimum": self.phi_buffer_min,
            "respects_sovereign_buffer": respects_sovereign_buffer,
            "combined_uncertainty_reduction_pct": combined_uncertainty_reduction,
            "selected_experiments": [
                {
                    "experiment_id": e.experiment_id,
                    "code": e.code,
                    "title": e.title,
                    "tag": e.tag.value,
                    "cost_brl": e.cost_brl,
                    "efficiency_per_1k_brl": e.uncertainty_reduction_per_1k_brl,
                }
                for e in chosen
            ],
            "recommendation_summary": (
                f"Combinar {[e.code for e in chosen]} consome R$ {total_cost:.2f}, preserva Phi_buffer={simulated_phi} (>= 1.20) "
                f"e reduz incerteza crítica estimada em {combined_uncertainty_reduction}%."
                if respects_sovereign_buffer
                else f"Atenção: Custo simulado de R$ {total_cost:.2f} pressiona o buffer fiduciário (Phi_buffer={simulated_phi}). Priorize apenas C e A."
            ),
        }

    def build_executable_plan(self, opportunity_id: str = "opp:curadoria_corpus_b2b") -> ExecutableActionPlan:
        """Transforma uma oportunidade em um plano executável com cronograma, tarefas e critérios de validação."""
        opp = self.opportunities.get(opportunity_id) or next(iter(self.opportunities.values()))
        return ExecutableActionPlan(
            plan_id=f"plan:{opp.opportunity_id.split(':')[-1]}",
            opportunity_id=opp.opportunity_id,
            title=f"Plano Executável — {opp.title}",
            total_budget_brl=1300.0,
            duration_weeks=4,
            tasks=[
                ExecutableTask(
                    task_id="task:w1_rights_audit",
                    week="Semana 1",
                    title="Executar Experimento C: Auditoria de Proveniência e Limpeza SPDX",
                    owner_module="License Manifest",
                    resource_brl=350.0,
                    deliverable="LICENSE_MANIFEST.json assinado + isolamento de clippings de terceiros no Wordsmith",
                    validation_metric="100% dos arquivos distribuíveis com cabeçalho SPDX MIT/Apache-2.0 verificável",
                ),
                ExecutableTask(
                    task_id="task:w2_customer_discovery",
                    week="Semana 2",
                    title="Executar Experimento A: 8 Entrevistas de Descoberta e Teste de Oferta Simples",
                    owner_module="ValueCurator",
                    resource_brl=450.0,
                    deliverable="Relatório empírico de entrevistas (/interview) + 2 propostas comerciais enviadas",
                    validation_metric="Pelo menos 2 clientes dispostos a pagar pelo piloto de curadoria semântica",
                ),
                ExecutableTask(
                    task_id="task:w3_semantic_packaging",
                    week="Semana 3",
                    title="Integrar Pipeline Wordsmith -> Proterol para Entrega Automatizada do Piloto",
                    owner_module="Proterol & Wordsmith",
                    resource_brl=300.0,
                    deliverable="CLI automatizado que gera o relatório executivo + grafo de ativos do cliente",
                    validation_metric="Tempo de processamento de corpus de 500 páginas inferior a 5 minutos",
                ),
                ExecutableTask(
                    task_id="task:w4_review_and_reinvest",
                    week="Semana 4",
                    title="Auditoria de Resultados no Sovereign Budget e Decisão de Escala (Go/No-Go)",
                    owner_module="Planner & SovereignBudget",
                    resource_brl=200.0,
                    deliverable="Registro contábil Beancount do ROI do piloto e atualização do grafo no PixelCoin",
                    validation_metric="Receita realizada >= 2x custo do experimento mantendo Phi_buffer >= 1.20",
                ),
            ],
            go_no_go_criteria=[
                "GO para construção de SaaS completo apenas se >= 2 pilotos pagos forem concluídos na Semana 2-3",
                "NO-GO / PIVOT se o custo de aquisição ou customização manual superar 4 horas por cliente",
                "BLOQUEIO IMEDIATO se qualquer artefato listado no pacote possuir license_status == unclear_pending_audit",
            ],
            risk_mitigations=opp.key_risks,
        )

    def record_experiment_result(
        self,
        experiment_id: str,
        outcome_summary: str,
        realized_cost_brl: float,
        realized_revenue_brl: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Fluxo bidirecional: registra o resultado observado de um experimento,
        atualizando o estado do experimento, o fluxo de capital e o log de decisões.
        """
        if experiment_id not in self.experiments:
            raise KeyError(f"Experimento não encontrado: {experiment_id}")
        exp = self.experiments[experiment_id]
        exp.status = "completed"
        exp.recorded_outcome = outcome_summary
        exp.is_cost_estimate = False
        exp.cost_brl = realized_cost_brl

        # Atualiza a oportunidade vinculada com a nova evidência observada
        opp = self.opportunities.get(exp.related_opportunity_id)
        if opp:
            opp.committed_cost_brl = round(opp.committed_cost_brl + realized_cost_brl, 2)
            opp.realized_value_brl = round(opp.realized_value_brl + realized_revenue_brl, 2)
            for dim in opp.radial_dimensions:
                if dim.dimension_key in ("evidence", "commercial_readiness"):
                    dim.is_estimate = False
                    dim.score = min(100.0, round(dim.score + 8.0, 1))
                    dim.basis_explanation = f"[ATUALIZADO POR EXPERIMENTO {exp.code}] {outcome_summary}"

        record = {
            "event": "experiment_result_recorded",
            "experiment_id": experiment_id,
            "code": exp.code,
            "outcome_summary": outcome_summary,
            "realized_cost_brl": realized_cost_brl,
            "realized_revenue_brl": realized_revenue_brl,
        }
        self.decision_log.append(record)
        return record
