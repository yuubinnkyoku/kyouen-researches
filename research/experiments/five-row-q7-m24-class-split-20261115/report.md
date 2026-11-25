# 5x24 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

Date: 2026-11-15. Fast lane, successor of K0835 (5x23). Extends the (5,7) witness-free
sweep one width on the same class-split SAT machinery (K0816/K0821/K0834/K0835 protocol).

## Claim

1. On the 5x24 integer grid (q=7), for every one of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under
   y -> 4-y), the class-split SAT instance — rows in D hold at most 5 stones (unit ¬rowGe[y]),
   rows outside D hold exactly 6 (unit rowGe[y]; safety caps every row at 6 since a row is
   a line of length 24 ≥ q), safety ≤ 6 stones per census curve, maximality (every empty
   cell covered by a ≥6-stone curve) — has **no solution**:
   - 17/19 classes directly **UNSAT** (kissat 4.0.4, exit 20; hardest {0,1}: 707,981
     conflicts / 23.7 s; {2}: 259,828; direct total 4,160,006 conflicts — the
     m21→m22→m23→m24 difficulty trend is now clearly decreasing: 5,256,816 →
     4,673,619 → 4,160,006).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834/K0835 protocol): k = 0..4 (exact deficient-row stone count, 5
     instances each; hardest {0} k=4: 989,392 / {1} k=4: 847,693) and k = 5 ×
     minpos = 0..11 (12 instances each; the sound bound is floor((m−1)/2) = 11 at
     m = 24: x1 ≥ 12 forces the mirror's leftmost column 23−x5 ≤ 11). All 34
     sub-instances **UNSAT** (hardest {1} k=5 mp=0: 2,282,668 conflicts / 92.83 s;
     {0} k=5 mp=0: 1,745,942 / 74.97 s — both below their m=23 counterparts).
   - Total conflicts across the 51 deciding instances: **17,349,736** (17 direct:
     4,160,006; 34 decomposition: 13,189,730); the two lex=H cross-checks add 851,128
     (records.jsonl total 18,543,998). No SAT, no INDET among the deciding instances.
2. Coverage: the exact deficiency set D = {rows with ≤ q-2 stones} is non-empty for every
   deficient maximal safe configuration and the exact-D instances partition them
   (K0818/K0816 class logic, brute-force-validated on small boards in K0818); the
   k×minpos decomposition is exhaustive: k = 0..5 partitions the deficient row's stone
   count, and for k = 5 the minpos split pins the **leftmost stone of the first deficient
   row at column exactly P**; every configuration or its column mirror has leftmost stone
   column ≤ 11 at m = 24 (if x1 ≥ 12 then the mirror has leftmost column 23−x5 ≤ 23−12
   = 11); the column mirror preserves row occupancy, hence the class. Therefore
   **no row-deficient maximal safe configuration exists on 5x24**; every maximal safe
   configuration on 5x24 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19), K0816 (5x20), K0821 (5x21), K0834 (5x22), K0835
   (5x23) — all witness-free — and K0332 (29-stone witness at 5x18, least witness width
   18): the witness-free width set of (5,7) is **{19, 20, 21, 22, 23, 24}**, so in the
   set form **M_{5,7} ∈ {19,...,24} or M_{5,7} ≥ 25**, sharpened (the K0821-audit
   convention, applied to the extended free set) to **M_{5,7} = 19 or M_{5,7} ≥ 26**:
   widths 20–24 are verified witness-free and cannot be the threshold, and M = 25 would
   require a witness at the verified witness-free width 24, so the next possible witness
   sits at w ≥ 25, forcing M = w + 1 ≥ 26. The upper bound 158 (K0332/K0024
   substitution) is unchanged. The witness-search frontier moves to 5x25.

## Method

`sat3.js` class-split encoder on the K0810 census (circleABC integer triples) and
sequential-counter core, decided by the official kissat 4.0.4 linux-amd64 release binary
(arminbiere/kissat rel-4.0.4 asset). 2-worker queue runs with per-instance `timeout`
60–260 s; CNF regeneration + solve + records by mkcnf.sh / qrun.sh / mkrecords5724.js
(scripts/ dir, deterministic; byte-identical encoders to the K0834/K0835 lanes).

## Verification

- **Positive control**: 5x18 q=7 class {0} **SAT** — 343,134 conflicts / 10.6 s,
  **bit-exact with the K0821, K0834 and K0835 lane control runs**; decoded model
  29 stones rows (5,6,6,6,6), census-free `verifyConfig` PASS (K0332 witness board
  rediscovered end-to-end).
- **Cross-encoding**: {0,1} and {2} re-encoded with --lex=H (lex-leader over column
  reflection — class-preserving, hence sound) are UNSAT again (555,120 / 296,008
  conflicts).
- **Determinism**: the whole sweep ran in one uninterrupted pass on this environment;
  the encoders and solver are byte-identical to the K0835 lane whose cross-reset
  bit-exact re-run reconciliation is documented there (and the 5x18 control again
  reproduces 343,134 bit-exactly, the third cross-lane reproduction of that number).

## Scope and limits

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and k×minpos decomposition (protocol brute-force-validated in K0816/K0818), and
kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 25 remains open: exact
M_{5,7} needs witness-free verification for all widths up to the K0332/K0024 bound
U=158 or a universal tail argument. The witness frontier moves to 5x25: a witness there
gives M ≥ 26; witness-free there extends the free set to {19,...,25}. The 11x11 empty
board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain
UNKNOWN.
