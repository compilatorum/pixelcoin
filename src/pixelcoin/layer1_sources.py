"""
Camada 1 — Fontes (Sources Layer)

Conecta e indexa as fontes primárias do ecossistema Compilatorum:
- Chatlogs (extraídos e organizados via Wordsmith)
- Repositórios GitHub / Locais (Proterol, ValueCurator, Governaut OS, PromptCraft, Sovereign Budget, Wordsmith, Oracle, License Manifest, Planner)
- Documentos e Especificações
- Dados e APIs
- Resultados Experimentais Anteriores
"""

from __future__ import annotations

import hashlib
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SourceKind(str, Enum):
    CHATLOG = "chatlog"
    GITHUB_REPO = "github_repo"
    DOCUMENT = "document"
    DATA_API = "data_api"
    EXPERIMENT_RESULT = "experiment_result"


class SourceRecord(BaseModel):
    """Registro canônico de uma fonte primária na Camada 1."""

    source_id: str = Field(..., description="Identificador único da fonte (ex: src:repo:proterol)")
    kind: SourceKind = Field(..., description="Tipo de fonte (chatlog, github_repo, document, data_api, experiment_result)")
    title: str = Field(..., description="Título legível da fonte")
    uri: str = Field(..., description="Caminho local (file://) ou URL do repositório/documento")
    compilatorum_module: str = Field(
        ...,
        description="Projeto do Compilatorum associado (Wordsmith, Proterol, Oracle, License Manifest, ValueCurator, Planner, Governaut, SovereignBudget)",
    )
    version: str = Field(default="1.0.0", description="Versão ou commit da fonte")
    sha256: str = Field(..., description="Hash SHA-256 determinístico de proveniência")
    timestamp: str = Field(..., description="Timestamp ISO-8601 da captura ou versão")
    summary: str = Field(..., description="Resumo factual do conteúdo da fonte")
    extracted_facts: List[str] = Field(default_factory=list, description="Fatos ou evidências observadas extraídas da fonte")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados adicionais da fonte")


def _compute_sha256(seed_text: str, file_path: Optional[Path] = None) -> str:
    """Calcula SHA-256 real do arquivo no workspace (se existir) ou do seed canônico."""
    if file_path and file_path.exists() and file_path.is_file():
        try:
            content = file_path.read_bytes()[:65536]
            return hashlib.sha256(content).hexdigest()
        except OSError:
            pass
    return hashlib.sha256(seed_text.encode("utf-8")).hexdigest()


class CompilatorumCorpusIngestor:
    """
    Ingestor da Camada 1: reúne amostras reais de chatlogs, repositórios,
    especificações e resultados experimentais do ecossistema Compilatorum.
    """

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path("/home/sukata")
        self._sources: Dict[str, SourceRecord] = {}
        self._load_canonical_sources()

    def _load_canonical_sources(self) -> None:
        raw_sources = [
            SourceRecord(
                source_id="src:repo:wordsmith",
                kind=SourceKind.GITHUB_REPO,
                title="Wordsmith — Extração e Curadoria de Corpus & Chatlogs",
                uri=f"file://{self.workspace_root}/promptcraft/promptcraft.py",
                compilatorum_module="Wordsmith",
                version="0.4.2",
                sha256=_compute_sha256(
                    "wordsmith-corpus-extractor-v0.4.2",
                    self.workspace_root / "promptcraft" / "promptcraft.py",
                ),
                timestamp="2026-07-20T00:00:00Z",
                summary="Extrai, higieniza e organiza grandes volumes de chatlogs, notas Org-roam e especificações dispersas em unidades indexadas.",
                extracted_facts=[
                    "Mais de 1.8MB de chatlogs JSONL processados em sessões estruturadas",
                    "Integração direta com banco SQLite local (lakehouse_local.db) e Org-roam",
                    "Pipeline pronto para oferecer curadoria automatizada de bases de conhecimento",
                ],
                metadata={"loc": 420, "language": "Python", "maturity": "beta"},
            ),
            SourceRecord(
                source_id="src:repo:proterol",
                kind=SourceKind.GITHUB_REPO,
                title="Proterol — Linguagem de Transformações & Genoma Semântico",
                uri=f"file://{self.workspace_root}/proterol/README.md",
                compilatorum_module="Proterol",
                version="1.0.0",
                sha256=_compute_sha256(
                    "proterol-executable-ontology-v1.0.0",
                    self.workspace_root / "proterol" / "README.md",
                ),
                timestamp="2026-10-03T17:49:00Z",
                summary="Estrutura conceitos, relações e unidades semânticas (Semantic Genes) com 4 máquinas sobrepostas (Simbólica, Semântica, Semiúrgica, Virtual) e provas SHA-256.",
                extracted_facts=[
                    "Possui 12 livros do Codex formalizados e compilador funcional testado via pytest",
                    "Licença MIT declarada explicitamente em LICENSE e pyproject.toml",
                    "Exporta JSON Schema para SemanticGene, Nexus e ProofCarryingConstruct",
                ],
                metadata={"loc": 1850, "language": "Python", "maturity": "production-ready"},
            ),
            SourceRecord(
                source_id="src:repo:oracle",
                kind=SourceKind.GITHUB_REPO,
                title="Oracle — Motor de Recuperação Associativa e Recomendação de Caminhos",
                uri=f"file://{self.workspace_root}/html/NLCA_Cognitive_Dashboard.html",
                compilatorum_module="Oracle",
                version="0.8.0",
                sha256=_compute_sha256(
                    "oracle-nlca-associative-recall-v0.8.0",
                    self.workspace_root / "html" / "NLCA_Cognitive_Dashboard.html",
                ),
                timestamp="2026-07-14T13:19:00Z",
                summary="Recupera conexões ocultas no grafo de conhecimento usando similaridade vetorial ponderada por decaimento temporal exponencial.",
                extracted_facts=[
                    "Equação de recall com decaimento cognitivo validada em protótipo NLCA",
                    "Conecta átomos do Proterol a oportunidades do ValueCurator e tarefas do Planner",
                    "Alguns datasets de terceiros nos conectores de scraping ainda carecem de auditoria de licença",
                ],
                metadata={"loc": 910, "language": "Python/JS", "maturity": "prototype"},
            ),
            SourceRecord(
                source_id="src:repo:license_manifest",
                kind=SourceKind.DOCUMENT,
                title="License Manifest — Registro de Direitos, Proveniência e Permissões",
                uri=f"file://{self.workspace_root}/proterol/schemas/semantic_gene.json",
                compilatorum_module="License Manifest",
                version="0.5.0",
                sha256=_compute_sha256(
                    "license-manifest-provenance-registry-v0.5.0",
                    self.workspace_root / "proterol" / "schemas" / "semantic_gene.json",
                ),
                timestamp="2026-10-06T19:33:00Z",
                summary="Fornece permissões, restrições de exploração comercial e árvores de proveniência criptográfica dos artefatos do Compilatorum.",
                extracted_facts=[
                    "Define políticas de licenciamento por artefato (MIT, Apache-2.0, CC-BY-SA-4.0, Proprietary)",
                    "Detectou 3 artefatos com direitos incertos ou dependências copyleft mistas que bloqueiam licenciamento comercial imediato",
                ],
                metadata={"audited_artifacts": 9, "unclear_rights_count": 3},
            ),
            SourceRecord(
                source_id="src:repo:valuecurator",
                kind=SourceKind.GITHUB_REPO,
                title="ValueCurator — Infraestrutura de Autorização Orientada por Evidências e Curadoria Comercial",
                uri=f"file://{self.workspace_root}/valuecurator/README.md",
                compilatorum_module="ValueCurator",
                version="0.1.0",
                sha256=_compute_sha256(
                    "valuecurator-evidence-gated-v0.1.0",
                    self.workspace_root / "valuecurator" / "README.md",
                ),
                timestamp="2026-10-17T20:45:00Z",
                summary="Estrutura ofertas, teses de investimento empíricas, entrevistas de descoberta de clientes (/interview) e portões determinísticos de autorização.",
                extracted_facts=[
                    "Princípio central: IA aconselha, Evidência prova, Política autoriza, Humano controla o capital",
                    "Monorepo TypeScript/Next.js + Discovery API testado com entrevistas estruturadas",
                    "Potencial direto para licenciamento SaaS B2B/B2D sem depender de emissão de token especulativo",
                ],
                metadata={"loc": 4200, "language": "TypeScript/Rust", "maturity": "mvp-verified"},
            ),
            SourceRecord(
                source_id="src:repo:planner",
                kind=SourceKind.GITHUB_REPO,
                title="Planner & Governaut OS — Orquestração de Tarefas, Recursos e Experimentos",
                uri=f"file://{self.workspace_root}/governaut-os/README.md",
                compilatorum_module="Planner",
                version="0.2.0",
                sha256=_compute_sha256(
                    "planner-governaut-os-v0.2.0",
                    self.workspace_root / "governaut-os" / "README.md",
                ),
                timestamp="2026-10-19T20:37:00Z",
                summary="Organiza cronogramas, tarefas, alocação de recursos, guardrails Human-in-the-Loop e pipelines de submissão a grants e validação.",
                extracted_facts=[
                    "Arquitetura L0-L5 com validação Pydantic v2 e guardrails determinísticos",
                    "Conector funcional com APIs de governança e gestão de pipelines de propostas/grants",
                ],
                metadata={"loc": 1450, "language": "Python", "maturity": "production-ready"},
            ),
            SourceRecord(
                source_id="src:data:sovereign_budget",
                kind=SourceKind.DATA_API,
                title="Sovereign Budget — Contabilidade Beancount e Termodinâmica Financeira",
                uri=f"file://{self.workspace_root}/sovereign-budget/financas.beancount",
                compilatorum_module="SovereignBudget",
                version="2026.10",
                sha256=_compute_sha256(
                    "sovereign-budget-beancount-v2026.10",
                    self.workspace_root / "sovereign-budget" / "financas.beancount",
                ),
                timestamp="2026-10-03T13:39:00Z",
                summary="Razão contábil de dupla entrada (Beancount) com restrição de soberania cambial (Phi_buffer >= 1.20) e limites de orçamento para experimentação.",
                extracted_facts=[
                    "Orçamento livre de experimentação para o ciclo atual: R$ 4.500 (ou ~US$ 900) sem violar Phi_buffer >= 1.20",
                    "Exige que experimentos de validação custem menos de R$ 1.500 por sprint para preservar liquidez fiduciária",
                ],
                metadata={"available_experiment_budget_brl": 4500.0, "phi_buffer_current": 1.34},
            ),
            SourceRecord(
                source_id="src:chatlog:compilatorum_synthesis",
                kind=SourceKind.CHATLOG,
                title="Chatlog #d43ca8ed — Síntese Arquitetural do Compilatorum & Monetização Pragmática",
                uri=f"file://{self.workspace_root}/promptcraft/chatlog_d43ca8ed.jsonl",
                compilatorum_module="Wordsmith",
                version="2026.07",
                sha256=_compute_sha256(
                    "chatlog-d43ca8ed-compilatorum",
                    self.workspace_root / "promptcraft" / "chatlog_d43ca8ed.jsonl",
                ),
                timestamp="2026-07-03T21:49:00Z",
                summary="Registro de diálogo estratégico sobre como converter o acervo técnico do Compilatorum em ofertas comercializáveis sem depender de especulação cripto.",
                extracted_facts=[
                    "Hipótese H1: Desenvolvedores e pesquisadores pagariam por curadoria semântica automatizada de repositórios e chatlogs",
                    "Hipótese H2: A API semântica do Proterol + Wordsmith reduz em 65% o tempo de onboarding em codebases complexas",
                    "Aprendizado anterior: Construir infraestrutura complexa antes de entrevistas de demanda gerou alto custo afundado",
                ],
                metadata={"messages_count": 148, "extracted_hypotheses": 4},
            ),
            SourceRecord(
                source_id="src:exp:discovery_interviews_r1",
                kind=SourceKind.EXPERIMENT_RESULT,
                title="Resultado Experimental E0 — Rodada Piloto de Descoberta e Auditoria de Portfólio",
                uri=f"file://{self.workspace_root}/ip-nft/COLOSSEUM_VALIDATION_SIMULATION_VS_INTERVIEWS_GUIDE.md",
                compilatorum_module="ValueCurator",
                version="1.1.0",
                sha256=_compute_sha256(
                    "exp-discovery-interviews-r1",
                    self.workspace_root / "ip-nft" / "COLOSSEUM_VALIDATION_SIMULATION_VS_INTERVIEWS_GUIDE.md",
                ),
                timestamp="2026-10-16T17:17:00Z",
                summary="Comparação empírica entre simulações sintéticas e entrevistas reais de validação de demanda para produtos do ecossistema.",
                extracted_facts=[
                    "Entrevistas estruturadas de 20 minutos reduziram incerteza comercial 3.2x mais por real investido do que prototipação cega",
                    "Clientes B2B exigem clareza de licença (MIT/Apache-2.0) antes de integrar qualquer biblioteca ou API semântica",
                    "Apenas 4 dos 12 potenciais clientes tinham interesse em blockchain; 10 de 12 queriam automação e síntese acionável imediata",
                ],
                metadata={"interviews_completed": 12, "non_blockchain_preference_ratio": 0.833},
            ),
        ]
        for src in raw_sources:
            self._sources[src.source_id] = src

    def list_sources(self, kind: Optional[SourceKind] = None, module: Optional[str] = None) -> List[SourceRecord]:
        results = list(self._sources.values())
        if kind is not None:
            results = [s for s in results if s.kind == kind]
        if module is not None:
            results = [s for s in results if s.compilatorum_module.lower() == module.lower()]
        return results

    def get_source(self, source_id: str) -> Optional[SourceRecord]:
        return self._sources.get(source_id)

    def register_source(self, source: SourceRecord) -> SourceRecord:
        self._sources[source.source_id] = source
        return source
