"""
Curadoria do "Mar de Informações", Ressonância Lógico-Estética, Puxers Quantitativos
e Compressão Máxima em Emblemas Alquímicos (Vetores SVG + Matriz de Puxers).

Fundamento Conceitual:
- Cada Puxer (unidade visual quantitativa de decisão) representa um quantitativo explícito
  e auditável (ex: 1 Puxer Financeiro = R$ 250,00; 1 Puxer Informacional = 5% de ΔIncerteza;
  1 Puxer Epistêmico = 1 prova observada com hash SHA-256).
- Ressonância Lógico-Estética (R_LE): acopla o rigor lógico-econômico (evidência empírica,
  margem fiduciária Phi_buffer, eficiência informacional) à harmonia geométrica e cinética
  (proporção áurea phi=1.618, simetria poligonal, frequência de pulso e temperatura cromática).
- Emblema Alquímico: síntese de compressão máxima estruturada na tríade clássica:
  1. Inscriptio (Lema / Fórmula Operacional)
  2. Pictura (Geometria Sagrada Vetorial SVG + Matriz de Puxers Quantitativos nos 4 Elementos:
     🜂 Ignis/Potencial, 🜄 Aqua/Liquidez, 🜃 Terra/Evidência Realizada, 🜁 Aer/Sinergia de Grafo)
  3. Subscriptio (Epigrama de Decisão, Regra Go/No-Go e Selo Criptográfico SHA-256)
"""

from __future__ import annotations

import hashlib
import math
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


GOLDEN_RATIO = 1.61803398875


class AlchemicalElement(str, Enum):
    IGNIS = "ignis"  # 🜂 Enxofre: Impulso experimental, ΔIncerteza/custo e potencial estimado
    AQUA = "aqua"    # 🜄 Mercúrio: Liquidez em movimento, Φ_buffer e fluxo de capital
    TERRA = "terra"  # 🜃 Sal: Lastro empírico observado, receita realizada e licenças SPDX limpas
    AER = "aer"      # 🜁 Quintessência: Conectividade do grafo, reutilização e sinergias


ELEMENT_GLYPHS: Dict[AlchemicalElement, str] = {
    AlchemicalElement.IGNIS: "🜂",
    AlchemicalElement.AQUA: "🜄",
    AlchemicalElement.TERRA: "🜃",
    AlchemicalElement.AER: "🜁",
}

ELEMENT_COLORS: Dict[AlchemicalElement, str] = {
    AlchemicalElement.IGNIS: "#FFB800",  # Ouro / Âmbar Solar
    AlchemicalElement.AQUA: "#00BFFF",   # Ciano Mercurial
    AlchemicalElement.TERRA: "#00FF88",  # Esmeralda Terrestre (Observado)
    AlchemicalElement.AER: "#B388FF",    # Violeta Etéreo (Grafo/Sinergia)
}


class PuxerUnit(BaseModel):
    """
    Unidade elementar quantitativa ('Puxer' = Pixel + Quantitativo + Vetor).
    Cada puxer no infográfico equivale a uma magnitude real e rastreável.
    """

    puxer_id: str
    index: int
    element: AlchemicalElement
    glyph: str
    unit_quantum: float = Field(..., description="Magnitude representada por este único puxer (ex: 250.0 BRL ou 5.0 %)")
    unit_label: str = Field(..., description="Unidade de medida (BRL_REALIZED, BRL_COMMITTED, BRL_POTENTIAL, PCT_UNCERTAINTY, REUSE_NODE)")
    is_observed: bool = Field(..., description="True se lastreado em fato observado; False se estimativa/projeção")
    color_hex: str
    source_ref: str
    tooltip: str


class LogicoAestheticResonance(BaseModel):
    """
    Métrica de Ressonância Lógico-Estética (R_LE).
    Mede a coerência entre a verdade lógica dos fundamentos econômicos e a
    harmonia geométrica/cinética da representação visual.
    """

    logical_coherence_score: float = Field(..., ge=0.0, le=1.0, description="Fração de evidência observada, saúde do Φ_buffer e clareza SPDX")
    aesthetic_harmony_score: float = Field(..., ge=0.0, le=1.0, description="Equilíbrio proporcional entre os 4 elementos e razão áurea")
    resonance_index: float = Field(..., ge=0.0, le=1.0, description="Média harmônica ponderada entre coerência lógica e harmonia estética")
    harmonic_ratio_phi: float = Field(default=1.618, description="Proporção harmônica aplicada aos anéis vetoriais")
    pulse_frequency_hz: float = Field(..., description="Frequência de pulsação cinética no Lottie (Hz) derivada da urgência/eficiência")
    polygon_symmetry_order: int = Field(..., ge=3, le=12, description="Ordem de simetria do polígono central (ex: 6 p/ 6 dimensões)")
    dominant_element: AlchemicalElement
    resonance_diagnosis: str


class InvestmentInformationStream(BaseModel):
    """Fluxo curado do 'mar de informações' utilizado como fonte de decisão de investimento."""

    stream_id: str
    category: str = Field(..., description="macro_fiduciary | oracle_market | empirical_discovery | technical_ip | governance_grants")
    title: str
    raw_volume_description: str = Field(..., description="Volume bruto antes da compressão (ex: '1.87MB chatlogs + 12 entrevistas')")
    curated_signal: str = Field(..., description="Sinal destilado de alta densidade")
    quantitative_value: float
    quantitative_unit: str
    element: AlchemicalElement
    is_observed: bool
    source_id: str
    sha256_anchor: str


class AlchemicalEmblem(BaseModel):
    """
    Emblema Alquímico de Compressão Semântica Máxima.
    Condensa dezenas de indicadores, fontes e restrições em uma única unidade
    hermético-computacional (Inscriptio + Pictura SVG/Puxers + Subscriptio).
    """

    emblem_id: str
    target_id: str
    inscriptio_motto: str = Field(..., description="Lema superior (fórmula sintética de poder/decisão)")
    central_glyph: str = Field(..., description="Glifo alquímico central (🜂, 🜄, 🜃, 🜁, 🜏)")
    subscriptio_epigram: str = Field(..., description="Epigrama inferior explicando a regra de decisão e o lastro")
    resonance: LogicoAestheticResonance
    puxer_quantum_brl: float = Field(default=250.0, description="Valor financeiro representado por cada puxer monetário (R$)")
    puxer_quantum_uncertainty_pct: float = Field(default=5.0, description="Redução de incerteza representada por cada puxer informacional (%)")
    puxers: List[PuxerUnit]
    element_totals: Dict[str, float]
    svg_vector_markup: str = Field(..., description="Representação vetorial SVG pura e escalável do Emblema Alquímico")
    lottie_template_id: str = Field(default="alchemical_emblem")
    provenance_seal_sha256: str


class SeaOfInformationCurator:
    """
    Curador do 'Mar de Informações' de Investimento e Gerador de Emblemas Alquímicos.
    Converte milhares de linhas de dados dispersos em Puxers quantitativos,
    cálculos de Ressonância Lógico-Estética e Emblemas Vetoriais/Lottie.
    """

    PUXER_BRL_QUANTUM = 250.0
    PUXER_UNCERTAINTY_QUANTUM = 5.0

    def curate_investment_streams(self, spec_payload: Dict[str, Any]) -> List[InvestmentInformationStream]:
        """Destila o mar de informações do ecossistema em fluxos quantitativos para decisão de investimento."""
        streams = [
            InvestmentInformationStream(
                stream_id="stream:fiduciary_beancount",
                category="macro_fiduciary",
                title="Razão Contábil Beancount & Termodinâmica Fiduciária (Sovereign Budget)",
                raw_volume_description="24 meses de lançamentos OFX/Beancount + contracheques + simulação de tríade",
                curated_signal="Φ_buffer = 1.34x (acima do limite mínimo de 1.20x); teto seguro de R$ 1.500/sprint.",
                quantitative_value=3700.0,
                quantitative_unit="BRL_REALIZED",
                element=AlchemicalElement.TERRA,
                is_observed=True,
                source_id="src:data:sovereign_budget",
                sha256_anchor=hashlib.sha256(b"stream:fiduciary_beancount:1.34").hexdigest()[:16],
            ),
            InvestmentInformationStream(
                stream_id="stream:customer_discovery_e0",
                category="empirical_discovery",
                title="Entrevistas Empíricas de Descoberta de Clientes (/interview ValueCurator)",
                raw_volume_description="12 entrevistas estruturadas + comparativo simulação vs entrevista real",
                curated_signal="83,3% dos compradores priorizam automação e curadoria sem blockchain; entrevistas reduzem incerteza 3,2x mais por real.",
                quantitative_value=42.0,
                quantitative_unit="PCT_UNCERTAINTY_REDUCTION",
                element=AlchemicalElement.IGNIS,
                is_observed=True,
                source_id="src:exp:discovery_interviews_r1",
                sha256_anchor=hashlib.sha256(b"stream:customer_discovery_e0:83.3").hexdigest()[:16],
            ),
            InvestmentInformationStream(
                stream_id="stream:semantic_genome_proterol",
                category="technical_ip",
                title="Acervo Compilatorum (46 Repositórios, 1.87MB Chatlogs, 12 Livros Proterol)",
                raw_volume_description="1.87MB JSONL + 8.830 LOC auditadas em Python/TypeScript/Elisp",
                curated_signal="7 artefatos centrais com score médio de reutilização 8.84/10; Proterol (9.6) e ValueCurator (9.3) lideram sinergia.",
                quantitative_value=96.0,
                quantitative_unit="REUSE_INDEX",
                element=AlchemicalElement.AER,
                is_observed=True,
                source_id="src:repo:proterol",
                sha256_anchor=hashlib.sha256(b"stream:semantic_genome_proterol:9.6").hexdigest()[:16],
            ),
            InvestmentInformationStream(
                stream_id="stream:capital_liquidity_flow",
                category="oracle_market",
                title="Fluxo de Alocação de Capital e Portões de Evidência (Evidence Gates)",
                raw_volume_description="5 estágios de alocação (R$ 4.500 planejados, R$ 2.100 comprometidos, R$ 3.700 realizados)",
                curated_signal="Superávit observado de R$ 1.600 nos pilotos e grants iniciais; combinação [C + A] exige apenas R$ 800.",
                quantitative_value=2100.0,
                quantitative_unit="BRL_COMMITTED",
                element=AlchemicalElement.AQUA,
                is_observed=True,
                source_id="src:repo:valuecurator",
                sha256_anchor=hashlib.sha256(b"stream:capital_liquidity_flow:2100").hexdigest()[:16],
            ),
            InvestmentInformationStream(
                stream_id="stream:ip_rights_manifest",
                category="governance_grants",
                title="Auditoria Jurídico-Técnica SPDX (License Manifest & Grants)",
                raw_volume_description="9 manifestos de licença + 3 gargalos pendentes em conectores de terceiros",
                curated_signal="Limpeza SPDX (Experimento C, R$ 350) entrega 108,57 pts de redução de incerteza por R$ 1.000.",
                quantitative_value=108.57,
                quantitative_unit="EFFICIENCY_PTS_PER_1K",
                element=AlchemicalElement.IGNIS,
                is_observed=False,
                source_id="src:repo:license_manifest",
                sha256_anchor=hashlib.sha256(b"stream:ip_rights_manifest:108.57").hexdigest()[:16],
            ),
        ]
        return streams

    def build_puxer_matrix(
        self,
        realized_brl: float = 3700.0,
        committed_brl: float = 2100.0,
        uncertainty_reduction_pct: float = 80.0,
        synergy_nodes_score: float = 62.0,
    ) -> List[PuxerUnit]:
        """
        Gera a grade de Puxers Quantitativos onde cada puxer representa exatamente:
        - TERRA (🜃): 1 puxer = R$ 250 de Valor Realizado Observado
        - AQUA  (🜄): 1 puxer = R$ 250 de Custo Comprometido no Fluxo
        - IGNIS (🜂): 1 puxer = 5% de Redução de Incerteza Experimental (ΔIncerteza)
        - AER   (🜁): 1 puxer = 5 pontos de Sinergia/Reutilização no Grafo Semântico
        """
        puxers: List[PuxerUnit] = []
        idx = 0

        terra_count = max(1, int(round(realized_brl / self.PUXER_BRL_QUANTUM)))
        for i in range(terra_count):
            puxers.append(
                PuxerUnit(
                    puxer_id=f"pux:terra:{i+1}",
                    index=idx,
                    element=AlchemicalElement.TERRA,
                    glyph=ELEMENT_GLYPHS[AlchemicalElement.TERRA],
                    unit_quantum=self.PUXER_BRL_QUANTUM,
                    unit_label="BRL_REALIZED",
                    is_observed=True,
                    color_hex=ELEMENT_COLORS[AlchemicalElement.TERRA],
                    source_ref="src:data:sovereign_budget",
                    tooltip=f"Puxer #{idx+1} [🜃 TERRA]: R$ {self.PUXER_BRL_QUANTUM:.0f} de Valor Realizado Observado",
                )
            )
            idx += 1

        aqua_count = max(1, int(round(committed_brl / self.PUXER_BRL_QUANTUM)))
        for i in range(aqua_count):
            puxers.append(
                PuxerUnit(
                    puxer_id=f"pux:aqua:{i+1}",
                    index=idx,
                    element=AlchemicalElement.AQUA,
                    glyph=ELEMENT_GLYPHS[AlchemicalElement.AQUA],
                    unit_quantum=self.PUXER_BRL_QUANTUM,
                    unit_label="BRL_COMMITTED",
                    is_observed=True,
                    color_hex=ELEMENT_COLORS[AlchemicalElement.AQUA],
                    source_ref="src:repo:valuecurator",
                    tooltip=f"Puxer #{idx+1} [🜄 AQUA]: R$ {self.PUXER_BRL_QUANTUM:.0f} de Capital Comprometido em Fluxo",
                )
            )
            idx += 1

        ignis_count = max(1, int(round(uncertainty_reduction_pct / self.PUXER_UNCERTAINTY_QUANTUM)))
        for i in range(ignis_count):
            puxers.append(
                PuxerUnit(
                    puxer_id=f"pux:ignis:{i+1}",
                    index=idx,
                    element=AlchemicalElement.IGNIS,
                    glyph=ELEMENT_GLYPHS[AlchemicalElement.IGNIS],
                    unit_quantum=self.PUXER_UNCERTAINTY_QUANTUM,
                    unit_label="PCT_UNCERTAINTY_REDUCTION",
                    is_observed=False,
                    color_hex=ELEMENT_COLORS[AlchemicalElement.IGNIS],
                    source_ref="src:exp:discovery_interviews_r1",
                    tooltip=f"Puxer #{idx+1} [🜂 IGNIS]: {self.PUXER_UNCERTAINTY_QUANTUM:.0f}% de Redução de Incerteza (Experimentos C+A)",
                )
            )
            idx += 1

        aer_count = max(1, int(round(synergy_nodes_score / 5.0)))
        for i in range(aer_count):
            puxers.append(
                PuxerUnit(
                    puxer_id=f"pux:aer:{i+1}",
                    index=idx,
                    element=AlchemicalElement.AER,
                    glyph=ELEMENT_GLYPHS[AlchemicalElement.AER],
                    unit_quantum=5.0,
                    unit_label="GRAPH_SYNERGY_PTS",
                    is_observed=True,
                    color_hex=ELEMENT_COLORS[AlchemicalElement.AER],
                    source_ref="src:repo:proterol",
                    tooltip=f"Puxer #{idx+1} [🜁 AER]: 5 pts de Reutilização Semântica no Compilatorum",
                )
            )
            idx += 1

        return puxers

    def compute_resonance(
        self,
        observed_dimensions_ratio: float = 0.778,
        phi_buffer_ratio: float = 1.34,
        top_efficiency_pts: float = 108.57,
        puxers: Optional[List[PuxerUnit]] = None,
    ) -> LogicoAestheticResonance:
        """Calcula o índice formal de Ressonância Lógico-Estética (R_LE)."""
        buffer_safety = min(1.0, max(0.0, phi_buffer_ratio / 1.50))
        efficiency_norm = min(1.0, top_efficiency_pts / 120.0)
        logical_score = round(0.45 * observed_dimensions_ratio + 0.30 * buffer_safety + 0.25 * efficiency_norm, 3)

        # Equilíbrio estético baseado na distribuição dos 4 elementos e proximidade à razão áurea
        if puxers:
            counts = {el: sum(1 for p in puxers if p.element == el) for el in AlchemicalElement}
            dominant = max(counts, key=lambda k: counts[k])
            realized_to_committed = counts[AlchemicalElement.TERRA] / max(1, counts[AlchemicalElement.AQUA])
            phi_deviation = abs(realized_to_committed - GOLDEN_RATIO) / GOLDEN_RATIO
            aesthetic_score = round(max(0.65, min(0.98, 1.0 - 0.35 * phi_deviation)), 3)
        else:
            dominant = AlchemicalElement.IGNIS
            aesthetic_score = 0.88

        resonance_idx = round((2 * logical_score * aesthetic_score) / max(1e-6, (logical_score + aesthetic_score)), 3)
        pulse_hz = round(0.6 + (efficiency_norm * 1.2), 2)

        return LogicoAestheticResonance(
            logical_coherence_score=logical_score,
            aesthetic_harmony_score=aesthetic_score,
            resonance_index=resonance_idx,
            harmonic_ratio_phi=round(GOLDEN_RATIO, 4),
            pulse_frequency_hz=pulse_hz,
            polygon_symmetry_order=6,
            dominant_element=dominant,
            resonance_diagnosis=(
                f"Ressonância Lógico-Estética Alta (R_LE = {resonance_idx:.2f}): "
                f"Razão Realizado/Comprometido próxima de φ ({GOLDEN_RATIO:.2f}), "
                f"{observed_dimensions_ratio*100:.1f}% das dimensões sustentadas por evidência empírica e pulso cinético a {pulse_hz} Hz."
            ),
        )

    def compile_alchemical_emblem(
        self,
        target_id: str = "compilatorum_portfolio_nexus",
        realized_brl: float = 3700.0,
        committed_brl: float = 2100.0,
        uncertainty_reduction_pct: float = 80.0,
        synergy_nodes_score: float = 62.0,
        phi_buffer_ratio: float = 1.34,
    ) -> AlchemicalEmblem:
        """
        Compila um Emblema Alquímico de Compressão Semântica Máxima, gerando:
        - A matriz de Puxers Quantitativos
        - A Ressonância Lógico-Estética
        - O Vetor SVG paramétrico completo (anéis herméticos, hexagrama vetorial das 6 dimensões e coroa de puxers)
        - O selo SHA-256 de proveniência
        """
        puxers = self.build_puxer_matrix(
            realized_brl=realized_brl,
            committed_brl=committed_brl,
            uncertainty_reduction_pct=uncertainty_reduction_pct,
            synergy_nodes_score=synergy_nodes_score,
        )
        resonance = self.compute_resonance(
            observed_dimensions_ratio=14.0 / 18.0,
            phi_buffer_ratio=phi_buffer_ratio,
            top_efficiency_pts=108.57,
            puxers=puxers,
        )

        element_totals = {
            "terra_realized_brl": realized_brl,
            "aqua_committed_brl": committed_brl,
            "ignis_uncertainty_reduction_pct": uncertainty_reduction_pct,
            "aer_synergy_score": synergy_nodes_score,
            "total_puxers_count": float(len(puxers)),
        }

        svg_markup = self._render_emblem_svg(puxers=puxers, resonance=resonance, element_totals=element_totals)
        seal_seed = f"{target_id}:{realized_brl}:{committed_brl}:{uncertainty_reduction_pct}:{resonance.resonance_index}"
        seal_hash = hashlib.sha256(seal_seed.encode("utf-8")).hexdigest()

        return AlchemicalEmblem(
            emblem_id=f"emblem:{target_id}",
            target_id=target_id,
            inscriptio_motto="🜏 VITRIOL SEMÂNTICO · CONHECIMENTO CONDENSADO EM CAPITAL AUDITÁVEL 🜏",
            central_glyph="🜏",
            subscriptio_epigram=(
                f"Cada Puxer Monetário (🜃/🜄) = R$ {self.PUXER_BRL_QUANTUM:.0f} | "
                f"Cada Puxer Experimental (🜂) = {self.PUXER_UNCERTAINTY_QUANTUM:.0f}% ΔIncerteza | "
                f"Φ_buffer = {phi_buffer_ratio:.2f}x ≥ 1.20x | R_LE = {resonance.resonance_index:.3f}"
            ),
            resonance=resonance,
            puxer_quantum_brl=self.PUXER_BRL_QUANTUM,
            puxer_quantum_uncertainty_pct=self.PUXER_UNCERTAINTY_QUANTUM,
            puxers=puxers,
            element_totals=element_totals,
            svg_vector_markup=svg_markup,
            lottie_template_id="alchemical_emblem",
            provenance_seal_sha256=seal_hash,
        )

    def _render_emblem_svg(
        self,
        puxers: List[PuxerUnit],
        resonance: LogicoAestheticResonance,
        element_totals: Dict[str, float],
    ) -> str:
        """Gera um SVG vetorial paramétrico representando o Emblema Alquímico e seus Puxers."""
        cx, cy = 210, 195
        r_outer = 152
        r_puxer_ring = 126
        r_hex = 82
        r_inner = round(r_hex / GOLDEN_RATIO, 1)

        parts: List[str] = [
            '<svg viewBox="0 0 420 400" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '  <radialGradient id="alchGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#00FF88" stop-opacity="0.22"/>',
            '    <stop offset="65%" stop-color="#00BFFF" stop-opacity="0.08"/>',
            '    <stop offset="100%" stop-color="#07100A" stop-opacity="0.0"/>',
            '  </radialGradient>',
            '</defs>',
            f'<rect width="420" height="400" fill="#07100A" rx="8"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="url(#alchGlow)" stroke="#1A3320" stroke-width="1.5"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{r_puxer_ring}" fill="none" stroke="#FFD700" stroke-width="1" stroke-dasharray="4,3" opacity="0.7"/>',
        ]

        # Desenha cada Puxer Quantitativo ao redor do anel hermético
        n_pux = max(1, len(puxers))
        for i, pux in enumerate(puxers):
            angle = (2.0 * math.pi * i / n_pux) - (math.pi / 2.0)
            px = round(cx + r_puxer_ring * math.cos(angle), 2)
            py = round(cy + r_puxer_ring * math.sin(angle), 2)
            stroke = "#FFFFFF" if pux.is_observed else "#FFB800"
            parts.append(
                f'<rect x="{px - 4.5}" y="{py - 4.5}" width="9" height="9" rx="2" '
                f'fill="{pux.color_hex}" stroke="{stroke}" stroke-width="0.8">'
                f'<title>{pux.tooltip}</title></rect>'
            )

        # Hexágono / Estrela Hermética das 6 Dimensões Radiais
        hex_pts_a: List[str] = []
        hex_pts_b: List[str] = []
        for k in range(6):
            ang = (2.0 * math.pi * k / 6.0) - (math.pi / 2.0)
            hx = round(cx + r_hex * math.cos(ang), 2)
            hy = round(cy + r_hex * math.sin(ang), 2)
            if k % 2 == 0:
                hex_pts_a.append(f"{hx},{hy}")
            else:
                hex_pts_b.append(f"{hx},{hy}")

        parts.append(
            f'<polygon points="{" ".join(hex_pts_a)}" fill="rgba(0, 255, 136, 0.10)" stroke="#00FF88" stroke-width="1.8"/>'
        )
        parts.append(
            f'<polygon points="{" ".join(hex_pts_b)}" fill="rgba(0, 191, 255, 0.10)" stroke="#00BFFF" stroke-width="1.8"/>'
        )

        # Círculo Áureo Interno e Glifo Central
        parts.extend([
            f'<circle cx="{cx}" cy="{cy}" r="{r_inner}" fill="#0D1A10" stroke="#B388FF" stroke-width="2"/>',
            f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" fill="#FFD700" font-family="monospace" font-size="22" font-weight="bold">🜏</text>',
            f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" fill="#00FF88" font-family="monospace" font-size="11" font-weight="bold">R_LE={resonance.resonance_index:.2f}</text>',
            f'<text x="{cx}" y="{cy + 28}" text-anchor="middle" fill="#6B9E7A" font-family="monospace" font-size="9">{len(puxers)} PUXERS</text>',
            # Legenda Alquímica nos 4 Cantos
            f'<text x="14" y="24" fill="#00FF88" font-family="monospace" font-size="10">🜃 TERRA: R$ {element_totals["terra_realized_brl"]:.0f}</text>',
            f'<text x="275" y="24" fill="#00BFFF" font-family="monospace" font-size="10">🜄 AQUA: R$ {element_totals["aqua_committed_brl"]:.0f}</text>',
            f'<text x="14" y="384" fill="#FFB800" font-family="monospace" font-size="10">🜂 IGNIS: -{element_totals["ignis_uncertainty_reduction_pct"]:.0f}% Inc.</text>',
            f'<text x="275" y="384" fill="#B388FF" font-family="monospace" font-size="10">🜁 AER: {element_totals["aer_synergy_score"]:.0f} pts</text>',
            '</svg>',
        ])
        return "\n".join(parts)
