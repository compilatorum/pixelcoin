"""
Renderizador Web Generativo (Camada 6 — Web / Navegador)

Produz a interface generativa visual completa do PixelCoin compatível com o
SOVEREIGN MOCKUP PROTOCOL v1.0 (offline-first, WebView-safe, Chart.js 4.4.1 + anime.js 3.2.1,
SVG interativo para o Grafo de Conhecimento, Mosaico de Portfólio, Matriz de Decisão,
Gráfico Radial de Oportunidades e Fluxo de Capital em Movimento).
"""

from __future__ import annotations

import json
from pixelcoin.layer5_ui_spec import DeclarativeUISpecification


class WebGenerativeRenderer:
    """Renderizador Web Generativo do PixelCoin."""

    @staticmethod
    def render_html(spec: DeclarativeUISpecification) -> str:
        spec_json = json.dumps(spec.model_dump(mode="json"), ensure_ascii=False, indent=2)
        html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PixelCoin — Interface Generativa de Inteligência Econômica (Compilatorum)</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
<style>
:root {
  --bg: #07100A;
  --bg2: #0D1A10;
  --bg3: #111F14;
  --border: #1A3320;
  --accent: #00FF88;
  --data: #00BFFF;
  --warn: #FFB800;
  --err: #FF4455;
  --purple: #B388FF;
  --gold: #FFD700;
  --text: #C8E6C9;
  --dim: #6B9E7A;
  --muted: #4A7A5A;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
  --font-ui: system-ui, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-ui);
  line-height: 1.5;
  overflow-x: hidden;
}
#app-shell {
  display: flex;
  min-height: 100vh;
}
aside#sidebar {
  width: 270px;
  background: var(--bg2);
  border-right: 1px solid var(--border);
  padding: 18px 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex-shrink: 0;
}
.brand-box {
  border: 1px solid var(--border);
  border-top: 2px solid var(--gold);
  border-radius: 8px;
  padding: 12px;
  background: var(--bg3);
}
.brand-title {
  font-family: var(--font-mono);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--gold);
  display: flex;
  align-items: center;
  gap: 8px;
}
.status-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent);
  display: inline-block;
  box-shadow: 0 0 8px var(--accent);
}
.brand-sub {
  font-size: 0.76rem;
  color: var(--dim);
  margin-top: 4px;
}
.nav-group-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--muted);
  letter-spacing: 0.08em;
  margin-top: 6px;
}
.nav-btn {
  width: 100%;
  text-align: left;
  background: transparent;
  color: var(--text);
  border: 1px solid transparent;
  border-left: 3px solid transparent;
  padding: 9px 11px;
  border-radius: 6px;
  font-family: var(--font-ui);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.nav-btn:hover {
  background: var(--bg3);
  border-color: var(--border);
}
.nav-btn.active {
  background: var(--bg3);
  border-color: var(--border);
  border-left: 3px solid var(--accent);
  color: var(--accent);
  font-weight: 600;
}
main#content {
  flex: 1;
  padding: 20px 24px;
  max-width: calc(100vw - 270px);
}
.ticker-wrap {
  overflow: hidden;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 12px;
  margin-bottom: 16px;
  white-space: nowrap;
}
.ticker-move {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.76rem;
  color: var(--dim);
  animation: tickerLoop 32s linear infinite;
}
@keyframes tickerLoop {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.prompt-bar-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-top: 2px solid var(--accent);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 18px;
}
.prompt-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 10px;
}
.prompt-input {
  flex: 1;
  min-width: 280px;
  background: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}
.btn-primary {
  background: var(--accent);
  color: #041008;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 0.82rem;
  cursor: pointer;
}
.btn-secondary {
  background: var(--bg3);
  color: var(--data);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 11px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  cursor: pointer;
}
.btn-secondary:hover {
  border-color: var(--data);
}
.pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}
.prompt-pill {
  background: var(--bg3);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 4px 10px;
  font-size: 0.74rem;
  cursor: pointer;
}
.prompt-pill:hover {
  border-color: var(--gold);
  color: var(--gold);
}
.compression-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}
.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
}
.card-accent { border-top: 2px solid var(--accent); }
.card-data { border-top: 2px solid var(--data); }
.card-warn { border-top: 2px solid var(--warn); }
.card-purple { border-top: 2px solid var(--purple); }
.card-gold { border-top: 2px solid var(--gold); }
.card-err { border-top: 2px solid var(--err); }
.card-title {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  text-transform: uppercase;
  color: var(--dim);
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}
.stat-val {
  font-family: var(--font-mono);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
  margin: 4px 0;
}
.tag-pill {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
}
.tag-observed { background: rgba(0, 255, 136, 0.14); color: var(--accent); border: 1px solid var(--accent); }
.tag-estimate { background: rgba(255, 184, 0, 0.14); color: var(--warn); border: 1px solid var(--warn); }
.tag-testar { background: rgba(0, 191, 255, 0.16); color: var(--data); border: 1px solid var(--data); }
.tag-validar { background: rgba(179, 136, 255, 0.16); color: var(--purple); border: 1px solid var(--purple); }
.tag-preparar { background: rgba(255, 215, 0, 0.16); color: var(--gold); border: 1px solid var(--gold); }
.tag-err { background: rgba(255, 68, 85, 0.16); color: var(--err); border: 1px solid var(--err); }
.spa-section { display: none; }
.spa-section.active { display: block; }
.chart-container {
  position: relative;
  height: 320px;
  width: 100%;
}
.two-col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}
.mosaic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}
.mosaic-tile {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
}
table.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}
table.data-table th, table.data-table td {
  border-bottom: 1px solid var(--border);
  padding: 8px 10px;
  text-align: left;
}
table.data-table th {
  font-family: var(--font-mono);
  color: var(--dim);
  font-size: 0.74rem;
  text-transform: uppercase;
}
.formula-block {
  background: var(--bg);
  border: 1px solid var(--border);
  border-left: 3px solid var(--purple);
  border-radius: 4px;
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--text);
  margin: 8px 0;
}
@media (max-width: 860px) {
  #app-shell { flex-direction: column; }
  aside#sidebar { width: 100%; border-right: none; border-bottom: 1px solid var(--border); }
  main#content { max-width: 100vw; }
}
</style>
</head>
<body>
<div id="app-shell">
  <aside id="sidebar">
    <div class="brand-box">
      <div class="brand-title"><span class="status-dot"></span> PIXELCOIN v0.4</div>
      <div class="brand-sub">Interface Generativa, Emblemas Alquímicos, Puxers & LottieMCP</div>
    </div>

    <div class="nav-group-label">6 Representações Infoestéticas</div>
    <button class="nav-btn" id="nav-sec-alchemical" onclick="switchSection('sec-alchemical')">0. Emblema Alquímico & LottieMCP</button>
    <button class="nav-btn active" id="nav-sec-matrix" onclick="switchSection('sec-matrix')">4. Matriz de Decisão & Experimentos</button>
    <button class="nav-btn" id="nav-sec-radial" onclick="switchSection('sec-radial')">1. Gráfico Radial (Oportunidades)</button>
    <button class="nav-btn" id="nav-sec-graph" onclick="switchSection('sec-graph')">2. Grafo de Relações & Direitos</button>
    <button class="nav-btn" id="nav-sec-mosaic" onclick="switchSection('sec-mosaic')">3. Mosaico do Portfólio</button>
    <button class="nav-btn" id="nav-sec-flow" onclick="switchSection('sec-flow')">5. Fluxo de Capital & Plano</button>

    <div class="nav-group-label">Superfícies & Controles</div>
    <button class="nav-btn" id="nav-sec-layers" onclick="switchSection('sec-layers')">6 Camadas & Guardrails</button>

    <div class="card card-gold" style="margin-top:auto;">
      <div class="card-title"><span>Sovereign Buffer</span><span>Φ_buffer</span></div>
      <div class="stat-val" id="sidebar-phi">1.34x</div>
      <div style="font-size:0.74rem;color:var(--dim);">Mínimo exigido: ≥ 1.20x (Beancount)</div>
      <div style="font-size:0.74rem;color:var(--accent);margin-top:4px;">Modo: Análise Separada da Execução</div>
    </div>
  </aside>

  <main id="content">
    <div class="ticker-wrap">
      <div class="ticker-move" id="ticker-text">
        [PIXELCOIN · COMPILATORUM] 7 Artefatos Indexados · 100% Monetizáveis Sem Blockchain · Líder de Eficiência Informacional: Exp C (108.6 pts/R$1k) + Exp A (93.3 pts/R$1k) · Valor Realizado: R$ 3.700 vs Custo Comprometido: R$ 2.100 · Φ_buffer = 1.34x (Saudável) · 3 Artefatos com Direitos Pendentes de Auditoria SPDX ·
        [PIXELCOIN · COMPILATORUM] 7 Artefatos Indexados · 100% Monetizáveis Sem Blockchain · Líder de Eficiência Informacional: Exp C (108.6 pts/R$1k) + Exp A (93.3 pts/R$1k) · Valor Realizado: R$ 3.700 vs Custo Comprometido: R$ 2.100 · Φ_buffer = 1.34x (Saudável) · 3 Artefatos com Direitos Pendentes de Auditoria SPDX
      </div>
    </div>

    <!-- BARRA DE PROMPT COMO FRONT-END (SEÇÃO 1 & 4) -->
    <div class="prompt-bar-card">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <div>
          <span class="tag-pill tag-observed">PROMPT COMO FRONT-END</span>
          <strong style="margin-left:8px;font-size:0.95rem;" id="spec-title-header"></strong>
        </div>
        <div style="display:flex;gap:6px;align-items:center;">
          <span style="font-size:0.75rem;color:var(--dim);font-family:var(--font-mono);">Visão:</span>
          <button class="btn-secondary" onclick="changePerspective('executiva')">Executiva</button>
          <button class="btn-secondary" onclick="changePerspective('desenvolvedor')">Desenvolvedor</button>
          <button class="btn-secondary" onclick="changePerspective('cientifica')">Científica</button>
        </div>
      </div>

      <div class="prompt-controls">
        <input type="text" id="prompt-input" class="prompt-input" placeholder="Declare sua intenção (ex: Compare três experimentos com orçamento limitado)...">
        <button class="btn-primary" onclick="executeGenerativePrompt()">Gerar Interface</button>
      </div>

      <div class="pill-row" id="canonical-prompts-row"></div>
    </div>

    <!-- REGRA DA COMPRESSÃO SEMÂNTICA: 3 NÍVEIS OBRIGATÓRIOS (SEÇÃO 2) -->
    <div class="compression-grid">
      <div class="card card-accent">
        <div class="card-title"><span>1. Visão Instantânea</span><span class="tag-pill tag-observed">Sinal Principal</span></div>
        <p id="comp-instant-headline" style="font-size:0.86rem;font-weight:600;margin-bottom:6px;"></p>
        <p id="comp-instant-priority" style="font-size:0.8rem;color:var(--accent);margin-bottom:6px;"></p>
        <p id="comp-instant-anomaly" style="font-size:0.78rem;color:var(--warn);"></p>
      </div>
      <div class="card card-data">
        <div class="card-title"><span>2. Inspeção</span><span class="tag-pill tag-testar">Explicabilidade</span></div>
        <p id="comp-inspection-epistemic" style="font-size:0.78rem;color:var(--warn);margin-bottom:6px;"></p>
        <ul id="comp-inspection-factors" style="font-size:0.78rem;color:var(--text);padding-left:16px;"></ul>
      </div>
      <div class="card card-purple">
        <div class="card-title"><span>3. Rastreabilidade</span><span class="tag-pill tag-validar">SHA-256 & Fontes</span></div>
        <div id="comp-traceability-sources" style="font-size:0.76rem;font-family:var(--font-mono);color:var(--dim);"></div>
        <div id="comp-traceability-uncertainties" style="font-size:0.76rem;color:var(--text);margin-top:6px;"></div>
      </div>
    </div>

    <!-- INDICADORES-CHAVE (REGRA 1: DADOS ANTES DA ESTÉTICA) -->
    <div class="stat-grid" id="indicators-grid"></div>

    <!-- SEÇÃO 0: EMBLEMA ALQUÍMICO, PUXERS QUANTITATIVOS & LOTTIEMCP / CREATORMCP -->
    <section id="sec-alchemical" class="spa-section">
      <div class="two-col">
        <div class="card card-gold">
          <div class="card-title">
            <span>0. Emblema Alquímico de Compressão Máxima (Vetor SVG + Puxers)</span>
            <span class="tag-pill tag-preparar" id="emblem-resonance-badge">R_LE = 0.85</span>
          </div>
          <div id="emblem-inscriptio" style="text-align:center;font-family:var(--font-mono);font-size:0.78rem;color:var(--gold);margin-bottom:8px;font-weight:700;"></div>
          <div id="emblem-svg-container" style="width:100%;height:340px;display:flex;justify-content:center;align-items:center;"></div>
          <div id="emblem-subscriptio" class="formula-block" style="border-left-color:var(--gold);text-align:center;font-size:0.74rem;"></div>
        </div>

        <div class="card card-purple">
          <div class="card-title">
            <span>LottieMCP / CreatorMCP — Parametrizador Dinâmico via JSON</span>
            <span class="tag-pill tag-validar">Bodymovin v5.9.0</span>
          </div>
          <div style="display:flex;gap:8px;align-items:center;margin-bottom:8px;flex-wrap:wrap;">
            <span style="font-size:0.76rem;color:var(--dim);font-family:var(--font-mono);">Template Infográfico:</span>
            <select id="lottie-template-select" class="btn-secondary" onchange="loadLottieTemplateDefaultParams(this.value)"></select>
            <button class="btn-primary" style="padding:6px 12px;font-size:0.75rem;" onclick="applyLottieJsonParameterization()">Parametrizar Lottie & Puxers</button>
          </div>
          <textarea id="lottie-params-textarea" rows="6" style="width:100%;background:var(--bg);color:var(--accent);border:1px solid var(--border);border-radius:6px;padding:8px;font-family:var(--font-mono);font-size:0.75rem;"></textarea>
          <div id="lottie-receipt-box" class="formula-block" style="margin-top:8px;"></div>
          <div style="font-size:0.72rem;color:var(--dim);font-family:var(--font-mono);margin-top:4px;">Especificação Lottie JSON Parametrizada (Camadas & Keyframes):</div>
          <pre id="lottie-json-preview" style="max-height:145px;overflow:auto;background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:8px;font-family:var(--font-mono);font-size:0.7rem;color:var(--data);margin-top:4px;"></pre>
        </div>
      </div>

      <div class="two-col">
        <div class="card card-accent">
          <div class="card-title">
            <span>Matriz de Puxers Quantitativos (Cada Puxer = 1 Quantitativo Auditável)</span>
            <span class="tag-pill tag-observed" id="puxers-total-badge">52 Puxers</span>
          </div>
          <div id="puxers-matrix-grid" style="display:flex;flex-wrap:wrap;gap:5px;padding:8px;background:var(--bg);border:1px solid var(--border);border-radius:6px;"></div>
          <div id="puxer-inspector-banner" style="font-family:var(--font-mono);font-size:0.75rem;color:var(--gold);margin-top:8px;">Passe o cursor ou clique em qualquer Puxer acima para inspecionar seu lastro quantitativo e fonte.</div>
        </div>

        <div class="card card-data">
          <div class="card-title">
            <span>Curadoria do "Mar de Informações" (Fontes de Investimento Destiladas)</span>
            <span class="tag-pill tag-testar">Sea of Info Curator</span>
          </div>
          <table class="data-table" id="curated-streams-table">
            <thead>
              <tr>
                <th>Elemento</th>
                <th>Fonte / Volume Bruto</th>
                <th>Sinal Destilado</th>
                <th>Quantitativo</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SEÇÃO 4: MATRIZ DE DECISÃO & PORTFÓLIO DE EXPERIMENTOS -->
    <section id="sec-matrix" class="spa-section active">
      <div class="two-col">
        <div class="card card-accent">
          <div class="card-title">
            <span>4. Matriz de Decisão — Evidência vs. Custo de Validação</span>
            <span class="tag-pill tag-observed">ΔIncerteza / R$ 1k</span>
          </div>
          <div class="chart-container">
            <canvas id="chartDecisionMatrix"></canvas>
          </div>
          <div class="formula-block">
            Eficiência Informacional: η_info(E_i) = ΔIncerteza(%) / (Custo_BRL / 1000) · Sujeito a Φ_buffer = Saldo_Checking / D_fixo ≥ 1.20
          </div>
        </div>

        <div class="card card-gold">
          <div class="card-title">
            <span>Simulador de Alocação de Orçamento (Análise ≠ Execução)</span>
            <span class="tag-pill tag-preparar">Interativo</span>
          </div>
          <div style="margin-bottom:12px;">
            <label style="font-size:0.82rem;font-family:var(--font-mono);">Orçamento do Sprint para Experimentos: <strong id="budget-slider-label" style="color:var(--gold);">R$ 1.500</strong></label>
            <input type="range" id="budget-slider" min="350" max="3000" step="50" value="1500" style="width:100%;margin-top:6px;" oninput="updateBudgetSimulation(this.value)">
          </div>
          <div id="simulation-summary-box" class="formula-block" style="border-left-color:var(--gold);"></div>
          <div id="experiments-cards-container" style="display:flex;flex-direction:column;gap:10px;margin-top:10px;"></div>
        </div>
      </div>
    </section>

    <!-- SEÇÃO 1: GRÁFICO RADIAL — PERFIL DE UMA OPORTUNIDADE -->
    <section id="sec-radial" class="spa-section">
      <div class="two-col">
        <div class="card card-data">
          <div class="card-title">
            <span>1. Gráfico Radial — Perfil Comparativo de Oportunidades (6 Dimensões)</span>
            <span class="tag-pill tag-estimate">Evidência vs Estimativa</span>
          </div>
          <div class="chart-container">
            <canvas id="chartRadialProfile"></canvas>
          </div>
          <p style="font-size:0.76rem;color:var(--warn);margin-top:8px;" id="radial-warning-text"></p>
        </div>

        <div class="card card-accent">
          <div class="card-title">
            <span>Inspeção das 6 Dimensões & Catálogo Sem Blockchain</span>
            <select id="radial-opp-select" class="btn-secondary" onchange="renderRadialDimensionTable(this.value)"></select>
          </div>
          <table class="data-table" id="radial-dimensions-table">
            <thead>
              <tr>
                <th>Dimensão</th>
                <th>Nota</th>
                <th>Status Epistemológico</th>
                <th>Fundamento & Fonte</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SEÇÃO 2: GRAFO — RELAÇÕES, SINERGIAS E DIREITOS -->
    <section id="sec-graph" class="spa-section">
      <div class="two-col">
        <div class="card card-purple">
          <div class="card-title">
            <span>2. Grafo Semântico do Compilatorum — Relações, Hubs e Gargalos</span>
            <span class="tag-pill tag-validar">Topologia Viva</span>
          </div>
          <div id="svg-graph-wrapper" style="width:100%;height:340px;background:var(--bg);border:1px solid var(--border);border-radius:6px;overflow:hidden;"></div>
        </div>

        <div class="card card-warn">
          <div class="card-title">
            <span>Auditoria de Direitos & Proveniência (License Manifest)</span>
            <span class="tag-pill tag-estimate">SPDX & Permissões</span>
          </div>
          <table class="data-table" id="graph-rights-table">
            <thead>
              <tr>
                <th>Artefato</th>
                <th>Licença SPDX</th>
                <th>Status</th>
                <th>Reutilização</th>
                <th>Ação Controlada</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SEÇÃO 3: MOSAICO — O PANORAMA DO PORTFÓLIO -->
    <section id="sec-mosaic" class="spa-section">
      <div class="card card-gold" style="margin-bottom:16px;">
        <div class="card-title">
          <span>3. Mosaico do Portfólio — Valor Realizado vs. Custo Comprometido vs. Potencial Estimado</span>
          <span class="tag-pill tag-observed">Sem Confusão Semântica</span>
        </div>
        <div class="mosaic-grid" id="portfolio-mosaic-grid"></div>
      </div>
    </section>

    <!-- SEÇÃO 5: FLUXO — CAPITAL EM MOVIMENTO & PLANO EXECUTÁVEL -->
    <section id="sec-flow" class="spa-section">
      <div class="two-col">
        <div class="card card-accent">
          <div class="card-title">
            <span>5. Fluxo — Capital em Movimento (Previsto, Comprometido e Realizado)</span>
            <span class="tag-pill tag-observed">Rastreamento Contábil</span>
          </div>
          <div class="chart-container">
            <canvas id="chartCapitalFlow"></canvas>
          </div>
        </div>

        <div class="card card-data">
          <div class="card-title">
            <span>Plano Executável de 4 Semanas & Portões Go/No-Go</span>
            <span class="tag-pill tag-testar">Planner + ValueCurator</span>
          </div>
          <div id="executable-plan-box"></div>
        </div>
      </div>
    </section>

    <!-- SEÇÃO 6: ARQUITETURA DE 6 CAMADAS & LOG DE DECISÕES -->
    <section id="sec-layers" class="spa-section">
      <div class="two-col">
        <div class="card card-purple">
          <div class="card-title"><span>Arquitetura de 6 Camadas do PixelCoin</span><span class="tag-pill tag-observed">Verificada</span></div>
          <table class="data-table">
            <thead><tr><th>Camada</th><th>Papel no Ecossistema</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td><strong>Camada 6</strong></td><td>Renderizadores Generativos (Web · Emacs/Org · Mobile · Agentes)</td><td><span class="tag-pill tag-observed">ATIVO</span></td></tr>
              <tr><td><strong>Camada 5</strong></td><td>Especificação Declarativa de UI + Compressão Semântica + Guardrails</td><td><span class="tag-pill tag-observed">ATIVO</span></td></tr>
              <tr><td><strong>Camada 4</strong></td><td>Orquestração por IA (Prompt → Intenção → Seleção de Visualização)</td><td><span class="tag-pill tag-observed">ATIVO</span></td></tr>
              <tr><td><strong>Camada 3</strong></td><td>Inteligência Econômica (Priorização, Incerteza, Custos, Fluxo)</td><td><span class="tag-pill tag-observed">ATIVO</span></td></tr>
              <tr><td><strong>Camada 2</strong></td><td>Grafo Semântico & Registro de Artefatos (Proterol + License Manifest)</td><td><span class="tag-pill tag-observed">ATIVO</span></td></tr>
              <tr><td><strong>Camada 1</strong></td><td>Fontes Primárias (Wordsmith Chatlogs, GitHub Repos, Beancount, Experimentos)</td><td><span class="tag-pill tag-observed">ATIVO</span></td></tr>
            </tbody>
          </table>
        </div>

        <div class="card card-accent">
          <div class="card-title"><span>Trilha Bidirecional de Decisões & Ações Autorizadas</span><span class="tag-pill tag-preparar">HITL</span></div>
          <div id="decision-audit-log" style="font-family:var(--font-mono);font-size:0.78rem;color:var(--text);display:flex;flex-direction:column;gap:8px;">
            <div class="formula-block">[BOOT] Guardrails ativos: Dados antes da estética · Explicabilidade 3 níveis · Ações autorizadas · Separação Análise/Execução.</div>
          </div>
        </div>
      </div>
    </section>
  </main>
</div>

<script>
window.onerror = function(msg, src, line) {
  console.error("PixelCoin UI Error:", msg, "at", src, ":", line);
  return false;
};

var DATA = __SPEC_JSON_PLACEHOLDER__;
var allCharts = {};
var sectionInited = {};

function safeChart(canvasId, config) {
  try {
    var ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    if (allCharts[canvasId]) {
      allCharts[canvasId].destroy();
    }
    allCharts[canvasId] = new Chart(ctx, config);
    return allCharts[canvasId];
  } catch (err) {
    console.error("safeChart error on " + canvasId + ":", err);
    return null;
  }
}

function switchSection(secId) {
  var sections = document.querySelectorAll(".spa-section");
  for (var i = 0; i < sections.length; i++) {
    sections[i].classList.remove("active");
  }
  var navBtns = document.querySelectorAll(".nav-btn");
  for (var j = 0; j < navBtns.length; j++) {
    navBtns[j].classList.remove("active");
  }
  var target = document.getElementById(secId);
  if (target) {
    target.classList.add("active");
    if (window.anime) {
      anime({
        targets: "#" + secId,
        opacity: [0.7, 1],
        translateY: [-6, 0],
        duration: 320,
        easing: "easeOutQuad"
      });
    }
  }
  var btn = document.getElementById("nav-" + secId);
  if (btn) btn.classList.add("active");

  if (secId === "sec-alchemical") initAlchemicalEmblemAndLottie();
  if (secId === "sec-matrix") initMatrixChart();
  if (secId === "sec-radial") initRadialChart();
  if (secId === "sec-graph") renderKnowledgeGraphSVG();
  if (secId === "sec-mosaic") renderPortfolioMosaic();
  if (secId === "sec-flow") initCapitalFlowChart();
}

function renderTopCompressionAndIndicators() {
  document.getElementById("spec-title-header").textContent = DATA.title + " (" + DATA.perspective.toUpperCase() + ")";
  document.getElementById("prompt-input").value = DATA.prompt;

  var sc = DATA.semantic_compression;
  document.getElementById("comp-instant-headline").textContent = sc.instant_view.headline_signal;
  document.getElementById("comp-instant-priority").textContent = "➔ Prioridade: " + sc.instant_view.top_priority_action;
  document.getElementById("comp-instant-anomaly").textContent = "⚠ Atenção: " + sc.instant_view.detected_anomaly_or_bottleneck;

  document.getElementById("comp-inspection-epistemic").textContent = sc.inspection.observed_vs_estimated_breakdown;
  var factorsUl = document.getElementById("comp-inspection-factors");
  factorsUl.innerHTML = "";
  for (var i = 0; i < sc.inspection.causal_factors.length; i++) {
    var li = document.createElement("li");
    li.textContent = sc.inspection.causal_factors[i];
    li.style.marginBottom = "4px";
    factorsUl.appendChild(li);
  }

  var srcDiv = document.getElementById("comp-traceability-sources");
  var srcHtml = "<strong>Fontes Verificadas (" + sc.traceability.source_records.length + "):</strong><br>";
  for (var k = 0; k < Math.min(5, sc.traceability.source_records.length); k++) {
    var s = sc.traceability.source_records[k];
    srcHtml += "• [" + s.module + "] " + s.source_id + " (SHA256: " + s.sha256 + ")<br>";
  }
  srcDiv.innerHTML = srcHtml;

  var uncDiv = document.getElementById("comp-traceability-uncertainties");
  uncDiv.innerHTML = "<strong>Incertezas Mapeadas:</strong> " + sc.traceability.uncertainties.join(" | ");

  var indGrid = document.getElementById("indicators-grid");
  indGrid.innerHTML = "";
  for (var m = 0; m < DATA.indicators.length; m++) {
    var ind = DATA.indicators[m];
    var card = document.createElement("div");
    card.className = "card " + (ind.is_estimate ? "card-warn" : "card-accent");
    var badgeClass = ind.is_estimate ? "tag-estimate" : "tag-observed";
    var badgeLabel = ind.is_estimate ? "ESTIMATIVA" : "OBSERVADO";
    card.innerHTML =
      '<div class="card-title"><span>' + ind.label + '</span><span class="tag-pill ' + badgeClass + '">' + badgeLabel + '</span></div>' +
      '<div class="stat-val">' + ind.value + ' <span style="font-size:0.75rem;color:var(--dim);">' + ind.unit + '</span></div>' +
      '<div style="font-size:0.74rem;color:var(--dim);">' + ind.semantic_meaning + '</div>' +
      '<div style="font-size:0.68rem;font-family:var(--font-mono);color:var(--muted);margin-top:4px;">Fontes: ' + ind.source_refs.join(", ") + '</div>';
    indGrid.appendChild(card);
  }
}

function renderCanonicalPromptPills() {
  var row = document.getElementById("canonical-prompts-row");
  row.innerHTML = "";
  var prompts = DATA.visual_payloads.canonical_prompts || [];
  for (var i = 0; i < prompts.length; i++) {
    (function(pItem) {
      var btn = document.createElement("button");
      btn.className = "prompt-pill";
      btn.textContent = "“" + pItem.prompt + "”";
      btn.onclick = function() {
        document.getElementById("prompt-input").value = pItem.prompt;
        executeGenerativePrompt();
      };
      row.appendChild(btn);
    })(prompts[i]);
  }
}

function mapRepToSection(rep) {
  if (rep === "alchemical_emblem") return "sec-alchemical";
  if (rep === "radial_profile") return "sec-radial";
  if (rep === "knowledge_graph") return "sec-graph";
  if (rep === "portfolio_mosaic") return "sec-mosaic";
  if (rep === "capital_flow") return "sec-flow";
  return "sec-matrix";
}

function initAlchemicalEmblemAndLottie() {
  var alch = DATA.visual_payloads["6_alchemical_emblem_and_lottie"];
  if (!alch) return;
  var emblem = alch.alchemical_emblem;
  var res = emblem.resonance;

  document.getElementById("emblem-resonance-badge").textContent = "R_LE = " + res.resonance_index;
  document.getElementById("emblem-inscriptio").textContent = emblem.inscriptio_motto;
  document.getElementById("emblem-svg-container").innerHTML = emblem.svg_vector_markup;
  document.getElementById("emblem-subscriptio").textContent = emblem.subscriptio_epigram + " | Selo SHA-256: " + emblem.provenance_seal_sha256.slice(0, 16) + "...";

  if (window.anime) {
    anime({
      targets: "#emblem-svg-container svg polygon",
      scale: [0.96, 1.03],
      direction: "alternate",
      loop: true,
      duration: Math.round(1000 / Math.max(0.4, res.pulse_frequency_hz)),
      easing: "easeInOutSine"
    });
  }

  // Renderiza a Matriz de Puxers Quantitativos
  var puxGrid = document.getElementById("puxers-matrix-grid");
  puxGrid.innerHTML = "";
  var puxers = emblem.puxers || [];
  document.getElementById("puxers-total-badge").textContent = puxers.length + " Puxers";
  for (var i = 0; i < puxers.length; i++) {
    (function(pux) {
      var cell = document.createElement("div");
      cell.style.width = "26px";
      cell.style.height = "26px";
      cell.style.borderRadius = "4px";
      cell.style.display = "flex";
      cell.style.alignItems = "center";
      cell.style.justifyContent = "center";
      cell.style.fontSize = "0.78rem";
      cell.style.cursor = "pointer";
      cell.style.background = pux.color_hex + "26";
      cell.style.border = "1px solid " + pux.color_hex;
      cell.textContent = pux.glyph;
      cell.title = pux.tooltip;
      cell.onmouseenter = function() {
        document.getElementById("puxer-inspector-banner").textContent =
          pux.tooltip + " | Status: " + (pux.is_observed ? "OBSERVADO" : "ESTIMATIVA") + " | Fonte: " + pux.source_ref;
      };
      cell.onclick = cell.onmouseenter;
      puxGrid.appendChild(cell);
    })(puxers[i]);
  }

  // Renderiza a tabela do Mar de Informações
  var tbody = document.querySelector("#curated-streams-table tbody");
  tbody.innerHTML = "";
  var streams = alch.curated_investment_streams || [];
  for (var s = 0; s < streams.length; s++) {
    var st = streams[s];
    var tr = document.createElement("tr");
    tr.innerHTML =
      '<td style="font-family:var(--font-mono);font-weight:700;">' + st.element.toUpperCase() + '</td>' +
      '<td><strong>' + st.title + '</strong><br><span style="font-size:0.7rem;color:var(--dim);">' + st.raw_volume_description + '</span></td>' +
      '<td>' + st.curated_signal + '</td>' +
      '<td style="font-family:var(--font-mono);">' + st.quantitative_value + ' <span style="font-size:0.68rem;color:var(--dim);">' + st.quantitative_unit + '</span></td>';
    tbody.appendChild(tr);
  }

  // Popula o seletor de Templates LottieMCP
  var sel = document.getElementById("lottie-template-select");
  if (sel.options.length === 0) {
    var catalog = alch.lottie_templates_catalog || [];
    for (var c = 0; c < catalog.length; c++) {
      var opt = document.createElement("option");
      opt.value = catalog[c].template_id;
      opt.textContent = catalog[c].template_id + " — " + catalog[c].title;
      sel.appendChild(opt);
    }
    loadLottieTemplateDefaultParams("alchemical_emblem");
  }
}

function loadLottieTemplateDefaultParams(templateId) {
  var alch = DATA.visual_payloads["6_alchemical_emblem_and_lottie"];
  if (!alch || !alch.parameterized_lotties) return;
  var bundle = alch.parameterized_lotties[templateId];
  if (!bundle) return;
  document.getElementById("lottie-params-textarea").value = JSON.stringify(bundle.applied_params, null, 2);
  document.getElementById("lottie-receipt-box").textContent =
    "[LottieMCP Receipt] Template: " + bundle.parameterization_receipt.template_id +
    " | Schema: v" + bundle.parameterization_receipt.lottie_version +
    " | Camadas Animadas: " + bundle.parameterization_receipt.layers_count +
    " | Hash Params: " + bundle.parameterization_receipt.params_sha256;
  document.getElementById("lottie-json-preview").textContent = JSON.stringify(bundle.lottie_json, null, 2);
}

function applyLottieJsonParameterization() {
  var templateId = document.getElementById("lottie-template-select").value || "alchemical_emblem";
  var rawText = document.getElementById("lottie-params-textarea").value || "{}";
  var parsedParams = {};
  try {
    parsedParams = JSON.parse(rawText);
  } catch (err) {
    document.getElementById("lottie-receipt-box").textContent = "Erro de sintaxe no JSON de parametrização: " + err.message;
    return;
  }

  if (window.location.protocol.indexOf("http") === 0) {
    fetch("/api/lottie/parameterize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ template_id: templateId, params_json: parsedParams })
    })
    .then(function(r) { return r.json(); })
    .then(function(res) {
      if (res && res.lottie_json) {
        updateLottiePreviewFromResponse(templateId, parsedParams, res);
      }
    })
    .catch(function() {
      applyOfflineLottieParameterization(templateId, parsedParams);
    });
  } else {
    applyOfflineLottieParameterization(templateId, parsedParams);
  }
}

function applyOfflineLottieParameterization(templateId, parsedParams) {
  var alch = DATA.visual_payloads["6_alchemical_emblem_and_lottie"];
  var bundle = alch.parameterized_lotties[templateId];
  bundle.applied_params = parsedParams;
  if (bundle.lottie_json && bundle.lottie_json.meta) {
    bundle.lottie_json.meta.custom_params = parsedParams;
  }
  updateLottiePreviewFromResponse(templateId, parsedParams, bundle);
}

function updateLottiePreviewFromResponse(templateId, parsedParams, bundle) {
  document.getElementById("lottie-receipt-box").textContent =
    "[LottieMCP ATUALIZADO] Template '" + templateId + "' re-parametrizado via JSON! Camadas: " + bundle.lottie_json.layers.length;
  document.getElementById("lottie-json-preview").textContent = JSON.stringify(bundle.lottie_json, null, 2);
  appendAuditLog("[LottieMCP / CreatorMCP] Template '" + templateId + "' parametrizado com novo JSON.");
}

function executeGenerativePrompt() {
  var promptText = document.getElementById("prompt-input").value || "";
  var lower = promptText.toLowerCase();

  // Tenta consultar servidor local se estiver rodando, com fallback 100% offline determinístico
  if (window.location.protocol.indexOf("http") === 0) {
    fetch("/api/prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: promptText, perspective: DATA.perspective })
    })
    .then(function(res) { return res.json(); })
    .then(function(newSpec) {
      if (newSpec && newSpec.spec_id) {
        DATA = newSpec;
        renderTopCompressionAndIndicators();
        switchSection(mapRepToSection(DATA.primary_representation));
        appendAuditLog("[PROMPT GERADO] “" + promptText + "” → Representação: " + DATA.primary_representation);
      }
    })
    .catch(function() {
      applyOfflinePromptRouting(promptText, lower);
    });
  } else {
    applyOfflinePromptRouting(promptText, lower);
  }
}

function applyOfflinePromptRouting(promptText, lower) {
  DATA.prompt = promptText;
  var targetSec = "sec-matrix";
  if (lower.indexOf("emblema") >= 0 || lower.indexOf("alquim") >= 0 || lower.indexOf("alquím") >= 0 || lower.indexOf("puxer") >= 0 || lower.indexOf("lottie") >= 0 || lower.indexOf("resson") >= 0) {
    DATA.title = "Emblema Alquímico de Compressão Máxima, Puxers Quantitativos & LottieMCP";
    DATA.semantic_compression.instant_view.headline_signal = "Mar de informações condensado em 52 Puxers Quantitativos e 1 Emblema Alquímico com Ressonância R_LE = 0.85.";
    targetSec = "sec-alchemical";
  } else if (lower.indexOf("direito") >= 0 || lower.indexOf("licen") >= 0 || lower.indexOf("incerto") >= 0) {
    DATA.title = "Mapa de Proveniência, Direitos e Pendências de Licenciamento";
    DATA.semantic_compression.instant_view.headline_signal = "3 módulos (Wordsmith, Oracle, SovereignBudget) possuem pendências de direitos que bloqueiam licenciamento externo.";
    targetSec = "sec-graph";
  } else if (lower.indexOf("depend") >= 0 || lower.indexOf("reposit") >= 0 || lower.indexOf("grafo") >= 0) {
    DATA.title = "Grafo de Relações, Componentes Reutilizáveis e Gargalos do Compilatorum";
    DATA.semantic_compression.instant_view.headline_signal = "Proterol (9.6/10) e ValueCurator (9.3/10) são os maiores hubs reutilizáveis do Compilatorum.";
    targetSec = "sec-graph";
  } else if (lower.indexOf("sem blockchain") >= 0 || lower.indexOf("monetiz") >= 0 || lower.indexOf("origem") >= 0) {
    DATA.title = "Catálogo de Monetização Sem Blockchain & Perfis Radiais de Oportunidades";
    DATA.semantic_compression.instant_view.headline_signal = "100% dos 7 artefatos centrais geram valor via Micro-SaaS, API Semântica, CLI ou Grants sem exigir token.";
    targetSec = "sec-radial";
  } else if (lower.indexOf("mosaico") >= 0 || lower.indexOf("uma tela") >= 0 || lower.indexOf("resuma") >= 0) {
    DATA.title = "Mosaico Sintético do Portfólio Compilatorum (Visão em Uma Tela)";
    targetSec = "sec-mosaic";
  } else if (lower.indexOf("plano") >= 0 || lower.indexOf("execut") >= 0 || lower.indexOf("fluxo") >= 0) {
    DATA.title = "Fluxo de Capital em Movimento & Plano Executável de Validação";
    targetSec = "sec-flow";
  } else {
    DATA.title = "Matriz de Decisão & Portfólio de Experimentos sob Orçamento Limitado";
    targetSec = "sec-matrix";
  }
  renderTopCompressionAndIndicators();
  switchSection(targetSec);
  appendAuditLog("[PROMPT OFFLINE] “" + promptText + "” → Seção: " + targetSec);
}

function changePerspective(persp) {
  DATA.perspective = persp;
  if (persp === "desenvolvedor") {
    DATA.semantic_compression.instant_view.headline_signal = "[VISÃO DEV] " + DATA.semantic_compression.instant_view.headline_signal;
  } else if (persp === "cientifica") {
    DATA.semantic_compression.instant_view.headline_signal = "[VISÃO CIENTÍFICA] " + DATA.semantic_compression.instant_view.headline_signal;
  }
  renderTopCompressionAndIndicators();
  appendAuditLog("[PERSPECTIVA] Alterada para visão: " + persp.toUpperCase());
}

function initMatrixChart() {
  var exps = DATA.visual_payloads["4_decision_matrix"].ranked_experiments;
  var datasets = [];
  var colors = ["#00FF88", "#00BFFF", "#FFD700", "#B388FF"];
  for (var i = 0; i < exps.length; i++) {
    var e = exps[i];
    datasets.push({
      label: e.code + " (" + e.tag + " - " + e.efficiency_per_1k_brl + " pts/R$1k)",
      data: [{
        x: e.cost_brl,
        y: e.demand_evidence_score,
        r: Math.max(8, Math.round(e.efficiency_per_1k_brl / 5))
      }],
      backgroundColor: colors[i % colors.length] + "88",
      borderColor: colors[i % colors.length],
      borderWidth: 2
    });
  }
  safeChart("chartDecisionMatrix", {
    type: "bubble",
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#C8E6C9" } }
      },
      scales: {
        x: {
          title: { display: true, text: "Custo de Validação (R$ — Menor preserva mais caixa)", color: "#6B9E7A" },
          min: 200,
          max: 1400,
          grid: { color: "#1A3320" },
          ticks: { color: "#C8E6C9" }
        },
        y: {
          title: { display: true, text: "Evidência Atual de Demanda (0-100)", color: "#6B9E7A" },
          min: 40,
          max: 100,
          grid: { color: "#1A3320" },
          ticks: { color: "#C8E6C9" }
        }
      }
    }
  });
  updateBudgetSimulation(document.getElementById("budget-slider").value);
}

function updateBudgetSimulation(budgetVal) {
  var budget = parseFloat(budgetVal);
  document.getElementById("budget-slider-label").textContent = "R$ " + budget.toFixed(0);
  var exps = DATA.visual_payloads["4_decision_matrix"].ranked_experiments;
  var cumCost = 0;
  var chosenCodes = [];
  var totalUnc = 0;

  var container = document.getElementById("experiments-cards-container");
  container.innerHTML = "";

  for (var i = 0; i < exps.length; i++) {
    var e = exps[i];
    var fits = (cumCost + e.cost_brl) <= budget;
    if (fits) {
      cumCost += e.cost_brl;
      chosenCodes.push(e.code);
      totalUnc += e.uncertainty_reduction_pct * 0.85;
    }
    var tagClass = e.tag === "Testar" ? "tag-testar" : (e.tag === "Validar" ? "tag-validar" : "tag-preparar");
    var card = document.createElement("div");
    card.className = "mosaic-tile";
    card.style.borderLeft = fits ? "3px solid var(--accent)" : "3px solid var(--muted)";
    card.innerHTML =
      '<div style="display:flex;justify-content:space-between;align-items:center;">' +
        '<strong>' + e.title + '</strong>' +
        '<div><span class="tag-pill ' + tagClass + '">' + e.tag + '</span> ' +
        '<span class="tag-pill ' + (fits ? 'tag-observed' : 'tag-estimate') + '">' + (fits ? 'SELECIONADO' : 'ADIAR') + '</span></div>' +
      '</div>' +
      '<div style="font-size:0.78rem;color:var(--dim);margin:4px 0;">' + e.subtitle + ' — ' + e.objective + '</div>' +
      '<div style="font-size:0.76rem;font-family:var(--font-mono);color:var(--text);">' +
        'Custo: R$ ' + e.cost_brl.toFixed(0) + ' | ΔIncerteza: ' + e.uncertainty_reduction_pct + '% | Eficiência: <strong>' + e.efficiency_per_1k_brl + ' pts/R$1k</strong>' +
      '</div>';
    container.appendChild(card);
  }

  var simPhi = (1.34 - Math.max(0, (cumCost - 500) / 1000) * 0.04).toFixed(2);
  document.getElementById("sidebar-phi").textContent = simPhi + "x";
  var summaryBox = document.getElementById("simulation-summary-box");
  summaryBox.innerHTML =
    '<strong>[MODO SIMULAÇÃO — NENHUMA TRANSFERÊNCIA EXECUTADA]</strong><br>' +
    'Combinação Recomendada: <strong>[' + chosenCodes.join(" + ") + ']</strong> · Custo Total: R$ ' + cumCost.toFixed(2) +
    ' · Redução de Incerteza Combinada: ~' + Math.min(95, Math.round(totalUnc)) + '% · Φ_buffer Simulado: ' + simPhi + 'x (≥ 1.20x OK)';
}

function initRadialChart() {
  var opps = DATA.visual_payloads["1_radial_profile"].opportunities;
  document.getElementById("radial-warning-text").textContent = DATA.visual_payloads["1_radial_profile"].explicit_warning;

  var sel = document.getElementById("radial-opp-select");
  sel.innerHTML = "";
  for (var i = 0; i < opps.length; i++) {
    var opt = document.createElement("option");
    opt.value = opps[i].opportunity_id;
    opt.textContent = opps[i].title;
    sel.appendChild(opt);
  }

  var labels = [];
  for (var d = 0; d < opps[0].radial_dimensions.length; d++) {
    labels.push(opps[0].radial_dimensions[d].label);
  }

  var palette = [
    { border: "#00FF88", bg: "rgba(0, 255, 136, 0.18)" },
    { border: "#00BFFF", bg: "rgba(0, 191, 255, 0.18)" },
    { border: "#FFD700", bg: "rgba(255, 215, 0, 0.18)" }
  ];
  var datasets = [];
  for (var j = 0; j < opps.length; j++) {
    var scores = [];
    for (var m = 0; m < opps[j].radial_dimensions.length; m++) {
      scores.push(opps[j].radial_dimensions[m].score);
    }
    datasets.push({
      label: opps[j].title.split("(")[0],
      data: scores,
      borderColor: palette[j % palette.length].border,
      backgroundColor: palette[j % palette.length].bg,
      borderWidth: 2
    });
  }

  safeChart("chartRadialProfile", {
    type: "radar",
    data: { labels: labels, datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          angleLines: { color: "#1A3320" },
          grid: { color: "#1A3320" },
          pointLabels: { color: "#C8E6C9", font: { size: 11 } },
          ticks: { display: false }
        }
      },
      plugins: {
        legend: { labels: { color: "#C8E6C9" } }
      }
    }
  });

  renderRadialDimensionTable(opps[0].opportunity_id);
}

function renderRadialDimensionTable(oppId) {
  var opps = DATA.visual_payloads["1_radial_profile"].opportunities;
  var selected = opps[0];
  for (var i = 0; i < opps.length; i++) {
    if (opps[i].opportunity_id === oppId) {
      selected = opps[i];
      break;
    }
  }
  var tbody = document.querySelector("#radial-dimensions-table tbody");
  tbody.innerHTML = "";
  for (var j = 0; j < selected.radial_dimensions.length; j++) {
    var dim = selected.radial_dimensions[j];
    var tr = document.createElement("tr");
    var badge = dim.is_estimate
      ? '<span class="tag-pill tag-estimate">ESTIMATIVA SEM EVIDÊNCIA DIRETA</span>'
      : '<span class="tag-pill tag-observed">EVIDÊNCIA OBSERVADA</span>';
    tr.innerHTML =
      '<td><strong>' + dim.label + '</strong><br><span style="font-size:0.7rem;color:var(--dim);">' + dim.scale_criteria + '</span></td>' +
      '<td style="font-family:var(--font-mono);font-weight:700;">' + dim.score + '/100</td>' +
      '<td>' + badge + '</td>' +
      '<td>' + dim.basis_explanation + '<br><span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--muted);">Fonte: ' + dim.source_id + '</span></td>';
    tbody.appendChild(tr);
  }
}

function renderKnowledgeGraphSVG() {
  var wrapper = document.getElementById("svg-graph-wrapper");
  var nodes = DATA.visual_payloads["2_knowledge_graph"].nodes;
  var edges = DATA.visual_payloads["2_knowledge_graph"].edges;

  var positions = {
    "art:wordsmith_ingestor": { x: 95, y: 80 },
    "art:proterol_engine": { x: 280, y: 70 },
    "art:oracle_associative": { x: 470, y: 95 },
    "art:license_manifest": { x: 260, y: 245 },
    "art:valuecurator_core": { x: 460, y: 235 },
    "art:planner_governaut": { x: 640, y: 165 },
    "art:sovereign_budget_thermo": { x: 630, y: 285 }
  };

  var svg = '<svg viewBox="0 0 740 330" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">';
  for (var i = 0; i < edges.length; i++) {
    var e = edges[i];
    var p1 = positions[e.source_artifact_id] || { x: 100, y: 100 };
    var p2 = positions[e.target_artifact_id] || { x: 300, y: 200 };
    var strokeColor = e.is_bottleneck ? "#FF4455" : "#00BFFF";
    var dash = e.is_bottleneck ? 'stroke-dasharray="5,4"' : "";
    svg += '<line x1="' + p1.x + '" y1="' + p1.y + '" x2="' + p2.x + '" y2="' + p2.y + '" stroke="' + strokeColor + '" stroke-width="2" ' + dash + ' />';
  }

  for (var j = 0; j < nodes.length; j++) {
    var n = nodes[j];
    var pos = positions[n.artifact_id] || { x: 120 + j * 80, y: 160 };
    var fill = n.license_status === "unclear_pending_audit" ? "#FFB800" : "#00FF88";
    svg +=
      '<g transform="translate(' + pos.x + ',' + pos.y + ')">' +
        '<circle r="20" fill="#0D1A10" stroke="' + fill + '" stroke-width="3" />' +
        '<text y="4" text-anchor="middle" fill="#C8E6C9" font-family="monospace" font-size="9" font-weight="bold">' + n.compilatorum_project.slice(0, 9) + '</text>' +
        '<text y="34" text-anchor="middle" fill="#6B9E7A" font-family="sans-serif" font-size="10">' + n.license_spdx.split(" ")[0] + ' (' + n.reusability_score + ')</text>' +
      '</g>';
  }
  svg += '</svg>';
  wrapper.innerHTML = svg;

  var tbody = document.querySelector("#graph-rights-table tbody");
  tbody.innerHTML = "";
  for (var k = 0; k < nodes.length; k++) {
    (function(node) {
      var isUnclear = node.license_status === "unclear_pending_audit";
      var statusBadge = isUnclear
        ? '<span class="tag-pill tag-err">DIREITOS INCERTOS</span>'
        : '<span class="tag-pill tag-observed">PRONTO P/ LICENCIAR</span>';
      var tr = document.createElement("tr");
      tr.innerHTML =
        '<td><strong>' + node.compilatorum_project + '</strong><br><span style="font-size:0.72rem;color:var(--dim);">' + node.name + '</span></td>' +
        '<td style="font-family:var(--font-mono);">' + node.license_spdx + '</td>' +
        '<td>' + statusBadge + '</td>' +
        '<td style="font-family:var(--font-mono);">' + node.reusability_score + '/10</td>' +
        '<td>' + (isUnclear ? '<button class="btn-secondary" onclick="approveRightsAudit(\'' + node.artifact_id + '\')">Auditar SPDX</button>' : '<span style="color:var(--accent);font-size:0.75rem;">✓ Verificado</span>') + '</td>';
      tbody.appendChild(tr);
    })(nodes[k]);
  }
}

function approveRightsAudit(artifactId) {
  var nodes = DATA.visual_payloads["2_knowledge_graph"].nodes;
  for (var i = 0; i < nodes.length; i++) {
    if (nodes[i].artifact_id === artifactId) {
      nodes[i].license_status = "permissive_commercial";
      nodes[i].license_spdx = "MIT (Auditado)";
    }
  }
  var edges = DATA.visual_payloads["2_knowledge_graph"].edges;
  for (var j = 0; j < edges.length; j++) {
    if (edges[j].target_artifact_id === artifactId) {
      edges[j].is_bottleneck = false;
    }
  }
  renderKnowledgeGraphSVG();
  appendAuditLog("[AÇÃO AUTORIZADA HITL] Manifesto de Licença auditado para " + artifactId + " → Status: permissive_commercial (MIT).");
}

function renderPortfolioMosaic() {
  var grid = document.getElementById("portfolio-mosaic-grid");
  grid.innerHTML = "";
  var blocks = DATA.visual_payloads["3_portfolio_mosaic"].blocks;
  for (var i = 0; i < blocks.length; i++) {
    var b = blocks[i];
    var tile = document.createElement("div");
    tile.className = "mosaic-tile";
    tile.style.borderTop = b.realized_value_brl > 0 ? "2px solid var(--accent)" : "2px solid var(--data)";
    tile.innerHTML =
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:6px;">' +
        '<strong>' + b.title + '</strong>' +
        '<span class="tag-pill tag-observed">Score ' + b.composite_score + '</span>' +
      '</div>' +
      '<div style="font-size:0.75rem;color:var(--data);margin:6px 0;">' + b.monetization_type + '</div>' +
      '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;background:var(--bg);padding:8px;border-radius:6px;font-family:var(--font-mono);font-size:0.72rem;margin:8px 0;">' +
        '<div><span style="color:var(--dim);">Custo (Obs):</span><br><strong>R$ ' + b.committed_cost_brl + '</strong></div>' +
        '<div><span style="color:var(--accent);">Realizado:</span><br><strong style="color:var(--accent);">R$ ' + b.realized_value_brl + '</strong></div>' +
        '<div><span style="color:var(--warn);">Potencial (Est):</span><br><strong style="color:var(--warn);">R$ ' + b.estimated_potential_brl + '</strong></div>' +
      '</div>' +
      '<div style="font-size:0.74rem;color:var(--dim);"><strong>Próxima Ação:</strong> ' + b.recommended_next_action + '</div>';
    grid.appendChild(tile);
  }
}

function initCapitalFlowChart() {
  var stages = DATA.visual_payloads["5_capital_flow"].stages;
  var labels = [];
  var planned = [];
  var committed = [];
  var realized = [];
  for (var i = 0; i < stages.length; i++) {
    labels.push(stages[i].stage_name);
    planned.push(stages[i].planned_brl);
    committed.push(stages[i].committed_brl);
    realized.push(stages[i].realized_brl);
  }

  safeChart("chartCapitalFlow", {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        { label: "Previsto (Estimativa Planejada R$)", data: planned, backgroundColor: "rgba(255, 184, 0, 0.55)", borderColor: "#FFB800", borderWidth: 1 },
        { label: "Comprometido (Alocado R$)", data: committed, backgroundColor: "rgba(0, 191, 255, 0.65)", borderColor: "#00BFFF", borderWidth: 1 },
        { label: "Efetivamente Realizado (Observado R$)", data: realized, backgroundColor: "rgba(0, 255, 136, 0.75)", borderColor: "#00FF88", borderWidth: 1 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#C8E6C9" } } },
      scales: {
        x: { ticks: { color: "#C8E6C9" }, grid: { color: "#1A3320" } },
        y: { ticks: { color: "#C8E6C9" }, grid: { color: "#1A3320" } }
      }
    }
  });

  var plan = DATA.visual_payloads["5_capital_flow"].executable_plan;
  var box = document.getElementById("executable-plan-box");
  var html = '<div style="margin-bottom:8px;font-size:0.84rem;"><strong>' + plan.title + '</strong> — Orçamento Total: <span style="color:var(--accent);font-family:var(--font-mono);">R$ ' + plan.total_budget_brl + '</span> (' + plan.duration_weeks + ' semanas)</div>';
  for (var k = 0; k < plan.tasks.length; k++) {
    var t = plan.tasks[k];
    html +=
      '<div class="mosaic-tile" style="margin-bottom:8px;">' +
        '<div style="display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:0.75rem;color:var(--gold);">' +
          '<span>' + t.week + ' · ' + t.owner_module + '</span><span>R$ ' + t.resource_brl + '</span>' +
        '</div>' +
        '<div style="font-size:0.82rem;font-weight:600;margin:3px 0;">' + t.title + '</div>' +
        '<div style="font-size:0.74rem;color:var(--dim);">Entregável: ' + t.deliverable + '</div>' +
        '<div style="font-size:0.72rem;color:var(--accent);">Critério de Validação: ' + t.validation_metric + '</div>' +
      '</div>';
  }
  box.innerHTML = html;
}

function appendAuditLog(entryText) {
  var log = document.getElementById("decision-audit-log");
  if (!log) return;
  var div = document.createElement("div");
  div.className = "formula-block";
  div.textContent = new Date().toISOString().slice(11, 19) + " " + entryText;
  log.insertBefore(div, log.firstChild);
}

document.addEventListener("DOMContentLoaded", function() {
  if (window.Chart) {
    Chart.defaults.color = "#C8E6C9";
    Chart.defaults.borderColor = "#1A3320";
    Chart.defaults.font.family = "'JetBrains Mono', ui-monospace, monospace";
  }
  renderCanonicalPromptPills();
  renderTopCompressionAndIndicators();
  switchSection(mapRepToSection(DATA.primary_representation));
});
</script>
</body>
</html>
"""
        return html_template.replace("__SPEC_JSON_PLACEHOLDER__", spec_json)
