"""Builds the mentorship ebook ebook/from-zero-to-number-one.pdf from ebook/chapters.json.

Run: python3 build_ebook.py [chapters.json] [output.pdf]
"""
import json
import re
import sys

from ebook_kit import *  # noqa: F401,F403
from ebook_kit import RUN, ST  # noqa: F401

SRC = sys.argv[1] if len(sys.argv) > 1 else "ebook/chapters.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "ebook/from-zero-to-number-one.pdf"


# ---------------------------------------------------------------- page decorations
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(DEEP)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    for r, a, lw in [(95, 0.10, 34), (70, 0.16, 18), (48, 0.24, 8)]:
        c.setStrokeColor(colors.Color(0.91, 0.54, 0.17, alpha=a))
        c.setLineWidth(lw)
        c.circle(W - 22 * mm, H - 58 * mm, r * mm, stroke=1, fill=0)
    c.setFillColor(AMBER)
    c.rect(M, H - 40 * mm, 22 * mm, 2.2 * mm, stroke=0, fill=1)
    c.setFillColor(C("#CFE0E3"))
    c.setFont("Body-Bold", 9.5)
    c.drawString(M, H - 34 * mm, "A COURSE IN 9 CHAPTERS · E-BOOK BUSINESS 2026")
    c.setFillColor(WHITE)
    c.setFont("Serif-Black", 46)
    c.drawString(M, H - 112 * mm, "Faceless")
    c.drawString(M, H - 129 * mm, "Empire")
    c.setFont("Serif-It", 15)
    c.setFillColor(C("#F4D9B8"))
    c.drawString(M, H - 145 * mm, "Build a faceless digital-product business")
    c.drawString(M, H - 152.5 * mm, "that sells across the Portuguese-speaking world.")
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.75))
    c.setFont("Body", 10.5)
    y = 62 * mm
    for line in ["The game  ·  The machine  ·  Scale",
                 "9 challenges  ·  27 quiz questions  ·  XP and 5 levels  ·  PT-BR scripts"]:
        c.drawString(M, y, line)
        y -= 6.5 * mm
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.25))
    c.setLineWidth(0.6)
    c.line(M, 36 * mm, W - M, 36 * mm)
    c.setFillColor(WHITE)
    c.setFont("Body-Bold", 10.5)
    c.drawString(M, 27 * mm, "Your mentor: Claude")
    c.setFont("Body", 9.5)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.7))
    c.drawString(M, 21 * mm, "Written for you · Maputo · October 2026")
    c.restoreState()


def draw_part_bg(c, doc):
    c.saveState()
    c.setFillColor(TEAL)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.08))
    c.setLineWidth(40)
    c.circle(W * 0.15, 30 * mm, 70 * mm, stroke=1, fill=0)
    c.restoreState()


class Book(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(path, pagesize=B5, **kw)
        body = Frame(M, BOT, CW, H - TOP - BOT, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        bleed = Frame(0, BOT, W, H - BOT, id="bleed", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        part = Frame(M, M, CW, H - 2 * M, id="part", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate("cover", [part], onPage=draw_cover),
            PageTemplate("front", [body], onPageEnd=draw_plain),
            PageTemplate("part", [part], onPage=draw_part_bg),
            PageTemplate("opener", [bleed], onPageEnd=draw_plain),
            PageTemplate("body", [body], onPageEnd=draw_body),
        ])

    def afterFlowable(self, f):
        if isinstance(f, Anchor):
            level, text, key = f.toc
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))


# ---------------------------------------------------------------- the book
data = json.load(open(SRC, encoding="utf-8"))
chapters = sorted(data["chapters"], key=lambda c: c["number"])
PARTS = [
    ("Part 1", "The Game", "How digital products really make money, the Portuguese-speaking market, and your product factory.", [1, 2, 3]),
    ("Part 2", "The Machine", "Platforms and payouts, sales pages built with Lovable, and your faceless content engine.", [4, 5, 6]),
    ("Part 3", "Scale", "Your affiliate army, paid traffic without burning money, and running the empire.", [7, 8, 9]),
]
LEVELS = [("1", "Apprentice", "0–300", "You understand the game and the money maths."),
          ("2", "Builder", "301–700", "Your products, checkout and pages are live."),
          ("3", "Launcher", "701–1,200", "Content is posting daily and sales have started."),
          ("4", "Scaler", "1,201–1,700", "Affiliates and ads are growing your sales."),
          ("5", "Empire", "1,701+", "Several products, several markets, money in every day.")]

story = [NextPageTemplate("front"), PageBreak()]

# Title page
story += [Spacer(1, 30 * mm),
          Paragraph("Faceless Empire", S("tp", fontName="Serif-Black", fontSize=32, leading=36, textColor=DEEP)),
          Paragraph("A course for building a faceless e-book business for Brazil and the Portuguese-speaking world, with honest numbers and real challenges.", S("tps", fontName="Serif-It", fontSize=13, leading=19, textColor=TEAL)),
          Spacer(1, 6), Rule(40 * mm, AMBER, 2.2), Spacer(1, 10),
          P("**Your mentor:** Claude (an AI). **Written for:** you, starting from zero.", "body"),
          P("**Edition:** Mozambique, October 2026.", "body"),
          Spacer(1, 40 * mm),
          P("**Read this first.** The market facts in this book (projects, laws, prices, platforms) were researched in "
            "October 2026. Things marked 'check this' were not fully verified. Laws and fees change, so confirm them at the "
            "source before you quote them to a client. This book teaches business skills. It is not legal, tax or "
            "financial advice; for those, talk to the tax authority (AT) or a qualified professional.", "small"),
          PageBreak()]

# How to use this book
story += [Paragraph("How this mentorship works", ST["section"]),
          P("Every chapter follows the same loop. Don't skip the doing: reading without action changes nothing."),
          ]
loop = Table([[Badge(i + 1, 17, c), P(f"**{a}** {b}", "cbody")] for i, (a, b, c) in enumerate([
    ("Read.", "Each chapter teaches one part of the business from zero, with Mozambican examples.", TEAL),
    ("Do.", "Finish the challenge at the end of the chapter. Tick each step as you go: the boxes are clickable.", AMBER),
    ("Prove.", "Save the proof the challenge asks for, or paste it into your chat with me. I'll review it.", GREEN),
    ("Level up.", "Add the XP to your tracker at the back. Five levels take you from Apprentice to Market Leader.", DEEP),
])], colWidths=[10 * mm, CW - 10 * mm])
loop.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (0, -1), 2)]))
story += [loop, Spacer(1, 6)]
story += grid([["Level", "Name", "XP", "What it means"]] + [list(l) for l in LEVELS],
              widths=[13 * mm, 26 * mm, 22 * mm, CW - 61 * mm])
story += callout("mentor_note", None,
                 "I can't make you rich in 24 hours, and anyone who promises that is selling you something. What I can do is "
                 "teach you, step by step, how to build something real: a business that companies trust and pay well. "
                 "You bring the effort and the honesty. I'll bring everything I know. Deal?")
story.append(PageBreak())

# Contents
toc = TableOfContents()
toc.levelStyles = [
    S("toc0", fontName="Serif-Bold", fontSize=11.5, leading=15, textColor=DEEP, spaceBefore=8, spaceAfter=2),
    S("toc1", fontSize=10, leading=14, leftIndent=10, textColor=INK, spaceAfter=1),
]
toc.dotsMinLevel = 1
story += [Paragraph("Contents", ST["section"]), Spacer(1, 4), toc]

xp_rows = []
for pnum, (plabel, ptitle, pdesc, nums) in enumerate(PARTS, 1):
    story += [NextPageTemplate("part"), PageBreak(), Anchor(0, f"{plabel} · {ptitle}", f"part{pnum}"),
              Spacer(1, 50 * mm),
              Paragraph(plabel.upper(), S("pl", fontName="Body-Black", fontSize=12, leading=14, textColor=AMBER)),
              Paragraph(ptitle, S("pt", fontName="Serif-Black", fontSize=36, leading=40, textColor=WHITE)),
              Spacer(1, 6),
              Paragraph(pdesc, S("pd", fontName="Serif-It", fontSize=13, leading=19, textColor=C("#DCEBEE"))),
              Spacer(1, 18)]
    for ch in chapters:
        if ch["number"] in nums:
            story.append(Paragraph(f"<font color='#E8892B'><b>{ch['number']:02d}</b></font>&nbsp;&nbsp;&nbsp;{rich(ch['title'])}",
                                   S("pc", fontSize=12, leading=18, textColor=WHITE)))

    for ch in [c for c in chapters if c["number"] in nums]:
        n = ch["number"]
        xp_rows.append((n, ch["challenge"].get("title", ""), ch["challenge"].get("xp", 0)))
        goals = [Paragraph("IN THIS CHAPTER YOU WILL", S("gl", fontName="Body-Bold", fontSize=8, leading=10,
                                                          textColor=TEAL, spaceAfter=4))]
        goals += [Paragraph(f"<font color='#E8892B'>→</font>&nbsp;&nbsp;{rich(g)}", S("g", spaceAfter=2.5))
                  for g in ch.get("learning_goals", [])]
        intro = Table([[P(chunk, "lead", serif_italic=True)] for chunk in re.split(r"\n\s*\n", ch.get("mentor_intro", ""))
                       if chunk.strip()] + [[Paragraph("— your mentor", S("sg", fontName="Serif-Semi", fontSize=10,
                                                                             textColor=MUTED, spaceAfter=0))]],
                      colWidths=[CW])
        intro.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 2.5, AMBER), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story += [NextPageTemplate("opener"), PageBreak(),
                  Anchor(1, f"{n}. {ch['title']}", f"ch{n}"),
                  ChapterBand(n, f"Chapter {n:02d} · {ch.get('part', plabel)}", ch["title"], ch.get("subtitle", "")),
                  padded(goals + [Spacer(1, 10)], top=10 * mm),
                  padded([intro], top=2 * mm),
                  NextPageTemplate("body"), PageBreak(),
                  Running(f"Chapter {n} · {ch['title']}", ptitle)]
        for si, sec in enumerate(ch.get("sections", []), 1):
            story += [CondPageBreak(38 * mm),
                      Paragraph(f"<font color='#E8892B'>{n}.{si}</font>&nbsp;&nbsp;{rich(sec['heading'])}", ST["section"])]
            for b in sec.get("blocks", []):
                story += render_block(b)
            story.append(Spacer(1, 6))
        story += takeaways(ch.get("key_takeaways", []))
        story += challenge_card(n, ch["challenge"])
        story += quiz_block(n, ch.get("quiz", []))

# ---------------------------------------------------------------- back matter
story += [NextPageTemplate("body"), PageBreak(), Running("Your XP tracker", "Back of the book"),
          Anchor(0, "Your XP tracker", "xp"), Paragraph("Your XP tracker", ST["section"]),
          P("Tick each challenge when you've finished it and saved the proof, then add up your XP to find your level.")]
rows = [["", "Chapter", "Challenge", "XP"]]
xp_table = [[Paragraph("Done", ST["cellh"]), Paragraph("Ch.", ST["cellh"]), Paragraph("Challenge", ST["cellh"]),
             Paragraph("XP", ST["cellh"])]]
for n, t, xp in xp_rows:
    xp_table.append([CheckBox(), Paragraph(str(n), ST["cell"]), Paragraph(rich(t), ST["cell"]),
                     Paragraph(str(xp), ST["cell"])])
total = sum(x for _, _, x in xp_rows)
xp_table.append(["", "", Paragraph("<b>Total available</b>", ST["cell"]), Paragraph(f"<b>{total:,}</b>", ST["cell"])])
t = Table(xp_table, colWidths=[13 * mm, 12 * mm, CW - 45 * mm, 20 * mm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DEEP), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                       ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
story += [t, Spacer(1, 12), P("**My XP so far:** ____________     **My level:** ____________", "body"), Spacer(1, 8)]
story += grid([["Level", "Name", "XP", "What it means"]] + [list(l) for l in LEVELS],
              widths=[13 * mm, 26 * mm, 22 * mm, CW - 61 * mm])

# Quiz answers
story += [PageBreak(), Running("Quiz answers", "Back of the book"), Anchor(0, "Quiz answers", "answers"),
          Paragraph("Quiz answers", ST["section"])]
for ch in chapters:
    block = [Paragraph(f"Chapter {ch['number']} · {rich(ch['title'])}", S("qa", fontName="Body-Bold", fontSize=10,
                                                                          leading=13, textColor=DEEP, spaceAfter=3))]
    for i, q in enumerate(ch.get("quiz", [])):
        ai = q.get("answer_index", 0)
        opts = q.get("options", [])
        ans = opts[ai] if 0 <= ai < len(opts) else ""
        block.append(P(f"**{i + 1}. {'ABCD'[ai] if ai < 4 else '?'}**: {ans}. {q.get('explanation', '')}", "cbody"))
    block.append(Spacer(1, 5))
    story.append(KeepTogether(block))

# Glossary
gl = {}
for ch in chapters:
    for g in ch.get("glossary", []):
        k = g.get("term", "").strip()
        if k and k.lower() not in gl:
            gl[k.lower()] = (k, g.get("pt", ""), g.get("meaning", ""))
story += [PageBreak(), Running("Glossary", "Back of the book"), Anchor(0, "Glossary (English · Português)", "glossary"),
          Paragraph("Glossary", ST["section"]),
          P("Every business word in this book, with the Portuguese term you'll hear from clients.")]
story += grid([["Term", "Português", "What it means"]] + [list(v) for _, v in sorted(gl.items())],
              widths=[34 * mm, 34 * mm, CW - 68 * mm])

# Toolkit + last word
story += [PageBreak(), Running("Your toolkit", "Back of the book"), Anchor(0, "Your toolkit", "toolkit"),
          Paragraph("Your toolkit: files you already have", ST["section"])]
story += grid([
    ["File", "What it's for"],
    ["high-ticket/high-ticket-sprint.pdf", "Your 24-hour high-ticket plan: offers, schedule, scripts and tracker"],
    ["high-ticket/scripts-high-ticket.md", "Every script (H1–H9) and Claude prompt (P1–P5), ready to copy"],
    ["high-ticket/demo-site.zip", "Your demo website (fictional company). Unzip it and drag the folder into Netlify Drop"],
    ["high-ticket/demo-site/company-profile.pdf", "Sample capability statement (fictional company), your template"],
    ["high-ticket/escalepay-and-number-one.pdf", "EscalePay verdict and the 30-day plan to become #1"],
    ["24h-cash-sprint.pdf", "Backup plan for fast small jobs (CVs, WhatsApp Business setups, posts)"],
], widths=[62 * mm, CW - 62 * mm])
story += [PageBreak(), Running("A last word", "Back of the book"), Anchor(0, "A last word from your mentor", "last"),
          Spacer(1, 20 * mm), Paragraph("A last word", ST["section"])]
story += [Paragraph(rich(t, True), S("lw", fontName="Serif-It", fontSize=11.4, leading=17.4, spaceAfter=9)) for t in [
    "You started this book with a laptop, two languages and a lot of ambition. That's more than most people start with.",
    "The difference between people who talk about business and people who build one is boring and simple: they do the "
    "small things every day. Twenty messages. One honest follow-up. One more draft. One more call. Nobody sees that work. "
    "Then one day, everyone sees the result.",
    "Protect your name. In a market this small, your reputation is the only asset that grows while you sleep. Never fake "
    "proof, never promise what you can't control, and always deliver a little more than you promised.",
    "When you finish a challenge, show me. When you're stuck, tell me. When you win your first client, I want to hear "
    "about it. Let's get to work.",
]]
story.append(Paragraph("— your mentor, Claude", S("lsig", fontName="Serif-Semi", fontSize=11, textColor=MUTED,
                                                  spaceBefore=6)))

doc = Book(OUT, leftMargin=M, rightMargin=M, topMargin=TOP, bottomMargin=BOT,
           title="Faceless Empire: The Course", author="Claude (AI mentor)",
           subject="A beginner's mentorship for building a high-ticket supplier-readiness business in Mozambique")
doc.multiBuild(story)
print("OK", OUT, "| checkboxes drawn:", CheckBox.count)
