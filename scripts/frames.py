"""Frame and audio helpers for QA and relay handoffs (needs ffmpeg/ffprobe on PATH).

  frames.py sheet  clip.mp4 sheet.jpg [--fps 4] [--width 150] [--cols 10]   contact sheet
  frames.py grab   clip.mp4 4.9 out.png                                     one frame at t seconds (handoff frame)
  frames.py grab   clip.mp4 100 out.png --frame                             frame number N (0-based; matches edit.json in/out)
  frames.py last   clip.mp4 out.png                                         final frame
  frames.py info   clip.mp4                                                 size, fps, frames, duration
  frames.py motion clip.mp4                                                 mean frame difference (stiff≈0.5, lively≈3)
  frames.py loudness audio.wav [--step 0.5]                                 RMS dBFS per step (shows the music arc)
  frames.py fit    image.png ref.png out.png                                resize image to ref's size
"""
import json, re, subprocess, sys

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def info(path):
    r = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate,nb_read_frames:format=duration", "-of", "json", path])
    d = json.loads(r.stdout); s = d["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return {"width": s["width"], "height": s["height"], "fps": round(int(num) / int(den), 3),
            "frames": int(s.get("nb_read_frames", 0)), "duration": float(d["format"]["duration"])}

def main(argv):
    if len(argv) < 2: sys.exit(__doc__)
    cmd, args = argv[1], argv[2:]
    opt = lambda name, default: (args[args.index(name) + 1] if name in args else default)
    if cmd == "sheet":
        clip, out = args[0], args[1]
        fps, width, cols = float(opt("--fps", 4)), int(opt("--width", 150)), int(opt("--cols", 10))
        n = max(1, int(info(clip)["duration"] * fps + 0.999)); rows = (n + cols - 1) // cols
        r = run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", f"fps={fps},scale={width}:-1,tile={cols}x{rows}",
                 "-frames:v", "1", out])
        print(r.stderr or json.dumps({"sheet": out, "frames": n, "fps": fps}))
    elif cmd == "grab":
        clip, t, out = args[0], args[1], args[2]
        if "--frame" in args:
            r = run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", f"select=eq(n\\,{int(t)})", "-vsync", "0", "-frames:v", "1", out])
        else:
            r = run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", clip, "-frames:v", "1", out])
        print(r.stderr or out)
    elif cmd == "last":
        clip, out = args[0], args[1]
        r = run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", clip, "-frames:v", "1", out]); print(r.stderr or out)
    elif cmd == "info":
        print(json.dumps(info(args[0])))
    elif cmd == "motion":
        r = run(["ffmpeg", "-hide_banner", "-i", args[0], "-vf", "scale=184:-1,format=gray,tblend=all_mode=difference,"
                 "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"])
        vals = [float(v) for v in re.findall(r"YAVG=([0-9.]+)", r.stderr)]
        print(json.dumps({"mean_motion": round(sum(vals) / max(1, len(vals)), 2), "frames": len(vals)}))
    elif cmd == "loudness":
        path, step = args[0], float(opt("--step", 0.5))
        sr = int(json.loads(run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate",
                                 "-of", "json", path]).stdout)["streams"][0]["sample_rate"])
        r = run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"asetnsamples=n={int(sr * step)},astats=metadata=1:reset=1,"
                 "ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"])
        vals = re.findall(r"RMS_level=(-?[0-9.]+|-inf)", r.stderr)
        print(" ".join(f"{i * step:.1f}s:{v if v == '-inf' else round(float(v))}" for i, v in enumerate(vals)))
    elif cmd == "fit":
        from PIL import Image
        img, ref, out = args
        Image.open(img).convert("RGB").resize(Image.open(ref).size, Image.LANCZOS).save(out); print(out)
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main(sys.argv)
