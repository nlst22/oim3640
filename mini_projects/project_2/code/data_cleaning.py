from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

ALBUM_FILES = {
    "Short n' Sweet": DATA_DIR / "short_n_sweet_lyrics.txt",
    "emails i can't send": DATA_DIR / "emails_i_cant_send_lyrics.txt",
}

CLEANED_OUTPUTS = {
    "Short n' Sweet": DATA_DIR / "short_n_sweet_cleaned.txt",
    "emails i can't send": DATA_DIR / "emails_i_cant_send_cleaned.txt",
}

FREQUENCY_OUTPUTS = {
    "Short n' Sweet": DATA_DIR / "short_n_sweet_frequencies.txt",
    "emails i can't send": DATA_DIR / "emails_i_cant_send_frequencies.txt",
}

STOP_WORDS = {
    "the", "and", "a", "an", "i", "you", "me", "my", "we", "our",
    "is", "it", "to", "of", "in", "on", "for", "with", "that",
    "this", "at", "by", "from", "be", "are", "was", "were",
    "so", "but", "if", "or", "as", "not", "no", "just",
    "he", "she", "him", "her", "his", "hers",
    "they", "them", "their", "theirs",
    "im", "youre", "hes", "shes", "were", "theyre",
    "ive", "youve", "weve", "theyve",
    "ill", "id", "cant", "dont", "wont",
    "shouldnt", "couldnt", "wouldnt", "its", "your",
    "am", "what", "have", "has", "had", "do", "did", "does", "can",
    "all", "up", "one", "let", "there", "theres", "here", "these",
    "about", "like", "know", "say", "said", "tell", "told",
    "think", "when", "how", "now",
    "really", "maybe", "guess", "wonder",
    "time", "times", "day", "still", "back",
    "get", "got", "make", "take", "give",
    "go", "going", "gone", "come", "came",
    "see", "find", "call",
    "wanna", "gonna", "gotta",
    "talkin", "talk", "lookin", "feelin",
    "tryna", "goin", "comin", "doin",
    "nothin", "somethin", "gettin",
    "yeah", "oh", "ooh", "uh",
    "ah", "ahah", "ahha", "ahahah", "ahahahah",
    "mm", "mmm", "mmmm",
    "ohoh", "uhhuh", "haha", "ha",
    "nananana", "nana", "lalalalalalala", "nonono",
    "la", "ya",
    "t", "s", "m", "re", "ll", "ve", "d", "na", "don", "won",
}


def normalize_text(text):
    replacements = {
        "can't": "cant",
        "won't": "wont",
        "i'm": "im",
        "you're": "youre",
        "it's": "its",
        "don't": "dont",
        "didn't": "didnt",
        "isn't": "isnt",
        "there's": "theres",
        "that's": "thats",
        "i've": "ive",
        "i'll": "ill",
        "i'd": "id",
        "we're": "were",
        "they're": "theyre",
        "\u2005": " ",
        "\u2009": " ",
        "\u00a0": " ",
        "â€™": "'",
        "’": "'",
        "“": " ",
        "”": " ",
        "â€œ": " ",
        "â€": " ",
        "–": " ",
        "—": " ",
    }

    text = text.lower()
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"sabrina carpenter\s*-\s*[^\n]+", " ", text)
    text = re.sub(r"=+", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return text


def tokenize(text):
    return [
        word
        for word in text.split()
        if len(word) > 1 and word not in STOP_WORDS
    ]


def process_lyrics_file(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    normalized = normalize_text(text)
    return tokenize(normalized)


def word_frequency(words):
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def save_cleaned(words, path):
    path.write_text("\n".join(words), encoding="utf-8")


def save_frequencies(freq_dict, path):
    lines = []
    for word, count in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True):
        lines.append(f"{word}: {count}")
    path.write_text("\n".join(lines), encoding="utf-8")


def clean_all_albums():
    cleaned_data = {}
    DATA_DIR.mkdir(exist_ok=True)

    for album, path in ALBUM_FILES.items():
        words = process_lyrics_file(path)
        cleaned_data[album] = words
        save_cleaned(words, CLEANED_OUTPUTS[album])
        save_frequencies(word_frequency(words), FREQUENCY_OUTPUTS[album])

    return cleaned_data


if __name__ == "__main__":
    cleaned = clean_all_albums()
    for album, words in cleaned.items():
        print(f"{album}: cleaned {len(words)} words")
