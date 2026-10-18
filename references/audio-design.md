# Stages 4 & 6 · Audio design

Three layers: **music** (one continuous instrumental track), **sound effects** (from each H3 segment's native audio), and **voice** (none by default; silent autoplay is the norm on social feeds).

## 1. Music follows the acts

`audio_plan.json` gives each act a mood, an energy level (1–5) and lead instruments, all derived from the brand:

| Brand tone | Palette starting point |
|---|---|
| Classical Chinese / poetic | guzheng, xiao or dizi flute, soft piano, light strings |
| Cute / playful | ukulele, glockenspiel, pizzicato, kalimba |
| Premium / minimal | felt piano, warm pads, soft cello |
| Street / trendy | lo-fi beat, Rhodes, vinyl texture, soft city-pop guitar |
| Unknown | **relaxed and soothing** by default: ~70–85 BPM lo-fi acoustic, felt piano, nylon guitar, kalimba; no claps, no heavy drums, no drops |

The user preferred calm over bouncy in testing, so keep energy modest even in the "fun" act. Change instrumentation more than volume.

## 2. Transitions that follow the picture without jolting

**Generate early, fit late.** Handoff choices move act boundaries by a second or more, so the planned times are only approximate. The free music quota, though, is often one track per day, and it ran out before the first call in one test. So generate the track at Stage 4 from the storyboard's planned times, plus ~2 s of slack at each end. After the cut is final (sum of trimmed segment lengths before each boundary), fit it with `offset` / `envelope` (point 6 below). Regenerate with the real times only if the fit is poor and quota remains.

1. **Generate one continuous track** whose description lays out each act with times ("0–6 s: a few sleepy felt-piano notes; at about 6.5 s a glockenspiel twinkle marks the first sip and a gentle nylon-guitar groove begins; from 12 s airy pads and kalimba, floating; from 18.5 s it settles into a soft resolved chord with a bell"). Transitions written inside one generation come out musically connected.
2. **One key, one tempo** for the whole ad. Make change with instruments, density, register and energy, or a half-time feel. Don't switch keys or jump tempo.
3. **Snap act boundaries to bar lines.** Bar = 60 / BPM × 4 s (78 BPM → 3.08 s). You control segment trims, so nudge the handoff or end-card hold by a few frames to put each act boundary on a bar line.
4. **Bridge every boundary**: a swell or riser, a held note, a filter opening, or a sound effect synced to the visual cue (the sip "ding", a lid pop). Never hard-cut the music.
5. **Fallback when you can regenerate.** If the sections land more than ~0.5 s off the act times, generate one short cue per act in the same key and tempo, then join them with a 1–1.5 s equal-power crossfade centred on a downbeat at the boundary.
6. **Fallback when you can't regenerate** (quota gone, which is common on the free Space). Fix it in post with `edit.json`:
   - `music.offset` (seconds to skip at the start of the track) slides the track so its biggest change lands on your strongest visual change.
   - `music.envelope` (`[[t, dB], …]`, linear between points) rides down a jump or swells into a boundary, e.g. `[[0,0],[11,0],[12.5,-7],[21,-7]]`.
   - Look at `frames.py loudness` before and after.

## 3. Generating with MiniMax-Music3

The MiniMax music API is closed to new users (status 2153). Use the open-source **MiniMax-Music3**:
- `scripts/music3.py brief.json out.wav`. It calls the official Hugging Face Space `MiniMaxAI/MiniMax-Music3` (`/studio_generate`) through `gradio_client`. Local inference needs a CUDA GPU (≥ 8 GB with offload), which Apple Silicon can't provide, so the Space is the portable path. With your own GPU, self-host per the model card.
- Brief fields: `global_meta` (BPM, key, genre, the timed emotional progression, production notes; the arc goes here), `arrangement` (which instruments enter and leave, and when), `vocals: "Instrumental, no vocals. The lead melodic role is carried by …"`, `lyrics` made only of section tags (`[intro]`, `[instrumental]`, `[outro]` on their own lines), `duration` = ad length + 1 s, `seed`.
- Gotcha: the Space needs the state as an object. A JSON string silently falls back to its built-in demo song, which has vocals. `music3.py` handles this.
- **Quota.** The free ZeroGPU tier allowed about one ~25 s generation per day in testing (each call reserves ~72 s of GPU). Get the brief right the first time. Setting `HF_TOKEN` (a logged-in Hugging Face account) raises the quota. Hugging Face PRO gives 40 min of ZeroGPU per day, roughly 30 tracks, which is the practical choice for anyone making ads regularly. `music3.py` prints a clear message when the quota is gone.
- Checks: run speech recognition on the result and expect no lyrics. Use any available ASR: local `whisper` / `mlx_whisper` / `faster-whisper` with a tiny model, or the agent's own audio understanding. Hallucinated fillers like "Thank you" on pure music are normal. If no ASR is available, rely on the instrumental-only brief and say in the report that vocals were not machine-checked. The real duration must be ≥ the ad length, because the Space sometimes returns shorter audio (18 s for a 26 s request), so regenerate with a new seed if it's short. The loudness curve should be quiet at the start, show change near each act boundary, and have no jumps above ~6 dB between adjacent half-seconds.
## No music available

If no track can be generated at all (quota exhausted, Space down, no built-in tool):
1. Deliver anyway, but make the silence intentional. Extend the last SFX tail and add a short sound-design sting on the hero shot (a chime or the drink's own sound from the clips). Fade the end card's audio out rather than leaving dead air.
2. Write `music_brief.json` and the exact re-run commands into `report.md` (`music3.py brief.json music.wav`, then `finish.py edit.json final.mp4` with `music` set). Adding the music later then takes one step.
3. Flag it at the top of the report: "delivered without music".

With a Hugging Face account, `HF_TOKEN` gives a larger quota. With a CUDA GPU, self-host MiniMax-Music3.

- License: MiniMax-Music3 Community License. Publicly shared outputs must disclose that they are AI-generated. Organisations above US$20 M annual revenue need written authorisation. Put this in `report.md`.

Inside MiniMax Agent, a built-in music tool may be available. Use it with the same brief content if so.

## 4. Sound effects

H3 generates audio with each segment. Ask for SFX only in `overall_soundscape` and set `non_diegetic_music: none`. Music generated per segment would break at every seam. List effects in beat order, concretely ("a long satisfying slurp through a straw", "a soft fluffy plop"). `finish.py` keeps them as the SFX layer, short-fades each seam, and mixes the music underneath (default music gain 0.55–0.9 depending on track loudness; final loudness normalised to -16 LUFS).

## 5. Voice (optional)

Only if the user asks. Use MiniMax TTS (speech-2.8) in the market language. Keep it to one short line in the payoff act, and duck the music by ~6 dB under it.
