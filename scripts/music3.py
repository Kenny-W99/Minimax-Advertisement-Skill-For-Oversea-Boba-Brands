"""Generate an instrumental ad track with the open-source MiniMax-Music3 through its official
Hugging Face Space (no GPU needed locally).

usage: python3 music3.py brief.json out.wav [--min-seconds 25] [--tries 3]

brief.json:
{
  "title": "...", "duration": 26, "seed": 11,
  "global_meta": "Basic Attributes: bpm is 78. key is D, and scale is major. <genre>. Global Emotional Progression: <timed arc per act>. Sonics & Production Profile: <...>",
  "arrangement": "Primary: ... Secondary: ... Groove: ...",
  "vocals": "Instrumental, no vocals. The lead melodic role is carried by ...",
  "lyrics": "[intro]\n\n[instrumental]\n\n[instrumental]\n\n[outro]"
}

Requires: pip install gradio_client
License of outputs: MiniMax-Music3 Community License — disclose AI generation when shared publicly.
"""
import argparse, json, os, random, shutil, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("brief"); ap.add_argument("out")
ap.add_argument("--min-seconds", type=float, default=None); ap.add_argument("--tries", type=int, default=3)
ap.add_argument("--space", default="MiniMaxAI/MiniMax-Music3")
a = ap.parse_args()
try:
    from gradio_client import Client
except ImportError:
    sys.exit("gradio_client is missing: pip install gradio_client")

b = json.load(open(a.brief, encoding="utf-8"))
need = a.min_seconds or (b.get("duration", 25) - 1)
# The Space only accepts the state as a dict. A JSON string silently falls back to its demo song (with vocals).
state = {"mode": "studio", "description": "Instrumental, no vocals.", "instrumental": True,
         "title": b.get("title", "ad music"), "lyrics": b.get("lyrics", "[intro]\n\n[instrumental]\n\n[outro]"),
         "global_meta": b["global_meta"], "arrangement": b.get("arrangement", ""),
         "vocals": b.get("vocals", "Instrumental, no vocals.")}

def duration(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

token = os.environ.get("HF_TOKEN")   # optional: a logged-in Hugging Face account gets more ZeroGPU quota
try:
    client = Client(a.space, hf_token=token) if token else Client(a.space)
except Exception as e:
    sys.exit(f"could not reach the Space {a.space}: {e}")
seed = b.get("seed", random.randint(1, 10_000))
audio = None
for attempt in range(a.tries):
    try:
        res = client.predict(state, b.get("duration", 25), seed, False, 0, b.get("steps", 30), b.get("guidance", 1.7),
                             api_name="/studio_generate")
    except Exception as e:
        msg = str(e)
        if audio is not None:   # keep the best previous result instead of failing
            print(json.dumps({"warning": f"retry failed ({msg[:160]}); keeping previous track"})); break
        if "quota" in msg.lower() or "gpu" in msg.lower():
            sys.exit("Hugging Face ZeroGPU quota exhausted (the free tier allows roughly one ~25 s track per day). "
                     "Options: wait and retry later, set HF_TOKEN for a logged-in account with more quota, "
                     "self-host MiniMax-Music3 on a CUDA GPU, or fix the existing track in post "
                     "(edit.json music.offset / music.envelope). Details: " + msg[:300])
        sys.exit(f"music generation failed: {msg[:500]}")
    audio = next((r for r in res if isinstance(r, str) and r.lower().endswith((".wav", ".mp3", ".flac"))), None)
    if audio is None:
        audio = next((r.get("path") or r.get("value") for r in res if isinstance(r, dict) and (r.get("path") or r.get("value"))), None)
    if not audio:
        sys.exit(f"no audio returned: {str(res)[:500]}")
    dur = duration(audio)
    print(json.dumps({"attempt": attempt + 1, "seed": seed, "seconds": round(dur, 2)}), flush=True)
    if dur >= need:
        shutil.copy(audio, a.out); print(json.dumps({"saved": a.out, "seed": seed, "seconds": round(dur, 2)})); break
    seed += 101
else:
    shutil.copy(audio, a.out)
    print(json.dumps({"saved": a.out, "warning": f"track is {dur:.1f}s, shorter than {need}s"}))
if not os.path.exists(a.out) and audio is not None:
    shutil.copy(audio, a.out); print(json.dumps({"saved": a.out, "warning": "kept a track that failed a check"}))
