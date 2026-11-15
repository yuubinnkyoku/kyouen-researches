# 5x22 q=6 row-deficient maximal witness — discovery and verification report

Date: 2026-11-15 (UTC). Fast lane. Knowledge item: K0852 (number to be
re-confirmed at integration). This resolves the 5x22 frontier of the (5,6)
family that the five-row-q6-m22-class-split-20261114 sweep left INDET.

## Claim

1. On the 5x22 integer grid (q=6), there exists a **24-stone row-deficient
   maximal safe configuration**: the class-split instance with deficiency
   class {0} (row 0 at most 4 stones, rows 1-4 exactly 5 — safety caps every
   row at 5 since a row is a line of length 22 >= q), safety <= 5 stones per
   census curve, maximality (every empty cell covered by a >=5-stone curve),
   refined by krow=0:4 (row 0 exactly 4 stones) and minpos=0 (leftmost stone
   of row 0 at column 0), is **SAT**:
   kissat 4.0.4, 3,126,820 conflicts, 194.87 s process-time (CNF 20,948 vars /
   73,232 clauses).
2. Witness (24 stones, rows (4,5,5,5,5)):
   (0,0),(11,0),(15,0),(20,0),(3,1),(6,1),(10,1),(15,1),(18,1),
   (3,2),(6,2),(8,2),(10,2),(15,2),(4,3),(6,3),(9,3),(16,3),(17,3),
   (7,4),(9,4),(11,4),(12,4),(14,4).
3. Verification (three independent checks):
   - sat3.js model decode + sat.js census-free `verifyConfig`: PASS
     (safe + maximal, size 24, rows (4,5,5,5,5), minRow 4).
   - Independent pure-TypeScript reimplementation (own census: lines through
     stone pairs, circles through stone triples, canonical integer
     coefficients; no sat.js code shared): safe — 0 unsafe curves among the
     1,824 distinct stone-curves, maximum 5 stones on any curve; maximal —
     all 86 empty cells blocked by some >=5-stone curve. PASS.
   - krow/minpos pins verified on the witness (row 0 exactly 4 stones,
     leftmost stone column 0).
4. Positive control: 5x21 q=6 class {0} SAT — 330,743 conflicts, bit-exact
   with the five-row-q6-m22-class-split-20261114 control record (same CNF
   generation path, same solver); decoded 24 stones rows (4,5,5,5,5),
   verifyConfig PASS. The control and witness SAT runs are deterministic
   and were reproduced bit-exactly after a full environment reset (see
   Reproducibility).
5. Consequence: the (5,6) deficient-maximal witness band extends from
   m = 15..21 to **m = 15..22** (24-stone witnesses now known at 5x15..5x22;
   5x15..5x21 previously: K0723, K0810, K0811, K0815). Therefore
   **M_{5,6} >= 23**, and with the substitution upper bound 249 (K0318),
   **M_{5,6} in [23, 249]**. The frontier moves to 5x23.

## m=23 honest negatives (INDET, not absence)

- 5x23 class {0} krow=0:4 minpos=0: INDET, kissat --time=220,
  3,343,593 conflicts / 219.54 s.
- 5x23 class {0} krow=0:4 minpos=1: INDET, kissat --time=220,
  3,369,340 conflicts / 219.56 s.
- Time-cut INDET conflict counts follow the same deterministic search
  trajectory but are not bit-exact across runs (the cut point depends on
  wall clock). The published raw logs are the fresh post-reset runs;
  pre-reset values on the same trajectory were 3,347,880 / 3,268,987.
- Addendum batch (same session, same protocol): class {0} k4p2 INDET
  3,686,541 conflicts / 219.53 s (the hardest m=23 sub-instance so far)
  and k3p0 (krow=0:3, minpos=0) INDET 3,276,028 conflicts / 219.57 s.
  Remaining m=23 sub-instances (k4p3..p11, k3p1.., k2/k1/k0, other
  classes) are unprobed.

## Witness-neighborhood surgery (complete enumerations, negative)

Transplanting the m=22 witness unchanged onto 5x23 (all stones lie in
columns 0..20): safe (0 unsafe curves — any curve with >= 6 seed points has
>= 3 points in the 5x22 sub-board and was already enumerated and safe
there), non-maximal with **exactly one unblocked cell U = (22,0)**. The 32
census curves through U (T-curves) carry seed stone counts 4, 3, 3, then
2, 2, 2 and lower.

- **1-stone surgery** (remove 1 of 24, add 1; sound restriction: the added
  stone must lie on a T-curve (58 seed-empty candidate cells) or be U
  itself, since U must end blocked or occupied and a single off-T add
  cannot raise any T-curve to 5): **1,416 configurations, 0 witnesses.**
- **2-stone surgery** (remove 2 of 24, add 2; sound restriction: U blocked
  or occupied requires some T-curve to reach 5; with at most 2 adds and
  removals only decreasing counts, a T-curve with seed count <= 2 cannot
  reach 5, so at least one added stone lies on a heavy T-curve (seed >= 3,
  25 seed-empty candidate cells including U) or at U; the other add is any
  vacant cell; add-at-vacated-position degeneracies reduce to the complete
  1-stone enumeration or to no-ops): **552,000 configurations, 0 witnesses.**
- Conclusion: any 24-stone row-deficient maximal configuration on 5x23 (if
  one exists) differs from this seed by **more than 2 stone-moves
  (symmetric difference > 4 cells)**. This is a statement about this seed's
  neighborhood only; it is NOT an m=23 nonexistence claim, and the m=23
  SAT question remains open (INDET probes above).

## Reproducibility (environment-reset recovery)

The witness was discovered pre-reset; a full execution-environment reset
then destroyed all local artifacts. Recovery protocol (now exercised
twice in this lane family, cf. K0837/K0838/K0842/K0846):

1. Scripts restored from main: sat.js / sat2.js / sat3.js byte-identical,
   git blob shas verified (6c3262d6 / edfae1d2 / 6dfa7db3).
2. kissat 4.0.4 re-downloaded from the official rel-4.0.4 GitHub asset;
   binary md5 verified (3a5eba830aa6008a604fcc9bbe99a325).
3. All four CNFs regenerated and re-run deterministically: the control
   (330,743) and the witness (3,126,820) reproduced **bit-exactly**,
   including an identical witness stone set; the two INDET runs follow the
   same trajectory cut at the 220 s wall clock (fresh values published).

## Scope

Finite machine verification: the witness existence is a fully verified
finite fact (dual-verified by two independent census implementations plus
the encoder's own decode/verify path), but the band statement
M_{5,6} in [23, 249] is a bounds statement, not a threshold determination;
5x23 and beyond remain open. Surgery negatives are neighborhood statements
about one seed. The 11x11 empty board, two-stone root {49,60}/{59,60},
S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
