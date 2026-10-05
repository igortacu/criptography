"""Replays scripted sessions through caesar.main() with the typed input echoed (for the report)."""
import builtins, contextlib, io, sys
sys.path.insert(0, "..")
import caesar

SESSIONS = {
    "task1_ok": ["1", "e", "3", "cifrul cezar", "1", "d", "3", "FKITXOFHÂBT", "0"],
    "task1_invalid": ["1", "e", "0", "31", "abc", "5", "hello, world", "Ştiinţă şi artă", "0"],
    "task2_ok": ["2", "e", "3", "criptografie", "Cifrul Cezar", "2", "d", "3", "criptografie", "TODO", "0"],
    "task2_invalid": ["2", "e", "3", "cripto", "cripto grafie", "cripto9rafie", "criptografie", "ab", "0"],
}

def replay(inputs):
    it = iter(inputs)
    def fake(prompt=""):
        v = next(it); print(prompt + v); return v
    builtins.input = fake
    caesar.main()

if __name__ == "__main__":
    # task2_ok: fill in the real ciphertext produced by the first run
    ct = caesar.encrypt2(caesar.normalize("Cifrul Cezar"), 3, "CRIPTOGRAFIE")
    SESSIONS["task2_ok"][-2] = ct
    for name, inputs in SESSIONS.items():
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            replay(inputs)
        open(f"{name}.txt", "w").write(buf.getvalue().replace("\n\n=== ", "\n=== ").lstrip())
        print(f"--- {name}\n{buf.getvalue()}")
