# Stage 1 · Brand and product research

Goal: know the brand's visual identity and the product's exact appearance well enough that a fan would recognise both. Everything you can't verify stays `unknown`; pick a safe default and say so. Never invent facts about a real product (ingredients, prices, claims).

## What to find

| Item | Why | Where to look |
|---|---|---|
| **Product appearance**: cup type (clear / frosted / paper), shape (straight / tapered / bowl), lid (flat / dome / sealed film), straw, liquid layers top→bottom with colors, foam / cheese cap / cream, toppings and where they sit, cup print or sleeve, typical size | Product lock — the product must never drift | official site & menu, official Instagram / Xiaohongshu / Weibo / WeChat posts, delivery apps (Meituan, Uber Eats, Grab), recent review photos |
| **Official product photos** (2–4, clean, front-ish) | Hero-shot base, reference for every product keyframe | same; save locally with source URL |
| **Product story & hook material**: name meaning, key ingredient, origin, texture, aroma, limited edition / season | The creative hook (Stage 3) | product launch posts, press, menu descriptions |
| **Logo** file and **logo style** (single line / geometric / mascot / wordmark / calligraphy / hand-drawn), stroke weight, corner style | Drives the art style; overlaid on the end card | official site header/footer, press kit, app icon, high-res social avatar |
| **Palette**: primary, secondary, accent (HEX) | Color roles | logo, packaging, site CSS, store photos — sample colors from images if no guide exists |
| **Typography**: official / custom typeface for headings and body; or its look (serif / rounded sans / calligraphy / handwritten) | End-card text | site CSS (`font-family`), packaging photos, brand guideline PDFs; if custom, find the closest open-license (OFL) match |
| **Voice & slogans** (playful / premium / poetic / bold / cozy), existing taglines and their language | Copy tone | site, ads, captions |
| **Mascot / IP** | If present it becomes the hero character | site, merchandise |
| **Culture & place cues**: home city, heritage, recurring motifs (e.g. classical poetry, ink painting, a city skyline) | Story and style flavour | about page, store design |
| **Existing ads** (brand and 1–2 competitors) | Avoid copying, avoid clichés | social video posts |

## Search patterns

Run several in parallel; mix languages for Chinese and Asian brands.

- `"<brand>" "<product>"` · `<brand> <product> 图片` · `<brand> <product> 小红书` · `<brand> menu <product>`
- `<brand> logo` · `<brand> brand guidelines` · `<brand> 品牌 字体` · `<brand> 官网`
- `<brand> 新品 <product> 上新` (launch posts carry the best descriptions)

Read official pages before third-party ones. Record every source URL. Some pages (press sites, Weibo, Xiaohongshu) block fetch tools with 403 or a login wall. Use the search snippets and image results instead, and note in the brief which facts came only from snippets. Regional sites of the same brand (e.g. Malaysia, Singapore) often have cleaner product photos than the home market, but their cups may differ, so say which region your reference shows.

## Outputs

`brand_profile.json` and `product_spec.json` (shapes in `schemas.md`). In `product_spec`, write **one canonical English sentence** describing the product's look. That exact sentence is pasted into every prompt that shows the product, so it must be complete and concrete. Example: *"a tall clear plastic cup with a flat sealed lid and a wide straw, a creamy pale-ivory milk tea layer under a thick white foam cap, with a small printed orchid motif on the cup"*.

If official photos of the product cannot be found at all, say so in the report, describe the product from text sources, and keep the hero shot simpler (fewer claims about details you could not see).
