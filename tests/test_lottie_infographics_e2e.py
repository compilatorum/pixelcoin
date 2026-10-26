"""
Suíte End-to-End de Testes de Infográficos Lottie + SVG Vetorial sobre o Projeto PixelCoin.

Exercita todas as capacidades do ecossistema PixelCoin:
1. Protocolo JSON-RPC 2.0 via `stdio` no servidor `LottieMCP` / `CreatorMCP` (`pixelcoin.mcp_server`).
2. Curadoria do "mar de informações" (`creator_curate_investment_sea`) + Matriz de Puxers Quantitativos
   (🜃 Terra, 🜄 Aqua, 🜂 Ignis, 🜁 Aer) + Ressonância Lógico-Estética (R_LE).
3. Compilação de Emblemas Alquímicos (`creator_compile_alchemical_emblem`: Inscriptio, Pictura SVG + Lottie, Subscriptio).
4. Parametrização dinâmica (`lottie_parameterize_template`) dos 6 templates de infográficos sobre o próprio
   projeto PixelCoin (`alchemical_emblem`, `radial_profile`, `knowledge_graph`, `portfolio_mosaic`,
   `decision_matrix`, `capital_flow`), validando tanto o JSON Bodymovin v5.9.0 quanto o `svg_vector`.
5. Ciclo de vida completo com mutação de estado nas Camadas 2 e 3 (`resolve_artifact_rights` +
   `record_experiment_result`) seguido de patch incremental (`lottie_patch_infographic`) e verificação
   das mudanças nos keyframes Lottie, raios, escalas e SVGs.
6. Integração com envelopes `GenUI-MD` multi-janela e exportação de artefatos em `dist/lottie/`.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from pixelcoin.genui_md import GenUIMDAdapter, GenUIMDParser, GenUIWorkspaceRuntime
from pixelcoin.layer4_orchestrator import CANONICAL_PROMPTS, PixelCoinOrchestrator
from pixelcoin.lottie_templates import LottieTemplateRegistry
from pixelcoin.mcp_server import PixelCoinMCPBridge


def test_stdio_mcp_jsonrpc_full_protocol() -> None:
    """Testa o servidor LottieMCP / CreatorMCP real via subprocesso JSON-RPC 2.0 stdio."""
    requests: List[Dict[str, Any]] = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "creator_curate_investment_sea",
                "arguments": {
                    "realized_brl": 4500.0,
                    "committed_brl": 2100.0,
                    "uncertainty_reduction_pct": 85.0,
                    "synergy_nodes_score": 74.0,
                    "phi_buffer_ratio": 1.38,
                },
            },
        },
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "lottie_parameterize_template",
                "arguments": {
                    "template_id": "radial_profile",
                    "params_json": {
                        "target_label": "PixelCoin Generative UI v0.5",
                        "axes": {
                            "evidencia": 88.0,
                            "utilidade": 94.0,
                            "viabilidade": 90.0,
                            "risco_invertido": 82.0,
                            "clareza_direitos": 100.0,
                            "prontidao_comercial": 86.0,
                        },
                        "composite_score": 90.0,
                    },
                },
            },
        },
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "lottie_generate_project_infographics_suite",
                "arguments": {
                    "simulate_lifecycle_mutation": True,
                    "budget_limit_brl": 1500.0,
                },
            },
        },
    ]

    import os

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    stdin_payload = "\n".join(json.dumps(req) for req in requests) + "\n"
    proc = subprocess.run(
        [sys.executable, "-m", "pixelcoin.mcp_server"],
        input=stdin_payload,
        text=True,
        capture_output=True,
        check=True,
        timeout=15,
        env=env,
    )

    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert len(lines) == 5

    # 1. initialize
    resp_init = json.loads(lines[0])
    assert resp_init["id"] == 1
    assert resp_init["result"]["serverInfo"]["name"] == "pixelcoin-lottie-creator-mcp"

    # 2. tools/list
    resp_tools = json.loads(lines[1])
    tool_names = {t["name"] for t in resp_tools["result"]["tools"]}
    assert {
        "creator_curate_investment_sea",
        "creator_compile_alchemical_emblem",
        "lottie_list_templates",
        "lottie_parameterize_template",
        "lottie_patch_infographic",
        "lottie_generate_project_infographics_suite",
    }.issubset(tool_names)

    # 3. creator_curate_investment_sea
    resp_curate = json.loads(lines[2])
    curate_data = json.loads(resp_curate["result"]["content"][0]["text"])
    assert curate_data["puxers_count"] > 20
    assert curate_data["logico_aesthetic_resonance"]["resonance_index"] >= 0.70

    # 4. lottie_parameterize_template (radial_profile)
    resp_radial = json.loads(lines[3])
    radial_bundle = json.loads(resp_radial["result"]["content"][0]["text"])
    assert radial_bundle["template_id"] == "radial_profile"
    assert radial_bundle["lottie_json"]["v"] == "5.9.0"
    assert "<svg" in radial_bundle["svg_vector"]
    assert "PixelCoin Generative UI v0.5" in radial_bundle["svg_vector"]

    # 5. lottie_generate_project_infographics_suite
    resp_suite = json.loads(lines[4])
    suite_data = json.loads(resp_suite["result"]["content"][0]["text"])
    assert suite_data["project"] == "compilatorum/pixelcoin"
    assert len(suite_data["baseline_infographics"]) == 6
    assert len(suite_data["mutated_infographics"]) == 6
    assert len(suite_data["lifecycle_events"]) == 4


def test_all_six_lottie_and_svg_infographics_for_pixelcoin_project() -> None:
    """Verifica a geração e parametrização dos 6 templates Lottie + SVG com dados reais do projeto PixelCoin."""
    bridge = PixelCoinMCPBridge()
    suite = bridge.call_tool(
        "lottie_generate_project_infographics_suite",
        {"simulate_lifecycle_mutation": True, "budget_limit_brl": 1500.0},
    )

    expected_templates = [
        "alchemical_emblem",
        "radial_profile",
        "knowledge_graph",
        "portfolio_mosaic",
        "decision_matrix",
        "capital_flow",
    ]

    for tid in expected_templates:
        base_bundle = suite["baseline_infographics"][tid]
        mut_bundle = suite["mutated_infographics"][tid]

        # Valida estrutura Bodymovin v5.9.0
        for bundle in (base_bundle, mut_bundle):
            lottie = bundle["lottie_json"]
            assert lottie["v"] == "5.9.0"
            assert lottie["fr"] == 60
            assert lottie["ip"] == 0
            assert lottie["op"] > 0
            assert len(lottie["layers"]) >= 2
            assert "svg_vector" in bundle
            assert bundle["svg_vector"].startswith("<svg")
            assert bundle["svg_vector"].endswith("</svg>")
            assert bundle["parameterization_receipt"]["status"] == "parameterized_ok"

    # Verifica mutações específicas entre o Baseline e o Pós-Experimento/Auditoria SPDX:
    # 1. Alchemical Emblem: Terra (Realizado BRL) subiu de 3700 para 6500 após o Experimento A
    base_emblem_params = suite["baseline_infographics"]["alchemical_emblem"]["parameterization_receipt"]["applied_params"]
    mut_emblem_params = suite["mutated_infographics"]["alchemical_emblem"]["parameterization_receipt"]["applied_params"]
    assert mut_emblem_params["realized_brl"] > base_emblem_params["realized_brl"]
    assert mut_emblem_params["realized_brl"] == 6500.0
    assert "6500" in suite["mutated_infographics"]["alchemical_emblem"]["svg_vector"]

    # 2. Knowledge Graph: Gargalos de direitos caíram de 3 para 0 após resolve_artifact_rights
    base_kg_params = suite["baseline_infographics"]["knowledge_graph"]["parameterization_receipt"]["applied_params"]
    mut_kg_params = suite["mutated_infographics"]["knowledge_graph"]["parameterization_receipt"]["applied_params"]
    assert base_kg_params["bottlenecks_count"] == 3
    assert mut_kg_params["bottlenecks_count"] == 0
    assert "Gargalos: 0" in suite["mutated_infographics"]["knowledge_graph"]["svg_vector"]

    # 3. Portfolio Mosaic: Licenças pendentes caíram de 3 para 0 e claras subiram de 4 para 7
    base_mos_params = suite["baseline_infographics"]["portfolio_mosaic"]["parameterization_receipt"]["applied_params"]
    mut_mos_params = suite["mutated_infographics"]["portfolio_mosaic"]["parameterization_receipt"]["applied_params"]
    assert base_mos_params["pending_rights_count"] == 3
    assert mut_mos_params["pending_rights_count"] == 0
    assert mut_mos_params["clear_rights_count"] == 7

    # 4. Capital Flow: Valor realizado e ROI líquido aumentaram no Lottie e no SVG
    base_cap_params = suite["baseline_infographics"]["capital_flow"]["parameterization_receipt"]["applied_params"]
    mut_cap_params = suite["mutated_infographics"]["capital_flow"]["parameterization_receipt"]["applied_params"]
    assert mut_cap_params["realized_brl"] > base_cap_params["realized_brl"]
    assert mut_cap_params["net_roi_pct"] > base_cap_params["net_roi_pct"]
    assert mut_bundle["parameterization_receipt"]["patch_applied"] is True


def test_genui_md_workspace_integration_with_lottie_infographics(tmp_path: Path) -> None:
    """Testa a integração entre os infográficos Lottie/SVG, o envelope GenUI-MD e a exportação em disco."""
    orchestrator = PixelCoinOrchestrator()
    spec = orchestrator.generate_ui_spec(
        prompt=CANONICAL_PROMPTS[0]["prompt"],
        budget_limit_brl=1500.0,
    )

    genui_md_text = spec.visual_payloads["genui_md_serialized"]
    parsed_doc = GenUIMDParser.parse(genui_md_text)
    assert parsed_doc.envelope.mode.value == "interactive"
    assert len(parsed_doc.envelope.windows) == 8

    # Inicializa runtime multi-janela e propaga parametrização Lottie entre janelas
    runtime = GenUIWorkspaceRuntime(parsed_doc.envelope)
    updates = runtime.dispatch_event(
        from_ref="alchemical-emblem.lottie_params",
        event="lottie.parameterized",
        payload_value={"realized_brl": 6500.0, "resonance_index": 0.94},
    )
    assert len(updates) == 1
    assert updates[0][0] == "portfolio"
    assert runtime.window_states["portfolio"]["filter"]["realized_brl"] == 6500.0

    # Exporta todos os templates Lottie (baseline + mutados) e SVGs para diretório de teste
    bridge = PixelCoinMCPBridge()
    exported_files = bridge.export_all_templates_to_disk(tmp_path)

    for tid in LottieTemplateRegistry.TEMPLATES:
        assert Path(exported_files[tid]).exists()
        assert Path(exported_files[f"{tid}_svg"]).exists()
        assert Path(exported_files[f"{tid}_mutated_lottie"]).exists()
        assert Path(exported_files[f"{tid}_mutated_svg"]).exists()

    manifest_path = Path(exported_files["suite_manifest"])
    assert manifest_path.exists()
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_data["project"] == "compilatorum/pixelcoin"
    assert len(manifest_data["baseline_receipts"]) == 6
    assert len(manifest_data["mutated_receipts"]) == 6
