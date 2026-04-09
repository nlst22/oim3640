from dotenv import load_dotenv
import json
import os
from pathlib import Path

from lyricsgenius import Genius

load_dotenv()

token = os.getenv("CLIENT_ACCESS_TOKEN")
if not token:
    raise ValueError("CLIENT_ACCESS_TOKEN not found in .env")

genius = Genius(token)
genius.verbose = False
genius.remove_section_headers = True

BASE_DIR = Path(__file__).resolve().parent
SHORT_N_SWEET_DIR = BASE_DIR / "short_n_sweet"
SHORT_N_SWEET_DIR.mkdir(parents=True, exist_ok=True)

SHORT_N_SWEET_JSON_PATH = SHORT_N_SWEET_DIR / "short_n_sweet_lyrics.json"
SHORT_N_SWEET_TXT_PATH = SHORT_N_SWEET_DIR / "short_n_sweet_lyrics.txt"

EMAILS_I_CANT_SEND_DIR = BASE_DIR / "emails_i_cant_send"
EMAILS_I_CANT_SEND_DIR.mkdir(parents=True, exist_ok=True)

EMAILS_I_CANT_SEND_JSON_PATH = EMAILS_I_CANT_SEND_DIR / "emails_i_cant_send_lyrics.json"
EMAILS_I_CANT_SEND_TXT_PATH = EMAILS_I_CANT_SEND_DIR / "emails_i_cant_send_lyrics.txt"

SHORT_N_SWEET_TRACKS = [
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
]

EMAILS_I_CANT_SEND_TRACKS = [
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
]


def fetch_album_to_json(album_name: str, tracks: list[str], json_path: Path) -> None:
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

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def convert_json_to_txt(json_path: Path, txt_path: Path) -> None:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    with txt_path.open("w", encoding="utf-8") as f:
        f.write(f"{data['artist']} - {data['album']}\n\n")

        for i, song in enumerate(data.get("songs", []), start=1):
            f.write(f"{'=' * 60}\n")
            f.write(f"{i}. {song.get('title', 'Untitled')}\n")
            f.write(f"{'=' * 60}\n\n")
            f.write(song.get("lyrics", ""))
            f.write("\n\n")


if __name__ == "__main__":
    fetch_album_to_json("Short n' Sweet", SHORT_N_SWEET_TRACKS, SHORT_N_SWEET_JSON_PATH)
    convert_json_to_txt(SHORT_N_SWEET_JSON_PATH, SHORT_N_SWEET_TXT_PATH)
    print(f"Saved JSON: {SHORT_N_SWEET_JSON_PATH}")
    print(f"Saved TXT:  {SHORT_N_SWEET_TXT_PATH}")

    fetch_album_to_json("emails i can't send", EMAILS_I_CANT_SEND_TRACKS, EMAILS_I_CANT_SEND_JSON_PATH)
    convert_json_to_txt(EMAILS_I_CANT_SEND_JSON_PATH, EMAILS_I_CANT_SEND_TXT_PATH)
    print(f"Saved JSON: {EMAILS_I_CANT_SEND_JSON_PATH}")
    print(f"Saved TXT:  {EMAILS_I_CANT_SEND_TXT_PATH}")


