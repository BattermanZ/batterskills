# Recovering a recipe from YouTube

Work in the session scratchpad. `yt-dlp` is not installed; run it through `uvx`. There is no system ffmpeg; use the one bundled in `imageio-ffmpeg`.

## 1. Description and captions

```bash
uvx yt-dlp --skip-download --write-description --write-auto-subs \
  --sub-langs 'en-orig,en' --sub-format vtt -o v '<url>'
```

Most creators put the full recipe in the `.description` file. When it is empty or partial, the captions carry what the creator says: drop the timing lines and de-duplicate. Name the caption languages exactly: a wildcard such as `'en.*'` requests every translated track and draws an HTTP 429.

The description or captions settle the recipe only when they hold its method. When the creator says the recipe is "on screen", or the video shows cooking the words never describe, go on to the frames.

## 2. Map the whole video

Download the video stream and tile a frame every 2 seconds across the whole video into contact sheets:

```bash
uvx yt-dlp -f 'bv*[height<=720]' -o v.mp4 '<url>'
uv run --with imageio-ffmpeg python -c "
import imageio_ffmpeg, subprocess
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', 'v.mp4',
  '-vf', 'fps=1/2,scale=240:-1,tile=8x3', 'sheet%d.jpg'], check=True)"
```

Tile *n* (from 0) of sheet *k* (from 1) sits at `2 × (24 × (k − 1) + n)` seconds. Read every sheet as an image and write down each action, what goes in, and its time. A recipe card, when there is one, usually sits in the last third of a short.

Where the map is unsure (a cover, a glaze, what goes in when), cut a sheet at one frame a second over that stretch: add `-ss <start> -t <length>` and use `fps=1`. Settle every step this way before writing it. What the frames still leave unsure goes in the note.

## 3. Photos

Pick one full-size frame per step and one of the finished dish for the main photo:

```bash
<ffmpeg> -loglevel error -y -ss <seconds> -i v.mp4 -frames:v 1 -q:v 3 s01.jpg
```

Tile the picks into one strip and look at it before uploading: a frame a second off lands on a transition or a hand. Burned-in subtitles are on every frame of most shorts; that is acceptable. Upload them out of band as `SKILL.md`'s editing mechanics describe, then send steps, photos and main photo in one `edit_recipe`.
