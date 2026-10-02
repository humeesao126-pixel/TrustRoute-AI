import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

os.makedirs("tests", exist_ok=True)
styles = getSampleStyleSheet()

# Custom styles for clean, corporate document look
title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Heading1"],
    fontSize=18,
    leading=22,
    textColor=colors.HexColor("#0f172a"),
    fontName="Helvetica-Bold",
    alignment=1
)

sub_style = ParagraphStyle(
    "DocSub",
    parent=styles["Normal"],
    fontSize=10,
    leading=13,
    textColor=colors.HexColor("#475569"),
    fontName="Helvetica",
    alignment=1
)

body_style = ParagraphStyle(
    "DocBody",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    textColor=colors.HexColor("#1e293b"),
    fontName="Helvetica"
)

bold_style = ParagraphStyle(
    "DocBold",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    textColor=colors.HexColor("#0f172a"),
    fontName="Helvetica-Bold"
)

# -----------------------------------------------------------------------------
# PDF 1: High-Risk Deceptive Offer (Bavaria Cloud Solutions GmbH)
# -----------------------------------------------------------------------------
def make_pdf_1():
    doc = SimpleDocTemplate("tests/1_suspicious_offer.pdf", pagesize=letter, rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph("BAVARIA CLOUD SOLUTIONS GMBH", title_style))
    story.append(Paragraph("Commercial Register: HRB 94821 B | Amtsgericht Charlottenburg (Berlin)", sub_style))
    story.append(Paragraph("Friedrichstraße 120, 10117 Berlin, Germany", sub_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1")))
    story.append(Spacer(1, 15))

    story.append(Paragraph("OFFICIAL APPOINTMENT LETTER & VISA SPONSORSHIP", bold_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Dear Candidate,<br/>We are pleased to formally offer you the following employment position with Bavaria Cloud Solutions GmbH under the specialized German immigration framework:", body_style))
    story.append(Spacer(1, 10))

    data = [
        [Paragraph("<b>Position:</b>", body_style), Paragraph("Cloud Support Associate", body_style)],
        [Paragraph("<b>Duty Station:</b>", body_style), Paragraph("Berlin, Germany", body_style)],
        [Paragraph("<b>Stated Visa Route:</b>", body_style), Paragraph("EU Blue Card Fast Track", body_style)],
        [Paragraph("<b>Offered Annual Salary:</b>", body_style), Paragraph("€26,000 gross per annum", body_style)],
        [Paragraph("<b>Working Hours:</b>", body_style), Paragraph("40 Hours / Week", body_style)],
    ]
    t = Table(data, colWidths=[160, 340])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Facilitation Agency & Embassy Protocol:</b>", bold_style))
    story.append(Paragraph("This offer is processed exclusively via our regional intermediary partner: <b>Rawal Global Consultants</b> (Pakistani OEP License: <b>4521/RWP</b>).", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Special Mandatory Processing Clause:</b><br/>To guarantee your expedited German consulate visa interview appointment slot and document attestation clearance, a refundable security processing bond of <b>PKR 280,000</b> must be remitted within 48 hours. Funds must be transferred via personal IBAN / JazzCash Account: <b>PK36MEZN00012345678901</b>.<br/>Official Inquiry Contact: recruiter.nexus@gmail.com", body_style))
    
    story.append(Spacer(1, 25))
    story.append(Paragraph("Authorized Signatory:<br/><b>Dr. Marcus Weber</b><br/>Director Human Resources", body_style))

    doc.build(story)

# -----------------------------------------------------------------------------
# PDF 2: Verified Corporate Offer (Siemens Healthineers GmbH)
# -----------------------------------------------------------------------------
def make_pdf_2():
    doc = SimpleDocTemplate("tests/2_verified_enterprise_offer.pdf", pagesize=letter, rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph("SIEMENS HEALTHINEERS GMBH", title_style))
    story.append(Paragraph("Commercial Register: HRB 21400 | Amtsgericht Munich", sub_style))
    story.append(Paragraph("Henkestraße 127, 91052 Erlangen / Munich, Germany", sub_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1")))
    story.append(Spacer(1, 15))

    story.append(Paragraph("EMPLOYMENT AGREEMENT & REGULATORY RELOCATION TERMS", bold_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Dear Candidate,<br/>Siemens Healthineers GmbH is pleased to extend this formal offer of permanent employment in our Munich development center.", body_style))
    story.append(Spacer(1, 10))

    data = [
        [Paragraph("<b>Job Title:</b>", body_style), Paragraph("Junior Software Engineer", body_style)],
        [Paragraph("<b>Location:</b>", body_style), Paragraph("Munich, Germany", body_style)],
        [Paragraph("<b>Intended Visa Track:</b>", body_style), Paragraph("EU Blue Card (Fachkräfteeinwanderungsgesetz)", body_style)],
        [Paragraph("<b>Total Base Pay:</b>", body_style), Paragraph("€58,500 gross per annum", body_style)],
        [Paragraph("<b>Contract Type:</b>", body_style), Paragraph("Full-time, Permanent (40 Hours/Week)", body_style)],
    ]
    t = Table(data, colWidths=[160, 340])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Authorized Recruitment Channel:</b>", bold_style))
    story.append(Paragraph("Regional liaison services are coordinated through: <b>Al-Saqib Overseas Promoters</b> (BEOE License: <b>1234/LHR</b>). All operations comply strictly with the Pakistan Emigration Ordinance and German labor standards.", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Compliance & Payment Policy:</b><br/>In accordance with ethical recruitment principles, Siemens Healthineers covers all consular filing costs, visa processing vouchers, and relocation tickets directly. No candidate-side advance cash fees, personal deposits, or facilitation commissions are permitted.<br/>Contact: careers@siemens-healthineers.com", body_style))

    story.append(Spacer(1, 25))
    story.append(Paragraph("Authorized Corporate Representative:<br/><b>Elena Schneider</b><br/>Head of Global Talent Acquisition", body_style))

    doc.build(story)

# -----------------------------------------------------------------------------
# PDF 3: Ambiguous Offer / Company in Liquidation (Apex Logistik UG)
# -----------------------------------------------------------------------------
def make_pdf_3():
    doc = SimpleDocTemplate("tests/3_ambiguous_liquidation_offer.pdf", pagesize=letter, rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=40)
    story = []

    story.append(Paragraph("APEX LOGISTIK UG", title_style))
    story.append(Paragraph("Commercial Register: HRB 10293 | Amtsgericht Frankfurt am Main", sub_style))
    story.append(Paragraph("Hanauer Landstraße 45, 60314 Frankfurt, Germany", sub_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1")))
    story.append(Spacer(1, 15))

    story.append(Paragraph("PROVISIONAL LETTER OF INTENT FOR EMPLOYMENT", bold_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Dear Applicant,<br/>This letter serves as provisional confirmation of employment intent for logistics dispatch coordination:", body_style))
    story.append(Spacer(1, 10))

    data = [
        [Paragraph("<b>Job Role:</b>", body_style), Paragraph("Warehouse Dispatch Coordinator", body_style)],
        [Paragraph("<b>City / Station:</b>", body_style), Paragraph("Frankfurt am Main, Germany", body_style)],
        [Paragraph("<b>Visa Classification:</b>", body_style), Paragraph("General Skilled Work Permit", body_style)],
        [Paragraph("<b>Base Salary:</b>", body_style), Paragraph("€32,000 gross per annum", body_style)],
        [Paragraph("<b>Hours:</b>", body_style), Paragraph("Full-Time (38.5 Hours/Week)", body_style)],
    ]
    t = Table(data, colWidths=[160, 340])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Processing Terms & Advisory:</b>", bold_style))
    story.append(Paragraph("Intermediary hiring facilitation is handled by: <b>Direct Overseas Hiring Desk</b> (No OEP License number provided in records).", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Attestation Expense:</b><br/>A nominal documentation fee of <b>PKR 75,000</b> is required for state translation and consular dispatch, payable via official bank counter cash voucher before contract dispatch.", body_style))

    story.append(Spacer(1, 25))
    story.append(Paragraph("Issued by:<br/><b>H. Becker</b><br/>Operations Manager", body_style))

    doc.build(story)

if __name__ == "__main__":
    make_pdf_1()
    make_pdf_2()
    make_pdf_3()
    print("3 PDF test dossiers created inside 'tests/' folder:")
    print(" - tests/1_suspicious_offer.pdf")
    print(" - tests/2_verified_enterprise_offer.pdf")
    print(" - tests/3_ambiguous_liquidation_offer.pdf")