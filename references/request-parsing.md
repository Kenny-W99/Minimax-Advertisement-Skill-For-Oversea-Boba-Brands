# Stage 0 · Understanding the request

The brief (`request_brief.json`) is the single source of truth for the whole run. Write it first, then have every later stage read it instead of re-reading the user's message. That is what keeps a 30-minute pipeline from contradicting itself (a grape drink in the prompts but a mango in the slogan, a second product sneaking into the hero shot).

## Fields and their sources

Every field carries `value` and `source` ∈ `user_text | user_image | web | default` (shape in `schemas.md`).

| Field | Notes |
|---|---|
| `brand` | as the user wrote it, plus the official name once research confirms it |
| `product` | exactly one product; see input modes |
| `market`, `language` | default from brand's main market; on-screen text language follows the market |
| `platform` | default `tiktok_reels_shorts` (9:16) |
| `duration_target` | default by structure: 2-act 12 s, 3-act 22 s |
| `story_source` | `agent` or `user` |
| `holiday` | detected holiday or `none` |
| `style_hint`, `music_hint` | only if the user expressed one |
| `must_include`, `must_avoid` | anything explicit from the user |
| `notes` | your interpretation of anything ambiguous, and the choice you made |

## Input modes

**Brand + product** ("给某品牌的某款奶茶做广告", "Gong Cha brown sugar milk tea") — lock that product; research its look.

**Brand only** ("make an ad for Mixue") — research the current menu and pick one product: prefer the signature or currently promoted item that has clear official photos and a visual hook. Lock it in the brief immediately; no later stage may change it or show a second product. Say in the report which product you chose and why.

**Image** (product photo, cup, storefront, menu, poster, screenshot)
1. Look first: logo, brand name, text on the cup or sleeve, cup shape, layer colors, toppings.
2. Verify online with what you saw (brand + visible words + "menu").
3. The user's image becomes the **primary product reference** (ranked above web photos).
4. Continue exactly as brand + product.
5. If the brand cannot be identified, treat it as an unbranded product: lock its look from the image, derive the style from the product's own colors and packaging, and say so in the report.

**User storyline** ("a cat steals the drink and…")
1. Keep the user's characters, event order and emotional turns as written; do not swap in your own ideas.
2. Translate it into acts → 5 s segments → one main action per segment; add segments if needed, keep ≤ 30 s unless asked.
3. All quality rules still apply (product lock, mitten hands unless the story needs a specific creature, no generated text, physical logic, alive acting).
4. Where the story conflicts with a rule, implement the closest safe version and list the change in the report. Example: "pinches a pearl between two fingers" → "scoops a pearl up in a mitten hand".
5. Add the product hero shot at the end unless the user said not to.
6. Fill only what the user left out (e.g. they wrote the beginning) with your own beats, in the same style and causality.

Modes combine (image + storyline is common).

## Conflicts

User text > user image > web > default. Example: the text says grape, the photo shows a mango cup → make the grape ad and note the mismatch in the report.

## Holiday detection

Scan the user's message (any language) against the trigger list in `holidays.md`. A match sets `holiday` and adds that holiday's elements to the agent's own story — it never replaces the story.

## Final consistency pass (run just before finishing)

- Every prompt, keyframe, slogan and product name refers to the locked product.
- The flavor in the slogan and end card matches `product_spec`.
- One character spec from start to end.
- Holiday elements (if any) match the detected holiday.
- User-story mode: every beat the user wrote has a shot.

Fix and re-render anything inconsistent. Put the brief at the top of `report.md` so the user sees at a glance how you understood them.
