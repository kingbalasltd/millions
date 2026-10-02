"""Shared PDF building blocks: fonts, palette, tickable checklists, tables, script boxes."""
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (  # noqa: F401  (re-exported for the plan builders)
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



def script_block(code, title, text):
    body = escape(text).replace("\n", "<br/>")
    return KeepTogether([
        P(f"<font color='#E36414'>{code}</font>&nbsp;&nbsp;{escape(title)}", "h3"),
        box([P(body, "script")]),
        Spacer(1, 3),
    ])


def footer(text):
    """Page callback drawing a footer line with `text` and the page number."""
    def on_page(canv, doc):
        canv.saveState()
        canv.setFont("Sans", 7.5)
        canv.setFillColor(MUTED)
        canv.drawString(MARGIN, 9 * mm, text)
        canv.drawRightString(PAGE_W - MARGIN, 9 * mm, f"page {doc.page}")
        canv.setStrokeColor(LINE)
        canv.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
        canv.restoreState()
    return on_page
