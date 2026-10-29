# Plan: make a Scratch video using the repo's strategies

Study the techniques in this repo, then rebuild them with original art, voice and story. The repo's own rule: the reference reels are for private analysis, not reuse. Do not trace, copy footage or reuse their audio.

## 1. Pick the style that fits Scratch

Scratch is a 480x360 stage with sprites, costumes, backdrops, sounds and blocks. The repo's styles map onto it like this:

| Repo style | Fit in Scratch | How |
|---|---|---|
| 2D storybook + visual scoreboard (loreandproof) | Best | Flat characters, layered backdrops, counter variables, cards |
| Puppet-stage (maya_effects) | Very good | Jointed sprites (arm and leg parts rotate), a curtain backdrop, slow glide and twinkle |
| Cultural reveal (undiscovered.bharat) | Good | Familiar object, then label sprites, then a counter moving along a board |
| Biography to consequence (thehindu.archive) | Good | Alternate character backdrops with chalkboard/equation backdrops |
| Clay-look, 3D ritual | Poor | Needs lighting and depth that Scratch cannot do. Skip it |

**Recommendation:** start with 2D storybook plus puppet-stage, about 45-60 s.

## 2. The repeatable story shape (from the repo notes)

1. **Hook:** one unanswered question in the first 2-3 s. (Urmila: "who carried Lakshmana's sleep?")
2. **Pattern:** two or three parallel beats, or a repeated number or object.
3. **Pivot:** a question that changes the frame.
4. **Visible proof:** a diagram, counter, scoreboard or checklist. Show the argument, don't just narrate it.
5. **Return:** the last line goes back to the opening image with new meaning.
6. **Change the visual mode** when the explanation changes (person, then diagram).

Pacing: quick progress early, slower detail in the middle, brisk ending.

## 3. Prompts: what to write before building

The repo holds no ready-made generation prompts, only analysis notes, so you write them. Use `/prompts/` (create it) with one file per video.

- `script.md`: narration, about 130-150 words per minute, one idea per line.
- `shotlist.md`: per line, which backdrop, which sprites, what moves, how long.
- `assets.md`: a prompt for each image asset.
  - Style line to reuse: "flat 2D outlined characters, layered landscape, navy/gold palette, cream subtitles, simple shapes, transparent background".
  - If using AI image tools, generate each sprite part (head, body, arm) separately on a transparent background so Scratch can rotate them.
- Source check: for any scripture or historical claim, find the primary source yourself. The repo marks nearly every claim as unverified, so do not repeat them as fact.

## 4. Build in Scratch

1. Create the project at scratch.mit.edu or use the offline editor. TurboWarp is a good alternative with a higher framerate and bigger stage.
2. Import the backdrops (one per scene) and sprites.
3. Record the narration in the Sound tab, or import an original recording. Use your own voice or a licensed TTS, not the reference audio.
4. Script it with one "Director" sprite that broadcasts `scene1`, `scene2`... so timing lives in one place.
   - Each scene: `switch backdrop`, `show` sprites, `glide`, `say`, `play sound until done`, then `broadcast next`.
   - Subtitles: a sprite with a text costume per line, or the `say` block at large size.
   - Scoreboard or counter: a variable shown as a monitor, changed with `change by`.
5. Add a green-flag start and a reset block so each run is identical.

## 5. Get a video out of Scratch

Scratch cannot export MP4 itself. Options:

- Screen-record the stage in full-screen mode with OBS, Xbox Game Bar (Win+G) or Clipchamp. Simplest.
- Crop to 9:16 afterwards in Clipchamp or CapCut, since the stage is 4:3. Or design with the vertical crop in mind and keep the action centred.
- Add music (licensed or original) in the editor, not in Scratch.

## 6. Steps in order

1. Choose the story and check its sources.
2. Write `script.md`, then `shotlist.md`.
3. Make or generate the assets.
4. Build one scene end to end, then the rest.
5. Record, trim, add captions and export 1080x1920.
6. Review against the checklist in section 2.

## Optional: get the reference MP4s

The MP4s are not in the git clone. They are in the Assets of release v1.0 on GitHub (`gh` isn't installed here, so download them from the release page). Use them only to study pacing and layout.
