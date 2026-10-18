# JSON shapes

Keep files small and human-readable. Fields not listed are allowed.

## request_brief.json

```json
{
  "brand":   {"value": "Moonleaf Tea (fictional)", "source": "user_text"},
  "product": {"value": "Osmanthus Oolong Latte", "source": "user_text"},
  "market":  {"value": "Taiwan / Traditional Chinese", "source": "web"},
  "language": {"value": "zh-TW", "source": "default"},
  "platform": {"value": "tiktok_reels_shorts", "source": "default"},
  "duration_target": {"value": 22, "source": "default"},
  "story_source": {"value": "agent", "source": "default"},
  "holiday": {"value": "none", "source": "default"},
  "style_hint": null, "music_hint": null,
  "must_include": [], "must_avoid": [],
  "notes": ["Interpreted '创意广告' as a 9:16 social ad without voice-over."]
}
```

## brand_profile.json

```json
{
  "official_name": "...", "home_market": "...", "sources": ["https://..."],
  "logo": {"style": "single-line figure | mascot | calligraphy | wordmark | ...", "file": "assets/logo.png", "source": "https://..."},
  "palette": {"primary": "#...", "secondary": "#...", "accent": "#...", "background": "#..."},
  "typography": {"headline": "font name or look", "body": "...", "official_available": false, "fallback_ofl": "Noto Serif SC"},
  "voice": "poetic, classical, gentle", "taglines": ["..."],
  "mascot": null,
  "culture_cues": ["tea mountains", "night markets"],
  "unknowns": ["exact HEX of secondary color"]
}
```

## product_spec.json

```json
{
  "name": "...", "sources": ["https://..."], "photos": ["assets/product_1.jpg"],
  "cup": "clear plastic, tall, slightly tapered", "lid": "flat sealed film", "straw": "wide, clear",
  "layers_top_to_bottom": [{"what": "cream foam", "color": "#F4EFE6"}, {"what": "milk tea", "color": "#D9C3A5"}],
  "toppings": ["..."], "print": "...",
  "hook_material": ["osmanthus blossoms", "roasted oolong aroma"],
  "canonical_sentence": "a tall clear plastic cup with ..."
}
```

## style_guide.json

```json
{
  "style": "ink-wash illustration on rice paper", "why": "brand uses classical Chinese painting motifs",
  "style_lock": "<one sentence pasted verbatim into every prompt>",
  "color_roles": {"background": "#...", "line": "#...", "accent": "#...", "brand": "#..."},
  "color_rule": "monochrome until the first sip, then the drink's color washes into the scene",
  "character_spec": {"description": "...", "hands": "rounded mitten hands without fingers", "fill": "...", "forbidden": ["clothes", "stripes", "hair"]},
  "keyframes": {"K0": "keyframes/K0.png", "K_end": "keyframes/K_end.png"}
}
```

## concept.json

```json
{
  "inventory": ["..."], "raw_ideas": ["10+ one-liners with their technique"],
  "bridge": {"type": "rain / fall", "cause": "final chord shakes the jasmine stars loose", "travel": "blossoms rain down, camera tilts down", "arrival": "real jasmine ring on ivory; the cup drops into the centre with a thud", "k_end_needs": "jasmine ring around the cup"},
  "bar_check": {"swap_test": "fails with a competitor (good) because ...", "one_sentence_surprise": "...", "hero_image": "...", "payoff": "...", "product_role": "stage"},
  "structure": "two_act | three_act", "structure_why": "...",
  "candidates": [
    {"logline": "...", "technique": "packaging comes alive", "hero_image": "...", "payoff": "...", "acts": ["..."],
     "scores": {"surprise": 5, "only_this_product": 5, "payoff": 4, "brand_fit": 5, "product_clarity": 4},
     "weighted_total": 42, "gates": {"causality": "pass", "feasibility": "pass after simplifying X"}, "chosen": true},
    {"logline": "...", "weighted_total": 30, "chosen": false, "why_not": "..."}
  ]
}
```

## storyboard.json

See `storyboard-format.md`.

## audio_plan.json

```json
{
  "bpm": 78, "key": "D major", "bar_seconds": 3.077,
  "acts": [
    {"id": "A1", "start": 0.0, "end": 6.2, "mood": "sleepy, quiet", "energy": 1, "lead": ["felt piano"]},
    {"id": "A2", "start": 6.2, "end": 18.5, "mood": "relaxed, gently swaying → floating", "energy": 2, "lead": ["nylon guitar", "kalimba"], "bridge_in": "glockenspiel twinkle on the sip"},
    {"id": "A3", "start": 18.5, "end": 25.0, "mood": "settled, content", "energy": 1, "lead": ["pads", "bell"], "bridge_in": "soft swell"}
  ],
  "music_brief": "music_brief.json",
  "sfx_from_segments": true, "voice": null
}
```

## edit.json (input to scripts/finish.py)

```json
{
  "segments": [
    {"file": "clips/S1.mp4", "in": 0, "out": 118, "zoom": [1.4, 1.4], "cy": [0.66, 0.66]},
    {"file": "clips/S2.mp4", "in": 1, "out": 118, "zoom": [1.4, 1.2], "cy": [0.66, 0.62]},
    {"file": "clips/S3.mp4", "in": 1, "out": 118}
  ],
  "hold_end": 2.2,
  "whites": true,
  "on_twos": false,
  "background": null,
  "music": {"file": "music.wav", "gain": 0.8, "fade_out_at": 24.5, "offset": 0.0, "envelope": [[0, 0], [11, 0], [12.5, -7], [24, -7]]},
  "endcard": {
    "pullback": {"start": 21.0, "dur": 1.6, "scale": 0.74, "shift_y": 0.07, "drift": 0.006},
    "text_start": 21.4,
    "ink": "#2B2B2B",
    "slogan": {"lines": ["Line one", "line two."], "font": "fonts/Nunito-Regular.ttf", "size": 33, "y": 0.155},
    "accent": {"type": "swoosh", "color": "#D8336E", "width": 5},
    "note": {"words": ["crisp", "grape"], "font": "fonts/Caveat-Bold.ttf", "size": 34, "x": 0.735, "y": 0.53, "rotate": -6, "delay": 1.0, "cps": 12},
    "logo": {"file": "assets/logo.png", "width": 0.2, "max_height": 0.08, "y": 0.88},
    "brand": {"text": "BRAND", "font": "fonts/Nunito-SemiBold.ttf", "size": 19, "y": 0.925, "tracking": 7}
  }
}
```

- `in` / `out` are frame numbers, `[in, out)`. Drop frame 0 of every segment after the first: it duplicates the previous handoff frame.
- `accent.type`: `swoosh` (wavy underline) | `rule` (thin straight line) | `seal` (filled square stamp, color = accent) | `none`.
- `note.vertical: true` writes the note top-to-bottom (CJK calligraphy). `logo.y` is the top edge. `music.offset` skips the first seconds of the track. `music.envelope` is a gain curve in dB, linear between points.
- `note`, `logo`, `brand` and `music` are optional. With `logo`, `brand` is skipped unless both are given.
- `font` paths may be absolute; `"index"` selects a face inside .ttc collections; `"weight"` sets a variable font's weight axis (e.g. 400).
- `background` (end-card canvas): omit or `null` to auto-sample the last frame's edge color (recommended).
- `endcard.pullback.scale` / `shift_y` must match the `--pullback` / `--shift-y` you gave `compose_hero.py`.
