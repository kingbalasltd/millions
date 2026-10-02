"""Shared ebook design: fonts, palette, text styles, callouts, checklists and page callbacks."""
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import B5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (  # noqa: F401  (re-exported for the book builders)
    BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents  # noqa: F401

# ---------------------------------------------------------------- fonts & palette
FD = "ebook/fonts/"
for name, f in [
    ("Body", "SourceSansPro-Regular"), ("Body-It", "SourceSansPro-It"), ("Body-Bold", "SourceSansPro-Bold"),
    ("Body-BoldIt", "SourceSansPro-BoldIt"), ("Body-Semi", "SourceSansPro-Semibold"), ("Body-Black", "SourceSansPro-Black"),
    ("Serif", "SourceSerifPro-Regular"), ("Serif-It", "SourceSerifPro-It"), ("Serif-Bold", "SourceSerifPro-Bold"),
    ("Serif-BoldIt", "SourceSerifPro-BoldIt"), ("Serif-Semi", "SourceSerifPro-Semibold"), ("Serif-Black", "SourceSerifPro-Black"),
]:
    pdfmetrics.registerFont(TTFont(name, FD + f + ".ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-It", boldItalic="Body-BoldIt")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-It", boldItalic="Serif-BoldIt")

C = colors.HexColor
INK, MUTED = C("#1D2B33"), C("#5F6B70")
DEEP, TEAL, AMBER, AMBER_DK = C("#0E3B49"), C("#13647A"), C("#E8892B"), C("#B9620F")
SAND, LINE = C("#F7F2E8"), C("#E4DCCB")
RED, GREEN = C("#A4161A"), C("#2E7D5B")
SOFT_TEAL, SOFT_AMBER, SOFT_RED, SOFT_GREEN = C("#E6F0F1"), C("#FCEEDC"), C("#F9E4E3"), C("#E4F2E8")
WHITE = colors.white

W, H = B5
M = 17 * mm
TOP, BOT = 21 * mm, 19 * mm
CW = W - 2 * M


def S(name, **kw):
    base = dict(fontName="Body", fontSize=10.2, leading=15.2, textColor=INK, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "body": S("body"),
    "small": S("small", fontSize=8.4, leading=11.5, textColor=MUTED, spaceAfter=0),
    "lead": S("lead", fontName="Serif-It", fontSize=11.4, leading=17.4, textColor=INK, spaceAfter=0),
    "section": S("section", fontName="Serif-Bold", fontSize=15.5, leading=19.5, textColor=DEEP, spaceBefore=4, spaceAfter=7),
    "label": S("label", fontName="Body-Bold", fontSize=7.8, leading=10, textColor=TEAL, spaceAfter=2),
    "ctitle": S("ctitle", fontName="Body-Bold", fontSize=10.4, leading=14, spaceAfter=2),
    "cbody": S("cbody", fontSize=9.8, leading=14.4, spaceAfter=3),
    "script": S("script", fontSize=9.6, leading=14, spaceAfter=0),
    "note": S("note", fontName="Serif-It", fontSize=10.6, leading=15.6, spaceAfter=3),
    "quote": S("quote", fontName="Serif-It", fontSize=13.5, leading=19, textColor=TEAL, alignment=TA_CENTER, spaceAfter=0),
    "bullet": S("bullet", leftIndent=13, bulletIndent=2, bulletFontName="Body-Bold", bulletColor=AMBER, spaceAfter=3.5),
    "cell": S("cell", fontSize=8.9, leading=12, spaceAfter=0),
    "cellh": S("cellh", fontName="Body-Bold", fontSize=8.9, leading=12, textColor=WHITE, spaceAfter=0),
    "step": S("step", spaceAfter=0),
    "qq": S("qq", fontName="Body-Semi", spaceAfter=2),
    "qopt": S("qopt", leftIndent=14, spaceAfter=1, fontSize=9.8, leading=13.6),
}


def rich(s, serif_italic=False):
    s = escape(str(s or "")).strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = s.replace("\n", "<br/>")
    if serif_italic:  # Source Serif italic lacks these glyphs; borrow them from the sans
        for ch in "→✓":
            s = s.replace(ch, f'<font face="Body">{ch}</font>')
    return s


def P(text, style="body", serif_italic=False):
    return Paragraph(rich(text, serif_italic), ST[style] if isinstance(style, str) else style)


# ---------------------------------------------------------------- small flowables
RUN = {"left": "", "right": ""}


class Running(Flowable):
    """Zero-size marker that sets the running header text from this point on."""

    def __init__(self, left, right):
        super().__init__()
        self.left, self.right = left, right
        self.width = self.height = 0

    def draw(self):
        RUN["left"], RUN["right"] = self.left, self.right


class Anchor(Flowable):
    """Zero-size marker that becomes a TOC entry, a PDF bookmark and an outline entry."""

    def __init__(self, level, text, key):
        super().__init__()
        self.toc = (level, text, key)
        self.width = self.height = 0

    def draw(self):
        pass


class Badge(Flowable):
    def __init__(self, n, size=15, fill=AMBER):
        super().__init__()
        self.n, self.size, self.fill = str(n), size, fill
        self.width, self.height = size + 4, size

    def draw(self):
        r = self.size / 2
        self.canv.setFillColor(self.fill)
        self.canv.circle(r, r - 1, r, stroke=0, fill=1)
        self.canv.setFillColor(WHITE)
        self.canv.setFont("Body-Bold", 8.6)
        self.canv.drawCentredString(r, r - 4, self.n)


class CheckBox(Flowable):
    """Clickable checkbox (tick it in Chrome/Edge/Acrobat) that also prints as an empty box."""
    count = 0

    def __init__(self, size=10.5):
        super().__init__()
        self.size = size
        self.width = self.height = size

    def draw(self):
        CheckBox.count += 1
        self.canv.acroForm.checkbox(
            name=f"cb{CheckBox.count}", x=0, y=-1, size=self.size, buttonStyle="check",
            borderColor=AMBER_DK, fillColor=WHITE, textColor=DEEP, borderWidth=1,
            forceBorder=True, relative=True, tooltip="Tick when done")


class Rule(Flowable):
    def __init__(self, width=CW, color=LINE, thickness=0.6, space=4):
        super().__init__()
        self.w, self.color, self.t, self.space = width, color, thickness, space
        self.width, self.height = width, space * 2

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.t)
        self.canv.line(0, self.space, self.w, self.space)


class ChapterBand(Flowable):
    """Full-bleed chapter header: label, title, subtitle and a large faded chapter number."""

    def __init__(self, number, label, title, subtitle):
        super().__init__()
        self.number = f"{number:02d}"
        self.p_label = Paragraph(rich(label.upper()), S("bl", fontName="Body-Bold", fontSize=8.6, leading=11,
                                                         textColor=AMBER, spaceAfter=0))
        self.p_title = Paragraph(rich(title), S("bt", fontName="Serif-Bold", fontSize=24, leading=28.5,
                                                textColor=WHITE, spaceAfter=0))
        self.p_sub = Paragraph(rich(subtitle), S("bs", fontSize=11.5, leading=15.5,
                                                 textColor=C("#CFE0E3"), spaceAfter=0))

    def wrap(self, aw, ah):
        inner = W - 2 * M - 18 * mm
        self.hl = self.p_label.wrap(inner, ah)[1]
        self.ht = self.p_title.wrap(inner, ah)[1]
        self.hs = self.p_sub.wrap(inner, ah)[1]
        self.width = W
        self.height = 30 * mm + self.hl + 5 * mm + self.ht + 4 * mm + self.hs + 13 * mm
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(DEEP)
        c.rect(0, 0, W, self.height, stroke=0, fill=1)
        c.setStrokeColor(colors.Color(0.91, 0.54, 0.17, alpha=0.20))
        c.setLineWidth(16)
        c.circle(W - 14 * mm, self.height - 4 * mm, 38 * mm, stroke=1, fill=0)
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.08))
        c.setFont("Serif-Black", 150)
        c.drawRightString(W - 8 * mm, 9 * mm, self.number)
        c.setFillColor(AMBER)
        c.rect(M, self.height - 22 * mm, 16 * mm, 1.6 * mm, stroke=0, fill=1)
        c.restoreState()
        y = self.height - 30 * mm - self.hl
        self.p_label.drawOn(c, M, y)
        y -= 5 * mm + self.ht
        self.p_title.drawOn(c, M, y)
        y -= 4 * mm + self.hs
        self.p_sub.drawOn(c, M, y)


def padded(flowables, top=0, bottom=0):
    """Wrap flowables so they sit inside the page margins on a full-bleed frame."""
    t = Table([[f] for f in flowables], colWidths=[W])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), M), ("RIGHTPADDING", (0, 0), (-1, -1), M),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, 0), top), ("BOTTOMPADDING", (0, -1), (-1, -1), bottom),
    ]))
    return t


# ---------------------------------------------------------------- content blocks
CALLOUTS = {
    "tip": ("TIP", TEAL, SOFT_TEAL),
    "warning": ("WATCH OUT", RED, SOFT_RED),
    "example": ("EXAMPLE", AMBER_DK, SOFT_AMBER),
    "mentor_note": ("A NOTE FROM YOUR MENTOR", DEEP, SAND),
    "script": ("SCRIPT · COPY, PERSONALISE, SEND", GREEN, SOFT_GREEN),
}


def callout(kind, title, text, items=None):
    label, edge, bg = CALLOUTS[kind]
    rows = [[Paragraph(label, S("cl", fontName="Body-Bold", fontSize=7.6, leading=10, textColor=edge, spaceAfter=0))]]
    if title:
        rows.append([P(title, "ctitle")])
    body_style = "note" if kind == "mentor_note" else ("script" if kind == "script" else "cbody")
    if kind == "script":
        rows += [[P(chunk, "script")] for chunk in re.split(r"\n\s*\n", str(text or "")) if chunk.strip()]
    else:
        rows += [[P(chunk, body_style, serif_italic=(kind == "mentor_note"))]
                 for chunk in re.split(r"\n\s*\n", str(text or "")) if chunk.strip()]
    for it in items or []:
        rows.append([Paragraph(rich(it), ST["bullet"], bulletText="•")])
    if kind == "mentor_note":
        rows.append([Paragraph("— your mentor", S("sig", fontName="Serif-Semi", fontSize=9.6, textColor=MUTED,
                                                    spaceAfter=0))])
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
    ]))
    return [t, Spacer(1, 9)]


def steps_block(title, items):
    out = []
    if title:
        out.append(P(title, "ctitle"))
    rows = [[Badge(i + 1), P(it, "step")] for i, it in enumerate(items or [])]
    if rows:
        t = Table(rows, colWidths=[9 * mm, CW - 9 * mm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("TOPPADDING", (0, 0), (0, -1), 3.5),
        ]))
        out.append(t)
    out.append(Spacer(1, 6))
    return out


def bullets_block(title, items):
    out = [P(title, "ctitle")] if title else []
    out += [Paragraph(rich(it), ST["bullet"], bulletText="•") for it in items or []]
    out.append(Spacer(1, 4))
    return out


def grid(rows, title=None, widths=None):
    rows = [r for r in (rows or []) if r]
    if not rows:
        return []
    ncol = max(len(r) for r in rows)
    rows = [list(r) + [""] * (ncol - len(r)) for r in rows]
    widths = widths or [CW / ncol] * ncol
    data = [[Paragraph(rich(c), ST["cellh"] if i == 0 else ST["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), DEEP),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]
    for r in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, r), (-1, r), SAND))
    t.setStyle(TableStyle(style))
    out = [P(title, "ctitle")] if title else []
    return out + [t, Spacer(1, 10)]


def quote_block(text):
    t = Table([[Paragraph("“", S("qm", fontName="Serif-Black", fontSize=34, leading=30, textColor=AMBER,
                                  alignment=TA_CENTER, spaceAfter=0))],
               [P(text, "quote", serif_italic=True)]], colWidths=[CW])
    t.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("LEFTPADDING", (0, 0), (-1, -1), 14 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 14 * mm)]))
    return [Spacer(1, 4), t, Spacer(1, 12)]


def render_block(b):
    kind = b.get("kind", "paragraph")
    title, text, items, rows = b.get("title"), b.get("text"), b.get("items"), b.get("rows")
    if kind == "paragraph":
        out = [P(title, "ctitle")] if title else []
        return out + [P(chunk) for chunk in re.split(r"\n\s*\n", str(text or "")) if chunk.strip()]
    if kind == "bullets":
        return bullets_block(title, items or ([text] if text else []))
    if kind == "steps":
        return steps_block(title, items or ([text] if text else []))
    if kind == "table":
        return grid(rows, title)
    if kind == "quote":
        return quote_block(text)
    if kind in CALLOUTS:
        return callout(kind, title, text, items)
    return [P(text or "")]


# ---------------------------------------------------------------- chapter end pieces
def takeaways(items):
    rows = [[Paragraph("KEY TAKEAWAYS", S("kt", fontName="Body-Bold", fontSize=8, leading=10, textColor=TEAL,
                                           spaceAfter=0)), ""]]
    rows += [[Paragraph("✓", S("tk", fontName="Body-Bold", fontSize=11, leading=14, textColor=AMBER, spaceAfter=0)),
              P(it, "cbody")] for it in items]
    t = Table(rows, colWidths=[8 * mm, CW - 8 * mm])
    t.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)), ("BOX", (0, 0), (-1, -1), 1, TEAL), ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
    ]))
    return [CondPageBreak(45 * mm), t, Spacer(1, 14)]


def challenge_card(n, ch):
    xp = ch.get("xp", 0)
    head = Table([[Paragraph(f"CHALLENGE {n:02d}", S("chh", fontName="Body-Black", fontSize=10, leading=12,
                                                       textColor=WHITE, spaceAfter=0)),
                   Paragraph(f"+{xp} XP", S("chx", fontName="Body-Black", fontSize=10, leading=12,
                                             textColor=DEEP, alignment=2, spaceAfter=0))]],
                 colWidths=[(CW - 2) * 0.6, (CW - 2) * 0.4])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AMBER), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 6),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    rows = [[head],
            [P(ch.get("title", ""), S("cht", fontName="Serif-Bold", fontSize=17, leading=21, textColor=DEEP,
                                      spaceAfter=0))],
            [P(ch.get("mission", ""), "cbody")],
            [P(f"**Time box:** {ch.get('time_box', '')}     **Reward:** {xp} XP", "small")],
            [Paragraph("YOUR MISSION, STEP BY STEP", S("ms", fontName="Body-Bold", fontSize=7.8, leading=10,
                                                      textColor=AMBER_DK, spaceAfter=0))]]
    for s in ch.get("steps", []):
        st = Table([[CheckBox(), P(s, "cbody")]], colWidths=[8 * mm, CW - 8 * mm - 22])
        st.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (0, -1), 3)]))
        rows.append([st])
    rows.append([P(f"**Proof:** {ch.get('proof', '')}", "cbody")])
    if ch.get("bonus"):
        rows.append([P(f"**Bonus (optional, harder):** {ch.get('bonus')}", "cbody")])
    done = Table([[CheckBox(), P("**Challenge complete.** Date: ____________   XP added to the tracker", "cbody")]],
                 colWidths=[8 * mm, CW - 8 * mm - 22])
    done.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("TOPPADDING", (0, 0), (0, -1), 3)]))
    rows.append([done])
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.3, AMBER), ("BACKGROUND", (0, 1), (-1, -1), C("#FFFBF4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, 0), 0), ("RIGHTPADDING", (0, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, 0), 0), ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 1), (-1, 1), 9), ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
    ]))
    return [CondPageBreak(80 * mm), t, Spacer(1, 14)]


def quiz_block(n, quiz):
    out = [CondPageBreak(60 * mm),
           Paragraph(f"QUICK QUIZ · CHAPTER {n}", S("qz", fontName="Body-Bold", fontSize=8, leading=10,
                                                     textColor=TEAL, spaceAfter=6))]
    for i, q in enumerate(quiz):
        block = [P(f"{i + 1}. {q.get('question', '')}", "qq")]
        for j, o in enumerate(q.get("options", [])):
            block.append(Paragraph(f"<font color='#B9620F'><b>{'ABCD'[j]}</b></font>&nbsp;&nbsp;{rich(o)}", ST["qopt"]))
        block.append(Spacer(1, 6))
        out.append(KeepTogether(block))
    out.append(P("Answers are at the back of the book. Check yourself only after you've answered all three.", "small"))
    return out


# ---------------------------------------------------------------- page callbacks
def draw_body(c, doc):
    c.saveState()
    c.setFont("Body", 7.8)
    c.setFillColor(MUTED)
    c.drawString(M, H - 12 * mm, RUN["left"].upper())
    c.drawRightString(W - M, H - 12 * mm, RUN["right"])
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(M, H - 14 * mm, W - M, H - 14 * mm)
    c.setFont("Body-Bold", 8.5)
    c.setFillColor(DEEP)
    c.drawCentredString(W / 2, 10 * mm, str(doc.page))
    c.restoreState()


def draw_plain(c, doc):
    c.saveState()
    c.setFont("Body-Bold", 8.5)
    c.setFillColor(DEEP)
    c.drawCentredString(W / 2, 10 * mm, str(doc.page))
    c.restoreState()
