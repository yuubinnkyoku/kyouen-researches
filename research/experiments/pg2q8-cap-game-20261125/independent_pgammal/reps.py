"""Representatives for all claimed PGL(3,8) cap orbits, validated against the
board.  Expected sizes are the K1327 values that K1330 uses."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import conic as Q

# conic through C6 = {2,3,10,16,18,21}
CONIC_CO, CONIC9 = Q.conic_of_cap([2, 3, 10, 16, 18, 21])
assert CONIC9 == [2, 3, 10, 16, 18, 21, 29, 47, 48], CONIC9

C6 = [2, 3, 10, 16, 18, 21]            # conic 6-cap (given in the claim)
D6 = [1, 10, 12, 59, 62, 65]           # non-maximal non-conic 6-cap (claim)
PHI_C6 = [2, 5, 10, 12, 18, 23]
PHI_D6 = [1, 10, 14, 29, 32, 33]

# maximal 6-caps: K1329 representatives A, B, C
MAXA = [10, 47, 49, 55, 61, 64]
MAXB = [17, 27, 30, 44, 52, 70]
MAXC = [8, 48, 50, 51, 58, 61]

NONCONIC7 = [12, 16, 18, 22, 54, 66, 69]       # K1327
NONCONIC8 = [12, 16, 18, 22, 40, 54, 66, 69]   # K1327
NONCONIC9 = [2, 3, 10, 12, 21, 45, 47, 50, 52]  # K1326


def addable_points(pts):
    s = set(pts)
    out = []
    for p in range(C.N):
        if p in s:
            continue
        if C.is_cap(list(pts) + [p]):
            out.append(p)
    return out


def phi_set(pts):
    return sorted(C.PHI[p] for p in pts)


def build_hyperoval():
    """Conic9 plus its nucleus: scan for points extendable to a 10-cap."""
    extra = addable_points(CONIC9)
    assert len(extra) == 1, extra
    hyp = sorted(CONIC9 + extra)
    assert C.is_cap(hyp)
    assert addable_points(hyp) == []
    return hyp, extra[0]


HYPEROVAL, NUCLEUS = build_hyperoval()

REPS = [
    # (k, label, points, expected PGL orbit size, expected PGammaL class)
    (1, "k1", [CONIC9[0]], 73, "single"),
    (2, "k2", CONIC9[:2], 2628, "single"),
    (3, "k3", CONIC9[:3], 56064, "single"),
    (4, "k4", CONIC9[:4], 686784, "single"),
    (5, "k5", CONIC9[:5], 4120704, "single"),
    (6, "k6-conic", C6, 2747136, "single"),
    (6, "k6-nonmax-nonconic", D6, 4120704, "single"),
    (6, "k6-max-A", MAXA, 686784, "maximal-triple"),
    (6, "k6-max-B", MAXB, 686784, "maximal-triple"),
    (6, "k6-max-C", MAXC, 686784, "maximal-triple"),
    (7, "k7-conic", CONIC9[:7], 1177344, "single"),
    (7, "k7-nonconic", NONCONIC7, 2747136, "single"),
    (8, "k8-conic", CONIC9[:8], 294336, "single"),
    (8, "k8-nonconic", NONCONIC8, 1177344, "single"),
    (9, "k9-conic", CONIC9[:9], 32704, "single"),
    (9, "k9-nonconic", NONCONIC9, 294336, "single"),
    (10, "k10", HYPEROVAL, 32704, "single"),
]


def validate():
    print("conic through C6:", CONIC9)
    print("nucleus of the conic:", NUCLEUS, "-> hyperoval size", len(HYPEROVAL))
    assert C.is_cap(HYPEROVAL) and addable_points(HYPEROVAL) == []
    for k, label, pts, exp, cls in REPS:
        assert len(pts) == k and len(set(pts)) == k, label
        assert C.is_cap(pts), label
        conic_flag = Q.is_conic_set(pts)
        add = addable_points(pts)
        maximal = (add == [])
        if label.startswith("k6-conic") or label in (
                "k7-conic", "k8-conic", "k9-conic"):
            assert conic_flag, (label, "should be conic")
        if "nonconic" in label:
            assert not conic_flag, (label, "should be non-conic")
        if label.startswith("k6-max-"):
            assert maximal, (label, "should be maximal")
        if label in ("k6-conic", "k6-nonmax-nonconic"):
            assert not maximal, (label, "should be non-maximal")
        print(f"{label:24s} k={k:2d} conic={str(conic_flag):5s} "
              f"maximal={str(maximal):5s} addable={len(add):2d} "
              f"expected_orbit={exp}")
    # Frobenius images stated in the claim
    assert phi_set(C6) == PHI_C6, phi_set(C6)
    assert phi_set(D6) == PHI_D6, phi_set(D6)
    print("phi(C6) =", phi_set(C6))
    print("phi(D6) =", phi_set(D6))
    # K1329 stated images
    print("phi(A)   =", phi_set(MAXA))
    print("phi^2(A) =", sorted(C.PHI[C.PHI[p]] for p in MAXA))
    assert phi_set(MAXA) == [10, 28, 31, 59, 65, 67], phi_set(MAXA)
    assert sorted(C.PHI[C.PHI[p]] for p in MAXA) == [10, 29, 33, 37, 43, 46]
    print("representatives validated")


if __name__ == "__main__":
    validate()
