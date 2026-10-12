from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
import re
import re

ROOT = Path(__file__).parent
OUT = ROOT / "cloudops-01-monitoring-guide.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Subtitle2", parent=styles["BodyText"], fontSize=12, leading=15, textColor="#455a64", spaceAfter=10))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontSize=17, leading=21, textColor="#17365d", spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontSize=13, leading=16, textColor="#17365d", spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.2, leading=12.5, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontSize=8, leading=10, textColor="#455a64", spaceAfter=5))
styles.add(ParagraphStyle(name="Codex", parent=styles["Code"], fontName="Courier", fontSize=7.1, leading=8.6, leftIndent=8, rightIndent=8, backColor="#f3f6f8", borderColor="#c8d0d6", borderWidth=.4, borderPadding=6, spaceBefore=4, spaceAfter=7))



def clean_inline(value):
    value = value.replace("&", "&amp;")
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"<font name='Courier' color='#263238'>\1</font>", value)
    return value



def clean_inline(value):
    value = value.replace("&", "&amp;")
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"<font name='Courier' color='#263238'>\1</font>", value)
    return value

def add_md(path):
    out = []
    code, in_code = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            if in_code:
                out += [Preformatted("\n".join(code), styles["Codex"]), Spacer(1, 4)]
                code, in_code = [], False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line); continue
        if not line.strip(): out.append(Spacer(1, 3)); continue
        if line.startswith("# "): out.append(Paragraph(line[2:], styles["H1x"])); continue
        if line.startswith("## "): out.append(Paragraph(line[3:], styles["H2x"])); continue
        if line.startswith("- "): out.append(Paragraph("&#8226; " + line[2:], styles["Bodyx"])); continue
        out.append(Paragraph(clean_inline(line), styles["Bodyx"]))
    return out

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=.62*inch, leftMargin=.62*inch, topMargin=.55*inch, bottomMargin=.5*inch)
story = [Paragraph("CloudOps 01 Monitoring and Incident Response", styles["Title"]), Paragraph("Detailed Console walkthrough, visual sequence, and completed evidence", styles["Subtitle2"]), Paragraph("Complete this exercise in a dedicated nonproduction AWS account in us-east-1 using synthetic data. No CLI profile is required for the Console-first run.", styles["Bodyx"])]
flow = Table([["Readiness", "Logs + IAM", "Lambda", "Dashboard + alarm", "Failure", "Recovery"], ["account", "1-day logs", "deploy", "Errors metric", "In alarm", "OK"]], colWidths=[1.08*inch]*6)
flow.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365d")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#e8f1f8")), ("GRID", (0,0), (-1,-1), .4, colors.HexColor("#9eabb5")), ("ALIGN", (0,0), (-1,-1), "CENTER"), ("FONTSIZE", (0,0), (-1,-1), 7.5), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
handler = (ROOT / "src" / "lambda_function.py").read_text(encoding="utf-8")
handler_block = Table([[Preformatted(handler, styles["Codex"])]], colWidths=[6.95*inch])
handler_block.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f3f6f8")), ("BOX", (0,0), (-1,-1), .4, colors.HexColor("#c8d0d6")), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7)]))
story += [flow, Spacer(1, 10), Paragraph("Copy-paste Lambda handler", styles["H1x"]), Paragraph("Save this file as lambda_function.py at the root of the deployment package and keep the handler setting lambda_function.lambda_handler.", styles["Bodyx"]), handler_block, Spacer(1, 8)] + add_md(ROOT / "walkthrough.md") + [PageBreak(), Paragraph("AWS CLI equivalent", styles["H1x"])] + add_md(ROOT / "cli-equivalent.md") + [PageBreak(), Paragraph("Completed evidence", styles["H1x"])] + add_md(ROOT / "evidence.md")
story.append(Paragraph("The chat screenshots showed the Hello World response, the corrected RuntimeError response, the wrong metric-name configuration, the corrected Errors alarm in alarm, and the final recovered OK state. Original chat image attachments were not available as local files for direct embedding; these states are preserved in the visual flow and evidence record.", styles["Smallx"]))
doc.build(story)
print(OUT)
