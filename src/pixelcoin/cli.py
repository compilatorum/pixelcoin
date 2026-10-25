"""
CLI do PixelCoin — Interface de Linha de Comando e Gerador Multi-Ambiente.

Exemplos de uso:
  python -m pixelcoin prompt "Tenho pouco orçamento para desenvolver o Compilatorum. Compare minhas opções e encontre a ação que mais reduz incerteza por unidade de recurso."
  python -m pixelcoin render --surface org --output relatorio_pixelcoin.org
  python -m pixelcoin render --surface web --output dist/pixelcoin_generative_ui.html
  python -m pixelcoin render --surface mobile
  python -m pixelcoin render --surface agent
  python -m pixelcoin server --port 8090
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Optional

from pixelcoin.genui_md import GenUIEnvelope, GenUIMDAdapter, GenUIMDParser, GenUIMode
from pixelcoin.layer4_orchestrator import CANONICAL_PROMPTS, PixelCoinOrchestrator
from pixelcoin.layer5_ui_spec import PersonaPerspective
from pixelcoin.layer6_renderers import (
    AgentConversationalRenderer,
    EmacsOrgRenderer,
    MobileMicroRenderer,
    WebGenerativeRenderer,
)
from pixelcoin.mcp_server import PixelCoinMCPBridge, run_stdio_mcp_server
from pixelcoin.server import run_server


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pixelcoin",
        description="PixelCoin — Interface Generativa de Inteligência Econômica do Compilatorum",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Subcomando: prompt
    p_prompt = sub.add_parser("prompt", help="Gera a especificação declarativa de UI a partir de um prompt")
    p_prompt.add_argument(
        "query",
        nargs="?",
        default=CANONICAL_PROMPTS[0]["prompt"],
        help="Intenção / pergunta em linguagem natural",
    )
    p_prompt.add_argument(
        "--perspective",
        choices=["executiva", "desenvolvedor", "cientifica"],
        default="executiva",
        help="Perspectiva de síntese (executiva, desenvolvedor, cientifica)",
    )
    p_prompt.add_argument(
        "--budget",
        type=float,
        default=1500.0,
        help="Orçamento disponível para simulação de experimentos em R$",
    )

    # Subcomando: render
    p_render = sub.add_parser("render", help="Renderiza a interface para Web, Emacs Org-mode, GenUI-MD, Mobile ou Agentes")
    p_render.add_argument(
        "--surface",
        choices=["web", "org", "genui-md", "mobile", "agent"],
        default="org",
        help="Ambiente alvo de renderização (Camada 6 / GenUI-MD)",
    )
    p_render.add_argument(
        "--prompt",
        default=CANONICAL_PROMPTS[0]["prompt"],
        help="Prompt que orienta a geração da interface",
    )
    p_render.add_argument(
        "--perspective",
        choices=["executiva", "desenvolvedor", "cientifica"],
        default="executiva",
    )
    p_render.add_argument(
        "--output",
        help="Arquivo de saída opcional (ex: dist/pixelcoin_generative_ui.html ou relatorio.org)",
    )

    # Subcomando: server
    p_server = sub.add_parser("server", help="Inicia o servidor HTTP Generativo do PixelCoin")
    p_server.add_argument("--host", default="127.0.0.1")
    p_server.add_argument("--port", type=int, default=8090)

    # Subcomando: lottie
    p_lottie = sub.add_parser("lottie", help="Parametriza templates Lottie/Vetoriais via JSON ou exporta o pacote completo")
    p_lottie.add_argument(
        "--template",
        choices=["alchemical_emblem", "radial_profile", "knowledge_graph", "portfolio_mosaic", "decision_matrix", "capital_flow"],
        default="alchemical_emblem",
        help="Estrutura de infográfico Lottie a parametrizar",
    )
    p_lottie.add_argument(
        "--params",
        default="{}",
        help="JSON de parâmetros quantitativos para atualizar o Lottie",
    )
    p_lottie.add_argument(
        "--export-dir",
        help="Diretório opcional para exportar todos os 6 arquivos .lottie.json e o emblema .svg",
    )

    # Subcomando: mcp
    p_mcp = sub.add_parser("mcp", help="Inicia o servidor LottieMCP / CreatorMCP via stdio ou lista ferramentas")
    p_mcp.add_argument("--list-tools", action="store_true", help="Lista os schemas das ferramentas LottieMCP / CreatorMCP")

    # Subcomando: genui
    p_genui = sub.add_parser("genui", help="Gera, valida ou exporta o JSON Schema da especificação GenUI-MD")
    p_genui.add_argument("--prompt", default=CANONICAL_PROMPTS[0]["prompt"], help="Prompt para compor o documento GenUI-MD")
    p_genui.add_argument("--mode", choices=["text", "interactive"], default="interactive", help="Modo do envelope GenUI-MD")
    p_genui.add_argument("--layout", default="capital-workbench", help="Layout multi-janela registrado")
    p_genui.add_argument("--validate-file", help="Valida um arquivo .md contendo um bloco :::genui")
    p_genui.add_argument("--export-schema", help="Exporta o JSON Schema formal do envelope GenUI-MD para o arquivo indicado")
    p_genui.add_argument("--output", help="Salva a saída GenUI-MD gerada em arquivo")

    args = parser.parse_args(argv)
    orchestrator = PixelCoinOrchestrator()
    mcp_bridge = PixelCoinMCPBridge()

    if args.command == "prompt":
        spec = orchestrator.generate_ui_spec(
            prompt=args.query,
            perspective=PersonaPerspective(args.perspective),
            budget_limit_brl=args.budget,
        )
        print(json.dumps(spec.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0

    if args.command == "render":
        spec = orchestrator.generate_ui_spec(
            prompt=args.prompt,
            perspective=PersonaPerspective(args.perspective),
        )
        if args.surface == "web":
            rendered = WebGenerativeRenderer.render_html(spec)
        elif args.surface == "org":
            rendered = EmacsOrgRenderer.render(spec)
        elif args.surface == "genui-md":
            rendered = spec.visual_payloads.get("genui_md_serialized", "")
        elif args.surface == "mobile":
            rendered = json.dumps(MobileMicroRenderer.render(spec), ensure_ascii=False, indent=2)
        else:
            rendered = json.dumps(AgentConversationalRenderer.render(spec), ensure_ascii=False, indent=2)

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(rendered, encoding="utf-8")
            print(f"[PixelCoin] Interface '{args.surface}' salva em: {out_path}")
        else:
            print(rendered)
        return 0

    if args.command == "server":
        run_server(host=args.host, port=args.port)
        return 0

    if args.command == "lottie":
        if args.export_dir:
            exported = mcp_bridge.export_all_templates_to_disk(Path(args.export_dir))
            print(json.dumps({"exported_files": exported}, ensure_ascii=False, indent=2))
            return 0
        params_dict = json.loads(args.params)
        rendered_lottie = mcp_bridge.call_tool(
            "lottie_parameterize_template",
            {"template_id": args.template, "params_json": params_dict},
        )
        print(json.dumps(rendered_lottie, ensure_ascii=False, indent=2))
        return 0

    if args.command == "mcp":
        if args.list_tools:
            print(json.dumps({"tools": mcp_bridge.list_tools()}, ensure_ascii=False, indent=2))
            return 0
        run_stdio_mcp_server()
        return 0

    if args.command == "genui":
        if args.export_schema:
            schema_path = Path(args.export_schema)
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema_json = json.dumps(GenUIEnvelope.model_json_schema(by_alias=True), ensure_ascii=False, indent=2)
            schema_path.write_text(schema_json, encoding="utf-8")
            print(f"[PixelCoin GenUI-MD] JSON Schema exportado em: {schema_path}")
            return 0
        if args.validate_file:
            md_content = Path(args.validate_file).read_text(encoding="utf-8")
            doc = GenUIMDParser.parse(md_content)
            adapted = GenUIMDAdapter.to_declarative_spec(doc)
            print(
                json.dumps(
                    {
                        "valid": True,
                        "id": doc.envelope.id,
                        "mode": doc.envelope.mode.value,
                        "windows_count": len(doc.envelope.windows),
                        "links_count": len(doc.envelope.links),
                        "adapted_spec_id": adapted.spec_id,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        spec = orchestrator.generate_ui_spec(prompt=args.prompt)
        doc = GenUIMDAdapter.from_declarative_spec(
            spec,
            mode=GenUIMode(args.mode),
            layout=args.layout,
        )
        serialized = GenUIMDParser.serialize(doc)
        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(serialized, encoding="utf-8")
            print(f"[PixelCoin GenUI-MD] Documento salvo em: {out_p}")
        else:
            print(serialized)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
