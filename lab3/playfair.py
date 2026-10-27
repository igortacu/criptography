"""Playfair pentru varianta 23 (alfabet românesc, matrice 5 x 6)."""

import unicodedata


ROMANIAN = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
# În 30 de celule nu încap 31 de litere. Q este rar în română; îl citim ca K.
ALPHABET = ROMANIAN.replace("Q", "")
ROWS, COLS = 5, 6
FILLERS = ("X", "Z")
CEDILLA = str.maketrans({"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"})


class InputError(ValueError):
    """Datele introduse nu respectă formatul cerut."""


def clean(raw: str, *, spaces: bool = False) -> str:
    """Majuscule, diacritice canonice și Q->K; spațiile sunt opționale."""
    raw = unicodedata.normalize("NFC", raw).translate(CEDILLA)
    result = []
    for ch in raw:
        if ch == " " and spaces:
            continue
        upper = ch.upper()
        if upper not in ROMANIAN or len(upper) != 1:
            allowed = "A-Z, a-z, Ă/ă, Â/â, Î/î, Ș/ș, Ț/ț"
            if spaces:
                allowed += " și spații"
            raise InputError(f"Caracter nepermis {ch!r}. Folosiți doar {allowed}.")
        result.append("K" if upper == "Q" else upper)
    if not result:
        raise InputError("Textul nu poate fi gol.")
    return "".join(result)


def key_square(key: str) -> str:
    """Literele unice ale cheii, apoi restul alfabetului de 30 de litere."""
    word = clean(key)
    if len(word) < 7:
        raise InputError("Cheia trebuie să aibă cel puțin 7 litere.")
    return "".join(dict.fromkeys(word + ALPHABET))


def prepare(plaintext: str) -> str:
    """Formează digrame fără litere egale; completează ultima digramă."""
    letters = clean(plaintext, spaces=True)
    pairs = []
    i = 0
    while i < len(letters):
        first = letters[i]
        if i + 1 == len(letters) or letters[i + 1] == first:
            second = FILLERS[0] if first != FILLERS[0] else FILLERS[1]
            i += 1
        else:
            second = letters[i + 1]
            i += 2
        pairs.append(first + second)
    return "".join(pairs)


def transform(pairs: str, square: str, direction: int) -> str:
    """Aplică regulile Playfair; direction este +1 sau -1."""
    positions = {letter: divmod(index, COLS) for index, letter in enumerate(square)}
    output = []
    for i in range(0, len(pairs), 2):
        a, b = pairs[i:i + 2]
        ra, ca = positions[a]
        rb, cb = positions[b]
        if ra == rb:
            output.extend((square[ra * COLS + (ca + direction) % COLS],
                           square[rb * COLS + (cb + direction) % COLS]))
        elif ca == cb:
            output.extend((square[((ra + direction) % ROWS) * COLS + ca],
                           square[((rb + direction) % ROWS) * COLS + cb]))
        else:
            output.extend((square[ra * COLS + cb], square[rb * COLS + ca]))
    return "".join(output)


def encrypt(plaintext: str, key: str) -> str:
    return transform(prepare(plaintext), key_square(key), +1)


def decrypt(ciphertext: str, key: str) -> str:
    square = key_square(key)
    return transform(valid_ciphertext(ciphertext), square, -1)


def grouped(text: str) -> str:
    return " ".join(text[i:i + 2] for i in range(0, len(text), 2))


def ask(prompt: str, parse):
    while True:
        try:
            return parse(input(prompt))
        except InputError as exc:
            print(f"Eroare: {exc}")


def main() -> None:
    print("Playfair românesc | varianta 23 | 5 x 6 | Q se citește ca K")
    while True:
        choice = input("Operația [c]riptare / [d]ecriptare / [i]eșire: ").lower()
        if choice == "i":
            return
        if choice not in {"c", "d"}:
            print("Alegeți c, d sau i.")
            continue
        key = ask("Cheia (minimum 7 litere): ", key_square)
        print("Matricea:")
        for row in range(ROWS):
            print("  " + " ".join(key[row * COLS:(row + 1) * COLS]))
        if choice == "c":
            message = ask("Mesajul: ", lambda value: prepare(value))
            print("Digrame pregătite:", grouped(message))
            print("Criptograma:", transform(message, key, +1))
        else:
            message = ask("Criptograma: ", valid_ciphertext)
            print("Mesajul pregătit:", grouped(transform(message, key, -1)))
            print("Restabiliți manual spațiile, Q și eventualele litere de umplere.")


def valid_ciphertext(value: str) -> str:
    letters = clean(value)
    if len(letters) % 2:
        raise InputError("Criptograma trebuie să conțină un număr par de litere.")
    if any(letters[i] == letters[i + 1] for i in range(0, len(letters), 2)):
        raise InputError("Criptograma nu poate avea două litere identice în aceeași digramă.")
    return letters


if __name__ == "__main__":
    main()
