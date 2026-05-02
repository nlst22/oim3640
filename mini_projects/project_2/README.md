# Mini Project 2: Text Analysis

## Project Overview

This project analyzes lyrics from two Sabrina Carpenter albums:

- `Short n' Sweet`
- `emails i can't send`

The goal is to answer two questions:

1. Which album has richer vocabulary?
2. What words are most distinctive to each album?

## Files

- `PROPOSAL.md` - project proposal
- `code/data_extraction.py` - optional script to fetch lyrics from Genius
- `code/data_cleaning.py` - cleans raw lyrics and saves cleaned word lists
- `code/analysis.py` - runs the comparison, prints findings, and saves charts
- `data/` - raw lyrics, cleaned word lists, and frequency files
- `outputs/analysis_summary.txt` - written summary of the findings
- `outputs/*.svg` - saved charts

## How It Works

The project uses built-in Python for the main text analysis:

- strings for cleaning text
- lists for tokenized words
- dictionaries for word frequencies
- sets for vocabulary size
- file I/O for reading lyrics and writing results

Then it uses built-in Python to write simple SVG bar charts for the final visuals.

## Questions and Findings

### 1. Which album has richer vocabulary?

Based on type-token ratio, `Short n' Sweet` has slightly richer vocabulary.

- `Short n' Sweet`: 1480 total words, 584 unique words, type-token ratio `0.395`, average word length `5.04`
- `emails i can't send`: 1574 total words, 607 unique words, type-token ratio `0.386`, average word length `5.24`

The two albums are close. `Short n' Sweet` has the stronger type-token ratio, while `emails i can't send` has more total unique words and slightly longer average word length.

### 2. What words are most distinctive to each album?

Some of the most distinctive words in `Short n' Sweet` are:

- `please`
- `lie`
- `girls`
- `taste`
- `chem`

Some of the most distinctive words in `emails i can't send` are:

- `why`
- `mind`
- `things`
- `decode`
- `vicious`

This suggests that `Short n' Sweet` leans more playful and sharp, while `emails i can't send` sounds more reflective and emotional.

## Visualizations

The project saves these charts in `outputs/`:

- top words for `Short n' Sweet` as an SVG chart
- top words for `emails i can't send` as an SVG chart
- a vocabulary richness comparison chart as SVG

## Built-in Python vs Libraries Reflection

Doing the cleaning and counting with built-in Python helped me understand exactly how the analysis works. I had to think through how to normalize text, remove stop words, and count frequencies myself.

Writing the SVG charts directly in Python took more work than using a charting library, but it kept the project self-contained and helped me understand how the visual output is built from the data.

## What Surprised Me

What surprised me most was how close the albums were on vocabulary richness. I expected one album to stand out much more, but instead the biggest difference showed up in the kinds of words repeated, not just the number of different words.

## How to Run

From the project root, run:

```bash
python mini_projects/project_2/code/analysis.py
```

This will:

- regenerate cleaned text files
- update frequency files
- print the findings
- save charts and a written summary in `mini_projects/project_2/outputs/`
