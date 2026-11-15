---
id: K0852
title: "5x22 q=6 row-deficient maximal witness exists (class {0} k=4 minpos=0 SAT, 24 stones, dual-verified) — (5,6) witness band m=15..22, M_{5,6} in [23, 249], frontier 5x23"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs), sequential-counter/maximality encoding core used verbatim (sat.js / sat2.js / sat3.js; blob shas 6c3262d6 / edfae1d2 / 6dfa7db3)"
- type: depends_on
  target: K0815
  note: "24-stone witnesses at 5x20/5x21 (q=6) and the 5x22 kissat 240s INDET frontier (2.77M conflicts) that this SAT result resolves"
- type: depends_on
  target: K0723
  note: "the m=15 witness at the base of the (5,6) witness band m=15..21 which this item extends to m=15..22"
- type: depends_on
  target: K0318
  note: "substitution upper bound M_{5,6} <= 249 (with K0024 T=10101), unchanged by this item"
- type: supports
  target: K0815
  note: "the (5,6) lower-bound side: witness band m=15..21 -> m=15..22, lower bound 22 -> 23"
artifacts:
- path: research/experiments/five-row-q6-m22-witness-20261115/scripts/sat3.js
  role: solver
  note: "class-split / krow / minpos encoder + kissat model decode with census-free verifyConfig (byte-identical to the K0836..K0851 lane scripts)"
- path: research/experiments/five-row-q6-m22-witness-20261115/raw/r5x22q6_0k4p0.txt
  role: certificate
  note: "raw kissat 4.0.4 log of the deciding SAT instance: class {0} krow=0:4 minpos=0, 3,126,820 conflicts / 194.87 s; reproduced bit-exactly after a full environment reset"
- path: research/experiments/five-row-q6-m22-witness-20261115/raw/witness_5x22q6_0k4p0.json
  role: data
  note: "decoded witness: 24 stones, rows (4,5,5,5,5), verifyConfig PASS (safe + maximal)"
- path: research/experiments/five-row-q6-m22-witness-20261115/report.md
  role: proof
  note: "claim, three-way verification (decode+verifyConfig, independent pure-TS census reimplementation, krow/minpos pin check), positive-control bit-exactness, m=23 INDET negatives, complete 1- and 2-stone surgery enumerations from the seed on 5x23 (1,416 / 552,000 configs, 0 witnesses), environment-reset reproducibility protocol, scope"
- path: research/experiments/five-row-q6-m22-witness-20261115/scripts/surgery_m23.js
  role: source
  note: "5x23 transplant analysis (single unblocked cell U=(22,0), 32 T-curves, seed counts 4,3,3,...) and the complete 1-stone surgery enumeration (1,416 configs, 0 witnesses)"
- path: research/experiments/five-row-q6-m22-witness-20261115/scripts/surgery2b_m23.js
  role: source
  note: "complete 2-stone surgery enumeration with the heavy-T-curve sound filter (>=1 add on a seed>=3 T-curve or at U; 552,000 configs, 0 witnesses)"
- path: research/experiments/five-row-q6-m22-witness-20261115/records.jsonl
  role: data
  note: "4 kissat records: control 5x21 {0} SAT 330,743 (bit-exact with the five-row-q6-m22-class-split-20261114 control); witness 5x22 {0} k4p0 SAT 3,126,820; m=23 k4p0 / k4p1 INDET 3,343,593 / 3,369,340 at the 220 s wall clock (time-cut counts are same-trajectory, not bit-exact)"
- path: research/experiments/five-row-q6-m22-witness-20261115/summary.json
  role: data
  note: "aggregate: witness, band update (5,6) m=15..22 with M in [23, 249], honest negatives, surgery counts, reset-recovery reproducibility notes"
scope: "'finite machine verification (SAT witness + dual census verification, kissat 4.0.4); 5x22 q=6 only; band bounds statement, not a threshold determination.'"
evidence: "'complete-solver-run-witness (verification: encoder decode + census-free verifyConfig + independent pure-TS census reimplementation + positive-control bit-exact reproduction + deterministic post-reset re-run bit-exact for both SAT instances). See report.md.'"
---

# 5x22 q=6 row-deficient maximal witness — (5,6) band extends to m=15..22

## Claim

1. On the 5x22 integer grid (q=6), a **24-stone row-deficient maximal safe
   configuration exists**: the class-split instance with deficiency class
   {0} (row 0 at most 4 stones, rows 1-4 exactly 5 — a row is a line of
   length 22 >= q so safety caps every row at 5), safety <= 5 stones per
   census curve, maximality (every empty cell covered by a >=5-stone
   curve), refined by krow=0:4 (row 0 exactly 4 stones) and minpos=0
   (leftmost stone of row 0 at column 0), is **SAT** (kissat 4.0.4,
   3,126,820 conflicts / 194.87 s). Witness (24 stones, rows (4,5,5,5,5)):
   (0,0),(11,0),(15,0),(20,0),(3,1),(6,1),(10,1),(15,1),(18,1),
   (3,2),(6,2),(8,2),(10,2),(15,2),(4,3),(6,3),(9,3),(16,3),(17,3),
   (7,4),(9,4),(11,4),(12,4),(14,4).
2. Verification: (a) sat3.js decode + sat.js census-free verifyConfig PASS;
   (b) independent pure-TS reimplementation (own pair-line / triple-circle
   census, canonical integer coefficients) — safe (0 unsafe curves among
   1,824 stone-curves, max 5 stones per curve) and maximal (86/86 empty
   cells blocked) PASS; (c) krow/minpos pins verified. Positive control
   5x21 {0} SAT 330,743 conflicts is bit-exact with the
   five-row-q6-m22-class-split-20261114 control; both SAT runs were
   reproduced bit-exactly (identical conflicts, identical witness stone
   set) after a full environment reset.
3. The (5,6) witness band extends **m = 15..21 -> m = 15..22** (with
   K0723 (5x15), K0810 (5x16,17), K0811, K0815 (5x19,20,21)); hence
   **M_{5,6} in [23, 249]** (upper: K0318 substitution, unchanged).
   The frontier moves to 5x23. The five-row-q6-m22-class-split-20261114
   250 s INDET values for class {0} (3,556,467) and {0}krow0:4 (2,019,686)
   are thereby explained: the sweep stopped just short of this witness.
4. m=23 honest negatives (INDET, **not** absence): class {0} k4p0
   3,343,593 and k4p1 3,369,340 conflicts at the 220 s wall clock
   (time-cut counts follow the same deterministic trajectory but are not
   bit-exact across runs).
5. Seed-neighborhood surgery on 5x23 (complete enumerations, negative):
   the transplanted witness is safe with exactly one unblocked cell
   U=(22,0) (32 T-curves through it, seed counts 4,3,3,...). All 1-stone
   surgeries (1,416 configs — adds restricted soundly to the 58 seed-empty
   T-curve cells or U) and all 2-stone surgeries (552,000 configs — at
   least one add on a heavy (seed>=3) T-curve or at U, sound by the
   seed<=2 curves reaching at most 4 with two adds) yield **0 witnesses**.
   So any 5x23 24-stone deficient-maximal configuration lies > 2
   stone-moves (symmetric difference > 4 cells) from this seed. This is a
   neighborhood statement about one seed, not an m=23 nonexistence claim;
   m=23 remains open.

## Scope

The witness existence is a finite verified fact; the band statement is a
bounds statement (M_{5,6} not determined). 5x23 and beyond open; the 11x11
empty board and its roots/classes are unaffected and remain UNKNOWN.
