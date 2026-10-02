"""Builds high-ticket/escalepay-and-number-one.pdf: the EscalePay verdict and the 30-day plan to lead the niche.

Run: python3 build_escalepay.py
"""
from pdf_kit import *  # noqa: F401,F403

OUT = "high-ticket/escalepay-and-number-one.pdf"
story = []

head = Table([[[
    P("ESCALEPAY: VERDICT + HOW TO BECOME #1", "title"), Spacer(1, 4),
    P("Research done 2 October 2026 by 9 research agents (4 research tracks, each checked by a skeptic agent, plus a gap check)", "subtitle"),
]]], colWidths=[CONTENT_W])
head.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), TEAL), ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story += [head, Spacer(1, 8)]

story.append(box([
    P("<b>VERDICT IN ONE LINE</b>", "h3"),
    P("EscalePay is a real, young, Mozambique-facing checkout for <b>digital products</b> (courses, e-books, PLR, "
      "mentorships), with M-Pesa/e-Mola. It is <b>fine to test for a small digital product</b> if you withdraw after every sale. "
      "<b>Never put your 25,000–65,000 MT company deals through it</b>: it takes 8–10%, companies need an invoice with "
      "your NUIT paid by bank transfer, and its 'make money online' image would hurt your brand with procurement managers."),
], bg=GREENBG, border=TEAL))

story.append(P("What we found (and how sure we are)", "h2"))
story.append(grid([
    ["Finding", "Status"],
    ["A checkout + members area for selling digital products: affiliates, co-production, order bumps, subscriptions, an app that "
     "notifies you of sales. Instagram @escalepay.mz (about 8,200 followers).", "Company's own pages"],
    ["Pitch: 'receive the same day, directly in e-Mola or M-Pesa'. The refund policy says refunds go back to the buyer's e-Mola/M-Pesa "
     "in 3–7 business days, which implies buyers pay with mobile money.", "Company's own pages"],
    ["Fee: <b>10% per sale</b> on escalepay.com but <b>8% + $0.50</b> on grupoescale.com (also titled 'EscalePay'). The two "
     "pages contradict each other.", "Company's own pages (conflicting)"],
    ["Operator named in the footer: GRUPO DIGITALIZE LLC, 30 N Gould St, Sheridan, Wyoming (USA). That address is a "
     "registered-agent address used by more than 200,000 companies, some of them linked to fraud cases.", "Footer: company page. Address: independent reporting"],
    ["One policy snippet instead names 'Escale Network, Lda', NUEL 105080035, registered in Mozambique and paying via "
     "'operators licensed in Mozambique'. An OpenCorporates link for 'Grupo Digitalize LLC' points to New Mexico, not Wyoming.",
     "Unverified and contradictory"],
    ["Its anti-money-laundering policy cites US law. We found no Banco de Moçambique licence and no named licensed partner. Reports say a new "
     "payments law (Lei 15/2026) puts all payment providers under BdM licensing.", "Not found + unverified"],
    ["Rules for sellers: identity verification is required (photo ID, proof of address, selfie, source of income). There is a 7-day refund window. "
     "Wording such as 'RG' and Pix looks copied from a Brazilian platform.", "Company's own pages"],
    ["The domain was about 8 months old in a scan from around late 2025 (so roughly 15–18 months now). No press coverage, "
     "no reviews, no complaints found. Complaints you may see online about 'EscalaPay' and 'Skale Pay' are about different, Brazilian companies.", "Third-party scan + searches"],
    ["Claims '500+ creators' and '10,000+ sales', with YouTube testimonials like '10,000 MT in 12 days'.", "Self-reported marketing"],
], [CONTENT_W - 48 * mm, 48 * mm]))
story.append(Spacer(1, 4))
story.append(P("Network limits: escalepay.com, its Instagram and YouTube were blocked from our research environment, so "
               "the findings come from search snippets of those pages. The 30-minute check on the next page closes the gaps from your own phone.",
               "small"))

# ---- Page 2: checks + alternatives -------------------------------------------------
story += [PageBreak(), band("THE 30-MINUTE CHECK: do this before selling anything"), Spacer(1, 6)]
story.append(checklist([
    ("1", "<b>Open an EscalePay account</b> and screenshot the fee and withdrawal settings: the fee per sale, minimum withdrawal, "
          "withdrawal fee and payout time."),
    ("2", "<b>Ask support in writing</b> (WhatsApp or email): 'Is it 10% or 8% + $0.50? What is your Mozambican company and NUEL? "
          "Which licensed entity receives the M-Pesa/e-Mola money? If a buyer is refunded after I've withdrawn, what happens?'"),
    ("3", "<b>Test sale:</b> publish a 50 MT test product and buy it with your own M-Pesa. <b>Read the merchant name on the "
          "M-Pesa SMS</b>: it tells you who really collects the money. Time how long the payout takes."),
    ("4", "<b>Check the Banco de Moçambique list</b> of authorised payment institutions on bancomoc.mz for EscalePay or the merchant from step 3."),
    ("5", "<b>Repeat steps 1–3 on one alternative</b> (Lojou, FambaPay or PaySuite) and pick the one with the best real net payout and a clear legal entity."),
    ("6", "<b>Rule from day one:</b> withdraw after every sale, never keep a balance on the platform, and keep every buyer's "
          "contact in your own list (WhatsApp + Google Sheet)."),
]))
story.append(P("Ways to get paid, compared", "h2"))
story.append(grid([
    ["Option", "What we found (claims, not verified)", "Best use for you"],
    ["Your bank account + NUIT receipt", "No platform fee. Companies are used to paying this way.", "<b>All B2B deals (25,000–65,000 MT)</b>"],
    ["M-Pesa / e-Mola direct", "Instant. Individual limit about 200,000 MT a day.", "Deposits and small payments"],
    ["EscalePay", "8–10% per sale; same-day payout to M-Pesa/e-Mola (claimed)", "Optional: low-ticket digital kit, after the test"],
    ["Lojou", "10% + 10 MT per sale, 48 h payout (claimed)", "Alternative for the kit"],
    ["FambaPay", "10% per sale + processor fees; 10–50,000 MT per transaction", "Alternative for the kit"],
    ["PaySuite (Hypertech)", "M-Pesa, e-Mola, mKesh, cards; about 6% via M-Pesa (3rd-party blog)", "Payment links / websites, if licensed"],
    ["Hotmart", "Pays Mozambicans in USD via Payoneer; no M-Pesa checkout for buyers (local blogs)", "Only if you later sell outside Mozambique"],
], [42 * mm, 78 * mm, CONTENT_W - 120 * mm]))

# ---- Page 3: using EscalePay the right way ------------------------------------------
story.append(CondPageBreak(75 * mm))
story.append(P("How EscalePay CAN help you win (the right way)", "h2"))
story += bullets([
    "<b>A small lead-magnet product, not the business.</b> Sell a 'Kit Fornecedor Pronto' for <b>1,500 MT</b>: a PT/EN "
    "capability-statement template, a document checklist (Mozambique LNG requests list Articles of Association, a "
    "commercial registration certificate under 90 days old, an alvará and past safety performance) and a plain-language "
    "summary of the Local Content Law. Every buyer is a company owner who has just shown interest, which makes them your best lead for the 25,000–65,000 MT packages.",
    "<b>Middle step:</b> 'Kit + 1-hour review call' at <b>5,000–7,500 MT</b>.",
    "<b>Affiliates:</b> give accountants, customs clearing agents and consultants 20–30% commission <b>on the kit only</b>. Never pay commission on the high-ticket service through a platform.",
    "<b>Don't</b> sell PLR, 'make money online' products or betting affiliate links. In Mozambique that market is crowded, cheap and "
    "close to the pyramid and task scams Banco de Moçambique keeps warning about. It would damage the trust your B2B clients need.",
])
story.append(Spacer(1, 4))
story.append(box([P("<b>The ladder:</b>  Free content / EOI radar  →  Kit 1,500 MT  →  Kit + review 5,000–7,500 MT  →  "
                    "<b>Portal-Ready 25,000 MT</b>  →  <b>Supplier-Ready 65,000 MT</b>  →  Retainer 15,000 MT/month", "body")]))

# ---- Page 4-5: be #1 ---------------------------------------------------------------
story += [PageBreak(), band("BECOMING #1 IN MOZAMBIQUE: own one niche completely"), Spacer(1, 6)]
story.append(box([
    P("<b>Your position:</b> \"O estúdio de prontidão de fornecedores para a cadeia do gás e da mineração de Moçambique.\" "
      "(The supplier-readiness studio for Mozambique's gas and mining supply chain.)", "body"),
    Spacer(1, 3),
    P("In everything we found, <b>nobody publicly sells the complete package</b>: a finished bilingual capability statement, "
      "help registering on the supplier portals, a website, and a local-content evidence folder for LNG suppliers. "
      "That's the gap to own.", "body"),
], bg=GREENBG, border=TEAL))
story.append(P("The competition, and the gap you fill", "h2"))
story.append(grid([
    ["Who", "What they do", "Price", "Your angle"],
    ["Web and branding agencies: GOLO, Create, DDB, Agência360, Lugela, DOTMOZ, Mattilo and others",
     "Websites, branding", "Websites listed at 5,000–35,000 MT (Descodando, WebSimples)",
     "They aren't specialised in procurement. Don't compete on 'a website'."],
    ["Local-content consultancies: SD&amp;MP, CLC Solution, consulting.co.mz, MB Consulting",
     "Compliance and qualification advice", "Not public",
     "They advise but don't visibly produce designed bilingual documents. <b>Partner with them.</b>"],
    ["Free programmes: MozUp, CapacitaMoz (100 SMEs trained), ACLM, CTA's Bureau de Conteúdo Local, Clube de Petróleo/IPEME",
     "Training, supplier portals", "Free or subsidised",
     "They train; you turn the training into <b>finished documents</b>. Don't compete with them, complement them."],
], [50 * mm, 32 * mm, 38 * mm, CONTENT_W - 120 * mm]))
story.append(P("Fix the offer before you quote anyone", "h2"))
story += bullets([
    "<b>Lead with 'Portal-Ready' at 25,000 MT:</b> a PT/EN capability statement, a document checklist and guided registration on the "
    "free Mozambique LNG and MozUp supplier portals.",
    "<b>Upsell 'Supplier-Ready' at 65,000 MT:</b> Portal-Ready + a bilingual website + a LinkedIn page + a local-content evidence folder "
    "(ownership, Mozambican payroll, national inputs).",
    "<b>Don't pitch 'a website for 45,000 MT'.</b> Local website price lists stop around 35,000 MT. Sell readiness for contracts, not web pages.",
    "<b>Guarantee:</b> unlimited revisions until the client's portal profile is submitted, plus a deposit refund if they don't "
    "approve the first draft. Never guarantee contracts or certification. Certification will come from entities accredited by the new Local Content Authority.",
])

story.append(CondPageBreak(120 * mm))
story.append(P("The 30-day plan: tick every box", "h2"))
story.append(P("WEEK 1 · 5–11 October · Get formal + get proof", "h3"))
story.append(checklist([
    ("", "<b>Formalise.</b> Find your NUIT and ask the tax office (AT) how to register as self-employed under the simplified small-taxpayer regime (ISPC) so you can issue "
         "receipts to companies. We found conflicting rate figures, so get the current rules from AT."),
    ("", "<b>Register YOURSELF</b> as a supplier on the Mozambique LNG platform (free), under ICT or office services, and on the MozUp portal. "
         "Screenshot every field and upload slot. You'll then know exactly what your clients face, and whether a company profile is requested."),
    ("", "<b>2–3 pilot clients</b> at a discount (e.g. Portal-Ready for 12,500 MT), in exchange for <b>written permission</b> to "
         "publish a before/after and a testimonial. Together with your demo, that's real proof."),
    ("", "<b>Run the 30-minute payment check</b> (page 2)."),
], with_time=False))
story.append(P("WEEK 2 · 12–18 October · The kit + your voice", "h3"))
story.append(checklist([
    ("", "<b>Build the 'Kit Fornecedor Pronto' with me</b> and put it on the checkout that passed your test, at 1,500 MT."),
    ("", "<b>Recruit 5 affiliates</b> (accountants, customs clearing agents, consultants) at 25% commission on the kit."),
    ("", "<b>LinkedIn + Facebook:</b> 3 bilingual posts a week explaining each new supplier opportunity (EOI) in plain Portuguese, including which documents it asks for. "
         "This is how you become the person people quote."),
    ("", "<b>Free credential:</b> HubSpot Inbound certification (free, about 3 h). Add it to LinkedIn."),
], with_time=False))
story.append(P("WEEK 3 · 19–25 October · Partners + lists", "h3"))
story.append(checklist([
    ("", "<b>Partnership pitch</b> to CTA's Bureau de Conteúdo Local, ACLM, Clube de Petróleo/IPEME and consultancies (SD&amp;MP, CLC "
         "Solution, consulting.co.mz, MB Consulting): 'You advise, I produce the bilingual documents.' Agree a referral fee and tell the clients about it."),
    ("", "<b>Target lists:</b> CapacitaMoz-trained SMEs, MozUp alumni, ACLM-certified companies, and companies named in "
         "supplier-opportunity (EOI) responses. They're already trained and motivated."),
    ("", "<b>Publish the pilot case studies</b> (with permission). Before/after pictures sell better than any claim."),
    ("", "<b>Price check:</b> ask 2 agencies and 2 consultancies for their rates on a bilingual company profile. Ask openly, as a "
         "freelancer looking for subcontract work."),
], with_time=False))
story.append(P("WEEK 4 · 26 October – 1 November · Scale your reach", "h3"))
story.append(checklist([
    ("", "<b>'Radar de Oportunidades':</b> a free weekly PT/EN summary of new EOIs on a WhatsApp channel and by email. Later it becomes a "
         "paid subscription at 1,500–3,000 MT a month per company."),
    ("", "<b>Second high-ticket line:</b> 'Business English for Procurement &amp; HSE' for supplier staff, 40,000–90,000 MT for an "
         "in-company group of 5–8 people (the British Council charges 28,875 MT per term per person). Your bilingual skill is the edge."),
    ("", "<b>Africa Gas &amp; LNG Summit, Maputo, 11–13 November 2026</b> (hosted by ACLM, with an SME session). Register or volunteer, bring the "
         "demo on your phone, and offer quick 'capability statement reviews'."),
    ("", "<b>Apply</b> to the next intake of Orange Corners Maputo, the Standard Bank incubator, Ideialab or INCM ThinkLab for mentors and network."),
    ("", "<b>Watch Rovuma LNG</b> (ExxonMobil): a final investment decision is expected around the end of 2026, which will bring a new wave of supplier events."),
], with_time=False))

# ---- Last page: lines never to cross + unverified + sources ------------------------
story += [PageBreak(), band("'AT ALL COSTS', BUT NEVER THESE", RED), Spacer(1, 6)]
story.append(P("In a small market where procurement teams talk to each other, each of these can end your business in a single day:", "body"))
story.append(Spacer(1, 3))
story.append(checklist([
    ("", "No fake reviews, testimonials or followers, and no invented case studies or 'past clients'."),
    ("", "No operator logos (TotalEnergies, ExxonMobil, Eni, ENH, MozUp) used as if they were your clients or partners."),
    ("", "Never claim to be 'certified' or 'accredited' for local content, or 'approved by' anyone."),
    ("", "Never inflate a client's capabilities, HSE record or Mozambican ownership in their documents. That's misrepresentation in a procurement bid."),
    ("", "No bribes and no 'paying for a way in' to a vendor list. Anti-corruption rules apply throughout LNG procurement."),
    ("", "No mass spam that gets your WhatsApp number or email banned."),
], with_time=False))
story.append(P("Unverified: check these before you quote them to clients", "h2"))
story += bullets([
    "<b>Local Content Law thresholds:</b> sources disagree (one says at least 20% Mozambican capital, another 40%). Read the Boletim da "
    "República text before putting numbers in a client document.",
    "<b>The new payments law (Lei 15/2026)</b> and the <b>changes to ISPC</b>: reported in the press and by law firms, but we haven't read the text.",
    "<b>EscalePay's legal entity:</b> the Wyoming LLC in the footer and the 'Escale Network, Lda' NUEL in a policy snippet don't match. Ask EscalePay for its certificate.",
    "<b>Every platform fee in this PDF</b> is the company's own claim. Your test sale is the only fee figure you can rely on.",
])
story.append(Spacer(1, 6))
story.append(box([
    P("<b>Main sources</b>", "h3"),
    P("escalepay.com (home, /politicas/pld, /politicas/privacidade, /politicas/reembolso) · grupoescale.com · instagram.com/escalepay.mz · "
      "wyofile.com (registered-agent fraud) · opencorporates.com/companies/us_nm/6965083 · reclameaqui.com.br (EscalaPay, a different company) · "
      "fambapay.com · kabum.digital (PaySuite; Mozambique agencies 2026) · universodigitalmoz.com (Hotmart in Mozambique) · descodando.com · "
      "websimplesmz.site · lexafrica.com and jlaadvogados.com (Lei 9/2026) · mozambiquelng.co.mz (supplier platform; EOI and seminar PDFs) · "
      "aimnews.org (CapacitaMoz) · dai.com (MozUp) · clubofmozambique.com (CTA Bureau; BdM pyramid warning) · energy-pedia.com (Africa Gas &amp; LNG "
      "Summit) · britishcouncil.org.mz · forbesafricalusofona.com (Lei 15/2026) · dlapiperafrica.com (ISPC) · orangecorners.com · "
      "360mozambique.com (Rovuma FID).", "small"),
]))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=14 * mm,
                        bottomMargin=17 * mm, title="EscalePay Verdict and #1 Plan", author="Plan built with Claude",
                        subject="EscalePay due diligence and a 30-day plan to lead Mozambique's supplier-readiness niche")
on_page = footer("EscalePay verdict + #1 plan  ·  researched 2 Oct 2026  ·  Mozambique")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("OK", CheckBox.count, "checkboxes")
