"""Shared A4 design system for the PT-BR digital products: fonts, family themes, covers, text helpers."""
import math
import os
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, "ebook", "fonts") + "/"
for name, f in [
    ("Body", "SourceSansPro-Regular"), ("Body-It", "SourceSansPro-It"), ("Body-Bold", "SourceSansPro-Bold"),
    ("Body-BoldIt", "SourceSansPro-BoldIt"), ("Body-Semi", "SourceSansPro-Semibold"), ("Body-Black", "SourceSansPro-Black"),
    ("Serif", "SourceSerifPro-Regular"), ("Serif-It", "SourceSerifPro-It"), ("Serif-Bold", "SourceSerifPro-Bold"),
    ("Serif-BoldIt", "SourceSerifPro-BoldIt"), ("Serif-Semi", "SourceSerifPro-Semibold"), ("Serif-Black", "SourceSerifPro-Black"),
]:
    try:
        pdfmetrics.getFont(name)
    except KeyError:
        pdfmetrics.registerFont(TTFont(name, FD + f + ".ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-It", boldItalic="Body-BoldIt")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-It", boldItalic="Serif-BoldIt")

C = colors.HexColor
W, H = A4
M = 18 * mm


class Theme:
    def __init__(self, name, primary, secondary, accent, paper, ink, soft, brand):
        self.name, self.primary, self.secondary, self.accent = name, C(primary), C(secondary), C(accent)
        self.paper, self.ink, self.soft, self.brand = C(paper), C(ink), C(soft), brand


CASAL = Theme("casal", "#8E3B2F", "#E9C9BE", "#C98B5A", "#FBF6F0", "#3B2A2E", "#F4E3DC", "Caderno do Casal")
FINANCAS = Theme("financas", "#1F5135", "#CFE6D8", "#C9A227", "#F8FAF7", "#1E2B24", "#E6F2EA", "Planner Financeiro 2027")
NATAL = Theme("natal", "#B3122E", "#1E6B3A", "#E0A526", "#FFFDF8", "#2A2422", "#FBEFE4", "Kit Natal")


def rich(s):
    s = escape(str(s or "")).strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("\n", "<br/>")


def style(name, **kw):
    base = dict(fontName="Body", fontSize=11, leading=16, textColor=C("#2B2B2B"), spaceAfter=7)
    base.update(kw)
    return ParagraphStyle(name, **base)


def para(text, st):
    return Paragraph(rich(text), st)


def draw_para(c, text, st, x, y_top, width, raw=False):
    """Draw a paragraph with its top at y_top; returns the new y below it (raw=True keeps markup)."""
    p = Paragraph(text if raw else rich(text), st)
    _, h = p.wrap(width, 2000)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def para_height(text, st, width, raw=False):
    return Paragraph(text if raw else rich(text), st).wrap(width, 2000)[1]


# ---------------------------------------------------------------- ornaments
def star(c, x, y, r, fill, stroke=None, points=5, inner=0.45):
    p = c.beginPath()
    for i in range(points * 2):
        ang = math.pi / 2 + i * math.pi / points
        rad = r if i % 2 == 0 else r * inner
        px, py = x + rad * math.cos(ang), y + rad * math.sin(ang)
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close()
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    c.drawPath(p, fill=1, stroke=1 if stroke else 0)


def heart(c, x, y, s, fill):
    p = c.beginPath()
    p.moveTo(x, y - s * 0.35)
    p.curveTo(x - s * 0.9, y + s * 0.25, x - s * 0.35, y + s * 0.85, x, y + s * 0.4)
    p.curveTo(x + s * 0.35, y + s * 0.85, x + s * 0.9, y + s * 0.25, x, y - s * 0.35)
    p.close()
    c.setFillColor(fill)
    c.drawPath(p, fill=1, stroke=0)


def leaf(c, x, y, s, angle, fill):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(s * 0.3, s * 0.35, s * 0.7, s * 0.35, s, 0)
    p.curveTo(s * 0.7, -s * 0.35, s * 0.3, -s * 0.35, 0, 0)
    c.setFillColor(fill)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def coin(c, x, y, r, fill, ink):
    c.setFillColor(fill)
    c.circle(x, y, r, stroke=0, fill=1)
    c.setStrokeColor(ink)
    c.setLineWidth(r * 0.08)
    c.circle(x, y, r * 0.78, stroke=1, fill=0)


def tree(c, x, y, s, fill, trunk):
    c.setFillColor(trunk)
    c.rect(x - s * 0.08, y, s * 0.16, s * 0.18, stroke=0, fill=1)
    for i, (w_, h_) in enumerate([(0.9, 0.42), (0.7, 0.38), (0.5, 0.34)]):
        base = y + s * (0.16 + i * 0.24)
        p = c.beginPath()
        p.moveTo(x - s * w_ / 2, base)
        p.lineTo(x + s * w_ / 2, base)
        p.lineTo(x, base + s * h_)
        p.close()
        c.setFillColor(fill)
        c.drawPath(p, fill=1, stroke=0)


def writing_lines(c, x, y_top, width, n, gap=8.5 * mm, color=None):
    c.setStrokeColor(color or C("#CFC7BE"))
    c.setLineWidth(0.6)
    for i in range(n):
        yy = y_top - gap * (i + 1)
        c.line(x, yy, x + width, yy)
    return y_top - gap * n


def rounded_box(c, x, y, w, h, fill, stroke=None, r=8, lw=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke else 0, fill=1)


# ---------------------------------------------------------------- covers & page furniture
def cover(c, theme, title, subtitle, tag, price_note=None, edition="Edição Brasil · 2026/2027"):
    t = theme
    c.setFillColor(t.primary)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    if t.name == "casal":
        c.setFillColor(t.secondary)
        c.circle(W * 0.92, H * 0.9, 80 * mm, stroke=0, fill=1)
        c.setFillColor(t.primary)
        c.circle(W * 0.92, H * 0.9, 60 * mm, stroke=0, fill=1)
        for i, (hx, hy, hs) in enumerate([(0.86, 0.86, 30), (0.95, 0.74, 14), (0.72, 0.95, 10)]):
            heart(c, W * hx, H * hy, hs * mm, t.secondary if i else t.accent)
        for i in range(7):
            leaf(c, W * 0.16 + i * 9 * mm, 40 * mm + (i % 2) * 6 * mm, 16 * mm, 30 + i * 18, t.accent)
    elif t.name == "financas":
        c.setFillColor(t.secondary)
        for i in range(6):
            c.rect(W * 0.58 + i * 12 * mm, H * 0.69, 8 * mm, (10 + i * 9) * mm, stroke=0, fill=1)
        for i, (cx, cy, r) in enumerate([(0.62, 0.9, 13), (0.74, 0.94, 9), (0.53, 0.84, 7)]):
            coin(c, W * cx, H * cy, r * mm, t.accent, t.primary)
    else:
        c.setFillColor(t.secondary)
        c.rect(0, 0, W, 70 * mm, stroke=0, fill=1)
        for i, (sx, sy, sr) in enumerate([(0.82, 0.86, 22), (0.68, 0.92, 9), (0.92, 0.72, 11), (0.6, 0.78, 6)]):
            star(c, W * sx, H * sy, sr * mm, t.accent)
        for i in range(6):
            tree(c, 20 * mm + i * 32 * mm, 52 * mm, (26 + (i % 3) * 8) * mm, C("#2E8B57") if i % 2 else t.accent,
                 C("#7B4A2A"))
    c.setFillColor(t.accent if t.name != "natal" else colors.white)
    c.rect(M, H - 52 * mm, 26 * mm, 2.4 * mm, stroke=0, fill=1)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    c.setFont("Body-Bold", 10.5)
    c.drawString(M, H - 45 * mm, tag.upper())
    st_title = style("cvt", fontName="Serif-Black", fontSize=40, leading=44, textColor=colors.white)
    y = draw_para(c, title, st_title, M, H - 110 * mm, W * 0.78)
    st_sub = style("cvs", fontName="Serif-It", fontSize=16, leading=22, textColor=colors.Color(1, 1, 1, alpha=0.9))
    draw_para(c, subtitle, st_sub, M, y - 8 * mm, W * 0.7)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.8))
    c.setFont("Body", 10)
    c.drawString(M, 22 * mm if t.name != "natal" else 80 * mm, edition)
    if price_note:
        c.drawRightString(W - M, 22 * mm if t.name != "natal" else 80 * mm, price_note)


def header_footer(c, theme, title, page_no, show_header=True):
    c.saveState()
    if show_header:
        c.setFillColor(theme.primary)
        c.rect(0, H - 8 * mm, W, 8 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Body-Bold", 8)
        c.drawString(M, H - 5.4 * mm, title.upper())
    c.setFillColor(C("#8A8A8A"))
    c.setFont("Body", 8)
    c.drawCentredString(W / 2, 9 * mm, str(page_no))
    c.restoreState()


def section_title(c, theme, kicker, title, y=None):
    y = y or H - 26 * mm
    c.setFillColor(theme.accent if theme.name != "natal" else theme.secondary)
    c.setFont("Body-Bold", 9.5)
    c.drawString(M, y, kicker.upper())
    st = style("stt", fontName="Serif-Bold", fontSize=24, leading=28, textColor=theme.primary)
    return draw_para(c, title, st, M, y - 4 * mm, W - 2 * M) - 6 * mm


def text_page(c, theme, doc_title, page_no, kicker, title, paragraphs, bullets=None, numbered=False):
    """A simple full text page (intro, how to use...). Returns the y after content."""
    header_footer(c, theme, doc_title, page_no)
    y = section_title(c, theme, kicker, title)
    body = style("tp", fontSize=11.5, leading=17.5, textColor=theme.ink)
    for p in paragraphs or []:
        y = draw_para(c, p, body, M, y, W - 2 * M) - 4 * mm
    if bullets:
        y -= 2 * mm
        for i, b in enumerate(bullets, 1):
            mark = f"<font color='{theme.primary.hexval()}'><b>{i}.</b></font>&nbsp;&nbsp;" if numbered else \
                f"<font color='{theme.accent.hexval()}'><b>•</b></font>&nbsp;&nbsp;"
            p = Paragraph(mark + rich(b), style("tb", fontSize=11.5, leading=17, textColor=theme.ink, leftIndent=14,
                                               firstLineIndent=-14))
            _, h = p.wrap(W - 2 * M, 2000)
            p.drawOn(c, M, y - h)
            y -= h + 2.5 * mm
    return y


def fits(y, needed):
    return y - needed > 16 * mm


class Flow:
    """Canvas page manager for text-heavy pages with automatic page breaks."""

    def __init__(self, c, theme, doc_title, start_page=1):
        self.c, self.t, self.title = c, theme, doc_title
        self.page = start_page
        self.y = None
        self.body = style("fb", fontSize=11.5, leading=17.5, textColor=theme.ink)
        self.small = style("fs", fontSize=9.5, leading=13, textColor=C("#6B6B6B"))
        self.h2 = style("fh2", fontName="Serif-Bold", fontSize=16, leading=20, textColor=theme.primary, spaceAfter=0)

    def new_page(self, header=True):
        if self.y is not None:
            self.c.showPage()
            self.page += 1
        self.c.setFillColor(self.t.paper)
        self.c.rect(0, 0, W, H, stroke=0, fill=1)
        header_footer(self.c, self.t, self.title, self.page, header)
        self.y = H - 22 * mm

    def ensure(self, h):
        if self.y is None or self.y - h < 18 * mm:
            self.new_page()

    def title_block(self, kicker, title):
        self.ensure(40 * mm)
        self.y = section_title(self.c, self.t, kicker, title, self.y - 4 * mm)

    def para(self, text, st=None, gap=3.5 * mm, raw=False):
        st = st or self.body
        if raw:
            h = para_height(text, st, W - 2 * M, raw=True)
            self.ensure(h)
            self.y = draw_para(self.c, text, st, M, self.y, W - 2 * M, raw=True) - gap
            return
        h = para_height(text, st, W - 2 * M)
        if h > H - 50 * mm:  # very long paragraph: split by sentences
            parts = re.split(r"(?<=[.!?])\s+", str(text))
            half = len(parts) // 2
            self.para(" ".join(parts[:half]), st, gap)
            self.para(" ".join(parts[half:]), st, gap)
            return
        self.ensure(h)
        self.y = draw_para(self.c, text, st, M, self.y, W - 2 * M) - gap

    def heading(self, text):
        self.ensure(30 * mm)
        self.y = draw_para(self.c, text, self.h2, M, self.y - 2 * mm, W - 2 * M) - 3 * mm

    def bullets(self, items, numbered=False):
        for i, b in enumerate(items or [], 1):
            mark = (f"<font color='{self.t.primary.hexval()}'><b>{i}.</b></font>&nbsp;&nbsp;" if numbered else
                    f"<font color='{self.t.accent.hexval()}'><b>•</b></font>&nbsp;&nbsp;")
            p = Paragraph(mark + rich(b), style("fbl", fontSize=11.5, leading=17, textColor=self.t.ink, leftIndent=14,
                                               firstLineIndent=-14))
            _, h = p.wrap(W - 2 * M, 2000)
            self.ensure(h)
            p.drawOn(self.c, M, self.y - h)
            self.y -= h + 2.5 * mm

    def boxed(self, label, text, fill=None, edge=None, italic=False):
        st = style("fbx", fontName="Serif-It" if italic else "Body", fontSize=11, leading=16, textColor=self.t.ink)
        h = para_height(text, st, W - 2 * M - 14 * mm) + 13 * mm
        self.ensure(h + 3 * mm)
        rounded_box(self.c, M, self.y - h, W - 2 * M, h, fill or self.t.soft, edge, r=6)
        self.c.setFillColor(edge or self.t.primary)
        self.c.setFont("Body-Bold", 8.5)
        self.c.drawString(M + 7 * mm, self.y - 7 * mm, label.upper())
        draw_para(self.c, text, st, M + 7 * mm, self.y - 9.5 * mm, W - 2 * M - 14 * mm)
        self.y -= h + 4 * mm

    def lines(self, n, gap=8 * mm):
        self.ensure(gap * n + 2 * mm)
        self.y = writing_lines(self.c, M, self.y, W - 2 * M, n, gap) - 3 * mm

    def finish(self):
        self.c.showPage()
