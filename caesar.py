# Lab 1 - Caesar cipher over the Romanian alphabet (one key and two keys)

ROMANIAN = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "Ș", "T", "Ț", "U", "V", "W", "X", "Y", "Z"]

# cedilla forms (ş, ţ) show up on some keyboards, treat them as ș, ț
CEDILLA = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}

MIN_KEYWORD = 7


class InvalidInput(ValueError):
    pass


def normalize(text, alphabet=ROMANIAN):
    out = ""
    for ch in text.replace(" ", ""):
        ch = CEDILLA.get(ch, ch).upper()
        if ch not in alphabet:
            raise InvalidInput(f"Invalid character '{ch}'. Allowed: letters of the "
                               f"Romanian alphabet (A-Z, Ă, Â, Î, Ș, Ț) and spaces.")
        out += ch
    return out


def validate_shift(raw, n=len(ROMANIAN)):
    try:
        k = int(raw)
    except ValueError:
        k = None
    if k is None or not 1 <= k < n:
        raise InvalidInput(f"Invalid key '{raw.strip()}'. The key must be an integer "
                           f"between 1 and {n - 1} inclusive.")
    return k


def validate_keyword(raw, alphabet=ROMANIAN):
    raw = raw.strip()
    if " " in raw:
        raise InvalidInput("Invalid keyword. It must be a single word without spaces.")
    word = normalize(raw, alphabet)
    if len(word) < MIN_KEYWORD:
        raise InvalidInput(f"Keyword too short ({len(word)} letters). "
                           f"It needs at least {MIN_KEYWORD}.")
    return word


def permuted_alphabet(keyword, alphabet=ROMANIAN):
    # dict keeps insertion order, so this drops repeats and keeps the first occurrence
    return list(dict.fromkeys(keyword + "".join(alphabet)))


def shift(text, k, alphabet):
    n = len(alphabet)
    pos = {ch: i for i, ch in enumerate(alphabet)}
    # python's % never returns a negative number, so (x - k) mod n is safe as is
    return "".join(alphabet[(pos[ch] + k) % n] for ch in text)


def encrypt(text, k, alphabet=ROMANIAN):
    return shift(text, k, alphabet)


def decrypt(text, k, alphabet=ROMANIAN):
    return shift(text, -k, alphabet)


def encrypt2(text, k, keyword, alphabet=ROMANIAN):
    return encrypt(text, k, permuted_alphabet(keyword, alphabet))


def decrypt2(text, k, keyword, alphabet=ROMANIAN):
    return decrypt(text, k, permuted_alphabet(keyword, alphabet))


def ask(prompt, validate):
    while True:
        try:
            return validate(input(prompt))
        except InvalidInput as err:
            print(f"  [!] {err}")


def operation(raw):
    raw = raw.strip().lower()
    if raw not in ("e", "d"):
        raise InvalidInput(f"Invalid operation '{raw}'. Type e to encrypt or d to decrypt.")
    return raw


def run(two_keys):
    op = ask("Operation - (e)ncrypt or (d)ecrypt: ", operation)
    k = ask("Key 1 (shift, 1-30): ", validate_shift)
    alphabet = ROMANIAN
    if two_keys:
        keyword = ask(f"Key 2 (keyword, min {MIN_KEYWORD} letters): ", validate_keyword)
        alphabet = permuted_alphabet(keyword)
    text = ask("Enter the " + ("plaintext: " if op == "e" else "ciphertext: "), normalize)

    if two_keys:
        print("Permuted alphabet:", " ".join(alphabet))
    print("Normalized input :", text)
    if op == "e":
        print("Ciphertext       :", encrypt(text, k, alphabet))
    else:
        print("Plaintext        :", decrypt(text, k, alphabet))


def main():
    while True:
        print("\n=== Caesar cipher - Romanian alphabet (n = 31) ===")
        print("1. Caesar cipher (one key)")
        print("2. Caesar cipher with a keyword permutation (two keys)")
        print("0. Exit")
        choice = input("Choice: ").strip()
        if choice == "0":
            break
        if choice in ("1", "2"):
            run(two_keys=choice == "2")
        else:
            print("  [!] Invalid choice. Type 1, 2 or 0.")


if __name__ == "__main__":
    main()
