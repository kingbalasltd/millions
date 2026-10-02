# 24-hour sprint plans

| Plan | Files |
|---|---|
| **High-ticket** (main): bilingual company profiles + websites for Mozambican suppliers, 25,000–65,000 MT per sale | `high-ticket/high-ticket-sprint.pdf`, `high-ticket/scripts-high-ticket.md` |
| Portfolio demo (fictional company) | `high-ticket/demo-site/` (website + `company-profile.pdf`), zipped as `high-ticket/demo-site.zip` |
| Fast cash (small jobs: CVs, WhatsApp setups, posts) | `24h-cash-sprint.pdf`, `scripts-copy-paste.md` |

Rebuild the PDFs after editing: `python3 build_high_ticket.py`, `python3 build_samples.py`, `python3 build_plan.py` (needs `reportlab`).

## Mentorship + products

| What | Files |
|---|---|
| **Mentorship ebook** "From Zero to #1" (12 chapters, challenges, quizzes) | `ebook/from-zero-to-number-one.pdf` (`python3 build_ebook.py`) |
| EscalePay verdict + 30-day #1 plan | `high-ticket/escalepay-and-number-one.pdf` |
| **Product A**: Inglês para o Gás e a Mineração (Kit Turno 15) | `products/A-ingles-gas/` launch pack PDF, `sales-copy.md`, `lovable-prompts.md` |
| **Product B**: WhatsApp que Vende | `products/B-whatsapp-vende/` launch pack PDF, `sales-copy.md`, `lovable-prompts.md` |

Rebuild product packs from `products/products.json` with `python3 build_products.py`.
