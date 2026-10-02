"""Builds one launch-pack PDF (plus copy-paste Markdown) per EscalePay product from products/products.json.

Run: python3 build_products.py [products.json]
"""
import json
import os
import re
import sys

from ebook_kit import *  # noqa: F401,F403
from ebook_kit import RUN, ST  # noqa: F401

SRC = sys.argv[1] if len(sys.argv) > 1 else "products/products.json"

THEMES = {
    "A-ingles-gas": ("OPÇÃO A", C("#0E3B49"), C("#E8892B"), "For job seekers"),
    "B-whatsapp-vende": ("OPÇÃO B", C("#14532D"), C("#F2B33D"), "For small businesses"),
}


def chunks(text, limit=1800):
    """Split long text into page-safe pieces: by blank lines, then lines, then sentences."""
    out = []
    for para in re.split(r"\n\s*\n", str(text or "")):
        para = para.strip("\n")
        if not para.strip():
            continue
        if len(para) <= limit:
            out.append(para)
            continue
        buf = ""
        for line in para.split("\n"):
            pieces = [line] if len(line) <= limit else re.split(r"(?<=[.!?])\s+", line)
            for piece in pieces:
                if len(buf) + len(piece) + 1 > limit and buf:
                    out.append(buf)
                    buf = ""
                buf = f"{buf}\n{piece}" if buf else piece
        if buf:
            out.append(buf)
    return out


def textbox(label, text, edge=GREEN, bg=SOFT_GREEN, title=None, style="script"):
    head = [Paragraph(label, S("tbl", fontName="Body-Bold", fontSize=7.6, leading=10, textColor=edge, spaceAfter=2))]
    if title:
        head.append(P(title, "ctitle"))
    parts = [P(c, style) for c in chunks(text)]
    rows = [[head + parts[:1]]] + [[f] for f in parts[1:]]
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
    ]))
    return [t, Spacer(1, 9)]


def checks(items, width=CW):
    rows = []
    for it in items or []:
        rows.append([CheckBox(), P(it, "cbody")])
    if not rows:
        return []
    t = Table(rows, colWidths=[8 * mm, width - 8 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (0, -1), 3.5),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE)]))
    return [t, Spacer(1, 8)]


class Button(Flowable):
    """A drawn call-to-action button, to show how the page will look."""

    def __init__(self, text, fill, ink=WHITE):
        super().__init__()
        self.text, self.fill, self.ink = text, fill, ink
        self.p = Paragraph(rich(text), S("btn", fontName="Body-Bold", fontSize=10, leading=12.5, textColor=ink,
                                         alignment=TA_CENTER, spaceAfter=0))

    def wrap(self, aw, ah):
        self.bw = min(aw, 100 * mm)
        self.ph = self.p.wrap(self.bw - 12 * mm, ah)[1]
        self.width, self.height = aw, self.ph + 6 * mm
        return self.width, self.height

    def draw(self):
        self.canv.setFillColor(self.fill)
        self.canv.roundRect(0, 0, self.bw, self.height, 6, stroke=0, fill=1)
        self.p.drawOn(self.canv, 6 * mm, 3 * mm)


def section_title(num, title, key):
    return [CondPageBreak(60 * mm), Anchor(0, f"{num}. {title}", key),
            Paragraph(f"<font color='#E8892B'>{num}</font>&nbsp;&nbsp;{rich(title)}",
                      S("pst", fontName="Serif-Bold", fontSize=19, leading=23, textColor=DEEP, spaceAfter=8)),
            Rule(CW, AMBER, 1.6, 2), Spacer(1, 6)]


def sales_section(i, sec, accent):
    head = Table([[Paragraph(f"SECÇÃO {i:02d} · {rich(sec.get('name', '')).upper()}",
                             S("ssh", fontName="Body-Bold", fontSize=8, leading=10, textColor=WHITE, spaceAfter=0))]],
                 colWidths=[CW])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), DEEP), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                              ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    rows = [[head]]
    if sec.get("purpose"):
        rows.append([P(f"**Why this section exists:** {sec['purpose']}", "small")])
    if sec.get("headline"):
        rows.append([P(sec["headline"], S("shl", fontName="Serif-Bold", fontSize=15.5, leading=19.5, textColor=DEEP,
                                          spaceAfter=0))])
    if sec.get("subheadline"):
        rows.append([P(sec["subheadline"], S("ssub", fontName="Body-Semi", fontSize=10.6, leading=15, textColor=TEAL,
                                             spaceAfter=0))])
    for c in chunks(sec.get("body", ""), 1400):
        rows.append([P(c, "cbody")])
    for b in sec.get("bullets", []) or []:
        rows.append([Paragraph(rich(b), ST["bullet"], bulletText="✓")])
    if sec.get("cta_text"):
        rows.append([Button(sec["cta_text"], accent)])
    if sec.get("design_notes"):
        rows.append([P(f"**Design notes for Lovable:** {sec['design_notes']}", "small")])
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, LINE), ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("LEFTPADDING", (0, 1), (-1, -1), 11), ("RIGHTPADDING", (0, 1), (-1, -1), 11),
        ("TOPPADDING", (0, 1), (-1, -1), 3), ("BOTTOMPADDING", (0, 1), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, 0), 0), ("RIGHTPADDING", (0, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, 0), 0), ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
        ("TOPPADDING", (0, 1), (-1, 1), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
    ]))
    return [t, Spacer(1, 10)]


def build(prod):
    key = prod["key"]
    bp, cp, lv = prod["blueprint"], prod["copy"], prod["lovable"]
    label, dark, accent, audience = THEMES.get(key, ("OPÇÃO", DEEP, AMBER, ""))
    name = bp["product_name"]
    os.makedirs(f"products/{key}", exist_ok=True)
    out = f"products/{key}/{key}-launch-pack.pdf"

    def cover(c, doc):
        c.saveState()
        c.setFillColor(dark)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        for r, a, lw in [(90, 0.10, 30), (64, 0.18, 14), (42, 0.28, 6)]:
            c.setStrokeColor(colors.Color(accent.red, accent.green, accent.blue, alpha=a))
            c.setLineWidth(lw)
            c.circle(W - 18 * mm, 60 * mm, r * mm, stroke=1, fill=0)
        c.setFillColor(accent)
        c.rect(M, H - 40 * mm, 22 * mm, 2.2 * mm, stroke=0, fill=1)
        c.setFont("Body-Black", 11)
        c.drawString(M, H - 34 * mm, f"{label} · {audience.upper()} · ESCALEPAY LAUNCH PACK")
        c.restoreState()

    def draw_back(c, doc):
        draw_body(c, doc)

    doc = BaseDocTemplate(out, pagesize=B5, title=f"{name}: Launch Pack", author="Claude (AI mentor)",
                          subject="Product blueprint, sales page copy, Lovable build prompts and launch plan")
    body = Frame(M, BOT, CW, H - TOP - BOT, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cov = Frame(M, M, CW, H - 2 * M - 30 * mm, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("cover", [cov], onPage=cover),
                          PageTemplate("body", [body], onPageEnd=draw_back)])

    def after(f):
        if isinstance(f, Anchor):
            lvl, text, k = f.toc
            doc.canv.bookmarkPage(k)
            doc.canv.addOutlineEntry(text, k, level=lvl, closed=False)
            doc.notify("TOCEntry", (lvl, text, doc.page, k))
    doc.afterFlowable = after

    RUN["left"], RUN["right"] = name, label
    story = [Spacer(1, 52 * mm),
             Paragraph(rich(name), S("cvn", fontName="Serif-Black", fontSize=34, leading=38, textColor=WHITE)),
             Spacer(1, 4),
             Paragraph(rich(bp.get("tagline", "")), S("cvt", fontName="Serif-It", fontSize=14, leading=20,
                                                       textColor=C("#F4E3C8"))),
             Spacer(1, 14),
             Paragraph(rich(bp.get("one_line_pitch", "")), S("cvp", fontSize=11, leading=16, textColor=C("#DCE8EA"))),
             Spacer(1, 30 * mm),
             Paragraph("Inside: product blueprint · 7-day build plan · full sales page copy in Portuguese · "
                       "thank-you, upsell and affiliate pages · step-by-step Lovable prompts · 14-day launch plan",
                       S("cvi", fontSize=9.5, leading=14, textColor=C("#C9D8DB"))),
             NextPageTemplate("body"), PageBreak(), Running(name, label)]

    toc = TableOfContents()
    toc.levelStyles = [S("pt0", fontName="Body", fontSize=10.5, leading=15, textColor=INK, spaceAfter=1)]
    story += [Paragraph("Contents", ST["section"]), toc, Spacer(1, 10)]

    p = bp.get("pricing", {})
    story += callout("mentor_note", None,
                     "No one can promise you the #1 spot on any platform, and I won't. What puts a product at the top is "
                     "simple: a real problem, an honest offer, a page that converts, affiliates who want to sell it, and "
                     "you showing up every day. This pack gives you all of that. The rest is your work.")
    story += grid([["Step of the funnel", "What happens", "Price"],
                   ["Content + affiliates", "People discover the product on Status, TikTok, Facebook and in groups", "Free"],
                   ["Sales page (Lovable)", "Explains the offer and sends buyers to the checkout", "-"],
                   ["EscalePay checkout", f"Main product, paid with M-Pesa/e-Mola", f"{p.get('main_price_mt', '')} MT"],
                   ["Order bump", p.get("order_bump", {}).get("name", ""), f"+{p.get('order_bump', {}).get('price_mt', '')} MT"],
                   ["Upsell page", p.get("upsell", {}).get("name", ""), f"{p.get('upsell', {}).get('price_mt', '')} MT"],
                   ["Downsell", p.get("downsell", {}).get("name", ""), f"{p.get('downsell', {}).get('price_mt', '')} MT"]],
                  widths=[36 * mm, CW - 62 * mm, 26 * mm])
    story.append(PageBreak())

    # 1. Why this product
    story += section_title(1, "Why this product", "s1")
    story += bullets_block("Why it can win", bp.get("why_it_can_win"))
    story += callout("warning", "Honest risks", "\n\n".join(bp.get("honest_risks", [])))
    story += textbox("THE PROMISE (PORTUGUÊS)", bp.get("promise", ""), TEAL, SOFT_TEAL, style="cbody")
    story += textbox(f"THE METHOD · {bp.get('mechanism_name', '').upper()}", bp.get("mechanism_explained", ""), AMBER_DK,
                     SOFT_AMBER, style="cbody")

    # 2. Buyer
    av = bp.get("avatar", {})
    story += section_title(2, "Your buyer", "s2")
    story += [P(f"**Who:** {av.get('who', '')}"), P(f"**Their situation:** {av.get('situation', '')}")]
    story += grid([["Pains (dores)", "Desires (desejos)"]] +
                  [[a, b] for a, b in zip(av.get("pains", []) + [""] * 12, av.get("desires", []) + [""] * 12)
                   if a or b][:12])
    story += bullets_block("Objections you must answer", av.get("objections"))
    story += bullets_block("Where they spend time online", av.get("where_they_hang_out"))

    # 3. Product
    story += section_title(3, "The product", "s3")
    for i, m in enumerate(bp.get("modules", []), 1):
        rows = [[P(f"**Módulo {i} · {m.get('title', '')}**", S("mh", fontName="Serif-Bold", fontSize=12.5, leading=16,
                                                                textColor=DEEP, spaceAfter=0))],
                [P(f"**Goal:** {m.get('goal', '')}", "cbody")]]
        rows += [[Paragraph(rich(x), ST["bullet"], bulletText="•")] for x in m.get("lessons", [])]
        if m.get("deliverables"):
            rows.append([P("**Deliverables:** " + "; ".join(m["deliverables"]), "small")])
        t = Table(rows, colWidths=[CW])
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, LINE), ("LINEABOVE", (0, 0), (-1, 0), 2.5, accent),
                               ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                               ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                               ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 8)]))
        story += [t, Spacer(1, 8)]
    story += grid([["Bonus", "What it is", "Why it matters"]] +
                  [[b.get("name", ""), b.get("what", ""), b.get("why_it_matters", "")] for b in bp.get("bonuses", [])])
    story += bullets_block("Formats", bp.get("formats"))

    # 4. Build in 7 days
    story += section_title(4, "Build it in 7 days", "s4")
    for d in bp.get("production_plan", []):
        story += [P(f"**{d.get('day', '')}**", "ctitle")] + checks(d.get("tasks"))
    story.append(P("Prompts to create the content with Claude", "ctitle"))
    for cpm in bp.get("claude_prompts", []):
        story += textbox("PASTE INTO CLAUDE", cpm.get("prompt", ""), TEAL, SOFT_TEAL, title=cpm.get("name"))

    # 5. Pricing + EscalePay
    story += section_title(5, "Pricing and EscalePay setup", "s5")
    story += [P(p.get("price_reasoning", ""))]
    story += grid([["Offer", "Name", "Price", "Pitch"],
                   ["Main", name, f"{p.get('main_price_mt', '')} MT", bp.get("one_line_pitch", "")],
                   ["Order bump", p.get("order_bump", {}).get("name", ""), f"{p.get('order_bump', {}).get('price_mt', '')} MT",
                    p.get("order_bump", {}).get("pitch", "")],
                   ["Upsell", p.get("upsell", {}).get("name", ""), f"{p.get('upsell', {}).get('price_mt', '')} MT",
                    p.get("upsell", {}).get("pitch", "")],
                   ["Downsell", p.get("downsell", {}).get("name", ""), f"{p.get('downsell', {}).get('price_mt', '')} MT",
                    p.get("downsell", {}).get("pitch", "")]],
                  widths=[20 * mm, 34 * mm, 18 * mm, CW - 72 * mm])
    story += [P("EscalePay setup checklist", "ctitle")] + checks(bp.get("escalepay_setup"))
    story += callout("warning", "Before you sell to anyone",
                     "Run a test purchase with your own M-Pesa, read the merchant name on the SMS, time the payout, and "
                     "withdraw after every sale. Keep every buyer's contact in your own list. EscalePay's fee claims "
                     "conflict (10% vs 8% + USD 0.50): use the number you see in your dashboard.")

    # 6. Sales page copy
    story += section_title(6, "The sales page: every section, ready to paste", "s6")
    story += [P(f"**SEO title:** {cp.get('seo_title', '')}"), P(f"**Meta description:** {cp.get('meta_description', '')}")]
    for i, sec in enumerate(cp.get("sections", []), 1):
        story += sales_section(i, sec, accent)
    story += [P("FAQ · Perguntas frequentes", "ctitle")]
    for f in cp.get("faq", []):
        story.append(KeepTogether([P(f"**{f.get('q', '')}**", "cbody"), P(f.get("a", ""), "cbody"), Spacer(1, 3)]))
    ck = cp.get("checkout", {})
    story += textbox("CHECKOUT · ORDER BUMP", ck.get("order_bump_text", ""), AMBER_DK, SOFT_AMBER,
                     title=ck.get("order_bump_headline"), style="cbody")
    ty = cp.get("thank_you_page", {})
    story += textbox("THANK-YOU PAGE · /obrigado", "\n\n".join(
        [ty.get("body", "")] + [f"{i}. {s}" for i, s in enumerate(ty.get("steps", []), 1)] + [ty.get("upsell_teaser", "")]),
        TEAL, SOFT_TEAL, title=ty.get("headline"), style="cbody")
    up = cp.get("upsell_page", {})
    story += textbox("UPSELL PAGE · /oferta-especial", "\n\n".join(
        [up.get("subheadline", ""), up.get("body", "")] + [f"✓ {b}" for b in up.get("bullets", [])] +
        [f"YES button: {up.get('cta_yes', '')}", f"NO link: {up.get('cta_no', '')}"]),
        AMBER_DK, SOFT_AMBER, title=up.get("headline"), style="cbody")
    af = cp.get("affiliate_page", {})
    story += textbox("AFFILIATE PAGE · /afiliados", "\n\n".join(
        [af.get("body", "")] + [f"• {b}" for b in af.get("bullets", [])] + [f"Button: {af.get('cta', '')}"]),
        DEEP, SAND, title=af.get("headline"), style="cbody")
    story += [P("WhatsApp messages", "ctitle")]
    for m in cp.get("whatsapp_messages", []):
        story += textbox("WHATSAPP", m.get("text", ""), GREEN, SOFT_GREEN, title=m.get("name"))
    story += callout("warning", "Disclaimers to show on the page", "\n\n".join(cp.get("disclaimers", [])))

    # 7. Lovable
    story += section_title(7, "Build the pages in Lovable", "s7")
    story += [P(lv.get("overview", ""))]
    story += [P("Before you start", "ctitle")] + checks(lv.get("before_you_start"))
    ds = lv.get("design_system", {})
    swatches = [["", "Colour", "Hex", "Use"]]
    for col in ds.get("colors", []):
        try:
            sw = Table([[""]], colWidths=[8 * mm], rowHeights=[5 * mm])
            sw.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C(col.get("hex", "#FFFFFF")))]))
        except Exception:  # bad hex from the model
            sw = ""
        swatches.append([sw, col.get("name", ""), col.get("hex", ""), col.get("use", "")])
    rows = [[c if not isinstance(c, str) else Paragraph(rich(c), ST["cellh"] if i == 0 else ST["cell"]) for c in r]
            for i, r in enumerate(swatches)]
    t = Table(rows, colWidths=[12 * mm, 32 * mm, 22 * mm, CW - 66 * mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DEEP), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story += [t, Spacer(1, 6), P("**Fonts:** " + ", ".join(ds.get("fonts", [])))]
    story += bullets_block("Style notes", ds.get("style_notes"))
    for pr in lv.get("prompts", []):
        story += [CondPageBreak(50 * mm),
                  P(f"**Step {pr.get('step', '')} · {pr.get('page', '')}**",
                    S("lst", fontName="Serif-Bold", fontSize=13, leading=17, textColor=DEEP, spaceAfter=2)),
                  P(f"**Goal:** {pr.get('goal', '')}", "cbody")]
        story += textbox("PASTE INTO LOVABLE", pr.get("prompt", ""), DEEP, C("#EEF2F3"), style="script")
        story += [P("Check in the preview:", "ctitle")] + checks(pr.get("check_after"))
    story += [P("If something goes wrong", "ctitle")]
    for fx in lv.get("fix_prompts", []):
        story += textbox("FIX PROMPT", fx.get("prompt", ""), RED, SOFT_RED, title=fx.get("problem"))
    story += [P("Publish", "ctitle")] + checks(lv.get("publish_steps"))
    story += [P("Final QA before you announce", "ctitle")] + checks(lv.get("qa_checklist"))

    # 8. Launch
    story += section_title(8, "Launch: 14 days to the top of your niche", "s8")
    ap = bp.get("affiliate_program", {})
    story += [P(f"**Affiliate commission:** {ap.get('commission_pct', '')}%. {ap.get('why', '')}")]
    story += bullets_block("Give every affiliate", ap.get("materials"))
    for lp in bp.get("launch_plan", []):
        story += [P(f"**{lp.get('day_range', '')}**", "ctitle")] + checks(lp.get("actions"))
    story += grid([["Platform", "Hook (Português)", "Outline"]] +
                  [[c.get("platform", ""), c.get("hook", ""), c.get("outline", "")] for c in bp.get("content_ideas", [])],
                  title="Content ideas", widths=[24 * mm, 50 * mm, CW - 74 * mm])
    story += grid([["Metric", "Starting target", "Why"]] +
                  [[m.get("metric", ""), m.get("target", ""), m.get("why", "")] for m in bp.get("metrics", [])],
                  title="What to track (starting targets, adjust with real data)", widths=[34 * mm, 34 * mm, CW - 68 * mm])
    story += [P("Rules this product must follow", "ctitle")] + checks(bp.get("compliance"))

    doc.multiBuild(story)

    # Copy-paste companions
    with open(f"products/{key}/sales-copy.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {name}: sales page copy\n\nSEO title: {cp.get('seo_title', '')}\n\nMeta description: {cp.get('meta_description', '')}\n\n")
        for i, sec in enumerate(cp.get("sections", []), 1):
            fh.write(f"## {i:02d} · {sec.get('name', '')}\n\n**{sec.get('headline', '')}**\n\n{sec.get('subheadline', '')}\n\n{sec.get('body', '')}\n\n")
            for b in sec.get("bullets", []) or []:
                fh.write(f"- {b}\n")
            if sec.get("cta_text"):
                fh.write(f"\n[Botão] {sec['cta_text']}\n")
            fh.write("\n")
        fh.write("## FAQ\n\n" + "".join(f"**{f.get('q', '')}**\n\n{f.get('a', '')}\n\n" for f in cp.get("faq", [])))
        fh.write(f"## Order bump\n\n**{ck.get('order_bump_headline', '')}**\n\n{ck.get('order_bump_text', '')}\n\n")
        fh.write(f"## /obrigado\n\n**{ty.get('headline', '')}**\n\n{ty.get('body', '')}\n\n" +
                 "".join(f"{i}. {s}\n" for i, s in enumerate(ty.get("steps", []), 1)) + f"\n{ty.get('upsell_teaser', '')}\n\n")
        fh.write(f"## /oferta-especial\n\n**{up.get('headline', '')}**\n\n{up.get('subheadline', '')}\n\n{up.get('body', '')}\n\n" +
                 "".join(f"- {b}\n" for b in up.get("bullets", [])) + f"\n[SIM] {up.get('cta_yes', '')}\n[NÃO] {up.get('cta_no', '')}\n\n")
        fh.write(f"## /afiliados\n\n**{af.get('headline', '')}**\n\n{af.get('body', '')}\n\n" +
                 "".join(f"- {b}\n" for b in af.get("bullets", [])) + f"\n[Botão] {af.get('cta', '')}\n\n")
        fh.write("## WhatsApp\n\n" + "".join(f"### {m.get('name', '')}\n\n```text\n{m.get('text', '')}\n```\n\n"
                                             for m in cp.get("whatsapp_messages", [])))
        fh.write("## Avisos\n\n" + "".join(f"- {d}\n" for d in cp.get("disclaimers", [])))
    with open(f"products/{key}/lovable-prompts.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {name}: Lovable prompts\n\nPaste one step at a time and check the preview before the next.\n\n")
        for pr in lv.get("prompts", []):
            fh.write(f"## Step {pr.get('step', '')} · {pr.get('page', '')}\n\nGoal: {pr.get('goal', '')}\n\n```text\n{pr.get('prompt', '')}\n```\n\nCheck after:\n" +
                     "".join(f"- [ ] {c}\n" for c in pr.get("check_after", [])) + "\n")
        fh.write("## Fix prompts\n\n" + "".join(f"### {fx.get('problem', '')}\n\n```text\n{fx.get('prompt', '')}\n```\n\n"
                                                for fx in lv.get("fix_prompts", [])))
    return out


if __name__ == "__main__":
    data = json.load(open(SRC, encoding="utf-8"))
    for prod in data["products"]:
        print("OK", build(prod))
    print("checkboxes drawn:", CheckBox.count)
