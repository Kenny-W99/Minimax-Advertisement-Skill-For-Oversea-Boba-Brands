# Prompt blocks

Copy these blocks **verbatim** into every video segment prompt (adapt the bracketed parts only). They were tuned on MiniMax H3 and each one fixed a specific failure.

## H3 segment prompt skeleton

H3 follows timed beats well. Use its three fields in this order (format from MiniMax's official `h3-prompt-writing` skill):

```
integrated_multimodal_description:
0.0-5.0s, one continuous shot, vertical frame. Starts exactly on the first frame: <describe the first frame: character, pose, props and where they are>.
<beat 1 with time range>
<beat 2 …>
<beat n …>
<STYLE-LOCK sentence from style_guide>
<ALIVE block>
<LOGIC block>
<STYLE LIMITS block>
<CONSISTENCY block>

overall_soundscape:
<concrete sound effects in order, synced to the beats; no music here>

non_diegetic_music:
none
```

For the final first+last-frame segment, add after the first sentence: `Ends exactly on the last frame: <describe K_end>.` In its consistency block, also say the product must match the last frame exactly and must fade in at its final size and position, never growing or shrinking.

**Illustrated world → photographic hero shot.** If the story's cup is drawn and K_end is a photo, H3 tends to drop the cup for a second or more mid-transition, or to duplicate props (two orchids, a plant jumping sides). Add: *"There is always exactly one cup on screen, in the same place: the drawn cup cross-dissolves in place into the photographic cup; it never disappears, never duplicates, never moves. Every other object keeps its side of the frame."* Keep the composition of the last story frame close to K_end (same cup position and size) so the model only has to change the rendering, not the layout.

**Bridge segments** (`creative-engine.md § Step 4b`): describe the cause, the travel (the camera follows the falling or flowing thing), the arrival (it becomes the real ingredient), and the product's entrance, e.g. *"the real cup drops in from above and lands upright with a soft solid thud in the centre of the jasmine ring; the blossoms hop once from the impact; the cup keeps exactly its shape, lid and print while it falls and lands, no squash, no stretch"*. Say there is exactly one cup and it only appears when it drops in. Story elements that shouldn't travel (characters, the ship) "leave the frame with the drawn world as the camera tilts down".

**Camera moves are allowed; the product resizing itself is not.** A pull-back reveal ("the whole night sky was the cup's print") naturally makes the cup smaller in frame. That's fine, and you should say so: "the camera pulls back; the cup's shape and proportions stay identical". What's forbidden is the product growing, shrinking or morphing *relative to its surroundings*.

Write concrete visuals and sounds. Avoid empty words like "cinematic" or "beautiful". Prompt in English; on-screen text never comes from the model.

## ALIVE block (fixes stiff, lifeless animation)

> Animation style: lively hand-drawn 2D cartoon animation with real character acting, never stiff. The character is always alive: continuous subtle breathing, small head tilts and bobs, tiny bounces, blinks. Its body is soft and elastic like rubber: squash and stretch on every action, clear anticipation before each move, overshoot and settle after it, loose follow-through. Arms and legs are bendy rubber-hose noodle limbs that can stretch comically long. Line art has a gentle hand-drawn line boil. Snappy cartoon timing: short holds, then quick bursts of motion.

For non-cartoon styles (product cinematography, ink-wash), keep the intent and swap the vocabulary: "gentle continuous motion, liquid and steam always moving, slow elegant camera drift, eased starts and stops, nothing frozen".

Measured effect: same first frame, same 5 s → motion energy 0.58 → 2.96 (the viral reference was 3.56).

## LOGIC block (fixes props moving by themselves, merging, impossible events)

> Physical logic rules (cartoon exaggeration is welcome, but cause and effect must always make sense): every prop stays exactly where it is and does not move, wobble or change unless the character physically touches it; nothing moves by itself; objects never merge with the character or with each other and never pass through each other; when the character holds something it moves with the mitten hand, when it lets go the object falls or rests under gravity; the character always has exactly two arms and two legs attached to its body; things only appear when the prompt says so, with a visible pop; the floor line stays in the same place; left-right positions of <list props> stay the same for the whole clip. Every transformation and destruction is complete and permanent: a popped balloon disappears completely, leaving only a brief pop burst; once the balloons are gone nothing lifts the character any more, so it must fall or rest on something.

(Edit the last sentence to match this segment's transformation, or drop it if there is none.)

With animals, add: "the <animal> keeps correct anatomy: its tail stays attached behind its body and swings only behind it, four legs, never touching or passing through other objects". In testing, a horse's tail swung forward into a prop twice.

## PHYSICS block (for any moving object that isn't a cartoon character)

> Real physics: <object> has weight and momentum. It moves forward along a smooth path in one direction, speeding up and slowing down gradually, and never hovers, floats in place, slides sideways or turns around by itself. Any change of direction has a visible cause (<a gust of wind / a bump>) and follows a gentle arc. When it lands it touches down, skids a short distance with friction and stops, without spinning in place. It keeps exactly the same shape, folds and size throughout; it never bends, morphs or rotates freely. The camera follows slightly slower than the object, so it travels across the frame rather than staying pinned at the centre.

## STYLE LIMITS block (fixes off-style effects)

The style lock describes the constant look. Rules that change during the ad (e.g. "monochrome in act 1, teal washes in after the bite") belong here, written per segment.

> Style limits: motion lines are only a few small strokes right next to the character, never full-screen speed lines, radial bursts or background effects. <Background elements, e.g. "Clouds are black outline only with pure white fill, never tinted or colored">. Only <the drink and its fruit/ingredient> have color.

## CONSISTENCY block (product, character, text)

Include the product sentence only in segments where the product is on screen. When it isn't, drop that clause and add "no drink cup appears in this segment" if the model might invent one.

> Consistency rules: same art style for the whole clip: <style essentials>. The character keeps the same <head/eyes/line weight from character_spec>; rounded mitten hands without any fingers; no extra limbs. The drink cup keeps an identical shape, colors and layers, no morphing: <product_spec.canonical_sentence>. No text, no letters, no logo, no new objects except the ones described. No camera cuts.

## Fruit and ingredient wording

Describe what makes the fruit recognisable: shape, surface and how it grows. Don't rely on the fruit's name.
- grapes: "round spherical berries clustered like a bunch of grapes, smooth glossy purple-red skin, no leaves, not heart-shaped, not strawberries"
- orchid: "a slender orchid stem with several pale flowers, each flower with three outer petals and a central lip"
- pearls: "small round dark-brown glossy tapioca pearls"

Illustrated styles need the fruit illustrated too ("illustrated in soft watercolor with a black ink outline, matching the doodle style, not photorealistic"). Otherwise H3 can make it photoreal and break the style.

## Writing constraints that work

- **Describe the wanted state positively.** "No flowers" still produced flowers. "A bare, grass-like plant with only long thin leaves" worked. Models latch onto the nouns you mention.
- **Chinese classical styles** (baimiao, ink-wash, rice paper) make image-01 add red seal stamps, signatures and calligraphy. Add by default: "no red stamps, no seals, no signature, no calligraphy, no writing". It still adds them sometimes, so check the corners at Gate A and paint them out (a flat fill with the background color) if needed.

## Keyframe image prompt pattern (image-01)

image-01 rejects prompts of **1500 characters or more** (status 2013). Image prompts get the style-lock sentence, staging, subject and colors only. Never paste the video blocks (ALIVE, LOGIC…) into them.

```
<style-lock sentence>. Clean readable staging with clear empty space between every object, no overlapping silhouettes.
<character from character_spec, drawn LARGE, pose>, <expression>.
<each prop with an explicit position and "clearly separated from the character">.
<what is colored and what is not>. No text, no letters, no logo. Vertical 9:16 composition.
```

## Hero product prompt pattern (when no usable official photo exists)

```
Premium product photography of <product_spec.canonical_sentence>, standing centered in the lower half of a <brand background> seamless background, <hero ingredient arranged beside it>, soft natural studio light, soft contact shadow, crisp focus, vertical 9:16, large empty space in the upper third for a headline. No text, no letters, no logo.
```
