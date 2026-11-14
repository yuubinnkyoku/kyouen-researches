---
id: K0822
title: "Row-mirror-canonical deficiency class count for w-row class-split sweeps: C(w) = 2^(w-1) + 2^(ceil(w/2)-1) - 1 (19 at w=5, 35 at w=6, 71 at w=7, 135 at w=8)"
kind: proposition
status: proved
topics: [rectangles, maximal-safe, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "the --class=D row constraints are unit clauses on the K0810 rowGe/row-chain core; the objects counted (non-empty exact deficiency sets of rows, modulo the row mirror) are defined by that machinery (sat3.js)"
- type: generalizes
  target: K0816
  note: "the 19 row-mirror-canonical classes swept at 5x20 equal C(5) = 19 (the first recorded use of the w=5 count)"
- type: generalizes
  target: K0818
  note: "the 35 row-mirror-canonical classes swept at 6x19 equal C(6) = 35 (K0819 at 6x20 and K0821 at 5x21 reuse the same counts)"
artifacts:
- path: research/experiments/row-mirror-class-count-20261114/report.md
  role: proof
  note: "Burnside proof (fixed subsets under the mirror: 2^ceil(w/2) including empty), machinery identification, cross-checks against the recorded 19/35-class sweeps, w=7 prediction"
- path: research/experiments/row-mirror-class-count-20261114/scripts/orbit_count.js
  role: source
  note: "standalone brute-force orbit counter vs the closed form (no dependencies)"
- path: research/experiments/row-mirror-class-count-20261114/output/counts.json
  role: data
  note: "w=1..14 orbits vs formula, all match (19 at w=5, 35 at w=6, 71 at w=7, 135 at w=8); sandbox-computed during the bash outage, reproducible by rerunning the script"
- path: research/experiments/six-row-q8-m20-class-split-20261114/scripts/sat3.js
  role: solver
  note: "the class-split encoder whose --class=D semantics (rows in D <= q-2 stones, rows outside exactly q-1) and mirror-canonical sweep protocol define the classes counted"
scope: "pure combinatorial identity proved for all w >= 1; the identification with the class-split machinery is definitional (sat3.js --class semantics plus mirror isometry), not a claim about census/solver correctness"
evidence: "mathematical-proof (Burnside lemma over the two-element mirror group) + independent brute-force orbit enumeration w=1..14 (all match)"
---

# Row-mirror-canonical deficiency class count — C(w) = 2^(w-1) + 2^(ceil(w/2)-1) - 1

## Claim

For every w >= 1, the non-empty subsets of the row set {0, ..., w-1} fall into exactly

    C(w) = 2^(w-1) + 2^(ceil(w/2)-1) - 1 = (2^w + 2^ceil(w/2) - 2) / 2

orbits under the row mirror V : y -> w-1-y. Values: C(1)=1, C(2)=2, C(3)=5, C(4)=9,
C(5)=19, C(6)=35, C(7)=71, C(8)=135, C(9)=271, C(10)=527.

In the class-split machinery (sat3.js --class=D): D is the exact set of deficient rows
(rows in D hold at most q-2 stones via not-rowGe[y]; rows outside D hold exactly q-1,
the safety cap of a row line when m >= q), D is non-empty for a deficient configuration,
and the board reflection (x, y) -> (x, w-1-y) is an isometry of the integer grid mapping
a class-D configuration to a class-V(D) configuration. Hence SAT(D) <=> SAT(V(D)), and a
sweep of one canonical representative per orbit is an exhaustive cover. C(w) is therefore
the number of canonical classes a complete w-row class-split sweep must cover:
19 at w=5 (K0816 5x20, K0821 5x21), 35 at w=6 (K0818 6x19, K0819 6x20), and 71 for the
first 7-row sweep (135 at w=8).

## Proof

Let G = {id, V} act on the power set X of {0, ..., w-1}. A subset is fixed by V iff
membership is constant on each mirror pair {i, w-1-i} (floor(w/2) pairs) and on the middle
row floor(w/2) when w is odd — ceil(w/2) independent binary choices — so |Fix(V)| =
2^ceil(w/2) (including the empty set) and |Fix(id)| = 2^w. By Burnside's lemma the number
of orbits on X is (2^w + 2^ceil(w/2)) / 2 = 2^(w-1) + 2^(ceil(w/2)-1). The empty set is a
fixed singleton orbit, so the non-empty orbits number 2^(w-1) + 2^(ceil(w/2)-1) - 1. QED.

## Cross-checks

- Brute-force orbit enumeration, w = 1..14 (scripts/orbit_count.js; output/counts.json):
  orbits equal the formula for every w.
- Recorded sweeps use exactly these counts: 19 canonical classes at w=5, 35 at w=6.

## Scope / limits

- Purely combinatorial; no statement about census, encoding or solver correctness
  (K0810 and the sweep items own those).
- The class does not distinguish deficiency depth: a deficient row may hold 0..q-2 stones;
  the k x minpos decompositions (K0816/K0821) split classes further, orthogonally to this
  count.
- The all-full class D = empty is not a deficient configuration and is excluded, matching
  the sweep items' convention.
