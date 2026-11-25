#!/usr/bin/env python3
"""verify_lowz_window2.py -- formal machine for the low-z window+2 banded rows.

THEOREMS (status target: proved; proofs pre-registered in the single-owner
declaration note, publish-then-execute):

  Z1 (fact):   H(2;W;0) = 0 for every multiset W with |W|>=2
               (|W|=1 rows are the single-token game itself).
  Z0 (lemma):  H(3;{1} u Y';0) = 2 for every nonempty Y' with min(Y')>=2,
               and H(3;(1);0) = v(1,0,3) = 1.
  T_A:  for all m>=2 and all finite multisets X with min(X)=m:
        H(m+2;X;0) = v(sumX,0,m+2)          (z=0 window+2 row)
  T_A3: for all m>=3 and all X with min(X)=m:
        H(m+3;X;0) = v(sumX,0,m+3)          (z=0 window+3 row)
  T_B:  for all m>=3 and all X with min(X)=m:
        H(m+3;X;1) = v(sumX,1,m+3)          (z=1 window+2 row)

Where v = the published K0832 single-token closed form; the engine block is
byte-exact (inner-block sha256 ENGINE_PIN below) against the published chain
K1264 -> K1268 -> K1271 -> ... -> this machine (see build_engine_from_published.py).

Proof skeleton (full text in the declaration note):
  z=0 slice, A-child analysis: with min>=2 there is no B-child and no
  C-child.  Every A-child sits at budget (index-1) with min either m
  (K1270 window+1 value) or m-1 (induction hypothesis of the previous row
  family), and both types collapse to the same single value, so the parent
  option set is a singleton identical to the single-token side's option set.
  Bases: T_A(2) closes via Z0 (options subset {1,2}, mex 0 = v(sumX,0,4));
  T_A3(3) closes via the absorption argument: a min-2 child W of a min-3
  parent contains a token >=3, and W's own A-child on that token is a
  budget-(2+2) min-2 position, which collapses to 0 by T_A(2), hence 0 is in
  W's options, hence c = H(5;W;0) != 0, hence parent mex({1,c}) = 0 =
  v(sumX,0,6) ... full detail in the note.
  z=1 slice: T_B(m>=4) is a two-option-set identity match (A-children via
  K1270 z=1 row / T_B(m-1), C-child via 1 XOR T_A(m)).  T_B(3) base: the
  min-2 child c of a min-3 parent satisfies c != 1 because c's C-child is
  1 XOR H(4;W;0) = 1 XOR T_A(2)(W) = 1 XOR 0 = 1, which lies in c's option
  set; parent options {0} u {c!=1} have mex 1 = v(sumX,1,6).

Checks (protocol registered in the declaration; all raw engines both
H_canonical and H_ordered, fixed seeds, deterministic, fail-closed):
  D0  closed form x dual-engine anchor grid (K0832 pin; spec shared with the
      published K1270 machine D0)
  D1  Z1 grid (arity<=4, tokens 1..6, both engines)
  D2  Z0 grid (Y' arity<=3, tokens 2..7, both engines) x engine cross
  D3  T_A grids: fixed battery m=2..14 + light m=15..25 + deep random
  D4  T_B grids: fixed battery m=3..14 + light m=15..25 + deep random
  D5  T_A3 grids: fixed battery m=3..14 + light m=15..25 + deep random
  D6  structural option-set checks (typed per-child analysis; live rerun of
      the induction-step obligations on the raw engine)
  D7  published anchors (17-row table identical to the K1270 machine)
  D8  deep fixed-seed probes (m=2..25, tokens<=60, arity<=4 + big-token
      spikes up to 211) x both engines, value-transparent cache clears
  D9  boundary records (observational only, no claims): m=2 z=0 R=5
      two-token deviants, m=2 z=1 R=5 band, m=1 z=0 R=4, window+4 z=0 and
      window+3 z=1 observational sweeps
  Battery of fail-closed tamper variants (each must be caught; see TAMPER).

Determinism: audit written only when every gate passes (fail-closed);
randomness only through fixed seeds; output keys sorted.
Bounded-memoization: the recursion is pure/deterministic; the cache caps and
intermittent clears are value-transparent (published census-machine
convention).
"""
import hashlib, itertools, json, os, random, sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

# === ENGINE BLOCK (machine-extracted from the published K1270 verifier; inner bytes sha-256 pinned and eight-way byte-verified by build_engine_from_published.py) ===
def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

# === END ENGINE BLOCK ===

SELF_PATH = os.path.abspath(__file__)
SELF_SHA = hashlib.sha256(open(SELF_PATH, "rb").read()).hexdigest()
ENGINE_PIN = ("bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3"
              "a92")


def _cut_engine_text():
    lines = open(SELF_PATH, encoding="utf-8").read().split("\n")
    s = e = None
    for i, ln in enumerate(lines):
        if ln.startswith("# === ENGINE BLOCK"):
            s = i + 1
        if ln.startswith("# === END ENGINE BLOCK"):
            e = i
    assert s is not None and e is not None and e > s, "engine markers missing"
    blk = lines[s:e]
    while blk and blk[-1].strip() == "":
        blk.pop()
    return "\n".join(blk) + "\n"


ENGINE_BLOCK_TEXT = _cut_engine_text()
ENGINE_SHA = hashlib.sha256(ENGINE_BLOCK_TEXT.encode("utf-8")).hexdigest()
assert ENGINE_SHA == ENGINE_PIN, "engine block sha gate failed"
ENGINE_BYTES = len(ENGINE_BLOCK_TEXT.encode("utf-8"))

# ---- bounded-memoization twin (value-transparent; published census convention)
_CAP = 1_200_000
H_ordered = lru_cache(maxsize=_CAP)(H_ordered.__wrapped__)
H_canonical = lru_cache(maxsize=_CAP)(H_canonical.__wrapped__)


def clear_engines():
    H_ordered.cache_clear()
    H_canonical.cache_clear()


def V(x, z, R):
    return single_token(x, z, R)


def TA(X, m):
    return V(sum(X), 0, m + 2)


def TB(X, m):
    return V(sum(X), 1, m + 3)


def TA3(X, m):
    return V(sum(X), 0, m + 3)


# ------------------------------------------------------------------ batteries
def multi(X):
    return tuple(sorted(X))


def shape_battery(m):
    shapes = set()
    for t in (m, m + 1, m + 2, 2 * m, 3 * m, 7, 22):
        if t >= m:
            shapes.add(multi((m, t)))
            shapes.add(multi((m, t, t)))
            shapes.add(multi((m, m, t)))
            shapes.add(multi((m, t, 2 * t)))
    shapes.add(multi((m,)))
    shapes.add(multi((m, m, m)))
    shapes.add(multi((m, m + 3, m + 5)))
    shapes.add(multi((m, m + 1, m + 2, m + 4)))
    out = sorted(shapes)
    assert all(min(X) == m for X in out)
    return out


def light_battery(m):
    out = [multi(X) for X in ((m,), (m, m), (m, 2 * m),
                             (m, m + 3, m + 5), (m, m + 7), (m, m + 11))]
    assert all(min(X) == m for X in out)
    return out


def rand_shapes(rng, m, n, maxtok, maxarity):
    out = []
    for _ in range(n):
        k = rng.randint(1, maxarity)
        out.append(multi([rng.randint(m, maxtok) for _ in range(k)]))
    return out


def m_gt_cap():
    ci = H_ordered.cache_info().currsize
    cc = H_canonical.cache_info().currsize
    if ci > 900_000 or cc > 900_000:
        clear_engines()


# ------------------------------------------------------------------ D0
def check_D0():
    bad = pts = 0
    for x in range(1, 41):
        for z in range(0, 21):
            rmax = min(x + z + 2, 40)
            for R in range(0, rmax + 1):
                s = single_token(x, z, R)
                pts += 1
                if H_canonical(R, (x,), z) != s:
                    bad += 1
                if H_ordered(R, (x,), z) != s:
                    bad += 1
        clear_engines()
    return {"label": "D0 closedform x dual-engine anchor grid",
            "points": pts, "comparisons": pts * 2, "bad": bad}


# ------------------------------------------------------------------ D1  Z1
def check_D1(z1_mut=None):
    bad = pts = 0
    for arity in (1, 2, 3, 4):
        for tok in itertools.product(range(1, 7), repeat=arity):
            W = multi(tok)
            if len(W) == 1:
                exp = V(W[0], 0, 2)
            else:
                exp = 0 if z1_mut is None else z1_mut
            for eng in (H_canonical, H_ordered):
                pts += 1
                if eng(2, W, 0) != exp:
                    bad += 1
    return {"label": "D1 Z1 grid (H(2;W;0)=0 for |W|>=2)",
            "points": pts, "comparisons": pts, "bad": bad}


# ------------------------------------------------------------------ D2  Z0
def check_D2(z0_mut=None, z0empty_mut=None):
    bad = pts = 0
    examples = []
    for n in range(0, 4):
        for tok in itertools.product(range(2, 8), repeat=n):
            Y = multi(tok)
            X = multi((1,) + Y)
            if n == 0:
                exp = V(1, 0, 3) if z0empty_mut is None else z0empty_mut
            else:
                exp = 2 if z0_mut is None else z0_mut
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(3, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "eng": eng.__name__,
                                         "got": val, "exp": exp})
    return {"label": "D2 Z0 grid (H(3;{1}uY';0)=2 / v(1,0,3))",
            "points": pts, "comparisons": pts, "bad": bad,
            "examples": examples}


# ------------------------------------------------------------------ D3  T_A
def check_D3(idx_mut=None):
    bad = pts = 0
    examples = []
    rng = random.Random(20261142)
    for m in range(2, 15):
        for X in shape_battery(m):
            R = m + (3 if idx_mut else 2)
            exp = V(sum(X), 0, R)
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(R, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
            m_gt_cap()
    for m in range(15, 26):
        for X in light_battery(m):
            exp = TA(X, m)
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 2, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
            m_gt_cap()
    for m in range(2, 21):
        for X in rand_shapes(rng, m, 10, 60, 4):
            exp = TA(X, m)
            clear_engines()
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 2, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
    return {"label": "D3 T_A grids (fix m2-14 + light 15-25 + deep random)",
            "points": pts, "comparisons": pts, "bad": bad,
            "examples": examples}


# ------------------------------------------------------------------ D4  T_B
def check_D4(mlo_mut=None):
    bad = pts = 0
    examples = []
    rng = random.Random(20261143)
    mstart = 2 if mlo_mut == 2 else 3
    for m in range(mstart, 15):
        for X in shape_battery(m):
            exp = TB(X, m)
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 3, X, 1)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
            m_gt_cap()
    for m in range(15, 26):
        for X in light_battery(m):
            exp = TB(X, m)
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 3, X, 1)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
            m_gt_cap()
    for m in range(3, 21):
        for X in rand_shapes(rng, m, 10, 60, 4):
            exp = TB(X, m)
            clear_engines()
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 3, X, 1)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
    return {"label": "D4 T_B grids (fix m3-14 + light 15-25 + deep random)",
            "points": pts, "comparisons": pts, "bad": bad,
            "examples": examples}


# ------------------------------------------------------------------ D5  T_A3
def check_D5(mlo_mut=None):
    bad = pts = 0
    examples = []
    rng = random.Random(20261144)
    mstart = 2 if mlo_mut == 2 else 3
    for m in range(mstart, 15):
        for X in shape_battery(m):
            exp = TA3(X, m)
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 3, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
            m_gt_cap()
    for m in range(15, 26):
        for X in light_battery(m):
            exp = TA3(X, m)
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 3, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
            m_gt_cap()
    for m in range(3, 21):
        for X in rand_shapes(rng, m, 10, 60, 4):
            exp = TA3(X, m)
            clear_engines()
            for eng in (H_canonical, H_ordered):
                pts += 1
                val = eng(m + 3, X, 0)
                if val != exp:
                    bad += 1
                    if len(examples) < 5:
                        examples.append({"X": list(X), "m": m,
                                         "engine": eng.__name__, "got": val,
                                         "exp": exp})
    return {"label": "D5 T_A3 grids (fix m3-14 + light 15-25 + deep random)",
            "points": pts, "comparisons": pts, "bad": bad,
            "examples": examples}


# ------------------------------------------------------------------ D6 structural
def raw_children_options(R, X, z, eng):
    vals = set()
    for i, w in enumerate(X):
        if w > 1:
            vals.add(eng(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            vals.add(eng(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        vals.add(1 ^ eng(R - 1, X, z - 1))
    return vals


def single_side_options(R, Sig, z, eng):
    vals = set()
    if Sig > 1:
        vals.add(eng(R - 1, (Sig - 1,), z))
    else:
        vals.add(eng(R - 1, (), z + 1))
    if z >= 1:
        vals.add(1 ^ eng(R - 1, (Sig,), z - 1))
    return vals


def check_D6():
    bad = pts = 0
    examples = []

    def eq(a, b, tag):
        nonlocal pts, bad
        pts += 1
        if a != b:
            bad += 1
            if len(examples) < 8:
                ga = sorted(a) if isinstance(a, (set, frozenset)) else a
                gb = sorted(b) if isinstance(b, (set, frozenset)) else b
                examples.append({"tag": tag, "got": ga, "exp": gb})

    # (a) T_A uniform step (m>=3): singleton option sets, both sides
    for m in range(3, 13):
        for X in shape_battery(m):
            if len(X) < 2:
                continue
            for eng in (H_canonical, H_ordered):
                po = raw_children_options(m + 2, X, 0, eng)
                so = single_side_options(m + 2, sum(X), 0, eng)
                eq(po, {(1 + m) % 2}, "TA po singleton m=%d" % m)
                eq(so, {(1 + m) % 2}, "TA so singleton m=%d" % m)
                eq(po, so, "TA po==so m=%d" % m)
                for i, w in enumerate(X):
                    child = X[:i] + (w - 1,) + X[i + 1:]
                    eq(eng(m + 1, child, 0), V(sum(X) - 1, 0, m + 1),
                       "TA typed child m=%d i=%d" % (m, i))
            m_gt_cap()
    # (b) T_A base m=2
    for X in shape_battery(2):
        if len(X) < 2:
            continue
        for eng in (H_canonical, H_ordered):
            po = raw_children_options(4, X, 0, eng)
            eq(po <= {1, 2}, True, "TA2 po subset")
            eq(eng(4, X, 0), V(sum(X), 0, 4), "TA2 parent")
            for i, w in enumerate(X):
                child = X[:i] + (w - 1,) + X[i + 1:]
                cv = eng(3, child, 0)
                eq(cv in (1, 2), True, "TA2 child value in {1,2}")
                if w == 2:
                    eq(cv, 2, "TA2 Z0 child (min dropped to 1)")
                else:
                    eq(cv, 1, "TA2 K1270 child (min kept)")
    # (c) T_B uniform step (m>=4)
    for m in range(4, 13):
        for X in shape_battery(m):
            if len(X) < 2:
                continue
            for eng in (H_canonical, H_ordered):
                po = raw_children_options(m + 3, X, 1, eng)
                so = single_side_options(m + 3, sum(X), 1, eng)
                eq(po, so, "TB po==so m=%d" % m)
                eq(po, {V(sum(X) - 1, 1, m + 2),
                        1 ^ V(sum(X), 0, m + 2)},
                   "TB po explicit m=%d" % m)
                eq(eng(m + 3, X, 1), V(sum(X), 1, m + 3), "TB parent m=%d" % m)
            m_gt_cap()
    # (d) T_B base m=3
    for X in shape_battery(3):
        if len(X) < 2:
            continue
        for eng in (H_canonical, H_ordered):
            so = single_side_options(6, sum(X), 1, eng)
            eq(so, {0}, "TB3 so singleton")
            po = raw_children_options(6, X, 1, eng)
            eq(0 in po, True, "TB3 0 in po")
            eq(eng(6, X, 1), 1, "TB3 parent == 1")
            for i, w in enumerate(X):
                child = X[:i] + (w - 1,) + X[i + 1:]
                if min(child) == 2:
                    copts = raw_children_options(5, child, 1, eng)
                    eq(1 in copts, True, "TB3 c-absorption (C-child value 1)")
                    eq(eng(5, child, 1) != 1, True, "TB3 c != 1")
                else:
                    eq(eng(5, child, 1), V(sum(X) - 1, 1, 5),
                       "TB3 min-kept child")
    # (e) T_A3 base m=3
    for X in shape_battery(3):
        if len(X) < 2:
            continue
        for eng in (H_canonical, H_ordered):
            for i, w in enumerate(X):
                child = X[:i] + (w - 1,) + X[i + 1:]
                if min(child) == 2:
                    copts = raw_children_options(5, child, 0, eng)
                    eq(0 in copts, True, "TA3(3) c-absorption (0 in options)")
                    eq(eng(5, child, 0) != 0, True, "TA3(3) c != 0")
                else:
                    eq(eng(5, child, 0), V(sum(X) - 1, 0, 5),
                       "TA3(3) min-kept child")
            eq(eng(6, X, 0), V(sum(X), 0, 6), "TA3(3) parent")
    return {"label": "D6 structural option-set / typed-child checks",
            "points": pts, "comparisons": pts, "bad": bad,
            "examples": examples}


# ------------------------------------------------------------------ D7 anchors
ANCHORS = [
    ((12, 6), 17, 24, 0, 1),
    ((12, 6), 18, 25, 0, 2),
    ((14, 6), 19, 26, 0, 1),
    ((16, 6), 20, 27, 2, 1),
    ((2, 1), 1, 3, 2, 0),
    ((1, 1, 1), 1, 3, 2, 0),
    ((2, 2), 2, 5, 2, 1),
    ((4, 3), 5, 9, 2, 0),
    ((4, 4), 6, 11, 2, 1),
    ((6, 5), 9, 15, 2, 0),
    ((6, 6), 10, 17, 2, 1),
    ((1, 1), 0, 1, 1, 1),
    ((1, 1), 0, 2, 0, 0),
    ((1, 1, 1), 0, 3, 0, 1),
    ((1, 1), 1, 3, 0, 0),
    ((2, 1), 0, 3, 2, 1),
    ((2, 1), 1, 3, 2, 0),
]


def check_D7(mut_row=None):
    bad = pts = 0
    for k, (X, z, R, parent, single) in enumerate(ANCHORS):
        if mut_row is not None and k == mut_row:
            parent = (parent + 1) % 3
        for eng in (H_canonical, H_ordered):
            pts += 1
            if eng(R, X, z) != parent:
                bad += 1
        pts += 1
        if V(sum(X), z, R) != single:
            bad += 1
    return {"label": "D7 published anchors (17 rows; table identical to K1270)",
            "points": pts, "comparisons": pts, "bad": bad}


# ------------------------------------------------------------------ D8 deep probes
def check_D8(cf_mut=False):
    bad = pts = 0
    examples = []

    def Vm(x, z, R):
        s = single_token(x, z, R)
        if cf_mut and z == 1 and R == 9:
            return (s + 1) % 3
        return s

    rng = random.Random(20261145)
    fams = [("TA", 0, 2), ("TB", 1, 3), ("TA3", 0, 3)]
    for m in range(2, 26):
        for (name, z, off) in fams:
            if m < (2 if name == "TA" else 3):
                continue
            for X in rand_shapes(rng, m, 5, 60, 4):
                clear_engines()
                exp = Vm(sum(X), z, m + off)
                for eng in (H_canonical, H_ordered):
                    pts += 1
                    val = eng(m + off, X, z)
                    if val != exp:
                        bad += 1
                        if len(examples) < 5:
                            examples.append({"fam": name, "X": list(X),
                                             "m": m, "engine": eng.__name__,
                                             "got": val, "exp": exp})
            m_gt_cap()
    for (name, z, off) in fams:
        for m in (2, 3, 5, 6, 8, 13, 21):
            if m < (2 if name == "TA" else 3):
                continue
            for X in (multi((m, 211)), multi((m, 137, 61)), multi((m, 199))):
                clear_engines()
                exp = Vm(sum(X), z, m + off)
                for eng in (H_canonical, H_ordered):
                    pts += 1
                    if eng(m + off, X, z) != exp:
                        bad += 1
                        if len(examples) < 5:
                            examples.append({"fam": name, "X": list(X),
                                             "m": m, "engine": eng.__name__})
    return {"label": "D8 deep fixed-seed probes + big-token spikes",
            "points": pts, "comparisons": pts, "bad": bad,
            "examples": examples}


# ------------------------------------------------------------------ D9 boundary records
def check_D9():
    rec = {}
    rows = []
    for x in range(3, 13):
        p = H_canonical(5, multi((x, 2)), 0)
        s = V(x + 2, 0, 5)
        rows.append({"X": [x, 2], "parent": p, "single": s, "sep": p != s})
    rec["m2_z0_R5_two_token"] = rows
    rows = []
    for X in ((2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 2, 2), (2, 3, 3),
              (2, 7), (2,), (2, 2, 5)):
        p = H_canonical(5, multi(X), 1)
        s = V(sum(X), 1, 5)
        rows.append({"X": list(multi(X)), "parent": p, "single": s,
                     "sep": p != s})
    rec["m2_z1_R5_band"] = rows
    rows = []
    for X in ((1,), (1, 1), (1, 1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
              (1, 1, 3)):
        p = H_canonical(4, multi(X), 0)
        s = V(sum(X), 0, 4)
        rows.append({"X": list(multi(X)), "parent": p, "single": s,
                     "sep": p != s})
    rec["m1_z0_R4"] = rows
    sw = {"TA4_z0_m4to12_sep": 0, "TA4_z0_m4to12_pts": 0,
          "TB3_z1_m4to12_sep": 0, "TB3_z1_m4to12_pts": 0}
    for m in range(4, 13):
        for X in shape_battery(m):
            sw["TA4_z0_m4to12_pts"] += 1
            if H_canonical(m + 4, X, 0) != V(sum(X), 0, m + 4):
                sw["TA4_z0_m4to12_sep"] += 1
            sw["TB3_z1_m4to12_pts"] += 1
            if H_canonical(m + 4, X, 1) != V(sum(X), 1, m + 4):
                sw["TB3_z1_m4to12_sep"] += 1
        m_gt_cap()
    rec["observational_windowplus4_z0_and_windowplus3_z1"] = sw
    return {"label": "D9 boundary records (observational, no claims)",
            "records": rec}


# ------------------------------------------------------------------ tamper battery
def tamper_battery():
    battery = []

    def rec(name, fn):
        try:
            res = fn()
            ok = res["bad"] > 0
            battery.append({"name": name, "caught": ok,
                            "bad": res.get("bad", 0)})
        except Exception as ex:
            battery.append({"name": name, "caught": False,
                            "error": str(ex)[:120]})

    rec("M1 Z0 constant 2->3", lambda: check_D2(z0_mut=3))
    rec("M2 Z0 empty-case ->0", lambda: check_D2(z0empty_mut=0))
    rec("M3 Z1 constant 0->1", lambda: check_D1(z1_mut=1))
    rec("M4 T_A window +2->+3", lambda: check_D3(idx_mut=True))
    rec("M5 T_B min threshold 3->2", lambda: check_D4(mlo_mut=2))
    rec("M6 T_A3 min threshold 3->2", lambda: check_D5(mlo_mut=2))
    rec("M7 closed-form corrupt z=1 R=9", lambda: check_D8(cf_mut=True))
    rec("M8 anchor row 0 flip", lambda: check_D7(mut_row=0))
    return battery


# ------------------------------------------------------------------ audit
def run_audit():
    results = {}
    results["D0"] = check_D0()
    clear_engines()
    results["D1"] = check_D1()
    results["D2"] = check_D2()
    clear_engines()
    results["D3"] = check_D3()
    clear_engines()
    results["D4"] = check_D4()
    clear_engines()
    results["D5"] = check_D5()
    clear_engines()
    results["D6"] = check_D6()
    clear_engines()
    results["D7"] = check_D7()
    clear_engines()
    results["D8"] = check_D8()
    clear_engines()
    results["D9"] = check_D9()
    total_pts = sum(r["points"] for k, r in results.items() if k != "D9")
    total_bad = sum(r["bad"] for k, r in results.items() if k != "D9")
    overall = (total_bad == 0)
    audit = {
        "engine_pin": ENGINE_PIN,
        "engine_sha": ENGINE_SHA,
        "engine_block_bytes": ENGINE_BYTES,
        "memo_cap": _CAP,
        "claims": {
            "T_A": "for all m>=2, min(X)=m: H(m+2;X;0)=v(sumX,0,m+2)",
            "T_A3": "for all m>=3, min(X)=m: H(m+3;X;0)=v(sumX,0,m+3)",
            "T_B": "for all m>=3, min(X)=m: H(m+3;X;1)=v(sumX,1,m+3)",
            "Z0": "H(3;{1}uY';0)=2 (Y' nonempty min>=2); =v(1,0,3) empty",
            "Z1": "H(2;W;0)=0 for |W|>=2",
        },
        "checks": results,
        "total_points": total_pts,
        "total_bad": total_bad,
        "overall": "PASS" if overall else "FAIL",
    }
    return audit


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--tamper":
        battery = tamper_battery()
        all_caught = all(b.get("caught") is True for b in battery)
        print(json.dumps({"battery": battery, "all_caught": all_caught},
                         sort_keys=True, indent=1))
        sys.exit(0 if all_caught else 1)
    audit = run_audit()
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(outdir, exist_ok=True)
    if audit["overall"] == "PASS":
        with open(os.path.join(outdir, "audit.json"), "w") as f:
            json.dump(audit, f, sort_keys=True, indent=1)
            f.write("\n")
        print("OVERALL PASS total_points=%d total_bad=%d"
              % (audit["total_points"], audit["total_bad"]))
    else:
        print("OVERALL FAIL total_bad=%d (audit not written)"
              % audit["total_bad"])
        sys.exit(1)


if __name__ == "__main__":
    main()
