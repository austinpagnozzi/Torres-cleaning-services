#!/usr/bin/env python3
"""Procedurally generated photo-style imagery for the Torres Cleaning Services
mockup. There is no network access to a stock-photo host in this environment,
so these are painterly renders built from layered noise rather than hotlinked
or downloaded photographs — see assets/img/generated/README.md.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageChops
import pathlib, colorsys

rng = np.random.default_rng(7)
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/img/generated"
OUT.mkdir(parents=True, exist_ok=True)


def value_noise(w, h, cell, octaves=4, seed=0):
    """Cheap Perlin-like noise: random low-res grids upsampled with bicubic
    interpolation, summed across a few octaves."""
    r = np.random.default_rng(seed)
    total = np.zeros((h, w), dtype=np.float64)
    amp = 1.0
    amp_sum = 0.0
    for o in range(octaves):
        gw, gh = max(2, w // (cell * (2 ** o))), max(2, h // (cell * (2 ** o)))
        grid = r.random((gh, gw)).astype(np.float32)
        img = Image.fromarray((grid * 255).astype(np.uint8), "L").resize((w, h), Image.BICUBIC)
        total += amp * (np.asarray(img, dtype=np.float64) / 255.0)
        amp_sum += amp
        amp *= 0.5
    total /= amp_sum
    return total  # 0..1


def lerp_color(c1, c2, t):
    t = np.clip(t, 0, 1)
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))


def grain(img, amount=10, seed=1):
    arr = np.asarray(img).astype(np.int16)
    r = np.random.default_rng(seed)
    noise = r.integers(-amount, amount + 1, size=arr.shape[:2])
    for c in range(3):
        arr[..., c] = np.clip(arr[..., c] + noise, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def vignette(img, strength=0.55, feather=1.15):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    d = np.sqrt(((xx - cx) / (w / 2)) ** 2 + ((yy - cy) / (h / 2)) ** 2)
    mask = np.clip(1 - strength * np.clip(d - (1 - feather), 0, None) / feather, 0, 1)
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), "L")
    black = Image.new("RGB", img.size, (5, 6, 7))
    return Image.composite(img, black, mask_img)


def mow_stripes(w, h, angle_deg, band_px, seed=0):
    """Alternating light/dark bands like a mowed lawn, in the stripe's own
    rotated coordinate space, with soft noise-jittered edges."""
    diag = int((w ** 2 + h ** 2) ** 0.5) + band_px * 4
    yy, xx = np.mgrid[0:diag, 0:diag]
    theta = np.radians(angle_deg)
    proj = xx * np.cos(theta) + yy * np.sin(theta)
    n = value_noise(diag, diag, cell=max(6, band_px // 3), octaves=3, seed=seed + 50)
    proj = proj + (n - 0.5) * band_px * 0.7
    stripe = (np.floor(proj / band_px).astype(np.int64) % 2).astype(np.float64)
    # soften the hard edge
    edge = np.abs((proj / band_px) - np.round(proj / band_px))
    soft = np.clip(edge / 0.12, 0, 1)
    stripe = stripe * soft + 0.5 * (1 - soft)
    img = Image.fromarray((stripe * 255).astype(np.uint8), "L")
    ox, oy = (diag - w) // 2, (diag - h) // 2
    return img.crop((ox, oy, ox + w, oy + h))


def lawn_base(w, h, seed, dark=0.72, sat=0.85, angle=-22, band=54):
    """A mown-lawn color field: stripe pattern + blade-scale noise, mapped to
    a charcoal-leaning green ramp so it reads as *this* site's lawn, not a
    generic stock green."""
    stripes = np.asarray(mow_stripes(w, h, angle, band, seed=seed), dtype=np.float64) / 255.0
    blade = value_noise(w, h, cell=3, octaves=3, seed=seed + 9)
    big = value_noise(w, h, cell=90, octaves=3, seed=seed + 3)  # broad light/shade patches

    t = 0.35 * stripes + 0.4 * blade + 0.25 * big
    t = np.clip(t * sat + (1 - sat) * 0.5, 0, 1)

    deep = (18, 26, 16)      # near-black moss shadow
    mid = (46, 66, 30)       # grass-dark, matches --charcoal mood
    lit = (91, 133, 48)      # the site's --green, slightly desaturated
    hi = (134, 172, 78)      # a sunlit blade highlight, used sparingly

    arr = np.zeros((h, w, 3), dtype=np.float64)
    lo_mask = t < 0.55
    arr[..., 0] = np.where(lo_mask, lerp_color(deep, mid, t / 0.55)[0], lerp_color(mid, lit, (t - 0.55) / 0.45)[0])
    arr[..., 1] = np.where(lo_mask, lerp_color(deep, mid, t / 0.55)[1], lerp_color(mid, lit, (t - 0.55) / 0.45)[1])
    arr[..., 2] = np.where(lo_mask, lerp_color(deep, mid, t / 0.55)[2], lerp_color(mid, lit, (t - 0.55) / 0.45)[2])

    hi_mask = np.clip((t - 0.86) / 0.14, 0, 1) ** 1.5
    for c in range(3):
        arr[..., c] = arr[..., c] * (1 - hi_mask) + hi[c] * hi_mask

    arr *= dark
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img


def soft_bokeh(img, n=14, seed=2, color=(220, 235, 170), max_r=90, alpha=26):
    r = np.random.default_rng(seed)
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    last_rad = max_r
    for _ in range(n):
        cx, cy = int(r.integers(0, w)), int(r.integers(0, int(h * 0.7)))
        rad = int(r.integers(max_r // 3, max_r))
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=color + (alpha,))
        last_rad = rad
    overlay = overlay.filter(ImageFilter.GaussianBlur(last_rad * 0.6))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


# ---------------------------------------------------------------------------
# 1. Hero background — wide, mowed lawn, soft focus. Left legible as an
#    actual lawn photo; the page's own CSS gradient handles the darkening
#    needed for text contrast, layered on top of this in the stylesheet.
# ---------------------------------------------------------------------------
W, H = 2400, 1500
hero = lawn_base(W, H, seed=11, dark=0.88, sat=0.92, angle=-20, band=70)
hero = hero.filter(ImageFilter.GaussianBlur(2.2))
hero = soft_bokeh(hero, n=10, seed=5, alpha=16, max_r=140)
hero = vignette(hero, strength=0.32, feather=1.3)
hero = grain(hero, amount=6, seed=21)
hero.save(OUT / "hero-lawn.jpg", quality=84)
print("hero-lawn.jpg", hero.size)

# ---------------------------------------------------------------------------
# 2. Gallery tile — freshly striped lawn, brighter / more daylight.
# ---------------------------------------------------------------------------
w2, h2 = 1000, 750
lawn2 = lawn_base(w2, h2, seed=31, dark=0.92, sat=0.95, angle=8, band=46)
lawn2 = lawn2.filter(ImageFilter.GaussianBlur(1.1))
lawn2 = vignette(lawn2, strength=0.35, feather=1.2)
lawn2 = grain(lawn2, amount=5, seed=32)
lawn2.save(OUT / "gallery-lawn.jpg", quality=84)
print("gallery-lawn.jpg", lawn2.size)

# ---------------------------------------------------------------------------
# 3. Gallery tile — trimmed hedge, dense clipped-leaf texture.
# ---------------------------------------------------------------------------
def hedge_texture(w, h, seed):
    r = np.random.default_rng(seed)
    canvas = Image.new("RGB", (w, h), (22, 30, 18))
    d = ImageDraw.Draw(canvas)
    base_n = value_noise(w, h, cell=8, octaves=4, seed=seed)
    for _ in range(2200):
        x, y = r.integers(0, w), r.integers(0, h)
        rad = r.integers(10, 26)
        t = base_n[min(y, h - 1), min(x, w - 1)]
        shade = 0.5 + 0.5 * t
        col = tuple(int(c) for c in lerp_color((28, 40, 20), (108, 142, 60), shade))
        jitter = r.integers(-8, 8)
        col = tuple(max(0, min(255, c + jitter)) for c in col)
        d.ellipse([x - rad, y - rad * 0.6, x + rad, y + rad * 0.6], fill=col)
    canvas = canvas.filter(ImageFilter.GaussianBlur(1.4))
    leaf_n = value_noise(w, h, cell=2, octaves=2, seed=seed + 1)
    arr = np.asarray(canvas).astype(np.float64)
    spec = np.clip((leaf_n - 0.75) / 0.25, 0, 1) * 40
    for c in range(3):
        arr[..., c] = np.clip(arr[..., c] + spec, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))

hedge = hedge_texture(w2, h2, seed=41)
hedge = vignette(hedge, strength=0.4, feather=1.2)
hedge = grain(hedge, amount=5, seed=42)
hedge.save(OUT / "gallery-hedge.jpg", quality=84)
print("gallery-hedge.jpg", hedge.size)

# ---------------------------------------------------------------------------
# 4. Gallery tile — mulch bed with a clean edge, fibrous wood-chip texture.
# ---------------------------------------------------------------------------
def mulch_texture(w, h, seed):
    n = value_noise(w, h, cell=4, octaves=5, seed=seed)
    streak = np.zeros_like(n)
    shifts = range(-14, 15, 2)
    src = Image.fromarray((n * 255).astype(np.uint8))
    for s in shifts:
        shifted = ImageChops.offset(src, s, int(s * 0.3))
        streak += np.asarray(shifted, dtype=np.float64) / 255.0
    streak /= len(list(shifts))

    deep = (24, 16, 10)
    mid = (63, 41, 22)
    lit = (112, 78, 41)
    t = np.clip(streak * 1.15, 0, 1)
    arr = np.zeros((h, w, 3))
    lo = t < 0.5
    for c in range(3):
        arr[..., c] = np.where(lo, lerp_color(deep, mid, t / 0.5)[c], lerp_color(mid, lit, (t - 0.5) / 0.5)[c])

    # a clean planting-bed edge with grass along the top third
    edge_y = int(h * 0.22)
    yy, xx = np.mgrid[0:h, 0:w]
    edge_noise = value_noise(w, h, cell=40, octaves=2, seed=seed + 2)
    edge_line = edge_y + (edge_noise - 0.5) * 26
    grass_mask = yy < edge_line
    grass = lawn_base(w, h, seed=seed + 3, dark=0.85, sat=0.85, angle=-10, band=34)
    garr = np.asarray(grass, dtype=np.float64)
    arr = np.where(grass_mask[..., None], garr, arr)

    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img

mulch = mulch_texture(w2, h2, seed=51)
mulch = mulch.filter(ImageFilter.GaussianBlur(0.8))
mulch = vignette(mulch, strength=0.35, feather=1.2)
mulch = grain(mulch, amount=5, seed=52)
mulch.save(OUT / "gallery-mulch.jpg", quality=84)
print("gallery-mulch.jpg", mulch.size)

# ---------------------------------------------------------------------------
# 5. Estimate-section background — same lawn language, dusk-toned and wide,
#    sitting behind the dark charcoal gradient already in the CSS.
# ---------------------------------------------------------------------------
w3, h3 = 2200, 1300
dusk = lawn_base(w3, h3, seed=61, dark=0.62, sat=0.65, angle=-30, band=80)
dusk = dusk.filter(ImageFilter.GaussianBlur(5))
dusk = vignette(dusk, strength=0.45, feather=1.4)
dusk = grain(dusk, amount=5, seed=62)
dusk.save(OUT / "estimate-bg.jpg", quality=80)
print("estimate-bg.jpg", dusk.size)

print("done")
