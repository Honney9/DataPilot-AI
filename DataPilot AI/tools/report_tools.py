from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os


def generate_pdf(report, session_id):
    os.makedirs("outputs/reports", exist_ok=True)

    file_path = f"outputs/reports/{session_id}.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    # 🎨 Custom styles
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=14)
    heading_style = ParagraphStyle("HeadingStyle", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor("#333"))
    body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontSize=10.5, leading=14)

    content = []

    # ✅ Title
    content.append(Paragraph(f"<b>{report['title']}</b>", title_style))

    # ✅ Date (formatted)
    formatted_date = datetime.fromisoformat(report["generated_at"]).strftime("%B %d, %Y %I:%M %p")
    content.append(Paragraph(f"<i>Generated: {formatted_date}</i>", styles["Normal"]))
    content.append(Spacer(1, 20))

    # ✅ Sections
    for section in report["sections"]:
        content.append(Paragraph(f"<b>{section['title']}</b>", heading_style))
        content.append(Spacer(1, 8))

        body_text = section["body"].replace("\n", "<br/>")
        content.append(Paragraph(body_text, body_style))
        content.append(Spacer(1, 16))

        content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        content.append(Spacer(1, 12))

    doc.build(content)

    return file_path