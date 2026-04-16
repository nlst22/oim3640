import os
import string

stop_words = {
    # --- Basic stop words ---
    "the", "and", "a", "an", "i", "you", "me", "my", "we", "our",
    "is", "it", "to", "of", "in", "on", "for", "with", "that",
    "this", "at", "by", "from", "be", "are", "was", "were",
    "so", "but", "if", "or", "as", "not", "no", "just",

    # --- Pronouns & contractions ---
    "he", "she", "him", "her", "his", "hers",
    "they", "them", "their", "theirs",
    "im", "youre", "hes", "shes", "were", "theyre",
    "ive", "youve", "weve", "theyve",
    "ill", "id", "cant", "dont", "wont",
    "shouldnt", "couldnt", "wouldnt", "its", "your"

    # --- Conversational / filler words ---
    "about", "like", "know", "say", "said", "tell", "told",
    "think", "when", "how", "now",
    "really", "maybe", "guess", "wonder",
    "time", "times", "day", "still", "back",

    # --- Generic verbs (low meaning) ---
    "get", "got", "make", "take", "give",
    "go", "going", "gone", "come", "came",
    "see", "find", "call",

    # --- Lyrics-specific filler ---
    "wanna", "gonna", "gotta",
    "talkin", "talk", "lookin", "feelin",
    "tryna", "goin", "comin", "doin",
    "nothin", "somethin", "gettin",

    # --- Sounds / noise ---
    "yeah", "oh", "ooh", "uh",
    "ah", "ahah", "ahha", "ahahah", "ahahahah",
    "mm", "mmm", "mmmm",
    "ohoh", "uhhuh", "haha", "ha",
    "nananana", "nana", "lalalalalalala", "nonono"
}

# function to clean text
def process_lyrics(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    
    text = open(file_path).read().lower()
    
    # remove punctuation
    for p in string.punctuation:
        text = text.replace(p, "")
    
    words = text.split()
    
    # remove stop words
    filtered_words = [w for w in words if w not in stop_words]
    
    return filtered_words


# process both albums
short_n_sweet_words = process_lyrics("short_n_sweet_lyrics.txt")
emails_words = process_lyrics("emails_i_cant_send_lyrics.txt")

# save cleaned data
def save_cleaned(words, filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    
    with open(file_path, "w") as f:
        f.write("\n".join(words))


save_cleaned(short_n_sweet_words, "short_n_sweet_cleaned.txt")
save_cleaned(emails_words, "emails_i_cant_send_cleaned.txt")

def save_frequencies(freq_dict, filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    
    with open(file_path, "w") as f:
        for word, count in sorted(freq_dict.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{word}: {count}\n")

save_frequencies({w: short_n_sweet_words.count(w) for w in set(short_n_sweet_words)}, "short_n_sweet_frequencies.txt")
save_frequencies({w: emails_words.count(w) for w in set(emails_words)}, "emails_i_cant_send_frequencies.txt")