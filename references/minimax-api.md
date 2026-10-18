# MiniMax API notes (API mode)

Verified October 2026. Prices and models change, so check https://platform.minimax.io/docs/pricing/overview when in doubt.

## Auth and hosts

- `Authorization: Bearer $MINIMAX_API_KEY`. H3 needs a **pay-as-you-go** key (platform.minimax.io → API Keys → create; top up under Billing).
- Host: `https://api.minimax.io` (international) or `https://api.minimaxi.com` (mainland). The key and host must belong to the same region.
- Never print or store the key in files. Read it from the environment.

## Images — `image-01` ($0.0035 / image)

`POST /v1/image_generation`

```json
{"model": "image-01", "prompt": "...", "aspect_ratio": "9:16", "n": 3, "response_format": "url", "prompt_optimizer": false}
```

Prompt length must be **under 1500 characters** (status 2013 otherwise). Returns `data.image_urls` (720×1280 for 9:16). `base_resp.status_code == 0` means success. `subject_reference` exists but is meant for people and doesn't hold cartoon characters. It's the only image model on the API.

Script: `scripts/minimax_image.py`.

## Video — `MiniMax-H3` (768P $0.08/s, 2K $0.13/s)

Create: `POST /v2/video_generation`

```json
{
  "model": "MiniMax-H3",
  "content": [
    {"type": "text", "text": "<three-field prompt>"},
    {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}, "role": "first_frame"},
    {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}, "role": "last_frame"}
  ],
  "resolution": "768P",
  "duration": 5
}
```

- `resolution`: `768P` | `2K`; `duration`: integer 4–15. With an image input, the aspect ratio follows the image (`ratio` is ignored).
- Images: JPG/PNG/WEBP, ≤ 30 MB, sides 256–5760 px, aspect 0.4–2.5. If the first and last frames differ in size, resize the last frame to match the first.
- Returns `{"task_id": ...}`.
- Query: `GET /v2/query/video_generation/{task_id}` → `task.status` ∈ `queued | running | succeeded | failed | cancelled`; the video is at `task.content.url` (time-limited, download promptly). Tasks are queryable for 7 days. Usually done in 1–4 min.
- Output: 768P 9:16 → 768×1344, 24 fps, stereo audio at 32 kHz. A 5 s request yields 124 frames.
- H3 always generates audio. Prompt for SFX only and add music in post.
- Error bodies: `{"type":"error","error":{...}}`; 422 / code 1026 = blocked by content moderation. In testing it was triggered by a **child character plus body or touch verbs** ("a kindergartener squeezes her head") and is likely with violence words ("smash"). Rephrase neutrally ("a small cartoon character", "taps", "pats") and resubmit. Treat a blocked attempt as possibly billed and count it against the budget. `minimax_video.py` prints this hint.
- `MiniMax-H3-Max` is faster and cheaper (480P/768P, 5–15 s) and has `extra.prompt_expansion_mode`. It wasn't tested for this skill.

Script: `scripts/minimax_video.py out.mp4 prompt.txt first.png [last.png] --res 768P --dur 5`. Use `--task <id>` to resume polling a task that was already created (no second charge).

## Music

The paid music API returns status 2153 ("no longer available to new users") for new accounts. Use `scripts/music3.py` (open-source MiniMax-Music3 via its HF Space); see `audio-design.md`.

## Speech (optional)

T2A v2 with `speech-2.8-hd` ($100 / M chars) or `speech-2.8-turbo` ($60 / M chars).

## Typical cost of one ad (768P)

| Item | Cost |
|---|---|
| Keyframes (~10–20 images incl. retries) | ~$0.05 |
| 5 segments × 5 s, plus ~2 retries | ~$2.8 |
| Music (HF Space) | free (subject to Space quota) |
| **Total** | **≈ $3** (2K final ≈ +$3.3) |
