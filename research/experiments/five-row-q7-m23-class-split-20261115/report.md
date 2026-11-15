# 5x23 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

Date: 2026-11-15. Fast lane, successor of K0834 (5x22). Extends the (5,7) witness-free
sweep one width on the same class-split SAT machinery (K0816/K0821/K0834 protocol).

## Claim

1. On the 5x23 integer grid (q=7), for every one of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under
   y -> 4-y), the class-split SAT instance — rows in D hold at most 5 stones (unit ¬rowGe[y]),
   rows outside D hold exactly 6 (unit rowGe[y]; safety caps every row at 6 since a row is
   a line of length 23 ≥ q), safety ≤ 6 stones per census curve, maximality (every empty
   cell covered by a ≥6-stone curve) — has **no solution**:
   - 17/19 classes directly **UNSAT** (kissat 4.0.4, exit 20; hardest {0,1}: 708,108
     conflicts / 22.3 s; {1,3}: 413,739; {0,4}: 542,893; {2}: 392,089; direct total
     4,673,619 conflicts — slightly *easier* than m=22's 5,256,816, continuing the
     m21→m22 flat-to-decreasing difficulty trend).
   - {0} and {1}: decided by the **complete k × minpos decomposition**
     (the K0816/K0821/K0834 protocol): k = 0..4 (exact deficient-row stone count,
     5 instances each; hardest {0} k=4: 1,185,996 / {1} k=4: 1,098,229) and
     k = 5 × minpos = 0..11 (12 instances each — the sound bound grows to
     floor((m−1)/2) = 11 at m = 23; hardest {1} k=5 mp=0: 2,555,137 conflicts / 107.96 s;
     {0} k=5 mp=0: 2,135,466 / 89.5 s). All 34 sub-instances **UNSAT**.
   - Total conflicts across the 51 deciding instances: **20,916,467**
     (17 direct: 4,673,619; 34 decomposition: 16,242,848); the two lex=H cross-checks add
     825,398 (records.jsonl total 22,084,999). No SAT, no INDET among the deciding
     instances.
2. Coverage: the exact deficiency set D = {rows with ≤ q-2 stones} is non-empty for every
   deficient maximal safe configuration and the exact-D instances partition them
   (K0818/K0816 class logic, brute-force-validated on small boards in K0818); the
   k×minpos decomposition is exhaustive: k = 0..5 partitions the deficient row's stone
   count, and for k = 5 the minpos split pins the **leftmost stone of the first deficient
   row at column exactly P**; every configuration or its column mirror has leftmost stone
   column ≤ 11 at m = 23 (if x1 ≥ 12 then the mirror has leftmost column 22−x5 ≤ 22−12 = 10);
   the column mirror preserves row occupancy, hence the class. Therefore
   **no row-deficient maximal safe configuration exists on 5x23**; every maximal safe
   configuration on 5x23 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20 witness-free), K0821
   (5x21 witness-free), K0834 (5x22 witness-free) and K0332 (29-stone witness at 5x18,
   least witness width 18): the witness-free width set of (5,7) is
   **{19, 20, 21, 22, 23}**, so in the set form **M_{5,7} ∈ {19,20,21,22,23} or
   M_{5,7} ≥ 24**, sharpened (K0821-audit convention, applied to the extended free set)
   to **M_{5,7} = 19 or M_{5,7} ≥ 25**: widths 20–23 are verified witness-free and cannot
   be the threshold, and M = 24 would require a witness at the verified witness-free
   width 23, so the next possible witness sits at w ≥ 24, forcing M = w + 1 ≥ 25.
   The upper bound 158 (K0332/K0024 substitution) is unchanged. The witness-search
   frontier moves to 5x24.

## Method

`sat3.js` class-split encoder on the K0810 census (circleABC integer triples — independent
of the K0738–K0759 runner's circumcenter form) and sequential-counter core, decided by the
official kissat 4.0.4 linux-amd64 release binary (github.com/arminbiere/kissat tag
rel-4.0.4 asset kissat-4.0.4-linux-amd64.zip). 2-worker queue runs with per-instance
`timeout` 60–260 s; per-class conflicts and process-time taken from each kissat log.
CNF regeneration + solve + records built by mkcnf.sh / qrun.sh / mkrecords5723.js
(scripts/ dir, deterministic).

## Verification

- **Positive control**: 5x18 q=7 class {0} **SAT** — 343,134 conflicts / 10.4 s,
  **bit-exact with the K0821 and K0834 lane control runs** (343,134); decoded model
  29 stones rows (5,6,6,6,6), census-free `verifyConfig` PASS. The K0332 witness board
  rediscovered end-to-end through the identical encode→solve→decode→verify path.
- **Cross-encoding**: {0,1} and {2} re-encoded with --lex=H (lex-leader over column
  reflection — class-preserving, hence sound) are UNSAT again
  (504,359 / 321,039 conflicts).
- **Determinism across an environment reset**: the local scratch directory was lost to a
  mid-sweep execution-environment reset on 2026-11-15 (after 27 of 51 deciding instances
  had finished locally). The full sweep was re-run from freshly generated CNFs and the
  re-download of the official kissat 4.0.4 binary; every pre-reset instance reproduces
  its conflict count bit-exactly in the re-run (e.g. {0,1}: 708,108; {0}k4: 1,185,995;
  {1}k5p3: 240,999; {1}k0: 202), and the 5x18 control matches the K0821/K0834 lanes
  bit-exactly. Raw logs were pushed batch-by-batch during the re-run (batches 1–4 on
  main) precisely so that any further reset could not lose evidence.

## Scope and limits

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and k×minpos decomposition (protocol brute-force-validated in K0816/K0818), and
kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 24 remains open: exact
M_{5,7} needs witness-free verification for all widths up to the K0332/K0024 bound U=158
or a universal tail argument. The witness frontier moves to 5x24: a witness there gives
M ≥ 25; witness-free there extends the free set to {19,...,24}. The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.
