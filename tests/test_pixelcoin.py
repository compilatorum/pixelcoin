"""Suíte completa de testes das 6 camadas, 5 representações infoestéticas e 4 guardrails do PixelCoin."""

from __future__ import annotations

import pytest

from pixelcoin.cli import main as cli_main
from pixelcoin.layer1_sources import CompilatorumCorpusIngestor, SourceKind
from pixelcoin.layer2_graph import LicenseStatus, SemanticKnowledgeGraph
from pixelcoin.layer3_economics import EconomicIntelligenceEngine, ExperimentTag
from pixelcoin.layer4_orchestrator import CANONICAL_PROMPTS, PixelCoinOrchestrator
from pixelcoin.layer5_ui_spec import (
    DeclarativeActionSpec,
    MetricIndicator,
    PersonaPerspective,
    PixelCoinGuardrailError,
    VisualRepresentationType,
)
from pixelcoin.layer6_renderers import (
    AgentConversationalRenderer,
    EmacsOrgRenderer,
    MobileMicroRenderer,
    WebGenerativeRenderer,
)


def test_layer1_sources_and_provenance() -> None:
    ingestor = CompilatorumCorpusIngestor()
    sources = ingestor.list_sources()
    assert len(sources) >= 9

    modules = {s.compilatorum_module for s in sources}
    for expected_mod in ("Wordsmith", "Proterol", "Oracle", "License Manifest", "ValueCurator", "Planner", "SovereignBudget"):
        assert expected_mod in modules

    for src in sources:
        assert len(src.sha256) == 64
        assert src.uri.startswith("file://")
        assert len(src.extracted_facts) >= 1

    repos = ingestor.list_sources(kind=SourceKind.GITHUB_REPO)
    assert len(repos) >= 5


def test_layer2_semantic_graph_and_rights_resolution() -> None:
    graph = SemanticKnowledgeGraph()
    all_nodes = graph.list_artifacts()
    assert len(all_nodes) == 7

    no_chain = graph.list_artifacts(only_monetizable_no_blockchain=True)
    assert len(no_chain) == 7

    unclear = graph.list_artifacts(only_unclear_rights=True)
    assert len(unclear) == 3

    topo = graph.find_bottlenecks_and_dependencies()
    assert topo["total_nodes"] == 7
    assert topo["total_edges"] == 9
    assert len(topo["bottlenecks"]) == 3
    assert topo["top_reusable_hubs"][0]["artifact_id"] == "art:proterol_engine"

    # Testa fluxo bidirecional: esclarecer direitos remove gargalos
    updated = graph.resolve_artifact_rights(
        artifact_id="art:wordsmith_ingestor",
        new_spdx="MIT",
        audit_note="Clippings isolados do pacote comercial.",
        source_id="src:repo:license_manifest",
    )
    assert updated.license_status == LicenseStatus.PERMISSIVE_COMMERCIAL
    assert len(graph.list_artifacts(only_unclear_rights=True)) == 2
    assert len(graph.find_bottlenecks_and_dependencies()["bottlenecks"]) == 2


def test_layer3_economic_intelligence_and_experiment_efficiency() -> None:
    econ = EconomicIntelligenceEngine()
    ranked = econ.rank_experiments_by_efficiency(max_budget_brl=900.0)
    assert len(ranked) == 4

    # C (R$ 350, 38% -> 108.57 pts/R$1k) e A (R$ 450, 42% -> 93.33 pts/R$1k) cabem no orçamento de R$ 900
    assert ranked[0]["code"] == "C"
    assert ranked[0]["tag"] == ExperimentTag.PREPARAR.value
    assert ranked[0]["fits_in_budget"] is True

    assert ranked[1]["code"] == "A"
    assert ranked[1]["tag"] == ExperimentTag.TESTAR.value
    assert ranked[1]["fits_in_budget"] is True

    # B (R$ 1200) não cabe no orçamento enxuto de R$ 900
    exp_b = [r for r in ranked if r["code"] == "B"][0]
    assert exp_b["fits_in_budget"] is False

    # Verifica transparência das 6 dimensões do gráfico radial (estimativas vs observadas)
    opp_api = econ.opportunities["opp:api_semantica_proterol"]
    assert len(opp_api.radial_dimensions) == 6
    assert opp_api.estimated_dimensions_count == 2

    # Simulação respeita separação entre análise e execução
    sim = econ.simulate_allocation(budget_brl=850.0)
    assert sim["mode"] == "simulation_only"
    assert sim["financial_execution_performed"] is False
    assert sim["respects_sovereign_buffer"] is True
    assert sim["total_simulated_cost_brl"] == 800.0

    # Registro bidirecional de resultado de experimento
    rec = econ.record_experiment_result(
        experiment_id="exp:A_validar_demanda_curadoria",
        outcome_summary="2 clientes fecharam piloto de curadoria semântica.",
        realized_cost_brl=420.0,
        realized_revenue_brl=1200.0,
    )
    assert rec["code"] == "A"
    assert econ.experiments["exp:A_validar_demanda_curadoria"].status == "completed"
    assert econ.opportunities["opp:curadoria_corpus_b2b"].realized_value_brl == 2400.0


def test_layer4_orchestrator_canonical_prompts_and_perspectives() -> None:
    orch = PixelCoinOrchestrator()

    for item in CANONICAL_PROMPTS:
        spec = orch.generate_ui_spec(item["prompt"])
        assert spec.primary_representation.value == item["representation"]
        assert spec.semantic_compression.instant_view.headline_signal
        assert len(spec.semantic_compression.traceability.source_records) >= 9
        # Verifica que todas as 6 representações (incluindo Emblema Alquímico) estão disponíveis para alternância
        assert len(spec.available_representations) == 6
        for key in (
            "1_radial_profile",
            "2_knowledge_graph",
            "3_portfolio_mosaic",
            "4_decision_matrix",
            "5_capital_flow",
            "6_alchemical_emblem_and_lottie",
        ):
            assert key in spec.visual_payloads

    # Verifica adaptação por perspectiva (Executiva, Desenvolvedor, Científica)
    dev_spec = orch.generate_ui_spec("Encontre dependências entre meus repositórios.", perspective=PersonaPerspective.DEVELOPER)
    assert "[VISÃO DEV]" in dev_spec.semantic_compression.instant_view.headline_signal

    sci_spec = orch.generate_ui_spec("Explique a origem desta recomendação.", perspective=PersonaPerspective.SCIENTIFIC)
    assert "[VISÃO CIENTÍFICA]" in sci_spec.semantic_compression.instant_view.headline_signal


def test_layer5_guardrails_enforcement() -> None:
    # Regra 1: Dados antes da estética — proíbe métrica marcada como observada sem fonte
    with pytest.raises(PixelCoinGuardrailError, match="Dados antes da estética"):
        MetricIndicator(
            indicator_id="ind:fake",
            label="Métrica inventada sem fonte",
            value=999,
            is_estimate=False,
            source_refs=[],
            semantic_meaning="Inválido",
        )

    # Regra 3 e 4: Ações autorizadas e proibição de transferência autônoma / JS arbitrário
    with pytest.raises(PixelCoinGuardrailError, match="proibido"):
        DeclarativeActionSpec(
            action_id="act:bad",
            action_type="transfer_funds_autonomous",
            label="Transferir fundos sozinho",
            target_id="wallet",
        )

    with pytest.raises(PixelCoinGuardrailError, match="Ações autorizadas"):
        DeclarativeActionSpec(
            action_id="act:unknown",
            action_type="exec_shell_script",
            label="Ação não listada",
            target_id="sys",
        )


def test_layer6_all_four_renderers_and_cli(tmp_path) -> None:
    orch = PixelCoinOrchestrator()
    spec = orch.generate_ui_spec(
        "Tenho pouco orçamento para desenvolver o Compilatorum. Compare minhas opções e encontre a ação que mais reduz incerteza por unidade de recurso."
    )

    # 1. Web / Navegador (Sovereign Mockup Protocol compliant)
    html = WebGenerativeRenderer.render_html(spec)
    assert "<!DOCTYPE html>" in html
    assert "safeChart(" in html
    assert "chartDecisionMatrix" in html
    assert "chartRadialProfile" in html
    assert "chartCapitalFlow" in html
    assert "=>" not in html  # Zero arrow functions

    # 2. Emacs / Org-mode
    org_text = EmacsOrgRenderer.render(spec)
    assert "#+TITLE: PixelCoin" in org_text
    assert "* 1. Compressão Semântica (3 Níveis)" in org_text
    assert "** TESTAR [A] A. Validar demanda por curadoria" in org_text
    assert "** VALIDAR [B] B. Construir uma API semântica" in org_text
    assert "** PREPARAR [C] C. Automatizar o registro de licenças" in org_text

    # 3. Mobile / Microinterface
    mobile_payload = MobileMicroRenderer.render(spec)
    assert mobile_payload["surface"] == "mobile_microinterface"
    assert len(mobile_payload["pending_decisions"]) == 3

    # 4. Agentes / Interfaces Conversacionais
    agent_payload = AgentConversationalRenderer.render(spec)
    assert agent_payload["@type"] == "PixelCoinSemanticInterface"
    assert agent_payload["access_policy"]["autonomous_capital_transfer"] is False

    # Testa CLI escrevendo artefatos Web e Org
    out_org = tmp_path / "relatorio.org"
    out_html = tmp_path / "dashboard.html"
    assert cli_main(["render", "--surface", "org", "--output", str(out_org)]) == 0
    assert cli_main(["render", "--surface", "web", "--output", str(out_html)]) == 0
    assert out_org.exists()
    assert out_html.exists()


def test_sea_of_information_puxers_and_alchemical_emblem() -> None:
    from pixelcoin.alchemical_infoaesthetics import AlchemicalElement, SeaOfInformationCurator

    curator = SeaOfInformationCurator()
    streams = curator.curate_investment_streams({})
    assert len(streams) == 5

    emblem = curator.compile_alchemical_emblem(
        target_id="compilatorum_portfolio_nexus",
        realized_brl=3700.0,
        committed_brl=2100.0,
        uncertainty_reduction_pct=80.0,
        synergy_nodes_score=62.0,
        phi_buffer_ratio=1.34,
    )
    # 3700/250=15 Terra + 2100/250=8 Aqua + 80/5=16 Ignis + 62/5=12 Aer = 51 Puxers
    assert len(emblem.puxers) == 51
    assert any(p.element == AlchemicalElement.TERRA for p in emblem.puxers)
    assert any(p.element == AlchemicalElement.AQUA for p in emblem.puxers)
    assert any(p.element == AlchemicalElement.IGNIS for p in emblem.puxers)
    assert any(p.element == AlchemicalElement.AER for p in emblem.puxers)
    assert 0.70 <= emblem.resonance.resonance_index <= 1.0
    assert "<svg" in emblem.svg_vector_markup
    assert "R_LE=" in emblem.svg_vector_markup
    assert len(emblem.provenance_seal_sha256) == 64


def test_lottiemcp_and_creatormcp_parameterization(tmp_path) -> None:
    from pixelcoin.mcp_server import PixelCoinMCPBridge

    bridge = PixelCoinMCPBridge()
    tools = bridge.list_tools()
    tool_names = {t["name"] for t in tools}
    assert "creator_curate_investment_sea" in tool_names
    assert "creator_compile_alchemical_emblem" in tool_names
    assert "lottie_list_templates" in tool_names
    assert "lottie_parameterize_template" in tool_names
    assert "lottie_patch_infographic" in tool_names

    templates_list = bridge.call_tool("lottie_list_templates", {})["templates"]
    assert len(templates_list) == 6

    # Parametriza o template alchemical_emblem com novos quantitativos JSON
    param_res = bridge.call_tool(
        "lottie_parameterize_template",
        {
            "template_id": "alchemical_emblem",
            "params_json": {
                "realized_brl": 5000.0,
                "committed_brl": 2500.0,
                "uncertainty_reduction_pct": 90.0,
                "synergy_score": 75.0,
                "resonance_index": 0.92,
                "pulse_frequency_hz": 1.6,
            },
        },
    )
    assert param_res["lottie_json"]["v"] == "5.9.0"
    assert len(param_res["lottie_json"]["layers"]) == 3
    assert param_res["lottie_json"]["meta"]["puxer_metrics"]["terra_realized_brl"] == 5000.0

    # Aplica um patch JSON incremental sobre o infográfico Lottie
    patched = bridge.call_tool(
        "lottie_patch_infographic",
        {
            "existing_bundle": param_res,
            "patch_json": {"realized_brl": 6250.0, "resonance_index": 0.95},
        },
    )
    assert patched["lottie_json"]["meta"]["puxer_metrics"]["terra_realized_brl"] == 6250.0

    # Testa exportação completa de Lotties e SVG via CLI
    lottie_dir = tmp_path / "lottie_out"
    assert cli_main(["lottie", "--export-dir", str(lottie_dir)]) == 0
    assert (lottie_dir / "alchemical_emblem.svg").exists()
    assert (lottie_dir / "alchemical_emblem.lottie.json").exists()
    assert (lottie_dir / "decision_matrix.lottie.json").exists()
