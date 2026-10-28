"""Frequency-analysis attack on variant 23, done as a chain of guesses (each one justified)."""
from freq import apply, ABC

text = open("cipher_v23.txt", encoding="utf-8").read()

# (cipher -> plain pairs, why we believe them)
STEPS = [
    ("V=e, W=t",           "V și W sunt cele mai frecvente litere, ca E și T în engleză."),
    ("Q=h",                "trigrama cea mai frecventă, WQV, este aproape sigur THE, deci Q = h."),
    ("T=a, G=n, O=d",      "TGO (trigramă frecventă, cuvânt de 3 litere) este AND."),
    ("N=o, C=f",           "NC este cuvântul de două litere OF (N a mai apărut în WN = to)."),
    ("X=i",                "XG este cuvântul IN (G = n deja cunoscut)."),
    ("R=w, P=s",           "RTP = WAS, RQN = WHO, RVIV = WERE, după ce T, Q, V sunt cunoscute."),
    ("I=r",                "CNI = FOR (I este ultima literă a cuvântului)."),
    ("J=g",                "trigrama XGJ = ING."),
    ("H=c, F=y, U=p, S=l", "HIFUWNSNJF = CRYPTOLOGY, găsit după șablonul c-r-y-p-t-o-l-o-g-y."),
    ("Z=m",                "ZTG = MAN."),
    ("A=b, D=u",           "Athng = BACON, ndwsvw = OUTLET."),
    ("L=k, M=z",           "Pqtlvpuvtiv = SHAKESPEARE, Vsxmtavwq = ELIZABETH."),
    ("K=v, B=q, Y=x, E=j", "Kxijxg = VIRGIN, bdxhl = QUICK, „4 Y 7” = 4 x 7, Enqg = JOHN."),
]

if __name__ == "__main__":
    mapping = {}
    for step, why in STEPS:
        for pair in step.split(", "):
            c, p = pair.split("=")
            mapping[c.upper()] = p
        print(f"--- {step}   ({why})")
        print(apply(text, mapping).splitlines()[1][:95], "\n")
    print("=== full plaintext ===")
    print(apply(text, mapping).lower())
    inv = {p: c for c, p in mapping.items()}
    print("\nplain  :", " ".join(ABC.lower()))
    print("cipher :", " ".join(inv.get(p, "?") for p in ABC.lower()))
