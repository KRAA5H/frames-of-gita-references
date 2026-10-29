# Example: code-built text scene

A minimal but complete code-built animation: an 8-second vertical (1080x1920) MP4 of a Gita verse fading in over a starfield, with a soft glow, a growing accent line and a fade to black. Every pixel is drawn by `generate.py`; there is no AI imagery and there are no third-party assets to license. Use it as a template: replace the lines in `LINES` and the colors at the top of the script with your own script and style.

## Dependencies

- Python 3.9 or newer
- Pillow: `pip install pillow`
- ffmpeg on your PATH: https://ffmpeg.org/download.html
- A TTF font. The script tries DejaVu Sans (bundled on most Linux desktops) then common macOS/Windows font paths, and falls back to Pillow's small built-in font with a warning.

## Run

```
python3 generate.py
```

Output: `example-scene.mp4` (8 seconds, 24 fps, 1080x1920, h264). Rendering takes about a minute on a typical machine. The video is silent; add narration and music in your editor as step 6 of the main guide describes.

## Tested

Run end-to-end on 29 Oct 2026 (Ubuntu 22.04, Python 3.10, Pillow 12.3.0, ffmpeg 4.4.2): produced the MP4 above from a fresh checkout, and extracted frames were visually inspected to confirm the scene renders as intended.
