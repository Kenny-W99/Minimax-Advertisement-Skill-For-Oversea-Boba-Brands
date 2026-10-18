# Stage 2 · Visual system

## 1. Art style from brand DNA

The style should feel like the brand drew it. Start from the logo and packaging, then from voice and culture.

| Brand signal | Style direction (starting point, not a rule) |
|---|---|
| Single-line or minimal line logo | bold single-weight black line doodles on white; only the drink and its fruit in color |
| Mascot or IP character | the mascot itself as the hero, in the brand's own illustration style (2D or soft 3D) |
| Flat geometric marks, saturated blocks | flat vector motion graphics, bold color fields |
| Serif or minimal premium identity | realistic macro product cinematography, slow elegant motion |
| Classical Chinese, poetry, calligraphy | ink-wash (水墨) or gongbi (工笔) illustration, rice-paper texture, seal-red accents |
| Pastel, cute | soft clay / plush 3D look |
| Retro, handmade | paper collage, risograph grain |

Write the choice and the reasons into `style_guide.json`.

**Known-good (verified):** line-art doodle with mitten-hand bean character on white, color only on the drink and its fruit, the color "blooming" into the world after the first sip. Other directions are sound but less tested. Keep them simple (flat backgrounds, few objects) until they have been tested.

## 2. Color roles

- `background`, `line`, `accent` (= the product/fruit color), `brand` (primary brand color, mostly on the end card).
- Strong, reusable hook: **restraint first, color bloom after the product enters**. Early frames stay mostly neutral; the drink is the one saturated object; after the first sip its color spreads into the world. Adapt it to non-white styles (e.g. ink-wash: monochrome ink, then the drink's color washes in).
- Holiday colors are accents only; they never replace the brand palette.

## 3. Hero character → `character_spec`

- Derive from the logo or mascot (a line logo of a person → a simple line person; a mascot → that mascot).
- Default hands: **rounded mitten hands without fingers**, or, for costume styles, **hands hidden inside long sleeves** (worked well for a classical-lady character). This is the cheapest fix for the most common AI artifact. Only a mascot that canonically has fingers gets them, with the count fixed in the spec.
- Freeze: head/body proportion, line weight, eyes/mouth style, fill color ("plain pure white body, no clothes, no stripes, no patterns, no hair" for doodle styles — image-01 tends to add sweaters, stripes, hair and bows otherwise), accessories.
- A character is optional. A product-only concept (e.g. ingredients dancing) is fine if the story is stronger that way.

## 4. Style-lock sentence

One English sentence that fixes medium, line, background, shading and palette, e.g. *"Minimalist hand-drawn doodle, bold uniform black ink outline, pure white background, flat, no shading, only the drink and grapes in color."* Paste it verbatim into every image and video prompt. Do not paraphrase it later.

## 5. Keyframe staging rules (checked at Gate A)

Most "logic" failures are planted in the keyframe. Example: a backpack drawn overlapping the character's raised feet made the model treat them as one object, so the backpack moved every time the legs kicked.

1. **No overlapping silhouettes.** Clear white space between the character and every prop. Only an object the character is holding may touch its hand.
2. **Readable limbs.** Both arms and both legs visible and not hidden behind props.
3. **Fixed layout.** Record each prop's position (left / centre / right, floor / table) in the storyboard; it stays there for the whole ad unless touched.
4. **Character big enough** — roughly a third of the frame width or more. If the generator frames it too small, keep the image and plan a virtual camera push-in in `edit.json` (`zoom`, `cy`), keeping the same value on both sides of each seam.
5. **9:16 only.** H3 adopts the input image's aspect ratio.
6. **No text** in keyframes (no signs, labels, writing on the notebook).
7. **Brand marks are pasted, not generated.** image-01 can't draw logos or emblems correctly. When the story needs a mark on the drawn cup (because it matters to the plot), generate the cup plain and paste the real mark, cut from the official photo, onto the keyframe at Gate A. Recolor it to the style if needed. That's an accepted fix, the same as painting out a stray stamp. H3 then carries the pasted mark through the relay.

**Keep image prompts short.** The style-lock sentence + character + cup descriptions approach image-01's 1500-character limit quickly. Use a compact form (~600–900 characters): style lock (1 sentence), staging (1 sentence), character (1 sentence, key traits only), props with positions (1 sentence), colors and "no text, no stamps" (1 sentence). Leave everything else for the video prompts.

## 6. Product hero frame (K_end)

- Best: the official product photo, cut out onto the brand background with `scripts/compose_hero.py`. It removes a plain background (or uses the photo's alpha channel) and scales the product so that, **after** finish.py's end-card pull-back (default 0.74), it fills about 45–55 % of the frame height, leaving ~30 % free above for the headline. Pass `--pullback` and `--shift-y` with exactly the values you will use in `edit.json` (`endcard.pullback.scale` / `shift_y`), or the product lands in the wrong place (e.g. on top of the logo). When the ending's bridge brings an ingredient into the shot (e.g. blossoms raining down), generate a background with that ingredient arranged on the surface and an empty spot for the product, then `--bg-image bg.png --base-y <spot> --height <size>` stands the product right there. image-01 tends to put a placeholder cup in the empty spot; that's fine if the real product fully covers it. For posters or menus with several items, crop to the product first (`--crop x0,y0,x1,y1`); the script warns when it finds several separate objects. Pass `--bg-image` to place it on a generated brand background (generate that background with "no text, no stamps, no signature").
- Lifestyle photo only (product on moss, held in a hand, on a busy table): outline the product with a polygon and pass `--mask polygon.json`. Get the polygon by opening the photo, noting the cup's corner points (lid edges, rim, base corners, and a few points along curved sides), and writing them as `[[x,y],…]`. Anything touching the product (leaves, ice, a hand) must be excluded from the polygon, or painted out first. Look at the result zoomed in, and remove leftover background wedges (e.g. around the lid) by refining the polygon.
- Otherwise: generate a premium product photo using `product_spec.canonical_sentence`; ask for "no text, no logo" and add the logo in post.
- It must be the same product as in the story, drawn in the hero style (photographic for most brands; an illustrated hero is fine for a fully illustrated style).

## Using image-01 (API mode)

- Generate 3–4 candidates per keyframe (`n`), pick by Gate A.
- `subject_reference` is built for human faces; it does not keep cartoon characters consistent. Don't rely on it. This is also why the video is generated by relay (Stage 5) and not from many separately generated keyframes.
- Put staging constraints in plain words ("a clear gap of white space between the backpack and the character's feet, never touching").
- Inside MiniMax Agent, stronger image models (with image editing) may be available. If so, you may also generate mid-story keyframes, but still check them at Gate A.
