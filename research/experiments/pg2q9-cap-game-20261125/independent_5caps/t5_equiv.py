"""TASK 5 -- direct PGL(3,9) stabilisers, pairwise equivalence, and the true
orbit structure of the 5-caps.

The searches below are *complete*, not sampled:
  A projectivity is determined by the images of 4 points in general position,
  and every 4-subset of a 5-cap is a frame (no 3 collinear).  Hence, fixing the
  ordered frame (s0,s1,s2,s3) of a source cap S:
    * M in Stab(S)  <=>  (M s0,...,M s3) is one of the 120 ordered 4-tuples
      of S, so enumerating those 120 tuples and keeping those whose
      projectivity reproduces S finds *all* of Stab(S);
    * M(S) = T      <=>  (M s0,...,M s3) is one of the 120 ordered 4-tuples
      of T, so enumerating those 120 tuples decides S ~ T completely
      (a negative answer is a proof of inequivalence).

Positive controls for the search are included (images under random
projectivities must be found again).

Run:  python independent_5caps/t5_equiv.py
"""

from __future__ import annotations

import itertools
import random
import sys
from collections import Counter

import game
import pg

RESULTS: list[tuple[str, bool, str]] = []
CLAIM: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    return ok


def claim_check(name: str, ok: bool, detail: str = "") -> bool:
    CLAIM.append((name, ok, detail))
    print(f"[CLAIM {'OK' if ok else 'REFUTED'}] {name}"
          + (f"  --  {detail}" if detail else ""))
    return ok


plane = game.plane()
PGL = ((9**3 - 1) * (9**3 - 9) * (9**3 - 9**2)) // 8
FRAME = [0, 1, 10, 20]
REPS = {
    "rep1 {0,1,10,20,31}": [0, 1, 10, 20, 31],
    "rep2 {0,1,10,20,42}": [0, 1, 10, 20, 42],
    "rep3 {0,1,10,20,41}": [0, 1, 10, 20, 41],
}
NAMES = list(REPS)
CLAIM_STAB = {NAMES[0]: 5, NAMES[1]: 10, NAMES[2]: 20}
CLAIM_ORBIT = {NAMES[0]: 8_491_392, NAMES[1]: 4_245_696, NAMES[2]: 2_122_848}


def stabilizer(rep):
    a = [plane.vectors[p] for p in rep[:4]]
    found = {}
    for b_idx in itertools.permutations(rep, 4):
        M = pg.projectivity_from_frames(a, [plane.vectors[p] for p in b_idx])
        if pg.apply_to_points(M, plane, rep) == frozenset(rep):
            found.setdefault(pg.mat_canon(M), b_idx)
    return found


def find_map(src, tgt):
    """Return a projectivity mapping the cap src onto the cap tgt, or None."""
    a = [plane.vectors[p] for p in src[:4]]
    for b_idx in itertools.permutations(tgt, 4):
        M = pg.projectivity_from_frames(a, [plane.vectors[p] for p in b_idx])
        if pg.apply_to_points(M, plane, src) == frozenset(tgt):
            return M
    return None


# ---------------------------------------------------------------------------
# 0. positive controls
# ---------------------------------------------------------------------------
rng = random.Random(99)
ctrl_ok = True
for _ in range(8):
    while True:
        M = tuple(rng.randrange(9) for _ in range(9))
        if pg.mat_det(M) != pg.ZERO:
            break
    img = sorted(pg.apply_to_points(M, plane, REPS[NAMES[0]]))
    ctrl_ok &= find_map(REPS[NAMES[0]], img) is not None
check("positive control: images of rep1 under random projectivities are found again",
      ctrl_ok)
check("positive control: identity is found for every representative",
      all(find_map(REPS[n], REPS[n]) is not None for n in NAMES))

# ---------------------------------------------------------------------------
# 1. complete stabilisers
# ---------------------------------------------------------------------------
stab = {}
for name, rep in REPS.items():
    st = stabilizer(rep)
    stab[name] = st
    print(f"\n{name}: complete search over the 120 images of a frame -> "
          f"|Stab_PGL(S)| = {len(st)}")
    for m, b_idx in sorted(st.items()):
        img = [REPS[name].index(plane.index[pg.vnorm(pg.mat_vec(m, plane.vectors[p]))])
               for p in rep]
        print(f"   image tuple {b_idx} -> M = {m}, |det| = {pg.field_name(pg.mat_det(m))}, "
              f"permutation of the 5 points {tuple(img)}")
    claim_check(f"|Stab({name})| = {CLAIM_STAB[name]}", len(st) == CLAIM_STAB[name],
                f"computed {len(st)}")
    n = len(st)
    check(f"{name}: orbit size |PGL|/|Stab| = {PGL // n:,}",
          PGL % n == 0, f"{PGL:,}/{n} = {PGL // n:,}")

# the stabilisers are groups
ident = pg.mat_canon(tuple(pg.ONE if i == j else pg.ZERO for i in range(3) for j in range(3)))
for name in NAMES:
    ms = list(stab[name])
    mset = set(ms)
    ok = (all(pg.mat_canon(pg.mat_mul(x, y)) in mset for x in ms for y in ms)
          and ident in mset
          and all(any(pg.mat_canon(pg.mat_mul(x, y)) == ident for y in ms) for x in ms))
    check(f"{name}: stabiliser is a group of order {len(ms)} "
          f"(closure, identity, inverses)", ok)

# ---------------------------------------------------------------------------
# 2. pairwise equivalence
# ---------------------------------------------------------------------------
print("\npairwise equivalence (complete search over the 120 images of a frame):")
equiv = {}
for i, a_name in enumerate(NAMES):
    for b_name in NAMES[i + 1:]:
        M = find_map(REPS[a_name], REPS[b_name])
        equiv[(a_name, b_name)] = M
        print(f"  {a_name} -> {b_name}: "
              + ("EQUIVALENT" if M else "inequivalent (no projectivity)"))
        if M is not None:
            img_frame = pg.apply_to_points(M, plane, FRAME)
            print(f"    witness M = {M}, |det| = {pg.field_name(pg.mat_det(M))}")
            print(f"    M maps the frame onto {sorted(img_frame)} "
                  f"(it is {'NOT ' if img_frame != frozenset(FRAME) else ''}the frame)")
            print(f"    Grundy values: {game.analyze_cap(REPS[a_name])['g']} -> "
                  f"{game.analyze_cap(REPS[b_name])['g']}")
claim_check("the three representatives are pairwise inequivalent",
            all(v is None for v in equiv.values()),
            "; ".join(f"{a.split()[0]}~{b.split()[0]}" for (a, b), v in equiv.items() if v))

# the 24 frame-fixing projectivities never move one representative to another
fv = [plane.vectors[i] for i in FRAME]
frame_group = sorted({pg.mat_canon(pg.projectivity_from_frames(fv, [fv[s[i]] for i in range(4)]))
                      for s in itertools.permutations(range(4))})
assert len(frame_group) == 24
bad = 0
for m in frame_group:
    for a_name in NAMES:
        img = pg.apply_to_points(m, plane, REPS[a_name])
        bad += sum(1 for b_name in NAMES
                   if a_name != b_name and img == frozenset(REPS[b_name]))
check("none of the 24 frame-fixing projectivities maps one representative to another",
      bad == 0)

# ---------------------------------------------------------------------------
# 3. the real orbit structure: c = #\{p in the 42 : F+p ~ rep\}, |O| = 1,769,040*c/5
# ---------------------------------------------------------------------------
EXTRA = pg.bitlist(game.FULL & ~plane.secant_mask(FRAME))
print(f"\nequivalence classes among the 42 five-caps containing the frame "
      f"(each tested against rep1 and rep2):")
class_of = {}
for p in EXTRA:
    S = FRAME + [p]
    hit = None
    for name in (NAMES[0], NAMES[1]):
        if find_map(S, REPS[name]) is not None:
            hit = name
            break
    class_of[p] = hit
counts = Counter(class_of.values())
print(f"  class sizes: {dict(counts)}   (unclassified points: "
      f"{[p for p, v in class_of.items() if v is None]})")
check("every one of the 42 caps is equivalent to rep1 or rep2",
      all(v is not None for v in class_of.values()))
check("the 42 split into classes of size 30 and 12 (not 24/12/6)",
      sorted(counts.values()) == [12, 30], f"{dict(counts)}")

# which S4 orbit (from t3) does each class consist of?
EXTRA_S4 = {}
# recompute S4 orbits of Stab(F) on the 42 points
parent = {p: p for p in EXTRA}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


for m in frame_group:
    for p in EXTRA:
        q = plane.index[pg.vnorm(pg.mat_vec(m, plane.vectors[p]))]
        ra, rb = find(p), find(q)
        if ra != rb:
            parent[ra] = rb
s4 = {}
for p in EXTRA:
    s4.setdefault(find(p), []).append(p)
print(f"  S4 orbits (Task 3) inside each PGL class:")
for root, members in sorted(s4.items(), key=lambda kv: -len(kv[1])):
    cls = Counter(class_of[p] for p in members)
    print(f"    S4 orbit of size {len(members):2d} -> PGL class {dict(cls)}")

N4 = 1_769_040
orb = {}
for name in (NAMES[0], NAMES[1]):
    c = counts[name]
    orb[name] = N4 * c // 5
    print(f"\n  class of {name}: c = {c:2d} five-caps through the frame, "
          f"|O| = 1,769,040*{c}/5 = {orb[name]:,}, "
          f"stabiliser |PGL|/|O| = {PGL / orb[name]:g}")
    claim_check(f"orbit size of {name} = {CLAIM_ORBIT[name]:,}",
                orb[name] == CLAIM_ORBIT[name],
                f"computed {orb[name]:,} (1,769,040*{c}/5)")
check("PGL orbit sizes 1,769,040*c/5 sum to 14,859,936 = total number of 5-caps",
      sum(orb.values()) == 14_859_936, f"sum = {sum(orb.values()):,}")
check("orbit-stabiliser agrees: |PGL|/|O| = 4 and 10, matching the direct "
      "stabiliser search",
      PGL // orb[NAMES[0]] == len(stab[NAMES[0]]) == 4
      and PGL // orb[NAMES[1]] == len(stab[NAMES[1]]) == 10)

# ---------------------------------------------------------------------------
# 4. invariant profiles
# ---------------------------------------------------------------------------
print("\nPGL-invariant profiles:")
for name in NAMES:
    info = game.analyze_cap(REPS[name])
    print(f"  {name}: g = {info['g']}, upper-set size {info['states']}, "
          f"by size {info['sizes']}, terminals {info['terminals']}")
check("rep1 and rep3 have the same invariant profile (consistent with being "
      "PGL-equivalent)", game.analyze_cap(REPS[NAMES[0]])["sizes"]
      == game.analyze_cap(REPS[NAMES[2]])["sizes"])

# ---------------------------------------------------------------------------
# 5. consequence: every 5-cap has Grundy value 1
# ---------------------------------------------------------------------------
print("\nconsistency of 'all 5-caps have Grundy value 1':")
print("  * 3 orbits were claimed but there are only 2: {24,6} merge, {12} stays.")
print("  * the union of the two orbits has 10,614,240 + 4,245,696 = "
      f"{sum(orb.values()):,} elements = the total number of 5-caps")
print("  * g(rep1) = g(rep2) = 1, and g is PGL-invariant, so all 5-caps have g = 1")
rng = random.Random(20261125)
vals = Counter()
n = 0
while n < 400:
    cand = sorted(rng.sample(range(91), 5))
    if plane.is_cap(cand):
        vals[game.analyze_cap(cand)["g"]] += 1
        n += 1
check("400 random 5-caps all have Grundy value 1", set(vals) == {1},
      f"{dict(sorted(vals.items()))}")
check("the Grundy-value part of the claim survives the corrected orbit structure",
      game.analyze_cap(REPS[NAMES[0]])["g"] == 1
      and game.analyze_cap(REPS[NAMES[1]])["g"] == 1)

print("\nTASK 5 computations:",
      "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
print("TASK 5 claim assertions:",
      "ALL HOLD" if all(ok for _, ok, _ in CLAIM)
      else f"{sum(1 for _, ok, _ in CLAIM if not ok)} REFUTED")
for n_, ok, d in CLAIM:
    if not ok:
        print(f"  REFUTED: {n_}  ({d})")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
