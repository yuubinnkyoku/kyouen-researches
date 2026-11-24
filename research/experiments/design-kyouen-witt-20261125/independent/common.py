"""Shared helpers for the independent verification.

Only reads output/board_*.txt (the board files) and, for comparison, the
already-published output/summary.json and output/ks_ilp.json.
No use of the Grundy executable or of scripts/ks_ilp.py.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
OUT = os.path.join(EXP, "output")
IODIR = os.path.join(HERE, "out")

TAGS = ["ag32", "ag42", "w11", "w12", "w22", "w23", "w24"]

# Claimed design parameters (from README.md/report.md), checked in Task 1.
CLAIMS = {
    "ag32": dict(name="AG(3,2)", v=8, b=14, k=4, t=3, lam={2: 3, 3: 1}),
    "ag42": dict(name="AG(4,2)", v=16, b=140, k=4, t=3, lam={2: 7, 3: 1}),
    "w11": dict(name="W_11", v=11, b=66, k=5, t=4, lam={2: 12, 3: 4, 4: 1}),
    "w12": dict(name="W_12", v=12, b=132, k=6, t=5, lam={2: 30, 3: 12, 4: 4, 5: 1}),
    "w22": dict(name="W_22", v=22, b=77, k=6, t=3, lam={2: 5, 3: 1}),
    "w23": dict(name="W_23", v=23, b=253, k=7, t=4, lam={2: 21, 3: 5, 4: 1}),
    "w24": dict(name="W_24", v=24, b=759, k=8, t=5, lam={2: 77, 3: 21, 4: 5, 5: 1}),
}

CLAIMED_K3 = {"ag32": 4, "ag42": 6, "w11": 3, "w12": 3, "w22": 7, "w23": 3, "w24": 3}
CLAIMED_K4 = {"ag32": 8, "ag42": 16, "w11": 6, "w12": 4, "w22": 10, "w23": 8, "w24": 4}


def load_board(tag):
    """Return (v, blocks) parsed from output/board_<tag>.txt."""
    path = os.path.join(OUT, "board_%s.txt" % tag)
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    n, b = (int(x) for x in lines[0].split())
    blocks = []
    for ln in lines[1:]:
        vals = [int(x) for x in ln.split()]
        assert vals[0] == len(vals) - 1
        blocks.append(tuple(vals[1:]))
    assert len(blocks) == b, (tag, len(blocks), b)
    return n, blocks


def block_masks(blocks):
    return [sum(1 << p for p in B) for B in blocks]


def incidence(v, blocks):
    inc = [[] for _ in range(v)]
    for bi, B in enumerate(blocks):
        for p in B:
            inc[p].append(bi)
    return inc


def enumerate_safe(v, blocks, s):
    """All S with |S cap B| <= s for every block, as bitmasks.

    Increasing-point DFS: every safe set is generated exactly once.
    """
    inc = incidence(v, blocks)
    b = len(blocks)
    counts = [0] * b
    out = []

    def rec(start, mask):
        out.append(mask)
        for p in range(start, v):
            ok = True
            for bi in inc[p]:
                if counts[bi] >= s:
                    ok = False
                    break
            if ok:
                for bi in inc[p]:
                    counts[bi] += 1
                rec(p + 1, mask | (1 << p))
                for bi in inc[p]:
                    counts[bi] -= 1

    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 10000))
    rec(0, 0)
    sys.setrecursionlimit(old)
    return out


def mask_points(mask):
    return [p for p in range(mask.bit_length()) if mask >> p & 1]


def block_intersections(mask, blocks):
    return [sum(1 for p in B if mask >> p & 1) for B in blocks]


def load_summary():
    with open(os.path.join(OUT, "summary.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def load_ks_ilp():
    with open(os.path.join(OUT, "ks_ilp.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_out():
    os.makedirs(IODIR, exist_ok=True)


def save_json(name, obj):
    ensure_out()
    with open(os.path.join(IODIR, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=False)


def binomial(n, r):
    if r < 0 or r > n:
        return 0
    num = 1
    den = 1
    for i in range(r):
        num *= n - i
        den *= i + 1
    return num // den


def board_lambdas(v, blocks, design_t):
    """Recompute the uniform lambda_t (t = 2..design_t) from the board alone.

    Raises AssertionError unless every t-subset is covered exactly the same
    number of times (i.e. unless the board really is the claimed t-design).
    """
    import itertools
    from collections import Counter

    lam = {}
    for t in range(2, design_t + 1):
        cnt = Counter()
        for B in blocks:
            for sub in itertools.combinations(sorted(B), t):
                cnt[sub] += 1
        vals = set(cnt.values())
        assert len(vals) == 1 and len(cnt) == binomial(v, t), (t, vals)
        lam[t] = vals.pop()
    return lam
