# Storyboard format

Three levels: **acts** (story and music sections) → **segments** (one H3 generation each, 5 s) → **beats** (timed acting inside a segment).

## Segment rules

- 5 s each (H3 accepts 4–15 s; 5 s gives the best control and was verified). A generated 5 s clip has 124 frames (≈5.17 s).
- One main action per segment. Beats are timed inside it (`0.0–1.2s: …`).
- Segment 1: `mode: "i2v"`, first frame = K0.
- Middle segments: `mode: "i2v"`, first frame = handoff frame of the previous segment.
- Last segment: `mode: "fl2v"`, first frame = handoff frame of the previous segment, last frame = K_end.
- The **handoff frame** is the latest clean frame of a segment. The segment is trimmed there, and the next segment starts from exactly that image, so the seam is invisible. Expect it around **4.2 s**: in testing, H3 drifted in the last second (a prop creeping toward the character, an unasked pan) more often than not. So **finish each segment's beats by 4.0 s** and treat 4.0–5.0 s as a gentle settle. Use 4.9 s only when the last second is verifiably clean.
- Every segment states: the layout of props (what is where), the beats, one camera beat, sound effects, and which act it belongs to.

## Length planning

| Structure | Segments | Approx. final length |
|---|---|---|
| Two-act | 2–3 | 10–15 s + ~2 s end-card hold |
| Three-act | 4–5 | 20–25 s + ~2 s end-card hold |

Act boundaries fall on segment seams or inside a segment at a beat. Their real times are known only after Gate B has fixed every handoff. Read them off `edit.json`, then generate the music (`audio-design.md`).

## storyboard.json (example)

```json
{
  "structure": "three_act",
  "layout": {"books": "floor, far left", "backpack": "floor, far right", "cup": "appears on the floor between character and backpack"},
  "acts": [
    {"id": "A1", "name": "setup", "start": 0.0, "end": 6.5, "mood": "tired, a little grumpy"},
    {"id": "A2", "name": "turn", "start": 6.5, "end": 18.5, "mood": "relief → playful → dreamy"},
    {"id": "A3", "name": "payoff", "start": 18.5, "end": 25.0, "mood": "calm, satisfied"}
  ],
  "segments": [
    {
      "id": "S1", "act": "A1", "mode": "i2v", "first_frame": "keyframes/K0.png", "duration": 5,
      "handoff_at": 4.9,
      "beats": [
        "0.0-1.2s: the scribble tangle boils; it scribbles hard, flops face-down with a squashy bounce, its own legs kick in the air; the backpack stays still",
        "1.2-2.2s: it lifts its head and peeks sideways; the drink pops into view on the floor between it and the backpack",
        "2.2-3.4s: its arm stretches like a noodle, grabs the cup, snaps back; quick gentle punch-in",
        "3.4-5.0s: sips with puffed cheeks, eyes squeezed shut; the tangle shrinks and pops; happy wiggle"
      ],
      "sfx": ["pencil scratching", "squashy flop", "bubbly pop", "rubbery boing", "long slurp", "sparkle"]
    }
  ]
}
```

The prompt for each segment is built from `beats` + `layout` + the blocks in `prompt-blocks.md`.
