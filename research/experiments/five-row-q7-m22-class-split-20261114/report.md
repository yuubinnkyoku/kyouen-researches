# 5x22 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

Date: 2026-11-15. Completion (takeover) of the 2026-11-14 batch-1 lane by the fast lane.
The (5,7) witness frontier opened by K0821 (5x21 witness-free) is settled by the same
class-split SAT machinery (K0816/K0821), one width further.

## Claim

1. On the 5x22 integer grid (q=7), for every one of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under
   y -> 4-y), the class-split SAT instance — rows in D hold at most 5 stones (unit ¬rowGe[y]),
   rows outside D hold exactly 6 (unit rowGe[y]; safety caps every row at 6 since a row is
   a line of length 22 ≥ q), safety ≤ 6 stones per census curve, maximality (every empty cell
   covered by a ≥6-stone curve) — has **no solution**:
   - 17/19 classes directly **UNSAT** (kissat 4.0.4, exit 20; batch-1 raw logs
     2026-11-14T15:25:57Z; hardest {0,1}: 875,682 conflicts / 32.5 s; {1,3}: 553,321;
     {0,4}: 532,938; {0,3}: 527,330; {0,2,3}: 199,205 / 5.9 s). All 17 were **re-run by the
     takeover lane and reproduce the batch-1 conflict counts bit-exactly**.
   - {0} and {1}: the plain instances resisted ~142 s single runs (2,849,545 / 3,330,616
     conflicts, batch-1 SIGTERM logs) and are decided by the **complete k × minpos
     decomposition** (the K0816/K0821 protocol): k = 0..4 (exact deficient-row stone count,
     5 instances each) and k = 5 × minpos = 0..10 (11 instances each). All 32 sub-instances
     **UNSAT** (hardest: {0} k=5 mp=0: 3,380,578 conflicts / 153.8 s;
     {1} k=5 mp=0: 3,111,756 / 144.1 s; then {0} k=4: 1,465,046 / 63.7 s and
     {1} k=4: 1,402,958 / 60.3 s).
   - Total conflicts across the 49 deciding instances: **24,581,763**
     (17 direct: 5,256,816; 32 decomposition: 19,324,947); the two lex=H cross-checks add
     937,505 (records.jsonl total 25,519,268). No SAT, no INDET among the deciding instances.
2. Coverage: the exact deficiency set D = {rows with ≤ q-2 stones} is non-empty for every
   deficient maximal safe configuration and the exact-D instances partition them
   (K0818/K0816 class logic, brute-force-validated on small boards in K0818); the k×minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's stone count, and
   for k = 5 the minpos split pins the **leftmost stone of the first deficient row at column
   exactly P**; every configuration or its column mirror has leftmost stone column ≤ 10 at
   m = 22 (min(x1, 21−x5) ≤ 10 — otherwise x1 ≥ 11 and x5 ≤ 10, contradicting x1 ≤ x5); the
   column mirror preserves row occupancy, hence the class. Therefore **no row-deficient
   maximal safe configuration exists on 5x22**; every maximal safe configuration on 5x22
   has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20 witness-free), K0821
   (5x21 witness-free) and K0332 (29-stone witness at 5x18, least witness width 18): the
   witness-free width set of (5,7) is **{19, 20, 21, 22}**, so
   **M_{5,7} ∈ {19, 20, 21, 22} or M_{5,7} ≥ 23**; the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier moves to 5x23.

## Method

`sat3.js` class-split encoder on the K0810 census (circleABC integer triples — independent
of the K0738–K0759 runner's circumcenter form) and sequential-counter core, decided by the
official kissat 4.0.4 linux-amd64 binary. 2-worker parallel batches with per-instance
`timeout` 250–260 s; per-class conflicts and process-time taken from each kissat log.
Batch-1 (2026-11-14T15:25:57Z) contributed the 17 direct-class raw logs and the two plain
{0}/{1} INDET logs; the takeover lane re-ran all 17 direct classes (bit-exact), produced the
32 decomposition logs, both lex cross-checks and the positive control.

## Verification

- **Positive control**: 5x18 q=7 class {0} **SAT** — 343,134 conflicts / 12.5 s, **bit-exact
  with the K0821 lane's control run** (343,134); decoded model 29 stones rows (5,6,6,6,6),
  census-free `verifyConfig` PASS. This is the K0332 witness board rediscovered end-to-end
  through the identical encode→solve→decode→verify path used for the 19 classes.
- **Cross-encoding**: {0,1} and {2} re-encoded with --lex=H (lex-leader over column
  reflection — class-preserving, hence sound) are UNSAT again
  (627,149 / 310,356 conflicts).
- **Determinism / batch-1 reconciliation**: all 17 direct classes re-run by the takeover
  lane reproduce the batch-1 conflict counts bit-exactly (17/17 exact matches, e.g.
  {0,1}: 875,682, {0,2,3}: 199,205 — the latter's batch-1 log is complete on main despite a
  corrupted local fetch); the 5x18 positive control reproduces the K0821 lane's 343,134
  bit-exactly; the m22 CNF header (`p cnf 4989 17791`) matches the batch-1 log's parsed
  header.

## Scope and limits

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and k×minpos decomposition (protocol brute-force-validated in K0816/K0818), and
kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 23 remains open: exact
M_{5,7} needs witness-free verification for all widths up to the K0332/K0024 bound U=158
or a universal tail argument. The witness frontier moves to 5x23: a witness there gives
M ≥ 23, witness-free there extends the free set to {19,20,21,22,23}. The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.

## Files

- `scripts/sat3.js` (+ `sat2.js`, `sat.js` core, byte-identical to
  five-row-q7-m21-class-split-20261114/scripts/)
- `scripts/runall5722.sh` — deterministic completion driver (17 direct re-runs +
  k×minpos decomposition + lex cross-checks + control + records build)
- `scripts/mkrecords5722.js` — records.jsonl/summary.json builder
- `output/records.jsonl` — 52 records (17 direct UNSAT + 32 decomposition UNSAT +
  2 lex cross-checks + 1 positive control)
- `output/summary.json` — aggregate
- `output/r5x22q7_c*.txt` — 19 direct-class raw logs (17 UNSAT from batch-1, re-verified
  bit-exact; `r5x22q7_c0.txt`/`r5x22q7_c1.txt` are the superseded plain INDET attempts),
  `output/r5x22q7_[01]k*.txt` — 32 decomposition raw logs,
  `output/r5x22q7_c01_lexH.txt`, `output/r5x22q7_c2_lexH.txt` — lex cross-check logs,
  `output/r_ctrl_5x18_c0.txt` — SAT control with model
