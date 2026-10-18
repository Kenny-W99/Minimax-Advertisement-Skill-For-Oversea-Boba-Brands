"""Build the product hero frame (K_end) from an official product photo.

  python3 compose_hero.py product.jpg K_end.png --size 768x1344 \
      [--bg "#F3EBDD" | --bg-image background.png] [--height 0.5] [--bottom 0.1] [--pullback 0.74] \
      [--tolerance 28] [--shadow 0.25] [--no-cutout]

- Cut-out: if the photo has an alpha channel it is used as is. Otherwise the background is removed by
  flood-filling from the borders over pixels close to the border color (works for studio/plain backgrounds;
  use --no-cutout for busy photos and pick a photo with a plain background instead).
- Layout: the product is scaled so that, AFTER finish.py's end-card pull-back (--pullback, default 0.74),
  it fills --height of the frame height. Its base sits --bottom above the bottom edge. This leaves the upper
  third free for the headline.
- A soft contact shadow is added under the product (--shadow opacity, 0 to disable).
- Lifestyle photos (product on moss, in a hand…): pass --mask polygon.json (outline points of the product).
- With --bg-image, set --base-y to the spot where the product should stand (e.g. the centre of a ring of
  ingredients) and --height for its size in the frame; the background shrinks together with it in the pull-back.
- --pullback and --shift-y must equal the values in edit.json endcard.pullback, or the product lands in the wrong place.
"""
import argparse
from collections import deque
from PIL import Image, ImageDraw, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("photo"); ap.add_argument("out")
ap.add_argument("--size", default="768x1344"); ap.add_argument("--bg", default="#FFFFFF"); ap.add_argument("--bg-image")
ap.add_argument("--height", type=float, default=0.5); ap.add_argument("--bottom", type=float, default=0.1)
ap.add_argument("--pullback", type=float, default=0.74); ap.add_argument("--tolerance", type=int, default=28)
ap.add_argument("--shadow", type=float, default=0.25); ap.add_argument("--no-cutout", action="store_true")
ap.add_argument("--crop", help="x0,y0,x1,y1 in source pixels: crop to the product first (posters, menus, multi-item photos)")
ap.add_argument("--mask", help="JSON file with a polygon [[x,y],...] in source pixels (after --crop) outlining the product; "
                               "use for lifestyle photos where automatic cut-out fails")
ap.add_argument("--shift-y", type=float, default=0.0, help="must equal edit.json endcard.pullback.shift_y")
ap.add_argument("--base-y", type=float, help="absolute position of the product's base as a fraction of frame height "
                                             "(use with --bg-image so the product stands on a spot in the background; "
                                             "disables the pull-back compensation of the position)")
a = ap.parse_args()
W, H = map(int, a.size.lower().split("x"))

src = Image.open(a.photo)
if a.crop:
    src = src.crop(tuple(int(v) for v in a.crop.split(",")))
if a.mask:
    import json as _json
    poly = [tuple(p) for p in _json.load(open(a.mask))]
    m = Image.new("L", src.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    prod = src.convert("RGBA"); prod.putalpha(m.filter(ImageFilter.GaussianBlur(1.0)))
elif src.mode == "RGBA" and src.getchannel("A").getextrema()[0] < 250:
    prod = src
elif a.no_cutout:
    prod = src.convert("RGBA")
else:
    rgb = src.convert("RGB"); w, h = rgb.size; px = rgb.load()
    border = [px[x, 0] for x in range(w)] + [px[x, h - 1] for x in range(w)] + [px[0, y] for y in range(h)] + [px[w - 1, y] for y in range(h)]
    ref = tuple(sorted(c[i] for c in border)[len(border) // 2] for i in range(3))   # median border color
    close = lambda c: sum(abs(c[i] - ref[i]) for i in range(3)) <= a.tolerance * 3
    mask = Image.new("L", (w, h), 255); m = mask.load(); seen = bytearray(w * h); q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft(); i = y * w + x
        if seen[i]: continue
        seen[i] = 1
        if not close(px[x, y]): continue
        m[x, y] = 0
        if x > 0: q.append((x - 1, y))
        if x < w - 1: q.append((x + 1, y))
        if y > 0: q.append((x, y - 1))
        if y < h - 1: q.append((x, y + 1))
    removed = 1 - sum(1 for v in mask.getdata() if v) / (w * h)
    # count separate large foreground blobs on a small grid: more than one means a poster / multi-item photo
    sm = mask.resize((64, max(1, int(64 * h / w))), Image.NEAREST); sw, shh = sm.size; g = sm.load(); lab = {}; blobs = 0
    for yy in range(shh):
        for xx in range(sw):
            if g[xx, yy] and (xx, yy) not in lab:
                st, n = [(xx, yy)], 0; lab[(xx, yy)] = 1
                while st:
                    cx, cy = st.pop(); n += 1
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < sw and 0 <= ny < shh and g[nx, ny] and (nx, ny) not in lab:
                            lab[(nx, ny)] = 1; st.append((nx, ny))
                blobs += n > 0.02 * sw * shh
    if blobs > 1:
        print({"warning": f"{blobs} separate objects found (logo, text, other items?). Crop to the product with "
               "--crop x0,y0,x1,y1 and check the result before using it."})
    if removed < 0.15:
        print({"warning": f"only {removed:.0%} of the photo was recognised as background; the cut-out probably failed "
               "(busy poster or textured backdrop). Use a photo of the product on a plain background, a PNG with "
               "transparency, or check the result before using it."})
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    prod = rgb.convert("RGBA"); prod.putalpha(mask)

bbox = prod.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
prod = prod.crop(bbox)
target_h = int(H * a.height / a.pullback)                 # compensate for the end-card pull-back
target_h = min(target_h, int(H * 0.9))
scale = target_h / prod.height
prod = prod.resize((max(1, int(prod.width * scale)), target_h), Image.LANCZOS)
if prod.width > W * 0.9:
    f = W * 0.9 / prod.width; prod = prod.resize((int(prod.width * f), int(prod.height * f)), Image.LANCZOS)

canvas = (Image.open(a.bg_image).convert("RGB").resize((W, H), Image.LANCZOS) if a.bg_image
          else Image.new("RGB", (W, H), a.bg)).convert("RGBA")
# place so that after pull-back the base sits `bottom` above the frame bottom
if a.base_y is not None:
    base_y = H * a.base_y
else:
    base_y = H / 2 + ((H * (1 - a.bottom)) - H / 2 - a.shift_y * H) / a.pullback
    base_y = min(base_y, H * 0.97)
x0, y0 = (W - prod.width) // 2, int(base_y - prod.height)
if a.shadow > 0:
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).ellipse((x0 + prod.width * 0.1, base_y - prod.width * 0.06, x0 + prod.width * 0.9, base_y + prod.width * 0.06), fill=int(255 * a.shadow))
    sh = sh.filter(ImageFilter.GaussianBlur(prod.width * 0.05))
    canvas = Image.alpha_composite(canvas, Image.merge("RGBA", (Image.new("L", (W, H), 0),) * 3 + (sh,)))
canvas.alpha_composite(prod, (x0, y0))
canvas.convert("RGB").save(a.out)
print({"saved": a.out, "product_px": prod.size, "position": (x0, y0)})
