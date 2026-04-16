import os
import matplotlib.pyplot as plt

def load_words(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    
    with open(file_path, "r") as f:
        words = f.read().splitlines()
    
    return words


def word_frequency(words):
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


# load cleaned data
sns_words = load_words("short_n_sweet_cleaned.txt")
emails_words = load_words("emails_i_cant_send_cleaned.txt")

# compute frequencies
short_n_sweet_freq = word_frequency(sns_words)
emails_freq = word_frequency(emails_words)

### Visualization

def get_top_words(freq, n=10):
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]

sns_top = get_top_words(short_n_sweet_freq)
emails_top = get_top_words(emails_freq)

# unpack
sns_words, sns_counts = zip(*sns_top)
emails_words, emails_counts = zip(*emails_top)

plt.figure()
plt.bar(sns_words, sns_counts)
plt.xticks(rotation=45)
plt.title("Top Words - Short n Sweet")
plt.show()

plt.figure()
plt.bar(emails_words, emails_counts)
plt.xticks(rotation=45)
plt.title("Top Words - Emails I Can't Send")
plt.show()