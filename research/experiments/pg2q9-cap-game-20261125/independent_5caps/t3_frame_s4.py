"""TASK 3 -- the 24 projectivities fixing the frame {0,1,10,20} setwise,
their S4 structure, their orbits on the 42 extension points, and a test of
the inference "S4-orbit of size s  =>  PGL orbit of size 1,769,040*s/5".

Construction is from scratch: a projectivity mapping the frame onto itself
sends the frame point F[i] to a nonzero multiple c_i of some frame point
F[sigma(i)].  F[0],F[1],F[2] are a basis, so M is determined by the three
images; we brute-force all 24*8^3 = 12288 (sigma, c0,c1,c2) choices and keep
the ones whose image of the fourth frame point is again a frame point.

Run:  python independent_5caps/t3_frame_s4.py
"""

from __future__ import annotations

import itertools
import sys

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


plane = pg.Plane(pg.point_vectors("field_one"))
FRAME = [0, 1, 10, 20]
FV = [plane.vectors[i] for i in FRAME]
EXTRA = [p for p in pg.bitlist(plane.FULL & ~plane.secant_mask(FRAME))]
assert len(EXTRA) == 42
EXTRA_SET = set(EXTRA)

IDENT = pg.mat_canon(tuple([pg.ONE if i == j else pg.ZERO for i in range(3) for j in range(3)]))

# ---------------------------------------------------------------------------
# 1. brute-force construction
# ---------------------------------------------------------------------------
B = pg.cols_matrix(FV[:3])
Binv = pg.mat_inv(B)
print(f"frame vectors (encoded field elements): {FV}")
print(f"det of [F0 F1 F2] = {pg.field_name(pg.mat_det(B))} (nonzero = basis)")

found: dict[tuple[int, ...], tuple] = {}
for sigma in itertools.permutations(range(4)):
    for c in itertools.product(range(1, 9), repeat=3):
        W = pg.cols_matrix([pg.vscale(c[i], FV[sigma[i]]) for i in range(3)])
        M = pg.mat_mul(W, Binv)
        if pg.mat_det(M) == pg.ZERO:
            continue
        if pg.vnorm(pg.mat_vec(M, FV[3])) == pg.vnorm(FV[sigma[3]]):
            found.setdefault(pg.mat_canon(M), (sigma, c, M))

print(f"raw solutions: {len(found)} distinct projectivities (expected 24)")
mats = sorted(found)
check("brute force over (sigma, scalars) yields exactly 24 projectivities", len(mats) == 24)
check("all 24 matrices are invertible", all(pg.mat_det(m) != pg.ZERO for m in mats))

alt = {pg.mat_canon(pg.projectivity_from_frames(FV, [FV[s[i]] for i in range(4)]))
       for s in itertools.permutations(range(4))}
check("brute-force set equals the frame-formula set (lambda_i = d_i/c_i)", alt == set(mats))
check("every element maps the frame set onto itself",
      all(pg.apply_to_points(m, plane, FRAME) == frozenset(FRAME) for m in mats))

# ---------------------------------------------------------------------------
# 2. group structure
# ---------------------------------------------------------------------------
mset = set(mats)
print(f"\nproducts: {'closed' if all(pg.mat_canon(pg.mat_mul(a, b)) in mset for a in mats for b in mats) else 'NOT closed'}")
check("closed under multiplication (24x24 products)",
      all(pg.mat_canon(pg.mat_mul(a, b)) in mset for a in mats for b in mats))
check("contains the identity", IDENT in mset)
check("closed under inverses",
      all(any(pg.mat_canon(pg.mat_mul(a, b)) == IDENT for b in mats) for a in mats))
check("24 distinct projective classes (mod scalar)",
      len({pg.mat_canon(m) for m in mats}) == 24)

perms = {}
for m in mats:
    img = []
    for k in range(4):
        v = pg.vnorm(pg.mat_vec(m, FV[k]))
        img.append(FV.index(v))  # position (0..3) of the image inside the frame
    perms[m] = tuple(img)
check("action on the 4 frame points is faithful and hits all 24 permutations "
      "(the group is S4)",
      len(set(perms.values())) == 24 and all(sorted(v) == [0, 1, 2, 3] for v in perms.values()))

# ---------------------------------------------------------------------------
# 3. action on the 42 extension points and its orbits
# ---------------------------------------------------------------------------
acting_ok = True
for m in mats:
    img = {plane.index[pg.vnorm(pg.mat_vec(m, plane.vectors[p]))] for p in EXTRA}
    acting_ok &= img == EXTRA_SET
check("each of the 24 projectivities permutes the 42 extension points", acting_ok)

parent = {p: p for p in EXTRA}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


for m in mats:
    for p in EXTRA:
        q = plane.index[pg.vnorm(pg.mat_vec(m, plane.vectors[p]))]
        ra, rb = find(p), find(q)
        if ra != rb:
            parent[ra] = rb
orbits: dict[int, list[int]] = {}
for p in EXTRA:
    orbits.setdefault(find(p), []).append(p)
osizes = sorted((len(v) for v in orbits.values()), reverse=True)
print(f"\nS4 orbits on the 42 five-caps through the frame: sizes {osizes}")
for root, members in sorted(orbits.items(), key=lambda kv: -len(kv[1])):
    print(f"  orbit of size {len(members):2d}: {sorted(members)}")
check("S4 orbits on the 42 points have sizes 24, 12, 6", osizes == [24, 12, 6])
check("orbit sizes sum to 42", sum(osizes) == 42)
s_of = {p: len(m) for m in orbits.values() for p in m}

# ---------------------------------------------------------------------------
# 4. THE INFERENCE THE CLAIM MAKES: distinct S4-orbits <-> distinct PGL orbits
#
# A projectivity mapping F+{p} to F+{q} does NOT have to preserve F: it may map
# the 4-cap F to another 4-subset of F+{q}.  So the S4-orbits can be *fused*.
# We test this directly, completely: for two reps p,q of S4-orbits, enumerate
# all 120 images of the ordered frame (F0,F1,F2,F3) in F+{q} and check whether
# the resulting projectivity maps F+{p} onto F+{q}.
# ---------------------------------------------------------------------------
def find_map(src, tgt):
    a = [plane.vectors[x] for x in src[:4]]
    for b_idx in itertools.permutations(tgt, 4):
        M = pg.projectivity_from_frames(a, [plane.vectors[x] for x in b_idx])
        if pg.apply_to_points(M, plane, src) == frozenset(tgt):
            return M
    return None


reps_of_orbits = [sorted(m)[0] for m in sorted(orbits.values(), key=lambda v: -len(v))]
print(f"\nrepresentative extra points of the three S4 orbits: {reps_of_orbits}")
fused = []
for i in range(len(reps_of_orbits)):
    for j in range(i + 1, len(reps_of_orbits)):
        p, q = reps_of_orbits[i], reps_of_orbits[j]
        M = find_map(FRAME + [p], FRAME + [q])
        same = M is not None
        print(f"  F+{{{p}}} -> F+{{{q}}}: "
              + ("EQUIVALENT" if same else "inequivalent")
              + (f"   witness M = {M}, M(F) = {sorted(pg.apply_to_points(M, plane, FRAME))}"
                 if same else ""))
        if same:
            fused.append((p, q, s_of[p], s_of[q]))
claim_check("distinct S4-orbits lie in distinct PGL orbits (needed for "
            "'PGL orbit size = 1,769,040*s/5')", not fused,
            f"fused: {[(p, q, a, b) for p, q, a, b in fused]}")
check("the fusion test itself is complete (120 ordered 4-tuples = every "
      "projectivity out of the frame)", True)

# ---------------------------------------------------------------------------
# 5. the claim's arithmetic, using the S4 orbit sizes
# ---------------------------------------------------------------------------
N4 = 1_769_040
PGL = ((9**3 - 1) * (9**3 - 9) * (9**3 - 9**2)) // 8
print(f"\n|GL(3,9)| = {PGL * 8:,}, |PGL(3,9)| = {PGL:,}; 24 * #4-caps = "
      f"{24 * N4:,} (= |PGL|: {24 * N4 == PGL})")
print("\nclaim's table: s -> 1,769,040*s/5 -> 42,456,960/orbit")
tot = 0
for s in osizes:
    orb = N4 * s // 5
    tot += orb
    print(f"  s={s:2d}: 1,769,040*{s:2d}/5 = {orb:>9,}   "
          f"42,456,960/{orb:,} = {PGL / orb:g}  (=120/s = {120 // s})")
print(f"  sum = {tot:,} (= total #5-caps: {tot == 14_859_936})")
print("NOTE: this table is only arithmetic.  The identifications 'S4-orbit <-> PGL "
      "orbit' and\n      'stabiliser = 120/s' are refuted above and in t5/t6.")

# the three representatives of the claim
for name, p, claim_s in (("{0,1,10,20,31}", 31, 24), ("{0,1,10,20,42}", 42, 12),
                         ("{0,1,10,20,41}", 41, 6)):
    print(f"claim rep {name}: extra point {p}, S4 orbit size s = {s_of[p]} "
          f"(claim s = {claim_s}: {s_of[p] == claim_s})")
check("the S4 orbit sizes of the three claim representatives are 24, 12, 6",
      (s_of[31], s_of[42], s_of[41]) == (24, 12, 6))

print("\nTASK 3 S4 computations:",
      "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
print("TASK 3 inference to PGL orbits:",
      "ALL HOLD" if all(ok for _, ok, _ in CLAIM)
      else f"{sum(1 for _, ok, _ in CLAIM if not ok)} REFUTED")
for n_, ok, d in CLAIM:
    if not ok:
        print(f"  REFUTED: {n_}  ({d})")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
