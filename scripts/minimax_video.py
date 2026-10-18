"""Generate one MiniMax-H3 segment from a first frame (image-to-video) or first + last frame.

usage:
  python3 minimax_video.py out.mp4 prompt.txt first.png [last.png] [--res 768P|2K] [--dur 5]
  python3 minimax_video.py out.mp4 prompt.txt first.png --task <task_id>   # resume polling, no new charge

The last frame is resized to the first frame's size automatically (H3 crops mismatched frames).
Reads MINIMAX_API_KEY / MINIMAX_API_HOST from the environment. Prints the task id immediately so a
crashed run can be resumed with --task.
"""
import argparse, base64, io, json, mimetypes, os, sys, time, urllib.error, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("prompt"); ap.add_argument("first"); ap.add_argument("last", nargs="?")
ap.add_argument("--res", default="768P", choices=["768P", "2K"]); ap.add_argument("--dur", type=int, default=5)
ap.add_argument("--model", default="MiniMax-H3"); ap.add_argument("--task", help="resume polling an existing task id")
a = ap.parse_args()

key = os.environ.get("MINIMAX_API_KEY") or sys.exit("MINIMAX_API_KEY is not set")
host = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")
H = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

def data_url(path, size=None):
    if size:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        if im.size != size:
            im = im.resize(size, Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def call(method, path, body=None):
    for attempt in range(4):
        req = urllib.request.Request(host + path, json.dumps(body).encode() if body else None, H, method=method)
        try:
            return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:800]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(10 * (attempt + 1)); continue
            if e.code == 422 or "1026" in msg or "sensitive" in msg.lower():
                sys.exit(f"HTTP {e.code}: blocked by content moderation (1026 / sensitive). Rephrase neutrally: describe "
                         "characters as 'a small cartoon character' (avoid child/kid/kindergartener/girl/boy together with "
                         "body or touching verbs), avoid violence words (smash, hit, attack). Treat the attempt as possibly "
                         f"billed. Details: {msg}")
            sys.exit(f"HTTP {e.code}: {msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == 3: sys.exit(f"network error: {e}")
            time.sleep(10 * (attempt + 1))

def poll(tid, timeout_s=1200):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        q = call("GET", f"/v2/query/video_generation/{tid}")
        t = q.get("task", q)
        if t.get("status") in ("succeeded", "failed", "cancelled"):
            return t
        time.sleep(15)
    sys.exit(f"timed out waiting for task {tid}; resume with --task {tid}")

if a.task:
    tid = a.task
else:
    content = [{"type": "text", "text": open(a.prompt, encoding="utf-8").read().strip()},
               {"type": "image_url", "image_url": {"url": data_url(a.first)}, "role": "first_frame"}]
    if a.last:
        from PIL import Image
        size = Image.open(a.first).size
        content.append({"type": "image_url", "image_url": {"url": data_url(a.last, size)}, "role": "last_frame"})
    r = call("POST", "/v2/video_generation", {"model": a.model, "content": content,
                                             "resolution": a.res, "duration": a.dur})
    tid = r.get("task_id") or r.get("id")
    if not tid:
        sys.exit(json.dumps(r)[:800])
    print(json.dumps({"task_id": tid}), flush=True)

t = poll(tid)
if t.get("status") != "succeeded":
    err = json.dumps(t.get('error') or t)[:800]
    hint = (" — content moderation: rephrase characters neutrally ('a small cartoon character'), avoid child + body/touch "
            "wording and violence words" if ("1026" in err or "sensitive" in err.lower()) else "")
    sys.exit(f"status {t.get('status')}: {err}{hint}")
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
urllib.request.urlretrieve(t["content"]["url"], a.out)
print(json.dumps({"saved": a.out, "task_id": tid, "usage": t.get("usage")}))
