"""Assemble relay segments into the finished ad.

  python3 finish.py edit.json final.mp4

Does: frame-accurate trims and concat, SFX seam fades, optional pure-white cleanup and "on twos",
optional per-segment virtual camera, end-card pull-back with feathered edges, animated typography
(headline fade/rise, drawn-on accent, letter-by-letter note, logo/brand fade), music mix and
-16 LUFS loudness. Paths in edit.json are relative to edit.json. Sizes (font px, accent width)
are specified for a 768-px-wide frame and scale automatically to the real width (e.g. 2K).
See references/schemas.md § edit.json.
"""
import json, math, os, random, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

cfg = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
base_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda f: f if os.path.isabs(f) else os.path.join(base_dir, f)
FPS = 24
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

segs = cfg["segments"]
probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "json", P(segs[0]["file"])],
                                  capture_output=True, text=True).stdout)["streams"][0]
W, H = cfg.get("width", probe["width"]), cfg.get("height", probe["height"])
U = W / 768                                         # layout unit: configs are authored at 768 px wide
def edge_color(path):
    """Median colour of the border of the last frame of the last segment: the end-card canvas must match it,
    otherwise the pull-back shows a visible rectangle."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-0.2", "-i", path, "-frames:v", "1", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True)
    im = Image.frombytes("RGB", (probe["width"], probe["height"]), r.stdout[:probe["width"] * probe["height"] * 3])
    w, h = im.size; px = im.load(); edge = [px[x, y] for x in range(0, w, 4) for y in (2, h - 3)] + [px[x, y] for y in range(0, h, 4) for x in (2, w - 3)]
    return tuple(sorted(c[i] for c in edge)[len(edge) // 2] for i in range(3))
BG = hexrgb(cfg["background"]) if cfg.get("background") else edge_color(P(segs[-1]["file"]))
hold = cfg.get("hold_end", 2.0)

# ---------- 1. frame-accurate concat + SFX ----------
inputs, fv, fa, labels = [], [], [], []
for i, s in enumerate(segs):
    inputs += ["-i", P(s["file"])]
    a, b = s["in"], s["out"]                       # frame numbers, [a, b)
    t0, t1 = a / FPS, b / FPS
    last = i == len(segs) - 1
    fv.append(f"[{i}:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,scale={W}:{H}:flags=lanczos,fps={FPS}"
              + (f",tpad=stop_mode=clone:stop_duration={hold}" if last else "") + f"[v{i}]")
    fade_out = max(0.0, t1 - t0 - 0.08)
    fa.append(f"[{i}:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
              f"afade=t=in:d=0.04,afade=t=out:st={fade_out:.3f}:d=0.08" + (f",apad=pad_dur={hold}" if last else "") + f"[a{i}]")
    labels.append(f"[v{i}][a{i}]")
levels = ",colorlevels=rimin=0.02:gimin=0.02:bimin=0.02:rimax=0.955:gimax=0.955:bimax=0.955" if cfg.get("whites", False) else ""
twos = ",fps=12,fps=24" if cfg.get("on_twos") else ""
graph = ";".join(fv + fa) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=1:a=1[cv][ca];[cv]format=rgb24{levels}{twos}[vout]"
base = os.path.join(tempfile.mkdtemp(), "base.mov")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[vout]", "-map", "[ca]",
                "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv444p", "-c:a", "pcm_s16le", base], check=True)

# ---------- 2. virtual camera, end card, typography ----------
ease = lambda x: 1 - (1 - max(0.0, min(1.0, x))) ** 3
ec = cfg.get("endcard", {})
INK = hexrgb(ec.get("ink", "#262626"))
def load_font(spec):
    f = ImageFont.truetype(P(spec["font"]), int(spec["size"] * U), index=spec.get("index", 0))
    if "weight" in spec:   # variable fonts (e.g. Noto Serif SC from Google Fonts) default to their lightest instance
        try:
            axes = f.get_variation_axes()
        except Exception:
            return f           # static font: the file already is a single weight
        try:
            f.set_variation_by_axes([spec["weight"] if a.get("name", b"").lower() == b"weight" else a["default"] for a in axes])
        except Exception as e:
            print(json.dumps({"warning": f"could not set weight on {spec['font']}: {e}"}))
    return f
sl, acc, note, logo_cfg, brand = ec.get("slogan"), ec.get("accent") or ec.get("swoosh"), ec.get("note") or ec.get("hand"), ec.get("logo"), ec.get("brand")
if acc and "type" not in acc: acc["type"] = "swoosh"
F_SL = load_font(sl) if sl else None
F_NOTE = load_font(note) if note else None
F_BRAND = load_font(brand) if brand else None
LOGO = None
if logo_cfg:
    LOGO = Image.open(P(logo_cfg["file"])).convert("RGBA")
    # "width" is a fraction of frame width, "max_height" a fraction of frame height (tall logos), "y" is the TOP edge
    lw = int(W * logo_cfg.get("width", 0.2)); lh_ = int(LOGO.height * lw / LOGO.width)
    mh = int(H * logo_cfg.get("max_height", 0.08))
    if lh_ > mh: lw, lh_ = int(lw * mh / lh_), mh
    LOGO = LOGO.resize((lw, lh_), Image.LANCZOS)
jit = [(r.uniform(-6, 6), r.uniform(-3, 3)) for r in [random.Random(7)] for _ in range(400)]

def accent(d, x0, x1, y, k, lh=0):
    color = hexrgb(acc["color"]) + (255,); wdt = max(1, int(acc.get("width", 5) * U))
    if acc["type"] == "swoosh":
        pts = [(x0 + (x1 - x0) * u, y - 10 * U * math.sin(math.pi * u) + 2.2 * U * math.sin(u * 17)) for u in (j / 59 for j in range(60))]
        pts += [(x1 - 4 * U, y + 6 * U), (x1 + 26 * U, y - 6 * U), (x1 + 10 * U, y + 8 * U), (x1 + 42 * U, y - 2 * U)]
        d.line(pts[:max(2, int(len(pts) * k))], fill=color, width=wdt, joint="curve")
    elif acc["type"] == "rule":
        d.line([(x0, y), (x0 + (x1 - x0) * k, y)], fill=color, width=wdt)
    elif acc["type"] == "seal":
        # a small square stamp to the right of the last headline line, vertically centred on it
        s = int(acc.get("size", 30) * U); cx = x1 + 52 * U; cy = y - 18 * U - lh * 0.5
        d.rectangle((cx, cy - s / 2, cx + s, cy + s / 2), fill=hexrgb(acc["color"]) + (int(255 * k),))

def text_layer(t):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer); T = ec["text_start"]
    if sl:
        lh = int(F_SL.size * 1.32); y0 = int(sl["y"] * H)
        for i, line in enumerate(sl["lines"]):
            k = ease((t - T - 0.15 * i) / 0.6)
            if k > 0:
                w = d.textlength(line, font=F_SL)
                d.text(((W - w) / 2, y0 + i * lh + (1 - k) * 16 * U), line, font=F_SL, fill=INK + (int(255 * k),))
        if acc and acc["type"] != "none":
            k = ease((t - T - 0.75) / 0.45)
            if k > 0:
                wmax = max(d.textlength(l, font=F_SL) for l in sl["lines"])
                accent(d, (W - wmax) / 2 + 10 * U, (W + wmax) / 2 - 40 * U, y0 + len(sl["lines"]) * lh + 18 * U, k, lh)
    if note:
        shown = int(max(0, (t - T - note.get("delay", 1.0)) * note.get("cps", 12))); idx = 0
        hx, hy, sz = int(note["x"] * W), int(note["y"] * H), F_NOTE.size
        hl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
        vertical = note.get("vertical", False)   # vertical CJK writing: columns right-to-left, characters top-to-bottom
        for li, word in enumerate(note["words"]):
            x = hx - li * sz * 1.25 if vertical else hx
            yv = hy
            for ch in word:
                if idx >= shown: break
                jx, jy = jit[idx % len(jit)]
                g = Image.new("RGBA", (sz * 2, sz * 2), (0, 0, 0, 0))
                ImageDraw.Draw(g).text((sz // 2, sz // 3), ch, font=F_NOTE, fill=INK + (255,))
                if vertical:
                    hl.alpha_composite(g.rotate(jx * 0.5, resample=Image.BICUBIC), (int(x - sz // 2 + jy * U), int(yv - sz // 3)))
                    yv += sz * 1.08
                else:
                    hl.alpha_composite(g.rotate(jx, resample=Image.BICUBIC), (int(x - sz // 2), int(hy + li * sz * 1.15 + jy * U - sz // 3)))
                    x += hd.textlength(ch, font=F_NOTE) + U
                idx += 1
        layer.alpha_composite(hl.rotate(note.get("rotate", -5), center=(hx, hy), resample=Image.BICUBIC))
    k = ease((t - T - 0.3) / 0.7)
    if k > 0 and LOGO is not None:
        lg = LOGO.copy(); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * k)))
        layer.alpha_composite(lg, ((W - lg.width) // 2, int(logo_cfg.get("y", 0.9) * H)))
    elif k > 0 and brand:
        sp = brand.get("tracking", 6) * U; txt = brand["text"]
        x = (W - (sum(d.textlength(c, font=F_BRAND) + sp for c in txt) - sp)) / 2
        for c in txt:
            d.text((x, int(brand["y"] * H)), c, font=F_BRAND, fill=INK + (int(255 * k),)); x += d.textlength(c, font=F_BRAND) + sp
    return layer

seg_cam, f0 = [], 0
for s in segs:
    nfr = s["out"] - s["in"]
    if "zoom" in s:
        seg_cam.append((f0, f0 + nfr, s["zoom"], s.get("cy", [0.5, 0.5]), s.get("ramp", nfr / FPS)))
    f0 += nfr

def seg_camera(img, n):
    for a, b, (z0, z1), (c0, c1), r in seg_cam:
        if a <= n < b:
            k = ease((n - a) / FPS / r) if r > 0 else 1
            z, cy = z0 + (z1 - z0) * k, c0 + (c1 - c0) * k
            if z <= 1.0001: return img
            cw, ch = W / z, H / z; y = min(max(0, H * cy - ch / 2), H - ch)
            return img.crop((int((W - cw) / 2), int(y), int((W + cw) / 2), int(y + ch))).resize((W, H), Image.LANCZOS)
    return img

_masks = {}
def feather(w, h):
    r = int(60 * U)
    if (w, h) not in _masks:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rectangle((r, r, w - r, h - r), fill=255)
        _masks[(w, h)] = m.filter(ImageFilter.GaussianBlur(r / 2))
    return _masks[(w, h)]

pb = ec.get("pullback")
def endcard_camera(img, t):
    if not pb or t < pb["start"]: return img
    k = ease((t - pb["start"]) / pb["dur"])
    s = 1 - (1 - pb["scale"]) * k + max(0, t - pb["start"] - pb["dur"]) * pb.get("drift", 0.006)
    nw, nh = int(W * s), int(H * s); small = img.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), BG); pos = ((W - nw) // 2, int((H - nh) / 2 + pb.get("shift_y", 0) * H * k))
    canvas.paste(small, pos, feather(nw, nh) if s < 1 else None)
    return canvas

# ---------- 3. encode with music ----------
music = cfg.get("music")

def envelope_expr(points):
    """[[t, dB], ...] -> piecewise-linear ffmpeg volume expression (gain in dB, linear between points)."""
    pts = sorted(points); e = f"{pts[-1][1]}"
    for (t0, g0), (t1, g1) in reversed(list(zip(pts, pts[1:]))):
        e = f"if(lt(t,{t1}),{g0}+({g1}-{g0})*(t-{t0})/({t1}-{t0}),{e})"
    return f"if(lt(t,{pts[0][0]}),{pts[0][1]},{e})"

def mix_graph(norm):
    sfx = f"[1:a]volume={cfg.get('sfx_gain', 1.0)}[s]"
    if not music:
        return f"[1:a]volume={cfg.get('sfx_gain', 1.0)},{norm}[aout]"
    m = f"[2:a]aresample=48000,aformat=channel_layouts=stereo"
    if music.get("offset"): m += f",atrim=start={music['offset']},asetpts=PTS-STARTPTS"   # skip the track's first seconds
    m += f",volume={music.get('gain', 0.6)}"
    if music.get("envelope"): m += f",volume='pow(10,({envelope_expr(music['envelope'])})/20)':eval=frame"
    m += f",afade=t=out:st={music.get('fade_out_at', 20)}:d={music.get('fade_out', 1.5)}[m]"
    return f"{m};{sfx};[s][m]amix=inputs=2:duration=first:normalize=0,{norm}[aout]"

# two-pass loudness: measure the mix first, then normalise linearly to -16 LUFS / -1.5 dBTP.
# A silent dummy input 0 keeps stream indices identical to the encode pass (0 = video pipe, 1 = base, 2 = music).
inputs_a = ["-i", base] + (["-i", P(music["file"])] if music else [])
meas = subprocess.run(["ffmpeg", "-hide_banner", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", *inputs_a,
                       "-filter_complex", mix_graph("loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json"),
                       "-map", "[aout]", "-f", "null", "-"], capture_output=True, text=True).stderr
try:
    js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    norm = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
            f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
except (ValueError, KeyError):
    norm = "loudnorm=I=-16:TP=-1.5"
norm += ",aresample=48000"
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc_cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", base]
if music:
    enc_cmd += ["-i", P(music["file"])]
amix = mix_graph(norm)
enc = subprocess.Popen(enc_cmd + ["-filter_complex", amix, "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-crf", "17",
                                  "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                                  "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
fs, n = W * H * 3, 0
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs: break
    t = n / FPS
    img = endcard_camera(seg_camera(Image.frombytes("RGB", (W, H), buf), n), t)
    if ec and t >= ec.get("text_start", 1e9):
        img = img.convert("RGBA"); img.alpha_composite(text_layer(t)); img = img.convert("RGB")
    enc.stdin.write(img.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(json.dumps({"saved": out, "frames": n, "seconds": round(n / FPS, 2), "size": [W, H]}))
