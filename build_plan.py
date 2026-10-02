"""Builds 24h-cash-sprint.pdf (tickable checklist) and scripts-copy-paste.md.

Run: python3 build_plan.py
"""
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak, Flowable, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                              italic="Sans", boldItalic="Sans-Bold")

INK = colors.HexColor("#1B1B1B")
MUTED = colors.HexColor("#5A5A5A")
TEAL = colors.HexColor("#0F4C5C")
AMBER = colors.HexColor("#E36414")
RED = colors.HexColor("#9A031E")
PAPER = colors.HexColor("#F4F1EA")
LINE = colors.HexColor("#D6D2C8")
GREENBG = colors.HexColor("#E8F1EF")

base = dict(fontName="Sans", textColor=INK, leading=13, fontSize=9.2, alignment=TA_LEFT)
S = {
    "body": ParagraphStyle("body", **base),
    "small": ParagraphStyle("small", **{**base, "fontSize": 8, "leading": 10.5, "textColor": MUTED}),
    "h1": ParagraphStyle("h1", **{**base, "fontName": "Sans-Bold", "fontSize": 15, "leading": 19,
                                  "textColor": colors.white}),
    "h2": ParagraphStyle("h2", **{**base, "fontName": "Sans-Bold", "fontSize": 11.5, "leading": 15,
                                  "textColor": TEAL, "spaceBefore": 8, "spaceAfter": 4}),
    "h3": ParagraphStyle("h3", **{**base, "fontName": "Sans-Bold", "fontSize": 9.6, "leading": 13,
                                  "spaceBefore": 6, "spaceAfter": 2}),
    "time": ParagraphStyle("time", **{**base, "fontName": "Sans-Bold", "textColor": TEAL}),
    "script": ParagraphStyle("script", **{**base, "fontSize": 8.9, "leading": 12.4}),
    "cell": ParagraphStyle("cell", **{**base, "fontSize": 8.4, "leading": 11}),
    "cellb": ParagraphStyle("cellb", **{**base, "fontName": "Sans-Bold", "fontSize": 8.4, "leading": 11}),
    "title": ParagraphStyle("title", **{**base, "fontName": "Sans-Bold", "fontSize": 26, "leading": 30,
                                        "textColor": colors.white}),
    "subtitle": ParagraphStyle("subtitle", **{**base, "fontSize": 10.5, "leading": 14,
                                              "textColor": colors.white}),
}

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
INNER_W = CONTENT_W - 16  # inside box() padding


class CheckBox(Flowable):
    """Clickable AcroForm checkbox: tick it in Chrome/Edge/Acrobat, or print and tick by pen."""
    count = 0

    def __init__(self, size=10.5):
        super().__init__()
        self.size = size
        self.width = self.height = size

    def draw(self):
        CheckBox.count += 1
        self.canv.acroForm.checkbox(
            name=f"cb{CheckBox.count}", x=0, y=0, size=self.size, buttonStyle="check",
            borderColor=TEAL, fillColor=colors.white, textColor=TEAL, borderWidth=1,
            forceBorder=True, relative=True, tooltip="Tick when done")


def P(text, style="body"):
    return Paragraph(text, S[style])


def band(text, color=TEAL):
    t = Table([[P(text, "h1")]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def box(flowables, bg=PAPER, border=LINE):
    t = Table([[flowables]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.6, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def checklist(rows, with_time=True, width=CONTENT_W):
    """rows: list of (time, text). Each row gets a clickable checkbox."""
    data, widths = [], ([7 * mm, 15 * mm, width - 22 * mm] if with_time
                        else [7 * mm, width - 7 * mm])
    for time, text in rows:
        cells = [CheckBox()]
        if with_time:
            cells.append(P(time, "time"))
        cells.append(P(text))
        data.append(cells)
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (0, -1), 0), ("TOPPADDING", (0, 0), (0, -1), 5),
    ]))
    return t


HEADER = ParagraphStyle("hdr", parent=S["cellb"], textColor=colors.white)


def grid(data, widths, header_bg=TEAL, zebra=True, font="cell"):
    rows = [[c if isinstance(c, Flowable)
             else Paragraph(str(c), HEADER) if i == 0 else P(str(c), font)
             for c in row] for i, row in enumerate(data)]
    t = Table(rows, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    if zebra:
        for r in range(2, len(rows), 2):
            style.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#FAF8F4")))
    t.setStyle(TableStyle(style))
    return t


def bullets(items, style="body"):
    return [P(f"<font color='#E36414'>•</font>&nbsp;&nbsp;{i}", style) for i in items]


# ---------------------------------------------------------------------------
# Copy-paste scripts (Portuguese, for customers). Shared by the PDF and the .md file.
# ---------------------------------------------------------------------------
SCRIPTS = [
    ("S1", "Warm message — individuals (send ONE BY ONE, change the name)", """Olá [Nome]! Tudo bem contigo?
Comecei a fazer CVs profissionais e cartas de candidatura, em português ou inglês, entregues em 2 horas (Word + PDF).
Preço de lançamento até amanhã: 500 MT.
Precisas, ou conheces alguém à procura de emprego ou estágio? Por cada pessoa que me indicares e fechar, ofereço-te 100 MT."""),
    ("S1-B", "Warm message — people you know who own a business", """Olá [Nome], tudo bem?
Estou a ajudar negócios a vender mais pelo WhatsApp: catálogo com preços, mensagens automáticas, cartaz com QR code e posts para o Facebook.
Preço de lançamento: 1500 MT, fica pronto hoje.
Posso mostrar-te um exemplo para o teu [negócio]?"""),
    ("S2", "WhatsApp Status #1 (11:45)", """CV PROFISSIONAL EM 2 HORAS
CV + carta de candidatura, em português ou inglês, Word + PDF.
Preço de lançamento: 500 MT (só até sábado às 12h).
Responde "CV" a este status."""),
    ("S2-2", "WhatsApp Status #2 (11:46)", """TEM UM NEGÓCIO?
Ponho o seu WhatsApp a vender: catálogo com preços, resposta automática e cartaz com QR code.
Pronto hoje. Preço de lançamento: 1500 MT.
Responda "NEGÓCIO" a este status."""),
    ("S2-3", "WhatsApp Status #3 — proof (16:15). Add a BLURRED screenshot, with the client's OK", """Mais um CV entregue hoje. Obrigado pela confiança, [primeiro nome]!
Ainda tenho vagas para hoje. Responde "CV"."""),
    ("S2-4", "WhatsApp Status #4 — deadline (19:30)", """Últimas 5 vagas para hoje.
CV + carta de candidatura: 800 MT. Só CV: 500 MT.
Pede agora: entrego hoje até às 22h ou amanhã até às 9h."""),
    ("S2-5", "WhatsApp Status #5 — final call (Sat 07:00)", """ÚLTIMO DIA do preço de lançamento: termina hoje às 12h.
CV: 500 MT | WhatsApp Business: 1500 MT | 10 posts: 1500 MT | Mini-site: 3500 MT
Responde a este status."""),
    ("S3", "Group post (only in groups you belong to, where selling is allowed — max 1 post per group)", """Bom dia a todos. Peço desculpa ao admin se não for permitido.
Faço CV profissional + carta de candidatura (português ou inglês), entregue em 2 horas: 800 MT (só CV: 500 MT).
Tenho exemplos para mostrar. Contacto por mensagem privada: [seu número]."""),
    ("S4", "Business — first WhatsApp (permission first, NO link, max 15 per hour)", """Boa tarde! Falo com a [Nome do Negócio]?
Encontrei-vos no [Google Maps / Facebook]. Chamo-me [Seu nome], sou de [cidade].
Tenho uma ideia rápida para a [Nome do Negócio] receber mais pedidos pelo WhatsApp. Posso enviar em 1 minuto?"""),
    ("S5", "Business — after they say yes", """Obrigado! Reparei que a [Nome do Negócio] [ainda não tem catálogo no WhatsApp / não tem preços visíveis / a página do Facebook não tem posts desde (mês)].
Faço hoje:
- Catálogo no WhatsApp com até 15 produtos e preços
- Mensagem automática de boas-vindas e de ausência
- Respostas rápidas para as perguntas mais frequentes
- Cartaz A4 com QR code para os clientes falarem consigo
Preço de lançamento: 1500 MT (normal: 2500 MT). Fica pronto em 3 horas.
Paga 50% para começar e 50% só depois de ver tudo pronto.
Quer ver um exemplo?"""),
    ("S6", "Follow-up — ONE time only, next morning", """Bom dia, [Nome]! Só para saber se viu a minha mensagem de ontem.
O preço de lançamento (1500 MT) termina hoje às 12h. Se não for o momento, sem problema. Obrigado!"""),
    ("S7", "Email — local business (Portuguese)", """Assunto: Ideia rápida para a [Nome do Negócio]

Bom dia,

Chamo-me [Seu nome], sou de [cidade] e ajudo negócios locais a apresentarem-se melhor online.

Vi a [Nome do Negócio] no [Google Maps / Facebook] e reparei que [observação concreta e verdadeira: o menu não está online / não há link directo para o WhatsApp / os preços não aparecem].

Posso fazer ainda esta semana:
1. WhatsApp Business com catálogo, preços e cartaz com QR code: 1500 MT
2. 10 posts prontos para o Facebook/Instagram, com legendas: 1500 MT
3. Mini-site de 1 página com botão de WhatsApp e mapa: 3500 MT

Se quiser, envio hoje um exemplo grátis com o nome da [Nome do Negócio]. Basta responder a este email ou escrever para o meu WhatsApp: [número].

Cumprimentos,
[Seu nome]
[Telefone / WhatsApp]"""),
    ("S8", "Email — tourism (lodges, guesthouses, dive centres, restaurants; English)", """Subject: Quick idea for [Business Name]'s international guests

Hi [Name],

I'm [Your name], based in [city], Mozambique. I help guesthouses and restaurants present themselves clearly to international guests.

I noticed [specific, true observation: your menu is only in Portuguese / there is no WhatsApp booking link / your price list isn't online].

I can deliver within 24 hours:
- English version of your menu, price list or booking info (from 300 MT per page)
- A one-page website with a WhatsApp booking button and map (3500 MT)
- 10 ready-to-post Facebook/Instagram posts with captions (1500 MT)

Reply "yes" and I'll send a free sample for [Business Name] today.

Best regards,
[Your name]
WhatsApp: [number]"""),
    ("S9", "Payment message (save as WhatsApp quick reply /pagar)", """Perfeito! Para começar:
Valor: [___] MT
M-Pesa: [número] - [nome exactamente como aparece]
e-Mola: [número] (se tiver)
Depois de enviar, mande-me a referência da transacção e começo logo.
Entrega: hoje até às [hora]."""),
    ("S10", "CV intake questions (send with the payment message)", """Para o seu CV, responda por favor (texto ou foto do CV antigo):
1. Nome completo, telefone, email, cidade
2. Vaga ou área que procura (e empresa, se souber)
3. Formação: escola/universidade, curso, ano
4. Experiência: empresa, cargo, datas, o que fazia (inclua estágios e voluntariado)
5. Línguas e nível
6. Informática (Word, Excel...) e carta de condução
7. Cursos e certificados
8. Quer o CV em português, inglês ou nos dois?"""),
    ("S10-B", "Business intake questions", """Para começar, envie por favor:
1. Nome do negócio, endereço e localização no Google Maps
2. Horário de funcionamento
3. Descrição curta: o que vende e o que vos torna diferentes
4. Até 15 produtos/serviços com preço e foto
5. As 5 perguntas que os clientes fazem mais
6. Formas de pagamento e se fazem entregas
7. Logotipo (se tiver)"""),
    ("S11", "Delivery + testimonial + referral", """Aqui está o seu trabalho em PDF e Word. Reveja o nome, telefone e email: se algo estiver errado, corrijo grátis hoje.
Pode deixar-me uma frase sobre o serviço? (ex.: "Rápido e bem feito")
Se conhecer alguém que precise, envie o meu contacto: por cada pessoa que fechar, ofereço-lhe 100 MT. Obrigado!"""),
    ("S12", "Objections", """"Está caro." → "Entendo. Posso fazer só o CV por 500 MT e a carta depois, se precisar." (Negócio: "Podemos começar só com o catálogo + cartaz QR por 1000 MT.")
"Vou pensar / depois." → "Claro! Só aviso que o preço de lançamento termina sábado às 12h. Quer que lhe reserve uma vaga para hoje à noite?"
"Como sei que é confiável?" → "Boa pergunta. Aqui estão exemplos do meu trabalho. Para negócios, paga 50% para começar e 50% só depois de ver tudo pronto."
"Eu faço sozinho." → "Claro que sim! A vantagem é ficar pronto hoje sem perder o seu tempo. Se mudar de ideias, estou aqui."
"Não tenho interesse." → "Obrigado pela resposta, bom dia!" (and never message again)"""),
]

PROMPTS = [
    ("A", "CV", """You are an expert recruiter in Mozambique. Using ONLY the information below, write a professional CV in [Portuguese/English] for a [target job].
Rules: never invent a job, date, degree, skill or reference. If something is missing, write [FALTA] so I can ask the client.
Sections: Dados Pessoais (only what the client gave), Perfil Profissional (3 lines), Formação Académica, Experiência Profissional (newest first, 2-3 achievement bullets each, action verbs), Competências, Línguas, Informática, Referências ("Disponíveis mediante solicitação"). Max 2 pages.
Client info: [paste]"""),
    ("B", "Cover letter", """Write a formal cover letter (carta de candidatura) in [language] for this CV, for the position [X] at [company, or "generic"]. Max 250 words, formal Mozambican Portuguese (or professional English). No invented facts.
CV: [paste]"""),
    ("C", "WhatsApp Business texts", """Write WhatsApp Business texts in Portuguese for a [business type] called [name] in [city]. Facts: [paste intake].
Produce: (1) business description, max 2 sentences; (2) greeting message for new customers, max 3 lines, with hours and how to order; (3) away message; (4) 5 quick replies with shortcut names: /precos /localizacao /horario /entrega /pagamento; (5) catalog: for each product a name (max 5 words) and a 1-line description.
Friendly and clear. Use only the facts given. No exaggerated claims."""),
    ("D", "10 social posts", """Create a 10-post plan for [business] in [city] for Facebook, Instagram and WhatsApp Status, in Portuguese.
Mix: 3 product/price posts, 2 trust posts, 2 behind-the-scenes, 2 offers with a call to action, 1 FAQ.
For each post: image headline (max 6 words) + caption (max 40 words) ending with "Encomende pelo WhatsApp: [número]". Use only these facts: [paste]"""),
    ("E", "Mini-site copy", """Write the copy for a one-page website in Portuguese for [business] in [city]. Facts: [paste].
Sections: headline (max 8 words), sub-headline (1 line), about (3 lines), services/products with prices, why choose us (3 bullets, only from the facts), hours + location, final call to action "Fale connosco no WhatsApp". No invented reviews."""),
    ("F", "Translation", """Translate the text below from [Portuguese/English] to [English/Portuguese]. Keep the meaning, names, numbers, prices and layout exactly. Use Mozambican/European Portuguese conventions. Put anything ambiguous in [brackets] so I can check.
Text: [paste]"""),
]


def script_block(code, title, text):
    body = escape(text).replace("\n", "<br/>")
    return KeepTogether([
        P(f"<font color='#E36414'>{code}</font>&nbsp;&nbsp;{escape(title)}", "h3"),
        box([P(body, "script")]),
        Spacer(1, 3),
    ])


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------
def on_page(canv, doc):
    canv.saveState()
    canv.setFont("Sans", 7.5)
    canv.setFillColor(MUTED)
    canv.drawString(MARGIN, 9 * mm, "24-Hour Cash Sprint  ·  Fri 2 Oct 11:00 → Sat 3 Oct 11:00  ·  Mozambique")
    canv.drawRightString(PAGE_W - MARGIN, 9 * mm, f"page {doc.page}")
    canv.setStrokeColor(LINE)
    canv.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canv.restoreState()


story = []

# ---- Page 1: cover + strategy ---------------------------------------------
cover = Table([[[
    P("24-HOUR CASH SPRINT", "title"), Spacer(1, 4),
    P("Laptop + WhatsApp + Email  ·  No ads  ·  Payments by M-Pesa / e-Mola / mKesh", "subtitle"),
    P("Friday 2 October 11:00  →  Saturday 3 October 11:00", "subtitle"),
]]], colWidths=[CONTENT_W])
cover.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), TEAL),
    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story += [cover, Spacer(1, 8)]

story.append(box([
    P("<b>THE PLAN IN ONE SENTENCE</b>", "h3"),
    P("Sell 3 fast, done-for-you digital services, priced in meticais and <b>paid upfront</b> by mobile "
      "money: first to people who already know you, then to local businesses. Deliver every order "
      "<b>the same day</b>, with Claude doing the heavy writing, so each happy client becomes your next "
      "Status post and referral."),
], bg=GREENBG, border=TEAL))

story.append(P("Why this is the fastest honest money from a laptop in Mozambique", "h2"))
story += bullets([
    "<b>Warm contacts buy fastest.</b> They already trust you, so you don't need ads. Your WhatsApp "
    "Status reaches everyone who saved your number, for free.",
    "<b>Demand is real today.</b> Job seekers apply by email with a CV and cover letter "
    "(emprego.co.mz listings ask for exactly that). Small businesses sell through WhatsApp and "
    "Facebook, the biggest social network in Mozambique (about 5 million users), but most have no "
    "catalogue, no price list and no website.",
    "<b>Payment is instant.</b> M-Pesa, e-Mola and mKesh settle in seconds, so there are no platform payout delays.",
    "<b>Claude does 80% of the work.</b> A CV takes about 25 minutes, a 10-post pack about 60 minutes and a mini-site about 90 minutes.",
    "<b>Early month timing.</b> Most salaries were paid in the last week of September, so people have money now.",
])

story.append(P("Money targets (honest numbers)", "h2"))
story.append(grid([
    ["Level", "Meticais", "≈ US$ (64 MT = $1)", "What it takes"],
    ["Floor: must hit", "5000 MT", "≈ $78", "10 CVs at 500, or 3 WhatsApp setups + 1 CV with letter (800)"],
    ["Target", "15 800 MT", "≈ $247", "8 CV packs (avg 600) + 3 WhatsApp setups + 2 post packs + 1 mini-site"],
    ["Stretch", "26 800+ MT", "≈ $420+", "Target + 2 full business packages (5500 each)"],
], [32 * mm, 26 * mm, 32 * mm, CONTENT_W - 90 * mm]))
story.append(Spacer(1, 4))
story.append(P("Nobody can guarantee sales. What you control is the number of messages you send, how fast "
               "you reply and how fast you deliver. Hit the activity numbers on the scoreboard and the money follows.",
               "small"))

story.append(P("What we are NOT doing (and why)", "h2"))
story += bullets([
    "<b>Fiverr/Upwork:</b> new profiles take weeks to get the first order and payouts take days.",
    "<b>Forex, crypto, betting or 'investment' groups:</b> that's gambling, and you can lose money.",
    "<b>Surveys or click-to-earn sites:</b> they pay pennies or are scams.",
    "<b>Doing students' assignments or exams:</b> that's academic fraud and it backfires. We only sell honest work.",
], "body")

# ---- Zero-mistakes rules ------------------------------------------------------------
story += [PageBreak(), band("ZERO-MISTAKES RULES: read before 11:00", RED), Spacer(1, 6)]
story.append(P("Money and scams", "h2"))
story.append(checklist([(s, t) for s, t in [
    ("1", "<b>Never start work until the money shows in YOUR M-Pesa/e-Mola SMS or app.</b> Screenshots of a "
          "'comprovativo' can be fake."),
    ("2", "<b>'I sent you money by mistake, please send it back'</b> is a classic scam. Never send money back. Tell them to "
          "ask their operator (Vodacom/Movitel/Tmcel) to reverse it."),
    ("3", "<b>Never share your PIN or any code you receive by SMS</b>, and never ask clients for theirs."),
    ("4", "<b>Log every payment immediately</b> with the name, amount, wallet, reference and time."),
    ("5", "<b>Businesses pay 50% first and 50% before the final files.</b> Show previews (screenshots) before the balance is paid."),
]]))
story.append(P("Protect your WhatsApp number (it's your whole business)", "h2"))
story.append(checklist([(s, t) for s, t in [
    ("6", "<b>No mass copy-paste.</b> Personalise the first line every time. Send at most 15 messages to new businesses per hour, "
          "and no links in the first message."),
    ("7", "WhatsApp has been rolling out <b>limits on messages to people who aren't your contacts and don't reply</b>, and many messages to "
          "new contacts in a short time can get a number restricted. That's why S4 asks a question: a reply makes "
          "it a conversation."),
    ("8", "<b>'Não tenho interesse'</b> means reply 'Obrigado, bom dia!' and never message them again. Blocks and reports "
          "get numbers banned."),
    ("9", "<b>Only post in groups where selling is allowed</b>, only once per group, and apologise to the admin."),
]]))
story.append(P("Quality and honesty", "h2"))
story.append(checklist([(s, t) for s, t in [
    ("10", "<b>Read every name, phone number, date and price twice</b> before sending."),
    ("11", "<b>Never invent experience, degrees or references</b> in a CV. Use only what the client gives you."),
    ("12", "<b>Don't promise what you can't control:</b> 'you'll get the job', 'guaranteed sales', 'sworn translation', "
           "'Google verification today'."),
    ("13", "<b>Send the right file to the right person.</b> Name every file with the client's name and check the chat header before you tap send."),
    ("14", "<b>Client data is private.</b> Never post a CV or a client's details on Status without blurring them and getting the client's OK."),
    ("15", "<b>Use only client photos or Canva free elements</b>, never images copied from Google."),
]]))
story.append(P("Energy", "h2"))
story.append(checklist([(s, t) for s, t in [
    ("16", "<b>Eat at 12:30 and 18:30. Drink water. Sleep 22:00–06:30.</b> Do one task at a time, and finish it before starting the next."),
]]))

# ---- Page 2: offer menu ------------------------------------------------------
story += [PageBreak(), band("THE OFFER MENU: copy this into your WhatsApp Business catalogue"), Spacer(1, 6)]
story.append(P("For individuals: 100% paid before you start", "h2"))
story.append(grid([
    ["#", "Offer (Portuguese name)", "What they get", "Price", "Your time"],
    ["A", "CV Express", "Professional CV, Word + PDF, delivered in 2 hours", "500 MT", "25 min"],
    ["B", "CV + Carta de candidatura", "CV + cover letter for a specific job", "800 MT", "35 min"],
    ["C", "Pacote Emprego", "CV + letter in Portuguese AND English + LinkedIn 'About' text", "1200 MT", "50 min"],
    ["D", "Tradução PT↔EN", "Simple documents, letters, emails. Not a sworn translation, so say so", "300 MT / page", "15 min / page"],
], [7 * mm, 38 * mm, 70 * mm, 24 * mm, CONTENT_W - 139 * mm]))

story.append(P("For businesses: 50% to start, 50% before final handover", "h2"))
story.append(grid([
    ["#", "Offer (Portuguese name)", "What they get", "Price", "Your time"],
    ["E", "WhatsApp Business Profissional",
     "Business profile, catalogue (up to 15 items), greeting + away messages, 5 quick replies, wa.me link + A4 QR poster",
     "1500 MT (normal 2500)", "60–90 min"],
    ["F", "Pack 10 Posts", "10 designed posts for Facebook / Instagram / Status + captions", "1500 MT", "60 min"],
    ["G", "Mini-site + QR", "1-page Google Site: WhatsApp button, prices, photos, map, plus a QR poster", "3500 MT", "90 min"],
    ["H", "Pacote Completo", "E + F + G together (saves the client 1000 MT)", "5500 MT", "3.5 h"],
    ["", "Downsell", "Catalogue + QR poster only (when they say 'too expensive')", "1000 MT", "40 min"],
], [7 * mm, 38 * mm, 70 * mm, 24 * mm, CONTENT_W - 139 * mm]))
story.append(Spacer(1, 6))
story.append(box([
    P("<b>Rules for the menu</b>", "h3"),
    *bullets([
        "Launch prices end <b>Saturday 12:00</b>. That's a real deadline, so use it in every follow-up.",
        "Promise delivery times you can beat: CV in 2 h, WhatsApp setup in 3 h, posts the same day "
        "or by 10:00 tomorrow, mini-site within 24 h. Then deliver early.",
        "Payment methods: M-Pesa (Vodacom), e-Mola (Movitel), mKesh (Tmcel) and bank transfer (NIB) as "
        "a backup. Write your number AND the account name exactly as it appears to the sender.",
        "Referral reward: 100 MT for every paid client someone sends you. Pay it the same day, because people talk.",
    ]),
]))
story.append(Spacer(1, 6))
story.append(P("Who to sell what to", "h2"))
story.append(grid([
    ["Audience", "Lead offer", "Upsell", "Channel"],
    ["Friends, family, ex-classmates, graduates, interns", "A / B (CV)", "C, D", "Personal WhatsApp + Status + groups"],
    ["People you know who own a shop, salon, restaurant or barbershop", "E (WhatsApp Business)", "F, H", "Personal WhatsApp"],
    ["Local businesses on Google Maps / Facebook", "E", "F, G, H", "WhatsApp (permission-first) + email"],
    ["Lodges, guesthouses, dive centres, restaurants with foreign guests", "D (English menu/info)", "G, F", "Email (English) + WhatsApp"],
], [58 * mm, 35 * mm, 22 * mm, CONTENT_W - 115 * mm]))

# ---- Pages 3-4: timeline checklist ---------------------------------------------
story += [PageBreak(), band("THE 24-HOUR CHECKLIST: tick every box"), Spacer(1, 6)]

story.append(P("BLOCK 1 · FRIDAY 11:00 – 12:30 · Setup + warm launch", "h2"))
story.append(checklist([
    ("11:00", "<b>WhatsApp Business profile.</b> If you already use WhatsApp Business: add a name "
              "(e.g. '[Your name] · Serviços Digitais'), a clear face photo, a description, hours and email. If you use normal "
              "WhatsApp: switching takes about 10 min and keeps your chats, but only do it if your chats are backed up. "
              "Otherwise skip this step, because the plan works on normal WhatsApp too."),
    ("11:10", "<b>Payment details ready.</b> M-Pesa number + exact account name, plus e-Mola/mKesh/NIB if you have them. "
              "Save script S9 as a quick reply (Business tools → Quick replies → '/pagar')."),
    ("11:15", "<b>Lead tracker.</b> Open Google Sheets or Excel and copy the columns from the tracker page at the end of this PDF."),
    ("11:20", "<b>Proof sample #1: your own CV.</b> Paste your real details into Claude with Prompt A, format it and export a PDF. "
              "This is your portfolio piece (keep it honest)."),
    ("11:35", "<b>Proof sample #2: 3 posts in Canva</b> for an imaginary 'Salão Exemplo' (Prompt D). Save them as images."),
    ("11:45", "<b>Post Status #1 and #2</b> (scripts S2, S2-2)."),
    ("11:50", "<b>Warm message to 40 contacts, ONE BY ONE, with their name</b> (S1 / S1-B). Start with: friends who are job-hunting, "
              "recent graduates, family, ex-classmates and people who own a business."),
    ("12:15", "<b>Post in 3–5 groups you're already in</b> where selling is allowed (S3): church, university, alumni, "
              "neighbourhood and job-seeker groups."),
    ("12:25", "<b>Reply to everyone within 5 minutes.</b> Send interested people S9 (payment) + S10 (intake) together."),
]))
story.append(Spacer(1, 4))
story.append(box([P("<b>CHECKPOINT 12:30</b>", "h3"), checklist([
    ("", "40+ personal messages sent"), ("", "2 Status posts up"), ("", "3+ group posts"),
    ("", "Replies: ______     Orders: ______     MT received: ______"),
], with_time=False, width=INNER_W)], bg=GREENBG, border=TEAL))

story.append(P("BREAK · 12:30 – 14:00", "h2"))
story.append(checklist([
    ("12:30", "Eat. Keep WhatsApp notifications ON. When someone wants to buy, send S9 + S10 only "
              "(30 seconds). Don't start the work yet."),
]))

story.append(CondPageBreak(90 * mm))
story.append(P("BLOCK 2 · FRIDAY 14:00 – 18:30 · Close, deliver, open the business pipeline", "h2"))
story.append(checklist([
    ("14:00", "<b>Clear every unread message.</b> Check each payment <b>in your own M-Pesa SMS/app</b>, not on a "
              "screenshot. Log it in the tracker."),
    ("14:10", "<b>Deliver paid CV orders</b>, oldest payment first (SOP 1, about 25 min each). Send with S11."),
    ("15:00", "<b>Build a 40-business lead list</b> from Google Maps + Facebook (search terms on the leads page). Note the "
              "name, WhatsApp, email and <i>one thing missing</i> (no catalogue, no prices, no website, dead Facebook page)."),
    ("15:30", "<b>Business WhatsApp round 1:</b> 15 permission-first messages (S4). Personalise the first line. "
              "Send no more than 15 an hour."),
    ("15:45", "<b>Email round 1:</b> 15 personalised emails (S7 local / S8 tourism), with no attachments."),
    ("16:15", "<b>Status #3: proof</b> (S2-3). Use a blurred screenshot of a delivered CV, only with the client's OK."),
    ("16:30", "<b>Close the yeses.</b> Send S5 to every business that said 'yes, send'. Collect 50%, then start (SOP 2/3/4)."),
    ("17:15", "<b>Business WhatsApp round 2:</b> the next 15 messages. Many shops close around 17:30–18:00, so send before that."),
    ("17:45", "<b>Ask every delivered client</b> for a one-line testimonial + referral (S11)."),
]))
story.append(Spacer(1, 4))
story.append(box([P("<b>CHECKPOINT 18:30</b>", "h3"), checklist([
    ("", "First 3 paid orders delivered"), ("", "30 business WhatsApps sent"), ("", "15 emails sent"),
    ("", "Replies: ______     Orders: ______     MT received: ______"),
], with_time=False, width=INNER_W)], bg=GREENBG, border=TEAL))

story.append(P("DINNER · 18:30 – 19:30", "h2"))
story.append(checklist([("18:30", "Eat, walk, drink water. Keep WhatsApp ON for buyers only.")]))

story.append(CondPageBreak(80 * mm))
story.append(P("BLOCK 3 · FRIDAY 19:30 – 22:00 · Evening push (everyone is on their phone now)", "h2"))
story.append(checklist([
    ("19:30", "<b>Status #4: deadline</b> (S2-4)."),
    ("19:35", "<b>Follow up everyone who said 'depois' / 'vou ver'</b>, one message each (S12)."),
    ("19:45", "<b>Second warm batch:</b> 30 more personal contacts you haven't messaged yet (S1 / S1-B)."),
    ("20:00", "<b>Deliver every remaining paid order</b>: CVs, translations, posts."),
    ("21:00", "<b>Email round 2:</b> 15 emails to lodges, guesthouses and restaurants (S8). They read in the morning."),
    ("21:30", "<b>Update the tracker.</b> Prepare tomorrow's list of 30 businesses. Write tomorrow's Status #5."),
    ("22:00", "<b>Stop and sleep.</b> Tired people send the wrong file to the wrong client. Sleep is part of the plan."),
]))

story.append(CondPageBreak(125 * mm))
story.append(P("BLOCK 4 · SATURDAY 06:30 – 11:00 · Morning close", "h2"))
story.append(checklist([
    ("06:30", "<b>Answer every overnight message and email.</b>"),
    ("07:00", "<b>Status #5: final call</b> (S2-5)."),
    ("07:15", "<b>One follow-up (S6)</b> to every business that read your message but didn't reply. Send only one."),
    ("08:00", "<b>Business WhatsApp round 3:</b> 15 new messages. Saturday mornings are busy, so catch owners early."),
    ("08:30", "<b>Deliver business orders</b>: WhatsApp setup calls, posts, mini-sites."),
    ("10:00", "<b>Collect every remaining 50% balance.</b> Confirm each one in your wallet before handing over the final files."),
    ("10:30", "<b>Thank every client, ask for a testimonial and offer the monthly plan:</b> 10 posts a month for 2500 MT a month. "
              "That's income for next month."),
    ("11:00", "<b>Final count.</b> Record total MT, best offer and best channel. Decide whether to run it again on Monday."),
]))
story.append(Spacer(1, 4))
story.append(box([P("<b>FINAL CHECKPOINT · SATURDAY 11:00</b>", "h3"), checklist([
    ("", "All paid orders delivered"), ("", "All balances collected and confirmed in the wallet"),
    ("", "Referral rewards paid"), ("", "TOTAL MT: ____________"),
], with_time=False, width=INNER_W)], bg=GREENBG, border=TEAL))

# ---- Scoreboard ----------------------------------------------------------------
story += [PageBreak(), band("SCOREBOARD: fill in at each checkpoint"), Spacer(1, 6)]
blank = ""
story.append(grid([
    ["Activity", "Goal by 12:30", "Actual", "Goal by 18:30", "Actual", "Goal by 22:00", "Actual", "Goal by Sat 11:00", "Actual"],
    ["Warm messages (one by one)", "40", blank, "40", blank, "70", blank, "70", blank],
    ["Status posts", "2", blank, "3", blank, "4", blank, "5", blank],
    ["Group posts", "3", blank, "5", blank, "5", blank, "5", blank],
    ["Business WhatsApps", "0", blank, "30", blank, "30", blank, "45", blank],
    ["Emails sent", "0", blank, "15", blank, "30", blank, "30", blank],
    ["Replies", "8", blank, "20", blank, "35", blank, "50", blank],
    ["Paid orders", "1", blank, "4", blank, "8", blank, "14", blank],
    ["MT received", "500", blank, "3000", blank, "8000", blank, "15 800", blank],
], [40 * mm] + [(CONTENT_W - 40 * mm) / 8] * 8, font="cell"))
story.append(Spacer(1, 6))
story.append(P("If you're behind at a checkpoint, don't panic and don't discount. Send more messages. "
               "Volume of honest, personal messages is the only lever without ads.", "small"))

story.append(P("Where to find leads (no ads)", "h2"))
story.append(P("<b>1. Your phone (the fastest money).</b> Scroll your WhatsApp contacts A→Z and mark each person: "
               "<b>J</b> = job seeker (CV), <b>N</b> = owns a business (offer E), <b>C</b> = connector who knows many "
               "people (ask for referrals)."))
story.append(Spacer(1, 3))
story.append(P("<b>2. Google Maps</b>: search these, replacing [cidade] with Maputo, Matola, Beira, Nampula, Quelimane, Tete, "
               "Chimoio, Pemba, Xai-Xai or Inhambane:"))
story.append(box([P("salão de beleza [cidade] · barbearia [cidade] · restaurante [cidade] · take away [cidade] · "
                    "pastelaria [cidade] · loja de roupa [cidade] · boutique [cidade] · ferragem [cidade] · "
                    "clínica dentária [cidade] · escola de condução [cidade] · centro de explicação [cidade] · "
                    "imobiliária [cidade] · rent a car [cidade] · lodge / guest house Tofo, Vilankulo, Bilene, "
                    "Ponta do Ouro, Inhambane", "script")]))
story.append(Spacer(1, 3))
story.append(P("<b>Pick these first:</b> they list a phone number, have good reviews (customers = money) but few photos, "
               "no website and no prices online. Note the <i>one specific thing missing</i>, because that goes in your first line."))
story.append(Spacer(1, 3))
story.append(P("<b>3. Facebook</b>: search the same terms and open Pages. The 'About' section shows WhatsApp and email. "
               "Pages that post rarely or post poor images are perfect leads for the 10-post pack."))
story.append(Spacer(1, 3))
story.append(P("<b>4. Email leads</b>: lodges, guesthouses, restaurants, private schools and clinics that show an email on "
               "Maps, Facebook or their website. Use English (S8) for tourism businesses with foreign guests."))

# ---- Scripts ---------------------------------------------------------------------
story += [PageBreak(), band("COPY-PASTE SCRIPTS (Portuguese, for your customers)"), Spacer(1, 4)]
story.append(P("Replace everything in [brackets]. Never send a script with a [bracket] left in it. Personalise the "
               "first line every time, because identical messages to many people get WhatsApp numbers banned. All scripts are "
               "also in <b>scripts-copy-paste.md</b> so you can copy them without broken line breaks.", "small"))
story.append(Spacer(1, 4))
for code, title, text in SCRIPTS:
    story.append(script_block(code, title, text))

# ---- Delivery SOPs ----------------------------------------------------------------
story += [PageBreak(), band("DELIVERY: step by step, with Claude"), Spacer(1, 4)]
story.append(P("When an order is paid, open Claude, paste the right prompt plus the client's answers, then check, "
               "format and send. <b>You</b> are responsible for the final check, so read every name, number, date and price twice.",
               "small"))

sops = [
    ("SOP 1 · CV / cover letter (25–35 min)", [
        "Payment confirmed in your wallet. Intake answers received (S10).",
        "Paste the answers into Claude with <b>Prompt A</b> (and <b>Prompt B</b> for a cover letter). Ask the client about anything marked [FALTA].",
        "Paste into Google Docs or Word using a clean 1–2 page layout. Add a photo only if the client wants one.",
        "Check the name, phone, email and dates twice. A wrong phone number means the client never gets the call.",
        "Export the PDF and DOCX, named CV_NomeApelido.pdf. Send with S11 and log it in the tracker.",
    ]),
    ("SOP 2 · WhatsApp Business setup (60–90 min)", [
        "50% confirmed. Intake received (S10-B).",
        "<b>Prompt C</b> writes the description, greeting, away message, 5 quick replies and catalogue texts.",
        "Send the texts to the owner, then do a 20-min call or visit while THEY tap: Settings → Business tools → "
        "Business profile / Catalogue / Greeting message / Away message / Quick replies. They paste, you guide.",
        "<b>Never ask for their 6-digit WhatsApp code.</b> Scammers ask for that, and it destroys trust.",
        "Make the link https://wa.me/258XXXXXXXXX (258 + the 9-digit number, no '+' or spaces). Open it to test it.",
        "In Canva, make an A4 poster: 'Fale connosco no WhatsApp' + the business name + a QR code (Canva's QR "
        "code app) pointing to the wa.me link. Scan it with your phone to test it, then send it as a PDF for printing.",
        "Collect the other 50%, confirm it, then send S11.",
    ]),
    ("SOP 3 · 10-post pack (60 min)", [
        "50% confirmed. Get the logo, 5–10 real photos, products and prices.",
        "<b>Prompt D</b> writes the 10 headlines and captions.",
        "In Canva (free), build one template, duplicate it 10 times and swap the photo and headline. Use only the client's photos "
        "or Canva's free elements, never images copied from Google.",
        "Export PNGs and send them with the captions as text. Collect the balance and send S11.",
    ]),
    ("SOP 4 · Mini-site + QR (90 min)", [
        "50% confirmed. Intake (S10-B) + 3–6 photos + their Google Maps link.",
        "<b>Prompt E</b> writes the copy.",
        "Build it at sites.google.com with this layout: header, a 'Falar no WhatsApp' button (wa.me link), "
        "prices, photos, an embedded Google Map and hours.",
        "Publish (sites.google.com/view/nomedonegocio). Test on a phone that the button opens the WhatsApp chat.",
        "Share → add the client's Gmail as Editor. Make a QR poster for the site. Collect the balance and send S11.",
    ]),
    ("SOP 5 · Translation (15 min per page)", [
        "100% confirmed. Run <b>Prompt F</b>, then proofread every name, number and price against the original.",
        "Write 'Tradução não oficial' at the top. Never present it as a sworn or certified translation.",
    ]),
]
for title, steps in sops:
    story.append(CondPageBreak(45 * mm))
    story.append(P(title, "h2"))
    story.append(checklist([("", s) for s in steps], with_time=False))

story.append(CondPageBreak(60 * mm))
story.append(P("Claude prompts (paste, then add the client's info)", "h2"))
for code, name, text in PROMPTS:
    story.append(script_block(f"Prompt {code}", name, text))

# ---- Tracker -------------------------------------------------------------------------
story += [PageBreak(), band("LEAD &amp; ORDER TRACKER: copy these columns into Google Sheets/Excel"), Spacer(1, 6)]
hdr = ["#", "Name / Business", "Source", "Offer", "Price", "Status", "Paid via + ref", "Notes"]
rows = [hdr] + [[str(i)] + [""] * 7 for i in range(1, 23)]
story.append(grid(rows, [8 * mm, 40 * mm, 18 * mm, 14 * mm, 16 * mm, 26 * mm, 30 * mm,
                         CONTENT_W - 152 * mm]))
story.append(Spacer(1, 4))
story.append(P("<b>Source:</b> Warm / Status / Group / Maps / FB / Email.  <b>Status:</b> Contacted → Replied → Intake → "
               "Paid 50% → Paid 100% → Delivered → Referral asked.", "small"))
story.append(Spacer(1, 8))
story.append(box([
    P("<b>After the sprint (next week)</b>", "h3"),
    *bullets([
        "Turn one-off clients into <b>monthly clients</b> (10 posts a month for 2500 MT, or WhatsApp/Facebook upkeep for 2000 MT a month).",
        "Collect testimonials and build a simple portfolio page from your best work (with the clients' OK).",
        "When income becomes regular, ask at your local tax office (AT) about registering under the "
        "simplified small-taxpayer regime (ISPC).",
    ]),
]))

doc = SimpleDocTemplate(
    "24h-cash-sprint.pdf", pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=14 * mm, bottomMargin=17 * mm,
    title="24-Hour Cash Sprint", author="Plan built with Claude",
    subject="24-hour checklist: laptop services sold via WhatsApp and email in Mozambique",
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

# ---- Markdown copy of scripts and prompts ---------------------------------------------
md = ["# Copy-paste scripts: 24-Hour Cash Sprint", "",
      "Replace every `[bracket]` before sending. Personalise the first line every time.", ""]
for code, title, text in SCRIPTS:
    md += [f"## {code}: {title}", "", "```text", text, "```", ""]
md += ["# Claude prompts", ""]
for code, name, text in PROMPTS:
    md += [f"## Prompt {code}: {name}", "", "```text", text, "```", ""]
with open("scripts-copy-paste.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print("OK", CheckBox.count, "checkboxes")
