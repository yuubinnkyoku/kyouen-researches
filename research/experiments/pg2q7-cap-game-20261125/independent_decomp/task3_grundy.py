"""Task 3: independent Grundy values.

Part A: full bottom-up DP over ALL caps (sizes 8 down to 0), using only the
        board definition G(S) = mex{ G(S+p) : p addable }.  This yields the
        complete Grundy distribution and is stronger than sampling.
Part B: for random samples of 5-caps with / without an extension to a MAXIMAL
        7-cap, recompute G by a fresh recursive upset DP and compare with Part A
        (the task's required sample check).
Part C: check, on all 5-caps, that every one has a maximal 6-child, and that
        {S : G(S)=2} equals exactly the set of 5-subsets of maximal 7-caps.

Outputs summary_grundy.json.
"""

import json
import random
import struct
import time
from array import array

from boardlib import Board, HERE, bits, read_board

t0 = time.time()
N, M, BLOCKS = read_board()
brd = Board(N, BLOCKS)
FULL = brd.FULL
PAIR = brd.pair_line


def load_caps(path=HERE / "caps_by_size.bin"):
    with open(path, "rb") as f:
        assert f.read(6) == b"CAPS1\n"
        n = struct.unpack("<I", f.read(4))[0]
        caps = []
        for _ in range(n + 1):
            cnt = struct.unpack("<Q", f.read(8))[0]
            arr = array("Q")
            if cnt:
                arr.fromfile(f, cnt)
            caps.append(arr)
    return n, caps


def forbidden_from_scratch(S):
    pts = []
    m = S
    while m:
        b = m & -m
        pts.append(b.bit_length() - 1)
        m ^= b
    f = 0
    for i, a in enumerate(pts):
        pa = PAIR[a]
        for b in pts[i + 1:]:
            f |= pa[b]
    return f


def make_forbidden(S):
    """(forbidden, addable) for arbitrary S."""
    f = forbidden_from_scratch(S)
    return f, FULL & ~S & ~f


def mex(values):
    g = 0
    while g in values:
        g += 1
    return g


N2, caps = load_caps()
max_size = max(k for k in range(N2 + 1) if caps[k])
assert N2 == N
total_caps = sum(len(caps[k]) for k in range(max_size + 1))

# ------------------------------------------------------------------ Part A: DP
G = {}
dist = [dict() for _ in range(max_size + 1)]
t_dp = time.time()
for k in range(max_size, -1, -1):
    for S in caps[k]:
        f = 0
        pts = []
        m = S
        while m:
            b = m & -m
            pts.append(b.bit_length() - 1)
            m ^= b
        for i, a in enumerate(pts):
            pa = PAIR[a]
            for b in pts[i + 1:]:
                f |= pa[b]
        A = FULL & ~S & ~f
        if k == max_size:
            assert A == 0, f"non-maximal {k}-cap {S}"
        seen = set()
        m = A
        while m:
            b = m & -m
            seen.add(G[S | b])
            m ^= b
        g = 0
        while g in seen:
            g += 1
        G[S] = g
        dist[k][g] = dist[k].get(g, 0) + 1
print(f"[A] full DP over {total_caps} caps in {time.time() - t_dp:.1f}s", flush=True)

grundy_totals = {}
for k in range(max_size + 1):
    for g, c in dist[k].items():
        grundy_totals[g] = grundy_totals.get(g, 0) + c
assert sum(grundy_totals.values()) == total_caps
assert G[0] == 0

# ------------------------------------------------- Part C prerequisites: 7/8 sets
# maximal 7-caps, determined from the board definition (not from stored flags)
max7 = []
for S in caps[7]:
    f, A = make_forbidden(S)
    if A == 0:
        max7.append(S)
assert len(max7) == sum(1 for S in caps[7] if G[S] == 0), "maximal 7-caps must have G=0"
for S in caps[8]:
    f, A = make_forbidden(S)
    assert A == 0, "8-cap is not maximal"

# 5-subsets of maximal 7-caps (the claimed "with a 7-extension" set)
five_max7 = set()
for S in max7:
    pts = list(bits(S))
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                for l in range(k + 1, 7):
                    for mm in range(l + 1, 7):
                        five_max7.add((1 << pts[i]) | (1 << pts[j]) | (1 << pts[k])
                                      | (1 << pts[l]) | (1 << pts[mm]))
assert len(five_max7) == len(max7) * 21

# reference sets under alternative readings of "7-extension"
max7_set = set(max7)
five_any7 = set()
five_nonmax7 = set()
for S in caps[7]:
    is_max = S in max7_set
    pts = list(bits(S))
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                for l in range(k + 1, 7):
                    for mm in range(l + 1, 7):
                        T = (1 << pts[i]) | (1 << pts[j]) | (1 << pts[k]) | (1 << pts[l]) | (1 << pts[mm])
                        five_any7.add(T)
                        if not is_max:
                            five_nonmax7.add(T)
five_in_8 = set()
for S in caps[8]:
    pts = list(bits(S))
    for i in range(8):
        for j in range(i + 1, 8):
            for k in range(j + 1, 8):
                for l in range(k + 1, 8):
                    for mm in range(l + 1, 8):
                        five_in_8.add((1 << pts[i]) | (1 << pts[j]) | (1 << pts[k])
                                      | (1 << pts[l]) | (1 << pts[mm]))

# ------------------------------------- Part C: all 5-caps, maximal 6-child, G=2 set
g2set = set()
five_all_have_max6 = 0
five_has_max6 = []
five_with_g1child = 0
five_with_g2 = 0
t5 = time.time()
for S in caps[5]:
    f = forbidden_from_scratch(S)
    A = FULL & ~S & ~f
    has_max6 = False
    has_g1child = False
    m = A
    while m:
        b = m & -m
        T = S | b
        f2 = f
        s = S
        pl = PAIR[b.bit_length() - 1]
        while s:
            bb = s & -s
            f2 |= pl[bb.bit_length() - 1]
            s ^= bb
        if (FULL & ~T & ~f2) == 0:
            has_max6 = True
        if G[T] == 1:
            has_g1child = True
        m ^= b
    if has_max6:
        five_all_have_max6 += 1
    if G[S] == 2:
        g2set.add(S)
        five_with_g2 += 1
    if has_g1child:
        five_with_g1child += 1
print(f"[C] 5-cap scan in {time.time() - t5:.1f}s", flush=True)

assert five_all_have_max6 == len(caps[5]), "not every 5-cap has a maximal 6-child"
assert g2set == five_max7, "G=2 set differs from 5-subsets of maximal 7-caps"
assert five_with_g1child == len(five_max7)

# ------------------------------------------------------- Part B: sample upset DP
def grundy_recursive(S):
    """Fresh memoised recursion from this position; returns (G, visited)."""
    memo = {}

    def rec(T):
        if T in memo:
            return memo[T]
        f = forbidden_from_scratch(T)
        A = FULL & ~T & ~f
        seen = set()
        m = A
        while m:
            b = m & -m
            seen.add(rec(T | b))
            m ^= b
        g = mex(seen)
        memo[T] = g
        return g

    g = rec(S)
    return g, len(memo)


rng = random.Random(20261125)
with7 = sorted(five_max7)
without7 = [S for S in caps[5] if S not in five_max7]
assert len(with7) == 49392
assert len(without7) == 395136

sample_with = rng.sample(with7, 30)
sample_without = rng.sample(without7, 30)
sample_rows = []
bad_samples = 0
for group, samples, expected in (("with7", sample_with, 2), ("without7", sample_without, 1)):
    for S in samples:
        g_rec, visited = grundy_recursive(S)
        # maximal 6-child check for this sample
        f, A = make_forbidden(S)
        has_max6 = False
        m = A
        while m:
            b = m & -m
            T = S | b
            f2 = f
            s = S
            pl = PAIR[b.bit_length() - 1]
            while s:
                bb = s & -s
                f2 |= pl[bb.bit_length() - 1]
                s ^= bb
            if (FULL & ~T & ~f2) == 0:
                has_max6 = True
            m ^= b
        ok = (g_rec == expected == G[S]) and has_max6
        if not ok:
            bad_samples += 1
        sample_rows.append({
            "group": group,
            "points": sorted(bits(S)),
            "g_recursive": g_rec,
            "g_full_dp": G[S],
            "expected": expected,
            "has_maximal_6_child": has_max6,
            "visited_positions": visited,
        })
assert bad_samples == 0

# ------------------------------------------------------------- write JSON summary
summary = {
    "total_caps": total_caps,
    "max_cap_size": max_size,
    "grundy_totals": {str(g): c for g, c in sorted(grundy_totals.items())},
    "distribution_by_size": {
        str(k): {str(g): c for g, c in sorted(dist[k].items())}
        for k in range(max_size + 1)
    },
    "five_caps": {
        "total": len(caps[5]),
        "g_distribution": {str(g): c for g, c in sorted(dist[5].items())},
        "with_maximal_6_child": five_all_have_max6,
        "with_g1_child": five_with_g1child,
        "g2_count": five_with_g2,
        "five_subsets_of_maximal7": len(five_max7),
        "five_subsets_of_any7": len(five_any7),
        "five_subsets_of_nonmaximal7": len(five_nonmax7),
        "five_subsets_of_8": len(five_in_8),
        "g2_equals_five_subsets_of_maximal7": g2set == five_max7,
    },
    "seven_caps": {
        "total": len(caps[7]),
        "maximal": len(max7),
        "nonmaximal": len(caps[7]) - len(max7),
        "g_distribution": {str(g): c for g, c in sorted(dist[7].items())},
    },
    "eight_caps": {
        "total": len(caps[8]),
        "maximal": len(caps[8]),
        "g_distribution": {str(g): c for g, c in sorted(dist[8].items())},
    },
    "samples": {
        "rng_seed": 20261125,
        "with7": sample_rows[:30],
        "without7": sample_rows[30:],
        "bad": bad_samples,
    },
    "root_grundy": G[0],
    "elapsed_sec": round(time.time() - t0, 1),
}
(HERE / "summary_grundy.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps({k: summary[k] for k in
                  ("total_caps", "grundy_totals", "distribution_by_size",
                   "five_caps", "root_grundy", "elapsed_sec")}, indent=2))
