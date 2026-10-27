import unittest

from playfair import (ALPHABET, InputError, clean, decrypt, encrypt,
                      key_square, prepare, transform, valid_ciphertext)


KEY = "SECURITATE"


class PlayfairTests(unittest.TestCase):
    def test_square_has_each_letter_once(self):
        square = key_square(KEY)
        self.assertEqual(len(square), 30)
        self.assertEqual(set(square), set(ALPHABET))
        self.assertEqual(square[:7], "SECURIT")

    def test_three_rules_and_wraparound(self):
        square = key_square(KEY)
        for plain, cipher in (("SE", "EC"), ("ST", "TF"), ("SA", "ET"),
                              ("IS", "SE"), ("ȚS", "ST")):
            with self.subTest(pair=plain):
                self.assertEqual(transform(plain, square, +1), cipher)
                self.assertEqual(transform(cipher, square, -1), plain)

    def test_every_distinct_pair_is_invertible(self):
        square = key_square(KEY)
        for a in square:
            for b in square:
                if a != b:
                    pair = a + b
                    cipher = transform(pair, square, +1)
                    self.assertEqual(transform(cipher, square, -1), pair)

    def test_repeated_letters_and_odd_length(self):
        self.assertEqual(prepare("ANA ARE MERE"), "ANAXAREMEREX")
        self.assertEqual(prepare("XXXX"), "XZXZXZXZ")
        self.assertEqual(prepare("AXA"), "AXAX")

    def test_round_trip_is_prepared_text(self):
        for message in ("ȘTIINȚĂ ȘI CERCETARE", "CRIPTOGRAFIE", "XXXX", "QATAR"):
            with self.subTest(message=message):
                self.assertEqual(decrypt(encrypt(message, KEY), KEY), prepare(message))

    def test_cedilla_and_combining_marks(self):
        self.assertEqual(clean("ştiinţă"), "ȘTIINȚĂ")
        self.assertEqual(clean("a\u0306"), "Ă")
        self.assertEqual(clean("Q"), "K")

    def test_bad_input(self):
        for value in ("", "ABC!", "A\tB", "АBC", "A1B"):
            with self.subTest(value=value), self.assertRaises(InputError):
                clean(value)
        with self.assertRaises(InputError):
            key_square("SCURT")
        for value in ("ABC", "AA", "AB CD"):
            with self.subTest(ciphertext=value), self.assertRaises(InputError):
                valid_ciphertext(value)


if __name__ == "__main__":
    unittest.main()
