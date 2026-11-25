#!/usr/bin/env python3
"""Pre-declaration probe: z=0/z=1 window+2 extension feasibility.
Engine block: sha-gated extraction from the published K1270 verifier
verify_ones_multiset_t2_lowz_banded.py (SHA-256 dda422f28f646821b4ec1529cac45837d5b4694246bb465f081a7beba1be9bdd)."""
import hashlib, itertools, json, random, sys

SRC = open("verify_ones_multiset_t2_lowz_banded.py", "rb").read()
PIN = "dda422f28f646821b4ec1529cac45837d5b4694246bb465f081a7beba1be9bdd"
assert hashlib.sha256(SRC).hexdigest() == PIN, "sha gate failed"
text = SRC.decode("utf-8")
s = text.index("# === ENGINE BLOCK")
e = text.index("# === END ENGINE BLOCK ===") + len("# === END ENGINE BLOCK ===")
engine_block = text[s:e]
ns = {}
import functools, sys as _sys
ns['lru_cache'] = functools.lru_cache
ns['sys'] = _sys
sys.setrecursionlimit(1_000_000)
exec(engine_block, ns)
# bounded-memoization twin (published convention: value-transparent recursive
# memo with explicit LRU cap; recursion is pure deterministic so results are
# unchanged; cap guards the host's memory as in the published census machines)
import functools as _ft
_CAP = 1_200_000
def _capped(fn):
    return _ft.lru_cache(maxsize=_CAP)(fn.__wrapped__)
ns["H_ordered"] = _capped(ns["H_ordered"])
ns["H_canonical"] = _capped(ns["H_canonical"])
H_ordered, H_canonical, single_token = ns["H_ordered"], ns["H_canonical"], ns["single_token"]
def clear_engines():
    H_ordered.cache_clear()
    H_canonical.cache_clear()

def V(x, z, R):  # published closed form
    return single_token(x, z, R)

def H(R, X, z, eng="canon"):
    return H_canonical(R, tuple(X), z) if eng == "canon" else H_ordered(R, tuple(X), z)

def multi(X):  # sorted non-decreasing multiset tuple
    return tuple(sorted(X))

results = {}

# P1: Z1 grid  H(2;W;0)=0 for |W|>=2 ; = v for |W|=1
bad = pts = 0
for arity in (1, 2, 3, 4):
    for tok in itertools.product(range(1, 7), repeat=arity):
        W = multi(tok)
        exp = V(W[0], 0, 2) if len(W) == 1 else 0
        for eng in ("canon", "ord"):
            pts += 1
            if H(2, W, 0, eng) != exp: bad += 1
results["P1_Z1_grid"] = {"points": pts, "bad": bad}

# P2: Z0 grid  H(3;{1} U Y';0) for len(Y')<=3, min(Y')>=2
bad = pts = 0
exs = []
for n in range(0, 4):  # Y' arity
    for tok in itertools.product(range(2, 8), repeat=n):
        Y = multi(tok)
        X = multi((1,) + Y)
        exp = 2 if n >= 1 else V(1, 0, 3)
        for eng in ("canon", "ord"):
            pts += 1
            v = H(3, X, 0, eng)
            if v != exp:
                bad += 1
                if len(exs) < 5: exs.append((X, eng, v, exp))
results["P2_Z0_grid"] = {"points": pts, "bad": bad, "examples": exs}

# P3: T_A grid  z=0, R=m+2, min>=2
def shape_battery(m):
    shapes = set()
    # fixed battery
    for t in (m, m + 1, m + 2, 2 * m, 3 * m, 7, 22):
        if t >= m:
            shapes.add(multi((m, t)))
            shapes.add(multi((m, t, t)))
            shapes.add(multi((m, m, t)))
            shapes.add(multi((m, t, 2 * t)))
    shapes.add(multi((m,)))
    shapes.add(multi((m,) * 3))
    shapes.add(multi((m, m + 3, m + 5)))
    return sorted(shapes)

bad = pts = 0; exs = []
for m in range(2, 15):
    for X in shape_battery(m):
        if min(X) != m: continue
        if H_ordered.cache_info().currsize > 900_000 or H_canonical.cache_info().currsize > 900_000: clear_engines()
        exp = V(sum(X), 0, m + 2)
        for eng in ("canon", "ord"):
            pts += 1
            v = H(m + 2, X, 0, eng)
            if v != exp:
                bad += 1
                if len(exs) < 5: exs.append((X, m, eng, v, exp))
results["P3_TA_fixed"] = {"points": pts, "bad": bad, "examples": exs}

# P4: T_B grid  z=1, R=m+3, min>=3
bad = pts = 0; exs = []
for m in range(3, 15):
    for X in shape_battery(m):
        if min(X) != m: continue
        if H_ordered.cache_info().currsize > 900_000 or H_canonical.cache_info().currsize > 900_000: clear_engines()
        exp = V(sum(X), 1, m + 3)
        for eng in ("canon", "ord"):
            pts += 1
            v = H(m + 3, X, 1, eng)
            if v != exp:
                bad += 1
                if len(exs) < 5: exs.append((X, m, eng, v, exp))
results["P4_TB_fixed"] = {"points": pts, "bad": bad, "examples": exs}

# P5: random deep probes T_A (m=2..25) / T_B (m=3..25)
rng = random.Random(20261124)
def rand_shape(m, maxtok=60, maxarity=4):
    k = rng.randint(1, maxarity)
    return multi([rng.randint(m, maxtok) for _ in range(k)])
bad = pts = 0; exs = []
for m in range(2, 21):
    for _ in range(12):
        X = rand_shape(m, maxtok=60, maxarity=3)
        clear_engines()
        exp = V(sum(X), 0, m + 2)
        for eng in ("canon", "ord"):
            pts += 1
            v = H(m + 2, X, 0, eng)
            if v != exp:
                bad += 1
                if len(exs) < 5: exs.append((X, m, eng, v, exp))
results["P5_TA_random"] = {"points": pts, "bad": bad, "examples": exs}
bad = pts = 0; exs = []
for m in range(3, 21):
    for _ in range(12):
        X = rand_shape(m, maxtok=60, maxarity=3)
        clear_engines()
        exp = V(sum(X), 1, m + 3)
        for eng in ("canon", "ord"):
            pts += 1
            v = H(m + 3, X, 1, eng)
            if v != exp:
                bad += 1
                if len(exs) < 5: exs.append((X, m, eng, v, exp))
results["P6_TB_random"] = {"points": pts, "bad": bad, "examples": exs}

# P7: boundary records (sharpeness, observational)
rec = {}
# (x,2) @ z=0 R=5: parent vs single (R=m+3 for m=2)
rec["m2_z0_R5_two_token"] = []
for x in (3, 4, 5, 6, 9):
    p = H(5, (x, 2), 0, "canon"); s = V(x + 2, 0, 5)
    rec["m2_z0_R5_two_token"].append({"X": [x, 2], "parent": p, "single": s, "sep": p != s})
# m=2 z=1 R=5 band: multi-token shapes
rec["m2_z1_R5_band"] = []
for X in [(2,2), (2,3), (2,4), (2,5), (2,2,2), (2,3,3), (2,9), (2,)]:
    p = H(5, multi(X), 1, "canon"); s = V(sum(X), 1, 5)
    rec["m2_z1_R5_band"].append({"X": list(multi(X)), "parent": p, "single": s, "sep": p != s})
# m=1 z=0 R=4: min=1 separation beyond window
rec["m1_z0_R4"] = []
for X in [(1,2), (1,3), (1,4), (1,1), (1,), (1,1,1)]:
    p = H(4, multi(X), 0, "canon"); s = V(sum(X), 0, 4)
    rec["m1_z0_R4"].append({"X": list(multi(X)), "parent": p, "single": s, "sep": p != s})
results["P7_boundary"] = rec

# P8: T_A3 / T_B3 observational (window+3; NOT a claim)
bad3 = pts3 = 0; exs3 = []
for m in range(3, 15):
    for X in shape_battery(m):
        for eng in ("canon",):
            pts3 += 1
            v = H(m + 3, X, 0, eng)
            if v != V(sum(X), 0, m + 3):
                bad3 += 1
                if len(exs3) < 8: exs3.append((X, m, v, V(sum(X), 0, m + 3)))
results["P8_TA3_observational"] = {"points": pts3, "sep_count": bad3, "examples": exs3}
bad3 = pts3 = 0; exs3 = []
for m in range(4, 15):
    for X in shape_battery(m):
        pts3 += 1
        v = H(m + 4, X, 1, "canon")
        if v != V(sum(X), 1, m + 4):
            bad3 += 1
            if len(exs3) < 8: exs3.append((X, m, v, V(sum(X), 1, m + 4)))
results["P9_TB3_observational"] = {"points": pts3, "sep_count": bad3, "examples": exs3}

out = {"engine_pin": PIN, "results": results}
print(json.dumps(out, sort_keys=True, indent=1))
