---
name: minimax-boba-ads
description: Direct and produce a complete, high-quality short vertical video ad (9:16, ~10–25 s, for TikTok / Reels / Shorts) for ONE specific bubble-tea, milk-tea, fruit-tea or coffee-drink product with MiniMax models (H3 video, image-01, open-source Music3). The skill researches the brand and product online, derives a brand-specific art style, palette and typography, invents an original 2- or 3-act story, designs act-matched music, then generates, assembles and quality-checks the finished ad in one go. Use it whenever someone wants an ad, promo, creative short, product video or social clip for a drink / tea / boba brand — e.g. "帮我给 Gong Cha 的黑糖珍珠鲜奶做个创意广告", "奶茶广告", "茶饮宣传短片", "make a TikTok ad for Gong Cha's brown sugar milk tea" — even if they only give a brand name, a photo of a cup, or their own storyline.
---

# MiniMax Boba Ads

## Delivery contract (read this first, check it last)

This skill makes a **short animated story ad**, not a product clip. Unless the user explicitly asks for something else, the finished `final.mp4` must be:

| | Required |
|---|---|
| Format | **9:16 vertical**, 24 fps |
| Length | **12–25 s** (two-act 12–15 s, three-act 20–25 s) |
| Shots | **2–5 relay segments** of ~5 s (two-act 2–3, three-act 4–5), each continuing from the previous one, plus an end card |
| Story | a **protagonist with a want, an obstacle, a product-caused turn and a planted payoff** (Stage 3) |
| Ending | a **bridge**: something from the story physically travels into the product hero shot |
| End card | slogan, product name and logo overlaid in post, held ≥ 2 s |

**These count as failure**: a single shot of the product with steam, light or petals moving; a landscape (16:9) video; anything under ~12 s; a montage of pretty shots with no character and no story. If your plan looks like one of these, go back to Stage 3.

**If another video skill is active at the same time** (e.g. a built-in "video-creator" in MiniMax Agent), this skill's contract, pipeline and rules take precedence for drink and tea ads. Use the other skill's tools if helpful, but not its format or structure.

**Running inside MiniMax Agent** (or any host with slow or asynchronous video tools):
- At the start, tell the user the plan and an honest estimate (research + images ~10 min, then ~3–10 min per segment at 768P; more at 2K).
- Generate all drafts at **768P**. Use 2K only if the user asks for it.
- Don't build extra mock or test pipelines; use the scripts and tools as they are.
- While a segment renders, prepare the next prompt, the end card or the music.
- If a video task runs over 20 minutes, check its status. If it's stuck or failed, resubmit at 768P, and tell the user what happened.

You are the director, art director, sound designer and editor of a short drink ad. The user gives you as little as a brand name; you hand back a finished, polished video plus the files that explain how it was made.

The skill encodes what was learned the hard way while reverse-engineering and rebuilding a set of viral boba ads: what makes them feel alive, which AI-video failure modes ruin them (morphing cups, extra fingers, props that move by themselves, stories that stop making sense), and how to avoid each one. Process and quality rules are fixed; **the story, art style, colors, fonts and music are not** — they are invented fresh for every brand and product.

## What "done" looks like

Deliver, in an output folder (default `./ad_output/<brand>-<product>/`):

1. `final.mp4` — 9:16, 24 fps, H.264 + AAC, loudness ≈ -16 LUFS
2. `report.md` — what you understood (the brief), what you found online (with source URLs), the 3 concepts and why one won, what QA caught and fixed, cost, anything still imperfect
3. All intermediate files: `request_brief.json`, `brand_profile.json`, `product_spec.json`, `style_guide.json`, `concept.json`, `storyboard.json`, `audio_plan.json`, keyframes, per-segment prompts and clips, `edit.json`

Work straight through without stopping to ask the user (they asked for one-shot output). When something is genuinely ambiguous, pick the most sensible option, write it down in the brief, and keep going. Two automatic gates (below) replace human checkpoints.

## Tools you need

Pick whichever is available; the instructions are tool-agnostic.

| Capability | Inside MiniMax Agent | Anywhere else (API mode) |
|---|---|---|
| Web search & page reading | built-in search / browse | your agent's web tools |
| Look at images & frames | built-in vision | your agent's image reading |
| Image generation | built-in image tool | `scripts/minimax_image.py` (image-01) |
| Video generation | built-in H3 video tool (image-to-video, first+last frame) | `scripts/minimax_video.py` (MiniMax-H3) |
| Music | built-in music tool, or `scripts/music3.py` | `scripts/music3.py` (open-source MiniMax-Music3 via its official Hugging Face Space) |
| Editing | code sandbox with ffmpeg + Python/Pillow | same: `scripts/finish.py`, `scripts/frames.py` |

API mode needs `MINIMAX_API_KEY` (pay-as-you-go key from platform.minimax.io) and optionally `MINIMAX_API_HOST` (default `https://api.minimax.io`; mainland keys use `https://api.minimaxi.com`). Never print, log or write the key into any file. See `references/minimax-api.md` for endpoints, limits and prices, and run `scripts/check_env.sh` once before starting.

## The pipeline

```
0 Brief → 1 Research → 2 Visual system → 3 Original story → [Gate A: keyframes]
→ 4 Audio plan (moods) → 5 Generate (relay) → [Gate B per segment] → 6 Music (on the real cut) → 7 Finish + final QA → report
```

Read the reference for each stage when you reach it — they hold the detail; this file holds the order and the non-negotiables.

### 0 · Understand the request → `request_brief.json`
Read `references/request-parsing.md`. Turn the user's words (and any image) into one brief that every later stage reads instead of re-interpreting the user. Every field records its source: `user_text`, `user_image`, `web`, or `default`. Priority when sources conflict: **user text > user image > web > default**.

- One ad = one specific product. Brand only → research and lock one product (signature or current hero item with clear official photos). Never show a second product.
- A photo → identify logo, brand and product from it, verify online, and use the photo as the primary product reference.
- The user's own storyline → follow it faithfully; quality rules still apply; adapt only what would break a rule and say what you changed.
- Holiday words (Christmas, 春节, Halloween, 中秋, Valentine's, Diwali, Eid…) → holiday mode (see `references/holidays.md`).

### 1 · Research online → `brand_profile.json`, `product_spec.json`
Read `references/brand-research.md`. Find, with source URLs: the exact product's appearance (cup shape, lid, liquid layers and their colors, toppings, cup print), official product photos, logo and logo style, brand palette (HEX), official or closest typefaces, brand voice and slogans, mascot/IP, culture and city cues, target market. Unknown stays `unknown` with a safe default — never invent facts about a real product.

### 2 · Visual system → `style_guide.json`, character + product references
Read `references/visual-system.md`. Derive the art style from the brand's own visual DNA (a single-line logo suggested single-line doodles for one brand; a mascot brand gets its mascot; a classical Chinese brand might get ink-wash or gongbi). Define color roles, the hero character (mitten hands by default, or hands hidden in sleeves — no fingers), a frozen style-lock sentence, and the product reference. Images come after the story, because the story decides what the opening frame shows.

### 3 · Invent the story → `concept.json`, `storyboard.json`
Read `references/creative-engine.md` and `references/storyboard-format.md`. Creativity is the point of the ad. A clean execution of a predictable idea ("sip → the rain stops / flowers bloom / mood fixed") was rejected in testing. Do not reuse the reference example's plot for another brand.

1. **Inventory** 10+ things only this product has: packaging and logo figures, name and puns, ingredient physics, drinking ritual, aroma, brand culture.
2. **Diverge:** 10+ one-line ideas using at least five techniques (packaging comes alive, personified attribute, scale reveal, match-cut rhyme, setup → payoff gag, role reversal, cultural remix, literal name…). Category clichés are banned as the core idea.
3. **Converge:** shortlist 3, each with a **story spine** (protagonist wants X, an obstacle blocks it, the product causes the turn, and a payoff that was planted on screen earlier), a logline, a hero image and a payoff. A journey from A to B isn't a story, and segments where nothing changes are filler. Score them with surprise weighted highest. Causality and feasibility are pass/fail gates: if the boldest idea is hard to generate, simplify how it's executed rather than choosing a safer idea. The winner must pass **the bar**: swap test, one-sentence surprise, a screenshot-worthy hero image, a real payoff, and the product as engine/stage/star rather than medicine. Then **critique it as a demanding creative director** (does anything happen? who do we care about? is the payoff planted? will any motion look fake?) and fix what the critique finds. Self-scores run high.
4. **Structure and expand:** two-act (setup → punchline, 10–15 s) or three-act (setup → escalation → twist/payoff, 20–25 s). The hero shot ends the ad, ideally as part of the payoff. Then acts → 5-second segments → acting beats, one main action per segment.
5. **Design the bridge into the hero shot.** Something from the story must physically travel into the product shot: it rains down, pours, gets thrown or kicked, or gallops across, and arrives as the real ingredient, with the cup dropping or settling among it. Plain pull-backs and dissolves are rejected. Build K_end so the arriving element is in it.
6. Run the **causality pass**: for each segment ask "after this happens, what must every object on screen do next?" Fix any segment you can't answer.

**Gate A (before any video spend):** now generate the opening keyframe K0 for the chosen story and the product hero frame K_end (`scripts/compose_hero.py` builds K_end from an official photo). Images are cheap; video is not. Check both against `references/qa-checklist.md § Gate A`: brand colors right, product matches `product_spec`, character matches its spec, every prop's silhouette separated from the character, nothing ambiguous. Regenerate until they pass (max 4 rounds per image, then take the best and note it). Small fixes such as painting out a stray stamp are fine.

### 4 · Audio plan + draft music → `audio_plan.json`, `music.wav`
Read `references/audio-design.md`. Decide each act's musical mood from the brand (default: relaxed, soothing), the key, tempo and instruments. **Generate the music now**, using the storyboard's planned act times plus ~2 s of slack. The free music quota is often a single track per day, so securing a track early beats finding out at the end. If the quota is already gone, note it and carry on; Stage 6 has the fallbacks.

### 5 · Generate video by relay → per-segment clips
Read `references/prompt-blocks.md` and `references/minimax-api.md`.

- Segment 1 starts from K0 (image-to-video). Each next segment starts from the **last clean frame** of the previous one. The final segment uses first+last frame mode landing exactly on K_end.
- Every segment prompt uses H3's three fields — `integrated_multimodal_description`, `overall_soundscape`, `non_diegetic_music: none` — with timed beats, and appends the verbatim blocks from `prompt-blocks.md`: **alive**, **logic**, **style limits**, **consistency**.
- Draft at 768P while iterating; render the final at 2K only if the user asked for top quality and budget allows (2K costs ~1.6×).

**Gate B (after every segment):** contact-sheet the clip (`scripts/frames.py sheet`) and check `qa-checklist.md § Gate B` — fingers, character, product, props moving untouched, colors, fruit recognisability, seam continuity. H3 tends to drift in the last 0.5–1.5 s: choose the latest clean frame as the handoff and trim there. Failing segment → regenerate it (max 2 retries) with the prompt fixed at the cause; still failing → simplify the action. A smaller, correct motion beats a spectacular broken one.

**Budget guard:** stop at 3× the planned video seconds; deliver the best version with an honest list of remaining issues.

### 6 · Fit the music to the real cut
Once `edit.json` is final, read the real act boundaries off it and fit the draft track: `music.offset` slides it so its biggest change lands on the strongest visual change, `music.envelope` rides gains into each boundary, and the end fades over the last ~1.5 s. Regenerate only if the draft is far off and quota remains, using the same brief with the real times. Check: no vocals, it covers the whole ad, energy changes near each act boundary, no sudden jumps. **No track at all** (quota gone, no built-in tool): follow `audio-design.md § No music available`. Never deliver a silent end card without saying so in the report.

### 7 · Finish → `final.mp4`, `report.md`
Read `references/end-card.md`. Assemble with `scripts/finish.py` (run it once without music to fix the cut, then again with music) (frame-accurate trims, pure-white cleanup for white-background styles, optional virtual camera, end-card pull-back, animated typography, logo, music + SFX mix). All on-screen text and logos are added here in post — never generated by the video model. Then run the final QA (`qa-checklist.md § Final`) on a 1-fps contact sheet and fix what fails. Write `report.md`. Before you deliver, re-check the **delivery contract** at the top: 9:16, 12–25 s, 2–5 relay segments, story spine, bridge, end card. If any item fails, fix it rather than explaining it away in the report.

## Non-negotiables (why they matter)

These come from real failures; each one is cheap to prevent and expensive to fix after generation.

- **One locked product, everywhere.** Product description copied verbatim from `product_spec.json` into every prompt; the hero shot built from an official photo when possible. The cup never grows, shrinks, rotates into a new shape or changes layers. Viewers forgive a simple animation, not a wrong product.
- **No fingers by default.** Rounded mitten hands remove the #1 AI artifact (3/4/6 fingers). If a mascot has fingers, fix the count in its spec and check every segment.
- **No model-generated text or logos.** Slogans, product names and logos are overlaid in post with real fonts and the real logo file, so they never come out garbled.
- **Physical and causal logic.** Props move only when touched; nothing merges or passes through; things appear only when the storyboard says so; transformations are complete (a popped balloon is gone, and then nothing holds the character up). Most logic errors are planted in keyframes — overlapping silhouettes make the model fuse objects — so staging is checked at Gate A.
- **Physically believable, not "AI-looking".** Fake physics is what gives AI video away: hovering, drifting, objects turning or spinning by themselves, sticker-like objects pinned in frame. Prefer motions H3 renders well (character acting, falling, pouring, blooming). Constrain risky ones with the PHYSICS block, and keep exaggerated action in illustrated worlds rather than photoreal ones.
- **Alive, not stiff.** Squash and stretch, anticipation, overshoot, rubber-hose limbs, continuous breathing, snappy holds-then-bursts, a camera beat per segment. Stiff, evenly paced motion is what makes AI ads feel dead.
- **Brand-true, not template-true.** Style, palette, fonts, music and story come from this brand and this product.
- **An idea, not a cliché.** If the story still works with a competitor's cup, or boils down to "drink it and things get better", it isn't done. Go back to Stage 3 Step 2.
- **Honest report.** Say what was inferred, what was a default, what QA caught, and what is still imperfect.

## Reference map

| Stage | Read |
|---|---|
| 0 | `references/request-parsing.md`, `references/holidays.md` |
| 1 | `references/brand-research.md` |
| 2 | `references/visual-system.md` |
| 3 + Gate A | `references/creative-engine.md`, `references/storyboard-format.md`, `references/prompt-blocks.md` |
| 4, 6 | `references/audio-design.md` |
| 5 | `references/prompt-blocks.md`, `references/minimax-api.md` |
| 7 | `references/end-card.md` |
| all gates | `references/qa-checklist.md` |
| JSON shapes | `references/schemas.md` |
| a worked example | `references/example-line-art-grape.md` |
