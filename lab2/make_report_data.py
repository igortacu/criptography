"""Builds the figure and the LaTeX fragments used by the Lab 2 report from the real attack output."""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from freq import ENGLISH, ABC, letter_freq, apply
from attack import STEPS, text

cnt = letter_freq(text)
total = sum(cnt.values())

# ---- figure: English (left) vs intercepted text (right), both in %
fig, ax = plt.subplots(1, 2, figsize=(10, 3.2), sharey=True)
ax[0].bar(list(ABC), [ENGLISH[c] for c in ABC], color="#4a7ebb")
ax[0].set_title("Limba engleză")
ax[1].bar(list(ABC), [100 * cnt[c] / total for c in ABC], color="#bb4a4a")
ax[1].set_title("Criptograma interceptată (V23)")
for a in ax:
    a.set_ylabel("Frecvența, %")
    a.tick_params(labelsize=7)
fig.tight_layout()
fig.savefig("images/freq_compare.png", dpi=200)

# ---- table 2.3 / 2.4 rows
by_alpha = " & ".join(f"{cnt[c]}" for c in ABC)
ranked = cnt.most_common()
with open("tables.tex", "w") as f:
    f.write("\\def\\rowAlpha{" + " & ".join(ABC) + "}\n")
    f.write("\\def\\rowCnt{" + by_alpha + "}\n")
    f.write("\\def\\rowRankL{" + " & ".join(c for c, _ in ranked) + "}\n")
    f.write("\\def\\rowRankN{" + " & ".join(str(k) for _, k in ranked) + "}\n")

# ---- partial plaintexts after every step (first 5 lines, wrapped)
def wrap(s, w=92):
    return "\n".join(textwrap.fill(line, w) for line in s.splitlines())

mapping = {}
out = []
for i, (step, why) in enumerate(STEPS, 1):
    for pair in step.split(", "):
        c, p = pair.split("=")
        mapping[c.upper()] = p
    head = "\n".join(l[:88] for l in apply(text, mapping).splitlines()[:5])
    out.append(f"\\paragraph{{Pasul {i}: {step}.}} {why.replace('_', ' ')}\n"
               f"\\begin{{lstlisting}}[language={{}}]\n{head}\n\\end{{lstlisting}}\n")
open("stages.tex", "w").write("\n".join(out))

plain = apply(text, mapping).lower().replace("\u2014", "--")
open("plaintext_v23.txt", "w").write(plain)
open("plaintext.tex", "w").write("\\begin{lstlisting}[language={}]\n" + textwrap.fill(plain.replace("\n", " "), 92) + "\n\\end{lstlisting}\n")

inv = {p: c for c, p in mapping.items()}
with open("key.tex", "w") as f:
    f.write("\\def\\keyPlain{" + " & ".join(ABC.lower()) + "}\n")
    f.write("\\def\\keyCipher{" + " & ".join(inv[p] for p in ABC.lower()) + "}\n")

# sanity: the key is a permutation and decryption is reversible
assert sorted(mapping) == list(ABC) and sorted(mapping.values()) == list(ABC.lower())
print("ok", total, "letters")
