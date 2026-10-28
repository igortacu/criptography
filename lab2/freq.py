"""Letter, bigram and trigram statistics for a monoalphabetic ciphertext (Lab 2)."""
import sys
from collections import Counter
from string import ascii_uppercase as ABC

# letter frequencies of English, % (Table 2.2 of the assignment)
ENGLISH = dict(zip(ABC, [8.17, 1.49, 2.78, 4.25, 12.7, 2.23, 2.01, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41,
                         6.75, 7.51, 1.93, 0.09, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]))


def letters(text):
    return [c for c in text.upper() if c in ABC]


def letter_freq(text):
    return Counter(letters(text))


def ngrams(text, n, top=10):
    words = "".join(c if c in ABC else " " for c in text.upper()).split()
    grams = Counter(w[i:i + n] for w in words for i in range(len(w) - n + 1))
    return grams.most_common(top)


def apply(text, mapping):
    """mapping: cipher letter -> plain letter. Known letters come out lowercase, the rest stay uppercase."""
    return "".join(mapping.get(c.upper(), c.upper()) if c.isalpha() else c for c in text)


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read()
    cnt = letter_freq(text)
    total = sum(cnt.values())
    print(f"{total} letters\n\nCipher letter frequencies (descending)")
    for ch, k in cnt.most_common():
        print(f"  {ch}  {k:4d}  {100 * k / total:5.2f}%")
    print("\nEnglish, descending:", " ".join(sorted(ABC, key=lambda c: -ENGLISH[c])))
    print("Cipher,  descending:", " ".join(ch for ch, _ in cnt.most_common()))
    for n, name in ((2, "bigrams"), (3, "trigrams")):
        print(f"\nTop {name}:", ", ".join(f"{g}({k})" for g, k in ngrams(text, n)))
    words = Counter("".join(c if c in ABC else " " for c in text.upper()).split())
    print("\nTop words:", ", ".join(f"{w}({k})" for w, k in words.most_common(12)))
