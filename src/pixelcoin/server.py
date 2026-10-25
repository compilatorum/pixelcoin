"""
Servidor HTTP & Renderizador Interativo do PixelCoin.

Exponibiliza:
- `GET /` — Interface Web Generativa interativa (Camada 6 Web)
- `GET /api/spec` — Especificação declarativa atual da UI (Camada 5 JSON)
- `GET /api/org` — Relatório renderizado em Emacs Org-mode (Camada 6 Emacs)
- `GET /api/mobile` — Payload enxuto para Mobile / Microinterface (Camada 6 Mobile)
- `GET /api/agent` — Envelope JSON-LD para Agentes Conversacionais (Camada 6 A2A)
- `POST /api/prompt` — Gera uma nova Especificação de UI a partir de um prompt e perspectiva (Camada 4)
- `POST /api/simulate` — Simula alocação de recursos sob restrição orçamentária (Camada 3, Modo Simulação)
- `POST /api/action` — Executa uma ação controlada autorizada (ex: auditar licença SPDX ou registrar resultado de experimento) com verificação Human-in-the-Loop
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from pixelcoin.layer4_orchestrator import CANONICAL_PROMPTS, PixelCoinOrchestrator
from pixelcoin.layer5_ui_spec import (
    ALLOWED_DECLARATIVE_ACTIONS,
    FORBIDDEN_UNCONTROLLED_OPERATIONS,
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
from pixelcoin.mcp_server import PixelCoinMCPBridge


ORCHESTRATOR = PixelCoinOrchestrator()
MCP_BRIDGE = PixelCoinMCPBridge()
DEFAULT_PROMPT = CANONICAL_PROMPTS[0]["prompt"]


class PixelCoinHTTPHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: Any) -> None:
        raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_text(self, status: int, content: str, content_type: str = "text/plain; charset=utf-8") -> None:
        raw = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        spec = ORCHESTRATOR.generate_ui_spec(DEFAULT_PROMPT)
        if self.path in ("/", "/index.html"):
            html = WebGenerativeRenderer.render_html(spec)
            self._send_text(200, html, "text/html; charset=utf-8")
            return
        if self.path == "/api/spec":
            self._send_json(200, spec.model_dump(mode="json"))
            return
        if self.path == "/api/org":
            org_doc = EmacsOrgRenderer.render(spec)
            self._send_text(200, org_doc, "text/org; charset=utf-8")
            return
        if self.path == "/api/mobile":
            self._send_json(200, MobileMicroRenderer.render(spec))
            return
        if self.path == "/api/agent":
            self._send_json(200, AgentConversationalRenderer.render(spec))
            return
        if self.path == "/api/mcp/tools":
            self._send_json(200, {"tools": MCP_BRIDGE.list_tools()})
            return
        self._send_json(
            200,
            {
                "service": "PixelCoin Generative UI, Alchemical Emblems & LottieMCP Server",
                "version": "0.4.0",
                "endpoints": [
                    "GET /",
                    "GET /api/spec",
                    "GET /api/org",
                    "GET /api/mobile",
                    "GET /api/agent",
                    "GET /api/mcp/tools",
                    "POST /api/prompt",
                    "POST /api/simulate",
                    "POST /api/lottie/parameterize",
                    "POST /api/mcp/call",
                    "POST /api/action",
                ],
            },
        )

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
            if self.path == "/api/prompt":
                prompt = body.get("prompt", DEFAULT_PROMPT)
                persp_str = body.get("perspective", "executiva")
                perspective = PersonaPerspective(persp_str)
                rep_str = body.get("override_representation")
                override_rep = VisualRepresentationType(rep_str) if rep_str else None
                budget = float(body.get("budget_limit_brl", 1500.0))
                spec = ORCHESTRATOR.generate_ui_spec(
                    prompt=prompt,
                    perspective=perspective,
                    override_representation=override_rep,
                    budget_limit_brl=budget,
                )
                self._send_json(200, spec.model_dump(mode="json"))
                return

            if self.path == "/api/simulate":
                budget = float(body.get("budget_brl", 1500.0))
                selected_ids = body.get("selected_experiment_ids")
                sim = ORCHESTRATOR.economics.simulate_allocation(
                    budget_brl=budget,
                    selected_experiment_ids=selected_ids,
                )
                self._send_json(200, sim)
                return

            if self.path == "/api/lottie/parameterize":
                template_id = body.get("template_id", "alchemical_emblem")
                params_json = body.get("params_json", {})
                res = MCP_BRIDGE.call_tool(
                    "lottie_parameterize_template",
                    {"template_id": template_id, "params_json": params_json},
                )
                self._send_json(200, res)
                return

            if self.path == "/api/mcp/call":
                tool_name = body.get("name", "")
                tool_args = body.get("arguments", {})
                res = MCP_BRIDGE.call_tool(tool_name, tool_args)
                self._send_json(200, res)
                return

            if self.path == "/api/action":
                action_type = body.get("action_type", "")
                if action_type in FORBIDDEN_UNCONTROLLED_OPERATIONS or action_type not in ALLOWED_DECLARATIVE_ACTIONS:
                    raise PixelCoinGuardrailError(
                        f"Operação bloqueada pelos Guardrails da Seção 7: '{action_type}' não é uma ação autorizada."
                    )
                human_confirmed = bool(body.get("human_confirmed", False))
                if not human_confirmed:
                    self._send_json(
                        403,
                        {
                            "guardrail_blocked": True,
                            "reason": "Separação entre análise e execução: mutações de estado exigem human_confirmed=True.",
                        },
                    )
                    return

                if action_type == "audit_artifact_rights":
                    artifact_id = body.get("artifact_id", "art:wordsmith_ingestor")
                    new_spdx = body.get("new_spdx", "MIT")
                    audit_note = body.get("audit_note", "Direitos esclarecidos e manifesto assinado.")
                    updated = ORCHESTRATOR.graph.resolve_artifact_rights(
                        artifact_id=artifact_id,
                        new_spdx=new_spdx,
                        audit_note=audit_note,
                        source_id="src:repo:license_manifest",
                    )
                    self._send_json(200, {"status": "ok", "updated_artifact": updated.model_dump(mode="json")})
                    return

                if action_type == "register_experiment_result":
                    exp_id = body.get("experiment_id", "exp:A_validar_demanda_curadoria")
                    outcome = body.get("outcome_summary", "2 pilotos pagos confirmados na rodada de entrevistas.")
                    cost = float(body.get("realized_cost_brl", 420.0))
                    rev = float(body.get("realized_revenue_brl", 1200.0))
                    rec = ORCHESTRATOR.economics.record_experiment_result(
                        experiment_id=exp_id,
                        outcome_summary=outcome,
                        realized_cost_brl=cost,
                        realized_revenue_brl=rev,
                    )
                    self._send_json(200, {"status": "ok", "recorded": rec})
                    return

                self._send_json(200, {"status": "ok", "action_type": action_type})
                return

            self._send_json(404, {"error": "Endpoint not found"})
        except PixelCoinGuardrailError as exc:
            self._send_json(403, {"guardrail_blocked": True, "detail": str(exc)})
        except Exception as exc:
            self._send_json(400, {"error": str(exc)})


def run_server(host: str = "127.0.0.1", port: int = 8090) -> None:
    server = HTTPServer((host, port), PixelCoinHTTPHandler)
    print(f"🪙 PixelCoin Generative UI Server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start PixelCoin Generative UI Server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
