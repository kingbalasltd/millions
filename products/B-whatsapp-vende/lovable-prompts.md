# WhatsApp que Vende: Lovable prompts

Paste one step at a time and check the preview before the next.

## Step 1 · Project setup + design system + global components

Goal: Create the foundation: config file with all links/flags, colour and font tokens, routes, RichText/placeholder helpers, CTA button, header, footer with exact copy, sticky mobile buy bar and the help (WhatsApp contact) button.

```text
Create a mobile-first sales website in Portuguese (Mozambique) for a digital product called “WhatsApp que Vende”. Stack: React + TypeScript + Tailwind CSS + shadcn/ui + React Router (your defaults). In THIS step build ONLY the foundation: config file, design system, routes and global components. Do not write the sales page content yet; I will send it in the next message.

1) CONFIG FILE. Create src/config/site.ts with exactly these exports (I will edit the values later; keep them exactly as written now):
SITE_URL = 'https://SEU-SITE.lovable.app'
ESCALEPAY_CHECKOUT_URL = 'https://COLE-AQUI-O-LINK-DO-CHECKOUT-PRINCIPAL'
ESCALEPAY_UPSELL_URL = 'https://COLE-AQUI-O-LINK-DO-CHECKOUT-DO-SERVICO'
REVISAO_EXPRESS_URL = ''
ESCALEPAY_REFUND_POLICY_URL = 'https://COLE-AQUI-O-LINK-DA-POLITICA-DE-REEMBOLSO'
AFFILIATE_APPLY_URL = ''
WHATSAPP_NUMBER = '258XXXXXXXXX'  (digits only, used in wa.me links)
WHATSAPP_DISPLAY = '[TEU_WHATSAPP]'
CREATOR_NAME = '[TEU_NOME]'
CREATOR_CITY = '[cidade]'
CREATOR_EMAIL = '[TEU_EMAIL]'
CREATOR_PHOTO = ''
MOCKUP_IMAGE = ''
BONUS_IMAGES: string[] = []
PDF_PAGE_IMAGES: string[] = []
SOCIAL_LINKS = { tiktok: '', instagram: '', facebook: '' }
PRICE_MAIN = 597; PRICE_BUMP = 147; PRICE_UPSELL = 1497; CURRENCY = 'MZN'
SHOW_TESTIMONIALS = false
SHOW_INTERVIEW_PARAGRAPHS = true
SHOW_STEP1_NOTE = true
HIGHLIGHT_PLACEHOLDERS = true
META_PIXEL_ID = ''
TIKTOK_PIXEL_ID = ''
LEGAL_LAST_UPDATED = '[data]'
Also export two helpers: waLink(text) returns 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(text); formatMT(n) returns Portuguese formatting with a dot for thousands plus ' MT' (597 → '597 MT', 1497 → '1.497 MT').
Never hardcode any of these values anywhere else in the project; always import them from this file.

2) DESIGN SYSTEM. Define these as CSS variables in index.css, map them in tailwind.config, and map shadcn's primary/background/foreground/border/ring to them:
background #FAF7F0 (warm off-white page), surface #FFFFFF (cards), ink #13261F (headings), body #33433D (paragraphs), muted #5E6E68 (notes), primary #0F7B5F (deep green: buttons, links, icons), primary-hover #0B634C, tint #E7F2EC (light green bands), border #DDE5E0, accent #D9952B (ochre, decorative only: thin bars, lines, rings, never text), neutral-icon #8C9A94, placeholder #FFF1A8.
FORBIDDEN anywhere in the project: the colours #25D366, #128C7E, #075E54 (WhatsApp greens), the WhatsApp logo, chat-bubble icons, Meta branding.
Fonts: load from Google Fonts in index.html with preconnect and display=swap: 'Bricolage Grotesque' weights 700 and 800 for headings, prices and big letters; 'Inter' weights 400, 500, 600 and 700 for everything else; fallback system-ui, sans-serif.
Type scale (mobile → desktop): h1 30-34px → 52px, line-height 1.15, weight 800; h2 26-28px → 40px, weight 800; h3 20px → 22px, weight 700; body 17px → 18px, line-height 1.6; small 14-15px. Headings use ink, paragraphs use body.
Shape: cards radius 16px, 1px border, very soft shadow (0 1px 2px rgba(19,38,31,.06), 0 8px 24px rgba(19,38,31,.06)); buttons radius 12px; pills fully rounded. Icons: lucide-react, stroke width 1.75. Spacing: page side padding 16px on mobile and 24px on tablet; content max width 1120px; text columns max 680px; section vertical padding 56px mobile and 96px desktop. Visible 3px primary focus ring on every interactive element. Respect prefers-reduced-motion; only subtle fade-ins.
Set <html lang='pt-MZ'> and overflow-x: hidden on body so the page never scrolls sideways.

3) ROUTES (React Router): '/' (temporary text 'Página de vendas em construção'), '/obrigado', '/oferta-especial', '/afiliados', '/privacidade', '/termos' (simple placeholders for now), '/configuracao' redirecting to '/oferta-especial', and a catch-all 404 page with the text “Página não encontrada.” and a link “Voltar à página inicial” to '/'. Scroll to the top on every route change.

4) SHARED UTILITIES AND COMPONENTS
a) fillPlaceholders(text): replaces “[TEU_WHATSAPP]” with WHATSAPP_DISPLAY, “[TEU_EMAIL]” with CREATOR_EMAIL, “[TEU_NOME ou nome do negócio registado]” and then “[TEU_NOME]” with CREATOR_NAME, “[cidade real]” and then “[cidade]” with CREATOR_CITY.
b) RichText component: takes a string, runs fillPlaceholders, splits paragraphs on blank lines into <p> elements, renders **text** as <strong> (the asterisks must never be visible), and wraps any remaining [text in square brackets] in a <mark> with the placeholder background and a dashed outline when HIGHLIGHT_PLACEHOLDERS is true (when false, render it as normal text). It must never change the words.
c) Container and Section components (Section takes an id and a background variant: page | white | tint | primary).
d) CtaButton: props label, href (default ESCALEPAY_CHECKOUT_URL), variant 'primary' (primary bg, white text) | 'outline' (white bg, 2px primary border, primary text) | 'white' (white bg, primary text, for the dark green band), ctaId, size 'lg' | 'sm', external (opens a new tab only when true). Render a real <a> element, same tab by default, full width on mobile with max-width 420px, min-height 52px (sm: 44px), 17px semibold, label may wrap to 2 lines and stays centred, hover uses primary-hover. On click call trackCheckoutClick(ctaId, href) from src/lib/analytics.ts. Create that file now with empty stub functions trackCheckoutClick and trackPageView; they will be filled in later. Clicking must never be blocked or delayed.
e) Header (not sticky): on the left the text wordmark “WhatsApp que Vende” (“WhatsApp” in ink, “que Vende” in primary, Bricolage Grotesque 800, 20px) linking to '/'. On the right, on desktop only, a CtaButton size sm with label “Comprar - 597 MT”. On '/oferta-especial' show only the wordmark, without link and without button.
f) Footer on all pages: small 14px muted text, background #FAF7F0, top border, and 96px extra bottom padding on mobile so the sticky bar never covers it. Use this exact copy, rendered through RichText, without changing any word:
Title: “WhatsApp que Vende”
Subtitle: “Guia prático para pequenos negócios que vendem pelo WhatsApp em Moçambique.”
P1: “Contacto: WhatsApp [TEU_WHATSAPP] | Email [TEU_EMAIL]”
P2: “Responsável: [TEU_NOME ou nome do negócio registado], [cidade], Moçambique.”
P3: “Este produto não é afiliado, patrocinado nem aprovado pela Meta ou pelo WhatsApp. WhatsApp é uma marca registada da Meta Platforms, Inc.”
P4: “Pagamentos processados pela EscalePay. Reembolsos dentro de 7 dias, de acordo com a política da plataforma.”
P5: “Os resultados variam. Não garantimos vendas, rendimentos, lucros nem empregos.”
Links row: “Política de privacidade” → /privacidade; “Termos e condições” → /termos; “Política de reembolso” → ESCALEPAY_REFUND_POLICY_URL (new tab, rel noopener noreferrer).
Last line: “© ” + current year + “ ” + CREATOR_NAME.
g) StickyMobileCTA: only on '/' and only below 768px. Fixed bottom bar, white background, top border, soft shadow, bottom padding with env(safe-area-inset-bottom). Left: “597 MT” (Bricolage Grotesque 800, 22px, ink). Right: CtaButton size sm with label “Comprar” and ctaId 'sticky'. Using IntersectionObserver, show it only after the element with id 'hero-cta' has scrolled out of view upwards, and hide it while the section with id 'final_cta' is on screen. Slide in and out smoothly.
h) HelpFloat (a contact button, NOT a WhatsApp-branded button): fixed bottom-right at 16px, pill shape, background ink #13261F, white text, lucide HelpCircle icon plus the text “Dúvidas?”, min height 48px, linking to waLink('Olá, tenho uma dúvida sobre o WhatsApp que Vende') in a new tab, aria-label “Tirar dúvidas pelo WhatsApp”. On '/' on mobile, while the sticky bar is visible, move it up (about 84px from the bottom) so the two never overlap. Hidden on '/oferta-especial'.
i) Layout component that wraps every page with Header, <main id='conteudo'>, Footer, HelpFloat and StickyMobileCTA, plus a skip link “Saltar para o conteúdo” that is visible on keyboard focus.

When finished, reply only with the list of files you created. Do not add any other sections, texts or features.
```

Check after:
- [ ] Mobile view (phone icon): off-white background, no sideways scrolling, wordmark 'WhatsApp que Vende' with 'que Vende' in deep green
- [ ] Headings look like Bricolage Grotesque (rounded, characterful) and body text like Inter; accents (ç, ã, é) display correctly
- [ ] Footer shows the 5 paragraphs word for word, and [TEU_WHATSAPP], [TEU_EMAIL], [TEU_NOME], [cidade] are highlighted yellow
- [ ] The dark 'Dúvidas?' pill is at the bottom right, with no WhatsApp logo and no bright WhatsApp green; tapping it opens wa.me/258XXXXXXXXX with the prefilled message
- [ ] /obrigado, /afiliados, /privacidade and /termos open; /oferta-especial shows only the wordmark and no Dúvidas? pill; /configuracao redirects; a random URL shows the Portuguese 404
- [ ] In Code view, src/config/site.ts exists with all the constants and src/lib/analytics.ts has the two stub functions

## Step 2 · Sales page (/)

Goal: Build the full sales page with all 16 sections in order, with the reviewed Portuguese copy stored and rendered word for word, and every buy button linked to ESCALEPAY_CHECKOUT_URL.

```text
Build the complete sales page on the route '/' (replace the placeholder). Reuse what exists from step 1: src/config/site.ts constants, colour tokens, fonts, Container/Section, RichText, fillPlaceholders, waLink, CtaButton, Header, Footer, StickyMobileCTA and HelpFloat. Design reminder: background #FAF7F0, cards #FFFFFF, headings #13261F, paragraphs #33433D, primary deep green #0F7B5F, green band #E7F2EC, border #DDE5E0, ochre #D9952B decorative only, neutral icon grey #8C9A94.

COPY RULES (follow strictly):
1. Every Portuguese text between “ and ” below is final, reviewed copy. First create src/content/salesCopy.ts and store every text there exactly as written, character for character: accents, hyphens, apostrophes, capitals and the Mozambican spelling (actualização, exactamente, objecções, reactivar, acção, colecções). Components must read the texts from this file. Do not translate, shorten, correct, reorder, 'improve' or add any marketing text. Do not include the “ ” marks themselves.
2. **double asterisks** = bold, rendered through RichText (asterisks never visible). P1, P2... = separate paragraphs.
3. [square brackets] = placeholders. Keep them exactly and render through RichText, so [TEU_WHATSAPP], [TEU_EMAIL], [TEU_NOME], [cidade], [cidade real] are filled from config and all others are highlighted.
4. Every buy button is a CtaButton → ESCALEPAY_CHECKOUT_URL, same tab, with ctaId = the section id.
5. FORBIDDEN on this page: countdown timers, visitor or stock counters, 'someone just bought' pop-ups, star ratings, crossed-out or 'valor real' prices, price tags on bonuses, invented testimonials, numbers or statistics, stock photos, the WhatsApp logo, chat-bubble icons, Meta branding, and the colours #25D366, #128C7E, #075E54.

LAYOUT: one <section> per block below, in this exact order, with the given id. Max width 1120px; text columns max 680px; 16px side padding on mobile; vertical padding 56px mobile and 96px desktop. Alternate page/white backgrounds so sections are clearly separated; the bonuses band uses #E7F2EC; the final CTA is solid #0F7B5F. Exactly one h1 (the hero headline); every other section headline is an h2 (26-28px mobile, 40px desktop, Bricolage Grotesque 800).

SECTION 1, id 'hero'
h1 (30px at 360px width up to 34px, max 3 lines on mobile, 52px desktop): “Transforma o teu WhatsApp numa loja organizada que atende, cobra e traz o cliente de volta.”
Subheadline: “Guia prático com scripts prontos, respostas rápidas, calendário de Status de 30 dias e modelos Canva, para quem vende pelo WhatsApp em Moçambique.”
Mockup image: MOCKUP_IMAGE, alt 'Capa do guia WhatsApp que Vende num telemóvel Android', max height 340px on mobile, loading eager. If MOCKUP_IMAGE is empty, show a phone-shaped placeholder card (28px radius, border, light green inside) containing the highlighted text “[IMAGEM_MOCKUP]”.
P1: “Para boutiques, salões, quem vende comida, revendedoras de cosméticos e perfumes, e lojas de bairro.”
P2: “Em 7 dias, com cerca de 30 minutos por dia no telemóvel que já tens, montas o teu WhatsApp Business como uma montra: perfil completo, catálogo com preços, mensagens automáticas, respostas rápidas e etiquetas.”
P3: “E ficas a saber o que responder, o que publicar no Status e como receber por M-Pesa e e-Mola **sem cair em comprovativos falsos**.”
Primary button, wrapped in an element with id 'hero-cta': “Quero o meu WhatsApp que Vende - 597 MT”
Trust items under the button, 14-15px, each with a primary-green lucide line icon (Wallet, Zap, ShieldCheck, Smartphone), 2x2 grid on mobile, one row on desktop:
“Pagamento com M-Pesa ou e-Mola”
“Acesso logo após a confirmação do pagamento”
“Garantia de 7 dias, de acordo com a política de reembolso da EscalePay”
“Escrito em português de Moçambique, passo a passo, para o telemóvel”
Mobile order: h1, subheadline, mockup, P1-P3, button, trust items. Desktop: two columns (text, button and trust items on the left; mockup on the right).

SECTION 2, id 'problem'
h2: “Isto acontece contigo?”
A white card list of 8 items, each row with a small neutral grey 'x' icon (#8C9A94, not red), 1-2 lines on mobile:
“Os clientes perguntam 'preço?' e desaparecem depois da resposta”
“Passas horas a responder às mesmas perguntas: preço, entrega, onde fica, como pagar”
“Esqueces quem já pagou, quem está à espera da entrega e quem pediu para lembrar”
“Tens medo de comprovativos falsos de M-Pesa ou e-Mola, ou do famoso 'enviei por engano, devolve'”
“Não sabes o que publicar no Status e sentes que estás sempre a repetir o mesmo”
“Pouca gente vê o teu Status porque os clientes nunca guardaram o teu número”
“O cliente compra uma vez e nunca mais volta”
“A tua vida pessoal e o teu negócio estão no mesmo WhatsApp, tudo misturado”
After the list, emphasised line (18px semibold): “Se disseste 'sim' a 3 ou mais, este guia foi feito para ti.”
P1: “Vendes todos os dias pelo WhatsApp. Trabalhas, respondes, entregas.”
P2: “Mas o telemóvel parece um mercado sem bancas: conversas de família misturadas com clientes, perguntas repetidas, pagamentos que não sabes se entraram, Status publicados à pressa.”
P3: “Não é falta de vontade. **É falta de organização.** E isso resolve-se com ferramentas que já existem no teu telemóvel, sem pagares nada por elas.”
Outline button: “Quero organizar o meu WhatsApp”

SECTION 3, id 'story' (no button; narrow column max 640px, 18px text, line-height 1.7)
At the top, a 96px round photo: CREATOR_PHOTO (alt 'Foto de ' + CREATOR_NAME). If empty, show a circle containing the highlighted text “[TUA_FOTO]”. Never use stock or AI photos.
h2: “Porque é que criei este guia”
Subheadline: “[Uma frase verdadeira, por exemplo: 'Cresci a ver a minha família vender pelo WhatsApp.']”
P1: “[Escreve aqui 3 a 5 frases verdadeiras sobre ti e sobre o que te levou a criar isto. Estrutura sugerida: quem és (nome, idade, cidade), a situação real que viste (por exemplo, alguém próximo que vende pelo WhatsApp) e o que te incomodou.]”
P2 (render only if SHOW_INTERVIEW_PARAGRAPHS): “Antes de escrever este guia, conversei com [número real] pessoas que vendem pelo WhatsApp em [bairros ou cidades reais]. Perguntei o que os clientes repetem, o que publicam no Status e se já receberam um comprovativo falso.”
P3 (render only if SHOW_INTERVIEW_PARAGRAPHS): “[Escreve 1 a 2 frases com o que ouviste de verdade, com as palavras delas, sem nomes e com autorização. Exemplo de formato: 'Uma vendedora de salgados disse-me: ...']”
P4: “Percebi uma coisa simples: quase todas já têm clientes. O que falta é um sistema para atender, cobrar e voltar a vender. Foi isso que pus neste guia.”

SECTION 4, id 'solution' (two columns on desktop, stacked on mobile)
h2: “O problema raramente é o WhatsApp. É a forma como está montado.”
Subheadline: “O WhatsApp Business já tem catálogo, mensagens automáticas, respostas rápidas e etiquetas. É grátis. Muita gente nunca o configurou.”
P1: “Quando o cliente não vê o preço, pergunta e vai embora. Quando a resposta demora, compra noutro lado. Quando ninguém faz o seguimento, a venda arrefece. Quando um print falso passa, perdes o produto e o dinheiro.”
P2: “Nenhum destes problemas precisa de publicidade paga nem de equipamento novo. Precisa de um **método**, de textos prontos e de um plano para os próximos 30 dias.”
P3: “O **WhatsApp que Vende** dá-te exactamente isso: um passo-a-passo no teu telemóvel, com tudo escrito para copiares e adaptares ao teu negócio.”
P4: “Não prometemos um número de vendas. Prometemos organização, método e ferramentas prontas a usar a partir de hoje.”
3 items with green check icons:
“Vês a diferença logo no primeiro dia: o teu perfil fica completo e profissional”
“Funciona em Android e iPhone (as capturas de ecrã são de [Android/iPhone], com aviso quando os menus são diferentes)”
“Sem precisar de computador e sem anúncios pagos”
Primary button: “Quero o método completo - 597 MT”
Right column (below the text on mobile): an illustration built with HTML/CSS only (no images, no WhatsApp icons or greens). Two simple phone-profile cards side by side, labelled 'Antes' and 'Depois', with a small tag 'exemplo ilustrativo' above them. The 'Antes' card has a grey avatar circle, grey lines and the items 'Sem descrição', 'Sem catálogo', 'Sem horário'. The 'Depois' card has a green avatar with the initials 'BV', the name 'Bolos da Vila (negócio fictício)', the line 'Bolos por encomenda · Matola · Entregas ao sábado · M-Pesa e e-Mola' and the chips 'Catálogo com preços', 'Horário', 'Mensagem de boas-vindas'. No numbers.

SECTION 5, id 'mechanism'
At the top, the word “MONTRA” very large (64px mobile, 112px desktop, Bricolage Grotesque 800, primary green, letter-spacing 0.08em, aria-hidden) as a visual anchor.
h2: “O Método MONTRA: 6 passos para o teu WhatsApp funcionar como uma loja”
Subheadline: “Cada letra é um módulo e uma acção concreta que fazes no teu telemóvel.”
P1: “A montra é a parte da loja onde o cliente vê os produtos, gosta e decide entrar. O Método MONTRA faz do teu WhatsApp essa montra, passo a passo.”
P2: “Cada passo é visível: no fim de cada dia podes tirar uma captura de ecrã do antes e do depois.”
6 cards (1 column mobile, 2 tablet, 3 desktop). Store each original bullet in full in salesCopy.ts, then display the big letter (48px, primary green), the bold title (the text between the dash and the colon) and the description (the text after the colon):
“**M - Montar o perfil:** logótipo, nome, categoria, descrição, horário e zona de entrega. O cliente sabe quem és antes de perguntar.”
“**O - Oferta no catálogo:** cada produto com foto, preço e descrição curta, para o 'preço?' deixar de ser a única conversa.”
“**N - Novidades no Status:** um calendário de 30 dias com 3 Status por dia (até 5, se tiveres material) e a rotina para os clientes guardarem o teu número.”
“**T - Tratar a conversa:** mensagens de boas-vindas e de ausência, respostas rápidas, script de 5 passos, respostas para objecções e etiquetas.”
“**R - Receber com segurança:** confirmar sempre no teu telemóvel, nunca por print; como lidar com o 'enviei por engano'; nunca partilhar o PIN nem códigos.”
“**A - Acompanhar e fazer recompra:** lista de clientes com consentimento, mensagens pós-venda e listas de transmissão para voltares a vender a quem já confia em ti.”
A 7th full-width card with a ShieldCheck icon instead of a letter and an ochre left border: “**Extra - Protege o teu número:** o que pode levar a restrições, como evitar e como activar a verificação em dois passos.”
Primary button: “Quero aplicar o Método MONTRA”

SECTION 6, id 'whats_inside'
h2: “O que vais aprender, módulo a módulo”
Subheadline: “8 módulos curtos (do 0 ao 7), organizados em 7 dias, com cerca de 30 minutos por dia.”
P1: “Cada módulo termina com uma 'Tarefa de hoje': no máximo 5 acções, cerca de 30 minutos. No Dia 1 fazes os Módulos 0 e 1; do Dia 2 ao Dia 7, um módulo por dia.”
P2: “Onde os menus podem ser diferentes entre Android e iPhone, ou depois de uma actualização, o guia avisa e mostra o caminho mais comum.”
shadcn Accordion (type multiple, all collapsed). The trigger shows the bold title plus the first line of the description (line-clamp-1, muted); expanding shows the full description. Store each original bullet in full; title = bold part, description = the rest:
“**Módulo 0 - Começa Aqui: o teu WhatsApp como loja.** WhatsApp pessoal vs Business, como mudar sem perder conversas (backup primeiro), mesmo número ou número novo, e diagnóstico do teu negócio em 10 perguntas.”
“**Módulo 1 - M de Montar: um perfil que inspira confiança.** Foto ou logótipo, a fórmula da descrição ('o que vendes + para quem + onde entregas + como pagar') e 15 descrições prontas por tipo de negócio.”
“**Módulo 2 - O de Oferta: o catálogo que responde 'preço?' por ti.** Fotografar com o telemóvel, descrever um produto em 4 linhas, organizar colecções e partilhar o link do catálogo.”
“**Módulo 3 - N de Novidades: vender todos os dias com o Status.** Quem vê o teu Status, a regra 3-5, os 5 tipos de Status e como usar o calendário de 30 dias sem ficar repetitivo.”
“**Módulo 4 - T de Tratar: responder rápido e fechar a venda na conversa.** Boas-vindas e ausência, respostas rápidas (/preco, /entrega, /pagamento...), script de 5 passos, objecções e etiquetas.”
“**Módulo 5 - R de Receber: M-Pesa e e-Mola sem burlas.** A regra de ouro, sinais de comprovativo falso, o golpe 'enviei por engano', sinal ou pagamento na entrega, e um registo simples de vendas.”
“**Módulo 6 - A de Acompanhar: lista de clientes e recompra.** Lista de clientes com consentimento, listas de transmissão, mensagens pós-venda, pedir avaliações reais e datas comerciais de Moçambique.”
“**Módulo 7 - Protege o teu número.** Regras de ouro para grupos e listas, verificação em dois passos e golpes de falso 'suporte do WhatsApp'.”
Under the accordion, a wrapping row of format chips (white, rounded, border): “Guia PDF 45-60 páginas”, “40+ scripts”, “25 respostas rápidas”, “Calendário de 30 dias”, “60 legendas”, “14 modelos Canva”, “Google Sheets”.
If PDF_PAGE_IMAGES is not empty, show a horizontally scrollable row of those page thumbnails (lazy-loaded); otherwise show nothing.
Primary button: “Quero os 8 módulos - 597 MT”

SECTION 7, id 'bonuses' (background band #E7F2EC)
h2: “E ainda recebes 4 bónus práticos”
Subheadline: “Ferramentas para usares no primeiro dia, não apenas para leres.”
4 white cards (1 column mobile, 2 desktop), each with a thumbnail from BONUS_IMAGES[i]. If empty, use a light-green square with a lucide icon (Table, ClipboardCheck, RefreshCw, Camera). Bold title = bold part; description = the rest:
“**Bónus 1 - Folha de Controlo de Encomendas e Clientes (Google Sheets):** separadores para encomendas, pagamentos confirmados, entregas e lista de clientes. Abres, fazes uma cópia e começas.”
“**Bónus 2 - Checklist Anti-Burla M-Pesa/e-Mola:** uma página para imprimir e colar perto do balcão. Confirmar no teu telemóvel, nunca entregar com base num print, nunca partilhar o PIN nem códigos.”
“**Bónus 3 - 20 Mensagens para Reactivar Clientes Antigos:** textos respeitosos para quem não compra há 30, 60 ou 90 dias, com uma linha para a pessoa sair da lista se quiser.”
“**Bónus 4 - Mini-Guia de Fotos de Produto com o Telemóvel:** luz da janela, fundos simples (capulana, cartolina, lençol), 3 ângulos e o mesmo enquadramento para todo o catálogo.”
Below the cards: “Os bónus estão incluídos no preço. Sem custos extra.”
No 'valor: X MT' tags on bonuses.
Primary button: “Quero o guia com os 4 bónus”

SECTION 8, id 'how_it_works'
h2: “Como funciona: 3 passos simples”
Subheadline: “Não precisas de cartão bancário. Pagas com o M-Pesa ou o e-Mola que já usas.”
3 steps: a vertical timeline on mobile (green circles with an icon, connected by a thin ochre line) and 3 columns on desktop. Icons: Pointer, Inbox, ListChecks. Texts:
“**1. Compra:** clica em 'Comprar', escolhe M-Pesa ou e-Mola e confirma o pagamento no teu telemóvel.”. Under it, only if SHOW_STEP1_NOTE, a tiny muted note: “Vais receber um pedido de confirmação no teu telemóvel”
“**2. Recebe o acesso:** recebes o acesso por email ou na área de membros. Abre primeiro o ficheiro 'Começa Aqui'.”
“**3. Aplica em 7 dias:** no Dia 1 fazes os Módulos 0 e 1; do Dia 2 ao Dia 7, um módulo por dia, cerca de 30 minutos. E vês o teu WhatsApp mudar.”
P1: “O pagamento é feito no checkout da EscalePay, uma plataforma de pagamentos para produtos digitais em Moçambique.”
P2: “Se tiveres alguma dificuldade, escreve-me pelo WhatsApp [TEU_WHATSAPP] e ajudo-te passo a passo. Nunca te vou pedir o PIN nem códigos.” (make the filled number a link to waLink('Olá, tenho uma dúvida sobre o WhatsApp que Vende'), new tab)
Primary button: “Começar agora - 597 MT”

SECTIONS 9 and 10 sit side by side on desktop (two columns, two separate <section> elements) and stack on mobile.
SECTION 9, id 'for_who'
h2: “Para quem é o WhatsApp que Vende”
Subheadline: “Para quem já vende alguma coisa real e quer vender de forma mais organizada.”
6 items with green check icons:
“Boutiques e revendedoras de roupa, calçado e acessórios”
“Salões, cabeleireiras, manicures e trancistas”
“Quem vende comida: bolos, refeições, salgados, frescos e encomendas”
“Revendedoras de cosméticos e perfumes”
“Lojas de bairro, mercearias e venda de acessórios de telemóvel”
“Qualquer pessoa que já recebe clientes pelo WhatsApp e quer menos confusão”
P1: “Não importa se vendes em Maputo, Matola, Beira, Nampula, Quelimane ou noutro sítio. Se os teus clientes falam contigo pelo WhatsApp, isto é para ti.”
Primary button: “Isto é para mim”
SECTION 10, id 'not_for_who' (calm tone, no button)
h2: “Para quem NÃO é”
Subheadline: “Prefiro ser honesto agora do que ter um cliente desiludido depois.”
P1: “Este guia ensina a organizar e a vender melhor um negócio que já existe. Não é um esquema para 'ganhar dinheiro online', nem um investimento, nem tarefas pagas.”
4 items with neutral grey 'x' icons:
“Quem procura ficar rico depressa”
“Quem quer enviar mensagens em massa a desconhecidos ou comprar listas de contactos”
“Quem espera vendas garantidas sem ter um produto ou serviço para vender”
“Quem não está disposto a dedicar cerca de 30 minutos por dia durante uma semana”

SECTION 11, id 'offer_stack'
h2: “Tudo o que recebes hoje”
Subheadline: “Pagamento único. Sem mensalidades.”
Centred price card (white, max width 560px, 1.5px primary border, 4px ochre top bar, 16px radius) containing in this order:
(a) 11 items with green check icons:
“Guia completo WhatsApp que Vende (45-60 páginas, legível no telemóvel)”
“Método MONTRA em 8 módulos (0 a 7) com tarefas diárias”
“40+ scripts de conversa e 25 respostas rápidas com atalhos”
“Respostas prontas para 'está caro', 'vou pensar', 'faz desconto?' e mais”
“Calendário de Status de 30 dias + 60 legendas por tipo de negócio”
“14 modelos Canva: 10 Status, 3 cartões de produto e 1 logótipo”
“Bónus 1 - Folha de Controlo de Encomendas e Clientes (Google Sheets)”
“Bónus 2 - Checklist Anti-Burla M-Pesa/e-Mola para imprimir”
“Bónus 3 - 20 Mensagens para Reactivar Clientes Antigos”
“Bónus 4 - Mini-Guia de Fotos de Produto com o Telemóvel”
“Garantia de 7 dias, de acordo com a política de reembolso da EscalePay”
(b) the price “597 MT” very large (56px mobile, 64px desktop, Bricolage Grotesque 800, ink) with the line “Pagamento único. M-Pesa ou e-Mola.” below it. No crossed-out price.
(c) P1: “Tudo isto por **597 MT**, pagamento único com M-Pesa ou e-Mola. Se pensares só no primeiro mês de uso, dá cerca de 20 MT por dia, e o material fica contigo para usares sempre que precisares.”
(d) Primary button: “Quero o meu WhatsApp que Vende - 597 MT”
(e) Store this original text: “**Como pagar:** 1) Clica em 'Comprar'. 2) Escolhe M-Pesa ou e-Mola. 3) Confirma no teu telemóvel. 4) Recebes o acesso.”. Display it as the small bold label “Como pagar:” followed by a small numbered list: “Clica em 'Comprar'.” / “Escolhe M-Pesa ou e-Mola.” / “Confirma no teu telemóvel.” / “Recebes o acesso.”. M-Pesa and e-Mola appear as text only, never operator logos.
(f) Small note box with tint background: “No checkout podes, se quiseres, adicionar o **Pack Datas Especiais** por 147 MT: 60 ideias de Status com legendas e 5 modelos Canva para Black Friday, Natal, Fim do Ano e outras datas. É opcional.”

SECTION 12, id 'guarantee' (centred, calm white background)
A simple seal: a 112px circle with an ochre ring, a ShieldCheck icon and the text “7 dias” inside (no 'certificado' badge).
h2: “Garantia de 7 dias”
Subheadline: “Se não for para ti, pedes o reembolso.”
P1: “Tens 7 dias para ver o guia, testar os scripts e começar a configurar o teu WhatsApp.”
P2: “Se achares que não é para ti, pedes o reembolso dentro de 7 dias pela plataforma de pagamento, de acordo com a política de reembolso da EscalePay. Da minha parte, sem discussões.” Make the words “política de reembolso” in this paragraph a link to ESCALEPAY_REFUND_POLICY_URL (new tab).
P3: “Se tiveres dúvidas antes de pedir, fala comigo. Muitas vezes é só um passo que ficou difícil e resolve-se depressa.”
3 check items: “7 dias a contar da compra” / “Pedido feito pela plataforma de pagamento (EscalePay)” / “Da minha parte, sem discussões nem perguntas difíceis”
Primary button: “Experimentar com garantia - 597 MT”

SECTION 13, id 'about_creator' (no button)
120px round photo from CREATOR_PHOTO (or a circle with the highlighted text “[TUA_FOTO]”).
h2: “Quem está por trás do WhatsApp que Vende”
Subheadline: “[TEU_NOME], [cidade real]”
P1: “[Escreve 3 linhas verdadeiras sobre ti. Estrutura sugerida: o que fazes, que competências tens (por exemplo: tecnologia, português e inglês) e porque te interessas por pequenos negócios. Não exageres nem inventes resultados.]”
P2: “O meu compromisso contigo é simples: conteúdo prático, em português de Moçambique, sem promessas de dinheiro fácil, e contacto directo se precisares de ajuda.”
P3: “Podes falar comigo pelo WhatsApp [TEU_WHATSAPP] ou pelo email [TEU_EMAIL].”
3 small check items: “Nome real e contacto real” / “Respondo pessoalmente às mensagens de suporte” / “[Opcional: 1 facto verdadeiro e verificável, por exemplo uma formação ou experiência real; apaga esta linha se não tiveres]”
Under that, text links for each non-empty entry in SOCIAL_LINKS (TikTok, Instagram, Facebook), new tab; render nothing for empty ones.

SECTION 14, id 'testimonials': render ONLY if SHOW_TESTIMONIALS is true AND the array in src/content/testimonials.ts is not empty. Create that file with an EMPTY array of type { quote: string; author: string; business: string; city: string; gifted?: boolean; image?: string }. Do NOT create any sample testimonials.
h2: “O que dizem as primeiras pessoas que usaram o guia”
Subheadline: “Depoimentos reais, partilhados com autorização. Os resultados variam de pessoa para pessoa.”
Quote cards show the quote, then 'author - business - city'; if gifted is true, add the line “Recebeu o guia gratuitamente para dar uma opinião sincera.”. If image is set, show it as a screenshot card.
Primary button: “Quero experimentar também”

SECTION 15, id 'faq'
h2: “Perguntas frequentes”
Subheadline: “As dúvidas mais comuns antes de comprar. Se a tua não estiver aqui, escreve-me.”
Small line: “Respondo com honestidade, mesmo quando a resposta é 'não'.”
shadcn Accordion (type single, collapsible, FIRST item open by default), with these 15 items (question → answer):
“Vou perder as minhas conversas se mudar para o WhatsApp Business?” → “Não precisas de perder. O Módulo 0 mostra como fazer o backup primeiro e depois passar o mesmo número para o WhatsApp Business. Faz sempre o backup antes de mudar. Se preferires, também explico as vantagens de usar um número só para o negócio.”
“Preciso de outro telemóvel ou de outro número?” → “Não. Podes usar o telemóvel que já tens. O guia explica os prós e contras de usar o mesmo número ou um número separado, para decidires o que é melhor para ti.”
“Funciona no iPhone?” → “Sim. O WhatsApp Business existe para Android e iPhone. As capturas de ecrã do guia são de [Android/iPhone]; quando os menus aparecem noutro sítio, o guia avisa. Os menus também podem mudar com as actualizações; mostro o caminho mais comum.”
“Quanto tempo preciso por dia?” → “Cerca de 30 minutos por dia, durante 7 dias. O catálogo pode levar um pouco mais se tiveres muitos produtos. Podes fazer ao teu ritmo: o material fica contigo.”
“Preciso de computador?” → “Não. Tudo funciona no telemóvel: o guia em PDF, os scripts, o Canva e o Google Sheets. Se tiveres computador, também podes usar.”
“Não tenho cartão bancário. Como pago?” → “Pagas com M-Pesa ou e-Mola no checkout da EscalePay. Clicas em 'Comprar', escolhes a carteira, confirmas no teu telemóvel e recebes o acesso. Se precisares de ajuda, escreve-me pelo WhatsApp.”
“Como recebo o produto?” → “Depois de o pagamento ser confirmado, recebes o acesso por email ou na área de membros. Começa pelo ficheiro 'Começa Aqui', que tem todos os links (guia, scripts, calendário, Canva e Google Sheets). Os ficheiros abrem no telemóvel.”
“Funciona se eu vender serviços, como cabelo, unhas ou tranças?” → “Sim. Há exemplos para salões e serviços: descrição do perfil, catálogo de serviços com preços, respostas rápidas para marcações e mensagens para clientes que voltam.”
“Não percebo muito de tecnologia. Vou conseguir?” → “O guia foi escrito para o telemóvel, com passos curtos e capturas de ecrã. Cada dia tem no máximo 5 tarefas. Se mesmo assim preferires que alguém faça por ti, existe um serviço opcional de configuração.”
“E se eu não souber usar o Canva?” → “O Canva tem versão gratuita e funciona no telemóvel. Os modelos já estão feitos: só trocas o texto, as cores e a foto. Se não quiseres usar o Canva, o guia e os scripts funcionam na mesma.”
“O que é o Pack Datas Especiais?” → “É um extra opcional de 147 MT que podes adicionar no checkout: 60 ideias de Status com legendas (10 por data) e 5 modelos Canva para Black Friday, Natal, Fim do Ano, Dia da Mulher Moçambicana, Dia das Mães e fim do mês. O guia funciona sem ele.”
“E se o WhatsApp mudar os menus?” → “Acontece. O guia indica o caminho mais comum e, quando houver mudanças importantes, actualizo o material sempre que possível. Se não encontrares uma opção, escreve-me.”
“Garantem que vou vender mais?” → “Não. Ninguém pode garantir vendas com honestidade. Ensino a organizar o teu WhatsApp e a atender, cobrar e acompanhar melhor. Os resultados dependem do teu produto, dos teus preços, da tua zona e do teu esforço.”
“Isto é burla? Como sei que é sério?” → “Tens o meu nome, o meu contacto real, e o pagamento é feito no checkout da EscalePay, com garantia de 7 dias de acordo com a política da plataforma. Não prometo dinheiro fácil e nunca peço códigos nem PIN. Antes de comprar, podes escrever-me e fazer todas as perguntas.”
“Posso pedir que configurem o WhatsApp por mim?” → “Sim, como serviço opcional (1.497 MT): preenches um formulário, eu escrevo tudo para o teu negócio e fazemos uma chamada em que colas os textos comigo. Nunca peço códigos nem acesso à tua conta. As vagas são limitadas a 5 por semana porque faço cada configuração pessoalmente.”
Below the accordion, an outline button (NOT a checkout: href waLink('Olá, tenho uma dúvida sobre o WhatsApp que Vende'), new tab, ctaId 'faq_whatsapp'): “Tenho outra dúvida - falar no WhatsApp”

SECTION 16, id 'final_cta' (full-width solid #0F7B5F band, white text)
h2: “O teu próximo cliente vai perguntar 'preço?'. Que resposta vai encontrar?”
Subheadline: “Transforma o teu WhatsApp numa loja organizada que atende, cobra e traz o cliente de volta.”
P1: “Podes continuar a responder a tudo à mão, a publicar Status ao acaso e a confiar em prints.”
P2: “Ou podes dedicar cerca de 30 minutos por dia, durante 7 dias, e ficar com um WhatsApp montado como uma loja, com textos prontos e um plano para o próximo mês.”
P3: “**597 MT. M-Pesa ou e-Mola. Garantia de 7 dias.**”
The mockup image again (MOCKUP_IMAGE, lazy-loaded, same placeholder fallback).
CtaButton variant 'white' (white background, green text): “Quero o meu WhatsApp que Vende - 597 MT”

FOOTER: keep the global Footer from step 1. Verify that its texts are exactly: “WhatsApp que Vende” / “Guia prático para pequenos negócios que vendem pelo WhatsApp em Moçambique.” / “Contacto: WhatsApp [TEU_WHATSAPP] | Email [TEU_EMAIL]” / “Responsável: [TEU_NOME ou nome do negócio registado], [cidade], Moçambique.” / “Este produto não é afiliado, patrocinado nem aprovado pela Meta ou pelo WhatsApp. WhatsApp é uma marca registada da Meta Platforms, Inc.” / “Pagamentos processados pela EscalePay. Reembolsos dentro de 7 dias, de acordo com a política da plataforma.” / “Os resultados variam. Não garantimos vendas, rendimentos, lucros nem empregos.”, with links “Política de privacidade”, “Termos e condições”, “Política de reembolso”.

Make sure the StickyMobileCTA uses #hero-cta and #final_cta as described in step 1. When finished, reply only with a list of every button on the page (section id, label, href).
```

Check after:
- [ ] All 16 blocks appear in this order: hero, problem, story, solution, mechanism, whats_inside, bonuses, how_it_works, for_who + not_for_who, offer_stack, guarantee, about_creator, (testimonials hidden), faq, final_cta, footer
- [ ] Spot-check 5 texts against the copy (hero headline, one pain item, one module, one FAQ answer, final CTA). Accents and spelling such as 'exactamente' and 'objecções' are unchanged
- [ ] No literal ** anywhere; bold appears only where the copy has it (for example 'É falta de organização.', 'método', 'WhatsApp que Vende')
- [ ] Placeholders are highlighted yellow: story texts, [TUA_FOTO], [IMAGEM_MOCKUP], [Android/iPhone], about-creator text, [número real]
- [ ] Testimonials section is NOT visible
- [ ] Every buy button opens the placeholder ESCALEPAY_CHECKOUT_URL in the same tab (it will show an error page for now, which is expected); the FAQ WhatsApp button opens wa.me in a new tab
- [ ] Mobile: hero headline is 3 lines or fewer at 360px; the sticky '597 MT · Comprar' bar appears after scrolling past the hero button and disappears on the green final band; the Dúvidas? pill sits above the bar
- [ ] Modules accordion starts closed, FAQ starts with the first question open, MONTRA cards are 1 column on mobile
- [ ] No countdowns, star ratings, crossed-out prices, WhatsApp logo or bright WhatsApp green anywhere

## Step 3 · Thank-you page (/obrigado)

Goal: Tell buyers exactly where to find their access and what to do on day 1, offer help by WhatsApp, and softly show the optional services.

```text
Build the thank-you page at the route '/obrigado' (replace the placeholder). Reuse the existing Layout, Header, Footer, HelpFloat, RichText, fillPlaceholders, waLink, CtaButton and constants from src/config/site.ts (background #FAF7F0, cards #FFFFFF, headings #13261F, primary #0F7B5F, tint #E7F2EC, ochre #D9952B decorative). No sticky buy bar on this page. Set the document title to 'Obrigado - WhatsApp que Vende' and add <meta name='robots' content='noindex'> for this route.

COPY RULES: Every text between “ ” is final copy. Store it in src/content/thankYouCopy.ts exactly, character for character, and render it with RichText (**bold** without asterisks, blank lines = paragraphs, [TEU_WHATSAPP] filled from config, other [brackets] highlighted). Do not add, remove or rewrite any words, and do not include the “ ” marks.

LAYOUT (single centred column, max width 640px, mobile first):
1. A large lucide CircleCheck icon (56px, primary green), then the h1: “Obrigado! O teu WhatsApp que Vende já é teu.”
2. Paragraphs:
P1: “Obrigado pela tua compra. Verifica o teu email ou a área de membros da EscalePay: é lá que encontras o acesso.”
P2: “Começa pelo ficheiro **Começa Aqui**. Lá encontras todos os links: guia, scripts, calendário de Status, modelos Canva e folhas Google Sheets.”
P3: “Não encontras o email? Vê também a pasta Spam ou Promoções. Se continuar sem aparecer, escreve-me pelo WhatsApp [TEU_WHATSAPP] com o teu nome e o número com que pagaste, e envio-te o acesso.”
3. An outline button (not a checkout: no checkout tracking, new tab) with the label “Falar comigo no WhatsApp”, linking to waLink('Olá! Comprei o WhatsApp que Vende e preciso de ajuda com o acesso.').
4. A white card with the h2 “Próximos passos” and a numbered list (numbers in green circles):
1. “Abre o email ou a área de membros e descarrega o ficheiro 'Começa Aqui'.”
2. “Faz o backup do teu WhatsApp antes de qualquer mudança (Módulo 0).”
3. “Hoje (Dia 1): faz o diagnóstico de 10 perguntas e as tarefas dos Módulos 0 e 1 (cerca de 30 minutos).”
4. “Guarda o meu número [TEU_WHATSAPP] para receberes ajuda e actualizações do guia.”
5. “Daqui a 3 dias vou perguntar-te se já configuraste o perfil. Responde com sinceridade, quero ajudar.”
5. Below it, two optional offer cards (background #E7F2EC, 4px ochre top bar, 16px radius):
Card A text: “Não tens tempo ou preferes que alguém faça por ti? **Configuro o teu WhatsApp Business por ti - 1.497 MT.** Preenches um formulário de 10 minutos, eu escrevo o perfil, as descrições de até 15 produtos, as mensagens automáticas, 10 respostas rápidas, 5 etiquetas e um plano de Status de 7 dias, e depois colas tudo comigo numa chamada de 30 a 45 minutos. Nunca peço códigos nem acesso à tua conta. Vagas limitadas a 5 por semana porque faço cada configuração pessoalmente.” Then an internal React Router link styled like a small primary button, label “Ver o serviço”, going to '/oferta-especial'.
Card B (render ONLY if REVISAO_EXPRESS_URL is not empty) text: “Preferes fazer por conta própria, mas com uma segunda opinião? **Revisão Express do teu WhatsApp Business - 497 MT.**” Then a CtaButton variant outline, size sm, label “Ver a revisão”, href REVISAO_EXPRESS_URL, same tab, ctaId 'thankyou_revisao'.
Do not fire any 'Purchase' tracking event on this page (anyone can open this URL). Do not add confetti, countdowns or extra texts.
```

Check after:
- [ ] /obrigado shows the green check icon, the headline and the 3 paragraphs word for word, with 'Começa Aqui' in bold
- [ ] 'Falar comigo no WhatsApp' opens wa.me with your number and the prefilled access-help message
- [ ] The 5 next steps are numbered and readable on mobile; [TEU_WHATSAPP] is highlighted until you set your number
- [ ] 'Ver o serviço' goes to /oferta-especial; the Revisão Express card is hidden while REVISAO_EXPRESS_URL is empty
- [ ] No sticky buy bar on this page; the Dúvidas? pill and footer are visible

## Step 4 · Upsell page (/oferta-especial)

Goal: Offer the 1.497 MT done-with-you setup right after purchase, with a clear YES to the upsell checkout and an always-visible NO to /obrigado.

```text
Build the upsell page at the route '/oferta-especial' (replace the placeholder). Buyers arrive here right after paying for the guide. Reuse the Layout (on this route the Header shows only the wordmark without link or button, and HelpFloat and StickyMobileCTA must NOT appear), Footer, RichText, CtaButton, formatMT and constants from src/config/site.ts (background #FAF7F0, cards #FFFFFF, headings #13261F, primary #0F7B5F, tint #E7F2EC, ochre #D9952B decorative). Document title 'Oferta especial - WhatsApp que Vende'; add <meta name='robots' content='noindex, nofollow'>.

COPY RULES: Every text between “ ” is final copy. Store it in src/content/upsellCopy.ts exactly, character for character, and render it with RichText (**bold** without asterisks, blank lines = paragraphs). Do not add, remove or rewrite any words, and do not include the “ ” marks.

Create an UpsellDecision component, used twice (near the top and at the end), centred, max width 520px:
- price “1.497 MT” (Bricolage Grotesque 800, 40px, ink)
- YES: a large primary CtaButton, label “Sim, quero que configures o meu WhatsApp Business - 1.497 MT”, href ESCALEPAY_UPSELL_URL, same tab, ctaId 'upsell_yes' (top) or 'upsell_yes_bottom' (end). The label may wrap to 2-3 centred lines; min height 60px.
- NO: 16px below, a plain underlined text link (muted #5E6E68, 15px, padding so the tap area is at least 44px high), label “Não, obrigado. Prefiro configurar por conta própria com o guia.”, linking to the internal route '/obrigado'. It must always be visible and readable, never hidden or disguised.

LAYOUT (centred column, max width 680px):
1. h1: “Antes de começares: queres que eu configure o teu WhatsApp Business por ti?”
2. Subheadline: “Serviço opcional para quem já tem o guia. Tu ficas com o resultado; eu faço o trabalho de escrita.”
3. UpsellDecision (top).
4. Paragraphs:
P1: “Já tens o guia e podes fazer tudo por conta própria. Mas se o tempo é curto ou preferes não errar, posso fazer a parte mais demorada por ti.”
P2: “**Como funciona:** preenches um formulário de 10 minutos sobre o teu negócio. Eu escrevo tudo, adaptado aos teus produtos e ao teu tom. Depois fazemos uma chamada de 30 a 45 minutos em que colas os textos no teu telemóvel, comigo a guiar.”
P3: “**Segurança:** nunca te peço códigos de verificação, PIN, códigos M-Pesa/e-Mola nem acesso à tua conta. És tu que fazes as alterações no teu telemóvel.”
P4: “**Entrega dos textos em até 72 horas** depois de receber o formulário completo.”
P5: “As vagas são limitadas a 5 por semana, porque faço cada configuração pessoalmente. Se a semana estiver cheia, aviso-te logo e combinamos a data seguinte; se essa data não te servir, podes pedir o reembolso dentro dos 7 dias.”
5. A white card (1.5px primary border, 4px ochre top bar) with the h2 “O que está incluído” and a list with green check icons:
“Descrição do perfil escrita para o teu negócio (3 opções à escolha)”
“Sugestão de categoria e organização do catálogo em colecções”
“Descrições de até 15 produtos do catálogo (4 linhas cada)”
“Mensagem de boas-vindas e mensagem de ausência”
“10 respostas rápidas com atalhos”
“5 etiquetas com regras de uso”
“Plano de Status de 7 dias com legendas para os teus produtos”
“Chamada guiada de 30 a 45 minutos para colares tudo comigo”
“Checklist do que tens de fazer tu: fotos e verificação em dois passos”
6. P6: “Preço do serviço: **1.497 MT**, pagamento com M-Pesa ou e-Mola. Garantia de 7 dias, de acordo com a política de reembolso da EscalePay.” Make the words “política de reembolso” a link to ESCALEPAY_REFUND_POLICY_URL (new tab).
P7: “Se preferires fazer tu, carrega em 'Não, obrigado' e mostro-te uma opção mais simples: a Revisão Express.”
7. UpsellDecision (end).

FORBIDDEN: countdown timers, 'only X spots left' counters, exit-intent pop-ups, automatic redirects, pre-ticked options, crossed-out prices, invented testimonials, WhatsApp logo or WhatsApp greens.
```

Check after:
- [ ] /oferta-especial shows only the wordmark in the header: no 'Comprar' button, no Dúvidas? pill, no sticky bar
- [ ] The YES button appears twice, wraps nicely on a 360px screen and opens the placeholder ESCALEPAY_UPSELL_URL in the same tab
- [ ] The NO link is clearly visible under each YES button and goes to /obrigado
- [ ] All 7 paragraphs and the 9 'O que está incluído' items match the copy word for word, with 'Como funciona:', 'Segurança:' and 'Entrega dos textos em até 72 horas' in bold
- [ ] No countdown, no scarcity counter, no pop-up

## Step 5 · Affiliate page (/afiliados)

Goal: Recruit approved affiliates honestly: 40% commission, the kit, strict rules, and an apply button that reaches the creator.

```text
Build the affiliate page at the route '/afiliados' (replace the placeholder). Reuse the Layout (normal Header, Footer and HelpFloat; no sticky bar), RichText, CtaButton, waLink and constants from src/config/site.ts (background #FAF7F0, cards #FFFFFF, headings #13261F, primary #0F7B5F, tint #E7F2EC, ochre #D9952B decorative, neutral icon #8C9A94). Document title 'Programa de afiliados - WhatsApp que Vende'.

COPY RULES: Every text between “ ” is final copy. Store it in src/content/affiliateCopy.ts exactly, character for character, and render it with RichText (**bold** without asterisks). Do not add, remove or rewrite any words, and do not include the “ ” marks. The only new UI labels allowed are the group headings given below.

LAYOUT (centred column max width 720px, mobile first):
1. h1 (28px mobile, 44px desktop): “Conheces quem vende pelo WhatsApp? Recomenda o WhatsApp que Vende e recebe 40% de comissão.”
2. P1: “O WhatsApp que Vende é um guia prático para pequenos negócios em Moçambique organizarem o WhatsApp Business: perfil, catálogo, respostas rápidas, Status e pagamentos seguros por M-Pesa e e-Mola.”
P2: “Se tens contacto com vendedoras, donas de salão, associações de vendedores, grupos de empreendedoras ou páginas de pequenos negócios, podes recomendar o guia com o teu link de afiliado na EscalePay.”
3. Highlight card (white, 1.5px primary border, 4px ochre top bar): “40%” very large (Bricolage Grotesque 800, primary green) and below it “cerca de 239 MT por venda”.
4. P3: “**Comissão:** 40% em cada venda do guia (597 MT), cerca de 239 MT por venda. O valor exacto e os pagamentos aparecem no teu painel da EscalePay, de acordo com as regras e taxas da plataforma.”
P4: “**Aprovação um a um:** analiso cada pedido para proteger a marca e os clientes. Quem faz spam ou promete dinheiro é removido.”
5. h2 'O que recebes', a list with green check icons:
“Kit de afiliado: PDF de boas-vindas, 7 imagens de Status (1080x1920), 5 legendas prontas e 3 textos para mensagens privadas”
“3 guiões de vídeo curtos (20-40 segundos) para gravares com o telemóvel”
“Modelo de publicação para grupos de Facebook que permitem promoção”
“Ficha de perguntas frequentes para responder a quem tem dúvidas”
“Imagens de mockup do produto e link da página de vendas”
6. h2 'Regras para afiliados', a white card list. The leading label of each item (up to and including the colon) is bold. Icons: green check for 'Podes dizer', grey x for the three 'Proibido' items, lucide Info for 'Obrigatório':
“Podes dizer: 'guia prático', 'scripts prontos', 'calendário de 30 dias', 'pagamento com M-Pesa/e-Mola', 'garantia de 7 dias'”
“Proibido dizer: 'vendas garantidas', 'vais ganhar X MT', 'renda extra garantida', 'o produto número 1'; proibido usar depoimentos falsos, urgência falsa ou o logótipo do WhatsApp/Meta”
“Proibido: mensagens em massa a desconhecidos, adicionar pessoas a grupos sem pedir, publicar em grupos que não permitem promoção”
“Obrigatório: dizer que é um link de afiliado (por exemplo: 'link de afiliado, recebo uma comissão se comprares')”
7. A small tint card with a lucide Award icon: “Reconhecimento mensal ao afiliado com mais vendas reais no painel”
8. P5: “Não prometo quanto vais ganhar. Depende de quem conheces, de onde partilhas e de como explicas o produto.”
9. Primary CtaButton, label “Quero ser afiliado - pedir aprovação”, ctaId 'affiliate_apply', opening in a new tab. href = AFFILIATE_APPLY_URL if not empty, otherwise waLink('Olá! Quero pedir aprovação como afiliado do WhatsApp que Vende. Nome: ... | Onde vou partilhar: ...'). This is not a product checkout, so do not send InitiateCheckout for it.
10. Under the button, a small text link 'Ver a página de vendas' to '/'.
FORBIDDEN: income claims, earnings calculators, 'top affiliate earned X' numbers, countdowns, WhatsApp logo or greens.
```

Check after:
- [ ] /afiliados headline, 5 paragraphs and all 10 list items match the copy word for word
- [ ] The '40%' card shows 'cerca de 239 MT por venda' and nothing more (no earnings calculator)
- [ ] In the rules list, the labels 'Podes dizer:', 'Proibido dizer:', 'Proibido:', 'Obrigatório:' are bold, with calm grey x icons for the prohibitions
- [ ] 'Quero ser afiliado - pedir aprovação' opens WhatsApp with the prefilled application message (or your form, if you set AFFILIATE_APPLY_URL)
- [ ] Check that the 40% commission really is what you configured in EscalePay before publishing

## Step 6 · Legal pages (/privacidade and /termos)

Goal: Publish simple, honest Portuguese privacy policy and terms, including every reviewed disclaimer word for word.

```text
Build two simple legal pages: '/privacidade' and '/termos' (replace the placeholders). Reuse the Layout (Header, Footer, HelpFloat; no sticky bar), RichText (fills [TEU_NOME], [cidade], [TEU_EMAIL], [TEU_WHATSAPP] from src/config/site.ts) and the colour tokens. Readable article layout: max width 720px, h1, then h2 per section (20-22px), paragraphs 17px, line-height 1.7, lists with small dots, generous spacing. At the top of each page, under the h1, show 'Última actualização: ' + LEGAL_LAST_UPDATED. At the bottom, links to the other legal page and to '/'. Titles: 'Política de Privacidade - WhatsApp que Vende' and 'Termos e Condições - WhatsApp que Vende'.
COPY RULES: Store all texts in src/content/legalCopy.ts exactly as written below (character for character) and render them with RichText. Do not add legal clauses, change words or translate. Do not include the “ ” marks.

PAGE /privacidade
h1: “Política de Privacidade”
Intro: “Esta política explica, de forma simples, que dados recolhemos quando visitas este site ou compras o WhatsApp que Vende, para que os usamos e o que podes pedir.”
h2 “1. Quem é o responsável” → “O responsável pelos teus dados é [TEU_NOME], [cidade], Moçambique. Contacto: WhatsApp [TEU_WHATSAPP] | Email [TEU_EMAIL].”
h2 “2. Que dados recolhemos” → list:
“**Dados da compra:** o pagamento é processado pela EscalePay. Para entregar o produto, recebemos da plataforma dados como o nome, o email e o número de telefone usados no checkout. Não temos acesso ao teu PIN nem aos códigos da tua conta M-Pesa ou e-Mola.”
“**Mensagens de suporte:** se nos escreves pelo WhatsApp ou por email, guardamos a conversa para te podermos ajudar.”
“**Serviços opcionais:** se contratares a configuração do WhatsApp Business ou a Revisão Express, guardamos as respostas do formulário e as capturas de ecrã que enviares, apenas para fazer o serviço.”
“**Dados de navegação:** se estiverem activas ferramentas de medição (por exemplo, Meta Pixel ou TikTok Pixel), podem ser recolhidos dados técnicos como as páginas visitadas, o tipo de dispositivo e os cliques nos botões, através de cookies ou tecnologias semelhantes.”
h2 “3. Para que usamos os dados” → list: “Entregar o produto e dar acesso aos ficheiros.” / “Responder às tuas mensagens e dar suporte.” / “Enviar informações sobre a tua compra e actualizações do guia.” / “Pedir a tua opinião. Só publicamos um depoimento com a tua autorização escrita.” / “Medir o funcionamento da página e dos anúncios, quando as ferramentas de medição estiverem activas.” / “Cumprir obrigações legais.”
h2 “4. Com quem partilhamos” → “Não vendemos, não alugamos e não partilhamos os teus dados para fins comerciais de terceiros. Os dados só são tratados pela EscalePay, que processa os pagamentos e o acesso ao produto; pela Meta e pelo TikTok, apenas se as ferramentas de medição estiverem activas; e por autoridades, quando a lei o exigir.”
h2 “5. Durante quanto tempo guardamos” → “Guardamos os dados apenas enquanto forem necessários para entregar o produto, dar suporte e cumprir obrigações legais. Depois disso, apagamo-los.”
h2 “6. Os teus direitos” → “Podes pedir, a qualquer momento, para ver, corrigir ou apagar os teus dados, e deixar de receber as nossas mensagens. Basta escrever para [TEU_EMAIL] ou pelo WhatsApp [TEU_WHATSAPP]. Respondemos o mais depressa possível.”
h2 “7. Segurança” → “Nunca te pediremos o PIN, códigos M-Pesa/e-Mola, códigos de verificação do WhatsApp nem acesso à tua conta. Se alguém te pedir isto em nosso nome, não envies nada e avisa-nos.”
h2 “8. Alterações” → “Podemos actualizar esta política. A data da última actualização aparece no topo desta página.”

PAGE /termos
h1: “Termos e Condições”
Intro: “Ao comprares o WhatsApp que Vende ou um serviço opcional, aceitas estes termos. Escrevemo-los de forma simples. Se tiveres dúvidas, fala connosco antes de comprar.”
h2 “1. Quem vende” → “[TEU_NOME], [cidade], Moçambique. Contacto: WhatsApp [TEU_WHATSAPP] | Email [TEU_EMAIL].”
h2 “2. O produto” → “O WhatsApp que Vende é um produto digital: um guia em PDF com scripts, respostas rápidas, calendário de Status, modelos Canva, uma folha Google Sheets e os bónus descritos na página de vendas. Nada é enviado fisicamente. O Pack Datas Especiais é um extra opcional, disponível no checkout.”
h2 “3. Preço e pagamento” → “Os preços estão em meticais (MT) e aparecem na página antes da compra. O pagamento é único, sem mensalidades, e é processado pela EscalePay com M-Pesa ou e-Mola.”
h2 “4. Acesso” → “Depois de o pagamento ser confirmado, recebes o acesso por email ou na área de membros da EscalePay. Se não o receberes, fala connosco e resolvemos.”
h2 “5. Reembolso” → “Podes pedir o reembolso do guia, do Pack Datas Especiais e dos serviços opcionais dentro de 7 dias a contar da compra, pela plataforma de pagamento, de acordo com a política de reembolso da EscalePay.” (make “política de reembolso da EscalePay” a link to ESCALEPAY_REFUND_POLICY_URL, new tab)
h2 “6. Licença de uso” → “O guia e os ficheiros são para uso pessoal e para o teu próprio negócio. Podes adaptar os scripts, as legendas e os modelos ao teu negócio. Não podes revender, partilhar, copiar, publicar ou distribuir o guia ou os ficheiros, gratuitamente ou não.”
h2 “7. Serviços opcionais” → “Os serviços 'Configuro o teu WhatsApp Business por ti' (1.497 MT) e 'Revisão Express do teu WhatsApp Business' (497 MT) são feitos pessoalmente e têm vagas limitadas. Os prazos de entrega contam a partir da recepção do formulário completo. És tu que fazes as alterações no teu telemóvel; nunca pedimos códigos, PIN nem acesso à tua conta.”
h2 “8. Resultados” → “O guia ensina organização e método. Não garantimos vendas, rendimentos, lucros, clientes nem empregos. Os resultados dependem do teu produto, dos teus preços, da tua zona, da tua dedicação e de factores fora do nosso controlo.”
h2 “9. Uso responsável do WhatsApp” → “O guia não ensina a enviar mensagens em massa a desconhecidos nem a comprar listas de contactos. Não somos responsáveis por restrições aplicadas pelo WhatsApp a contas que não sigam as regras da plataforma.”
h2 “10. Afiliados” → “Os afiliados são parceiros independentes. Devem identificar os seus links como links de afiliado e não estão autorizados a prometer resultados ou rendimentos.”
h2 “11. Alterações e lei aplicável” → “Podemos actualizar estes termos; a versão em vigor é a publicada nesta página. Estes termos regem-se pela lei da República de Moçambique.”
h2 “12. Avisos importantes” → list (exactly these 12 items):
“Este produto não é afiliado, patrocinado nem aprovado pela Meta Platforms, Inc. ou pelo WhatsApp. WhatsApp é uma marca registada da Meta. Não usamos o logótipo do WhatsApp.”
“Não garantimos vendas, rendimentos, lucros, clientes nem empregos. O guia ensina organização e método; os resultados variam e dependem do teu produto, preços, zona, dedicação e de factores fora do nosso controlo.”
“Isto não é um esquema de 'ganhar dinheiro online', de investimento ou de tarefas pagas. Nunca te pediremos pagamentos para 'desbloquear' ganhos.”
“Os exemplos de 'antes e depois' e as conversas mostradas na página são ilustrativos, salvo quando indicados como depoimento real com autorização.”
“Os depoimentos publicados são reais, com autorização escrita, e não representam resultados típicos. Quem recebeu o guia gratuitamente para dar opinião é identificado.”
“As funcionalidades e os menus do WhatsApp Business podem mudar com actualizações e variar entre Android e iPhone. O guia é actualizado sempre que possível.”
“As orientações sobre pagamentos M-Pesa e e-Mola são preventivas e gerais. Não substituem as indicações oficiais das operadoras; em caso de problema, contacta os canais oficiais da tua operadora.”
“Nunca te pediremos o PIN, códigos M-Pesa/e-Mola, códigos de verificação do WhatsApp nem acesso à tua conta, incluindo nos serviços de configuração e de revisão.”
“Os pagamentos são processados pela EscalePay. O reembolso do guia, do Pack Datas Especiais e dos serviços opcionais pode ser pedido dentro de 7 dias, de acordo com a política de reembolso da plataforma.”
“Os serviços 'Configuro o teu WhatsApp Business por ti' e 'Revisão Express do teu WhatsApp Business' têm capacidade limitada porque são feitos pessoalmente; os prazos de entrega contam a partir da recepção do formulário completo.”
“Recolhemos apenas os dados necessários para entregar o produto e dar suporte. Não vendemos nem partilhamos os teus dados. Podes pedir a eliminação a qualquer momento. Ver a Política de Privacidade.” (make “Política de Privacidade” a link to /privacidade)
“Os afiliados são parceiros independentes, devem identificar os seus links como links de afiliado e não estão autorizados a prometer resultados ou rendimentos.”
```

Check after:
- [ ] /privacidade shows 8 numbered sections and /termos shows 12, all in Portuguese and readable on mobile
- [ ] Name, city, email and WhatsApp are filled from config (or highlighted while still placeholders); 'Última actualização: [data]' is at the top
- [ ] Termos section 12 lists all 12 disclaimers word for word
- [ ] Refund links open the EscalePay policy URL in a new tab; 'Política de Privacidade' inside the disclaimers goes to /privacidade
- [ ] Footer links on every page reach both legal pages

## Step 7 · SEO, link previews, analytics, performance and accessibility (all pages)

Goal: Make the page look right when shared on WhatsApp/Facebook, set titles and robots rules, add optional Meta/TikTok pixels with honest events, and optimise speed and accessibility without changing any visible content.

```text
Add SEO, link previews, analytics, performance and accessibility. Do NOT change any visible text, colours or layout.
(I have attached my share image; if an image is attached, save it as public/og-image.jpg. If none is attached, still reference that path and tell me that I must upload it.)

1) index.html static tags (important: WhatsApp and Facebook link previews do not run JavaScript, so these must be static in index.html):
<html lang='pt-MZ'>
<title>: “WhatsApp que Vende - Guia prático para vender pelo WhatsApp em Moçambique”
meta description: “Configura o WhatsApp Business como uma loja em 7 dias: catálogo com preços, respostas rápidas, scripts, calendário de Status de 30 dias e regras anti-burla para M-Pesa e e-Mola. 597 MT.”
og:type website; og:locale pt_MZ; og:site_name 'WhatsApp que Vende'; og:title = the title above; og:description = the description above; og:url = the current SITE_URL value; og:image = SITE_URL + '/og-image.jpg' as an ABSOLUTE URL; og:image:width 1200; og:image:height 630; og:image:alt 'WhatsApp que Vende - guia prático, 597 MT'; twitter:card summary_large_image with the same title, description and image; theme-color #0F7B5F; canonical link = SITE_URL + '/'. Write the SITE_URL value literally and add the comment <!-- update these URLs when SITE_URL changes -->. Remove any default Lovable title, description, og image or favicon.

2) Per-route title and robots (small usePageMeta hook or react-helmet-async): '/' = the title above; '/obrigado' = 'Obrigado - WhatsApp que Vende' + noindex; '/oferta-especial' = 'Oferta especial - WhatsApp que Vende' + noindex, nofollow; '/afiliados' = 'Programa de afiliados - WhatsApp que Vende'; '/privacidade' = 'Política de Privacidade - WhatsApp que Vende'; '/termos' = 'Termos e Condições - WhatsApp que Vende'.

3) public/robots.txt: allow everything except 'Disallow: /obrigado' and 'Disallow: /oferta-especial'; add 'Sitemap: ' + SITE_URL + '/sitemap.xml'. Create public/sitemap.xml with '/', '/afiliados', '/privacidade', '/termos'.

4) Favicon: public/favicon.svg as a rounded square #0F7B5F with a bold white letter 'M', plus a 180x180 apple-touch-icon PNG version if possible. No WhatsApp logo.

5) Analytics in src/lib/analytics.ts (fill in the stubs from step 1):
- If META_PIXEL_ID is not empty, inject the standard Meta Pixel base code once and call fbq('init', META_PIXEL_ID). If TIKTOK_PIXEL_ID is not empty, inject the standard TikTok Pixel base code and call ttq.load(TIKTOK_PIXEL_ID). If both are empty, load NOTHING (no scripts, no network requests).
- trackPageView(): call it on every route change (fbq('track','PageView') and ttq.page()).
- trackCheckoutClick(ctaId, href): if href equals ESCALEPAY_CHECKOUT_URL, send Meta 'InitiateCheckout' with {value: 597, currency: 'MZN', content_name: 'WhatsApp que Vende', content_category: ctaId} and TikTok 'InitiateCheckout' with {value: 597, currency: 'MZN'}. If href equals ESCALEPAY_UPSELL_URL, send the same events with value 1497 and content_name 'Configuração WhatsApp Business'. For any other href, send nothing. Never block or delay navigation; wrap everything in try/catch.
- Do NOT fire 'Purchase' anywhere on this site (the thank-you page can be opened without buying). Add the code comment: 'Purchase must come from EscalePay's own pixel integration, if available.'

6) Performance: every <img> gets width and height attributes, decoding='async' and loading='lazy', except the hero mockup (loading='eager', fetchpriority='high'). Use object-fit: cover/contain to avoid stretching. Prefer WebP files from public/images, with a maximum display width of 1200px (creator photo 600px). Google Fonts: only Bricolage Grotesque 700;800 and Inter 400;500;600;700 with display=swap and preconnect. No autoplay video, no heavy animation libraries; remove unused shadcn components and unused dependencies. Target Lighthouse mobile: Performance ≥ 90, Accessibility ≥ 95, SEO 100.

7) Accessibility: Portuguese alt texts (mockup 'Capa do guia WhatsApp que Vende num telemóvel Android'; creator photo 'Foto de ' + CREATOR_NAME; bonus thumbnails 'Pré-visualização do Bónus 1' to 'Bónus 4'; PDF page previews 'Página de exemplo do guia'); decorative icons aria-hidden='true'. Accordions are keyboard-accessible with aria-expanded. All text meets WCAG AA contrast (never use #D9952B or #8C9A94 for text). Tap targets at least 44x44px. Exactly one h1 per page and logical h2/h3 order. prefers-reduced-motion disables animations. Links opening a new tab have rel='noopener noreferrer'. The skip link 'Saltar para o conteúdo' works.

When finished, reply with a short list of what you changed.
```

Check after:
- [ ] The browser tab shows the new title and the green 'M' favicon (not the Lovable default)
- [ ] Navigating between pages changes the tab title (Obrigado, Oferta especial, Programa de afiliados, ...)
- [ ] In Code view, index.html contains og:title, og:description and an absolute og:image URL; public/og-image.jpg, robots.txt and sitemap.xml exist
- [ ] With empty pixel IDs, no Meta/TikTok scripts load (Lovable's reply should confirm this). After you add IDs and publish, Meta Pixel Helper / TikTok Pixel Helper show PageView, and InitiateCheckout when you tap a buy button
- [ ] Nothing visible on the page changed (same texts, colours, layout); images still display correctly

## Step 8 · Final polish and mobile QA (all pages)

Goal: Fix layout bugs at every phone width, audit all links and forbidden elements, and get a list of the placeholders still to replace before publishing.

```text
Do a final polish and QA pass on the whole site. Do NOT change any Portuguese copy (everything in src/content/*.ts, the footer and the legal pages must stay word for word), colours, prices or link destinations. Only fix layout, spacing, consistency and bugs.

1. Check every route ('/', '/obrigado', '/oferta-especial', '/afiliados', '/privacidade', '/termos' and a 404) at widths 360px, 390px, 414px, 768px, 1024px and 1440px. Fix: any horizontal scrolling; text or buttons touching the screen edge (minimum 16px side padding); hero h1 longer than 3 lines at 360px; awkward headline breaks; uneven card heights in grids; stretched or blurry images; long words or URLs overflowing (overflow-wrap: anywhere on links and emails).
2. Sticky bar and 'Dúvidas?' pill: on '/' on mobile the bar appears only after scrolling past #hero-cta, hides while #final_cta is visible, never covers content (enough bottom padding above the footer), and the Dúvidas? pill sits above the bar without overlapping. On '/oferta-especial' neither appears. The sticky bar exists only on '/'.
3. Buttons: all buy buttons min height 52px, identical style per variant, labels wrap neatly and stay centred, 24px space above each section button, visible hover/active/focus states.
4. Spacing rhythm: section padding 56px mobile / 96px desktop everywhere; headline → subheadline 12px; subheadline → content 24-32px; alternating section backgrounds so every section is clearly separated.
5. Accordions: modules (type multiple, all closed by default); FAQ (type single, collapsible, first item open). Smooth, but respect prefers-reduced-motion.
6. Search the whole codebase and remove anything that matches: countdown timers, visitor or stock counters, fake purchase notifications, star ratings, crossed-out prices, sample or placeholder testimonials, stock photos, any WhatsApp logo or chat-bubble icon, and the colours #25D366, #128C7E, #075E54.
7. Link audit: every product buy button → ESCALEPAY_CHECKOUT_URL (same tab); upsell YES → ESCALEPAY_UPSELL_URL; upsell NO → '/obrigado'; refund links → ESCALEPAY_REFUND_POLICY_URL (new tab); all WhatsApp links → 'https://wa.me/' + WHATSAPP_NUMBER with a prefilled text; legal links work. No URLs, phone numbers or prices hardcoded outside src/config/site.ts (prices that are part of the copy text are fine).
8. Fix all console errors and warnings and all TypeScript errors.
9. Reply in chat with: (a) a table of every button and link: page, label, ctaId, destination; (b) a list of every text that still contains [square brackets], with the file and line, so I can replace each one before publishing.
```

Check after:
- [ ] Lovable's table: every buy button points to ESCALEPAY_CHECKOUT_URL, YES to ESCALEPAY_UPSELL_URL, NO to /obrigado, WhatsApp links to wa.me/ + your number
- [ ] Lovable's placeholder list: keep it. It is your to-do list (story, about, [Android/iPhone], [número real], [data], your contact details)
- [ ] Mobile preview at the smallest width: no sideways scroll on any page; the sticky bar and Dúvidas? pill never overlap each other or any text
- [ ] The copy is still unchanged: re-check the hero headline, one FAQ answer and the footer disclaimer
- [ ] No console errors shown in Lovable

## Fix prompts

### Layout broken or page scrolls sideways on mobile

```text
On mobile (360-414px), the section with id '[SECTION_ID]' is broken: [describe what you see]. Fix ONLY layout/CSS: no horizontal scroll anywhere, all grids become 1 column below 768px, 16px side padding, images max-width 100% with height auto, buttons full width up to 420px, long words and links wrap (overflow-wrap: anywhere). Do not change any text, colours, links or other sections.
```

### Wrong colours, or WhatsApp-style green or icons appeared

```text
The colours are wrong in '[SECTION_ID or page]'. Use only these tokens: page background #FAF7F0, cards #FFFFFF, headings #13261F, paragraphs #33433D, muted #5E6E68, primary buttons #0F7B5F (hover #0B634C) with white text, light band #E7F2EC, borders #DDE5E0, ochre #D9952B only for thin decorative bars/lines, final CTA band #0F7B5F with white text and a white button with green text. Remove any #25D366, #128C7E, #075E54 or similar bright WhatsApp greens, any WhatsApp logo and any chat-bubble icon from the whole project. Do not change text or layout.
```

### A buy button does not open the checkout (or opens the wrong link)

```text
The button '[button label]' in section '[SECTION_ID]' does not go to the right place. Every product buy button must be the CtaButton component with href = ESCALEPAY_CHECKOUT_URL imported from src/config/site.ts, rendered as a real <a href> that opens in the same tab. The upsell YES uses ESCALEPAY_UPSELL_URL; the upsell NO is a link to '/obrigado'. Remove any hardcoded URLs, onClick-only navigation or preventDefault, and make sure analytics never blocks the click. Reply with a list of all buttons and their destinations.
```

### Lovable changed, shortened or 'improved' the Portuguese copy

```text
You changed my Portuguese copy in section '[SECTION_ID]'. Restore it to EXACTLY the text below, character for character (keep accents and the spelling 'actualização', 'exactamente', 'objecções'), store it in src/content/salesCopy.ts and make the component read it from there. From now on, never rewrite, translate, shorten or improve any Portuguese text unless I paste new text. Correct text: “[paste the original text for that section from step 2]”
```

### Images load slowly or look stretched

```text
The page is slow on mobile data because of images. For every image in public/images and src: convert to WebP (or compressed JPG) under 200 KB, max width 1200px (creator photo 600px), add width and height attributes, loading='lazy' and decoding='async' (except the hero mockup: loading='eager', fetchpriority='high'), use object-fit so nothing stretches, and delete unused images. Do not change the design or any text.
```

### Sticky bar or 'Dúvidas?' button covers content or overlaps

```text
On mobile, the sticky bottom bar or the 'Dúvidas?' pill covers content at [where]. Fix: the sticky bar exists only on '/', appears only after #hero-cta has scrolled out of view upwards, and hides while #final_cta is visible. Add at least 96px bottom padding on mobile so the footer is never covered. While the bar is visible, the Dúvidas? pill moves up to sit above it. Neither appears on '/oferta-especial'. They must never overlap each other, buttons or text.
```

### Literal ** asterisks visible, bold missing, or placeholders not filled/highlighted

```text
In '[SECTION_ID or page]' I can see literal ** asterisks (or the bold is missing, or [placeholders] are not handled). Render all copy through the RichText component: **text** becomes <strong> with no asterisks, blank lines become separate paragraphs, [TEU_WHATSAPP], [TEU_EMAIL], [TEU_NOME], [TEU_NOME ou nome do negócio registado], [cidade] and [cidade real] are filled from src/config/site.ts, and any other [brackets] are highlighted only while HIGHLIGHT_PLACEHOLDERS is true. Do not change any words.
```

### Accordions don't open, all open at once, or fonts/accents look wrong

```text
The accordions in '#whats_inside' and/or '#faq' are not working correctly: [describe]. Use the shadcn Accordion: modules type 'multiple', all closed by default; FAQ type 'single', collapsible, with the first item open by default. Each trigger is a full-width button at least 48px tall, with aria-expanded and a chevron that rotates. Also confirm that headings use 'Bricolage Grotesque' (700/800) and body text 'Inter' (400-700) loaded from Google Fonts with display=swap, and that accented letters (ç, ã, õ, é, ê) display correctly. Do not change any text.
```

