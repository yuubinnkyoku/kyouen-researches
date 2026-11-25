# 6x20 q=8 row-deficient maximal nonexistence — all 35 canonical classes UNSAT

Date: 2026-11-14. Direct extension of the K0818 6x19 class-split sweep to the next width.

## Claim

1. On the 6x20 integer grid (q=8), for each of the 35 row-mirror-canonical deficiency classes
   D ⊆ {0..5} (canonical representatives of the 63 non-empty subsets under y -> 5-y), the
   class-split SAT instance — rows in D hold at most 6 stones (unit ¬rowGe[y]), rows outside D
   hold exactly 7 (unit rowGe[y]; safety caps every row at 7 since a row is a line of length
   20 ≥ q), safety ≤ 7 stones per census curve, maximality (every empty cell covered by a
   ≥7-stone curve) — is **UNSAT** (kissat 4.0.4, exit 20; **16,446,081 conflicts total**;
   hardest class {2}: 2,763,766 conflicts / 128.9 s; class {1}: 2,289,935 / 119.5 s).
2. Coverage (same partition argument as K0818/K0816, brute-force-validated on small boards in
   K0818): every deficient maximal safe configuration has a non-empty exact deficiency set
   D = {rows with ≤ q-2 stones}, the exact-D instances partition all such configurations, and
   row-mirror soundness reduces 63 classes to 35. Hence **no row-deficient maximal safe
   configuration exists on 6x20**; every maximal safe configuration on 6x20 has 42 stones.
3. Combined with K0818 (6x19 witness-free) and K0815 (41-stone deficient maximal at 6x18):
   the witness-free width set of (6,8) is **{19, 20}**, least witness width 9 (witnesses at
   6x9..6x18), so **M_{6,8} ∈ {19, 20} or M_{6,8} ≥ 22**; upper bound 371 (K0318/K0024
   substitution) unchanged. The witness-search frontier moves to 6x21.

## Method

Identical machinery to K0818: `sat3.js` class-split encoder on the K0810 census
(circleABC integer triples — independent of the K0738–K0759 runner's circumcenter form)
and sequential-counter core, decided by the official kissat 4.0.4 linux-amd64 binary.
Classes were run pairwise in parallel (2 workers, each `timeout 285`); per-class
`process-time` and conflicts are taken from each kissat log.

## Verification

- **Positive control**: 6x18 q=8 class {1} SAT — 511,895 conflicts / 20.1 s, bit-exact with the
  K0818 control; decoded model 41 stones rows (7,6,7,7,7,7), `verifyConfig` census-free
  independent verifier PASS (K0815 witness board rediscovered end-to-end through the
  same encoder+solver path used for the 35 UNSAT instances).
- **Negative controls**: 2x8 q=4 class {0} SAT (K0796 witness rediscovered);
  2x9 q=4 class {0} UNSAT (M_{2,4}=9 consistent).
- **Cross-encoding**: the two hardest singleton classes re-encoded with --lex=H
  (lex-leader over column reflection — class-preserving, hence sound for the class split)
  are UNSAT again: {1} 2,038,080 conflicts / 108.7 s; {2} 2,331,073 conflicts / 112.5 s.
- **Class logic**: the deficiency-set partition and mirror reduction are the K0818/K0816
  logic, brute-force validated there on 19/19 small-board instances; the only change here
  is the board width (20 vs 19).

## Per-class results (conflicts / kissat process-time seconds)

| class | conflicts | seconds | | class | conflicts | seconds |
|---|---|---|---|---|---|---|
| {0} | 494,294 | 19.8 | | {1} | 2,289,935 | 119.5 |
| {2} | 2,763,766 | 128.9 | | {0,1} | 550,215 | 22.3 |
| {0,2} | 493,781 | 18.5 | | {0,3} | 86,257 | 3.3 |
| {0,4} | 246,856 | 8.9 | | {0,5} | 457,514 | 18.4 |
| {1,2} | 2,729,150 | 120.4 | | {1,3} | 1,384,493 | 56.5 |
| {1,4} | 142,073 | 5.6 | | {2,3} | 1,185,037 | 45.0 |
| {0,1,2} | 535,086 | 19.6 | | {0,1,3} | 141,810 | 4.9 |
| {0,1,4} | 159,137 | 6.2 | | {0,1,5} | 199,254 | 8.1 |
| {0,2,3} | 109,963 | 4.3 | | {0,2,4} | 140,547 | 5.0 |
| {0,2,5} | 83,392 | 3.2 | | {0,3,4} | 126,645 | 4.8 |
| {1,2,3} | 281,513 | 10.0 | | {1,2,4} | 94,212 | 3.9 |
| {0,1,2,3} | 141,602 | 5.1 | | {0,1,2,4} | 115,765 | 4.2 |
| {0,1,2,5} | 97,066 | 4.0 | | {0,1,3,4} | 129,714 | 4.5 |
| {0,1,3,5} | 110,540 | 4.1 | | {0,1,4,5} | 150,688 | 5.2 |
| {0,2,3,4} | 143,648 | 5.1 | | {0,2,3,5} | 104,748 | 4.0 |
| {1,2,3,4} | 115,880 | 4.1 | | {1,2,3,4,5} | 102,406 | 3.8 |
| {0,2,3,4,5} | 169,736 | 5.7 | | {0,1,3,4,5} | 213,873 | 6.7 |
| {0,1,2,3,4,5} | 155,485 | 5.1 | | | | |

(Small numeric drift vs the table above is possible for the parallel-pair classes;
`records.jsonl` is the authoritative source.)

## Scope and limits

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding (brute-force validated in K0818), and kissat 4.0.4 — the same evidence level as
K0818/K0816; not a number-theoretic proof. Persistence at m ≥ 21 remains open: exact
M_{6,8} needs either witness-free verification for all widths up to the K0024/K0318 bound
U=371 or a universal tail argument. The witness frontier moves to 6x21 (witness there
would give M ≥ 22; witness-free there extends the free set to {19,20,21}).
The 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are
unaffected and remain UNKNOWN.

## Files

- `scripts/sat3.js` (+ `sat2.js`, `sat.js` core, verbatim from K0818/K0810 lanes)
- `scripts/runall.sh` — deterministic sweep driver
- `scripts/mkrecords.js` — records.jsonl/summary.json builder from raw kissat logs
- `output/records.jsonl` — 38 records (35 classes + 2 lex=H cross-checks + 1 positive control)
- `output/summary.json` — aggregate
- `output/r6x20q8_c*.txt` — raw kissat logs (35 classes + lexH cross-checks)
- `output/r_ctrl_6x18_c1.txt` — positive-control log (SAT model included)
