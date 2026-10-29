# Getting started: making a Frames of Gita video from scratch

Frames of Gita makes short vertical videos (Instagram reels) that explain stories and ideas from the Bhagavad Gita. This guide walks through making a first video. Most steps use tools outside this repo (a chatbot, a video generator or your own drawing/coding, an editor, Instagram). The one part that runs end-to-end from the repo alone is the tested code example in `examples/text-scene/`.

## What you need

- An AI chatbot for scriptwriting (Claude, ChatGPT or similar)
- A way to make visuals: an AI video generator that accepts text prompts, or code-built animation (HTML/CSS/JS rendered to video), or your own illustration/animation skills
- A video editor for assembly (CapCut, or any editor that exports 9:16)
- An Instagram account to publish

Some tools have paid tiers. Check cost and availability before you commit to a tool, and treat any tool named inside a pasted prompt as a suggestion, not a requirement.

## Workflow

1. **Pick one idea.** One story, verse or concept per video. Short reels teach one thing.
2. **Write the script.** Use `prompts/prompt-feynman-script-structure.txt` with your chatbot. It gives you a hook, a relatable beat, a plain explanation with an everyday analogy, and a natural close. Fill in your platform and theme where the prompt has brackets.
3. **Plan the scenes before generating anything.** One shot type and one line per scene. If a character recurs, make a character sheet (angles, expressions, outfit) and reuse it so the character stays consistent. Check your timing arithmetic: scene count times seconds per scene must equal your target duration.
4. **Make a small test first.** Produce the first few scenes only, review them on a phone screen, and only then build the rest. This catches style and cost problems early.
5. **Generate or build the visuals.** `prompts/prompt-kurzgesagt-explainer-finnardley.txt` is a full video-generation prompt template for an animated explainer style; fill in its input section. Code-built animation and hand illustration work too and give you exact control.
6. **Assemble and record narration.** Combine scenes, narration, sound and music in your editor. Test voices before committing; changing voice late can break sync with the picture.
7. **Export vertical.** 9:16, 1080x1920. If you post from Instagram on the web, change the crop from the default 1:1 to Original so the video stays vertical.
8. **Add music in the Instagram phone app.** Instagram's licensed music library is only available in the phone app, not the web composer. Using popular music outside Instagram's licence can get a reel muted or removed.

## Reference prompts

The `prompts/` folder holds prompts collected from X and chat, each verbatim in its own file with sources listed in `prompts/SOURCES.md`. They are starting points to adapt, not a runnable pipeline by themselves.

## Examples of finished reels

- Pixel-art style reel: https://www.instagram.com/framesofgita/reel/De95mvKqEZ0/
- Hare story reel: https://www.instagram.com/framesofgita/reel/De__z5dqlHR/
- Carousel post: https://www.instagram.com/p/DfAXDIjEQlt/

## Tested code examples

Two self-contained Python scripts draw complete vertical MP4s with no AI imagery and no third-party assets. Install Pillow and ffmpeg, run `python3 generate.py` in either folder, and you have a real exported video to inspect and adapt. Both were run end-to-end from a fresh checkout on 29 Oct 2026 and their frames were visually checked.

- `examples/text-scene/` - minimal starter template: a verse fading in over a starfield, 8 seconds
- `examples/diya-lamps/` - real project code: an oil-lamp ignition cascade with pull-out and closing text, 13 seconds

## Honest limits

- A prompt does not guarantee a good video. Expect to review and regenerate.
- Do not reuse other people's art, voice, music or footage without a licence or permission, even if others post the same content. Instagram removes repeat infringements.
- Clips from films and TV shows need rights clearance separate from any music licence; the repo's reference library is for studying technique, not for footage to republish.
