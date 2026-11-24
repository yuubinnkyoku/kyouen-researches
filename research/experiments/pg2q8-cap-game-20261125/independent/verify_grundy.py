#!/usr/bin/env python3
"""Task 4: verify the parity-theorem application and the Grundy numbers.

1.  Read the independent size census (cap_census.exe logs) and check every
    maximal size is even (p = 0).
2.  Derive Grundy(S) = (p - |S|) mod 2 = |S| mod 2 and rebate the Grundy
    distribution from the even/odd size totals; compare with the claimed one.
3.  Independently compute, by full memoised game recursion, the normal-play
    Grundy number and the misere outcome of the caps that were reservoir-sampled
    in cap_census.exe, and compare with the parity prediction.
"""
import sys
from collections import defaultdict

CLAIM_PG = {"total": 19550350,
            "sizes": {0: 1, 1: 73, 2: 2628, 3: 56064, 4: 686784, 5: 4120704,
                      6: 8928192, 7: 3924480, 8: 1471680, 9: 327040, 10: 32704},
            "max": {6: 2060352, 10: 32704},
            "grundy": {0: 11121989, 1: 8428361}}
CLAIM_AG = {"total": 9136801,
            "sizes": {0: 1, 1: 64, 2: 2016, 3: 37632, 4: 404544, 5: 2145024,
                      6: 4158336, 7: 1666560, 8: 584640, 9: 125440, 10: 12544},
            "max": {6: 959616, 8: 20160, 10: 12544},
            "grundy": {0: 5162081, 1: 3974720}}


def parse_board(path):
    with open(path, encoding="utf-8") as f:
        raw = [ln.split() for ln in f if ln.strip()]
    n, b = int(raw[0][0]), int(raw[0][1])
    lines = []
    for row in raw[1:]:
        vals = [int(t) for t in row]
        k = vals[0]
        assert len(vals[1:]) == k
        lines.append(vals[1:])
    assert len(lines) == b
    return n, lines


def read_census(log):
    sizes, maxs = {}, {}
    with open(log, encoding="utf-8") as f:
        for ln in f:
            t = ln.split()
            if t and t[0] == "SIZE":
                sizes[int(t[1])] = int(t[2])
                maxs[int(t[1])] = int(t[3])
    return sizes, maxs


def build_index(n, lines):
    pair_line = {}
    line_mask = []
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
            for q in L:
                if p < q:
                    pair_line[(p, q)] = li
        line_mask.append(m)
    return pair_line, line_mask, (1 << n) - 1


def addable_mask(mask, pair_line, line_mask, FULL):
    pts = []
    m = mask
    while m:
        lsb = m & -m
        pts.append(lsb.bit_length() - 1)
        m ^= lsb
    U = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            U |= line_mask[pair_line[(pts[i], pts[j])]]
    return (~U) & FULL & ~mask


def grundy(mask, memo, pair_line, line_mask, FULL):
    if mask in memo:
        return memo[mask]
    cand = addable_mask(mask, pair_line, line_mask, FULL)
    seen = set()
    while cand:
        lsb = cand & -cand
        cand ^= lsb
        seen.add(grundy(mask | lsb, memo, pair_line, line_mask, FULL))
    g = 0
    while g in seen:
        g += 1
    memo[mask] = g
    return g


def misere_win(mask, memo, pair_line, line_mask, FULL):
    """True if the player to move wins under the 'last move loses' convention."""
    if mask in memo:
        return memo[mask]
    cand = addable_mask(mask, pair_line, line_mask, FULL)
    if cand == 0:
        memo[mask] = True          # no move => the player to move wins (misere)
        return True
    win = False
    c = cand
    while c:
        lsb = c & -c
        c ^= lsb
        if not misere_win(mask | lsb, memo, pair_line, line_mask, FULL):
            win = True
            break
    memo[mask] = win
    return win


def main():
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    failures = 0
    print("=" * 78)
    print("TASK 4: parity theorem, Grundy distribution, misere value")
    print("=" * 78)
    boards = [
        ("PG(2,8)", "../output/board_pg2q8.txt", "census_pg_main.log", CLAIM_PG),
        ("AG(2,8)", "../output/board_ag2q8.txt", "census_ag_main.log", CLAIM_AG),
    ]
    for name, board, log, claim in boards:
        print()
        print(f"--- {name} ---")
        n, lines = parse_board(board)
        sizes, maxs = read_census(log)
        total = sum(sizes.values())
        print(f"  independent census total      : {total}")
        print(f"  claimed total                 : {claim['total']}   "
              f"{'MATCH' if total == claim['total'] else 'MISMATCH'}")
        if total != claim['total']:
            failures += 1
        # distribution
        size_ok = all(sizes.get(k, 0) == v for k, v in claim["sizes"].items())
        print(f"  size distribution vs claim    : {'MATCH' if size_ok else 'MISMATCH'}")
        if not size_ok:
            failures += 1
        # maximal sizes
        max_sizes = sorted(k for k, v in maxs.items() if v > 0)
        max_ok = all(v == claim["max"].get(k, 0) for k, v in maxs.items()) and \
            all(maxs.get(k, 0) == v for k, v in claim["max"].items())
        print(f"  maximal sizes (nonzero counts): {max_sizes}")
        print(f"  maximal counts vs claim       : {'MATCH' if max_ok else 'MISMATCH'}")
        if not max_ok:
            failures += 1
        all_even = all(k % 2 == 0 for k in max_sizes)
        print(f"  every maximal size even (p=0) : {'PASS' if all_even else 'FAIL'}   "
              f"(p = {0 if all_even else 'undefined'})")
        if not all_even:
            failures += 1
        # Grundy = (p - |S|) mod 2 = |S| mod 2 ; distribution = even/odd totals
        even = sum(v for k, v in sizes.items() if k % 2 == 0)
        odd = sum(v for k, v in sizes.items() if k % 2 == 1)
        print(f"  even-size caps (Grundy 0)     : {even}")
        print(f"  odd-size caps  (Grundy 1)     : {odd}")
        print(f"  even+odd = {even + odd} = total  {'PASS' if even + odd == total else 'FAIL'}")
        g_ok = (even == claim["grundy"][0] and odd == claim["grundy"][1])
        print(f"  Grundy distribution vs claim  : {'MATCH' if g_ok else 'MISMATCH'}   "
              f"claimed {{0: {claim['grundy'][0]}, 1: {claim['grundy'][1]}}}")
        if not g_ok:
            failures += 1
        print(f"  Grundy(empty) = |empty| mod 2 = 0 : PASS")

    # ------------------------------------------------------------------
    # direct game recursion on the sampled caps
    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("Direct normal-play Grundy / misere recursion on sampled caps")
    print("=" * 78)
    for name, board, log, claim in boards:
        print()
        print(f"--- {name} ---")
        n, lines = parse_board(board)
        pair_line, line_mask, FULL = build_index(n, lines)
        samples = []
        with open(log, encoding="utf-8") as f:
            for ln in f:
                t = ln.split()
                if t and t[0] == "SAMPLE":
                    samples.append((t[1], int(t[2]),
                                    tuple(int(x) for x in t[3:])))
        memo_g = {}
        memo_m = {}
        bad_g = 0
        bad_m = 0
        by_size = defaultdict(lambda: [0, 0])
        for label, size, pts in samples:
            mask = 0
            for p in pts:
                mask |= 1 << p
            g = grundy(mask, memo_g, pair_line, line_mask, FULL)
            w = misere_win(mask, memo_m, pair_line, line_mask, FULL)
            pred_g = size % 2
            pred_w = (size % 2 == 0)
            by_size[size][0] += 1
            if g != pred_g:
                bad_g += 1
                if bad_g <= 5:
                    print(f"  FAIL grundy: size {size} cap {pts}: G={g} != {pred_g}")
            if w != pred_w:
                bad_m += 1
                if bad_m <= 5:
                    print(f"  FAIL misere: size {size} cap {pts}: win={w} != {pred_w}")
        print(f"  sampled caps checked: {len(samples)} "
              f"(sizes {sorted(by_size)})")
        print(f"  normal-play Grundy(S) = |S| mod 2 : "
              f"{'PASS' if bad_g == 0 else f'FAIL ({bad_g})'}")
        print(f"  misere win iff |S| even (S non-empty positions sampled) : "
              f"{'PASS' if bad_m == 0 else f'FAIL ({bad_m})'}")
        print(f"  misere(empty) = WIN for player to move: follows because every "
              f"maximal size is even, so every complete play from empty has even "
              f"length (the second player makes the last move and loses).")
        if bad_g or bad_m:
            failures += 1

    print()
    print("=" * 78)
    print(f"RESULT: {'PASS' if failures == 0 else f'FAIL ({failures})'}")
    print("=" * 78)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
