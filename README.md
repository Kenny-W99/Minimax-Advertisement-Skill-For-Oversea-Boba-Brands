# MiniMax Boba Ads — an agent skill for brand-true drink ads

Give your agent one line, like *"Make a creative ad for Gong Cha's brown sugar milk tea"*, and get back a finished 9:16 short video ad. The agent:

1. **researches** the brand and the exact product online: what the cup looks like, logo, palette, fonts, voice, culture;
2. **designs a brand-specific look**: art style derived from the brand's own visual DNA, color roles, a hero character, locked product description;
3. **invents an original story** (two-act or three-act) built around something only this product has, after writing and scoring three concepts;
4. **plans act-matched music**: one continuous instrumental whose mood changes with each act, without abrupt transitions;
5. **generates** the video with MiniMax H3 by *relay*, so each segment continues seamlessly from the last;
6. **checks every segment** for the usual AI-video failures and regenerates what fails;
7. **finishes** the ad: animated typography, logo, end-card camera, music mix, loudness. It writes a report of every decision.

It works in one go, without pausing for approval. Two automatic quality gates take the place of human checkpoints.

## Why this skill exists

It was distilled from rebuilding a set of viral line-art boba ads, one failure at a time. These are the problems it now prevents by design:

| Failure | Prevention |
|---|---|
| Fingers changing count (3 → 4 → 6) | rounded mitten hands by default |
| The cup morphing, growing or changing layers | one locked product sentence in every prompt; hero shot from an official photo; "fade in at final size" |
| Garbled text and logos | no model-generated text; everything overlaid in post |
| Stiff, lifeless animation | an acting block (squash & stretch, anticipation, rubber-hose limbs) and beat-by-beat acting direction |
| Props moving by themselves | staging rules for keyframes plus a physical-logic block |
| Stories that stop making sense | a mandatory causality pass (popped balloons are gone, so the character falls and lands somewhere) |
| Wrong-looking fruit | describe the fruit by shape and growth, not by name; fruit-identity QA |
| Every brand getting the same ad | style, palette, fonts, story and music are derived per brand; the worked example is reference only |
| Predictable "sip → everything gets better" stories | a creative bar (swap test, surprise, hero image, payoff), a category-cliché blacklist, 10+ raw ideas across techniques, surprise weighted highest |
| A flat "and here's the product" ending | a mandatory bridge: something from the story falls, pours or flies into the hero shot and arrives as the real ingredient |
| Music that's missing or cuts abruptly | music generated early, then fitted to the final cut (offset, gain envelope); one key and tempo; bridges at act changes |

See `references/example-line-art-grape.md` for the full iteration log.

## Install

**MiniMax Agent** (agent.minimax.io): in the Skills section, import from GitHub with `https://github.com/Kenny-W99/Minimax-Advertisement-Skill-For-Oversea-Boba-Brands`. Or download this repository as a ZIP (*Code → Download ZIP*; it has exactly one `SKILL.md` at the root) and upload it under *Create → Upload a skill*. Keep it in *My skills*.

**Claude Code, Codex and other agents** (skills CLI):

```bash
npx skills add https://github.com/Kenny-W99/Minimax-Advertisement-Skill-For-Oversea-Boba-Brands
```

Or clone it straight into your agent's skills directory:

```bash
git clone https://github.com/Kenny-W99/Minimax-Advertisement-Skill-For-Oversea-Boba-Brands ~/.claude/skills/minimax-boba-ads
```

## Using it inside MiniMax Agent

What we learned from real runs:
- **Import the latest version.** Re-import from GitHub after updates; an old copy misses later rules.
- **Don't attach another video skill in the same message.** With MiniMax's built-in *video-creator* attached as well, the agent followed that skill's format and made a 7-second landscape product clip. Ask for this skill alone, e.g. *"用 minimax-boba-ads 这个 skill 给我做一个 X 的创意广告"*.
- **Use a strong model.** A lightweight "Flash" model skimmed the multi-step workflow and spent over an hour on one shot. Pick the most capable model available.
- **Expect ~30–60 minutes** for a full ad at 768P. The agent should tell you its plan and an estimate at the start.
- For the most reliable results today, run it in API mode from Claude Code or Codex (below) with your own MiniMax key.

## Quick start

After installing, just ask in plain words, in any language:

- *"Make a creative TikTok ad for Gong Cha's brown sugar milk tea."*
- *"帮我给这杯奶茶做一个创意广告"* (with a photo of the cup attached)
- *"Make a Christmas ad for Mixue — here's my story: …"*

The skill researches the brand, writes three concepts and picks the strongest, generates and checks every shot, and leaves `final.mp4` plus a `report.md` that explains every decision.

## Requirements

- **Inside MiniMax Agent**: the built-in search, image, video and code tools. Generation uses your own MiniMax credits.
- **API mode (any other agent)**:
  - `ffmpeg`, Python 3.10+, `pip install -r scripts/requirements.txt`
  - `MINIMAX_API_KEY`: a pay-as-you-go key from [platform.minimax.io](https://platform.minimax.io) (H3 is not included in subscription plans). Optionally set `MINIMAX_API_HOST` (`https://api.minimax.io` international, `https://api.minimaxi.com` mainland China).
  - Run `bash scripts/check_env.sh`.
- Music uses the open-source **MiniMax-Music3** through its official Hugging Face Space, so no GPU is needed. MiniMax's paid music API is closed to new users. The free Space quota is about one track per day. Set `HF_TOKEN` from a Hugging Face PRO account (40 GPU-minutes/day) if you make ads regularly.

Never commit your API key. The scripts only read it from the environment.

## Cost (API mode, approximate)

One ~25 s ad at 768P costs about **US$3** (five 5 s H3 segments plus a couple of retries, ~US$0.05 of images, free music). Rendering the final at 2K adds about US$3.3. Prices: [MiniMax pricing](https://platform.minimax.io/docs/pricing/overview).

## What you get

```
ad_output/<brand>-<product>/
├── final.mp4             9:16, 24 fps, -16 LUFS
├── report.md             brief, research sources, concepts & scores, QA log, cost, known issues
├── request_brief.json  brand_profile.json  product_spec.json  style_guide.json
├── concept.json  storyboard.json  audio_plan.json  edit.json
├── keyframes/  prompts/  clips/  music.wav
```

## Repository layout

```
SKILL.md                  the workflow and the non-negotiables (start here)
references/               stage-by-stage guidance the agent reads on demand
scripts/
  minimax_image.py        image-01 keyframes
  minimax_video.py        MiniMax-H3 segments (image-to-video / first+last frame, resumable)
  frames.py               contact sheets, handoff frames, motion energy, loudness
  music3.py               instrumental music via the MiniMax-Music3 HF Space
  compose_hero.py         product hero frame from an official photo (cut-out + layout)
  finish.py               assembly, typography, end card, mix
  check_env.sh            preflight
```

## Responsible use

- Use brand names, logos and product photos only for brands you represent or have permission to promote. The skill makes ads; it doesn't grant trademark rights.
- Output from MiniMax-Music3 falls under the [MiniMax-Music3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-Music3): disclose AI generation when you publish it, and get authorisation from MiniMax if your organisation's revenue exceeds US$20 M/year.
- Follow each platform's rules on labelling AI-generated content.

## License

MIT — see `LICENSE`. Third-party models and fonts keep their own licenses.
