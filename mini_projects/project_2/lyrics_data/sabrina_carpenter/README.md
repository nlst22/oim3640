# Sabrina Carpenter Dataset Setup

Use this folder structure for your two-album analysis:

- `emails_i_cant_send/`  -> one `.txt` file per song
- `short_n_sweet/`      -> one `.txt` file per song

## How to add data

1. Create one text file per song (example: `nonsense.txt`, `feather.txt`).
2. Paste only the lyrics text into each file.
3. Avoid adding metadata lines (credits, URLs, annotations).
4. Save files as UTF-8.

## Run analyzer

From workspace root:

`python mini_projects/project_2/code.py --data-dir mini_projects/project_2/lyrics_data/sabrina_carpenter --top-n 10 --drop-repeated-lines --plot`

If `matplotlib` is not installed, omit `--plot` and you'll still get an ASCII chart.

## API options for downloading lyrics files

If you want to automate `.txt` creation per song, use a **licensed lyrics API**.

### Recommended API stack

1. **Spotify Web API** (album + track list metadata)
   - Get album IDs and track names.
   - Docs: https://developer.spotify.com/documentation/web-api

2. **Musixmatch API** or **LyricFind API** (lyrics content)
   - These are licensed providers; access level determines whether full lyrics export is allowed.
   - Musixmatch: https://developer.musixmatch.com/
   - LyricFind: https://www.lyricfind.com/api/

> Note: The Genius API provides metadata but generally not full-lyrics text via official API endpoints.

### Minimal automation flow

1. Query album tracks from Spotify API.
2. For each track, request lyrics from Musixmatch/LyricFind (per your license).
3. Save response text to:
   - `emails_i_cant_send/<song_name>.txt`
   - `short_n_sweet/<song_name>.txt`
4. Keep UTF-8 encoding and plain lyrics text only.

### Python packages commonly used

- `requests`
- `python-dotenv` (store API keys in `.env`)
- optional: `spotipy` for Spotify convenience wrapper

### Important

Bulk downloading full lyrics without proper rights may violate API terms and copyright rules.  
Use only provider-approved endpoints and license scopes.
