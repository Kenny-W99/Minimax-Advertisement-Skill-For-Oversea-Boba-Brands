# Stage 7 · End card, typography and finishing

The last 3–5 seconds sell the product. The layout rules are fixed; the content (fonts, colors, copy, accents) comes from the brand.

## Fixed rules

- The product is the absolute hero, with generous empty space around it.
- All text and the logo are added in post by `scripts/finish.py`. The video model never draws text.
- Text animates in (below); nothing just pops on.
- Hold the finished end card for at least 2 s.
- A gentle camera keeps the frame alive. After the hero shot settles, `finish.py` slowly pulls back (default to 74 %) with feathered edges into the background color, then drifts a slow push-in. A fully frozen frame reads as "video ended".

## Brand-driven content

| Element | Rule |
|---|---|
| Headline / slogan | Write a new line in the brand's own voice and the market's language, ≤ 8 words per line, 1–2 lines. Use the brand's tagline only if the user wants it. Don't reuse the example's "A little X brightens your day" pattern for other brands. |
| Headline font | Variable fonts (e.g. Google Fonts' Noto Serif SC) default to their lightest instance; set `"weight": 400` (or 300 for light) on the text spec. The brand's official typeface if it can be legally obtained; otherwise the closest open-license (OFL) font: rounded sans → Nunito / Quicksand; geometric → Poppins / Montserrat; elegant serif → Playfair Display / Cormorant; Chinese serif → Noto Serif SC / Source Han Serif; Chinese rounded → ZCOOL / LXGW WenKai. Download from Google Fonts or the font's GitHub release, and note the license in the report. |
| Weight & size | Regular or light, never heavy; cap height ≈ 4–4.5 % of frame width; ink a deep tone from the palette (not pure black on white). |
| Accent mark | Something that matches the style, drawn on in ~0.45 s: a hand-drawn wavy underline (doodle styles), a red seal stamp (Chinese classical), a thin rule line (premium). |
| Product name note | Optional handwritten or calligraphic product name next to the product, written letter by letter (≈12 letters/s) with slight per-letter jitter and a -4° to -6° tilt. For Chinese brands, `note.vertical: true` writes it top-to-bottom (columns right-to-left), which suits calligraphy. |
| Logo | The official logo file, small (≈18–24 % of frame width), bottom centre, fade in. `logo.y` is the logo's **top** edge; `logo.max_height` (fraction of frame height, default 0.08) keeps tall or square logos from running off the bottom. If there is no clean file, set the brand name in its typeface with wide tracking. |

## Motion recipe (built into finish.py)

- Headline lines fade in and rise 16 px, 0.6 s ease-out, staggered 0.15 s.
- Accent draws on 0.75 s after the headline starts.
- Product note starts writing at +1.0 s.
- Logo fades in at +0.3 s over 0.7 s.

## Finishing passes

- **Canvas color.** The end-card pull-back reveals canvas around the shrinking frame. Leave `background` unset and `finish.py` samples the last frame's edge color automatically. A mismatched color shows as a visible rectangle.
- **Pure white cleanup** (`"whites": true`) for white-background styles. Generated frames sit at ~250 grey, which looks dirty. Turn it off for colored or textured backgrounds.
- **Virtual camera** per segment (`"zoom": [z0, z1], "cy": [c0, c1], "ramp": s`) to frame a character that was generated too small. The value at the end of one segment must equal the value at the start of the next.
- **On twos** (`"on_twos": true`) gives a hand-drawn cadence. Optional; review it before keeping it.
- Loudness: two-pass normalisation to -16 LUFS, true peak -1.5 dB, 48 kHz AAC.

See `schemas.md § edit.json` for the full config.
