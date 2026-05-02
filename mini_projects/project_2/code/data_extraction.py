import json
import os
from pathlib import Path

from dotenv import load_dotenv
from lyricsgenius import Genius


load_dotenv()

TOKEN = os.getenv("CLIENT_ACCESS_TOKEN")
if not TOKEN:
    raise ValueError("CLIENT_ACCESS_TOKEN not found in .env")

genius = Genius(TOKEN)
genius.verbose = False
genius.remove_section_headers = True

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw" / "sabrina_carpenter"
RAW_DIR.mkdir(parents=True, exist_ok=True)

ALBUMS = {
    "short_n_sweet": {
        "display_name": "Short n' Sweet",
        "tracks": [
            "Taste",
            "Please Please Please",
            "Good Graces",
            "Sharpest Tool",
            "Coincidence",
            "Bed Chem",
            "Espresso",
            "Dumb & Poetic",
            "Slim Pickins",
            "Juno",
            "Lie to Girls",
            "Don't Smile",
        ],
    },
    "emails_i_cant_send": {
        "display_name": "emails i can't send",
        "tracks": [
            "emails i can't send",
            "Vicious",
            "Read your Mind",
            "Tornado Warnings",
            "because i liked a boy",
            "Already Over",
            "how many things",
            "bet u wanna",
            "Nonsense",
            "Fast Times",
            "skinny dipping",
            "Bad for Business",
            "decode",
        ],
    },
}


def fetch_album_to_json(album_name, tracks, json_path):
    data = {
        "artist": "Sabrina Carpenter",
        "album": album_name,
        "songs": [],
    }

    for title in tracks:
        song = genius.search_song(title, "Sabrina Carpenter")
        if song:
            data["songs"].append({"title": title, "lyrics": song.lyrics})
        else:
            print(f"Skipped (not found): {title}")

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def convert_json_to_txt(json_path, txt_path):
    data = json.loads(json_path.read_text(encoding="utf-8"))
    lines = [f"{data['artist']} - {data['album']}", ""]

    for index, song in enumerate(data.get("songs", []), start=1):
        lines.append("=" * 60)
        lines.append(f"{index}. {song.get('title', 'Untitled')}")
        lines.append("=" * 60)
        lines.append("")
        lines.append(song.get("lyrics", ""))
        lines.append("")

    txt_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    DATA_DIR.mkdir(exist_ok=True)

    for album_slug, album_info in ALBUMS.items():
        album_dir = RAW_DIR / album_slug
        album_dir.mkdir(parents=True, exist_ok=True)

        json_path = album_dir / f"{album_slug}_lyrics.json"
        txt_path = DATA_DIR / f"{album_slug}_lyrics.txt"

        fetch_album_to_json(album_info["display_name"], album_info["tracks"], json_path)
        convert_json_to_txt(json_path, txt_path)
        print(f"Saved JSON: {json_path}")
        print(f"Saved TXT:  {txt_path}")


if __name__ == "__main__":
    main()
