# Worked example: line-art grape tea (fictional brand "Doodle Tea")

A reference for **execution quality** and process. It is **not** a plot to reuse and **not** a creativity benchmark: its core idea (tired → sip → escape to the sky) is a category cliché, and the creative bar in `creative-engine.md` now asks for more. It shows one finished run end to end and every fix it needed. The brand is fictional; the style was reverse-engineered from a set of viral ads made by a brand whose logo is a single-line drawing.

## Brief → style

- Brand DNA: single-line logo → bold black line doodles on pure white, a bean-shaped character with a big round head, dot eyes and mitten hands; color only on the drink and grapes; color blooms after the first sip.
- Structure: three-act, 5 segments, ~26 s with the end card.

## Story (final version)

| Seg | Act | Beats |
|---|---|---|
| S1 | setup | Lying on the floor doing homework, scribble tangle boiling overhead; flops face-down, legs kick; peeks; the drink pops onto the floor between it and the backpack; noodle-arm grab; puffed-cheek sip; tangle pops |
| S2 | turn | Sets the cup down, squashes flat, springs up, happy dance, arms up (small motion lines only) |
| S3 | turn | Illustrated watercolor grape balloons float down; it grabs them and lifts off; magenta watercolor bloom spreads |
| S4 | turn | Balloons plump up and pop one after another, showering grapes; strings go limp; it drops onto a cloud and laughs |
| S5 | payoff | Waves from the cloud; camera tilts down with the falling grapes; they land as real grapes; the cup fades in at full size; hero shot |

End card: "A grape moment / refreshes your day." in a light geometric sans, pink hand-drawn swoosh, handwritten "crisp grape boom" next to the cup, small wide-tracked brand name.
Music: 78 BPM lo-fi acoustic (felt piano, nylon guitar, kalimba), sleepy → gently swaying → floating → settled.

## What went wrong and how it was fixed

| Version | Problem | Root cause | Fix (now part of the skill) |
|---|---|---|---|
| v1 | Stiff, "dead" animation; heavy, static text | Prompts listed actions; no acting direction; text dropped on | ALIVE block + acting beats; animated typography; pure-white cleanup; end-card camera |
| v1 | Separately generated keyframes didn't match each other | image-01 can't hold a cartoon character across images | Relay generation from one K0 |
| v2 | Backpack moved when the legs kicked | Backpack silhouette overlapped the feet in K0 | Staging rules at Gate A + LOGIC block |
| v2 | Grape balloons turned photoreal | Prompt asked for "real grape skin texture" | "Illustrated … matching the doodle style, not photorealistic" |
| v2 | Cup "grew" into the hero shot | Transition prompt said "rises into place" | "Fades in at its final full size and position, never grows" |
| v3 | Full-screen manga speed lines; blue-tinted clouds | No style limits | STYLE LIMITS block |
| v3 | Balloons "burst" into a grape bunch while the character still floated | Storyboard broke causality | Causality pass: complete transformations, consequences follow |
| v4 | Balloons drawn as heart shapes with leaves (read as strawberries) | Fruit described by name, not by shape | Describe fruit by shape and growth; fruit-identity check at Gate B |
| all | Music API closed to new users | Platform change | Open-source Music3 via HF Space |
| all | Bouncy music felt too busy | Default mood too energetic | Default to relaxed, soothing |

Measured: motion energy of the opening segment 0.58 (v1) → 2.96 (v2+); the viral reference was 3.56.
