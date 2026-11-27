#!/usr/bin/env python3
"""Independent task 1: identify the board as W_24 = S(5,8,24) and recompute the
Golay span / dodecads from the 759 octads.

Input  : research/experiments/design-kyouen-witt-20261125/output/board_w24.txt  (read only)
Output : out/task1_board.json, out/dodecads.txt

Nothing outside independent_layer_map/ is written.
"""
import itertools
import json
import os
import random
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.abspath(os.path.join(
    HERE, "..", "..", "design-kyouen-witt-20261125", "output", "board_w24.txt"))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

N = 24


def read_board(path):
    with open(path) as f:
        tok = f.read().split()
    pos = 0
    n = int(tok[pos]); pos += 1
    nb = int(tok[pos]); pos += 1
    blocks = []
    for _ in range(nb):
        k = int(tok[pos]); pos += 1
        blk = tuple(int(t) for t in tok[pos:pos + k]); pos += k
        blocks.append(blk)
    if pos != len(tok):
        raise SystemExit("trailing tokens in board file")
    return n, nb, blocks


def mask_of(seq):
    m = 0
    for p in seq:
        m |= 1 << p
    return m


def bits(m):
    return [p for p in range(N) if (m >> p) & 1]


def rank_and_basis(words):
    piv = {}
    rank = 0
    basis = []
    for x in words:
        y = x
        while y:
            hb = y.bit_length() - 1
            if hb in piv:
                y ^= piv[hb]
            else:
                piv[hb] = y
                rank += 1
                basis.append(y)
                break
    return rank, basis


def main():
    res = {}
    n, nb, blocks = read_board(BOARD)
    bm = [mask_of(b) for b in blocks]

    # ---- basic format ----
    fmt_ok = True
    if n != N or nb != 759:
        fmt_ok = False
    if len(set(bm)) != nb:
        fmt_ok = False
    for b in blocks:
        if len(b) != 8 or len(set(b)) != 8 or min(b) < 0 or max(b) >= n:
            fmt_ok = False
        if list(b) != sorted(b):
            fmt_ok = False
    res["format_ok"] = fmt_ok
    res["n"] = n
    res["blocks"] = nb
    res["block_size"] = sorted(set(len(b) for b in blocks))
    res["block_size_hist"] = dict(Counter(len(b) for b in blocks))
    if not fmt_ok:
        print(json.dumps(res, indent=2))
        raise SystemExit("board format check FAILED")

    # ---- lambda_t for t = 0..5 : each t-subset in exactly lambda_t blocks ----
    lam = {}
    lam_detail = {}
    for t in range(0, 6):
        cnt = Counter()
        for b in blocks:
            for sub in itertools.combinations(b, t):
                cnt[mask_of(sub)] += 1
        expect_nsub = len(list(itertools.combinations(range(n), t)))
        mult = Counter(cnt.values())
        covered = len(cnt)
        lam[t] = sorted(set(cnt.values()))
        lam_detail[t] = {
            "t_subsets": expect_nsub,
            "covered": covered,
            "multiplicity_hist": dict(sorted(mult.items())),
            "incidences": sum(cnt.values()),
            "expected_incidences": nb * len(list(itertools.combinations(range(8), t))),
        }
        # every t-subset must appear, with one fixed multiplicity
        if covered != expect_nsub or len(lam[t]) != 1:
            raise SystemExit(f"lambda_{t} check FAILED: {lam_detail[t]}")
    res["lambda"] = lam
    res["lambda_detail"] = lam_detail

    # ---- pairwise block intersections ----
    inter = Counter()
    for i in range(nb):
        for j in range(i + 1, nb):
            inter[(bm[i] & bm[j]).bit_count()] += 1
    res["pair_intersections"] = dict(sorted(inter.items()))
    # sanity: sum of C(|A n B|,2) over pairs = lambda2 * C(24,2)... derived check
    lam2 = lam[2][0]
    if set(inter) - {0, 2, 4}:
        raise SystemExit(f"unexpected block intersection sizes: {res['pair_intersections']}")

    # ---- Golay span of the octads ----
    rank, basis = rank_and_basis(bm)
    res["golay_rank"] = rank
    if rank != 12:
        raise SystemExit(f"rank {rank} != 12")
    span = [0]
    for g in basis:
        span = span + [x ^ g for x in span]
    span_set = set(span)
    if len(span_set) != 1 << rank:
        raise SystemExit("span enumeration inconsistent")
    weight_hist = Counter(x.bit_count() for x in span_set)
    res["golay_span"] = len(span_set)
    res["weight_enumerator"] = {str(w): weight_hist[w] for w in sorted(weight_hist)}
    # self-orthogonal / doubly even / self-dual
    self_orth = all((x & y).bit_count() % 2 == 0 for x in span_set for y in span_set)
    res["self_orthogonal"] = bool(self_orth)
    res["doubly_even"] = all(w % 4 == 0 for w in weight_hist)
    res["weight8_equals_blocks"] = (set(x for x in span_set if x.bit_count() == 8) == set(bm))
    res["complements_closed"] = all(((~x) & ((1 << N) - 1)) in span_set for x in span_set)

    # ---- dodecads = weight-12 words ----
    dodecads = sorted(x for x in span_set if x.bit_count() == 12)
    res["dodecads"] = len(dodecads)
    dset = set(dodecads)
    res["dodecad_complements_are_dodecads"] = all(
        ((~d) & ((1 << N) - 1)) in dset for d in dodecads)

    # dodecad / octad intersection profiles
    prof_ok = True
    prof_hist = Counter()
    for d in dodecads:
        prof = Counter((d & b).bit_count() for b in bm)
        prof_hist[tuple(sorted(prof.items()))] += 1
        if any(t not in (2, 4, 6) for t in prof):
            prof_ok = False
    res["dodecad_octad_profiles"] = {"constant": len(prof_hist) == 1,
                                    "profile": {str(k): v for k, v in
                                                sorted(prof_hist.most_common(1)[0][0])},
                                    "ok_even_2_4_6": prof_ok}
    if not prof_ok or len(prof_hist) != 1:
        raise SystemExit("dodecad/octad profile check FAILED")

    # ---- dodecad k-subsets: counts, injectivity, safeness ----
    # Every block meets every dodecad in at most 6 points (checked above), so no
    # 8-point block can lie in a dodecad or in any of its subsets: all of them are
    # s=7 safe.  A direct block-containment scan is run on a sample for sanity.
    rnd = random.Random(20261128)
    res["dodecad_subsets"] = {}
    subsets_by_k = {}
    for k in (9, 10, 11, 12):
        allsub = set()
        for d in dodecads:
            dd = bits(d)
            for sub in itertools.combinations(dd, k):
                allsub.add(mask_of(sub))
        subsets_by_k[k] = allsub
        expected = len(dodecads) * len(list(itertools.combinations(range(12), k)))
        sample = rnd.sample(sorted(allsub), min(2000, len(allsub)))
        unsafe_sample = 0
        for s in sample:
            if any((b & s) == b for b in bm):
                unsafe_sample += 1
        res["dodecad_subsets"][k] = {
            "distinct": len(allsub),
            "expected": expected,
            "injective": len(allsub) == expected,
            "containing_a_block": 0,
            "containing_a_block_full_argument":
                "no block meets any dodecad in more than 6 points",
            "direct_scan_sample": len(sample),
            "direct_scan_sample_containing_a_block": unsafe_sample,
        }
        if len(allsub) != expected or unsafe_sample != 0:
            raise SystemExit(f"dodecad {k}-subset check FAILED")

    # ---- every octad meets every dodecad, and 12-caps count ----
    with open(os.path.join(OUT, "dodecads.txt"), "w") as f:
        f.write(f"{len(dodecads)}\n")
        for d in dodecads:
            f.write(" ".join(str(p) for p in bits(d)) + "\n")

    with open(os.path.join(OUT, "task1_board.json"), "w") as f:
        json.dump(res, f, indent=2)

    print("BOARD", n, nb, "blocks of size", res["block_size"], "format_ok", fmt_ok)
    print("lambda 0..5:", [lam[t][0] for t in range(6)])
    print("block intersections:", res["pair_intersections"])
    print("Golay rank", rank, "span", len(span_set), "weights", res["weight_enumerator"])
    print("self_orthogonal", self_orth, "doubly_even", res["doubly_even"],
          "weight8==blocks", res["weight8_equals_blocks"])
    print("dodecads", len(dodecads), "complement-closed", res["dodecad_complements_are_dodecads"])
    print("dodecad/octad profile:", res["dodecad_octad_profiles"])
    for k in (9, 10, 11, 12):
        print("  dodecad", k, "-subsets:", res["dodecad_subsets"][k])
    print("OK")


if __name__ == "__main__":
    main()
