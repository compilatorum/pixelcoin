"""
Motor de Templates/Scripts Lottie & Vetores Paramétricos (LottieMCP / CreatorMCP Engine).

Cada uma das 6 estruturas infoestéticas possui seu próprio template/script parametrizável
que recebe JSONs de atualização (quantitativos de investimento, puxers, scores radiais,
arestas do grafo, matriz de decisão, estágios de fluxo de capital e índice de ressonância R_LE)
e compila um objeto Lottie JSON válido (schema Bodymovin v5.9.0) + Vetor SVG sincronizado:

1. `alchemical_emblem` — Emblema Alquímico de Compressão Máxima (anéis áureos, hexagrama e coroa de puxers)
2. `radial_profile`    — Gráfico Radial de 6 Dimensões (polígono pulsante observado vs. estimado)
3. `knowledge_graph`   — Grafo Semântico e Sinergias (hubs orbitais e alertas de gargalo SPDX)
4. `portfolio_mosaic`  — Mosaico Quantitativo de Puxers (blocos proporcionais a Realizado, Comprometido e Potencial)
5. `decision_matrix`   — Matriz de Decisão e Eficiência Informacional (bolhas cinéticas ΔIncerteza/R$1k)
6. `capital_flow`      — Fluxo de Capital em Movimento (partículas e barras entre os 5 estágios)
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Callable, Dict, List, Optional


def _hex_to_rgb01(hex_color: str) -> List[float]:
    """Converte cor hexadecimal (#RRGGBB) para array normalizado [r, g, b, 1] do Lottie."""
    clean = hex_color.lstrip("#")
    if len(clean) != 6:
        return [0.0, 1.0, 0.533, 1.0]
    r = round(int(clean[0:2], 16) / 255.0, 4)
    g = round(int(clean[2:4], 16) / 255.0, 4)
    b = round(int(clean[4:6], 16) / 255.0, 4)
    return [r, g, b, 1.0]


def _make_animated_scale_ks(
    x: float,
    y: float,
    min_scale: float = 92.0,
    max_scale: float = 108.0,
    frames: int = 120,
    rotate_deg: float = 0.0,
) -> Dict[str, Any]:
    """Cria bloco `ks` (Transform) do Lottie com pulsação de escala e rotação opcional."""
    half = max(1, frames // 2)
    r_prop: Dict[str, Any]
    if rotate_deg != 0.0:
        r_prop = {
            "a": 1,
            "k": [
                {"t": 0, "s": [0.0], "i": {"x": [0.5], "y": [0.5]}, "o": {"x": [0.5], "y": [0.5]}},
                {"t": frames, "s": [rotate_deg]},
            ],
        }
    else:
        r_prop = {"a": 0, "k": 0.0}

    return {
        "o": {"a": 0, "k": 100},
        "r": r_prop,
        "p": {"a": 0, "k": [x, y, 0]},
        "a": {"a": 0, "k": [0, 0, 0]},
        "s": {
            "a": 1,
            "k": [
                {"t": 0, "s": [min_scale, min_scale, 100], "i": {"x": [0.4, 0.4, 0.4], "y": [1, 1, 1]}, "o": {"x": [0.6, 0.6, 0.6], "y": [0, 0, 0]}},
                {"t": half, "s": [max_scale, max_scale, 100], "i": {"x": [0.4, 0.4, 0.4], "y": [1, 1, 1]}, "o": {"x": [0.6, 0.6, 0.6], "y": [0, 0, 0]}},
                {"t": frames, "s": [min_scale, min_scale, 100]},
            ],
        },
    }


def _make_shape_layer(
    ind: int,
    name: str,
    x: float,
    y: float,
    shapes: List[Dict[str, Any]],
    frames: int = 120,
    min_scale: float = 95.0,
    max_scale: float = 105.0,
    rotate_deg: float = 0.0,
) -> Dict[str, Any]:
    """Cria uma Shape Layer (`ty: 4`) padrão Bodymovin/Lottie."""
    return {
        "ddd": 0,
        "ind": ind,
        "ty": 4,
        "nm": name,
        "sr": 1,
        "ks": _make_animated_scale_ks(x, y, min_scale=min_scale, max_scale=max_scale, frames=frames, rotate_deg=rotate_deg),
        "ao": 0,
        "shapes": shapes,
        "ip": 0,
        "op": frames,
        "st": 0,
        "bm": 0,
    }


def _ellipse_group(name: str, radius: float, stroke_hex: str, fill_hex: Optional[str] = None, stroke_width: float = 3.0) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = [
        {
            "ty": "el",
            "d": 1,
            "s": {"a": 0, "k": [radius * 2.0, radius * 2.0]},
            "p": {"a": 0, "k": [0, 0]},
            "nm": f"{name}_path",
        },
        {
            "ty": "st",
            "c": {"a": 0, "k": _hex_to_rgb01(stroke_hex)},
            "o": {"a": 0, "k": 100},
            "w": {"a": 0, "k": stroke_width},
            "lc": 2,
            "lj": 2,
            "nm": f"{name}_stroke",
        },
    ]
    if fill_hex:
        items.append(
            {
                "ty": "fl",
                "c": {"a": 0, "k": _hex_to_rgb01(fill_hex)},
                "o": {"a": 0, "k": 28},
                "r": 1,
                "nm": f"{name}_fill",
            }
        )
    items.append(
        {
            "ty": "tr",
            "p": {"a": 0, "k": [0, 0]},
            "a": {"a": 0, "k": [0, 0]},
            "s": {"a": 0, "k": [100, 100]},
            "r": {"a": 0, "k": 0},
            "o": {"a": 0, "k": 100},
        }
    )
    return {"ty": "gr", "it": items, "nm": name}


def _polystar_group(name: str, points: int, outer_radius: float, stroke_hex: str, fill_hex: str) -> Dict[str, Any]:
    return {
        "ty": "gr",
        "nm": name,
        "it": [
            {
                "ty": "sr",
                "sy": 2,  # Polygon
                "d": 1,
                "pt": {"a": 0, "k": points},
                "p": {"a": 0, "k": [0, 0]},
                "r": {"a": 0, "k": 0},
                "or": {"a": 0, "k": outer_radius},
                "os": {"a": 0, "k": 0},
                "nm": f"{name}_poly",
            },
            {
                "ty": "st",
                "c": {"a": 0, "k": _hex_to_rgb01(stroke_hex)},
                "o": {"a": 0, "k": 100},
                "w": {"a": 0, "k": 3.0},
                "lc": 2,
                "lj": 2,
                "nm": f"{name}_stroke",
            },
            {
                "ty": "fl",
                "c": {"a": 0, "k": _hex_to_rgb01(fill_hex)},
                "o": {"a": 0, "k": 30},
                "r": 1,
                "nm": f"{name}_fill",
            },
            {
                "ty": "tr",
                "p": {"a": 0, "k": [0, 0]},
                "a": {"a": 0, "k": [0, 0]},
                "s": {"a": 0, "k": [100, 100]},
                "r": {"a": 0, "k": 0},
                "o": {"a": 0, "k": 100},
            },
        ],
    }


def _rect_group(name: str, width: float, height: float, stroke_hex: str, fill_hex: str, roundness: float = 6.0) -> Dict[str, Any]:
    return {
        "ty": "gr",
        "nm": name,
        "it": [
            {
                "ty": "rc",
                "d": 1,
                "s": {"a": 0, "k": [width, height]},
                "p": {"a": 0, "k": [0, 0]},
                "r": {"a": 0, "k": roundness},
                "nm": f"{name}_rect",
            },
            {
                "ty": "st",
                "c": {"a": 0, "k": _hex_to_rgb01(stroke_hex)},
                "o": {"a": 0, "k": 100},
                "w": {"a": 0, "k": 2.0},
                "nm": f"{name}_stroke",
            },
            {
                "ty": "fl",
                "c": {"a": 0, "k": _hex_to_rgb01(fill_hex)},
                "o": {"a": 0, "k": 75},
                "r": 1,
                "nm": f"{name}_fill",
            },
            {
                "ty": "tr",
                "p": {"a": 0, "k": [0, 0]},
                "a": {"a": 0, "k": [0, 0]},
                "s": {"a": 0, "k": [100, 100]},
                "r": {"a": 0, "k": 0},
                "o": {"a": 0, "k": 100},
            },
        ],
    }


class LottieTemplateRegistry:
    """
    Registro de Templates/Scripts Lottie & Vetoriais do PixelCoin.
    Permite parametrizar qualquer uma das 6 estruturas infoestéticas com novos JSONs de dados.
    """

    TEMPLATE_METADATA: Dict[str, Dict[str, Any]] = {
        "alchemical_emblem": {
            "template_id": "alchemical_emblem",
            "title": "Emblema Alquímico de Compressão Semântica Máxima",
            "description": "Condensa os 4 elementos quantitativos (Terra/Realizado, Aqua/Comprometido, Ignis/ΔIncerteza, Aer/Sinergia), anéis áureos e índice de ressonância R_LE em animação Lottie + SVG.",
            "required_params": ["realized_brl", "committed_brl", "uncertainty_reduction_pct", "synergy_score", "resonance_index", "pulse_frequency_hz"],
        },
        "radial_profile": {
            "template_id": "radial_profile",
            "title": "Gráfico Radial Dinâmico de 6 Dimensões",
            "description": "Polígono hexagonal parametrizado pelas 6 dimensões da oportunidade, pulsando diferentemente para dimensões observadas vs. estimadas.",
            "required_params": ["opportunity_title", "scores", "estimated_flags"],
        },
        "knowledge_graph": {
            "template_id": "knowledge_graph",
            "title": "Grafo Semântico Orbital & Gargalos SPDX",
            "description": "Núcleos dos 7 módulos do Compilatorum conectados por órbitas de reutilização e alertas visuais para gargalos de licença.",
            "required_params": ["total_nodes", "total_edges", "bottlenecks_count", "top_hub_score"],
        },
        "portfolio_mosaic": {
            "template_id": "portfolio_mosaic",
            "title": "Mosaico Quantitativo de Puxers (Realizado vs. Custo vs. Potencial)",
            "description": "Grade de blocos e puxers onde a área e a cor distinguem estritamente valor realizado, custo comprometido e potencial estimado.",
            "required_params": ["realized_brl", "committed_brl", "estimated_potential_brl", "puxer_quantum_brl"],
        },
        "decision_matrix": {
            "template_id": "decision_matrix",
            "title": "Matriz de Decisão Cinética (Evidência vs. Custo de Validação)",
            "description": "Bolhas animadas posicionadas por Custo (X), Evidência de Demanda (Y) e Eficiência Informacional ΔIncerteza/R$1k (Raio/Pulso).",
            "required_params": ["experiments", "budget_brl", "phi_buffer"],
        },
        "capital_flow": {
            "template_id": "capital_flow",
            "title": "Fluxo Alquímico de Capital em 5 Estágios",
            "description": "Barras e pulsos de liquidez percorrendo Alocação → Execução → Marcos → Resultados → Reinvestimento.",
            "required_params": ["stages", "phi_buffer"],
        },
    }

    @classmethod
    def list_templates(cls) -> List[Dict[str, Any]]:
        return list(cls.TEMPLATE_METADATA.values())

    @classmethod
    def render_template(cls, template_id: str, params_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recebe o `template_id` e um JSON de parâmetros (`params_json`),
        e retorna o pacote completo: `lottie_json` (v5.9.0), `svg_vector` e `parameterization_receipt`.
        """
        builders: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
            "alchemical_emblem": cls._build_alchemical_emblem,
            "radial_profile": cls._build_radial_profile,
            "knowledge_graph": cls._build_knowledge_graph,
            "portfolio_mosaic": cls._build_portfolio_mosaic,
            "decision_matrix": cls._build_decision_matrix,
            "capital_flow": cls._build_capital_flow,
        }
        if template_id not in builders:
            raise ValueError(f"Template Lottie desconhecido: '{template_id}'. Opções: {list(builders.keys())}")

        result = builders[template_id](params_json)
        param_hash = hashlib.sha256(json.dumps(params_json, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]
        result["parameterization_receipt"] = {
            "status": "parameterized_ok",
            "template_id": template_id,
            "params_sha256": param_hash,
            "lottie_version": result["lottie_json"]["v"],
            "layers_count": len(result["lottie_json"]["layers"]),
            "applied_params": result.get("applied_params", {}),
            "patch_applied": False,
        }
        return result

    @classmethod
    def patch_lottie_animation(cls, existing_bundle: Dict[str, Any], patch_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recebe um bundle Lottie previamente gerado e um JSON de atualização incremental (`patch_json`),
        mescla os parâmetros quantitativos e recompila a estrutura Lottie + SVG.
        """
        template_id = existing_bundle.get("template_id", "alchemical_emblem")
        merged_params = copy.deepcopy(existing_bundle.get("applied_params", {}))
        merged_params.update(patch_json)
        res = cls.render_template(template_id, merged_params)
        res["parameterization_receipt"]["patch_applied"] = True
        return res

    @classmethod
    def _build_alchemical_emblem(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        realized = float(params.get("realized_brl", 3700.0))
        committed = float(params.get("committed_brl", 2100.0))
        uncertainty = float(params.get("uncertainty_reduction_pct", 80.0))
        synergy = float(params.get("synergy_score", 62.0))
        resonance_idx = float(params.get("resonance_index", 0.85))
        pulse_hz = float(params.get("pulse_frequency_hz", 1.45))

        fps = 60
        frames = max(60, int(round(fps / max(0.3, pulse_hz))))
        outer_r = round(110.0 + (resonance_idx * 45.0), 1)
        hex_r = round(outer_r / 1.618, 1)
        core_r = round(hex_r / 1.618, 1)

        layers = [
            _make_shape_layer(
                ind=1,
                name="Core_QuintaEssentia_Ring",
                x=200,
                y=200,
                shapes=[_ellipse_group("core_circle", core_r, "#FFD700", "#00FF88", stroke_width=3.5)],
                frames=frames,
                min_scale=90.0,
                max_scale=112.0,
            ),
            _make_shape_layer(
                ind=2,
                name="Hexagram_6_Dimensions_Star",
                x=200,
                y=200,
                shapes=[_polystar_group("hex_star", 6, hex_r, "#00BFFF", "#B388FF")],
                frames=frames,
                min_scale=96.0,
                max_scale=104.0,
                rotate_deg=360.0,
            ),
            _make_shape_layer(
                ind=3,
                name="Puxer_Quantitative_Corona",
                x=200,
                y=200,
                shapes=[_ellipse_group("puxer_ring", outer_r, "#00FF88", None, stroke_width=4.0)],
                frames=frames,
                min_scale=98.0,
                max_scale=102.0,
                rotate_deg=-180.0,
            ),
        ]

        lottie_json = {
            "v": "5.9.0",
            "fr": fps,
            "ip": 0,
            "op": frames,
            "w": 400,
            "h": 400,
            "nm": f"PixelCoin_Alchemical_Emblem_R{int(resonance_idx*100)}",
            "ddd": 0,
            "assets": [],
            "layers": layers,
            "meta": {
                "generator": "PixelCoin LottieMCP / CreatorMCP v0.4.0",
                "template_id": "alchemical_emblem",
                "puxer_metrics": {
                    "terra_realized_brl": realized,
                    "aqua_committed_brl": committed,
                    "ignis_uncertainty_pct": uncertainty,
                    "aer_synergy_score": synergy,
                    "resonance_index": resonance_idx,
                },
            },
        }
        return {
            "template_id": "alchemical_emblem",
            "applied_params": {
                "realized_brl": realized,
                "committed_brl": committed,
                "uncertainty_reduction_pct": uncertainty,
                "synergy_score": synergy,
                "resonance_index": resonance_idx,
                "pulse_frequency_hz": pulse_hz,
            },
            "lottie_json": lottie_json,
            "svg_vector": (
                f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
                f'<rect width="400" height="400" fill="#07100A" rx="8"/>'
                f'<circle cx="200" cy="200" r="{outer_r}" fill="none" stroke="#00FF88" stroke-width="2" stroke-dasharray="5,3"/>'
                f'<circle cx="200" cy="200" r="{hex_r}" fill="rgba(0,191,255,0.12)" stroke="#00BFFF" stroke-width="2"/>'
                f'<circle cx="200" cy="200" r="{core_r}" fill="#0D1A10" stroke="#FFD700" stroke-width="2.5"/>'
                f'<text x="200" y="196" text-anchor="middle" fill="#FFD700" font-family="monospace" font-size="18" font-weight="bold">🜏 R_LE={resonance_idx:.2f}</text>'
                f'<text x="200" y="216" text-anchor="middle" fill="#00FF88" font-family="monospace" font-size="11">🜃 R${realized:.0f} | 🜄 R${committed:.0f}</text>'
                f'<text x="200" y="382" text-anchor="middle" fill="#B388FF" font-family="monospace" font-size="10">🜂 ΔInc -{uncertainty:.0f}% · 🜁 Sinergia {synergy:.0f}pts · {pulse_hz}Hz</text>'
                f'</svg>'
            ),
        }

    @classmethod
    def _build_radial_profile(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        title = str(params.get("opportunity_title") or params.get("target_label") or "Curadoria Semântica B2B")
        axes_dict = params.get("axes")
        if isinstance(axes_dict, dict) and axes_dict:
            scores: List[float] = [float(v) for v in axes_dict.values()]
        else:
            scores = list(params.get("scores", [84.0, 90.0, 88.0, 82.0, 68.0, 76.0]))
        estimated_flags: List[bool] = list(params.get("estimated_flags", [False, False, False, False, False, True]))
        avg_score = float(params.get("composite_score", sum(scores) / max(1, len(scores))))
        est_count = sum(1 for f in estimated_flags if f)

        radius = round(60.0 + (avg_score * 0.85), 1)
        stroke_color = "#00FF88" if est_count <= 1 else "#FFB800"

        layers = [
            _make_shape_layer(
                ind=1,
                name="Radial_Observed_Polygon",
                x=200,
                y=200,
                shapes=[_polystar_group("radial_hex", 6, radius, stroke_color, "#00BFFF")],
                frames=120,
                min_scale=93.0,
                max_scale=107.0,
            ),
            _make_shape_layer(
                ind=2,
                name="Radial_Reference_Grid",
                x=200,
                y=200,
                shapes=[_ellipse_group("grid_100", 145.0, "#1A3320", None, stroke_width=1.5)],
                frames=120,
                min_scale=100.0,
                max_scale=100.0,
            ),
        ]
        return {
            "template_id": "radial_profile",
            "applied_params": {
                "opportunity_title": title,
                "target_label": title,
                "scores": scores,
                "estimated_flags": estimated_flags,
                "composite_score": round(avg_score, 2),
            },
            "lottie_json": {
                "v": "5.9.0",
                "fr": 60,
                "ip": 0,
                "op": 120,
                "w": 400,
                "h": 400,
                "nm": f"PixelCoin_Radial_{title[:18]}",
                "ddd": 0,
                "assets": [],
                "layers": layers,
                "meta": {"average_score": round(avg_score, 2), "estimated_dimensions_count": est_count},
            },
            "svg_vector": (
                f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
                f'<rect width="400" height="400" fill="#07100A" rx="8"/>'
                f'<circle cx="200" cy="200" r="145" fill="none" stroke="#1A3320" stroke-width="1.5"/>'
                f'<circle cx="200" cy="200" r="{radius}" fill="rgba(0,255,136,0.14)" stroke="{stroke_color}" stroke-width="2.5"/>'
                f'<text x="200" y="196" text-anchor="middle" fill="#C8E6C9" font-family="monospace" font-size="13" font-weight="bold">{title[:32]}</text>'
                f'<text x="200" y="216" text-anchor="middle" fill="{stroke_color}" font-family="monospace" font-size="12">Média={avg_score:.1f}/100 ({est_count} est.)</text>'
                f'</svg>'
            ),
        }

    @classmethod
    def _build_knowledge_graph(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        total_nodes = int(params.get("total_nodes", params.get("nodes_count", 7)))
        total_edges = int(params.get("total_edges", params.get("edges_count", 9)))
        bottlenecks = int(params.get("bottlenecks_count", 3))
        top_hub_score = float(params.get("top_hub_score", 9.6))

        layers: List[Dict[str, Any]] = []
        for idx in range(total_nodes):
            angle_offset = (idx * 50) % 300
            nx = 90 + (idx * 38)
            ny = 100 + ((idx % 3) * 85)
            is_bottleneck_node = idx < bottlenecks
            color = "#FF4455" if is_bottleneck_node else "#00FF88"
            layers.append(
                _make_shape_layer(
                    ind=idx + 1,
                    name=f"Graph_Node_{idx+1}",
                    x=nx,
                    y=ny,
                    shapes=[_ellipse_group(f"node_{idx+1}", 22.0, color, "#00BFFF", stroke_width=3.0)],
                    frames=120,
                    min_scale=92.0,
                    max_scale=108.0 + (angle_offset * 0.01),
                )
            )

        return {
            "template_id": "knowledge_graph",
            "applied_params": {
                "total_nodes": total_nodes,
                "nodes_count": total_nodes,
                "total_edges": total_edges,
                "edges_count": total_edges,
                "bottlenecks_count": bottlenecks,
                "top_hub_score": top_hub_score,
            },
            "lottie_json": {
                "v": "5.9.0",
                "fr": 60,
                "ip": 0,
                "op": 120,
                "w": 400,
                "h": 400,
                "nm": "PixelCoin_Knowledge_Graph_Topology",
                "ddd": 0,
                "assets": [],
                "layers": layers,
                "meta": {"total_nodes": total_nodes, "total_edges": total_edges, "bottlenecks": bottlenecks},
            },
            "svg_vector": (
                f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
                f'<rect width="400" height="400" fill="#07100A" rx="8"/>'
                f'<line x1="90" y1="120" x2="310" y2="280" stroke="#00BFFF" stroke-width="2"/>'
                f'<line x1="310" y1="120" x2="90" y2="280" stroke="#FF4455" stroke-width="2" stroke-dasharray="5,4"/>'
                f'<circle cx="200" cy="200" r="36" fill="#0D1A10" stroke="#00FF88" stroke-width="3"/>'
                f'<text x="200" y="204" text-anchor="middle" fill="#00FF88" font-family="monospace" font-size="11" font-weight="bold">Hub {top_hub_score}</text>'
                f'<text x="200" y="378" text-anchor="middle" fill="#C8E6C9" font-family="monospace" font-size="11">{total_nodes} Nós · {total_edges} Arestas · Gargalos: {bottlenecks}</text>'
                f'</svg>'
            ),
        }

    @classmethod
    def _build_portfolio_mosaic(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        realized = float(params.get("realized_brl", 3700.0))
        committed = float(params.get("committed_brl", 2100.0))
        potential = float(params.get("estimated_potential_brl", 180000.0))
        quantum = float(params.get("puxer_quantum_brl", 250.0))
        total_artifacts = int(params.get("total_artifacts", 7))
        clear_rights_count = int(params.get("clear_rights_count", 4))
        pending_rights_count = int(params.get("pending_rights_count", 3))
        mean_readiness = float(params.get("mean_readiness", 88.4))

        realized_puxers = max(1, int(round(realized / quantum)))
        committed_puxers = max(1, int(round(committed / quantum)))

        w_realized = min(180.0, 40.0 + realized_puxers * 6.0)
        w_committed = min(180.0, 40.0 + committed_puxers * 6.0)

        layers = [
            _make_shape_layer(
                ind=1,
                name="Mosaic_Realized_Block_Terra",
                x=115,
                y=140,
                shapes=[_rect_group("realized_rect", w_realized, 110.0, "#00FF88", "#00FF88")],
                frames=120,
                min_scale=96.0,
                max_scale=104.0,
            ),
            _make_shape_layer(
                ind=2,
                name="Mosaic_Committed_Block_Aqua",
                x=285,
                y=140,
                shapes=[_rect_group("committed_rect", w_committed, 110.0, "#00BFFF", "#00BFFF")],
                frames=120,
                min_scale=96.0,
                max_scale=104.0,
            ),
            _make_shape_layer(
                ind=3,
                name="Mosaic_Estimated_Potential_Ignis",
                x=200,
                y=295,
                shapes=[_rect_group("potential_rect", 310.0, 85.0, "#FFB800", "#FFB800")],
                frames=120,
                min_scale=98.0,
                max_scale=102.0,
            ),
        ]

        return {
            "template_id": "portfolio_mosaic",
            "applied_params": {
                "realized_brl": realized,
                "committed_brl": committed,
                "estimated_potential_brl": potential,
                "puxer_quantum_brl": quantum,
                "total_artifacts": total_artifacts,
                "clear_rights_count": clear_rights_count,
                "pending_rights_count": pending_rights_count,
                "mean_readiness": mean_readiness,
            },
            "lottie_json": {
                "v": "5.9.0",
                "fr": 60,
                "ip": 0,
                "op": 120,
                "w": 400,
                "h": 400,
                "nm": "PixelCoin_Portfolio_Puxer_Mosaic",
                "ddd": 0,
                "assets": [],
                "layers": layers,
                "meta": {
                    "realized_puxers": realized_puxers,
                    "committed_puxers": committed_puxers,
                    "puxer_quantum_brl": quantum,
                    "clear_rights_count": clear_rights_count,
                    "pending_rights_count": pending_rights_count,
                },
            },
            "svg_vector": (
                f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
                f'<rect width="400" height="400" fill="#07100A" rx="8"/>'
                f'<rect x="25" y="60" width="{w_realized}" height="120" rx="6" fill="rgba(0,255,136,0.22)" stroke="#00FF88" stroke-width="2"/>'
                f'<text x="35" y="120" fill="#00FF88" font-family="monospace" font-size="11" font-weight="bold">🜃 Realizado: R${realized:.0f} ({realized_puxers} pux)</text>'
                f'<rect x="215" y="60" width="{w_committed}" height="120" rx="6" fill="rgba(0,191,255,0.22)" stroke="#00BFFF" stroke-width="2"/>'
                f'<text x="225" y="120" fill="#00BFFF" font-family="monospace" font-size="11" font-weight="bold">🜄 Custo: R${committed:.0f} ({committed_puxers} pux)</text>'
                f'<rect x="25" y="210" width="350" height="120" rx="6" fill="rgba(255,184,0,0.16)" stroke="#FFB800" stroke-width="2" stroke-dasharray="5,3"/>'
                f'<text x="200" y="275" text-anchor="middle" fill="#FFB800" font-family="monospace" font-size="12" font-weight="bold">🜂 Potencial Estimado: R${potential:.0f}/ano · SPDX {clear_rights_count}/{total_artifacts}</text>'
                f'</svg>'
            ),
        }

    @classmethod
    def _build_decision_matrix(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        exps: List[Dict[str, Any]] = list(
            params.get(
                "experiments",
                [
                    {"code": "C", "cost_brl": 350.0, "demand_evidence_score": 76.0, "efficiency_per_1k_brl": 108.57},
                    {"code": "A", "cost_brl": 450.0, "demand_evidence_score": 84.0, "efficiency_per_1k_brl": 93.33},
                    {"code": "D", "cost_brl": 500.0, "demand_evidence_score": 78.0, "efficiency_per_1k_brl": 60.0},
                    {"code": "B", "cost_brl": 1200.0, "demand_evidence_score": 58.0, "efficiency_per_1k_brl": 29.17},
                ],
            )
        )
        budget = float(params.get("budget_brl", 1500.0))
        phi = float(params.get("phi_buffer", 1.34))

        colors = ["#FFD700", "#00FF88", "#B388FF", "#00BFFF"]
        layers: List[Dict[str, Any]] = []
        for idx, exp in enumerate(exps):
            cost = float(exp.get("cost_brl", 500.0))
            ev = float(exp.get("demand_evidence_score", 75.0))
            eff = float(exp.get("efficiency_per_1k_brl", 80.0))
            bx = round(50.0 + min(300.0, (cost / 1400.0) * 300.0), 1)
            by = round(350.0 - min(300.0, (ev / 100.0) * 300.0), 1)
            br = round(max(14.0, min(48.0, eff * 0.36)), 1)
            col = colors[idx % len(colors)]
            layers.append(
                _make_shape_layer(
                    ind=idx + 1,
                    name=f"Experiment_{exp.get('code', idx)}_Bubble",
                    x=bx,
                    y=by,
                    shapes=[_ellipse_group(f"bubble_{idx}", br, col, col, stroke_width=2.5)],
                    frames=120,
                    min_scale=90.0,
                    max_scale=112.0,
                )
            )

        return {
            "template_id": "decision_matrix",
            "applied_params": {
                "experiments": exps,
                "budget_brl": budget,
                "phi_buffer": phi,
            },
            "lottie_json": {
                "v": "5.9.0",
                "fr": 60,
                "ip": 0,
                "op": 120,
                "w": 400,
                "h": 400,
                "nm": "PixelCoin_Decision_Matrix_Efficiency",
                "ddd": 0,
                "assets": [],
                "layers": layers,
                "meta": {"budget_brl": budget, "phi_buffer": phi},
            },
            "svg_vector": (
                f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
                f'<rect width="400" height="400" fill="#07100A" rx="8"/>'
                f'<line x1="40" y1="350" x2="370" y2="350" stroke="#6B9E7A" stroke-width="1.5"/>'
                f'<line x1="40" y1="40" x2="40" y2="350" stroke="#6B9E7A" stroke-width="1.5"/>'
                f'<circle cx="115" cy="110" r="36" fill="rgba(255,215,0,0.24)" stroke="#FFD700" stroke-width="2.5"/>'
                f'<text x="115" y="114" text-anchor="middle" fill="#FFD700" font-family="monospace" font-size="11" font-weight="bold">Exp C (108.6)</text>'
                f'<circle cx="145" cy="90" r="32" fill="rgba(0,255,136,0.24)" stroke="#00FF88" stroke-width="2.5"/>'
                f'<text x="145" y="94" text-anchor="middle" fill="#00FF88" font-family="monospace" font-size="11" font-weight="bold">Exp A (93.3)</text>'
                f'<circle cx="310" cy="210" r="18" fill="rgba(0,191,255,0.20)" stroke="#00BFFF" stroke-width="2"/>'
                f'<text x="310" y="214" text-anchor="middle" fill="#00BFFF" font-family="monospace" font-size="10">Exp B (29.2)</text>'
                f'<text x="200" y="382" text-anchor="middle" fill="#C8E6C9" font-family="monospace" font-size="10">Orçamento R${budget:.0f} · Φ_buffer={phi:.2f}x</text>'
                f'</svg>'
            ),
        }

    @classmethod
    def _build_capital_flow(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        committed_brl = float(params.get("committed_brl", 2100.0))
        realized_brl = float(params.get("realized_brl", 3700.0))
        net_roi_pct = float(params.get("net_roi_pct", 76.19))
        learning_velocity = float(params.get("learning_velocity", 82.0))
        stages: List[Dict[str, Any]] = list(
            params.get(
                "stages",
                [
                    {"stage_name": "1. Alocação", "planned_brl": 4500.0, "committed_brl": committed_brl, "realized_brl": committed_brl},
                    {"stage_name": "2. Execução", "planned_brl": 2500.0, "committed_brl": 800.0, "realized_brl": 650.0},
                    {"stage_name": "3. Marcos", "planned_brl": 2000.0, "committed_brl": 1300.0, "realized_brl": 950.0},
                    {"stage_name": "4. Resultados", "planned_brl": 12000.0, "committed_brl": realized_brl, "realized_brl": realized_brl},
                    {"stage_name": "5. Reinvestimento", "planned_brl": 3000.0, "committed_brl": 1100.0, "realized_brl": 1100.0},
                ],
            )
        )
        phi = float(params.get("phi_buffer", 1.34))

        layers: List[Dict[str, Any]] = []
        for idx, stg in enumerate(stages):
            realized = float(stg.get("realized_brl", 1000.0))
            bar_h = round(max(30.0, min(260.0, (realized / 4500.0) * 220.0)), 1)
            sx = 55.0 + (idx * 72.0)
            sy = round(340.0 - (bar_h / 2.0), 1)
            layers.append(
                _make_shape_layer(
                    ind=idx + 1,
                    name=f"Capital_Stage_{idx+1}",
                    x=sx,
                    y=sy,
                    shapes=[_rect_group(f"stage_bar_{idx+1}", 44.0, bar_h, "#00FF88", "#00BFFF", roundness=4.0)],
                    frames=120,
                    min_scale=94.0,
                    max_scale=106.0,
                )
            )

        return {
            "template_id": "capital_flow",
            "applied_params": {
                "stages": stages,
                "phi_buffer": phi,
                "committed_brl": committed_brl,
                "realized_brl": realized_brl,
                "net_roi_pct": net_roi_pct,
                "learning_velocity": learning_velocity,
            },
            "lottie_json": {
                "v": "5.9.0",
                "fr": 60,
                "ip": 0,
                "op": 120,
                "w": 400,
                "h": 400,
                "nm": "PixelCoin_Capital_Flow_Stages",
                "ddd": 0,
                "assets": [],
                "layers": layers,
                "meta": {"stages_count": len(stages), "phi_buffer": phi, "net_roi_pct": net_roi_pct},
            },
            "svg_vector": (
                f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
                f'<rect width="400" height="400" fill="#07100A" rx="8"/>'
                f'<rect x="35" y="160" width="46" height="180" rx="4" fill="rgba(0,255,136,0.3)" stroke="#00FF88" stroke-width="2"/>'
                f'<rect x="105" y="260" width="46" height="80" rx="4" fill="rgba(0,191,255,0.3)" stroke="#00BFFF" stroke-width="2"/>'
                f'<rect x="175" y="230" width="46" height="110" rx="4" fill="rgba(179,136,255,0.3)" stroke="#B388FF" stroke-width="2"/>'
                f'<rect x="245" y="90" width="46" height="250" rx="4" fill="rgba(0,255,136,0.45)" stroke="#00FF88" stroke-width="2.5"/>'
                f'<rect x="315" y="210" width="46" height="130" rx="4" fill="rgba(255,215,0,0.3)" stroke="#FFD700" stroke-width="2"/>'
                f'<text x="200" y="378" text-anchor="middle" fill="#00FF88" font-family="monospace" font-size="10">Realizado R${realized_brl:.0f} · ROI {net_roi_pct:.1f}% · Φ={phi:.2f}x</text>'
                f'</svg>'
            ),
        }

    TEMPLATES = TEMPLATE_METADATA
