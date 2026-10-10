# Recovering a recipe from YouTube

Work in the session scratchpad.

## 1. Description and captions

```bash
uvx yt-dlp --skip-download --write-description --write-auto-subs \
  --sub-langs 'en-orig,en' --sub-format vtt -o v '<url>'
```

Most creators put the full recipe in the `.description` file. When it is empty or partial, the captions carry what the creator says: drop the timing lines and de-duplicate. Name the caption languages exactly: a wildcard such as `'en.*'` requests every translated track and draws an HTTP 429.

The description or captions settle the recipe only when they hold its method. When the creator says the recipe is "on screen", or the video shows cooking the words never describe, go on to the frames.

## 2. The creator's written recipe

When the description and captions give no amounts, the creator has usually written the recipe somewhere else. Look in both places before reading anything off the frames:

- **The pinned comment.**

  ```bash
  uvx yt-dlp --skip-download --write-comments \
    --extractor-args 'youtube:max_comments=40,all,0,0;comment_sort=top' -o c '<url>'
  ```

  The comments land in `c.info.json` under `comments`. The creator's own carry `author_is_uploader: true`, and they also answer viewers' questions (pan sizes, swaps), which go in the note.
- **The creator's site.** Follow the link in the description, or find the page with `donsetch search '<channel> <dish> recipe'`. Fetch the address the description or the search returned: a guessed address comes back as the site's "not found" page.

**A recipe is saved without amounts only after both places came up empty**, and its note says so: what the comments held, and which search found no page. A short that names its ingredients and shows a finished dish nearly always has a written recipe behind it.

A written recipe that is the same dish as the video (the frames show its ingredients) supplies the quantities, times, temperatures and yield, and the note says where they came from. The video still supplies the photos and any step the written recipe leaves out.

## 3. Map the whole video

Download the video stream at 720 pixels high (print on a jar is unreadable below that; check the height yt-dlp reports and download again if it is lower), and tile a frame every 2 seconds across the whole video into contact sheets:

```bash
uvx yt-dlp -f 'bv*[height<=720]' -o v.mp4 '<url>'
uv run --with imageio-ffmpeg python -c "
import imageio_ffmpeg, subprocess
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', 'v.mp4',
  '-vf', 'fps=1/2,scale=240:-1,tile=8x3', 'sheet%d.jpg'], check=True)"
```

Tile *n* (from 0) of sheet *k* (from 1) sits at `2 × (24 × (k − 1) + n)` seconds. Read every sheet as an image and write down each action, what goes in, and its time. A recipe card, when there is one, usually sits in the last third of a short.

Where the map is unsure (a cover, a glaze, what goes in when), cut a sheet at one frame a second over that stretch: add `-ss <start> -t <length>` and use `fps=1`. Settle every step this way before writing it.

When the words and the written recipe give no method or no amounts, the frames are the recipe, and the map goes deeper:

- **One frame a second across the whole video**, not only the unsure stretches.
- **A full-size frame of everything that carries a fact.** A 240-pixel tile shows an action and hides print. Pull the frame (the command in section 4) for each label, jar and package (its name and its weight), the oven or air fryer display, on-screen text, and the tray or plate that shows how many the recipe makes.
- **Count what can be counted**: thighs, cloves, tortillas, boxes on the tray.

The map is done when everything that goes into the pan has an ingredient line, and every cover, lid, foil, oven and grill has a step. An ingredient the frames show without naming it still gets its line, under the plainest name that fits what is seen ("stock", "soft white cheese", "tomato paste" for a red paste from a tube), and the note says it is a reading of the frames and what else it could be. Only what cannot be named at all ("a pale liquid from a small bottle") stays out of the ingredients, described in its step and in the note.

## 4. Photos

Pick one full-size frame per step and one of the finished dish for the main photo:

```bash
<ffmpeg> -loglevel error -y -ss <seconds> -i v.mp4 -frames:v 1 -q:v 3 s01.jpg
```

Tile the picks into one strip and look at it before uploading: a frame a second off lands on a transition or a hand. Burned-in subtitles are on every frame of most shorts; that is acceptable. Upload them out of band as `SKILL.md`'s editing mechanics describe, then send steps, photos and main photo in one `edit_recipe`.
