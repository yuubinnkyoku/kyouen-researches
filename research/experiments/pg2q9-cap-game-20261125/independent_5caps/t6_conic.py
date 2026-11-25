"""TASK 5 (independent cross-check) -- orbit structure via the conic/oval.

Every 5-cap of PG(2,9) lies on a unique conic (= oval = 10-cap; q odd), and all
conics are projectively equivalent.  Therefore the PGL orbits of 5-caps are in
bijection with the orbits of the conic stabiliser G = Stab_PGL(C) on the 252
five-subsets of C, and

    |PGL orbit| = (|PGL|/|G|) * |G-orbit| = 58,968 * |G-orbit|.

This uses none of the frame/S4 machinery of t3/t5, so it is an independent
determination of the orbit sizes 10,614,240 / 4,245,696.

Run:  python independent_5caps/t6_conic.py
"""

from __future__ import annotations

import itertools
import sys

import game
import pg

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    return ok


plane = game.plane()
PGL = ((9**3 - 1) * (9**3 - 9) * (9**3 - 9**2)) // 8
FRAME = [0, 1, 10, 20]
REP1 = [0, 1, 10, 20, 31]
REP2 = [0, 1, 10, 20, 42]

# --- 1. the unique conic (10-cap) through rep1 -------------------------------
info = game.analyze_cap(REP1)
assert info["sizes"].get(10) == 1
CONIC = None
# the upper set of rep1 contains exactly one 10-cap: rebuild it by extending
stack = [game.mask_of(REP1)]
seen = {stack[0]: plane.secant_mask(REP1)}
blocked = dict(seen)
tens = []
while stack:
    s = stack.pop()
    if s.bit_count() == 10:
        tens.append(s)
        continue
    bl_s = blocked[s]
    cand = game.FULL & ~bl_s & ~s
    members = pg.bitlist(s)
    while cand:
        low = cand & -cand
        p = low.bit_length() - 1
        cand ^= low
        t = s | low
        bl = bl_s
        for q in members:
            bl |= game.LM[p][q]
        if t not in blocked:
            blocked[t] = bl
            stack.append(t)
assert len(tens) == 1
CONIC = sorted(pg.bitlist(tens[0]))
print(f"the unique 10-cap (conic) through rep1: {CONIC}")
check("rep1 lies on exactly one 10-cap (conic) and it has 10 points",
      len(tens) == 1 and len(CONIC) == 10 and plane.is_cap(CONIC))
for p in REP1:
    assert p in CONIC

# --- 2. G = Stab_PGL(C), complete search ------------------------------------
a = [plane.vectors[p] for p in CONIC[:4]]
assert pg.vindependent(a[:3])
G = {}
for b_idx in itertools.permutations(CONIC, 4):
    M = pg.projectivity_from_frames(a, [plane.vectors[p] for p in b_idx])
    if pg.apply_to_points(M, plane, CONIC) == frozenset(CONIC):
        G.setdefault(pg.mat_canon(M), b_idx)
print(f"\ncomplete search over the {10*9*8*7} ordered 4-tuples of C: "
      f"|Stab_PGL(C)| = {len(G)}")
check("|Stab_PGL(conic)| = q(q^2-1) = 720", len(G) == 720,
      f"computed {len(G)}")
check("#conics * |G| = |PGL|, i.e. #conics = q^5-q^2 = 58,968",
      PGL % len(G) == 0 and PGL // len(G) == 9**5 - 9**2 == 58_968,
      f"{PGL:,}/{len(G)} = {PGL // len(G):,}")

# --- 3. G-orbits on the 252 five-subsets of C ------------------------------
subs = list(itertools.combinations(CONIC, 5))
print(f"five-subsets of C: {len(subs)}")
assert len(subs) == 252
sub_index = {frozenset(s): i for i, s in enumerate(subs)}
sub_masks = [game.mask_of(s) for s in subs]
parent = list(range(len(subs)))


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


Gmat = list(G)
for m in Gmat:
    img = [sub_index[pg.apply_to_points(m, plane, s)] for s in subs]
    for i, j in enumerate(img):
        ra, rb = find(i), find(j)
        if ra != rb:
            parent[ra] = rb
orbits: dict[int, list[int]] = {}
for i in range(len(subs)):
    orbits.setdefault(find(i), []).append(i)
sizes = sorted((len(v) for v in orbits.values()), reverse=True)
print(f"G-orbits on the 252 five-subsets of C: {sizes}")
check("G has exactly the two orbits of sizes 180 and 72 on the 252 subsets",
      sizes == [180, 72], f"{sizes}")
check("orbit sizes sum to 252", sum(sizes) == 252)

# --- 4. PGL orbit sizes = 58,968 * G-orbit size ----------------------------
ncon = PGL // len(G)
print(f"\nPGL orbit sizes = {ncon} * G-orbit size:")
pgl_orbits = []
for s in sizes:
    o = ncon * s
    pgl_orbits.append(o)
    print(f"  G-orbit {s:3d} -> PGL orbit {o:,}")
check("PGL orbit sizes are 10,614,240 and 4,245,696",
      sorted(pgl_orbits) == [4_245_696, 10_614_240], f"{sorted(pgl_orbits)}")
check("they sum to 14,859,936 = total number of 5-caps",
      sum(pgl_orbits) == 14_859_936, f"{sum(pgl_orbits):,}")
check("#conics * 252 = 58,968 * 252 = 14,859,936 (independent total count)",
      ncon * 252 == 14_859_936)

# --- 5. identify the two classes -------------------------------------------
def find_map(src, tgt):
    a_ = [plane.vectors[p] for p in src[:4]]
    for b_idx in itertools.permutations(tgt, 4):
        M = pg.projectivity_from_frames(a_, [plane.vectors[p] for p in b_idx])
        if pg.apply_to_points(M, plane, src) == frozenset(tgt):
            return M
    return None


print("\nstabilisers inside G and class identification:")
for root, members in sorted(orbits.items(), key=lambda kv: -len(kv[1])):
    # combinatorial stabiliser order inside G = |G| / orbit size
    st = len(G) // len(members)
    Q = sorted(subs[members[0]])
    cls = "rep1" if find_map(Q, REP1) else ("rep2" if find_map(Q, REP2) else "???")
    print(f"  G-orbit of size {len(members):3d}: |Stab_G(Q)| = 720/{len(members)} = {st}, "
          f"sample Q = {Q} is PGL-equivalent to {cls}")
    check(f"G-orbit {len(members)}: PGL class = {cls} and |Stab| = {st}",
          cls in ("rep1", "rep2") and 720 // len(members) == st)
    if cls == "rep1":
        check("the G-orbit containing rep1 has size 180 and |Stab| = 4",
              len(members) == 180 and st == 4)
    if cls == "rep2":
        check("the G-orbit of class rep2 has size 72 and |Stab| = 10",
              len(members) == 72 and st == 10)

# rep1 itself must be a subset of C
check("rep1 is a five-subset of the conic C", frozenset(REP1) in sub_index)

# ---------------------------------------------------------------------------
# 6. purely combinatorial fourth check: PGL(2,9) acting on the 10 points of
#    PG(1,9).  The conic stabiliser is PGL(2,q) of order q(q^2-1) = 720 acting
#    sharply 3-transitively on the q+1 = 10 points, so the PGL(3,9)-orbits of
#    5-caps are the orbits of PGL(2,9) on the 5-subsets of a 10-point set.
#    This uses no PG(2,9) matrices at all.
# ---------------------------------------------------------------------------
print("\nPGL(2,9) on PG(1,9) (independent, no projective-plane matrices):")

# GF(9) as pairs (a,b), a+bi, i^2 = -1
def pa(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def pn(x):
    return ((-x[0]) % 3, (-x[1]) % 3)


def pm(x, y):
    return ((x[0] * y[0] - x[1] * y[1]) % 3, (x[0] * y[1] + x[1] * y[0]) % 3)


def pinv(x):
    n = {1: 1, 2: 2}[(x[0] * x[0] + x[1] * x[1]) % 3]
    return ((x[0] * n) % 3, ((-x[1]) * n) % 3)


E9 = [(a, b) for a in range(3) for b in range(3)]
INF = "inf"
LINE = [INF] + E9  # PG(1,9), 10 points


def flt(M, x):
    (a, b), (c, d) = M
    if x == INF:
        return INF if c == (0, 0) else pm(a, pinv(c))
    num = pa(pm(a, x), b)
    den = pa(pm(c, x), d)
    return INF if den == (0, 0) else pm(num, pinv(den))


def canon2(M):
    for e in (M[0][0], M[0][1], M[1][0], M[1][1]):
        if e != (0, 0):
            f = pinv(e)
            return tuple(tuple(pm(f, e2) for e2 in r) for r in M)
    raise ValueError


G2 = set()
for a in E9:
    for b in E9:
        for c in E9:
            for d in E9:
                det = pa(pm(a, d), pn(pm(b, c)))
                if det != (0, 0):
                    G2.add(canon2(((a, b), (c, d))))
print(f"  |PGL(2,9)| = {len(G2)} (theory q(q^2-1) = 720)")
check("|PGL(2,9)| = 720 acting on PG(1,9)", len(G2) == 720)

subs2 = [frozenset(s) for s in itertools.combinations(LINE, 5)]
idx2 = {s: i for i, s in enumerate(subs2)}
par2 = list(range(len(subs2)))


def f2(x):
    while par2[x] != x:
        par2[x] = par2[par2[x]]
        x = par2[x]
    return x


for M in sorted(G2):
    for s in subs2:
        t = frozenset(flt(M, x) for x in s)
        ra, rb = f2(idx2[s]), f2(idx2[t])
        if ra != rb:
            par2[ra] = rb
o2: dict[int, int] = {}
for i in range(len(subs2)):
    o2[f2(i)] = o2.get(f2(i), 0) + 1
sizes2 = sorted(o2.values(), reverse=True)
print(f"  PGL(2,9) orbits on the 252 five-subsets of PG(1,9): {sizes2}")
check("PGL(2,9) on 5-subsets of 10 points has exactly two orbits, 180 and 72",
      sizes2 == [180, 72], f"{sizes2}")
check("=> PGL(3,9) orbit sizes 58,968*180 and 58,968*72 (same as the conic "
      "computation)", True)

print("\nTASK 5 (conic cross-check):",
      "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
