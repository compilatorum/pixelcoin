"""
GenUI-MD — Especificação de Linguagem, Parser Seguro, UI IR, Validador de Políticas,
Sincronizador Multi-Janela e Adaptador Bidirecional para o PixelCoin / Compilatorum.

Implementa as etapas P0 a P5 de `docs/GENUI-MD-SPEC.md`:
- P0 (Formalização): Modelos Pydantic v2 (`GenUIEnvelope`, `GenUIWindow`, `GenUILink`,
  `GenUIAction`, `GenUIFallback`, `GenUIDocument`) e geração de JSON Schema canônico.
- P1 (Parser Seguro): Extração de prosa Markdown + bloco `:::genui ... :::` com rejeição
  de YAML malformado, tags customizadas (`!!`), âncoras/aliases (`&`, `*`) e JS/HTML inline.
- P2 (Multi-Janela & Sincronização): Validação de IDs únicos, verificação de referências
  de janelas, detecção de ciclos em `links` e propagação determinística de estado (`GenUIWorkspaceRuntime`).
- P3/P4 (Adaptador & Ações Controladas): Conversão bidirecional (`GenUIMDAdapter`) entre
  `GenUIDocument` (UI IR) e `DeclarativeUISpecification` (Camadas 4, 5 e 6 do PixelCoin).
"""

from __future__ import annotations

import json
import re
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field, model_validator

from pixelcoin.layer5_ui_spec import (
    DeclarativeUISpecification,
    PersonaPerspective,
    VisualRepresentationType,
)


class GenUIValidationError(Exception):
    """Exceção disparada quando um documento ou envelope GenUI-MD viola a especificação."""


class GenUIMode(str, Enum):
    TEXT = "text"
    INTERACTIVE = "interactive"


class GenUISurface(str, Enum):
    INLINE = "inline"
    WORKSPACE = "workspace"
    MOBILE = "mobile"
    EMACS = "emacs"
    AGENT = "agent"
    AUTO = "auto"


class GenUIStateScope(str, Enum):
    LOCAL = "local"
    WINDOW = "window"
    WORKSPACE = "workspace"
    CONVERSATION = "conversation"
    PERSISTENT = "persistent"


REGISTERED_LAYOUTS: Set[str] = {
    "single",
    "stack",
    "grid",
    "split-horizontal",
    "split-vertical",
    "capital-workbench",
    "knowledge-workbench",
    "developer-workbench",
    "research-workbench",
    "agent-workbench",
    "alchemical-workbench",
    "freeform",
}

REGISTERED_COMPONENTS: Set[str] = {
    # Texto
    "text.summary",
    "text.markdown",
    "text.diff",
    # Dados
    "data.table",
    "data.metric",
    "data.timeline",
    # Visualização & Infoestética Alquímica
    "chart.radial",
    "chart.line",
    "chart.bar",
    "chart.scatter",
    "portfolio.mosaic",
    "alchemical.emblem",
    "puxer.matrix",
    "lottie.infographic",
    # Conhecimento
    "graph.knowledge",
    "graph.dependencies",
    "evidence.inspector",
    # Decisão
    "decision.matrix",
    "scenario.compare",
    "risk.register",
    # Capital
    "capital.flow",
    "treasury.summary",
    "budget.allocation",
    # Engenharia
    "code.viewer",
    "repo.status",
    "test.results",
    "dependency.map",
    # Trabalho
    "task.queue",
    "kanban.board",
    "calendar.agenda",
    "agent.console",
    # Artefatos
    "artifact.card",
    "license.manifest",
    "provenance.chain",
    # Entrada
    "form.schema",
    "filter.bar",
    "prompt.input",
}

REGISTERED_EVENTS: Set[str] = {
    "selection.changed",
    "filter.changed",
    "source.refreshed",
    "scenario.updated",
    "task.completed",
    "action.requested",
    "action.succeeded",
    "action.failed",
    "lottie.parameterized",
}

REGISTERED_ACTIONS: Set[str] = {
    "opportunity.simulate",
    "treasury.allocate",
    "rights.audit",
    "experiment.record",
    "lottie.parameterize",
    "org.export",
}


class GenUIWindow(BaseModel):
    """Unidade lógica de janela no workspace GenUI-MD (Seção 4)."""

    id: str = Field(..., min_length=1, description="ID único da janela no workspace")
    title: str = Field(..., min_length=1, description="Título legível da janela")
    component: str = Field(..., description="ID de componente registrado no catálogo (ex: chart.radial)")
    source: str = Field(..., min_length=1, description="Referência simbólica a dados autorizados")
    span: int = Field(default=6, ge=1, le=12, description="Largura relativa na grade de 12 colunas")
    priority: int = Field(default=1, ge=1, le=10, description="Prioridade para degradação responsiva")
    props: Dict[str, Any] = Field(default_factory=dict)
    state: Dict[str, Any] = Field(default_factory=dict)
    provenance: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_window_security_and_catalog(self) -> "GenUIWindow":
        if self.component not in REGISTERED_COMPONENTS:
            raise GenUIValidationError(
                f"Componente desconhecido ou não autorizado: '{self.component}'. "
                f"Deve pertencer ao catálogo registrado."
            )
        if self.source.startswith(("http://", "https://", "javascript:", "data:")):
            raise GenUIValidationError(
                f"Fonte inválida na janela '{self.id}': '{self.source}'. "
                "Fontes devem ser referências simbólicas autorizadas, nunca URLs externas ou scripts."
            )
        return self


class GenUILink(BaseModel):
    """Vínculo reativo de estado/evento entre janelas (Seção 7)."""

    from_ref: str = Field(..., alias="from", description="Origem no formato window_id.propriedade")
    to_ref: str = Field(..., alias="to", description="Destino no formato window_id.propriedade")
    event: str = Field(..., description="Nome simbólico do evento registrado")

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def validate_event(self) -> "GenUILink":
        if self.event not in REGISTERED_EVENTS:
            raise GenUIValidationError(
                f"Evento não registrado: '{self.event}'. Eventos permitidos: {sorted(REGISTERED_EVENTS)}"
            )
        if "." not in self.from_ref or "." not in self.to_ref:
            raise GenUIValidationError(
                f"Binding inválido ('{self.from_ref}' -> '{self.to_ref}'): deve usar formato 'window_id.campo'."
            )
        return self


class GenUIAction(BaseModel):
    """Ação controlada declarada no envelope GenUI-MD (Seção 8)."""

    id: str = Field(..., description="ID da ação no catálogo registrado")
    label: str = Field(..., min_length=1)
    kind: str = Field(..., description="invoke | mutate")
    permission: str = Field(..., min_length=1, description="Escopo de permissão exigido (ex: capital:simulate)")
    confirmation: str = Field(default="none", description="none | required")

    @model_validator(mode="after")
    def validate_action_policy(self) -> "GenUIAction":
        if self.id not in REGISTERED_ACTIONS:
            raise GenUIValidationError(
                f"Ação desconhecida ou não autorizada: '{self.id}'. Ações permitidas: {sorted(REGISTERED_ACTIONS)}"
            )
        if self.kind not in ("invoke", "mutate"):
            raise GenUIValidationError(f"Tipo de ação inválido '{self.kind}': use 'invoke' ou 'mutate'.")
        if self.confirmation not in ("none", "required"):
            raise GenUIValidationError(f"Campo confirmation inválido '{self.confirmation}': use 'none' ou 'required'.")
        if self.kind == "mutate" and self.confirmation != "required":
            raise GenUIValidationError(
                f"Violação de Segurança (Seção 8/10): A ação mutável '{self.id}' exige confirmation='required'."
            )
        return self


class GenUIFallback(BaseModel):
    """Alternativa legível obrigatória para ambientes sem suporte gráfico (Seção 3)."""

    mode: str = Field(default="markdown")
    summary: str = Field(..., min_length=1, description="Resumo legível em texto puro/Markdown")


class GenUIProvenancePolicy(BaseModel):
    """Política de exibição de proveniência e distinção epistemológica (Seção 10/12)."""

    show_sources: bool = True
    show_as_of: bool = True
    distinguish_observed_estimated_simulated: bool = True


class GenUIEnvelope(BaseModel):
    """
    Contrato canônico do bloco `:::genui ... :::` (UI IR — Seção 3 de `docs/GENUI-MD-SPEC.md`).
    """

    version: str = Field(default="0.1", description="Versão do contrato GenUI-MD")
    id: str = Field(..., min_length=1, description="Identificador único da instância de resposta/workspace")
    mode: GenUIMode = Field(..., description="text | interactive (obrigatório em toda resposta)")
    intent: str = Field(..., min_length=1, description="Propósito compreensível da interface/resposta")
    surface: GenUISurface = Field(default=GenUISurface.WORKSPACE)
    layout: str = Field(default="capital-workbench", description="ID de layout registrado")
    state_scope: GenUIStateScope = Field(default=GenUIStateScope.CONVERSATION)
    windows: List[GenUIWindow] = Field(default_factory=list)
    links: List[GenUILink] = Field(default_factory=list)
    actions: List[GenUIAction] = Field(default_factory=list)
    fallback: GenUIFallback
    provenance: GenUIProvenancePolicy = Field(default_factory=GenUIProvenancePolicy)

    @model_validator(mode="after")
    def validate_envelope_invariants(self) -> "GenUIEnvelope":
        if self.version not in ("0.1", "0.2", "0.1.0", "0.2.0"):
            raise GenUIValidationError(f"Versão GenUI-MD não suportada: '{self.version}'.")

        if self.layout not in REGISTERED_LAYOUTS:
            raise GenUIValidationError(
                f"Layout desconhecido: '{self.layout}'. Layouts permitidos: {sorted(REGISTERED_LAYOUTS)}"
            )

        if self.mode == GenUIMode.TEXT and len(self.windows) > 0:
            raise GenUIValidationError(
                "No modo 'text', a lista 'windows' deve ser vazia (windows: [])."
            )
        if self.mode == GenUIMode.INTERACTIVE and len(self.windows) == 0:
            raise GenUIValidationError(
                "No modo 'interactive', pelo menos uma janela deve ser declarada em 'windows'."
            )

        # Verifica IDs de janela duplicados
        seen_win_ids: Set[str] = set()
        for w in self.windows:
            if w.id in seen_win_ids:
                raise GenUIValidationError(f"ID de janela duplicado no workspace: '{w.id}'.")
            seen_win_ids.add(w.id)

        # Verifica referências de links e detecta ciclos
        adj: Dict[str, List[str]] = {wid: [] for wid in seen_win_ids}
        for link in self.links:
            src_win = link.from_ref.split(".")[0]
            dst_win = link.to_ref.split(".")[0]
            if src_win not in seen_win_ids:
                raise GenUIValidationError(
                    f"Link referencia janela de origem inexistente: '{src_win}' em '{link.from_ref}'."
                )
            if dst_win not in seen_win_ids:
                raise GenUIValidationError(
                    f"Link referencia janela de destino inexistente: '{dst_win}' em '{link.to_ref}'."
                )
            if src_win == dst_win:
                raise GenUIValidationError(
                    f"Auto-ciclo detectado na janela '{src_win}' ({link.from_ref} -> {link.to_ref})."
                )
            adj[src_win].append(dst_win)

        # Busca em profundidade (DFS) para detectar ciclos no grafo de sincronização de janelas
        visited: Set[str] = set()
        in_stack: Set[str] = set()

        def _has_cycle(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    if _has_cycle(neighbor):
                        return True
                elif neighbor in in_stack:
                    return True
            in_stack.remove(node)
            return False

        for wid in seen_win_ids:
            if wid not in visited and _has_cycle(wid):
                raise GenUIValidationError(
                    "Ciclo de sincronização detectado em 'links'. Os vínculos entre janelas devem formar um DAG."
                )

        return self


class GenUIDocument(BaseModel):
    """Documento GenUI-MD completo contendo a prosa Markdown e o envelope validado."""

    prose_markdown: str = Field(..., description="Prosa Markdown principal legível sem renderizador especial")
    envelope: GenUIEnvelope


class GenUIMDParser:
    """
    Parser Seguro para documentos GenUI-MD (Seção 3.1 e P1).
    Suporta YAML restrito (sem tags customizadas, sem âncoras/aliases) ou JSON dentro de `:::genui ... :::`.
    """

    BLOCK_PATTERN = re.compile(r"^:::genui\s*\n(.*?)\n:::\s*$", re.DOTALL | re.MULTILINE)

    @classmethod
    def parse(cls, markdown_text: str, allow_legacy_normalization: bool = False) -> GenUIDocument:
        matches = list(cls.BLOCK_PATTERN.finditer(markdown_text))
        if len(matches) > 1:
            raise GenUIValidationError(
                "Contrato violado: a resposta contém múltiplos blocos ':::genui'. Deve haver exatamente um envelope."
            )
        if len(matches) == 0:
            if allow_legacy_normalization:
                return cls.normalize_legacy_response(markdown_text)
            raise GenUIValidationError(
                "Contrato violado: nenhum bloco ':::genui ... :::' encontrado na resposta."
            )

        match = matches[0]
        raw_block = match.group(1)
        prose = (markdown_text[: match.start()] + markdown_text[match.end() :]).strip()

        cls._verify_raw_block_security(raw_block)
        parsed_dict = cls._parse_restricted_yaml_or_json(raw_block)
        if not isinstance(parsed_dict, dict):
            raise GenUIValidationError("O conteúdo do bloco :::genui deve ser um mapeamento chave-valor.")

        try:
            envelope = GenUIEnvelope.model_validate(parsed_dict)
        except GenUIValidationError:
            raise
        except Exception as exc:
            raise GenUIValidationError(f"Erro de validação do envelope GenUI-MD: {exc}") from exc

        if not prose:
            prose = envelope.fallback.summary

        return GenUIDocument(prose_markdown=prose, envelope=envelope)

    @classmethod
    def normalize_legacy_response(
        cls,
        raw_markdown: str,
        doc_id: str = "legacy-normalized-response",
        intent: str = "resposta textual normalizada para o contrato GenUI-MD",
    ) -> GenUIDocument:
        """
        Normaliza uma resposta Markdown legada (sem bloco :::genui) para o contrato
        padrão usando `mode: "text"` e `windows: []` (Seção 3).
        """
        clean_prose = raw_markdown.strip() or "Resposta vazia."
        first_line = clean_prose.splitlines()[0].lstrip("# ").strip()
        summary = first_line[:160] if first_line else "Resumo em Markdown."
        envelope = GenUIEnvelope(
            version="0.1",
            id=doc_id,
            mode=GenUIMode.TEXT,
            intent=intent,
            surface=GenUISurface.INLINE,
            layout="single",
            state_scope=GenUIStateScope.CONVERSATION,
            windows=[],
            links=[],
            actions=[],
            fallback=GenUIFallback(mode="markdown", summary=summary),
        )
        return GenUIDocument(prose_markdown=clean_prose, envelope=envelope)

    @classmethod
    def serialize(cls, doc: GenUIDocument) -> str:
        """Serializa um `GenUIDocument` de volta para a sintaxe autorável GenUI-MD."""
        env = doc.envelope
        lines: List[str] = []
        if doc.prose_markdown.strip():
            lines.append(doc.prose_markdown.strip())
            lines.append("")

        lines.extend([
            ":::genui",
            f'version: "{env.version}"',
            f'id: "{env.id}"',
            f'mode: "{env.mode.value}"',
            f'intent: "{env.intent}"',
            f'surface: "{env.surface.value}"',
            f'layout: "{env.layout}"',
            f'state_scope: "{env.state_scope.value}"',
        ])

        if not env.windows:
            lines.append("windows: []")
        else:
            lines.append("windows:")
            for w in env.windows:
                lines.extend([
                    f'  - id: "{w.id}"',
                    f'    title: "{w.title}"',
                    f'    component: "{w.component}"',
                    f'    source: "{w.source}"',
                    f"    span: {w.span}",
                    f"    priority: {w.priority}",
                ])

        if env.links:
            lines.append("links:")
            for lk in env.links:
                lines.extend([
                    f'  - from: "{lk.from_ref}"',
                    f'    to: "{lk.to_ref}"',
                    f'    event: "{lk.event}"',
                ])

        if env.actions:
            lines.append("actions:")
            for act in env.actions:
                lines.extend([
                    f'  - id: "{act.id}"',
                    f'    label: "{act.label}"',
                    f'    kind: "{act.kind}"',
                    f'    permission: "{act.permission}"',
                    f'    confirmation: "{act.confirmation}"',
                ])

        lines.extend([
            "fallback:",
            f'  mode: "{env.fallback.mode}"',
            f'  summary: "{env.fallback.summary}"',
            "provenance:",
            f"  show_sources: {'true' if env.provenance.show_sources else 'false'}",
            f"  show_as_of: {'true' if env.provenance.show_as_of else 'false'}",
            f"  distinguish_observed_estimated_simulated: {'true' if env.provenance.distinguish_observed_estimated_simulated else 'false'}",
            ":::",
        ])
        return "\n".join(lines) + "\n"

    @classmethod
    def _verify_raw_block_security(cls, raw_block: str) -> None:
        if re.search(r"![!a-zA-Z0-9_<]", raw_block):
            raise GenUIValidationError("Segurança YAML: Tags customizadas ('!!' ou '!<tag>') são proibidas em GenUI-MD.")
        if re.search(r"(^|\s)[&*][a-zA-Z0-9_]+", raw_block):
            raise GenUIValidationError("Segurança YAML: Âncoras ('&') e aliases ('*') são proibidos em GenUI-MD.")
        lower = raw_block.lower()
        if "<script" in lower or "javascript:" in lower or "onerror=" in lower or "onload=" in lower:
            raise GenUIValidationError("Segurança GenUI-MD: Execução de HTML/JavaScript inline é estritamente proibida.")

    @classmethod
    def _parse_restricted_yaml_or_json(cls, raw_block: str) -> Dict[str, Any]:
        stripped = raw_block.strip()
        if stripped.startswith("{"):
            try:
                return json.loads(stripped)
            except Exception as exc:
                raise GenUIValidationError(f"JSON malformado no bloco :::genui: {exc}") from exc

        try:
            import yaml  # type: ignore

            data = yaml.safe_load(stripped)
            if not isinstance(data, dict):
                raise GenUIValidationError("YAML GenUI-MD não produziu um objeto raiz.")
            return data
        except ImportError:
            return cls._fallback_minimal_yaml_parser(stripped)
        except GenUIValidationError:
            raise
        except Exception as exc:
            raise GenUIValidationError(f"YAML malformado no bloco :::genui: {exc}") from exc

    @classmethod
    def _fallback_minimal_yaml_parser(cls, text: str) -> Dict[str, Any]:
        """Parser determinístico para o subconjunto YAML restrito caso PyYAML não esteja instalado."""
        result: Dict[str, Any] = {}
        current_section: Optional[str] = None
        current_list_item: Optional[Dict[str, Any]] = None

        for raw_line in text.splitlines():
            if not raw_line.strip() or raw_line.strip().startswith("#"):
                continue
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            line = raw_line.strip()

            if indent == 0:
                current_list_item = None
                if ":" not in line:
                    raise GenUIValidationError(f"Linha YAML inválida: '{raw_line}'")
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                if v == "":
                    current_section = k
                    result[k] = None
                elif v == "[]":
                    current_section = None
                    result[k] = []
                else:
                    current_section = None
                    result[k] = cls._parse_scalar(v)
            elif indent == 2 and current_section:
                if line.startswith("- "):
                    if not isinstance(result.get(current_section), list):
                        result[current_section] = []
                    item_dict: Dict[str, Any] = {}
                    rest = line[2:].strip()
                    if ":" in rest:
                        ik, iv = rest.split(":", 1)
                        item_dict[ik.strip()] = cls._parse_scalar(iv.strip())
                    result[current_section].append(item_dict)
                    current_list_item = item_dict
                else:
                    if not isinstance(result.get(current_section), dict):
                        result[current_section] = {}
                    ik, iv = line.split(":", 1)
                    result[current_section][ik.strip()] = cls._parse_scalar(iv.strip())
            elif indent >= 4 and current_list_item is not None:
                if ":" not in line:
                    raise GenUIValidationError(f"Propriedade de item inválida: '{raw_line}'")
                ik, iv = line.split(":", 1)
                current_list_item[ik.strip()] = cls._parse_scalar(iv.strip())
            else:
                raise GenUIValidationError(f"Indentação YAML inesperada na linha: '{raw_line}'")

        return result

    @staticmethod
    def _parse_scalar(val: str) -> Any:
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            return val[1:-1]
        if val.lower() == "true":
            return True
        if val.lower() == "false":
            return False
        try:
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            return val


class GenUIWorkspaceRuntime:
    """
    Runtime de Estado e Sincronização Multi-Janela (Seção 7 e P2/P4).
    Mantém o estado das janelas e propaga eventos ao longo do DAG `links`.
    """

    def __init__(self, envelope: GenUIEnvelope) -> None:
        self.envelope = envelope
        self.window_states: Dict[str, Dict[str, Any]] = {
            w.id: dict(w.state) for w in envelope.windows
        }
        self.event_log: List[Dict[str, Any]] = []

    def dispatch_event(self, from_ref: str, event: str, payload_value: Any) -> List[Tuple[str, str, Any]]:
        """
        Propaga um evento emitido por `from_ref` (ex: 'portfolio.selection')
        para todas as janelas conectadas em `envelope.links`.
        """
        if event not in REGISTERED_EVENTS:
            raise GenUIValidationError(f"Tentativa de disparar evento não registrado: '{event}'.")

        src_win, src_prop = from_ref.split(".", 1)
        if src_win not in self.window_states:
            raise GenUIValidationError(f"Janela de origem inexistente no runtime: '{src_win}'.")

        self.window_states[src_win][src_prop] = payload_value
        updates: List[Tuple[str, str, Any]] = []

        for link in self.envelope.links:
            if link.from_ref == from_ref and link.event == event:
                dst_win, dst_prop = link.to_ref.split(".", 1)
                self.window_states[dst_win][dst_prop] = payload_value
                updates.append((dst_win, dst_prop, payload_value))

        self.event_log.append(
            {
                "from": from_ref,
                "event": event,
                "value": payload_value,
                "propagated_to": [f"{w}.{p}" for w, p, _ in updates],
            }
        )
        return updates


class GenUIMDAdapter:
    """
    Adaptador Bidirecional (Seção 13) entre `GenUIDocument` (GenUI-MD UI IR)
    e `DeclarativeUISpecification` (Camada 5 do PixelCoin).
    """

    @staticmethod
    def from_declarative_spec(
        spec: DeclarativeUISpecification,
        mode: GenUIMode = GenUIMode.INTERACTIVE,
        layout: str = "capital-workbench",
    ) -> GenUIDocument:
        """
        Converte uma `DeclarativeUISpecification` gerada pela Camada 4 em um
        documento completo `GenUIDocument` com prosa Markdown e bloco `:::genui`.
        """
        sc = spec.semantic_compression
        prose_lines = [
            f"# {spec.title}",
            "",
            f"**Sinal Principal:** {sc.instant_view.headline_signal}",
            "",
            f"- **Ação Prioritária:** {sc.instant_view.top_priority_action}",
            f"- **Anomalia / Gargalo:** {sc.instant_view.detected_anomaly_or_bottleneck}",
            f"- **Transparência Epistemológica:** {sc.inspection.observed_vs_estimated_breakdown}",
        ]
        prose = "\n".join(prose_lines)

        if mode == GenUIMode.TEXT:
            envelope = GenUIEnvelope(
                version="0.1",
                id=spec.spec_id,
                mode=GenUIMode.TEXT,
                intent=spec.interpreted_intent,
                surface=GenUISurface.INLINE,
                layout="single",
                state_scope=GenUIStateScope.CONVERSATION,
                windows=[],
                links=[],
                actions=[],
                fallback=GenUIFallback(mode="markdown", summary=sc.instant_view.headline_signal),
            )
            return GenUIDocument(prose_markdown=prose, envelope=envelope)

        windows = [
            GenUIWindow(
                id="alchemical-emblem",
                title="Emblema Alquímico & Puxers",
                component="alchemical.emblem",
                source="portfolio.alchemical_emblem",
                span=6,
                priority=1,
            ),
            GenUIWindow(
                id="portfolio",
                title="Mosaico do Portfólio",
                component="portfolio.mosaic",
                source="portfolio.opportunities",
                span=6,
                priority=2,
            ),
            GenUIWindow(
                id="decision",
                title="Matriz de Decisão & Experimentos",
                component="decision.matrix",
                source="portfolio.ranked_experiments",
                span=7,
                priority=1,
            ),
            GenUIWindow(
                id="radial-profile",
                title="Perfil Radial (6 Dimensões)",
                component="chart.radial",
                source="selection.opportunity_profile",
                span=5,
                priority=2,
            ),
            GenUIWindow(
                id="asset-graph",
                title="Grafo de Ativos & Direitos SPDX",
                component="graph.knowledge",
                source="portfolio.asset_graph",
                span=6,
                priority=2,
            ),
            GenUIWindow(
                id="capital-flow",
                title="Fluxo de Capital em Movimento",
                component="capital.flow",
                source="capital.flows",
                span=6,
                priority=3,
            ),
            GenUIWindow(
                id="evidence",
                title="Inspeção de Evidências & Rastreabilidade",
                component="evidence.inspector",
                source="selection.evidence_and_rights",
                span=8,
                priority=1,
            ),
            GenUIWindow(
                id="next-actions",
                title="Fila de Tarefas Executáveis",
                component="task.queue",
                source="plan.next_actions",
                span=4,
                priority=2,
            ),
        ]

        links = [
            GenUILink(
                **{
                    "from": "portfolio.selection",
                    "to": "decision.selection",
                    "event": "selection.changed",
                }
            ),
            GenUILink(
                **{
                    "from": "decision.selection",
                    "to": "radial-profile.target",
                    "event": "selection.changed",
                }
            ),
            GenUILink(
                **{
                    "from": "asset-graph.selection",
                    "to": "evidence.target",
                    "event": "selection.changed",
                }
            ),
            GenUILink(
                **{
                    "from": "alchemical-emblem.lottie_params",
                    "to": "portfolio.filter",
                    "event": "lottie.parameterized",
                }
            ),
        ]

        actions = [
            GenUIAction(
                id="opportunity.simulate",
                label="Simular Alocação de Orçamento",
                kind="invoke",
                permission="capital:simulate",
                confirmation="none",
            ),
            GenUIAction(
                id="lottie.parameterize",
                label="Parametrizar Infográfico Lottie via JSON",
                kind="invoke",
                permission="lottie:parameterize",
                confirmation="none",
            ),
            GenUIAction(
                id="rights.audit",
                label="Aprovar Limpeza de Licenças SPDX",
                kind="mutate",
                permission="rights:audit",
                confirmation="required",
            ),
            GenUIAction(
                id="treasury.allocate",
                label="Confirmar Alocação e Registrar Experimento",
                kind="mutate",
                permission="capital:allocate",
                confirmation="required",
            ),
        ]

        envelope = GenUIEnvelope(
            version="0.1",
            id=spec.spec_id,
            mode=GenUIMode.INTERACTIVE,
            intent=spec.interpreted_intent,
            surface=GenUISurface.WORKSPACE,
            layout=layout if layout in REGISTERED_LAYOUTS else "capital-workbench",
            state_scope=GenUIStateScope.WORKSPACE,
            windows=windows,
            links=links,
            actions=actions,
            fallback=GenUIFallback(
                mode="markdown",
                summary=sc.instant_view.headline_signal,
            ),
        )
        return GenUIDocument(prose_markdown=prose, envelope=envelope)

    @staticmethod
    def to_declarative_spec(
        doc: GenUIDocument,
        perspective: PersonaPerspective = PersonaPerspective.EXECUTIVE,
    ) -> DeclarativeUISpecification:
        """
        Converte um `GenUIDocument` validado (UI IR) para uma `DeclarativeUISpecification`
        da Camada 5, mapeando o componente prioritário para `VisualRepresentationType`.
        """
        from pixelcoin.layer4_orchestrator import PixelCoinOrchestrator

        orch = PixelCoinOrchestrator()
        comp_map = {
            "alchemical.emblem": VisualRepresentationType.ALCHEMICAL_EMBLEM,
            "puxer.matrix": VisualRepresentationType.ALCHEMICAL_EMBLEM,
            "lottie.infographic": VisualRepresentationType.ALCHEMICAL_EMBLEM,
            "chart.radial": VisualRepresentationType.RADIAL_PROFILE,
            "graph.knowledge": VisualRepresentationType.KNOWLEDGE_GRAPH,
            "graph.dependencies": VisualRepresentationType.KNOWLEDGE_GRAPH,
            "portfolio.mosaic": VisualRepresentationType.PORTFOLIO_MOSAIC,
            "decision.matrix": VisualRepresentationType.DECISION_MATRIX,
            "capital.flow": VisualRepresentationType.CAPITAL_FLOW,
            "treasury.summary": VisualRepresentationType.CAPITAL_FLOW,
        }

        override_rep: Optional[VisualRepresentationType] = None
        if doc.envelope.windows:
            first_comp = doc.envelope.windows[0].component
            override_rep = comp_map.get(first_comp)

        spec = orch.generate_ui_spec(
            prompt=doc.envelope.intent,
            perspective=perspective,
            override_representation=override_rep,
        )
        spec.spec_id = doc.envelope.id
        spec.visual_payloads["genui_md_envelope"] = doc.envelope.model_dump(mode="json", by_alias=True)
        spec.visual_payloads["genui_md_serialized"] = GenUIMDParser.serialize(doc)
        return spec
