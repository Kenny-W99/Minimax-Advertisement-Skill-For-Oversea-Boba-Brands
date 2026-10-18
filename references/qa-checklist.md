# QA checklist

Look at the actual pixels (frames and contact sheets). Unused tiles at the end of a contact sheet are grey padding, not black frames. Don't assume a prompt was obeyed. `scripts/frames.py sheet clip.mp4 sheet.jpg --fps 4` makes a 4-fps contact sheet; zoom in with `frames.py grab` when something looks off.

## Gate A — keyframes (before any video is generated)

| Check | Fail if |
|---|---|
| Product | K_end's cup shape, lid, layers or colors differ from `product_spec`; text or garbled logos on the cup |
| Brand colors | palette noticeably off from `brand_profile` |
| Character | proportions, eyes, line weight or fill differ from `character_spec`; extra clothes, stripes, hair, bows; fingers (unless the spec allows) |
| Staging | any prop overlaps or touches the character's silhouette; limbs hidden; ambiguous shapes that could be read as part of the character |
| Size | character < ~1/4 of frame width (plan a virtual push-in or regenerate) |
| Text & stamps | any letters, signs, writing, signatures or red seal stamps. **Check all four corners**, where image-01 tends to put them |
| Format | not 9:16 |

Regenerate a failing keyframe (up to 4 rounds), then take the best and note what's left.

## Gate B — every generated segment

| Check | Fail if |
|---|---|
| Fingers / limbs | fingers appear, finger count changes, extra or missing limbs (≥ 3 consecutive frames; 1–2-frame smears in fast motion are acceptable cartoon technique) |
| Character | proportions, face or line weight drift noticeably; head or body merges with another object |
| Product | cup shape, layers, colors, lid or print change; the cup grows or shrinks into place |
| Props | a prop moves, wobbles or deforms without being touched; objects merge or pass through each other |
| Causality | an event happens without its cause or consequence (e.g. balloons gone but the character still floats) |
| Color rules | color outside the allowed elements (tinted clouds, colored background in a monochrome act) |
| Style | off-style effects (full-screen speed lines, photoreal fruit in an illustrated world) |
| Fruit identity | the fruit or ingredient isn't instantly recognisable as the product's flavor |
| Seam | the first frame doesn't continue the previous handoff frame |
| AI feel | objects hover, drift sideways, turn around or rotate without a cause; an object stays pinned at frame centre while the world slides behind it; speed doesn't match the action; landings spin or bounce wrongly; textures or folds crawl during motion. Ask: "Would a viewer say *this looks AI*?" |
| Story progress | the segment doesn't change the situation (filler) |
| Bridge (last segment) | the transition is only a pull-back or dissolve; the travelling element doesn't arrive as something visible in the hero shot; the product squashes, stretches or morphs while dropping or landing |
| Presence (last segment) | the product disappears for any frames, or a prop duplicates or jumps sides during the illustrated → photo transition |
| Text | letters or logos appear |

Then pick the handoff frame: the latest frame (≤ 4.9 s) where everything above still passes. **Run the Gate A staging check on that handoff frame too.** It becomes the next segment's first frame, so any overlap in it (a tail touching a prop, a hand merged with a cup) gets inherited and amplified. Grab it frame-accurately with `frames.py grab clip.mp4 <N> out.png --frame`.

Fixing a failure: change the prompt at the cause (staging, missing rule, vague fruit wording, two actions crammed into one segment) and regenerate. Max 2 retries per segment. After that, simplify: shorter action, smaller motion, or a gentle hold-and-push-in. A smaller, correct motion beats a spectacular broken one.

## Final — the assembled ad (1-fps contact sheet + listen through the metrics)

- No visible jump at any seam (compare the frame before and after each cut).
- Every prompt, slogan and end-card element names the locked product; the flavor is consistent.
- End card: headline readable, not overlapping the product, logo present, hold ≥ 2 s, no black frames at the end.
- Music: no vocals (ASR check, see `audio-design.md`); covers the whole ad; changes near act boundaries; ends cleanly.
- SFX are audible and don't click at seams.
- Loudness ≈ -16 LUFS.
- Duration within the planned range.
- `report.md` lists remaining imperfections honestly.

## Useful measurements

- Motion energy (`frames.py motion clip.mp4`): mean absolute frame difference. Stiff ≈ 0.5, lively ≈ 2.5–3.5 for doodle styles.
- Loudness by half-second (`frames.py loudness audio.wav`) to see the music's arc.
