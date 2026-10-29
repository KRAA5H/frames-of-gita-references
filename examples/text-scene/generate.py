#!/usr/bin/env python3
"""
Frames of Gita - example code-built animation.

Renders a short vertical (1080x1920) animated text scene frame by frame
with Pillow and encodes it to MP4 with ffmpeg. No AI imagery and no
third-party assets: every pixel is drawn by this script.

Dependencies:
    Python 3.9+   (standard library + Pillow)
    Pillow        pip install pillow
    ffmpeg        https://ffmpeg.org/download.html (must be on PATH)

Run:
    python3 generate.py
Output:
    example-scene.mp4 (8 seconds, 24 fps, 1080x1920)
"""

import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --- Configuration ---------------------------------------------------------

WIDTH, HEIGHT = 1080, 1920
FPS = 24
DURATION_S = 8
TOTAL_FRAMES = FPS * DURATION_S
OUTPUT = "example-scene.mp4"

# Example text: a widely used English rendering of Bhagavad Gita 2.47.
# Replace LINES with your own script lines to reuse this template.
TITLE = "Bhagavad Gita 2.47"
LINES = [
    "You have a right to your actions,",
    "but never to the fruits",
    "of your actions.",
]

BACKGROUND_TOP = (10, 12, 40)      # deep navy
BACKGROUND_BOTTOM = (38, 20, 62)   # dark violet
TEXT_COLOR = (245, 240, 230)
ACCENT = (212, 175, 55)            # muted gold

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial.ttf",                       # macOS
    "C:/Windows/Fonts/arial.ttf",                     # Windows
]


def load_font(size, bold=False):
    candidates = FONT_CANDIDATES[1:2] + FONT_CANDIDATES[:1] if bold else FONT_CANDIDATES
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    print("warning: no TTF found, using Pillow's small default font", file=sys.stderr)
    return ImageFont.load_default()


def vertical_gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        px_row = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = px_row
    return img


def make_stars(count=90, seed=7):
    rng = random.Random(seed)
    return [(rng.uniform(0, WIDTH), rng.uniform(0, HEIGHT * 0.7),
             rng.uniform(1.0, 2.6), rng.uniform(0, 2 * math.pi)) for _ in range(count)]


def draw_glow(img, cx, cy, radius, color, alpha):
    """Soft glow: filled ellipse on its own layer, Gaussian-blurred, composited."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=radius / 2))
    img.alpha_composite(layer)


def draw_centered(draw, y, text, font, fill, tracking=0):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) / 2
    draw.text((x, y), text, font=font, fill=fill)


def render_frame(n, stars, fonts):
    t = n / TOTAL_FRAMES  # 0..1 over the whole clip
    base = vertical_gradient(WIDTH, HEIGHT, BACKGROUND_TOP, BACKGROUND_BOTTOM)
    img = base.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Twinkling stars
    for x, y, r, phase in stars:
        tw = 0.5 + 0.5 * math.sin(2 * math.pi * (t * 3) + phase)
        a = int(60 + 140 * tw)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

    # Slow pulsing glow behind the text block
    pulse = 0.75 + 0.25 * math.sin(2 * math.pi * t * 2)
    draw_glow(img, WIDTH / 2, HEIGHT * 0.52, int(420 * pulse), ACCENT, 60)
    draw = ImageDraw.Draw(img)  # redraw after compositing the glow layer

    # Title fades in during the first second
    title_font, line_font = fonts
    title_alpha = min(1.0, t / (1.0 / DURATION_S))
    draw_centered(draw, HEIGHT * 0.30, TITLE, title_font,
                  ACCENT + (int(255 * title_alpha),))

    # Each line fades in over 0.8s, staggered 1.2s apart, starting at 1.5s
    for i, line in enumerate(LINES):
        start = (1.5 + 1.2 * i) / DURATION_S
        fade = min(1.0, max(0.0, (t - start) / (0.8 / DURATION_S)))
        if fade <= 0:
            continue
        y = HEIGHT * 0.44 + i * 110
        draw_centered(draw, y, line, line_font,
                      TEXT_COLOR + (int(255 * fade),))

    # Accent underline grows under the text block in the last two seconds
    grow = min(1.0, max(0.0, (t - (DURATION_S - 2) / DURATION_S) / (2.0 / DURATION_S)))
    line_w = int(360 * grow)
    cy = HEIGHT * 0.44 + 3 * 110 + 10
    draw.rectangle([WIDTH / 2 - line_w / 2, cy, WIDTH / 2 + line_w / 2, cy + 4],
                   fill=ACCENT + (220,))

    # Fade the whole frame to black in the final half second
    fadeout_start = (DURATION_S - 0.5) / DURATION_S
    if t > fadeout_start:
        k = (t - fadeout_start) / (1 - fadeout_start)
        overlay = Image.new("RGBA", img.size, (0, 0, 0, int(255 * k)))
        img = Image.alpha_composite(img, overlay)

    return img.convert("RGB")


def main():
    fonts = (load_font(54, bold=True), load_font(64))
    stars = make_stars()

    tmp = tempfile.mkdtemp(prefix="frames-")
    try:
        for n in range(TOTAL_FRAMES):
            frame = render_frame(n, stars, fonts)
            frame.save(os.path.join(tmp, f"{n:04d}.png"))
            if n % FPS == 0:
                print(f"rendered second {n // FPS + 1}/{DURATION_S}", flush=True)

        cmd = [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", os.path.join(tmp, "%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            OUTPUT,
        ]
        print("encoding:", " ".join(cmd))
        subprocess.run(cmd, check=True)
        print(f"done: {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
