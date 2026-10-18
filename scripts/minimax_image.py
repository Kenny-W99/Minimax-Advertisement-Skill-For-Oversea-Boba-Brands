"""Generate keyframe candidates with MiniMax image-01.

usage:
  python3 minimax_image.py --prompt-file k0.txt --out-dir keyframes --name K0 [--n 3] [--aspect 9:16]
  python3 minimax_image.py --prompt "..." --out-dir keyframes --name K_end

Saves <out-dir>/<name>_0.jpg … Reads MINIMAX_API_KEY / MINIMAX_API_HOST from the environment.
"""
import argparse, json, os, sys, time, urllib.error, urllib.request

ap = argparse.ArgumentParser()
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--prompt"); g.add_argument("--prompt-file")
ap.add_argument("--out-dir", required=True); ap.add_argument("--name", required=True)
ap.add_argument("--n", type=int, default=3); ap.add_argument("--aspect", default="9:16")
a = ap.parse_args()

key = os.environ.get("MINIMAX_API_KEY") or sys.exit("MINIMAX_API_KEY is not set")
host = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")
prompt = a.prompt if a.prompt else open(a.prompt_file, encoding="utf-8").read().strip()
if len(prompt) >= 1500:
    sys.exit(f"prompt is {len(prompt)} characters; image-01 rejects >= 1500 (status 2013). Keep image prompts "
             "to the style-lock sentence + staging + subject (don't paste the video blocks into image prompts).")
os.makedirs(a.out_dir, exist_ok=True)

body = {"model": "image-01", "prompt": prompt, "aspect_ratio": a.aspect, "n": a.n,
        "response_format": "url", "prompt_optimizer": False}
for attempt in range(3):
    try:
        req = urllib.request.Request(f"{host}/v1/image_generation", json.dumps(body).encode(),
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        d = json.load(urllib.request.urlopen(req, timeout=180))
        break
    except (urllib.error.URLError, TimeoutError) as e:
        if attempt == 2: sys.exit(f"request failed: {e}")
        time.sleep(5 * (attempt + 1))
if d.get("base_resp", {}).get("status_code") != 0:
    sys.exit(f"image generation failed: {d.get('base_resp')}")
paths = []
for i, u in enumerate(d["data"]["image_urls"]):
    p = os.path.join(a.out_dir, f"{a.name}_{i}.jpg"); urllib.request.urlretrieve(u, p); paths.append(p)
print(json.dumps({"saved": paths}))
