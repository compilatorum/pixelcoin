# 🪙 PixelCoin — Interface Generativa de Inteligência Econômica, Emblemas Alquímicos & LottieMCP

**Camada transversal de apresentação, curadoria infoestética e inteligência econômica do ecossistema Compilatorum.**

> *"Em uma frase: o PixelCoin é um front-end generativo para navegar pelo espaço entre conhecimento e capital — condensando o mar de informações de investimento em Puxers quantitativos, Emblemas Alquímicos de compressão máxima, Vetores SVG e animações Lottie parametrizáveis via JSON (LottieMCP / CreatorMCP)."*

---

## 🏛️ 1. Arquitetura em 6 Camadas + Motor Alquímico & LottieMCP

O fluxo do PixelCoin opera de forma bidirecional (`Prompt → Contexto → Dados estruturados → Especificação da UI → Renderizador / LottieMCP → Interação → Resultado`):

| Camada / Módulo | Arquivo | Papel no Ecossistema |
| :--- | :--- | :--- |
| **Camada 6 — Renderizadores Generativos** | [`src/pixelcoin/layer6_renderers.py`](src/pixelcoin/layer6_renderers.py) & [`src/pixelcoin/web_renderer.py`](src/pixelcoin/web_renderer.py) | Renderiza a mesma especificação semântica para **Web/Navegador**, **Emacs/Org-mode**, **Mobile/Microinterface** e **Agentes Conversacionais (JSON-LD)**. |
| **LottieMCP & CreatorMCP Server** | [`src/pixelcoin/mcp_server.py`](src/pixelcoin/mcp_server.py) & [`src/pixelcoin/lottie_templates.py`](src/pixelcoin/lottie_templates.py) | Servidor MCP (JSON-RPC 2.0 `stdio` + API HTTP) com **6 templates/scripts de estruturas de infográfico** que recebem JSONs de atualização para parametrizar animações **Lottie (`v5.9.0`)** e **Vetores SVG**. |
| **Infoestética Alquímica & Puxers** | [`src/pixelcoin/alchemical_infoaesthetics.py`](src/pixelcoin/alchemical_infoaesthetics.py) | Faz a curadoria do **"Mar de Informações"** de investimento, calcula a **Ressonância Lógico-Estética ($\mathcal{R}_{LE}$)**, mapeia **Puxers Quantitativos** e compila **Emblemas Alquímicos** (*Inscriptio*, *Pictura SVG/Puxers*, *Subscriptio*). |
| **Camada 5 — Especificação de UI & Guardrails** | [`src/pixelcoin/layer5_ui_spec.py`](src/pixelcoin/layer5_ui_spec.py) | Define o contrato declarativo (`DeclarativeUISpecification`), a **Regra da Compressão Semântica (3 níveis)** e as **4 Regras de Controle (Guardrails)**. |
| **Camada 4 — Orquestração por IA** | [`src/pixelcoin/layer4_orchestrator.py`](src/pixelcoin/layer4_orchestrator.py) | Interpreta a intenção do prompt, adapta a perspectiva (`executiva`, `desenvolvedor`, `cientifica`) e seleciona a visualização primária. |
| **Camada 3 — Inteligência Econômica** | [`src/pixelcoin/layer3_economics.py`](src/pixelcoin/layer3_economics.py) | Avalia oportunidades em 6 dimensões radiais, prioriza experimentos por **Redução de Incerteza por Unidade de Recurso ($\Delta\text{Incerteza} / \text{R\$ 1k}$)** e rastreia o fluxo de capital. |
| **Camada 2 — Grafo Semântico e Direitos** | [`src/pixelcoin/layer2_graph.py`](src/pixelcoin/layer2_graph.py) | Conecta **Wordsmith**, **Proterol**, **Oracle**, **License Manifest**, **ValueCurator**, **Planner** e **SovereignBudget**, identificando hubs de reutilização e gargalos de direitos. |
| **Camada 1 — Fontes Primárias** | [`src/pixelcoin/layer1_sources.py`](src/pixelcoin/layer1_sources.py) | Ingere chatlogs, repositórios locais do workspace, documentos, razão contábil Beancount e resultados experimentais com hashes de proveniência `SHA-256`. |

---

## 🜏 2. Puxers Quantitativos, Ressonância Lógico-Estética & Emblemas Alquímicos

O módulo [`alchemical_infoaesthetics.py`](src/pixelcoin/alchemical_infoaesthetics.py) realiza a curadoria do **"mar de informações"** utilizado como fonte de investimentos e aplica compressão semântica máxima:

1. **Puxers Quantitativos (`PuxerUnit`)**: Cada unidade visual elementar (*Puxer* = Pixel + Quantitativo + Vetor) possui lastro exato nos 4 elementos alquímico-econômicos:
   - 🜃 **Terra (Sal — Evidência Realizada & Direitos SPDX)**: `1 Puxer = R$ 250,00` de Valor Realizado Observado.
   - 🜄 **Aqua (Mercúrio — Liquidez & Capital em Fluxo)**: `1 Puxer = R$ 250,00` de Custo Comprometido em Movimento.
   - 🜂 **Ignis (Enxofre — Impulso Experimental)**: `1 Puxer = 5%` de Redução de Incerteza ($\Delta\text{Incerteza}$).
   - 🜁 **Aer (Quintessência — Sinergia no Grafo)**: `1 Puxer = 5 pts` de Reutilização Semântica entre repositórios.
2. **Ressonância Lógico-Estética ($\mathcal{R}_{LE}$)**: Acopla a coerência lógica (fração de dimensões com evidência empírica, segurança do buffer fiduciário $\Phi_{\text{buffer}} \ge 1.20$ e eficiência informacional) à harmonia estética (proporção áurea $\varphi = 1.618$, simetria hexagonal e frequência de pulsação cinética em Hz).
3. **Templates LottieMCP / CreatorMCP (`lottie_templates.py`)**:
   - `alchemical_emblem` ([`dist/lottie/alchemical_emblem.lottie.json`](dist/lottie/alchemical_emblem.lottie.json) + [`dist/lottie/alchemical_emblem.svg`](dist/lottie/alchemical_emblem.svg))
   - `radial_profile` ([`dist/lottie/radial_profile.lottie.json`](dist/lottie/radial_profile.lottie.json))
   - `knowledge_graph` ([`dist/lottie/knowledge_graph.lottie.json`](dist/lottie/knowledge_graph.lottie.json))
   - `portfolio_mosaic` ([`dist/lottie/portfolio_mosaic.lottie.json`](dist/lottie/portfolio_mosaic.lottie.json))
   - `decision_matrix` ([`dist/lottie/decision_matrix.lottie.json`](dist/lottie/decision_matrix.lottie.json))
   - `capital_flow` ([`dist/lottie/capital_flow.lottie.json`](dist/lottie/capital_flow.lottie.json))

---

## 🚀 3. Como Executar

### 1. Executar a Suíte de Testes (8/8 passando)
```bash
PYTHONPATH=src pytest -v
```

### 2. Parametrizar Infográficos Lottie & Vetores via JSON (CLI & MCP)
```bash
# Parametrizar qualquer template de infográfico passando um JSON de atualização
PYTHONPATH=src python3 -m pixelcoin lottie --template alchemical_emblem \
  --params '{"realized_brl": 5000, "committed_brl": 2250, "uncertainty_reduction_pct": 90, "resonance_index": 0.92}'

# Exportar todos os 6 arquivos .lottie.json e o vetor alchemical_emblem.svg
PYTHONPATH=src python3 -m pixelcoin lottie --export-dir dist/lottie

# Listar ferramentas do servidor LottieMCP / CreatorMCP ou iniciar via stdio JSON-RPC 2.0
PYTHONPATH=src python3 -m pixelcoin mcp --list-tools
PYTHONPATH=src python3 -m pixelcoin mcp
```

### 3. Renderizar para Web, Emacs Org-mode, Mobile ou Agentes
```bash
PYTHONPATH=src python3 -m pixelcoin render --surface web --output dist/pixelcoin_generative_ui.html
PYTHONPATH=src python3 -m pixelcoin render --surface org --output dist/pixelcoin_compilatorum_report.org
PYTHONPATH=src python3 -m pixelcoin server --port 8090
```
