"""Task 2/4 for PG(2,9).

1. Parse and sanity-check the published census file; independently enumerate
   all caps of size <= 4 to check the low-size census rows and maximality.
2. Check the 8 published point permutations are incidence automorphisms.
3. Enumerate the complete 7-arc orbit of the known maximal 7-arc
   [33,39,57,70,74,80,89] under those automorphisms.  The orbit has
   2,021,760 elements, all 7-caps and (by automorphism) all maximal.
4. Hash all C(7,6)=7 six-subsets of every orbit member and check distinctness.
5. Compare with the census count and K1333's G=2 count 14,152,320.
"""

from __future__ import annotations

import json
import random
import time
from itertools import combinations

import g2common as C

PG = C.BOARDS["PG(2,9)"]
CENSUS = C.REPO / "research/experiments/pg2q9-cap-game-20261125/output/census_pg2q9.txt"
GENS = C.REPO / "research/experiments/pg2q9-cap-game-20261125/output/gens.txt"
SEED = [33, 39, 57, 70, 74, 80, 89]
CLAIM_MAX7 = 2021760
CLAIM_6SUBSETS = 14152320


def parse_census(path):
    head = {}
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "N":
            head = {parts[i]: int(parts[i + 1]) for i in range(0, len(parts), 2)}
        elif parts[0] == "SIZE":
            rows[int(parts[1])] = {"total": int(parts[2]), "maximal": int(parts[3])}
    return head, rows


def census_checks(head, rows, n, b):
    out = {}
    totals = {k: v["total"] for k, v in rows.items()}
    maxs = {k: v["maximal"] for k, v in rows.items()}
    out["header"] = head
    out["n_matches_board"] = head.get("N") == n
    out["b_matches_board"] = head.get("B") == b
    out["safe_matches_size_sum"] = head.get("SAFE") == sum(totals.values())
    out["safe_value"] = head.get("SAFE")
    out["size_sum"] = sum(totals.values())
    out["maximal_sum"] = sum(maxs.values())
    out["size0_is_1"] = totals.get(0) == 1
    out["size1_is_n"] = totals.get(1) == n
    out["size2_is_C_n_2"] = totals.get(2) == n * (n - 1) // 2
    out["no_maximal_below_6"] = all(maxs.get(k, 0) == 0 for k in range(0, 6))
    out["size9_equals_10_times_size10"] = totals.get(9) == 10 * totals.get(10, 0)
    out["size8_nonmax_equals_C10_8_times_ovals"] = (
        totals.get(8, 0) - maxs.get(8, 0) == 45 * totals.get(10, 0)
    )
    out["maximal_total"] = 707616 + 2021760 + 5307120 + 58968
    out["maximal_total_matches"] = out["maximal_total"] == out["maximal_sum"]
    out["claims"] = {
        "maximal7": maxs.get(7),
        "claim_max7": CLAIM_MAX7,
        "match": maxs.get(7) == CLAIM_MAX7,
    }
    return out, totals, maxs


def main():
    t0 = time.time()
    n, blocks = C.load_board(PG)
    head, rows = parse_census(CENSUS)
    census, totals_census, maxs_census = census_checks(head, rows, n, len(blocks))
    print("census header", head)
    print("census checks", {k: v for k, v in census.items() if k != "header"})

    # ---- independent low-size census (sizes 0..4) --------------------------
    low = C.enumerate_all_caps(n, blocks, size_limit=4)
    low_counts = {s: len(v) for s, v in enumerate(low) if v}
    pair_line = {}
    for B in blocks:
        lm = sum(1 << p for p in B)
        for i, p in enumerate(B):
            for q in B[i + 1:]:
                pair_line[(p, q) if p < q else (q, p)] = lm

    def addable_fast(mask):
        pts = C.bits(mask)
        sat = 0
        for i, p in enumerate(pts):
            for q in pts[i + 1:]:
                sat |= pair_line[(p, q)]
        return ((1 << n) - 1) & ~mask & ~sat

    low_maximal = {}
    for s in range(0, 5):
        low_maximal[s] = sum(1 for m in low[s] if addable_fast(m) == 0)
    print("low census", low_counts, "maximal", low_maximal,
          f"({time.time()-t0:.1f}s)", flush=True)
    low_ok = all(low_counts.get(s, 0) == totals_census.get(s) for s in range(5))
    low_max_ok = all(low_maximal[s] == maxs_census.get(s, 0) for s in range(5))
    del low

    # ---- generators --------------------------------------------------------
    lineset = {frozenset(B) for B in blocks}
    perms = []
    gen_bad = []
    for gi, line in enumerate(GENS.read_text(encoding="utf-8").splitlines()):
        perm = tuple(map(int, line.split()))
        ok_perm = len(perm) == n and sorted(perm) == list(range(n))
        bad = 0 if ok_perm else -1
        if ok_perm:
            for B in blocks:
                if frozenset(perm[p] for p in B) not in lineset:
                    bad += 1
        gen_bad.append({"gen": gi, "permutation": ok_perm, "bad_lines": bad})
        if bad == 0:
            perms.append(perm)
    gen_ok = len(perms) == len(gen_bad)
    print("generators ok", gen_ok, gen_bad, flush=True)

    # ---- cap / maximal check of the seed ----------------------------------
    seed_mask = C.mask_of(SEED)
    lmasks = C.line_masks(blocks)
    seed_cap = all((seed_mask & lm).bit_count() <= 2 for lm in lmasks)
    seed_max = C.addable_mask(seed_mask, n, lmasks) == 0
    print("seed cap/maximal", seed_cap, seed_max, flush=True)

    # ---- orbit BFS ---------------------------------------------------------
    def apply(mask, perm):
        m = 0
        while mask:
            low = mask & -mask
            m |= 1 << perm[low.bit_length() - 1]
            mask ^= low
        return m

    seen = {seed_mask}
    arcs = [seed_mask]
    frontier = [seed_mask]
    levels = []
    while frontier:
        nxt = []
        for mask in frontier:
            for perm in perms:
                m = apply(mask, perm)
                if m not in seen:
                    seen.add(m)
                    arcs.append(m)
                    nxt.append(m)
        frontier = nxt
        levels.append(len(arcs))
        print("orbit", len(arcs), f"{time.time()-t0:.1f}s", flush=True)
    orbit_size = len(arcs)
    print("orbit size", orbit_size, "claim", CLAIM_MAX7,
          "match", orbit_size == CLAIM_MAX7, f"({time.time()-t0:.1f}s)", flush=True)

    # every generator image of a maximal 7-arc is again one; check a sample
    rng = random.Random(20261126)
    sample = rng.sample(arcs, 1000)
    sample_ok = all(a.bit_count() == 7 and addable_fast(a) == 0 for a in sample)
    print("sample 1000 arcs maximal:", sample_ok)

    # save the arcs compactly (7 bytes per arc, sorted points)
    arc_path = C.OUT / "pg_max7_arcs.bin"
    with arc_path.open("wb") as fh:
        for m in arcs:
            fh.write(bytes(C.bits(m)))
    print("wrote", arc_path, arc_path.stat().st_size, "bytes", flush=True)

    # ---- six-subsets -------------------------------------------------------
    del seen
    t1 = time.time()
    subs = set()
    dup = 0
    for m in arcs:
        pts = C.bits(m)
        for drop in pts:
            x = m ^ (1 << drop)
            if x in subs:
                dup += 1
            subs.add(x)
    six = len(subs)
    print("6-subsets", six, "duplicates", dup,
          "expected", 7 * orbit_size, f"({time.time()-t1:.1f}s)", flush=True)

    six_ok = (
        six == 7 * orbit_size
        and six == CLAIM_6SUBSETS
        and dup == 0
        and six <= totals_census[6]
    )
    # random sample: every sampled six-subset is a cap and has its unique
    # 7-arc parent in the orbit
    sample_arcs = rng.sample(arcs, 200)
    sample6 = []
    for a in sample_arcs:
        pts = C.bits(a)
        sample6.append(a ^ (1 << pts[rng.randrange(7)]))
    sample6_caps = all(
        all((x & lm).bit_count() <= 2 for lm in lmasks) for x in sample6
    )
    result = {
        "census": census,
        "census_rows": {str(k): v for k, v in rows.items()},
        "low_size_independent": {
            "counts": low_counts,
            "maximal": low_maximal,
            "counts_match": low_ok,
            "maximal_match": low_max_ok,
        },
        "generators": {"count": len(perms), "all_ok": gen_ok, "records": gen_bad},
        "seed": {"arc": SEED, "mask": seed_mask, "is_cap": seed_cap,
                 "is_maximal": seed_max},
        "orbit": {
            "size": orbit_size,
            "claim": CLAIM_MAX7,
            "match": orbit_size == CLAIM_MAX7,
            "bfs_levels": levels,
            "sample_1000_all_maximal_7caps": sample_ok,
            "arcs_file": str(arc_path.relative_to(C.HERE)).replace("\\", "/"),
        },
        "six_subsets": {
            "count": six,
            "generated_with_multiplicity": 7 * orbit_size,
            "duplicates": dup,
            "claim": CLAIM_6SUBSETS,
            "match": six_ok,
            "total_6caps_census": totals_census[6],
            "fraction_of_6caps": round(six / totals_census[6], 6),
            "sample_200_caps": sample6_caps,
        },
        "seconds": round(time.time() - t0, 1),
    }
    # cross-check of the K1333 arithmetic: 52,009,776 - 14,152,320
    result["k1333_arithmetic"] = {
        "total6": totals_census[6],
        "g2_if_claim": CLAIM_6SUBSETS,
        "g0_implied": totals_census[6] - CLAIM_6SUBSETS,
        "published_g0": 37857456,
        "match": totals_census[6] - CLAIM_6SUBSETS == 37857456,
    }
    (C.OUT / "task2_pg.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1)[:3000])
    print("total", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
