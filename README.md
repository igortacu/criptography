# Cryptography - Laboratory Work No. 1: Caesar cipher

Caesar cipher (one key) and Caesar cipher with a keyword permutation (two keys) over the
Romanian alphabet (n = 31), written in Python 3 with no dependencies.

    python3 caesar.py            # interactive program
    python3 -m unittest -v       # tests (checked against the examples from the assignment)

- `caesar.py` - implementation and console interface
- `test_caesar.py` - unit tests
- `samples/` - recorded program sessions used in the report
- `report.tex` / `report.pdf` - the lab report (`pdflatex report.tex`, run twice)

## Lab 2 - Cryptanalysis of monoalphabetic ciphers (variant 23)

Frequency-analysis attack on an English ciphertext, see `lab2/`:

    cd lab2
    python3 freq.py cipher_v23.txt     # letter / bigram / trigram statistics
    python3 attack.py                  # the chain of substitutions and the recovered plaintext
    python3 make_report_data.py        # figure + LaTeX fragments, then: pdflatex report.tex

- `cipher_v23.txt` - intercepted ciphertext, `plaintext_v23.txt` - recovered message
- `report.tex` / `report.pdf` - the report (in Romanian)

## Lab 3 - Playfair (variant 23)

Variant 23 is odd, so the assigned task is 3.1 (Playfair). The Romanian alphabet
has 31 letters; the 5 x 6 square uses 30, with Q mapped to K as explained in the report.

    cd lab3
    python3 playfair.py                  # interactive encryption/decryption
    python3 -m unittest -v test_playfair.py
    pdflatex report.tex                  # run twice for the contents page

- `playfair.py` - cipher and console interface
- `test_playfair.py` - rule, round-trip, Unicode and input checks
- `report.tex` / `report.pdf` - Romanian report
