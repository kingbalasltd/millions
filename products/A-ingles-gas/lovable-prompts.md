# Inglês para o Gás e a Mineração: Kit Turno 15: Lovable prompts

Paste one step at a time and check the preview before the next.

## Step 1 · Project setup + design system + global components (all routes)

Goal: Create the project foundation: design tokens, fonts, the src/config.ts file with every link, fact and switch, the helpers (RichText, CheckoutButton, whatsappLink), the global components (notice bar, header, footer with the full legal notice, sticky mobile CTA, WhatsApp button) and every route as a placeholder.

```text
Create a new mobile-first marketing website called Kit Turno 15. All visible text is in Portuguese (Mozambique). This first message sets up the FOUNDATION ONLY: design system, config file, helpers, global components and routes. Do NOT build the page sections yet; I will send each page in later messages.

TECH: React + TypeScript + Vite + Tailwind CSS + shadcn/ui + react-router-dom + lucide-react icons. No backend, no database, no login, no animation libraries. No emojis anywhere.

1) DESIGN TOKENS (add to tailwind.config.ts as named colours and to index.css as CSS variables):
- navy #0B2545 (brand, hero and final CTA backgrounds, headings, text on orange buttons)
- navy-deep #071A33 (footer background)
- orange #F28C28 (CTA buttons, icons, tags). Text on orange is ALWAYS navy #0B2545 bold, never white. Never use orange as a text colour on white.
- orange-hover #E07B16
- orange-soft #FFF4E8 (notice boxes, guarantee)
- concrete #F4F5F7 (notice bar, alternate sections)
- ink #1B2430 (body text)
- muted #5B6573 (secondary text on white)
- mist #C9D2DE (small text on navy, footer text)
- line #D9DEE5 (borders)
- wa-green #1A9E4B (WhatsApp button only)
- placeholder #FFF3A3 (highlight for unfinished placeholders)
Fonts (Google Fonts, display=swap, with preconnect): Barlow weights 600,700,800 for headings; Source Sans 3 weights 400,600,700 for body. Load only these weights.
Typography: body 17px on mobile, 18px on desktop, line-height 1.6, colour ink. H1 font-size clamp(26px, 6.5vw, 44px), Barlow 800, line-height 1.15. H2 clamp(24px, 5.5vw, 36px), Barlow 700. H3 20px Barlow 700.
Layout: container max-width 1120px with 16px side padding on mobile; long text blocks max-width 680px; sections py-14 on mobile, py-20 on desktop. Cards: white, 1px line border, 12px radius, very soft shadow. Buttons: 10px radius. Focus style for every interactive element: 3px solid orange outline with 2px offset.
Create a <SafetyStripe /> component: a 6px-high full-width bar of 45-degree diagonal stripes alternating orange #F28C28 and navy #0B2545 (repeating-linear-gradient). It is decorative (aria-hidden).

2) CONFIG FILE: create src/config.ts with exactly these exports and comments. I will edit the values myself later:
// LINKS (replace before publishing)
export const ESCALEPAY_CHECKOUT_URL = 'https://SUBSTITUIR-link-checkout-kit-turno-15';
export const ESCALEPAY_UPSELL_URL = 'https://SUBSTITUIR-link-checkout-revisao-pessoal';
export const ESCALEPAY_AFFILIATE_URL = ''; // EscalePay affiliate sign-up link; if empty the affiliate button opens WhatsApp
export const WHATSAPP_NUMBER = '258XXXXXXXXX'; // digits only, no + or spaces
export const WHATSAPP_DISPLAY = '[número real]';
export const SUPPORT_HOURS = '[horário real de atendimento, ex.: de segunda a sábado, das 8h às 20h]';
export const SITE_URL = 'https://kit-turno-15.lovable.app'; // update after publishing
// REAL FACTS (never invent)
export const CREATOR_NAME = '[SEU NOME]';
export const CREATOR_CITY = '[SUA CIDADE]';
export const BUSINESS_NAME = '[SEU NOME ou nome do negócio]';
export const CREATOR_PHOTO = ''; // e.g. '/criador.webp' (your own photo). Empty = show initials
export const NEXT_COHORT_DATE = '[data real da próxima turma]';
export const COHORT_NUMBER = '[número]';
export const ENROLMENT_CLOSE_DATE = '[data real]';
export const KIT_SIZE_MB = '[TAMANHO REAL]';
export const UPSELL_DELIVERY_DAYS = '[X]';
export const UPSELL_SLOTS_PER_WEEK = '[N]';
export const LAUNCH_PRICE_END_DATE = '[data real]';
export const REVIEWER = '[nome e papel real da pessoa que ajudou]';
// SWITCHES
export const SHOW_STORY = false; // true only after writing your real story
export const SHOW_TESTIMONIALS = false; // Only show real testimonials with written permission.
export const TESTIMONIALS: { text: string; name: string; city: string; date: string; gotFree: boolean }[] = []; // Only real testimonials with written permission.
export const SHOW_LAUNCH_PRICE = false; // if true you must change every price on the page, in EscalePay and in WhatsApp on the same day
export const SHOW_PRICE_COMPARISON = false; // true only after confirming a current course price
export const SHOW_COHORT_LINE = false; // true only when the cohort dates are real
export const SHOW_ACESSO_IMEDIATO = true; // false if your test purchase did not confirm immediate access
export const SHOW_AI_DISCLOSURE = true; // keep true only if true
export const SHOW_REVIEWER_LINE = false;
export const SHOW_AFFILIATE_MANUAL_APPROVAL = false;
export const SHOW_ANTIBURLA_PAGE = true;
// ANALYTICS (leave empty if you have none)
export const META_PIXEL_ID = '';
export const TIKTOK_PIXEL_ID = '';

3) HELPERS:
a) <RichText text={string} className? />: splits the text into <p> paragraphs on blank lines, turns **double asterisks** into <strong> (removing the asterisks), and wraps any text in square brackets [like this] (brackets included) in <mark className='placeholder'> with background #FFF3A3, a 1px dashed #B8A100 border and 2px 4px padding, so I can see unfinished text in the preview. It must NEVER change any other character.
b) whatsappLink(message: string) in src/lib/links.ts returns 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(message).
c) <CheckoutButton href label variant='primary' | 'outline' onClick? />: primary = orange background, navy Source Sans 3 bold 18px text, min-height 52px, w-full on mobile and auto width with min-width 300px from sm up, hover orange-hover, 10px radius, focus ring. outline = transparent background, 2px navy border, navy bold text, same size. It is a normal <a> in the same tab (no target blank) with data-event='checkout'. By default it calls trackCheckout() from src/lib/analytics.ts. Create analytics.ts now with empty functions trackCheckout(), trackUpsellClick(), trackContact() and initAnalytics(); a later message fills them.
d) <Microcopy>: 14px text; muted colour on light backgrounds, mist colour on navy.

4) GLOBAL COMPONENTS (in a Layout wrapper used by every route):
a) Skip link: the first focusable element, text “Saltar para o conteúdo”, visible only on focus, jumps to <main id='conteudo'>.
b) NoticeBar: full-width thin bar at the very top of every page, background concrete #F4F5F7, navy text 13px on mobile and 14px on desktop, centred, 8px vertical padding. Exact text: “Produto independente. Não somos agência de recrutamento e não vendemos vagas.”
c) Header (white, 1px bottom border, height 60px, NOT sticky): left is the wordmark “Kit Turno 15” in Barlow 800 navy 20px with a small orange lucide HardHat icon before it (if public/logo.svg exists, use that image instead), linking to '/'. On desktop (md+), on the right: anchor links “Módulos” (#modulos), “Bónus” (#bonus), “Preço” (#oferta), “Perguntas” (#faq) in navy 16px, plus a compact orange button “Comprar por 697 MT” linking to ESCALEPAY_CHECKOUT_URL. On mobile: only the wordmark and a compact orange button “Comprar” (min-height 44px). On routes other than '/', the anchor links go to '/#modulos' etc. Hide the buy buttons and anchor links on /obrigado and /oferta-especial (show only the wordmark there). Use smooth scrolling with scroll-margin-top 16px on sections, turned off under prefers-reduced-motion.
d) Footer (background navy-deep #071A33, text mist #C9D2DE 14px, line-height 1.6, links underlined and white on hover, max-width 760px text block). Exact copy, rendered with RichText:
Title (Barlow 700, white, 18px): “Kit Turno 15 · Inglês de Trabalho”
Subtitle (white, 15px): “Produto independente de preparação. Não garante emprego.”
Paragraph 1: “**Aviso legal:** O Kit Turno 15 é um produto digital de aprendizagem de inglês e preparação de documentos. Não garante emprego, entrevistas, contratação, salário nem rendimento. Os resultados dependem do esforço e da prática de cada pessoa.”
Paragraph 2: “Este produto é independente e não tem ligação, patrocínio nem aprovação de nenhuma empresa, projecto, empreiteiro ou entidade do governo. Não somos agência de recrutamento e nunca pedimos dinheiro para vagas.”
Paragraph 3: “O vocabulário de segurança serve para aprender inglês. Não substitui formações oficiais de segurança, induções, exames médicos nem certificações profissionais. Os procedimentos do seu empregador vêm sempre primeiro.”
Paragraph 4: “Pagamentos processados pela EscalePay. Nunca envie dinheiro para números pessoais em nome deste produto. © ” + current year (new Date().getFullYear()) + “ ” + BUSINESS_NAME + “.”
Links list (vertical on mobile, inline with · separators on desktop): “Política de Privacidade” → /privacidade; “Termos de Uso” → /termos; “Programa de Afiliados” → /afiliados; “Checklist Anti-Burla grátis” → /anti-burla (only if SHOW_ANTIBURLA_PAGE); “Suporte por WhatsApp: ” + WHATSAPP_DISPLAY → whatsappLink('Olá! Tenho uma dúvida sobre o Kit Turno 15.') opening in a new tab with rel='noopener noreferrer'.
The full legal notice must always be visible (never inside an accordion). Add padding-bottom 112px on mobile so the sticky bar never covers the links.
e) StickyMobileCTA: only on route '/', only below the md breakpoint. A fixed bottom bar, white background, top border line, shadow, padding 12px plus env(safe-area-inset-bottom). It contains one full-width primary CheckoutButton “Comprar por 697 MT” → ESCALEPAY_CHECKOUT_URL. Use IntersectionObserver: hidden while the element with id='hero' is in view, slides up (200ms transform) after the hero has scrolled out, and hides again while the element with id='oferta' or the <footer> is in view. No animation under prefers-reduced-motion. Expose its visible state (context or a CSS class on body) so the WhatsApp button can move up.
f) WhatsAppButton: a floating 56px circle, background wa-green #1A9E4B, white WhatsApp glyph (inline SVG of the WhatsApp phone-in-bubble logo; if not possible, lucide MessageCircle), a 2px white border and a shadow, fixed bottom-right 16px. When the sticky bar is visible it moves up to bottom 96px. aria-label “Falar no WhatsApp”. Links to whatsappLink('Olá! Tenho uma dúvida sobre o Kit Turno 15.') in a new tab with rel='noopener noreferrer'; on click it calls trackContact(). Show it on every route EXCEPT /oferta-especial.
g) ScrollToTop: scroll to top on every route change, unless the URL has a #hash (then scroll to that id).

5) ROUTES (react-router-dom): '/' (Home: for now just a <section id='hero'> with H1 “Kit Turno 15”), '/obrigado', '/oferta-especial', '/afiliados', '/privacidade', '/termos', '/anti-burla'. Each one is a placeholder page with only its H1 for now. Replace the default NotFound page with Portuguese: H1 “Página não encontrada”, text “O endereço que abriu não existe.”, primary button “Voltar ao início” → '/'. Set <html lang='pt'>.

6) PROJECT RULES (follow them in this and every future message):
- Never rewrite, translate, shorten, 'improve' or correct any Portuguese text I give you. Copy it character for character, including accents, old spellings such as acção, projecto, correctamente, the · separators and 'MT'. Text I give inside “ ” is exact copy: do not include the “ ” marks themselves.
- No emojis, no stock photos of people, no company logos, no countdown timers, no fake reviews or star ratings, no strikethrough prices, no popups.
- Every checkout and WhatsApp URL comes from src/config.ts. Never hardcode one.
- Mobile first: design at 360px width first, then scale up.

When you finish, reply with the list of files you created. Do not add any other content.
```

Check after:
- [ ] In mobile view (360-390px), the grey bar at the very top shows 'Produto independente. Não somos agência de recrutamento e não vendemos vagas.' with all accents correct.
- [ ] The header shows the 'Kit Turno 15' wordmark with the hard-hat icon and an orange 'Comprar' button with NAVY text (not white). On desktop, the 4 anchor links and 'Comprar por 697 MT' appear.
- [ ] The footer is dark navy with all 4 legal paragraphs fully visible, the year and '[SEU NOME ou nome do negócio]' highlighted in yellow, and 5 links.
- [ ] The round green WhatsApp button sits bottom-right. Tap it: it opens wa.me/258XXXXXXXXX with the message 'Olá! Tenho uma dúvida sobre o Kit Turno 15.'
- [ ] Type /afiliados, /termos and /xyz into the preview address bar: the first two show placeholder H1s, and /xyz shows 'Página não encontrada' with 'Voltar ao início'.
- [ ] Open the Code view (or ask Lovable to show it) and confirm src/config.ts exists with ESCALEPAY_CHECKOUT_URL, WHATSAPP_NUMBER and all the SHOW_ switches.
- [ ] The fonts look condensed and bold in headings (Barlow) and clean in body text (Source Sans 3), not the default system font.

## Step 2 · Sales page (/)

Goal: Build all 15 sections of the sales page, in order, with the reviewed Portuguese copy word for word, stored in one content file. Every button uses ESCALEPAY_CHECKOUT_URL, the optional blocks are controlled by config switches, and unfinished facts are highlighted.

```text
BUILD THE COMPLETE SALES PAGE ON ROUTE '/' for Kit Turno 15. Follow this message exactly and build EVERY section listed. If you run out of room, stop at the end of a whole section and tell me which section is next.

CONTEXT (in case anything from my first message is missing): a mobile-first Portuguese sales page for a 697 MT digital English kit sold through EscalePay (M-Pesa/e-Mola). Colours: navy #0B2545, deep navy #071A33, orange #F28C28 (buttons, ALWAYS with navy bold text, never white), soft orange #FFF4E8, concrete #F4F5F7, ink #1B2430, muted #5B6573, mist #C9D2DE, line #D9DEE5. Fonts: Barlow (headings), Source Sans 3 (body, minimum 16px). Reuse the existing src/config.ts, Layout, NoticeBar, Header, Footer, StickyMobileCTA, WhatsAppButton, CheckoutButton, RichText, Microcopy, SafetyStripe and whatsappLink. If any of them is missing, create it first exactly as described in my first message. Icons: lucide-react line icons only. No emojis.

COPY RULES (critical):
1. Put ALL Portuguese text below into src/content/salesCopy.ts as typed constants, character for character, and render the page from that file. Text between “ and ” is exact copy; do not include the “ ” marks. Do not translate, shorten, rephrase, re-punctuate or 'fix' anything (keep acção, projecto, correctamente, directas, Bónus, 12ª classe, the · separators).
2. Render every paragraph with <RichText>: **double asterisks** = bold, a blank line = new paragraph, [square-bracket text] = yellow placeholder highlight (keep these, they are instructions for me).
3. {CONFIG_NAME} means: insert the value of that export from src/config.ts (if the value is still a [bracket] placeholder it will show highlighted, which is correct).
4. (IF FLAG) means: render this block only when that config switch is true.
5. MICRO = “Pagamento por M-Pesa ou e-Mola · Acesso imediato · Garantia de 7 dias”. When SHOW_ACESSO_IMEDIATO is false, use “Pagamento por M-Pesa ou e-Mola · Garantia de 7 dias” instead.
6. Every buy button is a primary <CheckoutButton href={ESCALEPAY_CHECKOUT_URL}>. Never hardcode a URL. Each button is followed by MICRO in small text unless I say otherwise.
7. Do NOT add any text, badge, statistic, number, testimonial, logo, popup, timer or section that is not listed below.

SECTIONS, IN THIS EXACT ORDER:

1) HERO: <section id='hero'>, background navy, white text, <SafetyStripe/> at the top. Mobile: one column. Desktop (lg): text left (7/12), image right (5/12).
H1 (white, Barlow 800): “Inglês de trabalho para o sector do gás e da mineração, no seu telemóvel, em 15 minutos por dia.”
Subheadline (18px, colour #DCE3EC): “Aprenda o inglês de segurança, do terreno e da entrevista, e prepare o seu CV e a sua carta em inglês com modelos prontos a adaptar. Um plano de 30 dias. Preparação real, sem promessas falsas.”
Paragraph (white): “Para moçambicanos que conhecem o trabalho, mas travam quando o chefe, o formulário ou o recrutador fala inglês.”
Bullets (orange CheckCircle2 icons, white 17px text):
- “Inglês de segurança (HSE), de terreno e de rádio”
- “3 modelos de CV e 2 modelos de carta em inglês, para adaptar ao seu percurso”
- “40 perguntas de entrevista com respostas modelo e tradução”
- “Guia para reconhecer vagas falsas e proteger o seu dinheiro”
- “Gasta poucos dados: descarrega uma vez e estuda os ficheiros sem internet”
Button: “Quero começar por 697 MT”. Directly under it: MICRO in mist colour.
Image: <img src='/hero-telemovel.webp' alt='Telemóvel com um cartão de vocabulário do Kit Turno 15' width='360' height='640' loading='eager' fetchpriority='high'>. Until that file exists, show a CSS-only phone mockup (dark rounded frame, white screen) with a white card inside showing “Kit Turno 15” and “hazard = RÉ-zârd (perigo)”. On mobile the image goes after the microcopy, max-width 240px, centred.

2) PROBLEMA: <section id='problema'>, background concrete #F4F5F7, text block max 680px.
H2 (navy): “Conhece o trabalho, mas o inglês trava-o?”
Subheadline: “Se se revê em pelo menos uma destas situações, este kit foi feito para si.”
Bullets: each one a short row with a small orange outline circle icon, 17px:
- “Quando o supervisor fala inglês, fica calado com medo de errar.”
- “Não percebe bem as palavras de segurança da toolbox talk, dos sinais e dos formulários.”
- “O seu CV está só em português, ou é uma tradução que não sabe se está correcta.”
- “Nunca treinou uma entrevista em inglês em voz alta.”
- “Já viu alguém perder dinheiro com uma 'vaga' que pedia taxa de inscrição, farda ou processamento.”
- “Os cursos de inglês são caros, ficam longe, têm horários fixos e gastam muitos dados.”
Body (RichText): “Tem a 12ª classe, um curso técnico ou anos de experiência prática. Sabe fazer o trabalho.

Mas quando a conversa passa para inglês, tudo fica mais difícil. Não é falta de capacidade. É falta de prática com as palavras certas.”
CTA: a TEXT LINK (navy, underlined, bold, with a lucide ArrowDown icon), not a button: “Quero resolver isto” → #oferta.

3) HISTÓRIA (IF SHOW_STORY): <section id='historia'>, white background, max-width 640px, line-height 1.75. Optional round photo from CREATOR_PHOTO if not empty.
H2: “Porque criei este kit”
Subheadline: “[UMA FRASE REAL SOBRE SI. Ex.: o que viu acontecer na sua família, no seu bairro ou na sua cidade.]”
Body (RichText): “[ESCREVA AQUI A SUA HISTÓRIA REAL EM 3 A 5 FRASES CURTAS. Não invente nada. Responda com factos verdadeiros:]

[1. Quem é? Nome, idade, cidade.]

[2. Qual é a sua relação com o inglês? Como aprendeu e onde o usa.]

[3. O que viu que o levou a criar este kit? Ex.: alguém próximo que travou numa entrevista ou que perdeu dinheiro numa vaga falsa. Só escreva isto se for verdade.]

[4. Porque decidiu fazer um produto honesto, sem promessas de emprego?]

Este kit não é magia. É prática diária, com as palavras certas, no seu telemóvel.”
CTA text link: “Ver o que está incluído” → #modulos.

4) SOLUÇÃO: <section id='solucao'>, white background, max 680px. No company names, logos or maps.
H2: “O sector está a mexer. A sua preparação também pode.”
Subheadline: “Não precisa de ser fluente. Precisa de dominar o inglês que se usa no trabalho, no CV e na entrevista.”
Paragraphs (RichText): “Em Janeiro de 2026 foram retomadas as obras de um dos grandes projectos de gás natural em Cabo Delgado. E a nova Lei de Conteúdo Local, de 2026, torna obrigatório o recurso a empresas e trabalhadores nacionais no sector do petróleo e gás.

Nestes projectos usa-se português e inglês. Quem entende as instruções de segurança, tem um CV claro em inglês e consegue responder numa entrevista chega mais bem preparado.”
Box (background #FFF4E8, 4px navy left border, 16px padding, 8px radius): “**Atenção:** estar preparado não é o mesmo que ter emprego garantido. Ninguém honesto lhe pode garantir uma vaga. Este kit prepara-o para que, quando surgir uma vaga verdadeira, o inglês não seja o motivo de ficar de fora.”
Paragraph: “Foi para isso que criei o **Kit Turno 15**: o inglês do terreno, do CV e da entrevista, num plano de 30 dias pensado para o telemóvel.”
Bullets (navy CheckCircle2):
- “Inglês específico do sector, não inglês genérico”
- “Começa do zero, com pronúncia escrita para quem fala português”
- “Feito para telemóveis simples e poucos dados”
- “Inclui CV, carta, entrevista e protecção contra burlas”
Button: “Quero preparar-me” + MICRO.

5) MÉTODO: <section id='metodo'>, background concrete.
H2: “Método Turno 15: Reconhecer, Repetir, Responder”
Subheadline: “Um 'turno' de 15 minutos por dia, em três blocos de 5 minutos.”
Intro paragraph: “Cada dia é como um pequeno turno de trabalho. Curto, claro e com uma tarefa no fim.”
Three step cards, stacked on mobile and 3 columns on desktop. Each card has a decorative top row (aria-hidden): a 48px navy circle with the step number in orange Barlow 800, plus a small pill tag “5 min” (orange background, navy text). Below it, the paragraph exactly as written:
Card 1: “**1. Reconhecer (5 min):** lê um cartão com 5 a 8 palavras ou frases de trabalho, com o significado e a pronúncia aproximada escrita para quem fala português. Exemplo: hazard = RÉ-zârd (perigo).”
Card 2: “**2. Repetir (5 min):** diz cada palavra e a frase de exemplo em voz alta, 3 vezes. Falar todos os dias dá mais confiança do que só ler.”
Card 3: “**3. Responder (5 min):** faz um desafio real. Por exemplo, enviar uma nota de voz a responder a uma pergunta de supervisor, escrever uma linha de um relatório de incidente ou responder a uma pergunta de entrevista. Depois publica-o no grupo de prática.”
Paragraph after the cards: “Cada semana tem um tema do trabalho real, para que uma coisa leve à outra. E há um registo de progresso para marcar cada dia concluído.”
Vertical timeline (a navy line with orange dots), 5 items:
- “Semana 1: Segurança (HSE)”
- “Semana 2: Terreno, números e rádio”
- “Semana 3: Formulários, emails, CV e carta”
- “Semana 4: Entrevista em inglês”
- “Dias 29-30: Revisão geral e simulação final de entrevista”
Optional image <img src='/cartao-diario.webp' alt='Exemplo de cartão diário do Kit Turno 15' width='320' height='400' loading='lazy' decoding='async'>, max-width 280px, centred. Render it only if the file exists; otherwise skip it (no broken image).
Button: “Quero começar o meu Turno 15” + MICRO.

6) MÓDULOS: <section id='modulos'>, white background.
H2: “O que vai aprender: 10 módulos práticos”
Subheadline: “Do primeiro dia de segurança até à simulação de entrevista.”
Paragraph: “Toque em cada módulo para ver o que inclui. Explicações em português de Moçambique, com os termos de trabalho em inglês, tal como os vai ouvir.”
Accordion built with native <details>/<summary> (NOT a JavaScript accordion), all closed by default, 1px line borders between items, a lucide ChevronDown that rotates when open, and each summary at least 56px tall. In each <summary>: an orange pill tag (navy text) with the module label, then the title in bold navy. Inside, the description in ink colour. Use exactly these labels, titles and descriptions:
- “Módulo 0” | “Comece Aqui” | “Como usar o kit no telemóvel, teste de nível com 20 perguntas, como poupar dados e o aviso honesto sobre o que o kit faz e não faz.”
- “Módulo 1” | “Inglês de Segurança (HSE)” | “EPI (PPE), perigos e sinais, permit to work, near miss, stop work authority, alarme, evacuação e muster point.”
- “Módulo 2” | “Toolbox Talk e Instruções no Terreno” | “Ordens, números, medidas, horas e turnos, como pedir para repetir e como dizer 'isto não é seguro'.”
- “Módulo 3” | “Rádio, Telefone e Comunicação Curta” | “Alfabeto fonético, palavras de rádio, chamadas simples e mensagens de trabalho por SMS ou WhatsApp.”
- “Módulo 4” | “Inglês por Função (8 Áreas de Trabalho)” | “Vocabulário-chave para construção e andaimes, logística e armazém, motoristas, catering e acampamento, segurança, HSE, técnicos e administração.”
- “Módulo 5” | “Emails, Formulários e Relatórios Simples” | “Fichas de admissão e indução, timesheet, relatório de incidente simples e 10 emails modelo.”
- “Módulo 6” | “CV e Carta de Apresentação em Inglês” | “3 modelos de CV, 2 modelos de carta e como traduzir correctamente a 12ª classe, o técnico médio e a carta de condução.”
- “Módulo 7” | “Entrevista em Inglês” | “'Tell me about yourself' em 60 segundos, 40 perguntas com respostas modelo, perguntas de segurança e o método SAR (Situação, Acção, Resultado).”
- “Módulo 8” | “Vaga Verdadeira ou Burla?” | “12 sinais de vaga falsa, como verificar uma vaga e como proteger o seu BI, NUIT e dinheiro.”
- “Módulo 9” | “Plano Turno 15 (30 Dias)” | “Calendário de 30 dias, 30 cartões diários para o WhatsApp e registo de progresso.”
Button under the accordion: “Quero os 10 módulos” + MICRO.

7) BÓNUS: <section id='bonus'>, background concrete.
H2: “4 bónus incluídos”
Subheadline: “Para praticar com outras pessoas, proteger-se de burlas e ter o vocabulário certo sempre à mão.”
Four white cards, 1 column on mobile and 2x2 on desktop. Each card has a navy line icon (MessageSquare, ShieldCheck, Radio, BookOpen in that order), an orange pill tag with the bonus label, the name in bold and the text. No prices or 'valor' next to the bonuses.
- “Bónus 1” | “Grupo de Prática no WhatsApp (30 Dias)” | “Todos os dias recebe o desafio Turno 15 (texto, imagem e nota de voz). Responde com uma nota de voz no grupo de prática e recebe comentários em grupo várias vezes por semana. A próxima turma começa no dia {NEXT_COHORT_DATE}.”
- “Bónus 2” | “Checklist Anti-Burla (12 Sinais de Vaga Falsa)” | “Os 12 sinais de vaga falsa numa página, para guardar no telemóvel e partilhar com a família.”
- “Bónus 3” | “Cartão de Bolso de Rádio e Emergência” | “A versão de bolso do Módulo 3: alfabeto fonético, palavras de rádio e 15 frases de segurança numa só página.”
- “Bónus 4” | “Dicionários de Bolso por Função (8 Áreas)” | “A versão de bolso do Módulo 4: uma página com o vocabulário-chave de cada área de trabalho. Escolha a sua.”
Paragraph under the cards (bold navy, centred): “Os bónus estão incluídos nos 697 MT. Não paga nada a mais por eles.”
Button: “Quero o kit com os 4 bónus” + MICRO.

8) COMO FUNCIONA: <section id='como-funciona'>, white background.
H2: “Como funciona a compra”
Subheadline: “Simples, pelo telemóvel, sem cartão bancário.”
Three numbered steps, vertical, each with a navy line icon in a soft-orange circle (MousePointerClick, Smartphone, Download):
- “1. Carregue no botão e preencha os dados pedidos na página de pagamento da EscalePay (normalmente nome, número de telemóvel e email).”
- “2. Escolha M-Pesa ou e-Mola e confirme o pagamento no seu telemóvel, seguindo as instruções que aparecem (normalmente com o seu PIN).”
- “3. Receba o acesso. Descarregue os ficheiros uma vez (de preferência com Wi-Fi) e entre no grupo de prática pelo link que está dentro da área de acesso.”
Paragraph (RichText): “O pagamento é feito na página de pagamento da EscalePay, com M-Pesa ou e-Mola. Logo depois do pagamento, recebe o acesso.

**Nunca pedimos pagamentos para números pessoais.**”
Write M-Pesa and e-Mola as plain text; no payment logos.
Button: “Quero começar por 697 MT” + MICRO.
Small text under it (14px, muted): “Problemas no pagamento? Fale connosco no WhatsApp: ” followed by a link with the text {WHATSAPP_DISPLAY} → whatsappLink('Olá! Tenho um problema no pagamento do Kit Turno 15.'), new tab.

9) PARA QUEM: <section id='para-quem'>, background concrete. Two cards, stacked on mobile and side by side on desktop.
Card A (white):
H2: “Para quem é”
Subheadline: “Este kit é para si se...”
Bullets with navy CheckCircle2 icons:
- “Tem a 12ª classe, um curso técnico (técnico básico ou médio, INEFP ou semelhante) ou experiência prática.”
- “Trabalha ou quer trabalhar na construção, logística, transporte, catering, segurança, HSE, manutenção técnica ou administração na cadeia do gás e da mineração.”
- “Quer perceber as instruções de segurança e de terreno em inglês.”
- “Quer ter um CV e uma carta em inglês prontos para quando surgir uma vaga verdadeira.”
- “Quer treinar a entrevista em inglês sem pagar um curso caro.”
- “Estuda pelo telemóvel e precisa de poupar dados.”
- “Consegue reservar 15 minutos por dia durante 30 dias.”
Paragraph: “Não importa se o seu inglês é zero. O kit começa do princípio.”
Button inside the card: “Sou eu, quero começar” + MICRO.
Card B (light grey #EEF0F3, calm tone, NO button):
H2: “Para quem NÃO é”
Subheadline: “Preferimos ser claros agora do que desiludi-lo depois.”
Paragraph: “Se procura alguma destas coisas, este kit não é para si. E está tudo bem.”
Bullets with grey lucide X icons:
- “Quem procura emprego garantido. Este kit não dá vagas. E ninguém honesto vende vagas.”
- “Quem quer ficar fluente em 30 dias. 15 minutos por dia dão uma boa base de inglês de trabalho, não fluência.”
- “Quem precisa de um certificado oficial. O certificado de conclusão do kit não é oficial nem acreditado.”
- “Quem procura formação de segurança oficial. Isto é aprendizagem de inglês. Não substitui induções, formações nem certificações exigidas pelo empregador.”
- “Quem não vai praticar. Sem os 15 minutos diários, o kit não faz efeito.”

10) OFERTA: <section id='oferta'>, white background.
H2 (centred): “Tudo o que recebe hoje”
Subheadline (centred): “Um único pagamento de 697 MT. Sem mensalidades.”
Paragraph above the card (max 560px, centred): (IF SHOW_PRICE_COMPARISON) “Um curso presencial de inglês em Maputo pode custar perto de 30.000 MT por período.” followed, always, by “O Kit Turno 15 não substitui um curso completo. Mas foca-se exactamente no inglês do trabalho, do CV e da entrevista, por um valor que cabe no bolso.”
Offer card: white, 2px navy border, 16px radius, max-width 480px, centred, 24px padding. Checklist with navy CheckCircle2 icons:
- “Guia principal em PDF (Módulos 0 a 9), formatado para ecrã de telemóvel”
- “Cerca de 240 cartões de vocabulário + 30 cartões diários para o WhatsApp”
- “3 modelos de CV em inglês + 2 modelos de carta de apresentação (Google Docs, Word e PDF)”
- “Banco de 40 perguntas de entrevista com respostas modelo e tradução”
- “10 emails modelo, formulários comentados e modelo de relatório de incidente simples”
- “Teste de nível, calendário de 30 dias e registo de progresso”
- “Bónus 1: Grupo de Prática no WhatsApp (30 Dias)”
- “Bónus 2: Checklist Anti-Burla (12 Sinais de Vaga Falsa)”
- “Bónus 3: Cartão de Bolso de Rádio e Emergência”
- “Bónus 4: Dicionários de Bolso por Função (8 Áreas)”
Then a divider, then the price block, centred: small label “Preço:” (16px, muted) and below it “697 MT” in Barlow 800, 48px, navy. No strikethrough price, no timer.
(IF SHOW_LAUNCH_PRICE) paragraph: “Preço de lançamento de 497 MT para a Turma 1, até ao dia {LAUNCH_PRICE_END_DATE}. A partir dessa data o preço passa a 697 MT.”
Paragraph: “Pagamento por M-Pesa ou e-Mola, na página de pagamento da EscalePay. Acesso imediato. Garantia de 7 dias.” (when SHOW_ACESSO_IMEDIATO is false, render “Pagamento por M-Pesa ou e-Mola, na página de pagamento da EscalePay. Garantia de 7 dias.”)
Full-width button: “Comprar agora por 697 MT”, then MICRO.

11) GARANTIA: <section id='garantia'>, background #FFF4E8, max 680px. At the top, an inline SVG shield outline (navy stroke, 72px) with the text “7 dias” inside in Barlow 800 navy. It is my own graphic, not a platform logo.
H2: “Garantia de 7 dias”
Subheadline: “Experimente sem medo.”
Body (RichText): “Os produtos vendidos na EscalePay têm garantia de reembolso de 7 dias, de acordo com a política da plataforma.

Se comprar, abrir o kit e sentir que não é para si, peça o reembolso dentro de 7 dias pela EscalePay [confirme no seu painel o processo exacto e descreva-o aqui numa frase]. Se tiver dúvidas, fale comigo no WhatsApp de suporte e eu ajudo.

Não precisa de dar longas explicações. O seu pedido será respeitado.”
Button: “Quero experimentar” + MICRO.

12) SOBRE O CRIADOR: <section id='criador'>, white background, max 680px, NO button.
H2: “Quem criou o Kit Turno 15”
Top row: if CREATOR_PHOTO is not empty, a round 120px photo (alt “Foto de ” + CREATOR_NAME). Otherwise a 120px navy circle with white initials taken from CREATOR_NAME (use 'KT' while CREATOR_NAME is still a placeholder). Next to it the subheadline in bold: {CREATOR_NAME}, {CREATOR_CITY}
Body (RichText): “[SUA HISTÓRIA REAL EM 3 FRASES: quem é, qual é a sua relação com o inglês e porque criou o kit. Não invente cargos, anos de experiência no sector, diplomas nem resultados de alunos.]

O que posso garantir, com toda a honestidade:”
Bullets (navy ShieldCheck icons):
- “Não sou agência de recrutamento e não vendo vagas.”
- “Este produto é independente. Não tem ligação a nenhuma empresa, projecto ou entidade do governo.”
- (IF SHOW_AI_DISCLOSURE) “O conteúdo foi preparado com o apoio de ferramentas de inteligência artificial e revisto por mim, frase a frase. Os termos de segurança foram verificados em fontes públicas de referência.”
- (IF SHOW_REVIEWER_LINE) “O conteúdo foi revisto também por {REVIEWER}.”
- “Respondo pessoalmente no WhatsApp de suporte: ” followed by a link with the text {WHATSAPP_DISPLAY} → whatsappLink('Olá! Tenho uma dúvida sobre o Kit Turno 15.')

13) DEPOIMENTOS (IF SHOW_TESTIMONIALS AND TESTIMONIALS.length > 0): <section id='depoimentos'>, background concrete. Add the code comment: // Only show real testimonials with written permission.
H2: “O que dizem os alunos”
Subheadline: “Opiniões reais sobre o kit, partilhadas com autorização.”
For each item in TESTIMONIALS, a simple quote card: the text in quotes, then “— name, city, date”, and if gotFree is true a small line “Recebeu o kit grátis.” No star ratings, no photos.

14) PERGUNTAS FREQUENTES: <section id='faq'>, white background, max 760px.
H2: “Perguntas frequentes”
Subheadline: “Respostas directas, sem rodeios.”
Accordion with native <details>/<summary>, all closed, the question in bold navy (min-height 56px, ChevronDown icon), and the answer rendered with RichText. Exactly these 12, in this order:
Q1 “Isto garante emprego?” A: “Não. Este kit prepara-o: inglês de trabalho, CV, carta e entrevista. Nenhum produto honesto pode garantir emprego. E é exactamente por isso que o Módulo 8 ensina a fugir de quem 'garante' vagas a troco de dinheiro.”
Q2 “É afiliado à TotalEnergies, à ExxonMobil ou a outra empresa?” A: “Não. É um produto independente, sem ligação a nenhuma empresa, projecto, empreiteiro ou entidade do governo. Não somos agência de recrutamento e não vendemos vagas.”
Q3 “O meu inglês é zero. Serve para mim?” A: “Serve. O kit começa do zero e cada palavra tem a pronúncia aproximada escrita para quem fala português. Comece pelo teste de nível do Módulo 0 e siga o plano dia a dia.”
Q4 “Preciso de computador?” A: “Não. Tudo funciona no telemóvel: os PDFs abrem em qualquer leitor de PDF e os modelos de CV abrem no Google Docs ou no Word do telemóvel. Se quiser imprimir o CV, pode usar uma reprografia.”
Q5 “Gasta muitos dados?” A: “Pouco. Descarrega os ficheiros uma vez (o kit principal tem cerca de {KIT_SIZE_MB} MB), de preferência com Wi-Fi, e depois estuda sem internet. No grupo, o conteúdo diário é um texto, uma imagem e uma nota de voz curta.”
Q6 “Como recebo o kit depois de pagar?” A: “O acesso chega logo depois do pagamento, na área de membros ou por link [confirme na sua compra de teste e escreva aqui o método real]. O link do grupo de prática no WhatsApp está dentro da área de acesso. Se tiver algum problema, fale connosco no WhatsApp de suporte.”
Q7 “Posso pagar com M-Pesa ou e-Mola?” A: “Sim. O pagamento é feito na página de pagamento da EscalePay, com M-Pesa ou e-Mola. Não precisa de cartão bancário. Confirma o pagamento no seu telemóvel. Nunca pedimos pagamentos para números pessoais.”
Q8 “Quando começa o grupo de prática?” A: “As turmas começam em datas fixas. A próxima começa no dia {NEXT_COHORT_DATE}. Se comprar depois dessa data, entra na turma seguinte e pode começar já a estudar o kit sozinho. Atenção: num grupo de WhatsApp, o seu número fica visível para os outros membros.”
Q9 “Os áudios de pronúncia estão incluídos?” A: “Não estão incluídos no preço do kit. Os Áudios de Pronúncia Turno 15 são um extra opcional de 147 MT, que pode adicionar na página de pagamento antes de pagar. O kit funciona sem eles: a pronúncia aproximada está escrita em cada cartão e há notas de voz diárias no grupo.”
Q10 “E se eu não gostar?” A: “Tem garantia de reembolso de 7 dias, de acordo com a política da EscalePay. Peça o reembolso dentro desse prazo e o seu pedido será respeitado.”
Q11 “Recebo um certificado?” A: “Recebe um certificado de conclusão do kit, para sua motivação. Não é um certificado oficial nem acreditado, e não substitui formações ou certificações de segurança.”
Q12 “Há vídeos no YouTube grátis. Porque pagar?” A: “Há, e muitos são bons. Mas estão espalhados e quase nunca são sobre o nosso sector. Aqui tem o vocabulário de segurança e de terreno, o CV, a carta, a entrevista e o guia anti-burla num só plano de 30 dias, com um grupo para praticar a falar.”
After the accordion, a paragraph: “Se a sua dúvida não estiver aqui, envie mensagem para o WhatsApp de suporte: {WHATSAPP_DISPLAY}. Respondo {SUPPORT_HOURS}.”
Then an OUTLINE button (navy border, navy text, not orange): “Falar no WhatsApp” → whatsappLink('Tenho uma dúvida sobre o Kit Turno 15.'), new tab with rel='noopener noreferrer', calling trackContact() instead of trackCheckout(). No MICRO under this one.

15) CHAMADA FINAL: <section id='final'>, background navy, white text, <SafetyStripe/> at the top, centred, max 680px.
H2 (white): “Daqui a 30 dias de prática, o inglês do trabalho pode deixar de o travar.”
Subheadline (orange-free, colour #DCE3EC, 20px bold): “15 minutos por dia. 697 MT. Garantia de 7 dias.”
Body (RichText, white): “Já tem a vontade e a experiência. Falta o inglês do trabalho, um CV claro e treino de entrevista.

Comece hoje, pratique todos os dias e esteja mais bem preparado quando surgir uma vaga verdadeira.”
(IF SHOW_COHORT_LINE) paragraph: “A Turma {COHORT_NUMBER} do grupo de prática começa no dia {NEXT_COHORT_DATE}. As inscrições para esta turma fecham no dia {ENROLMENT_CLOSE_DATE}.”
Bullets (orange CheckCircle2, white text, inline on desktop and stacked on mobile): (IF SHOW_ACESSO_IMEDIATO) “Acesso imediato depois do pagamento”, “Pagamento por M-Pesa ou e-Mola”, “Garantia de 7 dias”.
Large button: “Quero começar por 697 MT”, then MICRO in mist colour. No countdown timer.

The global Footer follows (already built). Make sure the StickyMobileCTA observes id='hero' and id='oferta'.

When you finish, reply with: (1) the list of section ids rendered, and (2) every [placeholder] still showing on the page.
```

Check after:
- [ ] Scroll the mobile preview from top to bottom and confirm this order: Hero → Problema → Solução → Método → Módulos → Bónus → Como funciona → Para quem / Para quem NÃO é → Oferta → Garantia → Sobre o criador → Perguntas frequentes → Chamada final → Footer. 'Porque criei este kit' and 'O que dizem os alunos' must NOT appear yet.
- [ ] Every orange button has navy text. Hover or long-press 2-3 buttons: they point to https://SUBSTITUIR-link-checkout-kit-turno-15, not to '#' or a made-up URL.
- [ ] Under each orange button you see 'Pagamento por M-Pesa ou e-Mola · Acesso imediato · Garantia de 7 dias'.
- [ ] Spot-check 4 texts against the copy: the hero H1, the 'Atenção' box, Module 7 ('Tell me about yourself'...) and FAQ Q9 (147 MT). Every word, accent and apostrophe must match. Look for 'acção', 'projecto' and 'correctamente' (Lovable sometimes 'corrects' them).
- [ ] The Módulos accordion has 10 items and the FAQ has 12, all closed. Tapping one opens it.
- [ ] Yellow highlights appear for [número real], [data real da próxima turma], [TAMANHO REAL], [SEU NOME] and the bracketed instructions in Garantia, Sobre o criador and FAQ Q6. That is expected for now.
- [ ] On mobile, the sticky 'Comprar por 697 MT' bar only appears after you scroll past the hero and disappears at the Oferta section and the footer. The WhatsApp button moves up so the two don't overlap.
- [ ] The 'Quero resolver isto' text link scrolls to the offer card. The header 'Módulos', 'Bónus', 'Preço' and 'Perguntas' links scroll to the right sections on desktop.
- [ ] There is no horizontal scrolling at 360px width, and no emojis, star ratings, timers or strikethrough prices anywhere.

## Step 3 · Thank-you page (/obrigado)

Goal: Build the post-purchase thank-you page with the exact copy, 3 clear access steps, a support link and an honest reminder. Add a soft upsell teaser that is hidden when the buyer arrives from the upsell's NO link.

```text
BUILD THE THANK-YOU PAGE ON ROUTE '/obrigado' for Kit Turno 15.

CONTEXT (in case anything is missing): Portuguese (Mozambique) site. Colours: navy #0B2545, orange #F28C28 (buttons with NAVY bold text, never white), soft orange #FFF4E8, concrete #F4F5F7, ink #1B2430, muted #5B6573, line #D9DEE5. Fonts Barlow (headings) and Source Sans 3 (body, min 16px). Reuse src/config.ts, Layout, RichText (bold with **, paragraphs on blank lines, [brackets] highlighted yellow), CheckoutButton and whatsappLink. If any are missing, create them. lucide-react icons only, no emojis. On this route the header shows only the wordmark (no buy button), there is NO sticky buy bar, and the WhatsApp floating button stays.

COPY RULES: Text between “ and ” is exact copy: copy it character for character into src/content/thankYouCopy.ts and render from there. Do not translate, shorten or 'fix' anything. {CONFIG_NAME} = insert the value from src/config.ts.

LAYOUT (white background, single column, max-width 640px, centred, py-12):
1) A 64px circle in soft orange #FFF4E8 with a navy lucide CheckCircle2 icon (decorative).
2) H1 (navy, Barlow 800): “Compra confirmada! Boas-vindas ao Turno 15.”
3) Paragraph: “Obrigado pela sua confiança. O seu kit já está disponível.”
4) Paragraph (bold): “Siga estes 3 passos agora, de preferência com Wi-Fi, para poupar dados.”
5) Three step cards (white, 1px line border, 12px radius, 16px padding). Each has a 40px navy circle with the number in orange Barlow 800 (decorative, aria-hidden), then the text rendered with RichText exactly as follows:
- “1. Abra o acesso: entre na área de membros da EscalePay ou no link que recebeu [confirme e escreva o método real] e descarregue o Guia Principal e o PDF 'Comece Aqui'.”
- “2. Guarde os ficheiros no telemóvel (pasta Downloads ou Google Drive offline) para estudar sem internet.”
- “3. Entre no Grupo de Prática no WhatsApp pelo link que está dentro da área de acesso. A sua turma começa no dia {NEXT_COHORT_DATE}. Até lá, faça o teste de nível do Módulo 0.”
6) Paragraph: “Se algo não funcionar, envie mensagem para o WhatsApp de suporte: {WHATSAPP_DISPLAY}. Respondo {SUPPORT_HOURS}.”
Then an OUTLINE button (navy border and text): “Falar no WhatsApp” → whatsappLink('Olá! Já comprei o Kit Turno 15 e preciso de ajuda com o acesso.'), new tab with rel='noopener noreferrer'. It calls trackContact(), not trackCheckout().
7) Reminder box (background #FFF4E8, 4px navy left border, 16px padding, 8px radius), RichText: “**Lembrete honesto:** este kit prepara-o, mas não garante emprego. Nunca pague a ninguém para conseguir uma vaga.”
8) UPSELL TEASER: render ONLY if the URL query does NOT contain upsell=nao (read it with useSearchParams). A divider, then:
Paragraph (bold navy, 18px): “Antes de sair: quer o seu CV e a sua carta em inglês feitos consigo, a partir do seu percurso real? Veja a oferta abaixo.”
A card (2px navy border, 12px radius, 20px padding) containing:
H2 (22px): “Quer o seu CV e a sua carta em inglês feitos consigo?”
Paragraph: “Revisão Pessoal: CV + Carta em Inglês, por 1.497 MT. Lugares limitados: {UPSELL_SLOTS_PER_WEEK} clientes por semana.”
Primary orange button: “Sim, quero a Revisão Pessoal por 1.497 MT” → ESCALEPAY_UPSELL_URL. It calls trackUpsellClick() instead of trackCheckout().
Under it, a navy underlined text link: “Ver detalhes da oferta” → '/oferta-especial'.
9) Add <meta name='robots' content='noindex, nofollow'> for this route (react-helmet-async if not installed yet; install it) and set the document title to “Compra confirmada | Kit Turno 15”.

Do not add any other text, timers, confetti animations or popups. When finished, list any [placeholder] still visible on this page.
```

Check after:
- [ ] Open /obrigado in mobile view: the H1 reads exactly 'Compra confirmada! Boas-vindas ao Turno 15.' and the 3 numbered step cards are easy to read at 360px.
- [ ] Step 1 shows the yellow '[confirme e escreva o método real]' and step 3 shows the highlighted cohort date. Replace them later via config or a text edit.
- [ ] The 'Falar no WhatsApp' button opens wa.me/258XXXXXXXXX with the message about access help.
- [ ] The orange 'Lembrete honesto' box is present with 'Lembrete honesto:' in bold.
- [ ] The upsell teaser card is visible on /obrigado. Now open /obrigado?upsell=nao: the teaser must be gone.
- [ ] The 'Sim, quero a Revisão Pessoal por 1.497 MT' button points to https://SUBSTITUIR-link-checkout-revisao-pessoal, and 'Ver detalhes da oferta' goes to /oferta-especial.
- [ ] The header shows no 'Comprar' button on this page and there is no sticky bottom bar.

## Step 4 · Upsell page (/oferta-especial)

Goal: Build a focused, honest one-offer upsell page for the Revisão Pessoal (1.497 MT): YES goes to ESCALEPAY_UPSELL_URL, NO goes to /obrigado?upsell=nao, with no distractions and no fake urgency.

```text
BUILD THE UPSELL PAGE ON ROUTE '/oferta-especial' for Kit Turno 15.

CONTEXT (in case anything is missing): Portuguese (Mozambique) site. Colours: navy #0B2545, orange #F28C28 (buttons with NAVY bold text, never white), soft orange #FFF4E8, concrete #F4F5F7, ink #1B2430, muted #5B6573, line #D9DEE5. Fonts Barlow (headings) and Source Sans 3 (body, min 16px). Reuse src/config.ts, Layout, RichText (bold with **, paragraphs on blank lines, [brackets] highlighted yellow) and CheckoutButton. If any are missing, create them. lucide-react icons only, no emojis.

THIS PAGE MUST BE FOCUSED: the header shows only the wordmark (no nav links, no buy button), there is NO sticky bar and NO floating WhatsApp button. The footer stays.

COPY RULES: Text between “ and ” is exact copy: copy it character for character into src/content/upsellCopy.ts and render from there. Do not translate, shorten or 'fix' anything (keep '1.497 MT' with the dot). {CONFIG_NAME} = insert the value from src/config.ts.

REUSABLE CTA BLOCK (call it UpsellChoice), centred, max-width 480px:
- Primary orange button, full width, min-height 56px: “Sim, quero a Revisão Pessoal por 1.497 MT” → ESCALEPAY_UPSELL_URL (same tab). On click it calls trackUpsellClick() (not trackCheckout).
- Directly under it, small muted text: “Pagamento por M-Pesa ou e-Mola, na página de pagamento da EscalePay.”
- Then 16px of space and a plain muted underlined TEXT LINK (16px, not a button, but with a tap area of at least 44px): “Não, obrigado. Vou fazer o meu CV sozinho com os modelos do kit.” → '/obrigado?upsell=nao' (react-router Link). The NO option must be clearly visible, not hidden or tiny.

LAYOUT (white background, max-width 680px, py-10):
1) H1 (navy, Barlow 800): “Quer o seu CV e a sua carta em inglês feitos consigo?”
2) Subheadline (18px, bold): “Revisão Pessoal: CV + Carta em Inglês, por 1.497 MT. Lugares limitados: {UPSELL_SLOTS_PER_WEEK} clientes por semana.”
3) UpsellChoice (first time).
4) Body (RichText), exactly:
“O kit já lhe dá os modelos e as regras para fazer o seu CV sozinho. Mas muita gente prefere ter alguém a olhar para o seu caso concreto.

Funciona assim: preenche um formulário simples sobre o seu percurso real (escola, cursos, experiência, carta de condução, função que procura). Eu transformo essa informação num CV em inglês de 1 a 2 páginas e numa carta de apresentação para a função que escolher.

Não invento nada. Se faltar alguma informação, pergunto-lhe. Por segurança, nunca peço o número do BI nem o NUIT.

Entrega em {UPSELL_DELIVERY_DAYS} dias úteis, em Word e PDF, com 1 ronda de ajustes. Aceito apenas {UPSELL_SLOTS_PER_WEEK} clientes por semana, porque cada CV leva tempo a fazer bem.”
5) Honesty box (background #FFF4E8, 4px navy left border, 16px padding, 8px radius), RichText: “**Com honestidade:** este serviço não garante emprego. Garante documentos claros, honestos e bem escritos. Os seus dados e o seu CV são apagados 30 dias depois da entrega.”
6) Checklist card (white, 2px navy border, 16px radius, 20px padding) with navy CheckCircle2 icons:
- “CV em inglês de 1 a 2 páginas, simples e fácil de ler por sistemas de recrutamento (sem fotos, sem tabelas)”
- “Carta de apresentação adaptada à função que escolher”
- “Resposta pronta para 'Tell me about yourself', com base nos seus factos reais”
- “Lista das 5 principais mudanças e porquê, explicada em português”
- “Entrega em Word e PDF em {UPSELL_DELIVERY_DAYS} dias úteis, com 1 ronda de ajustes”
- “Coberto pela garantia de 7 dias da EscalePay”
7) Price line, centred: “1.497 MT” in Barlow 800, 40px, navy.
8) UpsellChoice (second time).
9) Route meta: <meta name='robots' content='noindex, nofollow'> and title “Revisão Pessoal: CV + Carta em Inglês | Kit Turno 15” (react-helmet-async).

Do NOT add countdown timers, 'only X left' counters, progress bars, 'Wait!' popups, exit-intent popups or any text not listed above. When finished, list any [placeholder] still visible.
```

Check after:
- [ ] Open /oferta-especial in mobile view: there are no header nav links, no WhatsApp bubble and no sticky bar. Only the offer is on the page.
- [ ] The YES button appears twice (after the subheadline and at the end). Its text is exactly 'Sim, quero a Revisão Pessoal por 1.497 MT' and it points to the ESCALEPAY_UPSELL_URL placeholder.
- [ ] Tap the NO link 'Não, obrigado. Vou fazer o meu CV sozinho com os modelos do kit.': it opens /obrigado WITHOUT the upsell teaser.
- [ ] 'Por segurança, nunca peço o número do BI nem o NUIT.' is present, and the 'Com honestidade:' box is visible.
- [ ] [X] and [N] are highlighted in yellow (delivery days and weekly slots), to be filled via config.
- [ ] There is no timer, counter or popup of any kind.

## Step 5 · Affiliate page (/afiliados)

Goal: Build an honest affiliate recruitment page for Facebook and WhatsApp job-group admins and TikTok creators. It shows the 40% commission, the mandatory promotion rules prominently, the materials list, and a CTA to the EscalePay affiliate sign-up (WhatsApp fallback).

```text
BUILD THE AFFILIATE PAGE ON ROUTE '/afiliados' for Kit Turno 15.

CONTEXT (in case anything is missing): Portuguese (Mozambique) site. Colours: navy #0B2545, orange #F28C28 (buttons with NAVY bold text, never white), soft orange #FFF4E8, concrete #F4F5F7, ink #1B2430, muted #5B6573, line #D9DEE5. Fonts Barlow (headings) and Source Sans 3 (body, min 16px). Reuse src/config.ts, Layout, RichText (bold with **, paragraphs on blank lines, [brackets] highlighted yellow), CheckoutButton and whatsappLink. If any are missing, create them. lucide-react icons only, no emojis. On this route: normal header, NO sticky buy bar, WhatsApp floating button stays.

COPY RULES: Text between “ and ” is exact copy: copy it character for character into src/content/affiliateCopy.ts and render from there. Do not translate, shorten or 'fix' anything. {CONFIG_NAME} = insert the value from src/config.ts.

AFFILIATE CTA BUTTON (primary orange, full width on mobile): “Quero ser afiliado (pedir acesso na EscalePay)”. Its href is ESCALEPAY_AFFILIATE_URL if that is not empty; otherwise whatsappLink('Olá! Quero ser afiliado do Kit Turno 15.') in a new tab with rel='noopener noreferrer'. It does NOT call trackCheckout (call trackContact instead).

LAYOUT:
1) Top section, background navy, white text, py-12, max 720px:
H1 (white): “Recomende um produto honesto e receba 40% de comissão”
Paragraphs (RichText, white): “É administrador de uma página ou grupo de vagas no Facebook ou no WhatsApp, cria conteúdo no TikTok ou trabalha com jovens à procura de emprego? O seu público precisa de se preparar e de se proteger de burlas.

O Kit Turno 15 ensina inglês de trabalho para o gás e a mineração, CV e carta em inglês, entrevista e como reconhecer vagas falsas. Custa 697 MT e paga-se por M-Pesa ou e-Mola na EscalePay.”
Affiliate CTA button.
2) Commission section, white background, max 720px, RichText:
“Por cada venda feita pelo seu link de afiliado, recebe **40% de comissão** sobre o produto principal (cerca de 279 MT por venda de 697 MT [confirme no painel se a comissão é calculada sobre o preço total]), pagos pela EscalePay de acordo com as regras da plataforma. Vendas reembolsadas dentro dos 7 dias podem não gerar comissão [confirme a regra no painel da EscalePay].

Não prometemos quanto vai ganhar. Isso depende de quantas pessoas reais o seu público ajudar.”
No earnings calculator, no income examples, no screenshots of earnings.
3) Rules box (background #FFF4E8, 4px navy left border, 12px radius, 20px padding), a lucide ShieldAlert icon in navy, then the title in bold navy: “Regras obrigatórias (quem não cumprir é removido):”, then a list with grey X icons:
- “Nunca prometa emprego, vagas ou rendimentos.”
- “Nunca diga 'vaga garantida' nem 'vaga na TotalEnergies/Exxon'.”
- “Não diga que o kit é 'o mais vendido' ou 'nº 1'.”
- “Não use logótipos, fotos ou fardas de empresas.”
- “Não invente depoimentos nem prazos.”
- “Não faça spam em grupos sem autorização do administrador.”
- “Inclua sempre a frase: 'Produto independente de preparação. Não garante emprego.'”
(IF SHOW_AFFILIATE_MANUAL_APPROVAL) paragraph after the box: “Os pedidos de afiliação são analisados um a um.”
4) Materials card (white, 2px navy border, 16px radius, 20px padding, max 560px, centred), heading H2 22px: “O que recebe como afiliado”, then a checklist with navy CheckCircle2 icons:
- “Comissão de 40% no produto principal (697 MT)”
- “Regras de divulgação numa página, em português”
- “5 imagens para o Status do WhatsApp com legendas prontas”
- “3 guiões de vídeo curtos (30-45 segundos) para gravar com a sua voz”
- “10 publicações prontas para Facebook e WhatsApp, com espaço para o seu link”
- “Modelo de publicação fixada para páginas de vagas”
- “Checklist Anti-Burla grátis para oferecer ao seu público”
- “Respostas às perguntas e objecções mais comuns”
- “Vídeo de demonstração de 60 segundos do produto por dentro”
- “Calendário real das turmas, para usar prazos verdadeiros”
- “Grupo de WhatsApp de afiliados com novos materiais e dicas semanais”
5) Affiliate CTA button again, centred, then a small muted line: “Produto independente de preparação. Não garante emprego.”
6) Title “Programa de Afiliados | Kit Turno 15” and a meta description: “Programa de afiliados do Kit Turno 15: 40% de comissão no produto principal, com regras de divulgação honestas.” (react-helmet-async).

Do not add any other text, earnings claims, rankings or badges. When finished, list any [placeholder] still visible.
```

Check after:
- [ ] Open /afiliados in mobile view: the navy top section shows the H1 '...receba 40% de comissão' and the orange button with navy text.
- [ ] '40% de comissão' is bold, and the two bracketed 'confirme...' notes are highlighted yellow. Replace them after checking your EscalePay panel.
- [ ] The rules box shows all 7 rules, including 'Inclua sempre a frase: ...' with its single quotes intact.
- [ ] The materials card lists 11 items.
- [ ] The affiliate button opens WhatsApp ('Olá! Quero ser afiliado do Kit Turno 15.') while ESCALEPAY_AFFILIATE_URL is empty. After you add the link, it should open EscalePay.
- [ ] There is no sticky buy bar on this page, and no income examples or 'ganhe X por mês' text appeared.

## Step 6 · Legal pages (/privacidade, /termos) + /anti-burla

Goal: Add simple, honest Portuguese privacy and terms pages that include the full list of reviewed disclaimers, plus a small free-checklist page so the footer's /anti-burla link is never broken.

```text
BUILD THREE PAGES: '/privacidade', '/termos' and '/anti-burla' for Kit Turno 15.

CONTEXT (in case anything is missing): Portuguese (Mozambique) site. Colours: navy #0B2545, orange #F28C28 (buttons with NAVY bold text), soft orange #FFF4E8, concrete #F4F5F7, ink #1B2430, muted #5B6573, line #D9DEE5. Fonts Barlow (headings) and Source Sans 3 (body, min 16px). Reuse src/config.ts, Layout, RichText (bold with **, paragraphs on blank lines, [brackets] highlighted yellow), CheckoutButton and whatsappLink. If any are missing, create them. No emojis. On these routes: normal header, NO sticky buy bar, WhatsApp floating button stays.

COPY RULES: Text between “ and ” is exact copy: copy it character for character into src/content/legalCopy.ts and render from there. Do not translate, shorten or 'fix' anything. {CONFIG_NAME} = insert the value from src/config.ts. Add to src/config.ts: export const LEGAL_LAST_UPDATED = '[data de publicação]';

LEGAL LAYOUT (both legal pages): white background, max-width 720px, py-12, H1 navy, then “Última actualização: {LEGAL_LAST_UPDATED}” in muted 14px, then numbered H2 sections (20px Barlow 700) with 17px paragraphs and bullet lists. Add a small table of contents at the top with anchor links to each H2. At the end: a link “Voltar ao início” → '/'.

=== PAGE '/privacidade' ===
H1: “Política de Privacidade”
H2 “1. Quem somos” / “O Kit Turno 15 é um produto digital independente de aprendizagem de inglês, criado e gerido por {BUSINESS_NAME}. Para qualquer questão sobre os seus dados, fale connosco no WhatsApp de suporte: {WHATSAPP_DISPLAY}.”
H2 “2. Que dados recolhemos” / bullets:
- “**Dados de compra:** nome, número de telemóvel e email que preenche na página de pagamento da EscalePay. Os pagamentos por M-Pesa ou e-Mola são processados pela EscalePay. Nós não vemos nem guardamos o seu PIN.”
- “**Conversas no WhatsApp:** o seu número e as mensagens que nos envia.”
- “**Grupo de Prática no WhatsApp:** o seu número de telemóvel fica visível para os outros membros do grupo.”
- “**Serviços de revisão de CV:** as informações sobre o seu percurso que nos envia (escola, cursos, experiência, carta de condução, função que procura).”
- “**Dados de navegação:** se estiverem activas ferramentas de medição de anúncios (Meta Pixel ou TikTok Pixel), estas podem registar visitas e cliques nesta página através de cookies.”
H2 “3. O que nunca pedimos” / “Não pedimos o número do BI nem o NUIT. Nunca pedimos o seu PIN do M-Pesa ou do e-Mola. Nunca pedimos dinheiro para vagas de emprego.”
H2 “4. Para que usamos os seus dados” / bullets: “Entregar o produto e dar acesso ao kit e ao grupo de prática.” “Responder às suas dúvidas e pedidos de suporte.” “Fazer o seu CV e a sua carta, se comprar um serviço de revisão.” “Enviar dicas de inglês de trabalho, só se responder 'SIM'. Para parar, basta escrever 'SAIR'.” “Medir o funcionamento desta página e dos anúncios.”
H2 “5. Com quem partilhamos” / “Não vendemos os seus dados. Os dados são tratados pelas plataformas que usamos para funcionar: a EscalePay (pagamentos e acesso), o WhatsApp (mensagens e grupo de prática) e, se estiverem activas, a Meta e o TikTok (medição de anúncios). Cada uma tem a sua própria política de privacidade.”
H2 “6. Quanto tempo guardamos” / “CVs e dados de formulários dos serviços de revisão são apagados 30 dias depois da entrega. Os restantes contactos são guardados enquanto for nosso cliente ou até pedir a eliminação.”
H2 “7. Os seus direitos” / “Pode pedir a qualquer momento para ver, corrigir ou apagar os seus dados, e para deixar de receber mensagens. Basta enviar mensagem para o WhatsApp de suporte: {WHATSAPP_DISPLAY}. Respondo {SUPPORT_HOURS}.”
H2 “8. Alterações” / “Se mudarmos esta política, actualizamos esta página e a data no topo.”

=== PAGE '/termos' ===
H1: “Termos de Uso”
H2 “1. O produto” / “O Kit Turno 15 é um produto digital de aprendizagem de inglês e preparação de documentos: guia em PDF, cartões de vocabulário, modelos de CV e de carta, banco de perguntas de entrevista e bónus, incluindo um Grupo de Prática no WhatsApp com turmas em datas fixas.”
H2 “2. Compra e pagamento” / “As compras são feitas na página de pagamento da EscalePay, por M-Pesa ou e-Mola. O preço é o indicado na página no momento da compra. Os Áudios de Pronúncia Turno 15 (147 MT) são um extra opcional. Nunca envie dinheiro para números pessoais em nome deste produto.”
H2 “3. Acesso” / “Depois do pagamento, o acesso é entregue através da EscalePay [confirme e escreva o método real]. Se tiver algum problema, fale connosco no WhatsApp de suporte: {WHATSAPP_DISPLAY}.”
H2 “4. Uso pessoal” / “A compra dá-lhe uma licença de uso pessoal. Não é permitido revender, partilhar, copiar ou publicar o conteúdo do kit, no todo ou em parte, sem autorização escrita. O Checklist Anti-Burla pode ser partilhado livremente com a sua família.”
H2 “5. Garantia e reembolso” / “Todos os produtos têm garantia de reembolso de 7 dias, de acordo com a política da EscalePay. Peça o reembolso dentro desse prazo [confirme no seu painel o processo exacto e descreva-o aqui numa frase].”
H2 “6. Grupo de Prática e afiliados” / “No Grupo de Prática pedimos respeito. Quem publicar vagas, pedidos de dinheiro, links ou publicidade é removido. Os afiliados têm de cumprir as Regras de Divulgação da página Programa de Afiliados. Quem prometer emprego, vagas ou rendimentos é removido do programa.”
H2 “7. Avisos importantes” / render this list exactly (bullets, 16px):
- “O Kit Turno 15 é um produto digital de aprendizagem de inglês e preparação de documentos. Não garante emprego, entrevistas, contratação, salário nem qualquer rendimento.”
- “Os resultados dependem do esforço, da prática diária e da situação de cada pessoa. 30 dias de 15 minutos por dia dão uma base de inglês de trabalho, não fluência.”
- “Produto independente: não tem ligação, patrocínio nem aprovação da TotalEnergies, Mozambique LNG, ExxonMobil, Rovuma LNG, ENH, INP, de nenhuma empresa mineira, empreiteiro, projecto ou entidade do governo. Os nomes de empresas e projectos são referidos apenas como informação pública.”
- “Não somos agência de recrutamento. Não vendemos, prometemos nem facilitamos o acesso a vagas, e nunca pedimos dinheiro para conseguir emprego.”
- “O vocabulário de segurança (HSE) serve apenas para aprender inglês. Não substitui formações oficiais de segurança, induções no local de trabalho, exames médicos nem certificações profissionais. Os procedimentos do seu empregador vêm sempre primeiro.”
- “O 'certificado de conclusão do kit' é um registo pessoal de progresso. Não é um certificado oficial nem acreditado.”
- “Garantia de reembolso de 7 dias para todos os produtos (kit, Áudios de Pronúncia Turno 15, Revisão Pessoal: CV + Carta em Inglês e Revisão Rápida do CV), de acordo com a política da EscalePay.”
- “Os serviços Revisão Pessoal: CV + Carta em Inglês e Revisão Rápida do CV melhoram a apresentação dos seus documentos, mas não garantem emprego. Nunca inventamos experiência, certificados ou datas. Confirme todos os factos antes de enviar o seu CV.”
- “Privacidade: recolhemos apenas os dados necessários para entregar o produto e os serviços. Não pedimos o número do BI nem o NUIT. CVs e dados de formulários são apagados 30 dias depois da entrega. Pode pedir a eliminação dos seus dados a qualquer momento pelo contacto de suporte.”
- “Grupo de Prática no WhatsApp: o seu número de telemóvel fica visível para os outros membros. Membros que publiquem vagas, pedidos de dinheiro ou spam são removidos.”
- “Depoimentos, quando existirem, são reais, voluntários, publicados com autorização escrita e referem-se ao produto. Não representam resultados típicos nem garantem resultados.”
- “As datas e os lugares limitados indicados nesta página são reais: datas de início das turmas e capacidade semanal dos serviços de revisão. Não usamos contadores falsos.”
- (IF SHOW_AI_DISCLOSURE) “O conteúdo foi preparado com o apoio de ferramentas de inteligência artificial e revisto pelo criador.”
- “Os pagamentos são processados pela EscalePay através de M-Pesa ou e-Mola. Nunca envie dinheiro para números pessoais em nome deste produto.”
H2 “8. Alterações e contacto” / “Podemos actualizar estes termos. A data no topo indica a última versão. Para qualquer questão, fale connosco no WhatsApp de suporte: {WHATSAPP_DISPLAY}.”

=== PAGE '/anti-burla' ===
If SHOW_ANTIBURLA_PAGE is false, redirect this route to '/'. Otherwise: background concrete, centred card (white, 12px radius, max 560px, 24px padding), lucide ShieldCheck icon in navy (56px).
H1: “Checklist Anti-Burla grátis: 12 Sinais de Vaga Falsa”
Paragraph: “Os 12 sinais de vaga falsa numa página, para guardar no telemóvel e partilhar com a família.”
Box (#FFF4E8, navy left border), RichText: “**A regra de ouro:** desconfie de qualquer pedido de dinheiro para conseguir emprego.”
Primary orange button: “Receber o checklist no WhatsApp” → whatsappLink('Olá! Quero receber o Checklist Anti-Burla grátis.'), new tab with rel='noopener noreferrer', calling trackContact().
Small muted text: “Enviamos o checklist pelo WhatsApp. Não pedimos dinheiro nem dados pessoais.”
Navy underlined link: “Conhecer o Kit Turno 15” → '/'.
Small muted line at the bottom: “Produto independente de preparação. Não garante emprego.”

Titles (react-helmet-async): “Política de Privacidade | Kit Turno 15”, “Termos de Uso | Kit Turno 15”, “Checklist Anti-Burla grátis | Kit Turno 15”. When finished, list any [placeholder] still visible.
```

Check after:
- [ ] Open /privacidade: 8 numbered sections, the table of contents links jump correctly, and 'Não pedimos o número do BI nem o NUIT' appears.
- [ ] Open /termos: section 7 'Avisos importantes' lists 14 items (13 if SHOW_AI_DISCLOSURE is false), with company names spelled exactly as in the copy.
- [ ] 'Última actualização: [data de publicação]' is highlighted on both legal pages. Set LEGAL_LAST_UPDATED before publishing.
- [ ] Open /anti-burla: the button opens WhatsApp with 'Olá! Quero receber o Checklist Anti-Burla grátis.' Make sure you have the checklist image ready to send.
- [ ] The footer links Política de Privacidade, Termos de Uso, Programa de Afiliados and Checklist Anti-Burla grátis all open the right pages, and none of them shows 'Página não encontrada'.
- [ ] The text is plain and readable at 360px (no tiny legal font below 16px in the body).

## Step 7 · SEO, performance, analytics and accessibility (all routes)

Goal: Set the Portuguese SEO title and description, Open Graph and WhatsApp preview, per-route titles and noindex, optional Meta/TikTok pixels with honest events, image and font optimisation, and an accessibility pass.

```text
SEO, SHARING, ANALYTICS, PERFORMANCE AND ACCESSIBILITY PASS for the Kit Turno 15 site. Do NOT change any visible Portuguese copy or the layout in this message.

1) index.html (the static head is what Facebook, WhatsApp and TikTok read when a link is shared, so it must be correct even without JavaScript):
- <html lang='pt'>
- <title>Kit Turno 15: Inglês para o Gás e a Mineração | 697 MT</title>
- <meta name='description' content='Inglês de segurança, terreno e entrevista no telemóvel, 15 min por dia. Modelos de CV e carta, guia anti-burla e grupo de prática. M-Pesa ou e-Mola.'>
- Open Graph: og:type 'website', og:locale 'pt_PT', og:site_name 'Kit Turno 15', og:title (same as the title), og:description (same as the description), og:url = SITE_URL value, og:image = SITE_URL + '/og-image.jpg' (absolute URL), og:image:width 1200, og:image:height 630, og:image:alt 'Kit Turno 15: Inglês para o Gás e a Mineração'.
- Twitter: twitter:card 'summary_large_image', plus the same title, description and image.
- <meta name='theme-color' content='#0B2545'>, <link rel='icon' href='/favicon.png' type='image/png'>, <link rel='apple-touch-icon' href='/favicon.png'>.
- REMOVE every default Lovable meta tag (author 'Lovable', 'Lovable Generated Project' descriptions, the default lovable OG image and twitter:site) and the default favicon.
- Add a placeholder file note: if public/og-image.jpg does not exist yet, tell me in your reply. Do not generate a fake one with logos.
- Keep the Google Fonts link with preconnect to fonts.googleapis.com and fonts.gstatic.com (crossorigin), only Barlow 600/700/800 and Source Sans 3 400/600/700, with display=swap.

2) Per-route head with react-helmet-async (HelmetProvider in main.tsx): '/' uses the title and description above plus <link rel='canonical' href={SITE_URL + '/'}>; '/afiliados', '/privacidade', '/termos', '/anti-burla' keep the titles already set and get canonical links; '/obrigado' and '/oferta-especial' get <meta name='robots' content='noindex, nofollow'>.

3) public/robots.txt: 'User-agent: *', 'Allow: /', and 'Sitemap: ' + SITE_URL + '/sitemap.xml'. public/sitemap.xml listing '/', '/afiliados', '/anti-burla', '/privacidade', '/termos' using the SITE_URL value. Add a comment in config that SITE_URL must match the published URL.

4) Structured data on '/' only: a JSON-LD script of type Product with name 'Kit Turno 15: Inglês para o Gás e a Mineração', description (the meta description), brand name 'Kit Turno 15', and offers { '@type': 'Offer', price: '697', priceCurrency: 'MZN', availability: 'https://schema.org/InStock', url: SITE_URL }. NO aggregateRating and NO review fields.

5) ANALYTICS in src/lib/analytics.ts (replace the empty stubs):
- Add to config: export const FIRE_PURCHASE_ON_THANKYOU = false; // set true ONLY if EscalePay redirects to /obrigado exclusively after a confirmed payment
- initAnalytics(): if META_PIXEL_ID is not empty, inject the standard Meta Pixel base code and fbq('init', META_PIXEL_ID). If TIKTOK_PIXEL_ID is not empty, inject the standard TikTok pixel base code and ttq.load(TIKTOK_PIXEL_ID). If both are empty, do nothing (no scripts loaded). Load the scripts after window 'load' so they never block the first paint. Call initAnalytics() once in main.tsx.
- Track a PageView (fbq('track','PageView') and ttq.page()) on every route change, using a small RouteTracker component with useLocation.
- On '/', fire ViewContent once: { content_name: 'Kit Turno 15', value: 697, currency: 'MZN' }.
- trackCheckout(): InitiateCheckout with { content_name: 'Kit Turno 15', value: 697, currency: 'MZN' } on Meta, and 'InitiateCheckout' on TikTok with the same value and currency.
- trackUpsellClick(): InitiateCheckout with { content_name: 'Revisão Pessoal: CV + Carta em Inglês', value: 1497, currency: 'MZN' }.
- trackContact(): 'Contact' on Meta and 'Contact' on TikTok.
- Purchase: fire it ONLY when FIRE_PURCHASE_ON_THANKYOU is true, on '/obrigado', once per browser session (guard with sessionStorage key 'kt15_purchase_sent'), with value 697 and currency MZN. Never fire Purchase anywhere else.
- Every function must fail silently (try/catch, check that window.fbq or window.ttq exists). Add the TypeScript global declarations.

6) IMAGES AND PERFORMANCE:
- Every <img> must have width and height attributes and Portuguese alt text. All images below the hero use loading='lazy' and decoding='async'. Only the hero image uses loading='eager' and fetchpriority='high'.
- Images are referenced as .webp from /public: hero-telemovel.webp (target under 80 KB), cartao-diario.webp (under 60 KB), criador.webp (under 30 KB). If an image file is missing, render the fallback already built and never a broken image icon (use an onError handler that hides the image).
- No video embeds, no external widgets, no animation libraries. Remove unused heavy dependencies if any were added. Keep all icons from lucide-react (tree-shaken imports).
- Make sure the page has no layout shift when fonts load (font-display swap, fixed image sizes).

7) ACCESSIBILITY:
- Exactly one H1 per route; H2/H3 in order, no skipped levels.
- Every icon-only element has an aria-label (WhatsApp button: 'Falar no WhatsApp') and decorative icons have aria-hidden='true'.
- Colour contrast: body text ink on white; on navy use white or #C9D2DE only; orange buttons always have navy text; never orange text on white.
- Visible 3px orange focus outline on every link, button and <summary>.
- Tap targets at least 44x44px, including the footer links and the NO link on the upsell page.
- The <details> accordions work with the keyboard (Enter/Space) and their summaries have list-style none with a custom chevron.
- Respect prefers-reduced-motion everywhere (no smooth scroll, no sliding sticky bar animation).
- External links that open in a new tab have rel='noopener noreferrer'.

Reply with a checklist of what you changed and anything I still need to upload (og-image.jpg, favicon.png, images).
```

Check after:
- [ ] Open index.html in Code view (or ask Lovable to show it): the <title> is exactly 'Kit Turno 15: Inglês para o Gás e a Mineração | 697 MT' and there is no word 'Lovable' left in the meta tags.
- [ ] og:image is an absolute URL (starting with https://) ending in /og-image.jpg. Upload your 1200x630 og-image.jpg and favicon.png to the project's public folder (drag them into the chat or use the file upload) if you haven't.
- [ ] With META_PIXEL_ID and TIKTOK_PIXEL_ID empty, the page still loads normally and no pixel scripts appear.
- [ ] Hover the buy buttons: they still point to the checkout placeholder and the page copy is unchanged (spot-check the hero and the FAQ).
- [ ] Press Tab from the top of the page: first 'Saltar para o conteúdo' appears, then each link and button shows an orange outline.
- [ ] /obrigado and /oferta-especial still look the same as before (only their head tags changed).

## Step 8 · Final polish + mobile QA (all routes)

Goal: Run a careful check of the whole site at real phone widths, fix layout, spacing and behaviour bugs without changing the copy, and get a written report of the remaining placeholders and config values to fill before publishing.

```text
FINAL POLISH AND MOBILE QA for the whole Kit Turno 15 site. Fix problems only. Do NOT rewrite, translate, shorten or reorder any Portuguese text, do NOT add new sections, text, badges or features, and do NOT change the colours or fonts.

Check and fix each item at widths 360px, 390px, 768px and 1280px, on every route ('/', '/obrigado', '/oferta-especial', '/afiliados', '/privacidade', '/termos', '/anti-burla' and a 404 route):
1. No horizontal scrolling anywhere (watch long words like 'Situação, Acção, Resultado', the phone mockup, the stripe, the tables of contents and long links). Use min-w-0, break-words and max-w-full where needed.
2. Side padding is 16px on mobile on every section. Vertical spacing is consistent (56px between sections on mobile, 80px on desktop), with no double gaps or sections touching each other.
3. Typography: body text never smaller than 16px (only microcopy and the footer may be 13-14px). The H1 fits in at most 5 lines at 360px. No orphaned single words on buttons where avoidable.
4. Buttons: every orange button has navy bold text, a minimum height of 52px and full width on mobile. Button labels never overflow or wrap into 3 lines. Every buy button on '/' links to ESCALEPAY_CHECKOUT_URL, every upsell YES to ESCALEPAY_UPSELL_URL, the NO link to '/obrigado?upsell=nao', and all WhatsApp links use whatsappLink(). No '#' or empty hrefs.
5. Sticky mobile bar: it appears only on '/' and only below md, appears after the hero, hides at #oferta and at the footer, never covers footer links, and the WhatsApp button never overlaps it (it sits at 96px from the bottom when the bar is visible). On iPhone-style screens it respects the safe-area inset.
6. Accordions: the 10 modules and 12 FAQ items are all closed by default, open and close on tap, have chevrons that rotate, and anchor links to #modulos and #faq land with the heading visible (scroll-margin-top).
7. Switches: test in code that each flag in src/config.ts works both ways without errors (SHOW_STORY, SHOW_TESTIMONIALS with an empty array, SHOW_LAUNCH_PRICE, SHOW_PRICE_COMPARISON, SHOW_COHORT_LINE, SHOW_ACESSO_IMEDIATO, SHOW_AI_DISCLOSURE, SHOW_REVIEWER_LINE, SHOW_AFFILIATE_MANUAL_APPROVAL, SHOW_ANTIBURLA_PAGE). Then set them back to their current values.
8. Images: no broken image icons. Missing files fall back gracefully. Images keep their aspect ratio and don't cause layout shift.
9. The header on mobile shows the wordmark and the compact 'Comprar' button on one line at 360px (hidden on /obrigado and /oferta-especial).
10. The 404 page is in Portuguese and its button returns to '/'.
11. No console errors or React key warnings. No unused imports causing build warnings.
12. Desktop (1280px): the hero is two columns, the 'Para quem' cards sit side by side, the bonus cards are 2x2, the offer card is centred at max 480px, and line lengths stay under about 75 characters.

Then reply with a REPORT (no code changes for this part):
A) the list of fixes you made;
B) every visible [bracket] placeholder still on the site, grouped by page and section;
C) every value in src/config.ts that still contains 'SUBSTITUIR', 'XXXXXXXXX' or a '[' placeholder;
D) the image files I still need to upload to /public.
```

Check after:
- [ ] Read Lovable's report: section B (remaining placeholders) and C (config values) are your to-do list before publishing. Keep it.
- [ ] In the preview's mobile view, scroll every page at 360px: no sideways scrolling, no text touching the screen edge, and no overlapping buttons.
- [ ] Re-check 3 random paragraphs against the copy to confirm nothing was 'polished' or reworded.
- [ ] Tap every button and link on the sales page once: checkout placeholders, WhatsApp, the #oferta text link and the footer links.
- [ ] Open the preview on your own phone too (copy the preview link): check the sticky bar and WhatsApp button with your thumb, and check the load speed on mobile data.

## Fix prompts

### The layout is broken on mobile (sideways scrolling, text cut off, columns squeezed)

```text
Fix mobile layout only, without changing any text, colours or fonts. At 360px and 390px width there must be no horizontal scroll on any page. Find the elements wider than the screen (check the hero phone mockup, SafetyStripe, the 'Para quem' cards, the offer card, the timeline, long words in the accordions and long footer links) and fix them with max-w-full, min-w-0, break-words, flex-wrap and single-column stacking below md. Keep 16px side padding on every section. Report which elements caused the overflow.
```

### Wrong colours (white text on orange buttons, orange text on white, the default shadcn blue or black theme showing)

```text
Fix the colours only, without changing any text or layout. Apply these tokens everywhere: navy #0B2545, deep navy #071A33 (footer), orange #F28C28 (buttons), orange hover #E07B16, soft orange #FFF4E8, concrete #F4F5F7, ink #1B2430 (body text), muted #5B6573, mist #C9D2DE (small text on navy), line #D9DEE5, WhatsApp button #1A9E4B. Every orange button must have NAVY #0B2545 bold text, never white. Never use orange as a text colour on white. Replace any leftover shadcn default primary colour (blue, black or slate) in the CSS variables with navy, and make sure there is no dark mode switch. List every component you changed.
```

### A buy, upsell or WhatsApp button doesn't link, links to '#', opens the wrong URL or opens a blank tab

```text
Audit and fix every link, without changing any visible text. Rules: every buy button on '/' and the header 'Comprar' buttons use href={ESCALEPAY_CHECKOUT_URL} from src/config.ts and open in the same tab. Every 'Sim, quero a Revisão Pessoal por 1.497 MT' button uses href={ESCALEPAY_UPSELL_URL}. The upsell NO link goes to '/obrigado?upsell=nao'. All WhatsApp links use whatsappLink() with WHATSAPP_NUMBER (digits only, format 258XXXXXXXXX) and open in a new tab with rel='noopener noreferrer'. The affiliate button uses ESCALEPAY_AFFILIATE_URL or the WhatsApp fallback. Text links use '#oferta' and '#modulos'. Remove any hardcoded URL, empty href or href='#'. Also check the URL values in src/config.ts have no spaces or quotes inside. Reply with a table: button text → final href.
```

### Lovable changed, translated, shortened or 'corrected' the Portuguese copy

```text
You changed some Portuguese text. Restore it EXACTLY. Do not rewrite, translate, shorten, re-punctuate or modernise any spelling (keep 'acção', 'projecto', 'correctamente', 'directas', 'Bónus', '12ª classe', '1.497 MT' and the · separators). The correct text for the section [NAME OF SECTION] is below, between “ and ”. Replace the matching constants in src/content/*.ts with it character for character and change nothing else: “[PASTE HERE THE EXACT TEXT OF THAT SECTION FROM STEP 2, 3, 4, 5 OR 6 OF THIS PACK]”. Then confirm which constants you replaced.
```

### The page is slow on mobile data or images are heavy or blurry

```text
Optimise performance without changing text or layout. 1) Every image must be WebP from /public with explicit width and height: hero-telemovel.webp under 80 KB, cartao-diario.webp under 60 KB, criador.webp under 30 KB. If any image is PNG/JPG or larger, tell me its file size so I can re-export it. 2) Only the hero image is loading='eager' with fetchpriority='high'; all others are loading='lazy' with decoding='async'. 3) Load only Barlow 600/700/800 and Source Sans 3 400/600/700 with display=swap and preconnect. 4) Pixel scripts load only after window 'load' and only if their IDs are set. 5) Remove any animation library, video embed or unused heavy dependency. 6) Make sure nothing causes layout shift. Report the estimated size of each image and script.
```

### The sticky buy bar or WhatsApp button covers content, overlaps each other, or shows on the wrong pages

```text
Fix only the floating elements. StickyMobileCTA: render only on route '/' and only below the md breakpoint. Hidden while #hero is visible, visible after it, hidden again while #oferta or the <footer> is visible (IntersectionObserver). Add env(safe-area-inset-bottom) padding. The footer needs at least 112px of bottom padding on mobile. WhatsAppButton: hidden on '/oferta-especial'; at bottom 16px normally and bottom 96px while the sticky bar is visible, so they never overlap. Neither may cover the upsell NO link, a FAQ item or the footer links. No animation under prefers-reduced-motion. Do not change any text.
```

### The modules or FAQ accordion is open by default, won't open, or Lovable replaced it with a different component

```text
Rebuild the two accordions (Módulos: 10 items, Perguntas frequentes: 12 items) with native HTML <details>/<summary>, not a JavaScript accordion. All items closed by default, summary min-height 56px, list-style none with a lucide ChevronDown that rotates 180 degrees when open (no rotation under prefers-reduced-motion), a visible orange focus outline, and 1px #D9DEE5 dividers. Module summaries show the orange pill tag ('Módulo 0'... with navy text) plus the bold navy title. Use the existing text constants from src/content/salesCopy.ts without changing a single character, and keep the section ids 'modulos' and 'faq'.
```

### Lovable stopped halfway (missing sections) or a page shows 'Página não encontrada'

```text
Continue the previous task exactly as specified, without changing what is already built. First, list which of these section ids exist on '/': hero, problema, historia, solucao, metodo, modulos, bonus, como-funciona, para-quem, oferta, garantia, criador, depoimentos, faq, final. Then build ONLY the missing ones, using the exact Portuguese copy from my earlier message (copy it character for character into src/content/salesCopy.ts). Also confirm these routes exist in the router and render their page components: '/', '/obrigado', '/oferta-especial', '/afiliados', '/privacidade', '/termos', '/anti-burla', plus the Portuguese 404. If a route is missing, add it. Reply with the final list of sections and routes.
```

