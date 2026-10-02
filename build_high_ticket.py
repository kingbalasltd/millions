"""Builds high-ticket/high-ticket-sprint.pdf (tickable checklist) and high-ticket/scripts-high-ticket.md.

Run: python3 build_high_ticket.py
"""
from pdf_kit import *  # noqa: F401,F403

OUT = "high-ticket/"

SCRIPTS = [
    ("H1", "Email: value-first, A-list (Portuguese). Paste the free English paragraph from Prompt P1", """Assunto: [Empresa]: a vossa apresentação em inglês (feita para vocês)

Exmo(a). Sr(a). [Apelido],

Chamo-me [Seu nome] e, a partir de Maputo, preparo perfis de empresa e websites bilingues (português/inglês) para empresas moçambicanas que querem contratos com os sectores do gás, da mineração e com grandes projectos.

Com a retoma do projecto Mozambique LNG e a nova Lei de Conteúdo Local para o sector de petróleo e gás (Lei n.º 9/2026), as equipas de procurement internacionais vão procurar fornecedores moçambicanos online, e em inglês.

Pesquisei a [Empresa] e reparei que [observação concreta e verdadeira: o website só está em português / não encontrei website / a página do Facebook é a única presença online].

Para mostrar o que quero dizer, escrevi a apresentação da [Empresa] em inglês profissional, só com informação pública vossa:

"[parágrafo em inglês do Prompt P1]"

Podem usá-la à vontade. É vossa, sem compromisso.

Faço o pacote completo (perfil de capacidades em PT/EN + website bilingue) em 7 dias. Exemplo do meu trabalho (empresa fictícia): [link do demo]

Tem 15 minutos amanhã ou na segunda-feira para eu mostrar como ficaria para a [Empresa]?

Com os melhores cumprimentos,
[Assinatura]"""),
    ("H2", "WhatsApp: permission message (send after the email, max 15 per hour, no link)", """Boa tarde, Sr(a). [Apelido]. Chamo-me [Seu nome], de Maputo.
Acabei de enviar um email para a [Empresa] com a vossa apresentação escrita em inglês profissional: é gratuita, para usarem com clientes internacionais.
Posso enviar-lha também por aqui?"""),
    ("H3", "Email: short version, B-list (Portuguese)", """Assunto: Pergunta rápida sobre a [Empresa]

Bom dia, Sr(a). [Apelido],

Quando uma equipa de procurement internacional pesquisa a [Empresa] no Google, o que encontra? Hoje, [observação concreta].

Preparo perfis de capacidades e websites bilingues (PT/EN) para fornecedores moçambicanos, prontos em 7 dias. Exemplo (empresa fictícia): [link do demo]

Vale a pena 15 minutos para ver como ficaria para a [Empresa]?

[Assinatura]"""),
    ("H4", "Follow-up: reply on the SAME email thread, next morning (plus one WhatsApp)", """Bom dia, Sr(a). [Apelido],
Só para garantir que viu a apresentação em inglês que preparei para a [Empresa] (abaixo).
Estou a aceitar 3 clientes este mês ao preço de lançamento. Faz sentido falarmos 15 minutos hoje ou na segunda-feira?"""),
    ("H5", "15-minute call script (Portuguese). Ask, listen, then propose", """ABERTURA: "Obrigado pelo seu tempo. Posso fazer-lhe 4 perguntas rápidas e depois mostro-lhe uma proposta?"
1. "Que contratos ou clientes querem conquistar nos próximos 6 meses?"
2. "Quando um cliente grande vos pesquisa hoje, o que encontra?"
3. "Já perderam alguma oportunidade por não terem documentos ou website em inglês?"
4. "Se tivessem perfil e website profissionais em PT/EN dentro de 7 dias, o que isso mudaria?"
PROPOSTA: "Pelo que me disse, recomendo o Pacote Fornecedor Pronto: perfil de capacidades em PT/EN, website bilingue, página de LinkedIn e assinaturas de email. Fica pronto em 7 dias. O investimento é de 65.000 MT, preço de lançamento (o normal é 90.000). São 50% para começar e 50% na entrega. E se não aprovar o primeiro rascunho, devolvo o sinal."
FECHO: "Posso enviar-lhe agora a proposta e os dados de pagamento, para começar hoje?" (Then stay quiet and let them answer.)
OBJECÇÕES:
"Está caro." → "Compreendo. Podemos começar só pelo perfil de capacidades (25.000 MT), que é o documento que os compradores pedem primeiro, e fazer o website depois."
"Tenho de falar com o meu sócio." → "Claro. Envio-lhe já a proposta em PDF. Podemos falar os três amanhã às [hora]?"
"Precisamos de factura." → "Sem problema. Diga-me que documentos o vosso financeiro precisa e eu trato disso."
"Já temos website." → "Óptimo. Então começamos pelo perfil de capacidades em inglês e eu melhoro a versão inglesa do site."
"Mande-me informação." → "Envio já. Para lhe mandar a coisa certa: qual é o próximo contrato que querem ganhar?\""""),
    ("H6", "Proposal: one page (Portuguese). Send within 30 minutes of the call", """PROPOSTA · [Empresa] · [data]

Objectivo: apresentar a [Empresa] de forma profissional a clientes e parceiros internacionais, em português e inglês.

Entregáveis:
1. Perfil de capacidades (capability statement) PT/EN, 8 a 12 páginas, em PDF e editável
2. Website bilingue (PT/EN): 5 secções, botão de WhatsApp, download do perfil e mapa
3. Página de LinkedIn da empresa e assinaturas de email para a equipa

Prazo: 7 dias após o sinal e a recepção das informações.
Investimento: 65.000 MT (preço de lançamento; o normal é 90.000 MT). O domínio (.co.mz ou .com) é pago pelo cliente.
Pagamento: 50% (32.500 MT) para começar e 50% na entrega. Transferência bancária (NIB: [___]) ou M-Pesa ([número]).
Garantia: se não aprovar o primeiro rascunho do perfil, devolvo o sinal na totalidade.
Validade: 7 dias.
Próximo passo: confirmar por WhatsApp ou email e enviar o comprovativo do sinal.

[Seu nome] · [Telefone] · [Email]"""),
    ("H7", "Foreign track: email (English) to foreign companies working in Mozambique", """Subject: Portuguese versions for [Company]'s work in Mozambique

Hi [Name],

I'm [Your name], a bilingual (English/Portuguese) consultant based in Maputo.

I saw that [Company] [specific, true fact: is working on / has opened an office for ...]. Most local partners, staff and authorities here work in Portuguese, so I produce professional Portuguese versions of company profiles, HSE documents and websites, with consistent terminology and fast turnaround.

Example of my work (fictional demo company): [demo link]

Free sample: send me one page and I'll return it in Portuguese within 24 hours.
Projects start from USD 300, paid by bank transfer.

Best regards,
[Your name]
[WhatsApp] · [Email]"""),
    ("H8", "After the deposit: welcome + intake (Portuguese)", """Obrigado! Sinal recebido e confirmado: [valor] MT. Começo hoje.
Para o primeiro rascunho (entrega até [dia e hora]), envie por favor:
1. Logótipo (o ficheiro original, se tiver)
2. Apresentação actual ou qualquer documento da empresa
3. Lista de serviços e principais equipamentos
4. Projectos e clientes que podemos mencionar (só os que autorizam)
5. Certificações e documentos que têm (alvará, registo comercial, NUIT, certidões)
6. Fotos reais da equipa, das obras e dos equipamentos
7. Contactos a publicar (telefone, email e endereço)
Só uso informação verdadeira e confirmada por vocês."""),
    ("H9", "Email signature (set it up in Gmail → Settings → Signature)", """[Nome Apelido]
Websites e Perfis de Empresa Bilingues (PT/EN)
Bilingual Websites & Company Profiles
Maputo, Moçambique · WhatsApp +258 [número]
Exemplo de trabalho: [link do demo]"""),
]

PROMPTS = [
    ("P1", "Value-first mini-audit (use before every A-list email)", """I'm preparing value-first outreach to a Mozambican company. Here is their public information (website, Facebook or Google Maps text): [paste].
1) Write a professional English "About us" paragraph (80-110 words) using ONLY these facts. Don't invent any numbers, clients, years or certifications.
2) List 3 specific, polite observations about gaps in their online presence that an international procurement team would notice.
3) Write a one-line personalised opening for my email in Portuguese."""),
    ("P2", "Capability statement content (delivery)", """Using ONLY the client information below, write a capability statement in English with a Portuguese summary for [company]. Sections: Company overview; Key facts; Core services; Equipment & resources; HSE & quality; Compliance documents available; Project experience (only the projects listed); Contact. Mark anything missing as [MISSING] so I can ask the client. Tone: confident, factual, procurement-friendly.
Client info: [paste]"""),
    ("P3", "Website (say this to me in our chat)", """Adapt the demo website in high-ticket/demo-site for [company]. Replace all the English AND Portuguese text using only these facts: [paste]. Set WHATSAPP_NUMBER to 258XXXXXXXXX, use brand colours [hex codes], replace company-profile.pdf with their profile, and remove the demo ribbon and the 'example' labels."""),
    ("P4", "Proposal from call notes", """Write a one-page proposal in Portuguese for [company] following template H6. Call notes: [paste]. Recommended package: [pack]. Use these prices exactly: [prices]. Don't add any promise I didn't make."""),
    ("P5", "Translation (foreign track)", """Translate the document below from [English/Portuguese] to [Portuguese/English] for use in Mozambique. First list a glossary of 10-20 key technical terms with your chosen translation, then translate. Keep all numbers, names and layout exactly. Flag anything ambiguous in [brackets].
Text: [paste]"""),
]

story = []

# ---- Page 1: the truth + the opportunity -----------------------------------------
cover = Table([[[
    P("HIGH-TICKET SPRINT", "title"), Spacer(1, 4),
    P("Sell 25,000–65,000 MT packages to companies chasing gas, mining and big-project contracts", "subtitle"),
    P("Friday 2 October 11:00 → Saturday 3 October 11:00, then every weekday", "subtitle"),
]]], colWidths=[CONTENT_W])
cover.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), TEAL),
    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story += [cover, Spacer(1, 8)]

story.append(box([
    P("<b>THE HONEST MATHS OF 'A LOT OF MONEY'</b>", "h3"),
    P("One flagship sale is <b>65,000 MT (≈ $1,015)</b>, more than four times the whole small-jobs plan. But companies "
      "that pay this much usually take <b>days, not hours</b>, to decide. So these 24 hours are about filling the "
      "pipeline: <b>book calls, send proposals and, if it goes well, collect the first deposit.</b> Most of the money arrives "
      "over the next 1–14 days, and only if you keep following up. Anyone who promises big money in 24 hours from zero is selling you something."),
], bg=GREENBG, border=TEAL))

story.append(P("Why this market, why now", "h2"))
story += bullets([
    "<b>Mozambique LNG has restarted.</b> TotalEnergies' project fully restarted in January 2026 after force majeure was "
    "lifted, with about <b>USD 4.5 billion committed to Mozambican companies</b> during construction.",
    "<b>Supplier registration is mandatory</b> for any company that wants to supply the project, through its online "
    "supplier registration platform.",
    "<b>A new Local Content Law (Law No. 9/2026, 3 June)</b> makes using national companies mandatory in oil and gas, "
    "with supplier certification and preferential procurement rules.",
    "<b>The gap:</b> thousands of Mozambican SMEs in logistics, construction, catering, security, equipment rental and "
    "HSE training want these contracts, yet many have no English website, no company profile and only a Facebook "
    "page. International procurement teams search for you online before they ever call.",
    "<b>Your edge:</b> you speak Portuguese and English, you know tech, you can sell, and you have Claude. With that, one "
    "laptop can produce agency-quality documents and websites.",
])

story.append(P("Money targets", "h2"))
story.append(grid([
    ["Horizon", "Target", "≈ US$ (64 MT = $1)", "What it takes"],
    ["First 24 h (realistic)", "1 deposit: 12,500–32,500 MT", "$195–$510",
     "40 value-first outreaches → 4–8 replies → 2–4 calls → proposals out worth 150,000+ MT"],
    ["First 24 h (stretch)", "2 deposits: ≈ 65,000 MT", "≈ $1,015", "2 flagship packs closed on calls (50% each)"],
    ["Day 30 (the real prize)", "270,000 MT/month", "≈ $4,220/month",
     "3 flagship packs (195,000) + 5 monthly retainers (75,000). Do 20 outreaches every weekday."],
], [33 * mm, 42 * mm, 28 * mm, CONTENT_W - 103 * mm]))
story.append(Spacer(1, 4))
story.append(P("Day 1 can end with zero deposits. That's normal in high-ticket sales, so judge the day by calls booked and proposals sent. "
               "For scale: many Mozambican sector minimum wages are 7,000–20,000 MT a month.", "small"))

story.append(P("What we are NOT doing", "h2"))
story += bullets([
    "<b>Courses that promise high-ticket income</b> ('become a closer', 'dropshipping', 'AI agency in 7 days'). The person "
    "selling the course makes the money.",
    "<b>Crypto trading, forex signals, betting or 'investment' groups.</b> That's gambling, not income.",
    "<b>Faking it.</b> No invented clients, fake team or fake reviews. One lie found out in procurement ends you.",
])

# ---- Page 2: rules ----------------------------------------------------------------
story += [PageBreak(), band("ZERO-MISTAKES RULES (HIGH-TICKET EDITION): read at 11:00", RED), Spacer(1, 6)]
story.append(P("Money", "h2"))
story.append(checklist([(n, t) for n, t in [
    ("1", "<b>50% deposit before any work.</b> Confirm it in YOUR bank app or M-Pesa SMS, never from a screenshot. Large amounts "
          "should come by bank transfer (individual M-Pesa accounts have a 200,000 MT daily limit)."),
    ("2", "<b>Don't spend a deposit until the client approves the first draft.</b> That's what makes your money-back guarantee safe."),
    ("3", "<b>Overpayment scam:</b> 'I paid too much, please send back the difference' means stop. Never refund before the "
          "original payment has fully cleared in your account."),
    ("4", "<b>Crypto (foreign clients only, and only if THEY ask):</b> accept USDT only. Check the transaction yourself on "
          "the blockchain explorer for the exact network before you start. Never pay a 'fee' to receive money. When "
          "converting to MT peer-to-peer, use only the exchange's escrow and release only after the MT is in your account. "
          "Owning crypto isn't prohibited for individuals in Mozambique, but the central bank warns about the risks."),
]]))
story.append(P("Honesty (this is what protects your reputation)", "h2"))
story.append(checklist([(n, t) for n, t in [
    ("5", "<b>Never invent anything in a client's capability statement:</b> no projects, clients, certifications, staff "
          "numbers or years. False information in a tender can get them disqualified and cause legal trouble for them and you."),
    ("6", "<b>Your demo is labelled as a fictional company.</b> Never say it was a real client."),
    ("7", "<b>Don't imply any link to TotalEnergies, Mozambique LNG or other big names</b>, and don't use their logos. "
          "Mention only public facts."),
    ("8", "<b>Don't promise contract wins.</b> You sell credibility, speed and professionalism, not results."),
    ("9", "<b>You're an independent consultant.</b> Don't invent a team or an agency."),
]]))
story.append(P("Outreach", "h2"))
story.append(checklist([(n, t) for n, t in [
    ("10", "<b>Send at most about 30 personalised cold emails a day from a new Gmail.</b> Use plain text, put the demo LINK in the email "
           "instead of attachments, and never send one email to many recipients at once."),
    ("11", "<b>WhatsApp: ask permission first</b> (H2), send at most 15 an hour, and never paste the same text to many people."),
    ("12", "<b>Read the company name and the person's name twice.</b> 'Dear ABC Lda' sent to XYZ Lda kills the deal."),
    ("13", "<b>A 'no' is final.</b> Reply 'Obrigado pela resposta' and never contact them again."),
    ("14", "<b>Client documents are confidential.</b> Never reuse them or show them to anyone."),
    ("15", "<b>Sleep 22:00–06:30.</b> You'll be talking to directors in the morning, so be sharp."),
]]))

# ---- Page 3: offers ----------------------------------------------------------------
story += [PageBreak(), band("THE OFFER LADDER: few sales, big tickets"), Spacer(1, 6)]
story.append(P("Mozambican companies (paid in MT by bank transfer or M-Pesa)", "h2"))
story.append(grid([
    ["Offer", "What they get", "Launch price", "Normal", "Delivery"],
    ["1. Tender-Ready Company Profile",
     "Capability statement in PT and EN, 8–12 designed pages: overview, services, equipment, HSE, compliance "
     "documents, project experience. PDF + editable file.", "25,000 MT ≈ $390", "35,000", "3 days"],
    ["2. Bilingual Company Website",
     "5-section mobile website in PT/EN with a WhatsApp quote button, profile download and map. You set up free hosting; "
     "the client buys the domain (about $10–20 a year).", "45,000 MT ≈ $700", "60,000", "5 days"],
    ["3. SUPPLIER-READY PACK (flagship)",
     "1 + 2 + LinkedIn company page + email signatures for the team + a checklist of documents needed to register on "
     "supplier platforms.", "65,000 MT ≈ $1,015", "90,000", "7 days"],
    ["4. Monthly Growth Retainer",
     "8 bilingual LinkedIn/Facebook posts, website updates and translation of tender documents (up to 10 pages) every month. "
     "3-month minimum.", "15,000 MT/month ≈ $235", "n/a", "Monthly"],
    ["5. Automation add-on",
     "Website quote form → Google Sheet + instant email alert + WhatsApp pre-filled request + auto-reply.",
     "20,000 MT ≈ $310", "n/a", "2 days"],
], [36 * mm, 70 * mm, 28 * mm, 18 * mm, CONTENT_W - 152 * mm]))
story.append(Spacer(1, 4))
story.append(box([
    P("<b>Terms that close deals</b>", "h3"),
    *bullets([
        "<b>50% to start, 50% on delivery.</b> Send a proposal (H6) within 30 minutes of every call.",
        "<b>Guarantee:</b> 'If you don't approve the first draft, I'll refund your deposit.' That takes away the risk of "
        "hiring someone with no track record yet.",
        "<b>Real scarcity:</b> 'Launch price for my first 3 clients.' That's true, because you can only deliver about 3 packs a week.",
        "<b>Downsell, don't discount:</b> if 65,000 is too much, offer the company profile alone (25,000). Never cut the price of the same package.",
        "<b>Invoices:</b> some companies need a <i>factura</i>. Ask what their finance team needs and register with the tax authority (AT) this "
        "week if necessary. Your NUIT is usually on your bank account documents.",
    ]),
]))
story.append(P("Foreign track (USD): about 20% of your time", "h2"))
story.append(grid([
    ["Offer", "Who buys it", "Price"],
    ["Portuguese versions of company profiles, HSE documents and websites",
     "Foreign contractors and consultancies working in Mozambique (South African, Portuguese, Brazilian, international)",
     "from $300 per project"],
    ["English versions for their Mozambican partners' documents", "The same firms, and their local partners", "from $300"],
], [70 * mm, 72 * mm, CONTENT_W - 142 * mm]))
story.append(Spacer(1, 3))
story.append(P("Get paid by bank transfer: ask your bank (app, website or branch) for the SWIFT details your account needs to "
               "receive USD. Accept USDT only if the client asks for it (rule 4). Trust from abroad builds more slowly, so "
               "Mozambican companies come first.", "small"))

# ---- Pages 4-5: timeline -----------------------------------------------------------
story += [PageBreak(), band("THE 24-HOUR CHECKLIST: tick every box"), Spacer(1, 6)]
story.append(P("BLOCK 1 · FRIDAY 11:00 – 12:30 · Build your proof + your target list", "h2"))
story.append(checklist([
    ("11:00", "<b>Read the rules page.</b> Every rule there prevents a real mistake."),
    ("11:05", "<b>Professional email.</b> If your Gmail address isn't firstname.lastname, create one (free, 5 min). Add the "
              "signature (H9)."),
    ("11:15", "<b>Put the demo website online.</b> Go to app.netlify.com/drop, drag in the <b>demo-site</b> folder, then sign up "
              "free with Gmail to <i>claim</i> the site so it doesn't expire. Rename it (e.g. yourname-demo.netlify.app). "
              "Open it on your phone and test the PT/EN switch and the PDF download."),
    ("11:30", "<b>Check your portfolio:</b> the demo website + company-profile.pdf. Both are clearly labelled as a "
              "fictional sample. Copy the demo link into your notes."),
    ("11:35", "<b>WhatsApp Business profile:</b> '[Your name] · Websites &amp; Company Profiles PT/EN', with the demo link in "
              "the description and offers 1, 2 and 3 in the catalogue."),
    ("11:45", "<b>Target list: 25 companies</b> in the tracker (ideal client signals, sources on the leads page). For each one, write down the "
              "decision maker's name, email, WhatsApp and <i>one specific gap</i>."),
    ("12:20", "<b>Pick your A-list:</b> the 10 with the clearest money + clearest gap."),
]))
story.append(Spacer(1, 4))
story.append(box([P("<b>CHECKPOINT 12:30</b>", "h3"), checklist([
    ("", "Demo website live and tested on a phone"), ("", "Signature and WhatsApp profile done"),
    ("", "25 companies listed · 10 on the A-list"),
], with_time=False, width=INNER_W)], bg=GREENBG, border=TEAL))

story.append(P("BREAK · 12:30 – 14:00", "h2"))
story.append(checklist([("12:30", "Eat away from the laptop. If you're bored, use your phone to add 5 more companies to the list.")]))

story.append(CondPageBreak(140 * mm))
story.append(P("BLOCK 2 · FRIDAY 14:00 – 18:00 · Value-first outreach (the money block)", "h2"))
story.append(checklist([
    ("14:00", "<b>A-list, 10 companies at about 10 min each.</b> Copy their public About text → <b>Prompt P1</b> → you get a "
              "free English paragraph + gaps. Send <b>email H1</b> with the paragraph inside, then <b>WhatsApp H2</b>."),
    ("15:45", "<b>B-list, 10 companies at about 5 min each:</b> short <b>email H3</b>."),
    ("16:30", "<b>Reply to every response within 15 minutes.</b> The goal is a 15-min call today (17:00–18:00) or tomorrow (08:00–10:00)."),
    ("17:00", "<b>Calls:</b> follow the script (H5). Ask, listen, propose, then ask for the deposit. Make every call by WhatsApp or Google Meet."),
    ("17:30", "<b>Proposal within 30 minutes of each call</b> (Prompt P4 + template H6), sent as a PDF by email and WhatsApp."),
    ("17:50", "<b>Update the tracker:</b> stage and value for every company."),
]))
story.append(Spacer(1, 4))
story.append(box([P("<b>CHECKPOINT 18:00</b>", "h3"), checklist([
    ("", "20 value-first emails sent"), ("", "15 WhatsApp permission messages sent"),
    ("", "Replies: ______    Calls booked: ______    Proposals out: ______"),
], with_time=False, width=INNER_W)], bg=GREENBG, border=TEAL))

story.append(P("DINNER · 18:00 – 19:00", "h2"))
story.append(checklist([("18:00", "Eat. If a director replies, answer with a call time and nothing more.")]))

story.append(CondPageBreak(95 * mm))
story.append(P("BLOCK 3 · FRIDAY 19:00 – 22:00 · Foreign track + proposals + start delivering", "h2"))
story.append(checklist([
    ("19:00", "<b>Foreign track: 10 companies.</b> Search Google and news for 'contractor Mozambique LNG', 'South African company "
              "Mozambique office', 'Portuguese company Maputo project' and similar. Find a manager's email. Send <b>H7</b>."),
    ("20:00", "<b>Follow up every warm thread.</b> Send proposals to anyone who replied and confirm tomorrow's call times."),
    ("20:30", "<b>If a deposit arrived:</b> confirm it in your bank or M-Pesa, send <b>H8</b> and start the first draft of the company profile tonight "
              "(Prompt P2). Quick visible progress builds trust."),
    ("21:30", "<b>Prepare tomorrow:</b> 15 new companies in the tracker. Draft the follow-ups (H4)."),
    ("22:00", "<b>Sleep.</b>"),
]))

story.append(CondPageBreak(110 * mm))
story.append(P("BLOCK 4 · SATURDAY 06:30 – 11:00 · Follow-up is where high-ticket deals close", "h2"))
story.append(checklist([
    ("06:30", "<b>Answer every overnight reply.</b>"),
    ("07:30", "<b>Follow-up H4</b> to every A-list company that didn't reply: reply on the same email thread + 1 WhatsApp."),
    ("08:00", "<b>15 new value-first outreaches</b> (P1 + H1). Owners are often at their desks on Saturday mornings."),
    ("08:00", "<b>Bank:</b> if your branch opens on Saturday, ask for your SWIFT details for USD (foreign track) and confirm your NUIT."),
    ("09:00", "<b>Calls + proposals.</b> Ask for the deposit on every call: 'Posso enviar os dados de pagamento para começar hoje?'"),
    ("10:00", "<b>Deposits:</b> confirm each one in your account → send H8 → agree the first-draft deadline."),
    ("10:45", "<b>Final count:</b> deposits, proposals out, pipeline value and calls booked for next week."),
    ("11:00", "<b>Lock in the routine:</b> 20 value-first outreaches every weekday, with follow-ups on day 3 and day 7. "
              "Pipeline × time = money."),
]))
story.append(Spacer(1, 4))
story.append(box([P("<b>FINAL CHECKPOINT · SATURDAY 11:00</b>", "h3"), checklist([
    ("", "Deposits received and confirmed: ____________ MT"),
    ("", "Proposals out: ______  ·  total value: ____________ MT"),
    ("", "Calls booked for next week: ______"),
], with_time=False, width=INNER_W)], bg=GREENBG, border=TEAL))

# ---- Scoreboard + leads ----------------------------------------------------------------
story += [PageBreak(), band("SCOREBOARD + WHERE TO FIND COMPANIES"), Spacer(1, 6)]
story.append(grid([
    ["Activity", "Goal 12:30", "Actual", "Goal 18:00", "Actual", "Goal 22:00", "Actual", "Goal Sat 11:00", "Actual"],
    ["Value-first emails", "0", "", "20", "", "30", "", "45", ""],
    ["WhatsApp permission msgs", "0", "", "15", "", "20", "", "35", ""],
    ["Replies", "0", "", "2", "", "4", "", "8", ""],
    ["Calls booked", "0", "", "1", "", "2", "", "4", ""],
    ["Calls done", "0", "", "1", "", "1", "", "3", ""],
    ["Proposals sent", "0", "", "1", "", "2", "", "4", ""],
    ["Pipeline value (MT)", "0", "", "65,000", "", "130,000", "", "260,000", ""],
    ["Deposits (MT)", "0", "", "0", "", "0", "", "32,500", ""],
], [40 * mm] + [(CONTENT_W - 40 * mm) / 8] * 8))
story.append(Spacer(1, 4))
story.append(P("Behind schedule? Don't cut prices. Send more value-first outreach. Each P1 paragraph is a gift that "
               "gets replies.", "small"))

story.append(P("Ideal client: tick 3 or more before you contact them", "h2"))
story.append(grid([
    ["Signal", "What to look for"],
    ["Sector", "Logistics/transport, freight forwarding and customs clearing (despachantes), civil construction, equipment "
               "rental, security, catering and camp services, cleaning/facilities, HSE training, engineering or "
               "environmental consulting, IT, manpower agencies"],
    ["Region", "Pemba, Palma and Montepuez (Cabo Delgado) · Maputo/Matola · Beira · Nacala · Tete"],
    ["Has money", "Hiring now (on emprego.co.mz), shows a fleet or equipment, has a real office, in business 3+ years, has won tenders"],
    ["Has a gap", "No website, a Portuguese-only or outdated site (© 2018, not mobile-friendly), only a Facebook page, a Gmail "
                  "address, or no company profile online"],
    ["Decision maker", "Director-Geral, Sócio-Gerente, Administrador or Director Comercial. Find the name on their website, Facebook or LinkedIn."],
], [30 * mm, CONTENT_W - 30 * mm]))
story.append(P("Lead sources (all free, all online)", "h2"))
story.append(P("<b>1. emprego.co.mz.</b> Companies hiring right now have money and are growing. Job ads often show the company "
               "email. Look up each company's website and note what's missing."))
story.append(Spacer(1, 3))
story.append(P("<b>2. Google Maps.</b> Search these and open the businesses that have reviews:"))
story.append(box([P("transitário Pemba · despachante aduaneiro Maputo · logística Nacala · transporte de carga Beira · "
                    "aluguer de equipamentos Tete · construção civil Pemba · empreiteiro Maputo · catering Pemba · "
                    "segurança privada Maputo · limpeza industrial Maputo · formação HSE Maputo · consultoria ambiental "
                    "Maputo · engenharia Matola · recrutamento Maputo · serviços mineiros Tete", "script")]))
story.append(Spacer(1, 3))
story.append(P("<b>3. Chamber of commerce directories.</b> Search 'directório de associados' for the Portugal-Mozambique Chamber "
               "(CCPM), AMCHAM Mozambique and other bilateral chambers. These are lists of real companies with contacts."))
story.append(Spacer(1, 3))
story.append(P("<b>4. Facebook company pages.</b> Pages with photos of fleets and job sites but no website link are "
               "perfect A-list leads."))
story.append(Spacer(1, 3))
story.append(P("<b>5. News.</b> Local news about Mozambique LNG supplier workshops, tenders and new contracts names companies "
               "that are actively bidding."))
story.append(Spacer(1, 3))
story.append(P("<b>6. LinkedIn (optional, free):</b> make a profile with the headline 'Bilingual websites &amp; company profiles "
               "(PT/EN) for Mozambican suppliers' and use it to find directors' names. Don't send mass connection requests."))

# ---- Scripts -----------------------------------------------------------------------
story += [PageBreak(), band("SCRIPTS: copy, personalise, send"), Spacer(1, 4)]
story.append(P("Replace everything in [brackets] and never send a message with a bracket still in it. Mozambican directors usually "
               "prefer Portuguese, so start in Portuguese and switch to English if they do. Everything here is also in "
               "<b>scripts-high-ticket.md</b> for clean copy-paste.", "small"))
story.append(Spacer(1, 4))
for code, title, text in SCRIPTS:
    story.append(script_block(code, title, text))

# ---- Delivery ------------------------------------------------------------------------
story += [CondPageBreak(120 * mm), Spacer(1, 6), band("DELIVERY: the 7-day Supplier-Ready Pack, with Claude"), Spacer(1, 4)]
story.append(checklist([
    ("Day 0", "Deposit confirmed in your account → <b>H8</b> intake list → create a WhatsApp group with the client contact."),
    ("Day 1", "<b>Company profile first draft:</b> Prompt P2 → layout (ask me to build it like the sample) → send the draft. "
              "<b>Guarantee checkpoint:</b> get written approval ('aprovado') on WhatsApp or email."),
    ("Day 2", "Corrections → final PDF + editable version. Check every number, name and certificate against the client's documents."),
    ("Day 3–4", "<b>Website:</b> paste Prompt P3 to me with their facts → I adapt the demo → you check both languages on a phone."),
    ("Day 5", "Deploy to the client's own free Netlify account (they own it). Connect their domain. Test the WhatsApp button and the PDF download."),
    ("Day 6", "LinkedIn company page (created from the client's own LinkedIn profile, with you guiding) + email signatures for the team."),
    ("Day 7", "Final review call → collect the 50% balance and confirm it → hand over all files and logins → ask for a testimonial, "
              "a referral and the retainer (offer 4)."),
]))
story.append(Spacer(1, 6))
story.append(P("Claude prompts", "h2"))
for code, name, text in PROMPTS:
    story.append(script_block(code, name, text))

# ---- Tracker -------------------------------------------------------------------------
story += [CondPageBreak(150 * mm), Spacer(1, 6), band("PIPELINE TRACKER: copy these columns into Google Sheets"), Spacer(1, 6)]
hdr = ["#", "Company", "Sector / city", "Decision maker", "Email / WhatsApp", "Gap observed", "Stage", "Value (MT)", "Next step + date"]
rows = [hdr] + [[str(i)] + [""] * 8 for i in range(1, 16)]
story.append(grid(rows, [7 * mm, 27 * mm, 20 * mm, 22 * mm, 25 * mm, 25 * mm, 16 * mm, 16 * mm,
                         CONTENT_W - 158 * mm]))
story.append(Spacer(1, 4))
story.append(P("<b>Stage:</b> Listed → Sent → Replied → Call booked → Call done → Proposal → Deposit → Delivered → Retainer.", "small"))

story.append(Spacer(1, 8))
story.append(box([
    P("<b>Sources for the facts in this plan</b>", "h3"),
    P("Mozambique LNG restart (Jan 2026) and USD 4.5 bn for Mozambican companies: theenergyyear.com, worldoil.com, aljazeera.com · "
      "Supplier registration platform: mozambiquelng.co.mz · Local Content Law No. 9/2026: plmj.com, lexafrica.com, afriwise.com · "
      "M-Pesa daily limits: forbesafricalusofona.com · Crypto status: regalert.today, afriwise.com (VASP notice 4/GBM/2023) · "
      "Exchange rate about 64 MT/USD (Jul 2026): fx-rate.net · Sector minimum wages: wageindicator.org.", "small"),
]))

doc = SimpleDocTemplate(
    OUT + "high-ticket-sprint.pdf", pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=14 * mm, bottomMargin=17 * mm, title="High-Ticket Sprint",
    author="Plan built with Claude",
    subject="24-hour high-ticket plan: bilingual company profiles and websites for Mozambican suppliers",
)
on_page = footer("High-Ticket Sprint  ·  Fri 2 Oct 11:00 → Sat 3 Oct 11:00  ·  Mozambique")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

md = ["# High-Ticket Sprint: copy-paste scripts", "",
      "Replace every `[bracket]` before sending. Demo link goes where it says `[link do demo]`.", ""]
for code, title, text in SCRIPTS:
    md += [f"## {code}: {title}", "", "```text", text, "```", ""]
md += ["# Claude prompts", ""]
for code, name, text in PROMPTS:
    md += [f"## {code}: {name}", "", "```text", text, "```", ""]
with open(OUT + "scripts-high-ticket.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("OK", CheckBox.count, "checkboxes")
