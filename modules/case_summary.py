"""
NyayaSathi - Case Summary PDF Export Module
Generates a structured, professional case summary report in PDF format using ReportLab.
Contains Issue Summary, Laws, Action Plan, Evidence Checklist, and Helplines.
"""

import io
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def generate_case_summary_pdf(
    title: str,
    problem_text: str,
    category_name: str,
    urgency_badge: str,
    ai_analysis_text: str,
    action_plan: List[Dict[str, Any]],
    checklist: List[Dict[str, Any]],
    created_at: str = None
) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "SumHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0F2942"),
        alignment=1,
        spaceAfter=4
    )

    tagline_style = ParagraphStyle(
        "SumTagline",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#8C7030"),
        alignment=1,
        spaceAfter=10
    )

    sec_title_style = ParagraphStyle(
        "SumSecTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F2942"),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "SumBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#212529"),
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        "SumMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A5F")
    )

    disclaimer_style = ParagraphStyle(
        "SumDisc",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#6c757d"),
        spaceBefore=8
    )

    date_str = created_at or datetime.now().strftime("%d-%B-%Y %I:%M %p")
    story = []

    # Title & Branding
    story.append(Paragraph("NYAYASATHI LEGAL CASE SUMMARY", header_style))
    story.append(Paragraph("Know Your Rights. Take Your Next Step. | Citizen Legal Guidance Dossier", tagline_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#D4AF37"), spaceAfter=10))

    # Meta Table
    meta_data = [
        [Paragraph(f"<b>Case Title:</b> {title}", meta_style), Paragraph(f"<b>Date:</b> {date_str}", meta_style)],
        [Paragraph(f"<b>Category:</b> {category_name}", meta_style), Paragraph(f"<b>Urgency:</b> {urgency_badge}", meta_style)]
    ]
    t = Table(meta_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Reported Grievance
    story.append(Paragraph("1. REPORTED CITIZEN GRIEVANCE", sec_title_style))
    clean_prob = problem_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    story.append(Paragraph(clean_prob[:800] + ("..." if len(clean_prob) > 800 else ""), body_style))
    story.append(Spacer(1, 6))

    # AI Analysis & Statutory Guidance
    story.append(Paragraph("2. STATUTORY GUIDANCE & LEGAL ANALYSIS", sec_title_style))
    for p_line in ai_analysis_text.split("\n"):
        p_clean = p_line.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if not p_clean:
            continue
        if p_clean.startswith("#") or p_clean.startswith("**"):
            story.append(Paragraph(f"<b>{p_clean.replace('#', '').replace('*', '')}</b>", sec_title_style))
        else:
            story.append(Paragraph(p_clean.replace("*", ""), body_style))
    story.append(Spacer(1, 6))

    # Action Plan
    if action_plan:
        story.append(Paragraph("3. RECOMMENDED SEQUENTIAL ACTION PLAN", sec_title_style))
        for step in action_plan[:5]:
            step_num = step.get("step", "•")
            title_text = step.get("title", "").replace("&", "&amp;")
            desc_text = step.get("description", "").replace("&", "&amp;")
            time_text = step.get("timeframe", "")
            time_str = f" <i>[{time_text}]</i>" if time_text else ""
            story.append(Paragraph(f"<b>Step {step_num}: {title_text}</b>{time_str}", body_style))
            if desc_text:
                story.append(Paragraph(f"{desc_text}", body_style))
        story.append(Spacer(1, 6))

    # Evidence Checklist
    if checklist:
        story.append(Paragraph("4. EVIDENCE CHECKLIST TO PRESERVE", sec_title_style))
        for ev in checklist[:8]:
            item_text = ev.get("item", ev.get("item_text", str(ev))).replace("&", "&amp;")
            imp_text = ev.get("importance", "")
            imp_str = f" <b>({imp_text})</b>" if imp_text else ""
            story.append(Paragraph(f"• {item_text}{imp_str}", body_style))
        story.append(Spacer(1, 6))

    # Official Helplines
    story.append(Paragraph("5. DESIGNATED NATIONAL HELPLINES & PORTALS", sec_title_style))
    story.append(Paragraph("• <b>1930</b> - National Cyber Crime Helpline (cybercrime.gov.in)", body_style))
    story.append(Paragraph("• <b>112</b> - Emergency Police & Safety Response Services", body_style))
    story.append(Paragraph("• <b>15100</b> - NALSA National Free Legal Aid Helpline (nalsa.gov.in)", body_style))
    story.append(Paragraph("• <b>1915</b> - National Consumer Helpline (consumerhelpline.gov.in)", body_style))
    story.append(Spacer(1, 6))

    # Disclaimer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceBefore=6, spaceAfter=4))
    story.append(Paragraph(
        "⚖️ DISCLAIMER: This document is generated for informational and educational purposes by NyayaSathi. "
        "It does not constitute formal legal counsel or create an attorney-client relationship. Citizens are advised "
        "to consult an enrolled advocate or District Legal Services Authority (DLSA) for formal legal representation.",
        disclaimer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
