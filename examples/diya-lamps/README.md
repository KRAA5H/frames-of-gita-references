# Example: diya lamps cascade (real project code)

The generator behind an actual Frames of Gita scene. Four terracotta oil lamps (diyas) stand on dark ground; the first flame passes from lamp to lamp until all four burn, the camera slowly pulls out, and a closing line appears: "from one flame, many lights". Every pixel is drawn by `generate.py` with numpy and Pillow - no AI imagery, no third-party assets, nothing to license.

This is real production code from the project, not a simplified demo, so it is also a honest reference for how the text-scene example's techniques (gradients, sprites, staggered timing, text cards) scale up to a fuller scene: layered RGBA compositing, a reusable glow sprite, per-lamp ignition timing, and a slow zoom done as crop-and-resize.

## Dependencies

- Python 3.9 or newer
- `pip install pillow numpy`
- ffmpeg on your PATH: https://ffmpeg.org/download.html
- DejaVu Serif Bold (bundled on most Linux desktops) for the closing text; edit the `SERIF` path near the top of the script for macOS/Windows fonts

## Run

```
python3 generate.py            # full render, writes diya-lamps.mp4
python3 generate.py --test     # 6 preview frames into ./preview/ (2 seconds)
```

Output: `diya-lamps.mp4` (13 seconds, 24 fps, 1080x1920, h264). A full render takes a couple of minutes. The video is silent; add narration and music in your editor as step 6 of the main guide describes.

## Adapting it

- Lamp layout, ignition order and timing: the `LAMPS` list at the top
- Colors: the palette constants at the top
- Closing text: `text_card()`
- Duration and frame rate: `DUR` and `FPS`

## Tested

Run end-to-end from a fresh repo checkout on 29 Oct 2026 (Ubuntu 22.04, Python 3.10, Pillow 12.3.0, numpy 2.2.6, ffmpeg 4.4.2): produced the MP4 above, and frames at six points across the clip were visually inspected to confirm the ignition cascade, pull-out and closing text render as intended.
