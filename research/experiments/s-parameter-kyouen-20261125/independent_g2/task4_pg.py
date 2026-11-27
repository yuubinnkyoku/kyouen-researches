"""Task 4 (PG(2,9) part): published G=2 total, arithmetic, and a sample of
the K1333 six-cap classification (maximal-7 extension <=> G=2).

The exhaustive G=2 total 14,152,320 is K1333's value; this script checks the
published files and independently recomputes a sample of both classes.
"""

from __future__ import annotations

import json
import random
import time

import g2common as C

PG = C.BOARDS["PG(2,9)"]
SIXCAP_RESULTS = C.REPO / "research/experiments/pg2q9-sixcap-20261126/results.txt"


def main():
    t0 = time.time()
    n, blocks = C.load_board(PG)
    lmasks = C.line_masks(blocks)
    pair_line = {}
    for B in blocks:
        lm = sum(1 << p for p in B)
        for i, p in enumerate(B):
            for q in B[i + 1:]:
                pair_line[(p, q) if p < q else (q, p)] = lm

    def addable(mask):
        pts = C.bits(mask)
        sat = 0
        for i, p in enumerate(pts):
            for q in pts[i + 1:]:
                sat |= pair_line[(p, q)]
        return ((1 << n) - 1) & ~mask & ~sat

    def has_max7_child(mask):
        a = addable(mask)
        while a:
            b = a & -a
            a ^= b
            if addable(mask | b) == 0:
                return True
        return False

    def random_cap(k):
        while True:
            pts = rng.sample(range(n), k)
            mask = C.mask_of(pts)
            if all((mask & lm).bit_count() <= 2 for lm in lmasks):
                return mask

    rng = random.Random(424242)
    samples = {"with_max7": [], "without_max7": []}
    tries = 0
    while (len(samples["with_max7"]) < 10 or len(samples["without_max7"]) < 10) and tries < 20000:
        tries += 1
        X = random_cap(6)
        cls = "with_max7" if has_max7_child(X) else "without_max7"
        if len(samples[cls]) >= 10:
            continue
        upset = C.enumerate_upset(n, blocks, X)
        g, maximal, _, _ = C.grundy_all(n, blocks, upset)
        sizes = sorted(maximal)
        samples[cls].append({
            "X": C.bits(X),
            "addable": addable(X).bit_count(),
            "grundy": g[X],
            "maximal_extension_sizes": sizes,
            "maximal_extension_counts": dict(sorted(maximal.items())),
            "upset_positions": sum(len(v) for v in upset),
            "all_max_extensions_even": all(s % 2 == 0 for s in sizes),
            "has_7": 7 in maximal,
        })
        print(cls, len(samples[cls]), samples[cls][-1], flush=True)

    checks = {
        "with_max7_all_G2": all(r["grundy"] == 2 for r in samples["with_max7"]),
        "with_max7_all_have_7": all(r["has_7"] for r in samples["with_max7"]),
        "without_max7_all_G0": all(r["grundy"] == 0 for r in samples["without_max7"]),
        "without_max7_all_even": all(r["all_max_extensions_even"]
                                      for r in samples["without_max7"]),
        "without_max7_no_7": all(not r["has_7"] for r in samples["without_max7"]),
    }

    # published data
    six = {}
    for line in SIXCAP_RESULTS.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            lhs, rhs = line.split("=", 1)
            six[lhs.strip()] = rhs.strip()
        elif line.startswith("census reproduced"):
            six["census_reproduced"] = line
    task2 = json.loads((C.OUT / "task2_pg.json").read_text(encoding="utf-8"))
    published = {
        "sixcap_results": six,
        "our_six_subsets": task2["six_subsets"]["count"],
        "our_duplicates": task2["six_subsets"]["duplicates"],
        "our_orbit_size": task2["orbit"]["size"],
        "census_max7": task2["census"]["claims"]["maximal7"],
        "k1333_6cap_g2": 14152320,
        "k1333_6cap_g0": 37857456,
        "census_total6": task2["six_subsets"]["total_6caps_census"],
        "arithmetic_g0": task2["six_subsets"]["total_6caps_census"] - 14152320,
        "arithmetic_ok": task2["six_subsets"]["total_6caps_census"] - 14152320 == 37857456,
        "published_results_match_ours": (
            six.get("n") == "14152320 = 7 * 2021760"
            and six.get("distinct") == "14152320"
            and six.get("duplicates") == "0"
        ),
    }
    out = {
        "board": "PG(2,9)",
        "six_cap_sample": {
            "with_max7": samples["with_max7"],
            "without_max7": samples["without_max7"],
            "checks": checks,
        },
        "published": published,
        "seconds": round(time.time() - t0, 2),
    }
    (C.OUT / "task4_pg.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(checks, indent=1))
    print(json.dumps(published, indent=1))


if __name__ == "__main__":
    main()
