"""Mini Project 2: Song Lyrics Analyzer.

Expected data layout (one artist, multiple albums):

mini_projects/project_2/lyrics_data/
	album_1/
		song_a.txt
		song_b.txt
	album_2/
		song_c.txt
		song_d.txt

Run from workspace root:
	python mini_projects/project_2/code.py

Optional arguments:
	--data-dir <path>          Path to lyrics_data folder
	--top-n 10                 Number of top/distinctive words to show
	--drop-repeated-lines      Remove repeated lines within each song
	--plot                     Try plotting vocabulary richness by album
	--sentiment-engine         Sentiment backend: auto (prefer vader), vader (require), or lexicon (built-in tiny list)
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from statistics import mean
from string import punctuation
from typing import Any

# Simple built-in stopword list (customizable)
STOPWORDS = {
	"a",
	"an",
	"and",
	"are",
	"as",
	"at",
	"be",
	"been",
	"but",
	"by",
	"for",
	"from",
	"had",
	"has",
	"have",
	"he",
	"her",
	"here",
	"hers",
	"him",
	"his",
	"i",
	"if",
	"in",
	"into",
	"is",
	"it",
	"its",
	"me",
	"my",
	"of",
	"on",
	"or",
	"our",
	"ours",
	"she",
	"so",
	"than",
	"that",
	"the",
	"their",
	"theirs",
	"them",
	"then",
	"there",
	"these",
	"they",
	"this",
	"those",
	"to",
	"too",
	"up",
	"us",
	"was",
	"we",
	"were",
	"what",
	"when",
	"where",
	"which",
	"who",
	"why",
	"with",
	"you",
	"your",
	"yours",
	# Lyrics filler words you may or may not want to keep
	"oh",
	"yeah",
	"na",
	"la",
	"ooh",
	"ah",
}


# Tiny lexicon for sentiment trend (built-in, no external libs)
POSITIVE_WORDS = {
	"love",
	"happy",
	"smile",
	"good",
	"great",
	"light",
	"hope",
	"free",
	"heaven",
	"beautiful",
	"dream",
	"joy",
	"peace",
	"win",
	"alive",
}

NEGATIVE_WORDS = {
	"hate",
	"sad",
	"cry",
	"pain",
	"dark",
	"bad",
	"lost",
	"lonely",
	"cold",
	"fear",
	"broken",
	"tears",
	"hurt",
	"die",
	"death",
}


def read_text(path: Path) -> str:
	"""Read UTF-8 text file safely."""
	return path.read_text(encoding="utf-8", errors="ignore")


def normalize_line(line: str) -> str:
	"""Normalize line so duplicate detection is more robust."""
	translator = str.maketrans("", "", punctuation)
	return line.lower().translate(translator).strip()


def maybe_drop_repeated_lines(text: str, drop_repeated: bool) -> str:
	"""Remove repeated normalized lines within a song if requested."""
	if not drop_repeated:
		return text

	kept_lines: list[str] = []
	seen: set[str] = set()

	for raw_line in text.splitlines():
		normalized = normalize_line(raw_line)
		if not normalized:
			continue
		if normalized in seen:
			continue
		seen.add(normalized)
		kept_lines.append(raw_line)

	return "\n".join(kept_lines)


def tokenize(text: str) -> list[str]:
	"""Tokenize text into words (Unicode letters, optional apostrophes)."""
	text = text.replace("’", "'")
	return re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)*", text.lower(), flags=re.UNICODE)


def clean_tokens(tokens: list[str], stopwords: set[str]) -> list[str]:
	"""Remove punctuation remnants, short artifacts, and stopwords."""
	cleaned: list[str] = []
	for token in tokens:
		token = token.strip("'")
		if not token:
			continue
		if token in stopwords:
			continue
		cleaned.append(token)
	return cleaned


def get_sentiment_analyzer(engine: str) -> Any | None:
	"""Return a VADER analyzer when available/requested; else None."""
	if engine == "lexicon":
		return None
	try:
		from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
		return SentimentIntensityAnalyzer()
	except Exception:
		if engine == "vader":
			raise RuntimeError(
				"vaderSentiment is not installed. Install with: pip install vaderSentiment"
			)
		return None


def sentiment_score(tokens: list[str], analyzer: Any | None = None) -> float:
	"""Compute sentiment score in [-1, 1] via VADER if available, else tiny lexicon."""
	if not tokens:
		return 0.0
	if analyzer is not None:
		return float(analyzer.polarity_scores(" ".join(tokens))["compound"])
	pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
	neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
	return (pos - neg) / len(tokens)


def safe_div(a: float, b: float) -> float:
	return a / b if b else 0.0


def load_album_tokens(
	data_dir: Path, drop_repeated_lines: bool
) -> tuple[dict[str, list[str]], dict[str, int]]:
	"""Load album folders and aggregate cleaned tokens + raw word counts per album."""
	album_tokens: dict[str, list[str]] = {}
	album_raw_counts: dict[str, int] = {}

	if not data_dir.exists():
		raise FileNotFoundError(f"Data directory not found: {data_dir}")

	album_dirs = sorted([p for p in data_dir.iterdir() if p.is_dir()])
	if not album_dirs:
		raise ValueError(f"No album folders found in: {data_dir}")

	for album_dir in album_dirs:
		all_tokens: list[str] = []
		raw_total = 0
		song_files = sorted(
			[p for p in album_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".txt"]
		)

		if not song_files:
			print(f"Warning: no .txt files found in album folder '{album_dir.name}'")

		for song_file in song_files:
			raw_text = read_text(song_file)
			filtered_text = maybe_drop_repeated_lines(raw_text, drop_repeated_lines)
			raw_tokens = tokenize(filtered_text)
			raw_total += len(raw_tokens)
			tokens = clean_tokens(raw_tokens, STOPWORDS)
			all_tokens.extend(tokens)

		album_tokens[album_dir.name] = all_tokens
		album_raw_counts[album_dir.name] = raw_total

	return album_tokens, album_raw_counts


def album_stats(
	tokens: list[str], raw_total_words: int, analyzer: Any | None = None
) -> dict[str, float]:
	"""Compute vocabulary and style metrics for one album."""
	total_words = raw_total_words
	analyzed_words = len(tokens)
	unique_words = len(set(tokens))
	ttr = safe_div(unique_words, analyzed_words)
	avg_word_len = mean([len(t) for t in tokens]) if tokens else 0.0
	sent_score = sentiment_score(tokens, analyzer=analyzer)

	return {
		"total_words": float(total_words),
		"analyzed_words": float(analyzed_words),
		"unique_words": float(unique_words),
		"type_token_ratio": ttr,
		"avg_word_length": avg_word_len,
		"sentiment_score": sent_score,
	}


def distinctive_words(
	album_name: str,
	album_counter: Counter[str],
	all_counters: dict[str, Counter[str]],
	top_n: int = 10,
) -> list[tuple[str, float]]:
	"""Find words overrepresented in one album versus the others.

	Score is ratio of smoothed relative frequency:
		(p_album + eps) / (p_other + eps)
	"""
	eps = 1e-9
	total_album = sum(album_counter.values())

	other_counter: Counter[str] = Counter()
	for name, counter in all_counters.items():
		if name != album_name:
			other_counter.update(counter)

	total_other = sum(other_counter.values())
	results: list[tuple[str, float]] = []

	for word, count in album_counter.items():
		if count < 2:
			continue
		p_album = count / total_album if total_album else 0.0
		p_other = safe_div(other_counter[word], total_other)
		score = (p_album + eps) / (p_other + eps)
		results.append((word, score))

	return sorted(results, key=lambda x: x[1], reverse=True)[:top_n]


def print_section_header(title: str) -> None:
	print("\n" + "=" * 72)
	print(title)
	print("=" * 72)


def print_album_summary(
	stats_by_album: dict[str, dict[str, float]],
	counters_by_album: dict[str, Counter[str]],
	top_n: int,
) -> None:
	"""Print stats, top words, and distinctive words per album."""
	print_section_header("ALBUM SUMMARY")

	for album, stats in stats_by_album.items():
		print(f"\nAlbum: {album}")
		print(f"  Total words (raw): {int(stats['total_words'])}")
		print(f"  Words analyzed   : {int(stats['analyzed_words'])}")
		print(f"  Unique words     : {int(stats['unique_words'])}")
		print(f"  Type-token ratio : {stats['type_token_ratio']:.3f}")
		print(f"  Avg word length  : {stats['avg_word_length']:.2f}")
		print(f"  Sentiment score  : {stats['sentiment_score']:.4f}")

		top_words = counters_by_album[album].most_common(top_n)
		top_words_str = ", ".join([f"{w}({c})" for w, c in top_words]) if top_words else "None"
		print(f"  Top {top_n} words    : {top_words_str}")

		distinct = distinctive_words(album, counters_by_album[album], counters_by_album, top_n=top_n)
		distinct_str = ", ".join([f"{w}({s:.1f}x)" for w, s in distinct]) if distinct else "None"
		print(f"  Distinctive words: {distinct_str}")


def ascii_bar_chart(values: dict[str, float], title: str, width: int = 40) -> None:
	"""Fallback visualization using terminal bars."""
	print_section_header(title)

	if not values:
		print("No values to plot.")
		return

	max_value = max(values.values())
	if max_value <= 0:
		for label in values:
			print(f"{label:20} | ")
		return

	for label, value in values.items():
		bar_len = int((value / max_value) * width)
		bar = "#" * bar_len
		print(f"{label:20} | {bar} {value:.3f}")


def plot_vocab_richness(values: dict[str, float]) -> None:
	"""Optional matplotlib chart if available."""
	try:
		import matplotlib.pyplot as plt
	except Exception:
		ascii_bar_chart(values, "VOCABULARY RICHNESS (ASCII CHART)")
		return

	albums = list(values.keys())
	ttr_values = [values[a] for a in albums]

	plt.figure(figsize=(10, 5))
	plt.bar(albums, ttr_values)
	plt.title("Vocabulary Richness by Album (Type-Token Ratio)")
	plt.xlabel("Album")
	plt.ylabel("Type-Token Ratio")
	plt.xticks(rotation=30, ha="right")
	plt.tight_layout()
	plt.show()


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Song Lyrics Analyzer")
	parser.add_argument(
		"--data-dir",
		type=str,
		default="mini_projects/project_2/lyrics_data",
		help="Path to album folders containing .txt song lyrics",
	)
	parser.add_argument(
		"--top-n",
		type=int,
		default=10,
		help="Top N words to display",
	)
	parser.add_argument(
		"--drop-repeated-lines",
		action="store_true",
		help="Drop repeated lines per song to reduce chorus repetition bias",
	)
	parser.add_argument(
		"--plot",
		action="store_true",
		help="Show vocabulary richness chart (matplotlib if installed, else ASCII)",
	)
	parser.add_argument(
		"--sentiment-engine",
		type=str,
		choices=["auto", "vader", "lexicon"],
		default="auto",
		help="Sentiment backend: auto (prefer vader), vader (require), or lexicon (built-in tiny list)",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	data_dir = Path(args.data_dir)
	analyzer = get_sentiment_analyzer(args.sentiment_engine)

	album_tokens, album_raw_counts = load_album_tokens(data_dir, args.drop_repeated_lines)

	counters_by_album: dict[str, Counter[str]] = {
		album: Counter(tokens) for album, tokens in album_tokens.items()
	}
	stats_by_album: dict[str, dict[str, float]] = {
		album: album_stats(tokens, album_raw_counts.get(album, 0), analyzer=analyzer)
		for album, tokens in album_tokens.items()
	}

	print_album_summary(stats_by_album, counters_by_album, top_n=args.top_n)

	vocab_richness = {
		album: stats["type_token_ratio"] for album, stats in stats_by_album.items()
	}

	if args.plot:
		plot_vocab_richness(vocab_richness)
	else:
		ascii_bar_chart(vocab_richness, "VOCABULARY RICHNESS (ASCII CHART)")


if __name__ == "__main__":
	main()
