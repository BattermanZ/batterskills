# Recovering a recipe from its source

The recipe's Source link is the first place to look, and usually the last. Check what comes back against whatever the recipe already holds (same quantities, same dish) before using it. When the method comes from somewhere other than the cited source, say where in the note.

## Web pages

`donsetch fetch '<url>'` returns the page as markdown. Recipe cards keep their ingredient groups ("#### To serve:"), which become section headings. A page's FAQ or tips go in the note.

## YouTube and YouTube Shorts

Most creators put the full recipe in the description. `yt-dlp` is not installed; run it through `uvx`:

```bash
uvx yt-dlp --skip-download --write-description --write-auto-subs \
  --sub-langs 'en.*' --sub-format vtt -o '<name>' '<url>'
```

The `.description` file usually holds ingredients and method. When it is empty or partial, the captions carry what the creator says: strip the timing lines and de-duplicate.

When the creator says the recipe is "on screen", it is only in the frames. Download the video stream and cut frames with the ffmpeg bundled in `imageio-ffmpeg` (no system ffmpeg):

```bash
uvx yt-dlp -f 'bv*[height<=720]' -o <name>.mp4 '<url>'
uv run --with imageio-ffmpeg python -c "
import imageio_ffmpeg, subprocess
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-ss', '<start-seconds>',
  '-i', '<name>.mp4', '-vf', 'fps=1,scale=360:-1,tile=6x2', '-frames:v', '2', 'sheet%d.jpg'], check=True)"
```

Read the contact sheets as images. Recipe cards usually sit in the last third of a short.

## Instagram

The Crouton import stripped every non-ASCII character from Instagram captions. The live reel page still has them: re-fetch it rather than retyping accents. To find damaged recipes, search Kamosu for broken word forms (`mlangez`, `prparation`, `ingrdients`), never a stem that matches an intact word, since search folds accents.

## When the source has no method

A caption with ingredients and no method was often posted in full elsewhere by the same creator (their blog, a later post). Use it only when its quantities match the saved ones.
