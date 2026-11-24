"""Task 2: independent enumeration of the 3-caps and 4-caps of the board.

No reference to the experiment's own census: every subset is tested against the
line table built from scratch in core.py.
"""
import json
import time

import core

N = 91
FB = [[0] * N for _ in range(N)]     # points collinear with the pair {a,b}
for a in range(N):
    for b in range(N):
        if a != b:
            FB[a][b] = core.LMASK[a][b] & ~(1 << a) & ~(1 << b)
ALL = core.ALL_POINTS


def enumerate_caps3():
    caps3 = []
    for a in range(N - 2):
        fb_ab = FB[a]
        for b in range(a + 1, N - 1):
            fab = fb_ab[b]
            for c in range(b + 1, N):
                if (fab >> c) & 1:
                    continue
                caps3.append((a, b, c))
    return caps3


def enumerate_caps4(caps3=None):
    if caps3 is None:
        caps3 = enumerate_caps3()
    caps4 = []
    for (a, b, c) in caps3:
        forb = FB[a][b] | FB[a][c] | FB[b][c]
        allowed = ALL & ~forb & ~((1 << (c + 1)) - 1)
        while allowed:
            bit = allowed & -allowed
            allowed ^= bit
            d = bit.bit_length() - 1
            caps4.append((a, b, c, d))
    return caps4


def main():
    t0 = time.time()
    caps3 = enumerate_caps3()
    t1 = time.time()
    caps4 = enumerate_caps4(caps3)
    t2 = time.time()

    n3, n4 = len(caps3), len(caps4)
    total_triples = N * (N - 1) * (N - 2) // 6
    collinear_triples = 91 * (10 * 9 * 8 // 6)
    out = {
        "n_caps3": n3,
        "n_caps4": n4,
        "expected_caps3_from_counting": total_triples - collinear_triples,
        "caps3_matches_identity": n3 == total_triples - collinear_triples,
        "n_3subsets": total_triples,
        "n_collinear_triples": collinear_triples,
        "all_caps3_are_caps": all(core.is_cap(t) for t in caps3),
        "all_caps4_are_caps": all(core.is_cap(t) for t in caps4),
        "distinct_caps3": len(set(caps3)) == n3,
        "distinct_caps4": len(set(caps4)) == n4,
        "covers_all_3subsets": n3 + collinear_triples == total_triples,
        "claim_caps3_110565": n3 == 110565,
        "claim_caps4_1769040": n4 == 1769040,
        "seconds_enum_caps3": round(t1 - t0, 1),
        "seconds_enum_caps4": round(t2 - t1, 1),
    }
    print(json.dumps(out, indent=1))
    with open("out_task2.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("3-caps =", n3, " 4-caps =", n4)


if __name__ == "__main__":
    main()
