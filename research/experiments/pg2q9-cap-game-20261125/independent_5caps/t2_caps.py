"""TASK 2 -- the 4-cap frame, its 42 five-cap extensions, the three
representatives, and the global counts of 4- and 5-caps.

Run:  python independent_5caps/t2_caps.py
"""

from __future__ import annotations

import itertools
import sys

import pg

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    return ok


plane = pg.Plane(pg.point_vectors("field_one"))
FRAME = [0, 1, 10, 20]
REPS = {
    "rep1 {0,1,10,20,31}": [0, 1, 10, 20, 31],
    "rep2 {0,1,10,20,42}": [0, 1, 10, 20, 42],
    "rep3 {0,1,10,20,41}": [0, 1, 10, 20, 41],
}

# ---------------------------------------------------------------- the frame
print("frame points (encoded field coords):")
for p in FRAME:
    print(f"  {p:2d} -> {plane.vectors[p]}   field {tuple(pg.field_name(c) for c in plane.vectors[p])}")

triples = list(itertools.combinations(FRAME, 3))
collinear = []
for t in triples:
    l = pg.vnorm(pg.vcross(plane.vectors[t[0]], plane.vectors[t[1]]))
    on = pg.vdot(l, plane.vectors[t[2]]) == pg.ZERO
    if on:
        collinear.append(t)
    print(f"  triple {t}: {'COLLINEAR' if on else 'not collinear'}")
check("frame {0,1,10,20} is a 4-cap (no 3 of the 4 collinear)",
      plane.is_cap(FRAME) and not collinear)
check("frame is a proper frame: every 3 of the 4 points span a basis",
      all(pg.vindependent([plane.vectors[i] for i in t]) for t in triples))

# ------------------------------------------- the 42 five-caps through it
secant = [plane.line_mask((a, b)) for a, b in itertools.combinations(FRAME, 2)]
union = 0
for m in secant:
    union |= m
print(f"\n6 secant lines of the frame: {len(secant)} distinct, each with "
      f"{[m.bit_count() for m in secant]} points")
print(f"union of the 6 secant lines: {union.bit_count()} points "
      f"({sorted(pg.bitlist(union))})")
ext = [p for p in pg.bitlist(plane.FULL & ~union)]
print(f"extension points p with {FRAME} + p a 5-cap: {len(ext)}")
print(f"  {ext}")
check("exactly 42 points p extend the frame to a 5-cap", len(ext) == 42)
check("all 42 extensions really give 5-caps (independent is_cap check)",
      all(plane.is_cap(FRAME + [p]) for p in ext))
check("union of the 6 secant lines has 49 points and no extension is on a secant",
      union.bit_count() == 49 and not any((union >> p) & 1 for p in ext))
print(f"5-caps through the frame: {[(FRAME + [p]) for p in ext]}")

# ------------------------------------------------------- the representatives
for name, rep in REPS.items():
    ok = plane.is_cap(rep) and len(set(rep)) == 5
    print(f"\n{name}: {rep}")
    print(f"  coords: {[plane.vectors[p] for p in rep]}")
    ext_of_rep = plane.extensions(rep)
    print(f"  is a 5-cap: {ok}; has {len(ext_of_rep)} extension points "
          f"(6-caps through it)")
    check(f"{name} is a 5-cap", ok)
    check(f"{name} contains the frame", set(FRAME) <= set(rep))
    check(f"{name} is one of the 42 extensions of the frame", rep[-1] in ext)

# ------------------------------------------------------------ global counts
print("\n--- exhaustive counts (no group theory used) ---")
n_triples = 91 * 90 * 89 // 6
coll = 0
for line in plane.line_masks:
    coll += len(pg.bitlist(line)) * (len(pg.bitlist(line)) - 1) * (len(pg.bitlist(line)) - 2) // 6
print(f"all 3-subsets: {n_triples}; collinear triples: {coll} = 91 * C(10,3) = {91 * 120}")
check("collinear triples counted two ways agree", coll == 91 * 120)
n_3cap = n_triples - coll
print(f"3-caps (non-collinear triples): {n_3cap}")
check("3-cap count = C(91,3) - 91*C(10,3)", n_3cap == 110_565)

# every 3-cap has exactly 64 extensions (3 lines, 27 points covered)
hist3: dict[int, int] = {}
for t in itertools.combinations(range(91), 3):
    if plane.is_cap(t):
        m = 0
        for a, b in itertools.combinations(t, 2):
            m |= plane.line_mask((a, b))
        hist3[m.bit_count()] = hist3.get(m.bit_count(), 0) + 1
print(f"distribution of |covered points| over all 3-caps: {hist3}")
check("every 3-cap covers exactly 27 points and has 64 extensions",
      set(hist3) == {27} and hist3[27] == n_3cap)
n4 = n_3cap * 64 // 4
print(f"#4-caps by double counting: {n_3cap}*64/4 = {n4}")
check("#4-caps = 1,769,040 (triple double count)", n4 == 1_769_040)

# exhaustive enumeration of all 4-caps + their extension counts
FULL = plane.FULL
LM = [[0] * 91 for _ in range(91)]
for a in range(91):
    for b in range(91):
        if a != b:
            LM[a][b] = plane.line_masks[plane.pair_line[a][b]]
count4 = 0
hist4: dict[int, int] = {}
for a in range(91):
    for b in range(a + 1, 91):
        mab = LM[a][b]
        for c in range(b + 1, 91):
            if (mab >> c) & 1:
                continue
            mac = LM[a][c]
            mbc = LM[b][c]
            blocked3 = mab | mac | mbc
            cand = FULL & ~blocked3 & ~((1 << (c + 1)) - 1)
            while cand:
                low = cand & -cand
                d = low.bit_length() - 1
                cand ^= low
                blocked6 = blocked3 | LM[a][d] | LM[b][d] | LM[c][d]
                count4 += 1
                ne = (FULL & ~blocked6).bit_count()
                hist4[ne] = hist4.get(ne, 0) + 1
print(f"exhaustive enumeration of 4-caps: {count4}")
print(f"distribution of extension counts over all 4-caps: {hist4}")
check("exhaustive #4-caps equals 1,769,040", count4 == 1_769_040)
check("every 4-cap has exactly 42 extension points", set(hist4) == {42})
n5 = sum(k * v for k, v in hist4.items()) // 5
print(f"#5-caps by double counting: {sum(k*v for k,v in hist4.items())}/5 = {n5}")
check("#5-caps = 1,769,040*42/5 = 14,859,936", n5 == 14_859_936)
check("claim arithmetic: 1,769,040*42 divisible by 5 and equal to 14,859,936",
      1_769_040 * 42 % 5 == 0 and 1_769_040 * 42 // 5 == 14_859_936)

print("\nTASK 2:", "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
