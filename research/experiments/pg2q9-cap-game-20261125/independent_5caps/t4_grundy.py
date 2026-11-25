"""TASK 4 -- independent Grundy values of the three representatives.

Game (normal play, impartial): a position is a cap S; a move adds a point p
for which S + p is still a cap; the player with no move loses.  Hence

    g(S) = mex{ g(S + p) : p legal },     g(S) = 0 if S is maximal.

Method (two independent implementations, plus a certificate), see game.py:
  (1) memoised top-down recursion;
  (2) BFS enumeration of the whole upper set (all caps containing S) plus a
      bottom-up DP in decreasing size order;
  (3) a local certificate: for every state of the upper set we check
      g(S) = mex{g(child)} and g(S) = 0 iff S has no child.  On a finite,
      child-closed acyclic set such a labelling is *the* Grundy function
      (induction on size), so (3) makes the values rigorous rather than
      merely "computed by my recursion".

Note: 10 = q+1 is the largest cap size in PG(2,9), so the tree from a 5-cap
has depth <= 5 and the upper set is small (128-132 positions).

Run:  python independent_5caps/t4_grundy.py
"""

from __future__ import annotations

import random
import sys
from collections import Counter

import game
import pg

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    return ok


plane = game.plane()
FRAME = [0, 1, 10, 20]
REPS = {
    "rep1 {0,1,10,20,31}": [0, 1, 10, 20, 31],
    "rep2 {0,1,10,20,42}": [0, 1, 10, 20, 42],
    "rep3 {0,1,10,20,41}": [0, 1, 10, 20, 41],
}

gvals = {}
profiles = {}
for name, rep in REPS.items():
    info = game.analyze_cap(rep, want_topdown=True)
    gvals[name] = info["g"]
    profiles[name] = info
    print(f"\n{name}: points {rep}")
    print(f"  legal moves from the 5-cap: {info['root_children']}")
    print(f"  upper set: {info['states']} caps -- by size {info['sizes']}")
    print(f"  #caps strictly containing it: {info['strict']}")
    print(f"  terminal positions reachable, by size: {info['terminals']} "
          f"(total {sum(info['terminals'].values())})")
    print(f"  Grundy values of its children (6-caps): {info['child_vals']}")
    print(f"  Grundy value g(rep) = {info['g']}   (local mex certificate: {info['cert']})")
    check(f"{name} has Grundy value 1", info["g"] == 1, f"computed g = {info['g']}")
    check(f"{name}: local mex certificate holds on the whole upper set", info["cert"])
    check(f"{name}: upper set is nonempty and finite", info["states"] > 1)

# --- the frame itself (4-cap) -------------------------------------------------
info_f = game.analyze_cap(FRAME, want_topdown=True)
print(f"\nframe [0,1,10,20] (4-cap): g = {info_f['g']}, upper set {info_f['states']} caps, "
      f"by size {info_f['sizes']}, terminals {info_f['terminals']}")
print(f"  children (5-caps) Grundy distribution: {info_f['child_vals']}")
check("frame (4-cap) has Grundy value 0 (mex{1})",
      info_f["g"] == 0 and set(info_f["child_vals"]) == {1})

# --- all 42 five-caps through the frame --------------------------------------
EXTRA = pg.bitlist(game.FULL & ~plane.secant_mask(FRAME))
vals42 = {p: game.analyze_cap(FRAME + [p])["g"] for p in EXTRA}
print(f"\nGrundy values of all 42 five-caps through the frame: "
      f"{dict(Counter(vals42.values()))}")
check("all 42 five-caps through the frame have Grundy value 1",
      set(vals42.values()) == {1})

# --- PGL invariance: g(M S) = g(S) for the 24 frame stabiliser ---------------
import itertools

FV = [plane.vectors[i] for i in FRAME]
mats = sorted({pg.mat_canon(pg.projectivity_from_frames(FV, [FV[s[i]] for i in range(4)]))
               for s in itertools.permutations(range(4))})
assert len(mats) == 24
inv_ok = True
for name, rep in REPS.items():
    for m in mats:
        img = sorted(plane.index[pg.vnorm(pg.mat_vec(m, plane.vectors[p]))] for p in rep)
        if game.analyze_cap(img)["g"] != gvals[name]:
            inv_ok = False
print(f"\nPGL invariance: applied all 24 frame-fixing projectivities to each "
      f"representative ({3 * 24} images)")
check("g is invariant under the 24 frame-fixing projectivities", inv_ok)

# --- random 5-caps: empirical check of 'all 5-caps have Grundy 1' ------------
rng = random.Random(20261125)
vals_rand: Counter = Counter()
n_tested = 0
tries = 0
while n_tested < 400 and tries < 20000:
    tries += 1
    cand = sorted(rng.sample(range(91), 5))
    if not plane.is_cap(cand):
        continue
    vals_rand[game.analyze_cap(cand)["g"]] += 1
    n_tested += 1
print(f"\nrandom 5-caps tested: {n_tested} -> Grundy values {dict(sorted(vals_rand.items()))}")
check("400 random 5-caps all have Grundy value 1",
      n_tested == 400 and set(vals_rand) == {1},
      f"{n_tested} caps, values {dict(sorted(vals_rand.items()))}")

print("\nTASK 4:", "PASS" if all(ok for _, ok, _ in RESULTS) else "FAIL")
sys.exit(0 if all(ok for _, ok, _ in RESULTS) else 1)
