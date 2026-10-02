"""Family 1 (Caderno do Casal): front journal, question cards (bump), couples devotional (upsell)."""
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from design import (CASAL, Flow, H, M, W, C, cover, draw_para, header_footer, heart, leaf, para_height, rich,
                    rounded_box, style, writing_lines, mm)

T = CASAL


def _intro_pages(f, title, paragraphs, extra_title=None, extra=None, numbered=True):
    f.new_page()
    f.title_block("Antes de começar", title)
    for p in paragraphs:
        f.para(p)
    if extra:
        f.heading(extra_title)
        f.bullets(extra, numbered=numbered)


def season_opener(c, season, idx, encounters, page_no):
    c.setFillColor(T.primary)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(T.secondary)
    c.circle(W * 0.85, H * 0.15, 80 * mm, stroke=0, fill=1)
    c.setFillColor(T.primary)
    c.circle(W * 0.85, H * 0.15, 60 * mm, stroke=0, fill=1)
    heart(c, W * 0.85, H * 0.15, 26 * mm, T.accent)
    c.setFillColor(T.accent)
    c.setFont("Body-Bold", 11)
    c.drawString(M, H - 40 * mm, f"ESTAÇÃO {idx} DE 4")
    y = draw_para(c, season["name"], style("sn", fontName="Serif-Black", fontSize=46, leading=50,
                                           textColor=colors.white), M, H - 48 * mm, W - 2 * M)
    y = draw_para(c, season.get("subtitle", ""), style("ss", fontName="Serif-It", fontSize=16, leading=22,
                                                       textColor=T.secondary), M, y - 4 * mm, W * 0.75)
    y = draw_para(c, season.get("intro", ""), style("si", fontSize=12, leading=18, textColor=colors.white),
                  M, y - 8 * mm, W * 0.72)
    y -= 10 * mm
    c.setFont("Body", 11)
    for e in encounters:
        c.setFillColor(T.accent)
        c.drawString(M, y, f"{e['number']:02d}")
        c.setFillColor(colors.white)
        c.drawString(M + 11 * mm, y, e["title"][:70])
        y -= 7 * mm
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.6))
    c.setFont("Body", 8)
    c.drawCentredString(W / 2, 9 * mm, str(page_no))


def encounter_page(c, enc, season_name, page_no):
    c.setFillColor(T.paper)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    header_footer(c, T, "Caderno do Casal · 52 Encontros", page_no)
    # number badge
    c.setFillColor(T.primary)
    c.circle(W - M - 11 * mm, H - 28 * mm, 11 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Serif-Black", 18)
    c.drawCentredString(W - M - 11 * mm, H - 31 * mm, f"{enc['number']:02d}")
    c.setFillColor(T.accent)
    c.setFont("Body-Bold", 9)
    c.drawString(M, H - 22 * mm, f"ENCONTRO {enc['number']:02d} · {season_name.upper()}")
    width = W - 2 * M - 26 * mm
    y = draw_para(c, enc["title"], style("et", fontName="Serif-Bold", fontSize=21, leading=25, textColor=T.primary),
                  M, H - 25 * mm, width)
    y = draw_para(c, enc.get("intro", ""), style("ei", fontName="Serif-It", fontSize=11.5, leading=16.5,
                                                 textColor=T.ink), M, y - 3 * mm, W - 2 * M) - 4 * mm
    qs = enc.get("questions", [])[:5]
    qst = style("eq", fontName="Body-Semi", fontSize=11, leading=15, textColor=T.ink, leftIndent=8 * mm,
                firstLineIndent=-8 * mm)
    # budget lines to fit: reserve ~78mm for challenge + date + reflection
    avail = y - 18 * mm - 78 * mm
    q_heights = [para_height(f"{i + 1}. {q}", qst, W - 2 * M) + 2 * mm for i, q in enumerate(qs)]
    lines_each = 2 if avail - sum(q_heights) > len(qs) * 2 * 7.2 * mm else 1
    for i, q in enumerate(qs):
        p_text = f"<font color='{T.primary.hexval()}'><b>{i + 1}.</b></font>&nbsp;&nbsp;{rich(q)}"
        from reportlab.platypus import Paragraph
        p = Paragraph(p_text, qst)
        _, h = p.wrap(W - 2 * M, 2000)
        p.drawOn(c, M, y - h)
        y = writing_lines(c, M + 8 * mm, y - h, W - 2 * M - 8 * mm, lines_each, 7.2 * mm) - 3 * mm
    # challenge + date idea side by side
    bw = (W - 2 * M - 6 * mm) / 2
    sb = style("eb", fontSize=10.5, leading=14.5, textColor=T.ink)
    hc = max(para_height(enc.get("challenge", ""), sb, bw - 12 * mm), para_height(enc.get("date_idea", ""), sb, bw - 12 * mm))
    bh = hc + 15 * mm
    for i, (lab, txt, fill) in enumerate([("Desafio da semana", enc.get("challenge", ""), T.soft),
                                          ("Ideia de encontro", enc.get("date_idea", ""), C("#F1E7DA"))]):
        x = M + i * (bw + 6 * mm)
        rounded_box(c, x, y - bh, bw, bh, fill, r=6)
        c.setFillColor(T.primary)
        c.setFont("Body-Bold", 8.5)
        c.drawString(x + 6 * mm, y - 7 * mm, lab.upper())
        draw_para(c, txt, sb, x + 6 * mm, y - 9.5 * mm, bw - 12 * mm)
    y -= bh + 6 * mm
    c.setFillColor(T.primary)
    c.setFont("Body-Bold", 8.5)
    c.drawString(M, y, "O QUE APRENDEMOS HOJE")
    y = draw_para(c, enc.get("reflection_prompt", ""), style("er", fontName="Serif-It", fontSize=10.5, leading=14,
                                                             textColor=T.ink), M, y - 2 * mm, W - 2 * M)
    n_lines = max(2, int((y - 22 * mm) / (7.5 * mm)))
    writing_lines(c, M, y - 1 * mm, W - 2 * M, min(n_lines, 6), 7.5 * mm)
    # tiny check row
    c.setFillColor(C("#8A8A8A"))
    c.setFont("Body", 8.5)
    c.drawString(M, 14 * mm, "Data do encontro: ____/____/______")


def build_front(data_a, data_b, out):
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Caderno do Casal: 52 Encontros para Reconectar")
    c.setAuthor("Caderno do Casal")
    cover(c, T, "Caderno do Casal", "52 encontros para reconectar, conversar de verdade e criar memórias juntos",
          "Um encontro por semana · 4 estações · para imprimir ou usar no tablet")
    c.showPage()
    f = Flow(c, T, "Caderno do Casal · 52 Encontros", start_page=2)
    _intro_pages(f, data_a.get("intro_title", "Bem-vindos"), data_a.get("intro_paragraphs", []),
                 "Regras de ouro de cada encontro", data_a.get("golden_rules", []), numbered=False)
    f.heading("Como usar este caderno")
    f.bullets(data_a.get("how_to_use", []), numbered=True)
    f.c.showPage()
    page = f.page + 1
    seasons = data_a.get("seasons", []) + data_b.get("seasons", [])
    for si, s in enumerate(seasons, 1):
        season_opener(c, s, si, s.get("encounters", []), page)
        c.showPage()
        page += 1
        for enc in s.get("encounters", []):
            encounter_page(c, enc, s["name"], page)
            c.showPage()
            page += 1
    f2 = Flow(c, T, "Caderno do Casal · 52 Encontros", start_page=page)
    f2.new_page()
    f2.title_block("Fim de um ano juntos", data_b.get("closing_title", "Obrigado por chegar até aqui"))
    for p in data_b.get("closing_paragraphs", []):
        f2.para(p)
    heart(c, W / 2, 40 * mm, 14 * mm, T.accent)
    c.showPage()
    c.save()
    return out


CARD_COLORS = ["#C98B5A", "#8E3B2F", "#5B6C8F", "#4F7A5A", "#B5527A"]


def build_cards(data, out):
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("100 Cartões de Perguntas para Casais")
    cover(c, T, "100 Cartões de Perguntas para Casais", "Para jantares, viagens e noites de jogo a dois",
          "Bônus do Caderno do Casal · imprima, recorte e jogue")
    c.showPage()
    f = Flow(c, T, "100 Cartões de Perguntas", start_page=2)
    _intro_pages(f, data.get("intro_title", "Como jogar"), data.get("intro_paragraphs", []), "Como jogar",
                 data.get("how_to_play", []))
    f.heading("As 5 categorias")
    for i, cat in enumerate(data.get("categories", [])):
        f.para(f"<font color='{CARD_COLORS[i % 5]}'><b>{rich(cat['name'])}</b></font> · {rich(cat.get('description', ''))}", raw=True)
    c.showPage()
    page = f.page + 1
    cards = []
    for i, cat in enumerate(data.get("categories", [])):
        for q in cat.get("questions", []):
            cards.append((cat["name"], CARD_COLORS[i % 5], q))
    cw, ch = (W - 2 * M - 6 * mm) / 2, (H - 2 * M - 18 * mm) / 4
    for start in range(0, len(cards), 8):
        c.setFillColor(colors.white)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        for k, (cat, col, q) in enumerate(cards[start:start + 8]):
            col_i, row_i = k % 2, k // 2
            x = M + col_i * (cw + 6 * mm)
            y = H - M - 8 * mm - (row_i + 1) * ch - row_i * 2 * mm
            c.setStrokeColor(C("#BDBDBD"))
            c.setDash(3, 3)
            c.setLineWidth(0.5)
            c.rect(x - 2 * mm, y - 1 * mm, cw + 4 * mm, ch + 2 * mm, stroke=1, fill=0)
            c.setDash()
            rounded_box(c, x, y, cw, ch, colors.white, C(col), r=10, lw=1.4)
            c.setFillColor(C(col))
            c.roundRect(x, y + ch - 11 * mm, cw, 11 * mm, 10, stroke=0, fill=1)
            c.rect(x, y + ch - 11 * mm, cw, 5 * mm, stroke=0, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Body-Bold", 9.5)
            c.drawString(x + 5 * mm, y + ch - 7.3 * mm, cat.upper())
            c.drawRightString(x + cw - 5 * mm, y + ch - 7.3 * mm, f"#{start + k + 1:03d}")
            st = style("cq", fontName="Serif-Semi", fontSize=13, leading=17.5, textColor=T.ink, alignment=1)
            h = para_height(q, st, cw - 14 * mm)
            draw_para(c, q, st, x + 7 * mm, y + (ch - 11 * mm) / 2 + h / 2, cw - 14 * mm)
            heart(c, x + cw / 2, y + 6 * mm, 3 * mm, C(col))
        c.setFillColor(C("#8A8A8A"))
        c.setFont("Body", 8)
        c.drawCentredString(W / 2, 9 * mm, f"{page}  ·  recorte nas linhas tracejadas")
        c.showPage()
        page += 1
    c.save()
    return out


def build_devocional(data, out):
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("Devocional do Casal: 30 Dias Juntos com Deus")
    cover(c, T, "Devocional do Casal", "30 dias juntos com Deus: leitura, conversa e oração a dois",
          "Para casais cristãos · leia na sua própria Bíblia")
    c.showPage()
    f = Flow(c, T, "Devocional do Casal · 30 Dias", start_page=2)
    _intro_pages(f, data.get("intro_title", "Bem-vindos"), data.get("intro_paragraphs", []), "Como usar",
                 data.get("how_to_use", []))
    f.para("As passagens bíblicas aparecem como referência. Leiam juntos na Bíblia de vocês, na tradução que preferirem.",
           f.small)
    c.showPage()
    page = f.page + 1
    for d in data.get("days", []):
        f = Flow(c, T, "Devocional do Casal · 30 Dias", start_page=page)
        f.new_page()
        c.setFillColor(T.accent)
        c.setFont("Body-Bold", 9)
        c.drawString(M, f.y, f"DIA {d['day']:02d} DE 30")
        f.y = draw_para(c, d["title"], style("dt", fontName="Serif-Bold", fontSize=22, leading=26,
                                              textColor=T.primary), M, f.y - 3 * mm, W - 2 * M) - 3 * mm
        ref_w = c.stringWidth("Leitura: " + d.get("reference", ""), "Body-Bold", 10) + 12 * mm
        rounded_box(c, M, f.y - 9 * mm, ref_w, 9 * mm, T.soft, r=4)
        c.setFillColor(T.primary)
        c.setFont("Body-Bold", 10)
        c.drawString(M + 6 * mm, f.y - 6 * mm, "Leitura: " + d.get("reference", ""))
        f.y -= 14 * mm
        f.para(d.get("theme_summary", ""), style("ds", fontName="Serif-It", fontSize=11.5, leading=17, textColor=T.ink))
        f.para(d.get("reflection", ""))
        f.heading("Para conversar")
        for q in d.get("questions", []):
            f.para(f"<font color='{T.accent.hexval()}'><b>•</b></font>&nbsp;{rich(q)}",
                   style("dq", fontName="Body-Semi", fontSize=11, leading=16, textColor=T.ink), raw=True)
            f.lines(2, 7.5 * mm)
        f.boxed("Oração", d.get("prayer", ""), italic=True)
        f.boxed("Ação de hoje", d.get("action", ""), fill=C("#F1E7DA"))
        page = f.page + 1
        c.showPage()
    f = Flow(c, T, "Devocional do Casal · 30 Dias", start_page=page)
    f.new_page()
    f.title_block("Até aqui nos ajudou o Senhor", data.get("closing_title", "Continuem juntos"))
    for p in data.get("closing_paragraphs", []):
        f.para(p)
    c.showPage()
    c.save()
    return out
