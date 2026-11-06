"""Generate the demo artwork used by the blog (replace with your own photos anytime).

Run:  python scripts/generate-demo-images.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
COVERS = ROOT / "public" / "images" / "covers"
POSTS = ROOT / "public" / "images" / "posts"
PHOTOS = ROOT / "src" / "content" / "photos"
PUBLIC = ROOT / "public" / "images"

for folder in (COVERS, POSTS, PHOTOS, PUBLIC):
    folder.mkdir(parents=True, exist_ok=True)

VIOLET = (139, 92, 246)
VIOLET_LIGHT = (180, 155, 255)
ACID = (200, 255, 61)
ORANGE = (255, 92, 43)
INK = (8, 8, 11)
TEXT = (238, 235, 228)

FONT_CJK = "C:/Windows/Fonts/msyh.ttc"
FONT_CJK_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_LATIN_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"

random.seed(7)
rng = np.random.default_rng(7)


def canvas(w: int, h: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> np.ndarray:
    y = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(top, dtype=np.float32)[None, None, :] * (1 - y) + np.array(bottom, dtype=np.float32)[None, None, :] * y
    return np.broadcast_to(arr, (h, w, 3)).astype(np.float32).copy()


def glow(arr: np.ndarray, cx: float, cy: float, radius: float, color: tuple[int, int, int], strength: float = 0.75, power: float = 2.0) -> None:
    h, w, _ = arr.shape
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / radius
    amount = np.clip(1 - dist, 0, 1) ** power * strength
    arr[:] = arr * (1 - amount[..., None]) + np.array(color, dtype=np.float32)[None, None, :] * amount[..., None]


def grain(arr: np.ndarray, amount: float = 7.0) -> None:
    noise = rng.normal(0, amount, arr.shape[:2])[..., None]
    arr[:] = np.clip(arr + noise, 0, 255)


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")


def save(img: Image.Image, path: Path, quality: int = 82) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"wrote {path.relative_to(ROOT)}  ({path.stat().st_size // 1024} KB)")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def spaced(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fnt: ImageFont.FreeTypeFont, fill: tuple[int, ...], spacing: float = 3.0) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=fnt, fill=fill)
        x += draw.textlength(char, font=fnt) + spacing


def hexagon(cx: float, cy: float, radius: float, rotation: float = math.pi / 6) -> list[tuple[float, float]]:
    return [
        (cx + radius * math.cos(rotation + i * math.pi / 3), cy + radius * math.sin(rotation + i * math.pi / 3))
        for i in range(6)
    ]


def grid(draw: ImageDraw.ImageDraw, w: int, h: int, step: int, color: tuple[int, ...]) -> None:
    for x in range(0, w + step, step):
        draw.line([(x, 0), (x, h)], fill=color, width=1)
    for y in range(0, h + step, step):
        draw.line([(0, y), (w, y)], fill=color, width=1)


def cover_hello() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (9, 8, 14), (23, 13, 42))
    glow(arr, 1160, 430, 780, VIOLET, 0.55)
    glow(arr, 330, 700, 520, ACID, 0.05)
    grain(arr, 5)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = 1160, 450

    for i, r in enumerate(range(90, 570, 36)):
        alpha = int(95 * (1 - r / 760))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(139, 92, 246, max(alpha, 18)), width=1)

    d.arc([cx - 430, cy - 430, cx + 430, cy + 430], 196, 322, fill=(200, 255, 61, 205), width=3)
    d.arc([cx - 300, cy - 300, cx + 300, cy + 300], 20, 96, fill=(255, 92, 43, 150), width=2)

    for i in range(72):
        angle = math.radians(i * 5)
        r1 = 560
        r2 = 574 if i % 6 == 0 else 566
        color = ACID if i % 6 == 0 else (139, 92, 246, 90)
        d.line(
            [(cx + math.cos(angle) * r1, cy + math.sin(angle) * r1), (cx + math.cos(angle) * r2, cy + math.sin(angle) * r2)],
            fill=color if i % 6 == 0 else color,
            width=1,
        )

    d.line([(cx - 640, cy), (cx + 640, cy)], fill=(255, 255, 255, 18), width=1)
    d.line([(cx, cy - 420), (cx, cy + 420)], fill=(255, 255, 255, 18), width=1)

    spaced(d, (96, 760), "SIGNAL 01 / 2026", font(FONT_MONO, 18), (127, 122, 141, 220), 2.2)
    d.text((96, 480), "01", font=font(FONT_LATIN_BOLD, 170), fill=(238, 235, 228, 22))

    img = Image.alpha_composite(img, layer)
    save(img, COVERS / "hello.jpg")


def cover_attention() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (11, 9, 17), (31, 10, 18))
    glow(arr, 1240, 300, 700, ORANGE, 0.35)
    glow(arr, 460, 620, 680, VIOLET, 0.3)
    grain(arr, 10)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    for _ in range(26):
        y = random.randint(30, h - 30)
        thickness = random.randint(2, 14)
        x0 = random.randint(-100, 500)
        x1 = x0 + random.randint(300, 1200)
        color = random.choice([(255, 92, 43, 26), (139, 92, 246, 30), (200, 255, 61, 14)])
        d.rectangle([x0, y, x1, y + thickness], fill=color)

    cx, cy = 1200, 450
    for offset, color in [(-7, (255, 92, 43, 120)), (0, (238, 235, 228, 70)), (7, (139, 92, 246, 120))]:
        d.arc([cx - 330 + offset, cy - 330, cx + 330 + offset, cy + 330], 0, 360, fill=color, width=2)

    for y in range(0, h, 4):
        d.line([(0, y), (w, y)], fill=(255, 255, 255, 8), width=1)

    spaced(d, (96, 760), "SIGNAL 02 / 2026", font(FONT_MONO, 18), (127, 122, 141, 220), 2.2)
    d.text((96, 470), "02", font=font(FONT_LATIN_BOLD, 170), fill=(238, 235, 228, 20))

    img = Image.alpha_composite(img, layer)
    save(img, COVERS / "attention.jpg")


def cover_astro() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (8, 8, 12), (16, 11, 31))
    glow(arr, 760, 430, 720, VIOLET, 0.42)
    glow(arr, 1330, 710, 400, ACID, 0.05)
    grain(arr, 5)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    grid(d, w, h, 80, (255, 255, 255, 12))
    for i in range(0, w, 320):
        d.line([(i, 0), (i, h)], fill=(139, 92, 246, 40), width=1)
    for j in range(0, h, 320):
        d.line([(0, j), (w, j)], fill=(139, 92, 246, 40), width=1)

    cx, cy = 800, 450
    d.polygon(hexagon(cx, cy, 300), outline=(139, 92, 246, 120))
    d.polygon(hexagon(cx, cy, 230), outline=(180, 155, 255, 170))
    d.polygon(hexagon(cx, cy, 150), outline=(200, 255, 61, 150))
    d.line([(cx - 380, cy), (cx + 380, cy)], fill=(238, 235, 228, 35), width=1)
    d.line([(cx, cy - 380), (cx, cy + 380)], fill=(238, 235, 228, 35), width=1)

    for i in range(4):
        x = 170 + i * 64
        d.rectangle([x, 700, x + 30, 704], fill=(200, 255, 61, 90))
    for i in range(6):
        x = 1240 + i * 42
        d.rectangle([x, 180, x + 22, 184], fill=(139, 92, 246, 90))

    spaced(d, (96, 760), "SIGNAL 03 / 2026", font(FONT_MONO, 18), (127, 122, 141, 220), 2.2)
    d.text((1260, 600), "03", font=font(FONT_LATIN_BOLD, 150), fill=(238, 235, 228, 18))

    img = Image.alpha_composite(img, layer)
    save(img, COVERS / "astro.jpg")


def cover_notes() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (7, 10, 8), (10, 20, 12))
    glow(arr, 800, 480, 760, (50, 90, 20), 0.35)
    grain(arr, 6)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    for k in range(24):
        base_y = 80 + k * 36
        points = []
        for x in range(-40, w + 40, 8):
            y = base_y + 52 * math.sin(x / 210 + k * 0.52) + 20 * math.sin(x / 64 + k * 1.2)
            points.append((x, y))
        alpha = 26 + (k % 6) * 10
        d.line(points, fill=(200, 255, 61, alpha), width=2 if k % 5 == 0 else 1)

    for k in range(9):
        x = 160 + k * 160
        d.line([(x, 0), (x, h)], fill=(200, 255, 61, 12), width=1)

    spaced(d, (96, 760), "SIGNAL 04 / 2026", font(FONT_MONO, 18), (127, 122, 141, 220), 2.2)
    d.text((1180, 590), "04", font=font(FONT_LATIN_BOLD, 160), fill=(238, 235, 228, 16))

    img = Image.alpha_composite(img, layer)
    save(img, COVERS / "notes.jpg")


def cover_photo() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (20, 10, 32), (30, 14, 22))
    glow(arr, 1100, 340, 680, ORANGE, 0.3)
    glow(arr, 480, 560, 680, VIOLET, 0.45)
    grain(arr, 6)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    step = 18
    for y in range(0, h + step, step):
        for x in range(0, w + step, step):
            dist = math.hypot(x - 820, y - 450) / 720
            radius = max(1.2, 8.5 * (1 - dist) * (0.6 + 0.4 * math.sin(x / 90)))
            color = (200, 255, 61, int(50 * max(0, 1 - dist) + 8))
            d.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

    d.arc([820 - 400, 450 - 400, 820 + 400, 450 + 400], 0, 360, fill=(255, 92, 43, 100), width=2)
    d.arc([820 - 260, 450 - 260, 820 + 260, 450 + 260], 0, 360, fill=(238, 235, 228, 60), width=1)

    spaced(d, (96, 760), "SIGNAL 05 / 2026", font(FONT_MONO, 18), (127, 122, 141, 220), 2.2)
    d.text((1180, 580), "05", font=font(FONT_LATIN_BOLD, 160), fill=(238, 235, 228, 18))

    img = Image.alpha_composite(img, layer)
    save(img, COVERS / "photo.jpg")


def cover_markdown() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (8, 8, 11), (14, 13, 18))
    glow(arr, 800, 450, 780, VIOLET, 0.22)
    grain(arr, 5)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    for i in range(-h, w + h, 90):
        d.line([(i, 0), (i + h, h)], fill=(200, 255, 61, 12), width=26)
    d.rectangle([110, 130, 1490, 770], fill=(8, 8, 11, 235), outline=(58, 55, 72, 220), width=1)
    d.rectangle([110, 130, 1490, 178], fill=(22, 22, 29, 255))
    for i, color in enumerate([ORANGE, (255, 210, 80), ACID]):
        d.ellipse([136 + i * 22, 146, 148 + i * 22, 158], fill=color)

    widths = [420, 620, 300, 700, 480, 560, 240]
    colors = [(180, 155, 255, 150), (238, 235, 228, 80), (200, 255, 61, 120)]
    for i, width in enumerate(widths):
        x = 160
        y = 230 + i * 62
        d.rectangle([x, y, x + 70, y + 10], fill=(139, 92, 246, 120))
        d.rectangle([x + 92, y, x + 92 + width, y + 10], fill=colors[i % 3])
    d.rectangle([160, 680, 420, 692], fill=(200, 255, 61, 170))

    spaced(d, (96, 810), "SIGNAL 06 / 2026", font(FONT_MONO, 18), (127, 122, 141, 220), 2.2)

    img = Image.alpha_composite(img, layer)
    save(img, COVERS / "markdown.jpg")


def photo_target() -> None:
    w, h = 1200, 1500
    arr = canvas(w, h, (10, 8, 15), (24, 13, 40))
    glow(arr, 600, 720, 780, VIOLET, 0.5)
    grain(arr, 8)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = 600, 730
    for r in range(110, 760, 46):
        alpha = int(80 * (1 - r / 900)) + 12
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(180, 155, 255, alpha), width=1)
    d.ellipse([cx - 300, cy - 300, cx + 300, cy + 300], outline=(200, 255, 61, 150), width=3)
    d.line([(cx - 760, cy), (cx + 760, cy)], fill=(238, 235, 228, 30), width=1)
    d.line([(cx, 0), (cx, h)], fill=(238, 235, 228, 30), width=1)
    for i in range(60):
        angle = math.radians(i * 6)
        r1, r2 = 650, 668 if i % 5 else 680
        d.line([(cx + math.cos(angle) * r1, cy + math.sin(angle) * r1), (cx + math.cos(angle) * r2, cy + math.sin(angle) * r2)], fill=(200, 255, 61, 70), width=1)
    img = Image.alpha_composite(img, layer)
    save(img, PHOTOS / "signal-01" / "signal-01.jpg")


def photo_horizon() -> None:
    w, h = 1600, 1000
    arr = canvas(w, h, (8, 10, 9), (9, 16, 10))
    glow(arr, 800, 560, 620, (60, 140, 30), 0.35)
    grain(arr, 6)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(560, 1000, 5):
        alpha = int(90 * (1 - (y - 560) / 440)) + 5
        d.line([(0, y), (w, y)], fill=(200, 255, 61, alpha), width=1)
    d.line([(0, 558), (w, 558)], fill=(200, 255, 61, 210), width=2)
    d.line([(0, 300), (w, 300)], fill=(139, 92, 246, 50), width=1)
    d.arc([520, 250, 1080, 810], 200, 340, fill=(255, 92, 43, 80), width=2)
    d.text((80, 120), "HORIZON", font=font(FONT_MONO, 34), fill=(238, 235, 228, 55))
    img = Image.alpha_composite(img, layer)
    save(img, PHOTOS / "signal-02" / "signal-02.jpg")


def photo_orange() -> None:
    w, h = 1200, 1200
    arr = canvas(w, h, (18, 10, 30), (34, 12, 24))
    glow(arr, 600, 520, 640, ORANGE, 0.42)
    grain(arr, 10)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    grid(d, w, h, 100, (238, 235, 228, 12))
    for r, alpha in [(430, 60), (360, 90), (290, 120)]:
        d.ellipse([600 - r, 520 - r, 600 + r, 520 + r], outline=(255, 92, 43, alpha), width=2)
    d.ellipse([430, 350, 770, 690], fill=(255, 92, 43, 26), outline=(255, 92, 43, 150), width=2)
    d.line([(0, 520), (1200, 520)], fill=(255, 92, 43, 120), width=1)
    d.line([(600, 0), (600, 1200)], fill=(255, 92, 43, 120), width=1)
    for i in range(8):
        d.rectangle([80, 980 + i * 18, 80 + 260 - i * 22, 988 + i * 18], fill=(238, 235, 228, 35))
    img = Image.alpha_composite(img, layer)
    save(img, PHOTOS / "signal-03" / "signal-03.jpg")


def photo_city() -> None:
    w, h = 1000, 1400
    arr = canvas(w, h, (10, 8, 16), (26, 12, 36))
    glow(arr, 500, 700, 720, VIOLET, 0.3)
    grain(arr, 7)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 40
    random.seed(11)
    while x < w - 40:
        width = random.randint(50, 110)
        top = random.randint(240, 860)
        d.rectangle([x, top, x + width, h], fill=(8, 8, 12, 220), outline=(58, 55, 72, 160))
        for wy in range(top + 22, h - 30, 34):
            for wx in range(x + 12, x + width - 10, 24):
                if random.random() < 0.42:
                    d.rectangle([wx, wy, wx + 8, wy + 12], fill=(200, 255, 61, random.randint(40, 170)))
        x += width + random.randint(14, 34)
    d.line([(0, 880), (w, 880)], fill=(139, 92, 246, 80), width=1)
    d.text((50, 90), "VERTICAL / 2026", font=font(FONT_MONO, 26), fill=(238, 235, 228, 45))
    img = Image.alpha_composite(img, layer)
    save(img, PHOTOS / "signal-04" / "signal-04.jpg")


def photo_crosshair() -> None:
    w, h = 1600, 900
    arr = canvas(w, h, (8, 9, 10), (10, 17, 12))
    glow(arr, 800, 450, 640, (60, 150, 20), 0.3)
    grain(arr, 7)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    grid(d, w, h, 64, (200, 255, 61, 12))
    cx, cy = 800, 450
    d.line([(0, cy), (w, cy)], fill=(200, 255, 61, 180), width=2)
    d.line([(cx, 0), (cx, h)], fill=(200, 255, 61, 180), width=2)
    d.ellipse([cx - 230, cy - 230, cx + 230, cy + 230], outline=(200, 255, 61, 150), width=2)
    d.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=(238, 235, 228, 60), width=1)
    for i in range(40):
        angle = math.radians(i * 9)
        r1, r2 = 250, 268
        d.line([(cx + math.cos(angle) * r1, cy + math.sin(angle) * r1), (cx + math.cos(angle) * r2, cy + math.sin(angle) * r2)], fill=(200, 255, 61, 80), width=1)
    spaced(d, (70, 70), "TARGET // LOCKED", font(FONT_MONO, 22), (200, 255, 61, 140), 2)
    img = Image.alpha_composite(img, layer)
    save(img, PHOTOS / "signal-05" / "signal-05.jpg")


def photo_noise() -> None:
    w, h = 1200, 1500
    arr = canvas(w, h, (8, 8, 10), (14, 14, 18))
    glow(arr, 520, 700, 700, VIOLET, 0.22)
    grain(arr, 26)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    random.seed(23)
    for _ in range(60):
        y = random.randint(0, h)
        d.line([(0, y), (w, y)], fill=(200, 255, 61, random.randint(4, 26)), width=1)
    for _ in range(14):
        y = random.randint(100, h - 100)
        x = random.randint(-200, 400)
        d.rectangle([x, y, x + random.randint(300, 900), y + random.randint(4, 22)], fill=(139, 92, 246, random.randint(20, 60)))
    d.rectangle([50, 50, w - 50, h - 50], outline=(238, 235, 228, 30), width=2)
    spaced(d, (80, 90), "NOISE // 06", font(FONT_MONO, 22), (200, 255, 61, 110), 2)
    d.text((80, h - 160), "SIGNAL LOST", font=font(FONT_LATIN_BOLD, 58), fill=(238, 235, 228, 30))
    img = Image.alpha_composite(img, layer)
    save(img, PHOTOS / "signal-06" / "signal-06.jpg")


def og_image() -> None:
    w, h = 1200, 630
    arr = canvas(w, h, (8, 8, 12), (20, 11, 34))
    glow(arr, 1010, 300, 520, VIOLET, 0.45)
    grain(arr, 4)
    img = to_image(arr)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    grid(d, w, h, 60, (255, 255, 255, 10))

    spaced(d, (72, 64), "ROJECT // PERSONAL ARCHIVE", font(FONT_MONO, 19), (200, 255, 61, 210), 2.2)
    d.text((68, 118), "ROJECT", font=font(FONT_LATIN_BOLD, 150), fill=(238, 235, 228, 255))
    d.rectangle([76, 300, 480, 304], fill=(200, 255, 61, 220))
    d.text((72, 342), "在噪声中，保持清醒的记录。", font=font(FONT_CJK_BOLD, 46), fill=(238, 235, 228, 235))
    spaced(d, (74, 430), "STUDY / CODE / PHOTO / SOCIETY", font(FONT_MONO, 18), (183, 178, 194, 210), 2.4)
    spaced(d, (74, 540), "GITHUB PAGES  ·  BUILT WITH ASTRO", font(FONT_MONO, 15), (127, 122, 141, 220), 2)

    cx, cy = 980, 300
    for r in range(60, 250, 24):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(139, 92, 246, 70), width=1)
    d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], outline=(200, 255, 61, 180), width=2)
    d.line([(cx - 280, cy), (cx + 280, cy)], fill=(238, 235, 228, 40), width=1)
    d.line([(cx, cy - 280), (cx, cy + 280)], fill=(238, 235, 228, 40), width=1)

    img = Image.alpha_composite(img, layer)
    save(img, PUBLIC / "og-default.jpg", quality=86)


if __name__ == "__main__":
    cover_hello()
    cover_attention()
    cover_astro()
    cover_notes()
    cover_photo()
    cover_markdown()
    photo_target()
    photo_horizon()
    photo_orange()
    photo_city()
    photo_crosshair()
    photo_noise()
    og_image()
    print("done")