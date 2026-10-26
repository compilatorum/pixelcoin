"""
Servidor Unificado LottieMCP & CreatorMCP para o PixelCoin.

Implementa o protocolo JSON-RPC 2.0 (Model Context Protocol - MCP) via stdio e API Python:
- `creator_curate_investment_sea`: Faz a curadoria do "mar de informações" utilizadas como
  fontes de investimento e retorna os fluxos destilados, a matriz de Puxers Quantitativos
  e o índice de Ressonância Lógico-Estética (R_LE).
- `creator_compile_alchemical_emblem`: Compila um Emblema Alquímico de compressão máxima
  (Inscriptio, Pictura SVG Vetorial + Matriz de Puxers, Subscriptio e Lottie JSON).
- `lottie_list_templates`: Lista os 6 templates/scripts paramétricos para cada estrutura
  de infográfico (`alchemical_emblem`, `radial_profile`, `knowledge_graph`, `portfolio_mosaic`,
  `decision_matrix`, `capital_flow`).
- `lottie_parameterize_template`: Recebe o `template_id` e um JSON de atualização/parametrização
  (`params_json`) e compila a animação Lottie (v5.9.0) com os novos quantitativos.
- `lottie_patch_infographic`: Aplica um JSON incremental de atualização sobre um template Lottie.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from pixelcoin.alchemical_infoaesthetics import SeaOfInformationCurator
from pixelcoin.lottie_templates import LottieTemplateRegistry


class PixelCoinMCPBridge:
    """Ponte programática e despachante de ferramentas LottieMCP / CreatorMCP."""

    def __init__(self) -> None:
        self.curator = SeaOfInformationCurator()

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "creator_curate_investment_sea",
                "description": "Curadoria do 'mar de informações' de investimento em fluxos destilados, Puxers quantitativos e Ressonância Lógico-Estética (R_LE).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "realized_brl": {"type": "number", "default": 3700.0},
                        "committed_brl": {"type": "number", "default": 2100.0},
                        "uncertainty_reduction_pct": {"type": "number", "default": 80.0},
                        "synergy_nodes_score": {"type": "number", "default": 62.0},
                        "phi_buffer_ratio": {"type": "number", "default": 1.34},
                    },
                },
            },
            {
                "name": "creator_compile_alchemical_emblem",
                "description": "Gera um Emblema Alquímico de compressão semântica máxima (SVG Vetorial + Matriz de Puxers + Lottie JSON).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target_id": {"type": "string", "default": "compilatorum_portfolio_nexus"},
                        "realized_brl": {"type": "number", "default": 3700.0},
                        "committed_brl": {"type": "number", "default": 2100.0},
                        "uncertainty_reduction_pct": {"type": "number", "default": 80.0},
                        "synergy_nodes_score": {"type": "number", "default": 62.0},
                        "phi_buffer_ratio": {"type": "number", "default": 1.34},
                    },
                },
            },
            {
                "name": "lottie_list_templates",
                "description": "Lista os 6 templates/scripts de estruturas de infográfico suportados pelo LottieMCP.",
                "inputSchema": {"type": "object", "properties": {}},
            },
            {
                "name": "lottie_parameterize_template",
                "description": "Recebe um template_id e um JSON de parâmetros/atualizações quantitativas e gera a estrutura Lottie JSON v5.9.0 parametrizada.",
                "inputSchema": {
                    "type": "object",
                    "required": ["template_id", "params_json"],
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "enum": [
                                "alchemical_emblem",
                                "radial_profile",
                                "knowledge_graph",
                                "portfolio_mosaic",
                                "decision_matrix",
                                "capital_flow",
                            ],
                        },
                        "params_json": {"type": "object"},
                    },
                },
            },
            {
                "name": "lottie_patch_infographic",
                "description": "Recebe um bundle de infográfico Lottie existente e aplica um patch JSON incremental de atualização.",
                "inputSchema": {
                    "type": "object",
                    "required": ["existing_bundle", "patch_json"],
                    "properties": {
                        "existing_bundle": {"type": "object"},
                        "patch_json": {"type": "object"},
                    },
                },
            },
            {
                "name": "lottie_generate_project_infographics_suite",
                "description": "Orquestra as Camadas 1-6, GenUI-MD, CreatorMCP e LottieMCP para gerar a suíte completa de 6 infográficos Lottie + SVG sobre o projeto PixelCoin (incluindo baseline e mutação pós-experimento/auditoria SPDX).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "simulate_lifecycle_mutation": {"type": "boolean", "default": True},
                        "budget_limit_brl": {"type": "number", "default": 1500.0},
                    },
                },
            },
        ]

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        args = arguments or {}
        if name == "creator_curate_investment_sea":
            streams = self.curator.curate_investment_streams({})
            puxers = self.curator.build_puxer_matrix(
                realized_brl=float(args.get("realized_brl", 3700.0)),
                committed_brl=float(args.get("committed_brl", 2100.0)),
                uncertainty_reduction_pct=float(args.get("uncertainty_reduction_pct", 80.0)),
                synergy_nodes_score=float(args.get("synergy_nodes_score", 62.0)),
            )
            resonance = self.curator.compute_resonance(
                phi_buffer_ratio=float(args.get("phi_buffer_ratio", 1.34)),
                puxers=puxers,
            )
            return {
                "curated_streams": [s.model_dump(mode="json") for s in streams],
                "puxers_count": len(puxers),
                "puxers": [p.model_dump(mode="json") for p in puxers],
                "logico_aesthetic_resonance": resonance.model_dump(mode="json"),
            }

        if name == "creator_compile_alchemical_emblem":
            emblem = self.curator.compile_alchemical_emblem(
                target_id=str(args.get("target_id", "compilatorum_portfolio_nexus")),
                realized_brl=float(args.get("realized_brl", 3700.0)),
                committed_brl=float(args.get("committed_brl", 2100.0)),
                uncertainty_reduction_pct=float(args.get("uncertainty_reduction_pct", 80.0)),
                synergy_nodes_score=float(args.get("synergy_nodes_score", 62.0)),
                phi_buffer_ratio=float(args.get("phi_buffer_ratio", 1.34)),
            )
            lottie_bundle = LottieTemplateRegistry.render_template(
                "alchemical_emblem",
                {
                    "realized_brl": emblem.element_totals["terra_realized_brl"],
                    "committed_brl": emblem.element_totals["aqua_committed_brl"],
                    "uncertainty_reduction_pct": emblem.element_totals["ignis_uncertainty_reduction_pct"],
                    "synergy_score": emblem.element_totals["aer_synergy_score"],
                    "resonance_index": emblem.resonance.resonance_index,
                    "pulse_frequency_hz": emblem.resonance.pulse_frequency_hz,
                },
            )
            return {
                "emblem": emblem.model_dump(mode="json"),
                "lottie_bundle": lottie_bundle,
            }

        if name == "lottie_list_templates":
            return {"templates": LottieTemplateRegistry.list_templates()}

        if name == "lottie_parameterize_template":
            template_id = str(args.get("template_id", "alchemical_emblem"))
            params_json = dict(args.get("params_json", {}))
            return LottieTemplateRegistry.render_template(template_id, params_json)

        if name == "lottie_patch_infographic":
            existing = dict(args.get("existing_bundle", {}))
            patch = dict(args.get("patch_json", {}))
            return LottieTemplateRegistry.patch_lottie_animation(existing, patch)

        if name == "lottie_generate_project_infographics_suite":
            return self._generate_project_infographics_suite(
                simulate_lifecycle_mutation=bool(args.get("simulate_lifecycle_mutation", True)),
                budget_limit_brl=float(args.get("budget_limit_brl", 1500.0)),
            )

        raise ValueError(f"Ferramenta LottieMCP/CreatorMCP desconhecida: '{name}'")

    def _generate_project_infographics_suite(
        self,
        simulate_lifecycle_mutation: bool = True,
        budget_limit_brl: float = 1500.0,
    ) -> Dict[str, Any]:
        """Orquestra Camadas 1-6 + GenUI-MD + CreatorMCP + LottieMCP sobre os próprios dados do PixelCoin."""
        from pixelcoin.layer4_orchestrator import CANONICAL_PROMPTS, PixelCoinOrchestrator

        def _extract_metrics_from_spec(spec: Any, orch: PixelCoinOrchestrator) -> Dict[str, Any]:
            vp = spec.visual_payloads
            total_realized = round(sum(o.realized_value_brl for o in orch.economics.opportunities.values()), 2)
            total_committed = round(sum(o.committed_cost_brl for o in orch.economics.opportunities.values()), 2)
            net_roi = round(((total_realized - total_committed) / max(1.0, total_committed)) * 100.0, 2)
            kg = vp["2_knowledge_graph"]
            top_opp = vp["1_radial_profile"]["opportunities"][0]
            axes_map = {
                "evidencia": top_opp["radial_dimensions"][0]["score"],
                "utilidade": top_opp["radial_dimensions"][1]["score"],
                "viabilidade": top_opp["radial_dimensions"][2]["score"],
                "risco_invertido": top_opp["radial_dimensions"][3]["score"],
                "clareza_direitos": top_opp["radial_dimensions"][4]["score"],
                "prontidao_comercial": top_opp["radial_dimensions"][5]["score"],
            }
            all_nodes = kg["nodes"]
            unclear_nodes = kg["unclear_rights_artifacts"]
            clear_count = len(all_nodes) - len(unclear_nodes)
            ranked_exps = vp["4_decision_matrix"]["ranked_experiments"]
            return {
                "total_realized": total_realized,
                "total_committed": total_committed,
                "net_roi": net_roi,
                "nodes_count": len(all_nodes),
                "edges_count": len(kg["edges"]),
                "bottlenecks_count": len(kg["topology_analysis"]["bottlenecks"]),
                "synergies_count": len(kg["topology_analysis"]["top_reusable_hubs"]),
                "clear_rights_count": clear_count,
                "pending_rights_count": len(unclear_nodes),
                "mean_readiness": round(sum(n["reusability_score"] * 10.0 for n in all_nodes) / max(1, len(all_nodes)), 1),
                "top_opp_label": top_opp["title"],
                "top_opp_score": round(sum(axes_map.values()) / max(1, len(axes_map)), 1),
                "axes_map": axes_map,
                "experiments": [
                    {
                        "id": row["experiment_id"],
                        "cost_brl": row["cost_brl"],
                        "expected_gain_pct": row["uncertainty_reduction_pct"],
                        "voe_score": row["efficiency_per_1k_brl"],
                        "status": row["status"],
                    }
                    for row in ranked_exps[:3]
                ],
            }

        orchestrator = PixelCoinOrchestrator()
        baseline_spec = orchestrator.generate_ui_spec(
            prompt=CANONICAL_PROMPTS[0]["prompt"],
            budget_limit_brl=budget_limit_brl,
        )
        bm = _extract_metrics_from_spec(baseline_spec, orchestrator)

        baseline_curated = self.call_tool(
            "creator_curate_investment_sea",
            {
                "realized_brl": bm["total_realized"],
                "committed_brl": bm["total_committed"],
                "uncertainty_reduction_pct": 80.0,
                "synergy_nodes_score": float(bm["nodes_count"] * 8.8),
                "phi_buffer_ratio": orchestrator.economics.phi_buffer_ratio,
            },
        )

        baseline_params_by_template: Dict[str, Dict[str, Any]] = {
            "alchemical_emblem": {
                "realized_brl": bm["total_realized"],
                "committed_brl": bm["total_committed"],
                "uncertainty_reduction_pct": 80.0,
                "synergy_score": float(bm["nodes_count"] * 8.8),
                "resonance_index": baseline_curated["logico_aesthetic_resonance"]["resonance_index"],
                "pulse_frequency_hz": baseline_curated["logico_aesthetic_resonance"]["pulse_frequency_hz"],
            },
            "radial_profile": {
                "target_label": bm["top_opp_label"],
                "axes": bm["axes_map"],
                "composite_score": bm["top_opp_score"],
            },
            "knowledge_graph": {
                "nodes_count": bm["nodes_count"],
                "edges_count": bm["edges_count"],
                "bottlenecks_count": bm["bottlenecks_count"],
                "synergies_count": bm["synergies_count"],
            },
            "portfolio_mosaic": {
                "total_artifacts": bm["nodes_count"],
                "clear_rights_count": bm["clear_rights_count"],
                "pending_rights_count": bm["pending_rights_count"],
                "mean_readiness": bm["mean_readiness"],
            },
            "decision_matrix": {
                "budget_limit_brl": budget_limit_brl,
                "experiments": bm["experiments"],
            },
            "capital_flow": {
                "committed_brl": bm["total_committed"],
                "realized_brl": bm["total_realized"],
                "net_roi_pct": bm["net_roi"],
                "learning_velocity": 82.0,
            },
        }

        baseline_infographics: Dict[str, Dict[str, Any]] = {}
        for tid, tparams in baseline_params_by_template.items():
            baseline_infographics[tid] = self.call_tool(
                "lottie_parameterize_template",
                {"template_id": tid, "params_json": tparams},
            )

        mutated_infographics: Dict[str, Dict[str, Any]] = {}
        lifecycle_events: List[Dict[str, Any]] = []

        if simulate_lifecycle_mutation:
            # 1) Auditar licenças pendentes (reduz gargalos de direitos de 3 para 0)
            for art_id in ("art:wordsmith_ingestor", "art:oracle_associative", "art:sovereign_budget_thermo"):
                resolved = orchestrator.graph.resolve_artifact_rights(
                    artifact_id=art_id,
                    new_spdx="Apache-2.0",
                    audit_note="Direitos auditados via CreatorMCP Suite Test.",
                    source_id="src:repo:license_manifest",
                )
                lifecycle_events.append(
                    {
                        "event": "resolve_artifact_rights",
                        "artifact_id": resolved.artifact_id,
                        "new_spdx": resolved.license_spdx,
                        "license_status": resolved.license_status.value,
                    }
                )

            # 2) Registrar resultado empírico do Experimento A (eleva valor realizado e ROI)
            exp_rec = orchestrator.economics.record_experiment_result(
                experiment_id="exp:A_validar_demanda_curadoria",
                outcome_summary="3 clientes B2B fecharam piloto SaaS após demonstração com GenUI-MD e LottieMCP.",
                realized_cost_brl=450.0,
                realized_revenue_brl=2800.0,
            )
            lifecycle_events.append({"event": "record_experiment_result", "record": exp_rec})

            mutated_spec = orchestrator.generate_ui_spec(
                prompt=CANONICAL_PROMPTS[0]["prompt"],
                budget_limit_brl=budget_limit_brl,
            )
            mm = _extract_metrics_from_spec(mutated_spec, orchestrator)

            mutated_curated = self.call_tool(
                "creator_curate_investment_sea",
                {
                    "realized_brl": mm["total_realized"],
                    "committed_brl": mm["total_committed"],
                    "uncertainty_reduction_pct": 94.0,
                    "synergy_nodes_score": 88.0,
                    "phi_buffer_ratio": 1.38,
                },
            )

            patches_by_template: Dict[str, Dict[str, Any]] = {
                "alchemical_emblem": {
                    "realized_brl": mm["total_realized"],
                    "committed_brl": mm["total_committed"],
                    "uncertainty_reduction_pct": 94.0,
                    "synergy_score": 88.0,
                    "resonance_index": mutated_curated["logico_aesthetic_resonance"]["resonance_index"],
                    "pulse_frequency_hz": mutated_curated["logico_aesthetic_resonance"]["pulse_frequency_hz"],
                },
                "radial_profile": {
                    "target_label": mm["top_opp_label"],
                    "axes": mm["axes_map"],
                    "composite_score": mm["top_opp_score"],
                },
                "knowledge_graph": {
                    "nodes_count": mm["nodes_count"],
                    "edges_count": mm["edges_count"],
                    "bottlenecks_count": mm["bottlenecks_count"],
                    "synergies_count": mm["synergies_count"],
                },
                "portfolio_mosaic": {
                    "total_artifacts": mm["nodes_count"],
                    "clear_rights_count": mm["clear_rights_count"],
                    "pending_rights_count": mm["pending_rights_count"],
                    "mean_readiness": mm["mean_readiness"],
                },
                "decision_matrix": {
                    "budget_limit_brl": budget_limit_brl,
                    "experiments": mm["experiments"],
                },
                "capital_flow": {
                    "committed_brl": mm["total_committed"],
                    "realized_brl": mm["total_realized"],
                    "net_roi_pct": mm["net_roi"],
                    "learning_velocity": 95.0,
                },
            }

            for tid, patch_payload in patches_by_template.items():
                mutated_infographics[tid] = self.call_tool(
                    "lottie_patch_infographic",
                    {
                        "existing_bundle": baseline_infographics[tid],
                        "patch_json": patch_payload,
                    },
                )

        return {
            "project": "compilatorum/pixelcoin",
            "version": "0.5.0",
            "baseline_spec_id": baseline_spec.spec_id,
            "baseline_curated_sea": baseline_curated,
            "baseline_infographics": baseline_infographics,
            "lifecycle_events": lifecycle_events,
            "mutated_infographics": mutated_infographics,
            "genui_md_envelope": baseline_spec.visual_payloads.get("genui_md_serialized", ""),
        }

    def export_all_templates_to_disk(self, out_dir: Path) -> Dict[str, str]:
        """Gera e salva os 6 templates Lottie parametrizados, seus SVGs vetoriais e a suíte do projeto em disco."""
        out_dir.mkdir(parents=True, exist_ok=True)
        suite = self._generate_project_infographics_suite(simulate_lifecycle_mutation=True)
        emblem_res = self.call_tool(
            "creator_compile_alchemical_emblem",
            suite["baseline_infographics"]["alchemical_emblem"]["parameterization_receipt"]["applied_params"],
        )
        svg_path = out_dir / "alchemical_emblem.svg"
        svg_path.write_text(emblem_res["emblem"]["svg_vector_markup"], encoding="utf-8")

        exported: Dict[str, str] = {"alchemical_emblem_svg": str(svg_path)}
        for tmpl in LottieTemplateRegistry.list_templates():
            tid = tmpl["template_id"]
            rendered = suite["baseline_infographics"][tid]
            lpath = out_dir / f"{tid}.lottie.json"
            lpath.write_text(json.dumps(rendered["lottie_json"], ensure_ascii=False, indent=2), encoding="utf-8")
            exported[tid] = str(lpath)

            if "svg_vector" in rendered:
                vpath = out_dir / f"{tid}.svg"
                vpath.write_text(rendered["svg_vector"], encoding="utf-8")
                exported[f"{tid}_svg"] = str(vpath)

            if tid in suite["mutated_infographics"]:
                mrendered = suite["mutated_infographics"][tid]
                mlpath = out_dir / f"{tid}.mutated.lottie.json"
                mlpath.write_text(
                    json.dumps(mrendered["lottie_json"], ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                exported[f"{tid}_mutated_lottie"] = str(mlpath)

                if "svg_vector" in mrendered:
                    mvpath = out_dir / f"{tid}.mutated.svg"
                    mvpath.write_text(mrendered["svg_vector"], encoding="utf-8")
                    exported[f"{tid}_mutated_svg"] = str(mvpath)

        suite_manifest_path = out_dir / "pixelcoin_infographics_suite_manifest.json"
        suite_manifest_path.write_text(
            json.dumps(
                {
                    "project": suite["project"],
                    "version": suite["version"],
                    "baseline_spec_id": suite["baseline_spec_id"],
                    "lifecycle_events": suite["lifecycle_events"],
                    "baseline_receipts": {
                        k: v["parameterization_receipt"] for k, v in suite["baseline_infographics"].items()
                    },
                    "mutated_receipts": {
                        k: v["parameterization_receipt"] for k, v in suite["mutated_infographics"].items()
                    },
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        exported["suite_manifest"] = str(suite_manifest_path)
        return exported


def run_stdio_mcp_server() -> None:
    """Loop JSON-RPC 2.0 sobre stdio compatível com clientes Model Context Protocol (MCP)."""
    bridge = PixelCoinMCPBridge()
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped:
            continue
        try:
            req = json.loads(stripped)
            req_id = req.get("id")
            method = req.get("method", "")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "pixelcoin-lottie-creator-mcp", "version": "0.4.0"},
                    },
                }
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": bridge.list_tools()}}
            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_args = params.get("arguments", {})
                output = bridge.call_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(output, ensure_ascii=False)}],
                        "isError": False,
                    },
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                }
        except Exception as exc:
            resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32000, "message": str(exc)},
            }
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_mcp_server()
