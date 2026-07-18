"""Generate the editable, AWS-style AgentCore trading architecture diagram."""

from pathlib import Path
from urllib.parse import quote
import base64
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
ICONS = ROOT / "icons"
OUTPUT = ROOT / "strands-trader-agentcore.drawio"
PREVIEW = ROOT / "strands-trader-agentcore.svg"
WIDTH, HEIGHT = 1435, 755


def svg_uri(filename: str) -> str:
    return "data:image/svg+xml," + quote((ICONS / filename).read_text(encoding="utf-8"), safe="")


def png_as_svg_uri(filename: str) -> str:
    """Wrap an official PNG in SVG so draw.io receives a safe percent-encoded URI."""
    data = base64.b64encode((ICONS / filename).read_bytes()).decode("ascii")
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 460"><image width="460" height="460" href="data:image/png;base64,{data}"/></svg>'
    return "data:image/svg+xml," + quote(svg, safe="")


def generate() -> None:
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="Codex", version="26.0.16")
    diagram = ET.SubElement(mxfile, "diagram", id="agentcore-trader", name="AWS AgentCore Trading Architecture")
    model = ET.SubElement(diagram, "mxGraphModel", dx=str(WIDTH), dy=str(HEIGHT), grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(WIDTH), pageHeight=str(HEIGHT), math="0", shadow="0")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    def vertex(cid, value, x, y, w, h, style):
        cell = ET.SubElement(root, "mxCell", id=cid, value=value, style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})

    def box(cid, value, x, y, w, h, fill="#F2F3F3", stroke="#161E2D", size=15):
        vertex(cid, value, x, y, w, h, f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1.5;fontSize={size};fontColor=#161E2D;align=left;spacingLeft=12;")

    def text(cid, value, x, y, w, h, size=16, bold=False, align="center", color="#161E2D"):
        vertex(cid, value, x, y, w, h, f"text;html=1;align={align};verticalAlign=middle;fontSize={size};fontStyle={1 if bold else 0};fontColor={color};whiteSpace=wrap;")

    def icon(cid, value, filename, x, y, w=100, h=100, image_size=62):
        vertex(cid, value, x, y, w, h, "shape=label;html=1;verticalAlign=bottom;align=center;imageAlign=center;imageVerticalAlign=top;" f"image={svg_uri(filename)};imageWidth={image_size};imageHeight={image_size};fontSize=14;fontColor=#161E2D;spacingBottom=0;")

    def routed_edge(cid, start, end, points=(), dashed=False, both=False, color="#161E2D"):
        """Create an explicitly routed connector so draw.io cannot overlap lanes."""
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor={color};endArrow=block;endFill=1;"
        if both:
            style += "startArrow=block;startFill=1;"
        if dashed:
            style += "dashed=1;dashPattern=6 4;"
        cell = ET.SubElement(root, "mxCell", id=cid, value="", style=style, edge="1", parent="1")
        geometry = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        ET.SubElement(geometry, "mxPoint", x=str(start[0]), y=str(start[1]), **{"as": "sourcePoint"})
        ET.SubElement(geometry, "mxPoint", x=str(end[0]), y=str(end[1]), **{"as": "targetPoint"})
        if points:
            array = ET.SubElement(geometry, "Array", **{"as": "points"})
            for x, y in points:
                ET.SubElement(array, "mxPoint", x=str(x), y=str(y))

    # AWS Cloud boundary and its reference-style header.
    vertex("aws", "", 195, 18, 810, 705, "rounded=0;html=1;fillColor=#FFFFFF;strokeColor=#161E2D;strokeWidth=2;")
    vertex("aws-tab", "", 195, 18, 52, 49, "rounded=0;html=1;fillColor=#232F3E;strokeColor=#232F3E;")
    vertex("aws-logo", "", 202, 27, 38, 30, f"shape=image;html=1;imageAspect=0;aspect=fixed;image={svg_uri('AWS-Cloud-logo_32_Dark.svg')};")
    text("aws-title", "AWS Cloud", 260, 24, 145, 32, 20, True, "left")

    # User and request/response lanes.
    vertex("user", "user", 35, 120, 68, 96, "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fontSize=15;fontStyle=1;fontColor=#161E2D;strokeColor=#161E2D;strokeWidth=2;")

    # AgentCore Runtime.
    vertex("runtime", "", 310, 58, 630, 300, "rounded=0;html=1;fillColor=#FFFFFF;strokeColor=#5147D9;strokeWidth=2;")
    icon("runtime-icon", "", "Arch_Amazon-Bedrock-AgentCore_64.svg", 322, 67, 52, 52, 48)
    text("runtime-title", "AgentCore Runtime", 380, 68, 210, 34, 19, False, "left")
    vertex("trading-agent-card", "", 320, 120, 125, 150, "rounded=1;arcSize=8;html=1;fillColor=#FFFFFF;strokeColor=#161E2D;strokeWidth=1.5;")
    vertex("agent", "", 342, 132, 80, 80, f"shape=image;html=1;imageAspect=0;aspect=fixed;image={png_as_svg_uri('strands-agents-official.png')};")
    text("agent-label", "Trading Agent", 325, 220, 115, 35, 16, True)
    text("agent-role", "Orchestrator", 325, 245, 115, 18, 11, False, "center", "#545B64")
    vertex("research-agent-card", "", 785, 120, 125, 150, "rounded=1;arcSize=8;html=1;fillColor=#FAF7FF;strokeColor=#5147D9;strokeWidth=2;")
    vertex("research-agent", "", 807, 132, 80, 80, f"shape=image;html=1;imageAspect=0;aspect=fixed;image={png_as_svg_uri('strands-agents-official.png')};")
    text("research-agent-label", "Research Agent", 790, 220, 115, 35, 16, True, "center", "#5147D9")
    text("research-agent-role", "Specialist", 790, 245, 115, 18, 11, False, "center", "#545B64")

    vertex("trader-tools", "", 480, 110, 270, 215, "rounded=0;html=1;fillColor=#FFFFFF;strokeColor=#879596;strokeWidth=1;")
    text("trader-tools-title", "Trading Agent tools", 490, 113, 165, 22, 14, True, "left")
    box("tool-account", "account_report()", 495, 139, 240, 25, "#F2F3F3", "#161E2D", 12)
    box("tool-buy", "buy_shares()", 495, 168, 240, 25, "#F2F8F0", "#3F8624", 12)
    box("tool-sell", "sell_shares()", 495, 197, 240, 25, "#F2F8F0", "#3F8624", 12)
    box("tool-strategy", "change_strategy()", 495, 226, 240, 25, "#F2F3F3", "#161E2D", 12)
    box("tool-price", "lookup_share_price()", 495, 255, 240, 25, "#F2F3F3", "#161E2D", 12)
    box("tool-telegram", "send_telegram_message()", 495, 284, 240, 25, "#F2F3F3", "#161E2D", 12)
    routed_edge("agent-research-tool", (445, 145), (785, 145), ((460, 145), (460, 103), (770, 103), (770, 145)))
    routed_edge("agent-trader-tools", (445, 195), (480, 195))
    routed_edge("question", (120, 163), (310, 163))
    routed_edge("response", (310, 186), (120, 186))
    text("question-label", "User question", 145, 130, 145, 27, 16, True)
    text("response-label", "Agent response", 145, 190, 145, 27, 16, True)
    box("research-tool-label", "research_agent()<br>Agent-as-Tool", 600, 64, 165, 34, "#F5F3FF", "#5147D9", 10)

    # MCP server is deliberately external to the AWS Cloud boundary.
    vertex("mcp", "", 1060, 120, 345, 272, "rounded=0;html=1;fillColor=#FFFFFF;strokeColor=#161E2D;strokeWidth=2;")
    text("mcp-name", "Research tools", 1080, 128, 175, 34, 21, False, "left", "#5147D9")
    text("mcp-title", "MCP Server", 1260, 128, 125, 34, 17, True, "right")
    box("mcp-news", "search_financial_news()", 1095, 195, 275, 40)
    routed_edge("research-agent-mcp", (910, 145), (1060, 205), ((1040, 145), (1040, 205)))

    # Supporting AWS services and dashed control-plane flows.
    icon("bedrock", "Amazon Bedrock<br>LLMs", "Arch_Amazon-Bedrock_64.svg", 330, 535, 120, 112, 68)
    icon("dynamodb", "Amazon DynamoDB<br>Portfolio state", "Arch_Amazon-DynamoDB_64.svg", 615, 535, 135, 112, 68)
    routed_edge("agent-bedrock", (390, 270), (390, 535), ((390, 420),), dashed=True)
    routed_edge("agent-state", (420, 270), (682, 535), ((420, 415), (682, 415)), dashed=True)
    text("bedrock-flow-label", "Invokes LLM and<br>processes outputs", 230, 345, 190, 60, 16, True)
    text("state-flow-label", "Retrieve account and<br>previous trades", 455, 345, 195, 60, 16, True)

    ET.indent(mxfile, space="  ")
    ET.ElementTree(mxfile).write(OUTPUT, encoding="utf-8", xml_declaration=True)
    render_preview(root)
    workshop_images = ROOT.parent / "workshop" / "static" / "images"
    if workshop_images.exists():
        shutil.copy2(OUTPUT, workshop_images / OUTPUT.name)
        shutil.copy2(PREVIEW, workshop_images / PREVIEW.name)
    print(f"Generated {OUTPUT}")


def render_preview(graph_root: ET.Element) -> None:
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(WIDTH), height=str(HEIGHT), viewBox=f"0 0 {WIDTH} {HEIGHT}")
    defs = ET.SubElement(svg, "defs")
    for marker_id, color in (("arrow", "#161E2D"), ("purple-arrow", "#5147D9")):
        marker = ET.SubElement(defs, "marker", id=marker_id, markerWidth="8", markerHeight="8", refX="7", refY="4", orient="auto", markerUnits="strokeWidth")
        ET.SubElement(marker, "path", d="M0,0 L8,4 L0,8 Z", fill=color)
    ET.SubElement(svg, "rect", x="0", y="0", width=str(WIDTH), height=str(HEIGHT), fill="#ffffff")
    cells = {c.get("id"): c for c in graph_root.findall("mxCell")}

    def geo(c):
        g = c.find("mxGeometry")
        return tuple(float(g.get(k, "0")) for k in ("x", "y", "width", "height"))

    def styles(c):
        return {k: v for item in c.get("style", "").split(";") if "=" in item for k, v in [item.split("=", 1)]}

    def label(value, x, y, w, h, size=14, bold=False, color="#161E2D", align="center"):
        lines = str(value).replace("<br>", "\n").replace("<br/>", "\n").splitlines() or [""]
        anchor, tx = ("start", x + 8) if align == "left" else (("end", x + w - 8) if align == "right" else ("middle", x + w / 2))
        t = ET.SubElement(svg, "text", x=str(tx), y=str(y + h / 2 - (len(lines) - 1) * 9 + 5), fill=color, **{"font-family": "Arial, sans-serif", "font-size": str(size), "font-weight": "bold" if bold else "normal", "text-anchor": anchor})
        for i, line in enumerate(lines):
            span = ET.SubElement(t, "tspan", x=str(tx), dy="0" if i == 0 else "18")
            span.text = line

    # Nodes first; edges then appear above shapes, matching AWS reference diagrams.
    for c in cells.values():
        if c.get("vertex") != "1":
            continue
        x, y, w, h = geo(c)
        s = styles(c)
        raw = c.get("style", "")
        if "shape=image" in raw or "shape=label" in raw:
            image = s.get("image")
            image_size = float(s.get("imageWidth", min(w, h)))
            if image:
                ET.SubElement(svg, "image", href=image, x=str(x + (w-image_size)/2), y=str(y), width=str(image_size), height=str(image_size))
            if c.get("value"):
                label(c.get("value"), x, y + image_size, w, h-image_size, int(s.get("fontSize", "14")))
        elif "shape=umlActor" in raw:
            cx=x+w/2
            ET.SubElement(svg, "circle", cx=str(cx), cy=str(y+20), r="14", fill="none", stroke="#161E2D", **{"stroke-width":"2"})
            ET.SubElement(svg, "line", x1=str(cx), y1=str(y+34), x2=str(cx), y2=str(y+65), stroke="#161E2D", **{"stroke-width":"2"})
            ET.SubElement(svg, "line", x1=str(cx-22), y1=str(y+46), x2=str(cx+22), y2=str(y+46), stroke="#161E2D", **{"stroke-width":"2"})
            ET.SubElement(svg, "line", x1=str(cx), y1=str(y+65), x2=str(cx-18), y2=str(y+83), stroke="#161E2D", **{"stroke-width":"2"})
            ET.SubElement(svg, "line", x1=str(cx), y1=str(y+65), x2=str(cx+18), y2=str(y+83), stroke="#161E2D", **{"stroke-width":"2"})
            label(c.get("value"), x, y+78, w, 24, 15, True)
        elif "text" in raw:
            label(c.get("value"), x, y, w, h, int(s.get("fontSize", "16")), s.get("fontStyle") == "1", s.get("fontColor", "#161E2D"), s.get("align", "center"))
        else:
            ET.SubElement(svg, "rect", x=str(x), y=str(y), width=str(w), height=str(h), fill=s.get("fillColor", "#fff"), stroke=s.get("strokeColor", "#161E2D"), **{"stroke-width": s.get("strokeWidth", "1.5")})
            if c.get("value"):
                label(c.get("value"), x, y, w, h, int(s.get("fontSize", "15")), False, s.get("fontColor", "#161E2D"), s.get("align", "center"))

    for c in cells.values():
        if c.get("edge") != "1":
            continue
        geometry = c.find("mxGeometry")
        source = geometry.find("mxPoint[@as='sourcePoint']")
        target = geometry.find("mxPoint[@as='targetPoint']")
        waypoint_array = geometry.find("Array[@as='points']")
        route = [(source.get("x"), source.get("y"))]
        if waypoint_array is not None:
            route.extend((point.get("x"), point.get("y")) for point in waypoint_array.findall("mxPoint"))
        route.append((target.get("x"), target.get("y")))
        s = styles(c)
        attrs={"points":" ".join(f"{x},{y}" for x, y in route),"fill":"none","stroke":s.get("strokeColor", "#161E2D"),"stroke-width":"2","marker-end":"url(#arrow)"}
        if s.get("dashed") == "1":
            attrs["stroke-dasharray"] = "7 6"
        if s.get("startArrow") == "block":
            attrs["marker-start"] = "url(#arrow)"
        ET.SubElement(svg, "polyline", **attrs)

    ET.indent(svg, space="  ")
    ET.ElementTree(svg).write(PREVIEW, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    generate()
