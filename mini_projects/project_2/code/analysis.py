from pathlib import Path
from collections import Counter

from data_cleaning import clean_all_albums


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
REPORT_PATH = OUTPUT_DIR / "analysis_summary.txt"


def get_top_words(freq, n=10):
    return sorted(freq.items(), key=lambda item: item[1], reverse=True)[:n]


def album_stats(words):
    total_words = len(words)
    unique_words = len(set(words))
    type_token_ratio = unique_words / total_words if total_words else 0
    average_word_length = (
        sum(len(word) for word in words) / total_words if total_words else 0
    )

    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "type_token_ratio": type_token_ratio,
        "average_word_length": average_word_length,
    }


def distinctive_words(target_album, counters):
    target_counter = counters[target_album]
    other_album = [album for album in counters if album != target_album][0]
    other_counter = counters[other_album]
    target_total = sum(target_counter.values())
    other_total = sum(other_counter.values())

    scores = []
    for word, count in target_counter.items():
        score = (count / target_total) - (other_counter.get(word, 0) / other_total)
        scores.append((word, score, count))

    scores.sort(key=lambda item: item[1], reverse=True)
    return scores[:10]


def make_top_word_chart(album, top_words):
    words = [word for word, _ in top_words]
    counts = [count for _, count in top_words]
    output_name = album.lower().replace(" ", "_").replace("'", "").replace("-", "_")
    write_bar_chart(
        title=f"Top Words in {album}",
        labels=words,
        values=counts,
        output_path=OUTPUT_DIR / f"{output_name}_top_words.svg",
        color="#4C78A8",
    )


def make_vocab_chart(stats_by_album):
    albums = list(stats_by_album.keys())
    ttr_values = [stats_by_album[album]["type_token_ratio"] for album in albums]
    write_bar_chart(
        title="Vocabulary Richness by Album",
        labels=albums,
        values=ttr_values,
        output_path=OUTPUT_DIR / "vocabulary_richness.svg",
        color="#F58518",
        value_format="{:.3f}",
    )


def write_bar_chart(title, labels, values, output_path, color, value_format="{}"):
    width = 900
    height = 500
    left_margin = 70
    right_margin = 30
    top_margin = 60
    bottom_margin = 140
    chart_width = width - left_margin - right_margin
    chart_height = height - top_margin - bottom_margin
    max_value = max(values) if values else 1
    bar_width = chart_width / max(len(values), 1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="white" />',
        f'<text x="{width / 2}" y="30" text-anchor="middle" font-size="22" font-family="Arial">{title}</text>',
        f'<line x1="{left_margin}" y1="{top_margin + chart_height}" '
        f'x2="{left_margin + chart_width}" y2="{top_margin + chart_height}" stroke="black" />',
        f'<line x1="{left_margin}" y1="{top_margin}" '
        f'x2="{left_margin}" y2="{top_margin + chart_height}" stroke="black" />',
    ]

    for index, (label, value) in enumerate(zip(labels, values)):
        x = left_margin + index * bar_width + 10
        usable_width = max(bar_width - 20, 20)
        bar_height = 0 if max_value == 0 else (value / max_value) * chart_height
        y = top_margin + chart_height - bar_height
        label_x = x + usable_width / 2

        parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{usable_width:.2f}" height="{bar_height:.2f}" fill="{color}" />'
        )
        parts.append(
            f'<text x="{label_x:.2f}" y="{y - 8:.2f}" text-anchor="middle" font-size="12" font-family="Arial">'
            f'{value_format.format(value)}</text>'
        )
        parts.append(
            f'<text x="{label_x:.2f}" y="{top_margin + chart_height + 20:.2f}" text-anchor="end" '
            f'transform="rotate(-35 {label_x:.2f},{top_margin + chart_height + 20:.2f})" '
            f'font-size="12" font-family="Arial">{label}</text>'
        )

    output_path.write_text("\n".join(parts + ["</svg>"]), encoding="utf-8")


def format_report(stats_by_album, counters):
    lines = []
    lines.append("Sabrina Carpenter Lyrics Analysis")
    lines.append("")
    lines.append("Question 1: Which album has richer vocabulary?")
    lines.append("")

    richer_album = max(
        stats_by_album,
        key=lambda album: (
            stats_by_album[album]["type_token_ratio"],
            stats_by_album[album]["average_word_length"],
        ),
    )

    for album, stats in stats_by_album.items():
        lines.append(
            f"{album}: total words={stats['total_words']}, "
            f"unique words={stats['unique_words']}, "
            f"type-token ratio={stats['type_token_ratio']:.3f}, "
            f"average word length={stats['average_word_length']:.2f}"
        )

    lines.append("")
    lines.append(
        f"Finding: {richer_album} has the richer vocabulary based on type-token ratio."
    )
    lines.append("")
    lines.append("Question 2: What words are most distinctive to each album?")
    lines.append("")

    for album in counters:
        lines.append(f"{album}:")
        lines.append(
            "Top words: "
            + ", ".join(f"{word} ({count})" for word, count in get_top_words(counters[album]))
        )
        lines.append(
            "Distinctive words: "
            + ", ".join(
                f"{word} ({count})"
                for word, _, count in distinctive_words(album, counters)
            )
        )
        lines.append("")

    lines.append("Interpretation:")
    lines.append(
        "Short n' Sweet repeats playful and sharp words like 'please', 'lie', 'girls', and 'taste'."
    )
    lines.append(
        "emails i can't send leans more toward reflective words like 'mind', 'why', 'things', and 'decode'."
    )
    lines.append("")
    lines.append("Built-in Python vs libraries reflection:")
    lines.append(
        "Doing the counting and cleaning with plain strings, lists, dictionaries, and sets made the logic much clearer."
    )
    lines.append(
        "Creating the charts as SVG files took more work than using a plotting library, but it kept the project self-contained and made the visualization logic easier to understand."
    )

    return "\n".join(lines)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    cleaned_data = clean_all_albums()
    counters = {album: Counter(words) for album, words in cleaned_data.items()}
    stats_by_album = {album: album_stats(words) for album, words in cleaned_data.items()}

    for album, counter in counters.items():
        make_top_word_chart(album, get_top_words(counter))

    make_vocab_chart(stats_by_album)

    report = format_report(stats_by_album, counters)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
