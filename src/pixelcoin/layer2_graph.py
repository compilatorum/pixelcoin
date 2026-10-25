"""
Camada 2 — Grafo Semântico e Registro de Artefatos

Gerencia:
- Identidade canônica e versões dos artefatos do Compilatorum
- Relações e sinergias (dependências técnicas, reutilização, fluxo semântico, bloqueios)
- Evidências empíricas vs. estimativas
- Proveniência criptográfica (links para Camada 1 + SHA-256)
- Direitos e licenças (integração com License Manifest)
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from pixelcoin.layer1_sources import CompilatorumCorpusIngestor


class LicenseStatus(str, Enum):
    PERMISSIVE_COMMERCIAL = "permissive_commercial"  # MIT / Apache-2.0 — pronto p/ licenciar ou SaaS
    SHAREALIKE_CONDITIONAL = "sharealike_conditional"  # CC-BY-SA-4.0 — exige atribuição/compartilhamento
    UNCLEAR_PENDING_AUDIT = "unclear_pending_audit"  # Direitos incertos — requer auditoria antes de comercializar
    PROPRIETARY_INTERNAL = "proprietary_internal"  # Uso interno / segredo comercial


class ArtifactCategory(str, Enum):
    REPOSITORY = "repository"
    REUSABLE_COMPONENT = "reusable_component"
    MICRO_SAAS_API = "micro_saas_api"
    KNOWLEDGE_CORPUS = "knowledge_corpus"
    GOVERNANCE_ENGINE = "governance_engine"
    FINANCIAL_LEDGER = "financial_ledger"


class EvidenceItem(BaseModel):
    """Evidência rastreável vinculada a um artefato ou dimensão."""

    evidence_id: str
    description: str
    source_id: str
    is_observed: bool = Field(
        default=True,
        description="True se for evidência empírica observada; False se for hipótese/estimativa sem evidência direta",
    )
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class ArtifactNode(BaseModel):
    """Nó do grafo semântico representando um ativo intelectual ou técnico do Compilatorum."""

    artifact_id: str = Field(..., description="ID canônico (ex: art:proterol_compiler)")
    name: str
    compilatorum_project: str = Field(
        ...,
        description="Wordsmith, Proterol, Oracle, License Manifest, ValueCurator, Planner, SovereignBudget",
    )
    category: ArtifactCategory
    version: str = "1.0.0"
    license_spdx: str = Field(..., description="Identificador SPDX ou status (MIT, Apache-2.0, CC-BY-SA-4.0, UNCLEAR)")
    license_status: LicenseStatus
    rights_notes: str = Field(..., description="Explicação clara sobre permissões, restrições e pendências de direitos")
    monetizable_without_blockchain: bool = Field(
        default=True,
        description="Se o ativo pode ser monetizado via SaaS, API, consultoria, grant ou licenciamento tradicional sem token",
    )
    monetization_models: List[str] = Field(
        default_factory=list,
        description="Modelos aplicáveis: Micro-SaaS, API Semântica, Licenciamento Dual, Grant Científico, Consultoria B2B",
    )
    reusability_score: float = Field(..., ge=0.0, le=10.0, description="Índice de reutilização entre projetos (0 a 10)")
    source_ids: List[str] = Field(default_factory=list, description="IDs das fontes na Camada 1")
    evidences: List[EvidenceItem] = Field(default_factory=list)
    summary: str


class RelationType(str, Enum):
    EXTRACTS_TO = "extracts_to"
    STRUCTURES_INTO = "structures_into"
    RECOMMENDS_PATH = "recommends_path"
    AUDITS_RIGHTS_OF = "audits_rights_of"
    CURATES_VALUE_FOR = "curates_value_for"
    ORCHESTRATES_TASKS = "orchestrates_tasks"
    DEPENDS_ON = "depends_on"
    REUSES_COMPONENT = "reuses_component"


class SemanticEdge(BaseModel):
    """Aresta direcionada no grafo semântico do Compilatorum."""

    edge_id: str
    source_artifact_id: str
    target_artifact_id: str
    relation: RelationType
    label: str
    weight: float = Field(default=1.0, ge=0.1, le=5.0)
    is_bottleneck: bool = Field(default=False, description="True se esta dependência é um gargalo técnico ou jurídico")


class SemanticKnowledgeGraph:
    """
    Camada 2: Grafo semântico e registro de artefatos do Compilatorum.
    Conecta Wordsmith, Proterol, Oracle, License Manifest, ValueCurator, Planner e SovereignBudget.
    """

    def __init__(self, ingestor: Optional[CompilatorumCorpusIngestor] = None) -> None:
        self.ingestor = ingestor or CompilatorumCorpusIngestor()
        self.nodes: Dict[str, ArtifactNode] = {}
        self.edges: List[SemanticEdge] = []
        self._build_initial_graph()

    def _build_initial_graph(self) -> None:
        artifacts = [
            ArtifactNode(
                artifact_id="art:wordsmith_ingestor",
                name="Wordsmith Corpus & Chatlog Extractor",
                compilatorum_project="Wordsmith",
                category=ArtifactCategory.KNOWLEDGE_CORPUS,
                version="0.4.2",
                license_spdx="MIT (+ trechos de corpus UNCLEAR)",
                license_status=LicenseStatus.UNCLEAR_PENDING_AUDIT,
                rights_notes="Código-fonte do extrator é MIT, mas parte dos chatlogs brutos e clippings de terceiros na pasta takeout não possuem manifesto de cessão de direitos.",
                monetizable_without_blockchain=True,
                monetization_models=["Serviço de Curadoria de Conhecimento", "Pipeline CLI Licenciado"],
                reusability_score=8.8,
                source_ids=["src:repo:wordsmith", "src:chatlog:compilatorum_synthesis"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:ws:1",
                        description="Processou 1.87MB de chatlogs reais e integrou com SQLite lakehouse_local.db.",
                        source_id="src:repo:wordsmith",
                        is_observed=True,
                        confidence=0.95,
                    ),
                    EvidenceItem(
                        evidence_id="ev:ws:2",
                        description="Demanda por higienização de dados para RAG empresarial estimada a partir de entrevistas preliminares.",
                        source_id="src:exp:discovery_interviews_r1",
                        is_observed=True,
                        confidence=0.82,
                    ),
                ],
                summary="Extrai, limpa e organiza conteúdo de milhares de páginas de chatlogs, Org-roam e documentos técnicos.",
            ),
            ArtifactNode(
                artifact_id="art:proterol_engine",
                name="Proterol Semantic Compiler & Gene Engine",
                compilatorum_project="Proterol",
                category=ArtifactCategory.MICRO_SAAS_API,
                version="1.0.0",
                license_spdx="MIT",
                license_status=LicenseStatus.PERMISSIVE_COMMERCIAL,
                rights_notes="100% autoral com licença MIT explícita em pyproject.toml e LICENSE. Pronto para licenciamento comercial, SDK ou API SaaS.",
                monetizable_without_blockchain=True,
                monetization_models=["API Semântica B2B", "SDK de Ontologia Executável", "Grant de Pesquisa em IA Neuro-Simbólica"],
                reusability_score=9.6,
                source_ids=["src:repo:proterol", "src:chatlog:compilatorum_synthesis"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:pr:1",
                        description="4 máquinas semânticas (Simbólica, Semântica, Semiúrgica, Virtual) implementadas e cobertas por testes automatizados.",
                        source_id="src:repo:proterol",
                        is_observed=True,
                        confidence=0.98,
                    ),
                    EvidenceItem(
                        evidence_id="ev:pr:2",
                        description="Estimativa de redução de 65% no tempo de estruturação ontológica de repositórios (ainda requer benchmark externo).",
                        source_id="src:chatlog:compilatorum_synthesis",
                        is_observed=False,
                        confidence=0.60,
                    ),
                ],
                summary="Estrutura conceitos, relações e unidades semânticas (Semantic Genes) com provas determinísticas SHA-256.",
            ),
            ArtifactNode(
                artifact_id="art:oracle_associative",
                name="Oracle Associative Graph & Recall Engine",
                compilatorum_project="Oracle",
                category=ArtifactCategory.REUSABLE_COMPONENT,
                version="0.8.0",
                license_spdx="UNCLEAR (Mix MIT + Scrapers GPL/Third-Party)",
                license_status=LicenseStatus.UNCLEAR_PENDING_AUDIT,
                rights_notes="O motor matemático de recall é autoral, mas conectores de indexação herdam scripts sem SPDX definido e caches de terceiros.",
                monetizable_without_blockchain=True,
                monetization_models=["Motor de Recomendação Semântica", "Plugin para IDEs/Emacs"],
                reusability_score=8.4,
                source_ids=["src:repo:oracle", "src:repo:license_manifest"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:or:1",
                        description="Fórmula de recall ponderada por decaimento exponencial validada em painel NLCA.",
                        source_id="src:repo:oracle",
                        is_observed=True,
                        confidence=0.88,
                    ),
                    EvidenceItem(
                        evidence_id="ev:or:2",
                        description="Auditoria preliminar apontou dependência de adaptadores sem licença clara.",
                        source_id="src:repo:license_manifest",
                        is_observed=True,
                        confidence=0.90,
                    ),
                ],
                summary="Recupera conexões ocultas entre repositórios e recomenda caminhos de reutilização e síntese.",
            ),
            ArtifactNode(
                artifact_id="art:license_manifest",
                name="License Manifest & Provenance Registry",
                compilatorum_project="License Manifest",
                category=ArtifactCategory.GOVERNANCE_ENGINE,
                version="0.5.0",
                license_spdx="Apache-2.0",
                license_status=LicenseStatus.PERMISSIVE_COMMERCIAL,
                rights_notes="Direitos 100% claros sob Apache-2.0. Atua como validador jurídico-técnico para todos os demais artefatos.",
                monetizable_without_blockchain=True,
                monetization_models=["Auditoria Automatizada de IP/Compliance para IA", "Micro-SaaS de Proveniência de Código"],
                reusability_score=9.1,
                source_ids=["src:repo:license_manifest", "src:exp:discovery_interviews_r1"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:lm:1",
                        description="Schemas JSON de proveniência e licença já operam integrados aos Semantic Genes do Proterol.",
                        source_id="src:repo:license_manifest",
                        is_observed=True,
                        confidence=0.92,
                    ),
                ],
                summary="Fornece permissões, restrições e árvores de proveniência para destravar licenciamento comercial seguro.",
            ),
            ArtifactNode(
                artifact_id="art:valuecurator_core",
                name="ValueCurator Discovery & Evidence Gate",
                compilatorum_project="ValueCurator",
                category=ArtifactCategory.MICRO_SAAS_API,
                version="0.1.0",
                license_spdx="Apache-2.0",
                license_status=LicenseStatus.PERMISSIVE_COMMERCIAL,
                rights_notes="Monorepo com contratos tipados e entrevistas de discovery sob Apache-2.0; módulo on-chain é totalmente opcional e desacoplado.",
                monetizable_without_blockchain=True,
                monetization_models=["Micro-SaaS de Customer Discovery Assistido por IA", "Motor de Aprovação de Alocação Baseado em Evidências"],
                reusability_score=9.3,
                source_ids=["src:repo:valuecurator", "src:exp:discovery_interviews_r1"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:vc:1",
                        description="Módulo /interview e API de evidências testados com persistência PGlite/Postgres.",
                        source_id="src:repo:valuecurator",
                        is_observed=True,
                        confidence=0.95,
                    ),
                    EvidenceItem(
                        evidence_id="ev:vc:2",
                        description="10 de 12 entrevistados na rodada E0 preferiram usar o fluxo de evidências e curadoria sem precisar de carteira cripto.",
                        source_id="src:exp:discovery_interviews_r1",
                        is_observed=True,
                        confidence=0.91,
                    ),
                ],
                summary="Estrutura ofertas comerciais, executa entrevistas de validação de demanda e exige evidências antes de autorizar recursos.",
            ),
            ArtifactNode(
                artifact_id="art:planner_governaut",
                name="Planner & Governaut Pipeline Orchestrator",
                compilatorum_project="Planner",
                category=ArtifactCategory.GOVERNANCE_ENGINE,
                version="0.2.0",
                license_spdx="MIT",
                license_status=LicenseStatus.PERMISSIVE_COMMERCIAL,
                rights_notes="Licença MIT limpa. Arquitetura L0-L5 com guardrails Human-in-the-Loop pronta para empacotamento comercial ou grants.",
                monetizable_without_blockchain=True,
                monetization_models=["Copiloto de Submissão a Grants & Editais", "Orquestrador de Experimentos e OKRs Técnicos"],
                reusability_score=8.9,
                source_ids=["src:repo:planner"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:pl:1",
                        description="17 agentes de domínio + guardrails determinísticos testados em suíte pytest.",
                        source_id="src:repo:planner",
                        is_observed=True,
                        confidence=0.96,
                    ),
                ],
                summary="Organiza tarefas, cronogramas, alocação de recursos, propostas de grants e experimentos controlados.",
            ),
            ArtifactNode(
                artifact_id="art:sovereign_budget_thermo",
                name="Sovereign Budget — Motor de Restrição Orçamentária (Beancount)",
                compilatorum_project="SovereignBudget",
                category=ArtifactCategory.FINANCIAL_LEDGER,
                version="2026.10",
                license_spdx="UNCLEAR (Scripts MIT + Dados Pessoais Confidenciais)",
                license_status=LicenseStatus.UNCLEAR_PENDING_AUDIT,
                rights_notes="Os extratores OFX/Beancount podem ser licenciados sob MIT, mas os arquivos .beancount contêm dados financeiros pessoais que exigem sanitização estrita.",
                monetizable_without_blockchain=True,
                monetization_models=["Template & CLI de Contabilidade Soberana em Texto Puro (Beancount)"],
                reusability_score=7.8,
                source_ids=["src:data:sovereign_budget"],
                evidences=[
                    EvidenceItem(
                        evidence_id="ev:sb:1",
                        description="Inequação Phi_buffer >= 1.20 protege a reserva fiduciária e define o teto de R$ 4.500 para experimentos.",
                        source_id="src:data:sovereign_budget",
                        is_observed=True,
                        confidence=0.99,
                    ),
                ],
                summary="Fornece limites reais de caixa, restrições de liquidez e contabilidade de custos para alimentar decisões no PixelCoin.",
            ),
        ]

        for node in artifacts:
            self.nodes[node.artifact_id] = node

        self.edges = [
            SemanticEdge(
                edge_id="edge:ws_to_proterol",
                source_artifact_id="art:wordsmith_ingestor",
                target_artifact_id="art:proterol_engine",
                relation=RelationType.EXTRACTS_TO,
                label="Wordsmith extrai átomos brutos do corpus para compilação no Proterol",
                weight=3.5,
                is_bottleneck=False,
            ),
            SemanticEdge(
                edge_id="edge:proterol_to_oracle",
                source_artifact_id="art:proterol_engine",
                target_artifact_id="art:oracle_associative",
                relation=RelationType.STRUCTURES_INTO,
                label="Proterol fornece Semantic Genes tipados para indexação associativa no Oracle",
                weight=4.0,
                is_bottleneck=False,
            ),
            SemanticEdge(
                edge_id="edge:oracle_to_valuecurator",
                source_artifact_id="art:oracle_associative",
                target_artifact_id="art:valuecurator_core",
                relation=RelationType.RECOMMENDS_PATH,
                label="Oracle recupera sinergias técnicas e sugere oportunidades para o ValueCurator",
                weight=3.2,
                is_bottleneck=True,  # Gargalo porque Oracle tem direitos incertos que afetam pacotes integrados
            ),
            SemanticEdge(
                edge_id="edge:license_to_wordsmith",
                source_artifact_id="art:license_manifest",
                target_artifact_id="art:wordsmith_ingestor",
                relation=RelationType.AUDITS_RIGHTS_OF,
                label="License Manifest audita proveniência dos chatlogs e textos extraídos pelo Wordsmith",
                weight=4.5,
                is_bottleneck=True,
            ),
            SemanticEdge(
                edge_id="edge:license_to_oracle",
                source_artifact_id="art:license_manifest",
                target_artifact_id="art:oracle_associative",
                relation=RelationType.AUDITS_RIGHTS_OF,
                label="License Manifest bloqueia distribuição comercial do Oracle até limpeza de scrapers sem SPDX",
                weight=4.2,
                is_bottleneck=True,
            ),
            SemanticEdge(
                edge_id="edge:license_to_proterol",
                source_artifact_id="art:license_manifest",
                target_artifact_id="art:proterol_engine",
                relation=RelationType.AUDITS_RIGHTS_OF,
                label="License Manifest atesta licença MIT limpa do Proterol para API e SDK",
                weight=3.8,
                is_bottleneck=False,
            ),
            SemanticEdge(
                edge_id="edge:valuecurator_to_planner",
                source_artifact_id="art:valuecurator_core",
                target_artifact_id="art:planner_governaut",
                relation=RelationType.CURATES_VALUE_FOR,
                label="ValueCurator entrega oportunidades validadas para execução de tarefas no Planner",
                weight=4.1,
                is_bottleneck=False,
            ),
            SemanticEdge(
                edge_id="edge:budget_to_planner",
                source_artifact_id="art:sovereign_budget_thermo",
                target_artifact_id="art:planner_governaut",
                relation=RelationType.DEPENDS_ON,
                label="Sovereign Budget impõe teto fiduciário (Phi_buffer >= 1.20) aos experimentos do Planner",
                weight=4.8,
                is_bottleneck=False,
            ),
            SemanticEdge(
                edge_id="edge:proterol_reused_by_valuecurator",
                source_artifact_id="art:proterol_engine",
                target_artifact_id="art:valuecurator_core",
                relation=RelationType.REUSES_COMPONENT,
                label="ValueCurator reutiliza schemas de prova e proveniência SHA-256 do Proterol",
                weight=3.9,
                is_bottleneck=False,
            ),
        ]

    def list_artifacts(
        self,
        only_monetizable_no_blockchain: bool = False,
        only_unclear_rights: bool = False,
    ) -> List[ArtifactNode]:
        items = list(self.nodes.values())
        if only_monetizable_no_blockchain:
            items = [a for a in items if a.monetizable_without_blockchain]
        if only_unclear_rights:
            items = [a for a in items if a.license_status == LicenseStatus.UNCLEAR_PENDING_AUDIT]
        return items

    def get_artifact(self, artifact_id: str) -> Optional[ArtifactNode]:
        return self.nodes.get(artifact_id)

    def find_bottlenecks_and_dependencies(self) -> Dict[str, Any]:
        """Analisa dependências, componentes mais reutilizados e gargalos no grafo."""
        in_degree: Dict[str, int] = {aid: 0 for aid in self.nodes}
        out_degree: Dict[str, int] = {aid: 0 for aid in self.nodes}
        bottleneck_edges: List[SemanticEdge] = []

        for edge in self.edges:
            out_degree[edge.source_artifact_id] = out_degree.get(edge.source_artifact_id, 0) + 1
            in_degree[edge.target_artifact_id] = in_degree.get(edge.target_artifact_id, 0) + 1
            if edge.is_bottleneck:
                bottleneck_edges.append(edge)

        hubs = sorted(
            self.nodes.values(),
            key=lambda n: (out_degree.get(n.artifact_id, 0) + in_degree.get(n.artifact_id, 0), n.reusability_score),
            reverse=True,
        )
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "top_reusable_hubs": [
                {
                    "artifact_id": h.artifact_id,
                    "name": h.name,
                    "project": h.compilatorum_project,
                    "reusability_score": h.reusability_score,
                    "connections": out_degree.get(h.artifact_id, 0) + in_degree.get(h.artifact_id, 0),
                    "license_status": h.license_status.value,
                }
                for h in hubs[:4]
            ],
            "bottlenecks": [
                {
                    "edge_id": e.edge_id,
                    "from": e.source_artifact_id,
                    "to": e.target_artifact_id,
                    "label": e.label,
                }
                for e in bottleneck_edges
            ],
        }

    def resolve_artifact_rights(self, artifact_id: str, new_spdx: str, audit_note: str, source_id: str) -> ArtifactNode:
        """
        Fluxo bidirecional: atualiza o status de direitos de um artefato após
        execução de auditoria do License Manifest e remove gargalos associados.
        """
        if artifact_id not in self.nodes:
            raise KeyError(f"Artefato não encontrado: {artifact_id}")
        node = self.nodes[artifact_id]
        node.license_spdx = new_spdx
        node.license_status = LicenseStatus.PERMISSIVE_COMMERCIAL
        node.rights_notes = f"[AUDITADO] {audit_note}"
        node.evidences.append(
            EvidenceItem(
                evidence_id=f"ev:audit:{len(node.evidences) + 1}",
                description=f"Auditoria de direitos concluída ({new_spdx}): {audit_note}",
                source_id=source_id,
                is_observed=True,
                confidence=0.99,
            )
        )
        for edge in self.edges:
            if edge.target_artifact_id == artifact_id and edge.relation == RelationType.AUDITS_RIGHTS_OF:
                edge.is_bottleneck = False
        return node
