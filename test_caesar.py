"""Checks the implementation against the worked examples of the assignment (English alphabet)."""
import string
import unittest

import caesar as c

EN = list(string.ascii_uppercase)


class PdfExamples(unittest.TestCase):
    def test_caesar_k3(self):
        self.assertEqual(c.encrypt("CIFRULCEZAR", 3, EN), "FLIUXOFHCDU")
        self.assertEqual(c.decrypt("FLIUXOFHCDU", 3, EN), "CIFRULCEZAR")

    def test_brute_force_example(self):
        self.assertEqual(c.encrypt("BRUTEFORCEATTACK", 17, EN), "SILKVWFITVRKKRTB")
        self.assertEqual(c.decrypt("SILKVWFITVRKKRTB", 17, EN), "BRUTEFORCEATTACK")
        self.assertEqual(c.decrypt("SILKVWFITVRKKRTB", 1, EN), "RHKJUVEHSUQJJQSA")

    def test_permuted_alphabet(self):
        self.assertEqual("".join(c.permuted_alphabet("CRYPTOGRAPHY", EN)),
                         "CRYPTOGAHBDEFIJKLMNQSUVWXZ")

    def test_two_keys(self):
        self.assertEqual(c.encrypt2("CIFRULCEZAR", 3, "CRYPTOGRAPHY", EN), "PLKTXQPJYDT")
        self.assertEqual(c.decrypt2("PLKTXQPJYDT", 3, "CRYPTOGRAPHY", EN), "CIFRULCEZAR")


class Romanian(unittest.TestCase):
    def test_alphabet_size_and_codes(self):
        self.assertEqual(len(c.ROMANIAN), 31)
        self.assertEqual(c.ROMANIAN.index("Z"), 30)
        self.assertEqual(c.ROMANIAN.index("Ă"), 1)
        self.assertEqual(c.ROMANIAN.index("Ț"), 24)

    def test_roundtrip_every_key(self):
        text = "ŞTIINŢĂ ŞI ÎNVĂŢĂTURĂ ZAZ"
        norm = c.normalize(text)
        self.assertEqual(norm, "ȘTIINȚĂȘIÎNVĂȚĂTURĂZAZ")
        for k in range(1, 31):
            self.assertEqual(c.decrypt(c.encrypt(norm, k), k), norm)
            self.assertEqual(c.decrypt2(c.encrypt2(norm, k, "CRIPTOGRAFIE"), k, "CRIPTOGRAFIE"), norm)

    def test_wraparound(self):
        self.assertEqual(c.encrypt("Z", 1), "A")
        self.assertEqual(c.decrypt("A", 1), "Z")
        self.assertEqual(c.encrypt("Ă", 30), "A")

    def test_permuted_has_all_letters(self):
        p = c.permuted_alphabet(c.validate_keyword("Ștefănescu"))
        self.assertEqual(sorted(p), sorted(c.ROMANIAN))

    def test_validation(self):
        for bad in ("0", "31", "-3", "abc", "", "2.5"):
            with self.assertRaises(c.InvalidInput):
                c.validate_shift(bad)
        for bad in ("Hello1", "ab", "cripto", "două cuvinte", "şaizeci!"):
            with self.assertRaises(c.InvalidInput):
                c.validate_keyword(bad)
        with self.assertRaises(c.InvalidInput):
            c.normalize("hello, world")
        self.assertEqual(c.normalize("a ă â î ş ţ"), "AĂÂÎȘȚ")


if __name__ == "__main__":
    unittest.main()
