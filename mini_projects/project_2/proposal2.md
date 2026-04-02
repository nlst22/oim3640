## My Project Proposal

**What I'm building:**  
I'm building a Song Lyrics Analyzer in Python to compare vocabulary and themes across albums by one artist.

**Why I chose this:**  
I listen to this artist often and want to see whether their writing style changes over time (more complex words, different tone, recurring themes).

**Core features:**  
- Load lyrics from multiple songs/albums stored in text files.  
- Clean text (lowercase, remove punctuation, remove stop words).  
- Compute per-album stats: total words, unique words, type-token ratio, and average word length, sentiment shift over time. 
- Find most common words per album and words that are distinctive to each album.  
- Create at least one visualization (e.g., bar chart of top words or vocabulary richness by album).

**What I don't know yet:**  
- Best way to collect and format lyrics data cleanly.  
- How to handle repeated chorus lines fairly.  
- Which stop-word list to use for lyrics (some common words may still be meaningful).  
- How to measure “complexity” in a way that is easy to explain.  
- Which visualization best tells the story clearly.


# **Next steps:**

## Implementation Plan (Step-by-Step)

1. **Lock scope**
   - Choose one artist and 3–6 albums.
   - Define inclusion rules (standard tracks only vs deluxe/live/remix).

2. **Collect lyrics data**
   - Use **Genius API** through Python package `lyricsgenius` to search songs and fetch lyrics.
   - Save raw lyrics locally (`data/raw/<album>/<track>.txt`) for reproducibility.
   - Keep metadata in a table: `song`, `album`, `year`, `track_number`.

3. **Clean and preprocess text**
   - Lowercase, remove punctuation, tokenize.
   - Remove stop words (start with NLTK list, then customize for lyrics context).
   - Keep two modes for repeated choruses:
     - `full_text` (all lines kept)
     - `dedup_lines` (exact repeated lines removed)

4. **Compute album metrics**
   - Total words
   - Unique words
   - Type-token ratio
   - Average word length
   - Optional: hapax legomena count (words appearing once)

5. **Theme and distinctiveness analysis**
   - Most common words per album (top N).
   - Distinctive album words using TF-IDF by album.
   - Optional: bigrams for recurring themes.

6. **Sentiment over time**
   - Compute sentiment per song, then aggregate by album.
   - Plot trend by release year to show tonal shift.

7. **Visualize and interpret**
   - Bar chart: vocabulary richness (TTR) by album.
   - Line chart: sentiment shift by album/year.
   - Bar chart: top distinctive words for each album.

8. **Report limitations**
   - API coverage gaps / missing songs.
   - Chorus repetition handling impact.
   - Stop-word choice impact on interpretation.

## API + Library Recommendation

- **Lyrics source API:** `lyricsgenius` (Genius API wrapper)  
- **Data handling:** `pandas`  
- **Text preprocessing:** `nltk` (or `spaCy`)  
- **Distinctive words (TF-IDF):** `scikit-learn`  
- **Sentiment:** `vaderSentiment` (simple and effective for short text)  
- **Visualization:** `matplotlib` + `seaborn`

## Suggested Folder Structure

- `data/raw/` → original lyrics text files  
- `data/processed/` → cleaned/tokenized outputs  
- `notebooks/` or `src/` → analysis scripts  
- `outputs/figures/` → charts for final presentation

## Minimum Viable Milestones

1. Load + clean lyrics for at least 2 albums  
2. Produce core metrics table per album  
3. Generate 1 visualization  
4. Add sentiment trend  
5. Expand to full selected discography
