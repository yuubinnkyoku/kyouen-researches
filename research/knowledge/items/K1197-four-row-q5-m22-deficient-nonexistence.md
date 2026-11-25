---
id: K1197
title: "4x22 q=5 row-deficient maximal nonexistence (class-split cover complete: 65 direct UNSAT + 57 exhaustive disjoint second-stone x2 sub-bucket UNSAT deciding the three 600s-INDET class-0 k3 buckets) — witness-free width set of (4,5) is {21,22}: M_{4,5} = 21 or >= 24"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0857
  note: "(4,21,5) deficient nonexistence; this item instantiates the same 9-class cover / krow x minpos decomposition / exhaustive disjoint x2 second-stone split protocol at width 22 (m21 x2 encoder verified byte-identical on k=3 before the sweep)"
- type: depends_on
  target: K0833
  note: "the (4,5) witness band m=5..20 (all SAT, dual/triple-verified) and the m=20 positive-control witness reused as the calibration control here (CNF md5 362034b2, SAT 375,415 conflicts bit-exact in both the pre-reset and post-reset environments)"
- type: depends_on
  target: K0318
  note: "the upper bound U_{4,5}=140 (substitution), cited unchanged"
- type: depends_on
  target: K0821
  note: "the witness-free width-set audit convention: free set {21,22} gives M_{4,5} = 21 or >= 24 (M = last-witness+1; a reappearing witness must sit at m >= 23, forcing M >= 24, so M=22/23 impossible)"
artifacts:
- path: research/experiments/four-row-q5-m22-class-split-20261115/scripts/sat4.js
  role: solver
  note: "k-aware x2 second-stone encoder on the K0810 sat.js census + sat2.js counter core via sat3.js dumpClass (k=3 keeps B <= m-2 = 20; the k-aware m-1 extension applies to k=2 only and is not exercised by these instances)"
- path: research/experiments/four-row-q5-m22-class-split-20261115/scripts/sat3.js
  role: solver
  note: "class-split / --krow / --minpos encoder used for the 65 directly-decided instances"
- path: research/experiments/four-row-q5-m22-class-split-20261115/output/records.jsonl
  role: data
  note: "133 records: 1 positive control SAT + 3 superseded 600s direct-INDET honest negatives + 129 UNSAT (multi 7 + k0 2 + k1 22 + k2 22 + c1k3 direct 11 + c0k3p3..p10 direct 8 + x2 sub-buckets 57); append-only, pushed in 4 increments (497f4e17, 433215df, dddf26bd, 02517132)"
- path: research/experiments/four-row-q5-m22-class-split-20261115/output/x2-split-verification-20261121.json
  role: data
  note: "second verification: 57/57 UNSAT bucket tally, per-bucket conflict sums (14,914,910 / 11,831,256 / 9,750,138 = 36,496,304), 4 CNF regeneration md5 matches, 3 sample reruns bit-exact, environment-reset crossing reproductions 15/15"
- path: research/experiments/four-row-q5-m22-class-split-20261115/README.md
  role: proof
  note: "claim, coverage-completeness argument (9 canonical classes mod row-mirror V; k in 0..3 x minpos in 0..10 sound H-split with min(x1,21-x_k) <= 10; x2 split exhaustive disjoint on the k3 p0/p1/p2 buckets), calibration chain, operational incident record (07:53Z hard reset with 30 lost unpublished decisions re-run bit-exact), scope and limits"
scope: "'finite machine verification (kissat 4.0.4: 65 direct instances + 57 x2 sub-bucket instances, all UNSAT at cap 900s; positive control SAT). 4x22 q=5 only.'"
evidence: "'complete-enumeration-by-class-split with exhaustive disjoint second-stone case splits on the resistant buckets (deterministic-machine verification: per-instance CNF md5 ledger, CNF regeneration matches, bit-exact sample reruns, cross-environment conflict reproductions). See README.md and x2-split-verification-20261121.json.'"
---

# 4x22 q=5 row-deficient maximal nonexistence — class-split cover complete, witness-free width {21,22}

## Claim

1. On the 4x22 integer grid (q=5), for each of the 9 row-mirror-canonical deficiency
   classes D ⊆ {0,1,2,3} (canonical representatives of the 15 non-empty subsets under
   y -> 3-y), the class-split SAT instance — rows in D hold at most 3 stones (q−2),
   rows outside D held FULL (exactly 4, since a row is a line of length 22 ≥ q caps
   safety at 4), safety ≤ 4 stones per census curve, maximality (every empty cell
   covered by a ≥5-stone curve) — is **UNSAT**:
   - 7 multi-element canonical classes decide directly (c01 at 600s from the 2026-11-15
     session; c02/c03/c12/c012/c013/c0123 at cap 900s from the 2026-11-20 takeover).
   - Singletons {0},{1} decompose by exact deficient-row count k ∈ 0..3 and minpos
     p ∈ 0..10 (sound H-split: min(x1, 21−x_k) ≤ 10; H preserves rows):
     k=0 (2 instances), k=1 (22), k=2 (22) all decide directly, UNSAT, each ≤ 40s;
     k=3 class {1} decides directly (11 UNSAT, hardest c1k3p0 5,324,074 / 442.6s);
     k=3 class {0} splits: p3..p10 decide directly (8 UNSAT, hardest c0k3p3
     5,162,737 / 415s) and the three resistant buckets p0/p1/p2 (600s direct INDET
     honest negatives, already on record) are decided by the **complete disjoint
     second-stone split**: row 0 = {a, b, c} with a pinned by minpos, split on b:
     c0k3p0: b ∈ 1..20 (20); c0k3p1: b ∈ 2..20 (19); c0k3p2: b ∈ 3..20 (18).
     All **57 sub-buckets UNSAT** at cap 900s, 0 SAT, 0 INDET (per-bucket conflict
     sums 14,914,910 / 11,831,256 / 9,750,138; hardest c0k3p0x2b1 2,196,989 / 115s —
     1.1x the m21 x2 hardest, ring-fit against the width-21 anchor instance).
   - Total deciding machine effort at m=22: 129 UNSAT instances.
2. Coverage: every row-deficient maximal safe configuration has a non-empty exact
   deficiency set D; the exact-D instances partition them; the k × minpos
   decomposition and the second-stone splits are exhaustive and disjoint on their
   domains. Therefore **no row-deficient maximal safe configuration exists on
   4x22**: every maximal safe configuration on 4x22 has 16 stones with row
   occupancy (4,4,4,4).
3. Combined with K0857 (width 21 witness-free), K0833 (witness band m=5..20, all
   SAT) and K0318 (upper bound U_{4,5}=140): the witness-free width set of (4,5)
   is **{21,22}** — so in the audit-convention form **M_{4,5} = 21 or M_{4,5} ≥ 24**
   (M = last witness width + 1; if no witness ever reappears beyond 20, M = 21; a
   reappearing witness must sit at m ≥ 23, forcing M ≥ 24; hence M = 22, 23 are
   impossible). The upper bound 140 is unchanged. The frontier moves to 4x23
   (a witness there gives M ≥ 24 decided and the interval form M ∈ [24,140];
   witness-free there extends the free set to {21,22,23} and sharpens to
   M = 21 or ≥ 25).

## Verification

- Calibration (pre-sweep, this environment): positive control ctrl_4x20_c0k3p1 —
  CNF md5 362034b210d89ed3a25d34072995f3a6 byte-exact, kissat SAT, 375,415 conflicts
  bit-exact. Cross-instances: published c1k3p3 CNF regenerated byte-exact
  (25bccf63…); published c1k3p10 rerun UNSAT 1,146,769 conflicts bit-exact; the
  k-aware sat4 and the 4x21-lane sat4 produce byte-identical CNF on (4,21,5)
  c0k3p0 --x2=1 (13749780…). kissat 4.0.4 static binary md5-matches the published
  pin (3a5eba83…).
- Hard-reset crossing: at 07:53Z, mid-sweep, the execution environment was wiped
  (~30 unpublished x2 decisions lost; the repo base at HEAD 497f4e17 was intact).
  After rebuilding every artifact from repo pins and re-running, all 15 decisions
  that had been observed before the reset reproduced their conflict counts
  bit-exactly (c0k3p0 b1/b4/b5/b6/b7/b8/b18/b19/b20; c0k3p1 b2/b8/b9/b10/b11;
  plus the c1k3p10 rerun). All 57 final x2 records are from the post-reset
  environment.
- Second verification (x2-split-verification-20261121.json): 57/57 UNSAT tally;
  per-bucket conflict sums; 4 CNF regeneration md5 matches (c0k3p0x2b7/b12,
  c0k3p1x2b13, c0k3p2x2b10); 3 sample reruns bit-exact (c0k3p0x2b1, c0k3p1x2b2,
  c0k3p2x2b3); ledger provenance (133 lines, 4 append-only increment commits).
- Operational notes: records.jsonl is append-only and was pushed in 4 increments;
  the three direct-600s-INDET rows (2026-11-15) are retained as honest negatives,
  each now superseded by a complete 18-20 bucket split; cap-reach cuts are not
  bit-exact and nothing in the claim rests on one.

## Scope

Finite machine verification up to the correctness of the K0810 census, the
sat3/sat4 encodings and kissat 4.0.4; not a number-theoretic proof.
Persistence at m ≥ 23 remains open: the exact value of M_{4,5} needs witness-free
verification for all widths up to U=140 or a universal tail argument. The 11x11
empty board, the two-stone roots {49,60}/{59,60} and S2 {59,60} are unaffected
and remain as recorded (UNKNOWN). The 4x23 sweep is the next frontier: the m22
experience (direct k3 hardening ~2x while the x2 split hardest bucket ran at
merely 1.1x its m21 twin, finishing an order of magnitude under cap) suggests
per-bucket splitting will decide width 23 as well, but the multi-class direct
instances may thicken (c01-class UNSAT was 451s at m22).
