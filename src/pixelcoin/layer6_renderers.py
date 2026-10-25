"""
Camada 6 — Renderizadores Generativos (Multi-Environment Renderers)

Consome a `DeclarativeUISpecification` da Camada 5 e projeta a mesma oportunidade,
com o mesmo identificador, as mesmas fontes e os mesmos controles em 4 ambientes:
1. Web / Navegador (`WebGenerativeRenderer`) — Mosaicos, gráficos radiais, grafos SVG interativos, matriz de decisão, fluxo de capital e barra Prompt-como-Frontend.
2. Emacs / Org-mode (`EmacsOrgRenderer`) — Relatórios compactos, tabelas Org, propriedades, links para fontes `[[file:...]]` e agenda de experimentos (`TESTAR`, `VALIDAR`, `PREPARAR`).
3. Mobile / Microinterface (`MobileMicroRenderer`) — Alertas, decisões pendentes, resumo instantâneo e aprovações simples.
4. Agentes / Interfaces Conversacionais (`AgentConversationalRenderer`) — Envelope JSON-LD estruturado com limites de acesso, proveniência e permissões explícitas.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from pixelcoin.layer5_ui_spec import DeclarativeUISpecification
from pixelcoin.web_renderer import WebGenerativeRenderer

__all__ = [
    "WebGenerativeRenderer",
    "EmacsOrgRenderer",
    "MobileMicroRenderer",
    "AgentConversationalRenderer",
]


class EmacsOrgRenderer:
    """Renderizador para Emacs / Org-mode (Seção 5)."""

    @staticmethod
    def render(spec: DeclarativeUISpecification) -> str:
        sc = spec.semantic_compression
        lines: List[str] = [
            f"#+TITLE: PixelCoin — {spec.title}",
            f"#+SUBTITLE: {spec.subtitle}",
            f"#+PROPERTY: SPEC_ID {spec.spec_id}",
            f"#+PROPERTY: PROMPT {spec.prompt}",
            f"#+PROPERTY: INTENT {spec.interpreted_intent}",
            f"#+PROPERTY: PERSPECTIVE {spec.perspective.value}",
            f"#+PROPERTY: PRIMARY_VIEW {spec.primary_representation.value}",
            "#+STARTUP: overview indent",
            "",
            "* 1. Compressão Semântica (3 Níveis)",
            "** 1.1 Visão Instantânea (Sinal Principal)",
            f"- *Sinal Principal:* {sc.instant_view.headline_signal}",
            f"- *Ação Prioritária:* {sc.instant_view.top_priority_action}",
            f"- *Anomalia / Gargalo:* {sc.instant_view.detected_anomaly_or_bottleneck}",
            "",
            "** 1.2 Inspeção (Explicabilidade & Critérios)",
            f"- *Transparência Epistemológica:* {sc.inspection.observed_vs_estimated_breakdown}",
        ]
        for factor in sc.inspection.causal_factors:
            lines.append(f"  + {factor}")
        lines.append("- *Cenários Comparados:*")
        for scen in sc.inspection.alternative_scenarios:
            lines.append(f"  + {scen}")

        lines.extend([
            "",
            "** 1.3 Rastreabilidade (Fontes, Hashes SHA-256 e Incertezas)",
            "| Fonte ID | Módulo | Versão | SHA-256 | Link p/ Fonte |",
            "|---+---+---+---+---|",
        ])
        for src in sc.traceability.source_records:
            uri = src["uri"]
            lines.append(
                f"| ={src['source_id']}= | {src['module']} | {src['version']} | ={src['sha256']}= | [[{uri}][Abrir Fonte]] |"
            )

        lines.extend([
            "",
            "* 2. Indicadores-Chave (Dados antes da Estética)",
            "| ID | Indicador | Valor | Natureza Epistemológica | Fontes | Significado p/ Decisão |",
            "|---+---+---+---+---+---|",
        ])
        for ind in spec.indicators:
            epistemic = "[ESTIMATIVA]" if ind.is_estimate else "[OBSERVADO]"
            refs = ", ".join(ind.source_refs)
            lines.append(
                f"| ={ind.indicator_id}= | {ind.label} | *{ind.value}* {ind.unit} | ={epistemic}= | {refs} | {ind.semantic_meaning} |"
            )

        lines.extend([
            "",
            "* 3. Portfólio de Experimentos (Matriz de Decisão)",
            "Ordenado por *Redução de Incerteza por Unidade de Recurso* (pts / R$ 1.000):",
            "",
            "| Rank | Código | Experimento | Etiqueta | Custo (R$) | Δ Incerteza | Eficiência (pts/R$1k) | Cabe no Orçamento? |",
            "|---+---+---+---+---+---+---+---|",
        ])
        ranked = spec.visual_payloads["4_decision_matrix"]["ranked_experiments"]
        for exp in ranked:
            fits = "SIM" if exp["fits_in_budget"] else "ADIAR"
            lines.append(
                f"| {exp['rank']} | *{exp['code']}* | {exp['title']} | :{exp['tag'].upper()}: | R$ {exp['cost_brl']:.2f} | {exp['uncertainty_reduction_pct']}% | *{exp['efficiency_per_1k_brl']}* | {fits} |"
            )

        lines.append("")
        for exp in ranked:
            todo_kw = exp["tag"].upper()
            lines.extend([
                f"** {todo_kw} [{exp['code']}] {exp['title']} — {exp['subtitle']} :{exp['tag'].lower()}:",
                ":PROPERTIES:",
                f":EXPERIMENT_ID: {exp['experiment_id']}",
                f":COST_BRL: {exp['cost_brl']}",
                f":EFFICIENCY_PER_1K: {exp['efficiency_per_1k_brl']}",
                f":STATUS: {exp['status']}",
                ":END:",
                f"- *Objetivo:* {exp['objective']}",
                "- *Critérios de Validação:*",
            ])
            for crit in exp["validation_criteria"]:
                lines.append(f"  + [ ] {crit}")
            lines.append("")

        lines.extend([
            "* 4. Grafo de Artefatos, Licenças e Direitos (Camada 2)",
            "| Artefato | Projeto | Licença SPDX | Status de Direitos | Reutilização | Sem Blockchain? |",
            "|---+---+---+---+---+---|",
        ])
        for node in spec.visual_payloads["2_knowledge_graph"]["nodes"]:
            no_bc = "SIM" if node["monetizable_without_blockchain"] else "NÃO"
            lines.append(
                f"| ={node['artifact_id']}= | {node['compilatorum_project']} | {node['license_spdx']} | ={node['license_status']}= | {node['reusability_score']}/10 | {no_bc} |"
            )

        lines.extend([
            "",
            "* 5. Fluxo de Capital em Movimento & Plano Executável",
            "| Estágio | Previsto (R$) | Comprometido (R$) | Realizado (R$) | Fonte |",
            "|---+---+---+---+---|",
        ])
        for stage in spec.visual_payloads["5_capital_flow"]["stages"]:
            lines.append(
                f"| {stage['stage_name']} | R$ {stage['planned_brl']:.2f} | R$ {stage['committed_brl']:.2f} | R$ {stage['realized_brl']:.2f} | ={stage['source_id']}= |"
            )

        plan = spec.visual_payloads["5_capital_flow"]["executable_plan"]
        lines.extend([
            "",
            f"** {plan['title']} (Orçamento: R$ {plan['total_budget_brl']:.2f} / {plan['duration_weeks']} semanas)",
        ])
        for task in plan["tasks"]:
            lines.append(
                f"- [ ] *{task['week']}* ({task['owner_module']}, R$ {task['resource_brl']:.0f}): {task['title']} -> Entregável: ={task['deliverable']}="
            )

        alch = spec.visual_payloads.get("6_alchemical_emblem_and_lottie", {})
        if alch:
            emblem = alch["alchemical_emblem"]
            res = emblem["resonance"]
            lines.extend([
                "",
                "* 6. Emblema Alquímico, Puxers Quantitativos & LottieMCP / CreatorMCP",
                f"- *Inscriptio:* {emblem['inscriptio_motto']}",
                f"- *Subscriptio:* {emblem['subscriptio_epigram']}",
                f"- *Ressonância Lógico-Estética (R_LE):* *{res['resonance_index']}* (Lógica={res['logical_coherence_score']}, Estética={res['aesthetic_harmony_score']}, Pulso={res['pulse_frequency_hz']} Hz)",
                f"- *Total de Puxers Quantitativos:* {len(emblem['puxers'])} puxers (Selo SHA-256: ={emblem['provenance_seal_sha256'][:16]}...=)",
                "",
                "** 6.1 Curadoria do Mar de Informações de Investimento",
                "| Stream ID | Categoria | Sinal Destilado | Elemento | Quantitativo |",
                "|---+---+---+---+---|",
            ])
            for st in alch.get("curated_investment_streams", []):
                lines.append(
                    f"| ={st['stream_id']}= | {st['category']} | {st['curated_signal']} | {st['element'].upper()} | *{st['quantitative_value']}* {st['quantitative_unit']} |"
                )
            lines.extend([
                "",
                "** 6.2 Catálogo de Templates/Scripts LottieMCP Parametrizáveis via JSON",
                "| Template ID | Estrutura Infoestética | Parâmetros JSON Aceitos |",
                "|---+---+---|",
            ])
            for tmpl in alch.get("lottie_templates_catalog", []):
                req_p = ", ".join(tmpl["required_params"])
                lines.append(f"| ={tmpl['template_id']}= | {tmpl['title']} | ={req_p}= |")

        return "\n".join(lines) + "\n"


class MobileMicroRenderer:
    """Renderizador para Mobile / Microinterface (Seção 5)."""

    @staticmethod
    def render(spec: DeclarativeUISpecification) -> Dict[str, Any]:
        sc = spec.semantic_compression
        ranked = spec.visual_payloads["4_decision_matrix"]["ranked_experiments"]
        unclear = spec.visual_payloads["2_knowledge_graph"]["unclear_rights_artifacts"]
        return {
            "surface": "mobile_microinterface",
            "spec_id": spec.spec_id,
            "prompt": spec.prompt,
            "primary_representation": spec.primary_representation.value,
            "instant_card": {
                "signal": sc.instant_view.headline_signal,
                "priority_action": sc.instant_view.top_priority_action,
                "alert_banner": sc.instant_view.detected_anomaly_or_bottleneck,
            },
            "compact_metrics": [
                {
                    "label": ind.label,
                    "value": f"{ind.value} {ind.unit}".strip(),
                    "badge": "ESTIMATIVA" if ind.is_estimate else "OBSERVADO",
                }
                for ind in spec.indicators[:4]
            ],
            "pending_decisions": [
                {
                    "code": exp["code"],
                    "title": exp["title"],
                    "tag": exp["tag"],
                    "cost_brl": exp["cost_brl"],
                    "efficiency": f"{exp['efficiency_per_1k_brl']} pts/R$1k",
                    "recommended": exp["fits_in_budget"],
                }
                for exp in ranked[:3]
            ],
            "rights_alerts_count": len(unclear),
            "quick_approvals": [
                {
                    "action_id": act.action_id,
                    "label": act.label,
                    "mode": act.execution_mode,
                    "requires_human_approval": act.requires_human_approval,
                }
                for act in spec.allowed_actions
            ],
        }


class AgentConversationalRenderer:
    """Renderizador para Agentes / Interfaces Conversacionais (Seção 5)."""

    @staticmethod
    def render(spec: DeclarativeUISpecification) -> Dict[str, Any]:
        return {
            "@context": "https://compilatorum.org/schemas/pixelcoin/v1",
            "@type": "PixelCoinSemanticInterface",
            "spec_id": spec.spec_id,
            "prompt": spec.prompt,
            "interpreted_intent": spec.interpreted_intent,
            "perspective": spec.perspective.value,
            "primary_representation": spec.primary_representation.value,
            "access_policy": {
                "read_corpus": True,
                "simulate_allocations": True,
                "autonomous_capital_transfer": False,
                "requires_human_signature_for_mutations": True,
            },
            "guardrail_attestation": spec.guardrail_attestation,
            "semantic_compression": spec.semantic_compression.model_dump(mode="json"),
            "indicators": [ind.model_dump(mode="json") for ind in spec.indicators],
            "visual_payloads": spec.visual_payloads,
            "allowed_tool_calls": [act.model_dump(mode="json") for act in spec.allowed_actions],
        }
