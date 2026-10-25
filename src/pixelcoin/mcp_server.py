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

        raise ValueError(f"Ferramenta LottieMCP/CreatorMCP desconhecida: '{name}'")

    def export_all_templates_to_disk(self, out_dir: Path) -> Dict[str, str]:
        """Gera e salva os 6 templates Lottie parametrizados e o SVG do Emblema Alquímico em disco."""
        out_dir.mkdir(parents=True, exist_ok=True)
        emblem_res = self.call_tool("creator_compile_alchemical_emblem", {})
        svg_path = out_dir / "alchemical_emblem.svg"
        svg_path.write_text(emblem_res["emblem"]["svg_vector_markup"], encoding="utf-8")

        exported: Dict[str, str] = {"alchemical_emblem_svg": str(svg_path)}
        for tmpl in LottieTemplateRegistry.list_templates():
            tid = tmpl["template_id"]
            rendered = LottieTemplateRegistry.render_template(tid, {})
            lpath = out_dir / f"{tid}.lottie.json"
            lpath.write_text(json.dumps(rendered["lottie_json"], ensure_ascii=False, indent=2), encoding="utf-8")
            exported[tid] = str(lpath)
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
