stop_words = {
    "the", "and", "a", "an", "i", "you", "me", "my", "we", "our",
    "is", "it", "to", "of", "in", "on", "for", "with", "that",
    "this", "at", "by", "from", "be", "are", "was", "were",
    "so", "but", "if", "or", "as", "not", "no", "just", 
    "yeah", "oh", "ooh", "uh", "la", "na"
}

text = open("short_n_sweet_lyrics.txt").read().lower()

# remove punctuation
import string
for p in string.punctuation:
    text = text.replace(p, "")

words = text.split()

# remove stop words
filtered_words = []
for word in words:
    if word not in stop_words:
        filtered_words.append(word)

text = open("emails_i_cant_send_lyrics.txt").read().lower()

# remove punctuation
import string
for p in string.punctuation:
    text = text.replace(p, "")

words = text.split()

# remove stop words
filtered_words = []
for word in words:
    if word not in stop_words:
        filtered_words.append(word)