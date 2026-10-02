"""Builds the portfolio sample: a capability statement for a FICTIONAL company.

Output: high-ticket/demo-site/company-profile.pdf (served next to the demo website).
Run: python3 build_samples.py
"""
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate, NextPageTemplate

from pdf_kit import (
    A4, CONTENT_W, MARGIN, PAGE_H, PAGE_W, PageBreak, Paragraph, Spacer, Table, TableStyle, mm,
)

NAVY = colors.HexColor("#0B2A3C")
NAVY2 = colors.HexColor("#133A52")
AMBER = colors.HexColor("#F2A541")
AMBER_DK = colors.HexColor("#D98A1F")
INK = colors.HexColor("#14212B")
MUTED = colors.HexColor("#5B6B77")
LINE = colors.HexColor("#E3DED3")
SOFT = colors.HexColor("#F6F4EF")

base = dict(fontName="Sans", fontSize=9.4, leading=13.6, textColor=INK)
st = {
    "body": ParagraphStyle("b", **base),
    "pt": ParagraphStyle("pt", **{**base, "textColor": MUTED, "fontSize": 8.6, "leading": 12.4}),
    "label": ParagraphStyle("l", **{**base, "fontName": "Sans-Bold", "fontSize": 8, "textColor": AMBER_DK}),
    "h": ParagraphStyle("h", **{**base, "fontName": "Sans-Bold", "fontSize": 17, "leading": 21,
                                "textColor": NAVY, "spaceAfter": 2}),
    "hsub": ParagraphStyle("hs", **{**base, "fontSize": 9, "textColor": MUTED, "spaceAfter": 8}),
    "card_h": ParagraphStyle("ch", **{**base, "fontName": "Sans-Bold", "fontSize": 10, "textColor": NAVY}),
    "cell": ParagraphStyle("c", **{**base, "fontSize": 8.6, "leading": 11.6}),
    "cellh": ParagraphStyle("chh", **{**base, "fontName": "Sans-Bold", "fontSize": 8.6, "leading": 11.6,
                                      "textColor": colors.white}),
}
SAMPLE = "SAMPLE DOCUMENT · fictional company created for portfolio purposes · not a real business"


def cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canv.setStrokeColor(colors.Color(0.95, 0.65, 0.25, alpha=0.18))
    canv.setLineWidth(60)
    canv.circle(PAGE_W - 30 * mm, PAGE_H - 40 * mm, 70 * mm, fill=0, stroke=1)
    canv.setFillColor(AMBER)
    canv.rect(MARGIN, PAGE_H - 62 * mm, 14 * mm, 14 * mm, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.setFont("Sans-Bold", 22)
    canv.drawCentredString(MARGIN + 7 * mm, PAGE_H - 57.5 * mm, "E")
    canv.setFillColor(colors.white)
    canv.setFont("Sans-Bold", 30)
    canv.drawString(MARGIN, PAGE_H - 95 * mm, "Exemplo Engenharia")
    canv.drawString(MARGIN, PAGE_H - 108 * mm, "& Serviços, Lda")
    canv.setFillColor(AMBER)
    canv.setFont("Sans-Bold", 13)
    canv.drawString(MARGIN, PAGE_H - 126 * mm, "CAPABILITY STATEMENT 2026")
    canv.setFillColor(colors.Color(1, 1, 1, alpha=0.75))
    canv.setFont("Sans", 12)
    canv.drawString(MARGIN, PAGE_H - 134 * mm, "Perfil de Capacidades 2026")
    canv.setFont("Sans", 11)
    for i, line in enumerate([
        "Civil works · Equipment rental · Logistics",
        "Camp services · HSE & training · Facilities maintenance",
        "Energy · Mining · Infrastructure",
    ]):
        canv.drawString(MARGIN, PAGE_H - (160 + i * 8) * mm, line)
    canv.setFillColor(colors.white)
    canv.setFont("Sans-Bold", 10)
    canv.drawString(MARGIN, 52 * mm, "100% Mozambican-owned  ·  Maputo  ·  Pemba  ·  Tete")
    canv.setFont("Sans", 9.5)
    canv.setFillColor(colors.Color(1, 1, 1, alpha=0.75))
    canv.drawString(MARGIN, 44 * mm, "Av. Exemplo 123, Maputo  ·  info@example.com  ·  +258 00 000 0000")
    canv.setFillColor(AMBER)
    canv.rect(0, 0, PAGE_W, 14 * mm, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.setFont("Sans-Bold", 8)
    canv.drawCentredString(PAGE_W / 2, 5.5 * mm, SAMPLE)
    canv.restoreState()


def inner(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Sans-Bold", 8.5)
    canv.drawString(MARGIN, PAGE_H - 7.5 * mm, "EXEMPLO ENGENHARIA & SERVIÇOS, LDA")
    canv.setFillColor(AMBER)
    canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 7.5 * mm, "CAPABILITY STATEMENT 2026")
    canv.setFillColor(MUTED)
    canv.setFont("Sans", 7)
    canv.drawString(MARGIN, 9 * mm, SAMPLE)
    canv.drawRightString(PAGE_W - MARGIN, 9 * mm, f"{doc.page}")
    canv.setStrokeColor(LINE)
    canv.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canv.restoreState()


def heading(en, pt):
    return [Paragraph(en, st["h"]), Paragraph(pt, st["hsub"])]


def table(rows, widths, head=True):
    data = [[Paragraph(str(c), st["cellh"] if head and i == 0 else st["cell"]) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths)
    style = [("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    for r in range(2 if head else 1, len(rows), 2):
        style.append(("BACKGROUND", (0, r), (-1, r), SOFT))
    t.setStyle(TableStyle(style))
    return t


def cards(items, cols=2):
    cw = CONTENT_W / cols
    cells = []
    for title, en, pt in items:
        cells.append([Paragraph(title, st["card_h"]), Spacer(1, 3), Paragraph(en, st["body"]),
                      Spacer(1, 2), Paragraph(pt, st["pt"])])
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    t = Table(rows, colWidths=[cw] * cols)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE), ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("LINEABOVE", (0, 0), (-1, 0), 2.5, AMBER),
    ]))
    return t


story = [NextPageTemplate("inner"), PageBreak()]

# ---- Page 2: overview
story += heading("Company overview", "Apresentação da empresa")
story.append(Paragraph(
    "Exemplo Engenharia &amp; Serviços, Lda is a Mozambican-owned engineering and site-services company "
    "founded in 2015, with bases in Maputo, Pemba and Tete. We support energy, mining and infrastructure "
    "projects with civil works, equipment rental, logistics and camp services, delivered by a 90% Mozambican "
    "workforce to international health, safety and quality standards.", st["body"]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "A Exemplo Engenharia &amp; Serviços, Lda é uma empresa moçambicana de engenharia e serviços de apoio a obras, "
    "fundada em 2015, com bases em Maputo, Pemba e Tete. Apoiamos projectos de energia, mineração e "
    "infra-estruturas com obras civis, aluguer de equipamentos, logística e serviços de acampamento.", st["pt"]))
story.append(Spacer(1, 10))
story.append(table([
    ["Key facts · Dados principais", ""],
    ["Legal name", "Exemplo Engenharia &amp; Serviços, Lda"],
    ["Founded", "2015 · Maputo, Mozambique"],
    ["Ownership", "100% Mozambican"],
    ["Workforce", "120+ employees · 90% Mozambican nationals"],
    ["Bases", "Maputo (head office) · Pemba (Cabo Delgado) · Tete"],
    ["Sectors", "Energy (oil &amp; gas) · Mining · Infrastructure · Ports &amp; logistics"],
    ["Working languages", "Portuguese · English"],
], [45 * mm, CONTENT_W - 45 * mm]))
story.append(Spacer(1, 12))
story += heading("Why work with us", "Porquê trabalhar connosco")
story.append(cards([
    ("Local content partner", "Mozambican-owned, locally registered, hiring and training in the communities where we work.",
     "Empresa moçambicana, com contratação e formação nas comunidades onde trabalhamos."),
    ("International standards", "HSE procedures aligned with ISO 45001; quality plans and reports for every contract.",
     "Procedimentos de HSE alinhados com a ISO 45001; planos e relatórios de qualidade em cada contrato."),
    ("Own fleet", "Our own equipment and maintenance workshop mean fewer delays and predictable costs.",
     "Frota e oficina próprias: menos atrasos e custos previsíveis."),
    ("Bilingual reporting", "Daily and monthly reports in Portuguese and English for international project teams.",
     "Relatórios diários e mensais em português e inglês."),
]))

# ---- Page 3: capabilities + equipment
story.append(PageBreak())
story += heading("Core capabilities", "Capacidades principais")
story.append(cards([
    ("Civil works · Obras civis", "Access roads, platforms, drainage, foundations, fencing and light structures.",
     "Estradas de acesso, plataformas, drenagem, fundações, vedações e estruturas ligeiras."),
    ("Equipment rental · Aluguer de equipamentos", "Earthmoving, lifting and power equipment, with certified operators.",
     "Equipamento de terraplenagem, elevação e energia, com operadores certificados."),
    ("Logistics · Logística", "Cargo transport, site deliveries and warehousing between ports and project sites.",
     "Transporte de carga, entregas em obra e armazenagem entre portos e projectos."),
    ("Camp services · Acampamentos", "Catering, cleaning, laundry and maintenance for camps of up to 500 people.",
     "Catering, limpeza, lavandaria e manutenção para acampamentos até 500 pessoas."),
    ("HSE &amp; training · Formação", "Site induction, first aid, working at height and defensive driving.",
     "Indução, primeiros socorros, trabalho em altura e condução defensiva."),
    ("Facilities · Manutenção", "Electrical, plumbing and preventive maintenance of offices, camps and yards.",
     "Electricidade, canalização e manutenção preventiva de instalações."),
]))
story.append(Spacer(1, 12))
story += heading("Equipment &amp; resources", "Equipamentos e recursos")
story.append(table([
    ["Equipment · Equipamento", "Capacity · Capacidade", "Units · Unidades"],
    ["Hydraulic excavators", "20–30 t", "4"],
    ["Backhoe loaders", "8 t", "6"],
    ["Tipper trucks", "10–15 m³", "12"],
    ["Mobile cranes", "25 t", "2"],
    ["4x4 light vehicles", "Double cab, fitted for site use", "15"],
    ["Generators", "20–250 kVA", "10"],
], [70 * mm, 70 * mm, CONTENT_W - 140 * mm]))

# ---- Page 4: HSE, compliance, projects, contact
story.append(PageBreak())
story += heading("Health, safety, environment &amp; quality", "Saúde, segurança, ambiente e qualidade")
story.append(table([
    ["Practice · Prática", "How we apply it · Como aplicamos"],
    ["HSE policy", "Signed by management, reviewed yearly, shared with every worker at induction"],
    ["Daily controls", "Toolbox talks, job hazard analysis and a stop-work policy for everyone on site"],
    ["Performance", "1.2 million work hours without a lost-time incident (example figure)"],
    ["Environment", "Waste segregation, spill kits on every site, community grievance channel"],
], [45 * mm, CONTENT_W - 45 * mm]))
story.append(Spacer(1, 10))
story += heading("Compliance documents", "Documentação legal (disponível a pedido)")
story.append(table([
    ["Document · Documento", "Status"],
    ["Certidão de Registo Comercial", "Available on request"],
    ["NUIT (tax identification number)", "Available on request"],
    ["Alvará (activity / construction licence)", "Available on request"],
    ["Certidão de Quitação: tax and social security (INSS)", "Available on request"],
    ["Insurance: public liability and workers' compensation", "Available on request"],
], [CONTENT_W - 45 * mm, 45 * mm]))
story.append(Spacer(1, 10))
story += heading("Selected project experience", "Experiência seleccionada (projectos de exemplo)")
story.append(table([
    ["Project · Projecto", "Location", "Year", "Client type"],
    ["14 km access road rehabilitation", "Cabo Delgado", "2024", "International contractor"],
    ["Equipment and operators for port works", "Nacala", "2025", "Logistics operator"],
    ["Camp support for 300 people", "Tete", "2023–25", "Mining services company"],
], [72 * mm, 32 * mm, 22 * mm, CONTENT_W - 126 * mm]))
story.append(Spacer(1, 12))
contact = Table([[Paragraph(
    "<font color='#F2A541'><b>CONTACT · CONTACTO</b></font><br/>"
    "<font color='white'>Av. Exemplo 123, Maputo, Mozambique  ·  info@example.com  ·  +258 00 000 0000</font>",
    ParagraphStyle("ct", **{**base, "leading": 15}))]], colWidths=[CONTENT_W])
contact.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY2), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                             ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
story.append(contact)

doc = BaseDocTemplate("high-ticket/demo-site/company-profile.pdf", pagesize=A4,
                      title="Exemplo Engenharia & Serviços: Capability Statement (sample)",
                      author="Portfolio sample", subject=SAMPLE)
doc.addPageTemplates([
    PageTemplate("cover", [Frame(MARGIN, MARGIN, CONTENT_W, PAGE_H - 2 * MARGIN)], onPage=cover),
    PageTemplate("inner", [Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 34 * mm)], onPage=inner),
])
doc.build(story)
print("OK company-profile.pdf")
