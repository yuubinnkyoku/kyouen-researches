---
id: K0857
title: "4x21 q=5 row-deficient maximal nonexistence (all 75 class-split instances UNSAT; the two deep-cap-resistant buckets are decided by a complete 37-bucket second-stone case split) — witness-free width set of (4,5) starts at 21, M_{4,5} ∈ {21} or >= 23"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs), the sequential-counter/maximality core and the model decoder/verifyConfig are used verbatim (sat.js / sat2.js); sat4.js adds only the class-split unit clauses, --krow exact count, --minpos and --x2 second-stone pinning"
- type: depends_on
  target: K0833
  note: "the (4,5) witness band m=5..20 (all SAT, dual/triple-verified), the m=20 witness used as the positive-control board, the upper bound U_{4,5}=140 (K0318 substitution) and the frontier history (def-mode 210s INDET, 2-class lex=H covering 600s INDET x2) that motivated the absence-capable class split"
- type: depends_on
  target: K0821
  note: "the witness-free width-set audit convention (band + witness-free widths => M in the free-set complement or >= next width) and the 5x21 q=7 class-split protocol (canonical classes mod row-mirror V, k x minpos sound decomposition) that this (4,21,5) sweep instantiates; the x2 second-stone case split is the new ingredient beyond K0821"
artifacts:
- path: research/experiments/four-row-q5-m21-class-split-20261115/scripts/sat4.js
  role: solver
  note: "class-split / exact-count (--krow) / minpos / --x2 second-stone encoder on the K0810 sat.js census + sat2.js counter core, plus kissat model decoding with census-free verifyConfig"
- path: research/experiments/four-row-q5-m21-class-split-20261115/sweepp0x2.sh
  role: source
  note: "deterministic x2 sweep driver v2.1: second-stone sub-buckets c0k3p0 b=1..19 and c0k3p1 b=2..19, cap 900s, resumable with comma-anchored record keys (prefix-collision-proof)"
- path: research/experiments/four-row-q5-m21-class-split-20261115/output/records.jsonl
  role: data
  note: "117 records: 110 m=21 UNSAT (73 direct class-split instances + 37 x2 sub-buckets, deciding conflicts 102,380,271), 3 SAT positive controls (incl. (4,20,5) class{0} k3 p1 SAT 20.0s/375,415), 4 superseded INDET rows for the two x2-decided parent buckets (cap 600s/2400s honest negatives)"
- path: research/experiments/four-row-q5-m21-class-split-20261115/output/x2-split-verification-20261115.json
  role: data
  note: "second verification: 37/37 UNSAT tally, per-bucket conflict sums (c0k3p0 19 buckets 13,382,360; c0k3p1 18 buckets 10,930,286; total 24,312,646), 4 CNF regeneration md5 matches, 2 sample reruns bit-exact; deciding-total erratum 126,692,917 -> 102,380,271 recorded in the erratum section"
- path: research/experiments/four-row-q5-m21-class-split-20261115/output/c0k3p0b1.txt
  role: data
  note: "hardest deciding instance raw kissat log ({0} k=3 minpos=0 second stone x2=1: UNSATISFIABLE, 1,969,663 conflicts, 185.1s); the other 36 raw x2 logs are not individually archived — every instance is deterministically reproducible (sat4.js CNF md5 recorded per instance, kissat 4.0.4 deterministic), and records.jsonl carries per-instance result/conflicts/sec/md5"
- path: research/experiments/four-row-q5-m21-class-split-20261115/README.md
  role: proof
  note: "claim, class coverage and decomposition-completeness argument (9 canonical classes mod V; k in 0..3 x minpos in 0..10 sound H-split; x2 exhaustive disjoint case analysis), calibration, operational notes (records append-only incident, driver v2.1 comma anchor), scope and limits"
scope: "'finite machine verification (kissat 4.0.4: 73 direct UNSAT instances + 37 second-stone sub-bucket UNSAT instances + SAT positive controls); 4x21 q=5 only.'"
evidence: "'complete-enumeration-by-class-split with an exhaustive disjoint second-stone case split on the resistant buckets (verification: deterministic-machine + CNF regeneration md5 + sample reruns bit-exact). See README.md.'"
---

# 4x21 q=5 row-deficient maximal nonexistence — all 75 class-split instances UNSAT

## Claim

1. On the 4x21 integer grid (q=5), for each of the 9 row-mirror-canonical deficiency
   classes D ⊆ {0,1,2,3} (canonical representatives of the 15 non-empty subsets under
   y -> 3-y), the class-split SAT instance — rows in D hold at most 3 stones (q−2),
   rows outside D hold exactly 4 (safety caps every row at 4 since a row is a line of
   length 21 ≥ q), safety ≤ 4 stones per census curve, maximality (every empty cell
   covered by a ≥5-stone curve) — is **UNSAT**:
   - 73/75 instances directly UNSAT (kissat 4.0.4, exit 20). Singletons {0},{1} are
     decomposed by exact deficient-row stone count k ∈ 0..3 and minpos p ∈ 0..10
     (sound H-split: min(x1, 20−x_k) ≤ 10; the column mirror preserves row occupancy,
     hence the class); multi-element classes run directly.
   - The two resistant buckets — {0} k=3 p=0 (c0k3p0) and {0} k=3 p=1 (c0k3p1) —
     resisted caps 600 s (7,814,011 / 7,324,409 conflicts) and 2400 s
     (13,113,901 / 12,619,361 conflicts) as honest negatives, and are decided by the
     **complete disjoint second-stone case split**: row 0 = {a, b, c} with a pinned by
     minpos, split on the second stone b. c0k3p0: b ∈ 1..19 (19 buckets, a=0);
     c0k3p1: b ∈ 2..19 (18 buckets, a=1). The split is exhaustive (b > 19 leaves no
     column for the third stone c > b on width 21) and disjoint. All **37 sub-buckets
     UNSAT** at cap 900 s (c0k3p0: 13,382,360 conflicts, hardest b1: 1,969,663 /
     185.1 s; c0k3p1: 10,930,286, hardest b3: 1,082,095 / 102.6 s; 0 SAT, 0 INDET).
   - Total conflicts across all 110 deciding m=21 instances: **102,380,271**
     (73 direct: 78,067,625; 37 x2: 24,312,646).
2. Coverage: every row-deficient maximal safe configuration has a non-empty exact
   deficiency set D, the exact-D instances partition them, and row-mirror soundness
   reduces 15 classes to 9. The k × minpos decomposition and the second-stone split
   are exhaustive on their buckets. Therefore **no row-deficient maximal safe
   configuration exists on 4x21**; every maximal safe configuration on 4x21 has 16
   stones with row occupancy (4,4,4,4).
3. Combined with K0833 (witness band m=5..20, all SAT dual/triple-verified) and
   K0318 (upper bound U_{4,5}=140): the witness-free width set of (4,5) is
   **{21}** — witnesses exist at every width 5..20 and at no verified width
   beyond — so in the set form **M_{4,5} ∈ {21} or M_{4,5} ≥ 22**, sharpened to
   **M_{4,5} = 21 or M_{4,5} ≥ 23** by the K0821-audit convention (M = last
   witness width + 1; the last witness is 20 if none ever reappears, giving
   M = 21; a reappearing witness must sit at w ≥ 22 since 21 is verified
   witness-free, forcing M = w + 1 ≥ 23, so M = 22 is impossible); the upper
   bound 140 is unchanged. The witness-search frontier moves to 4x22 (a
   witness there gives M ≥ 23; witness-free there extends the free set to
   {21,22} and sharpens to M = 21 or ≥ 24).

## Verification

- Positive control: (4,20,5) class {0} k=3 minpos=1 SAT — 375,415 conflicts / 20.0 s;
  the decoded 15-stone witness is the V-image of the known m=20 witness (rows
  [4,4,4,3]), passing both the census-free `verifyConfig` (sat.js decode) and the
  independent pure-Python verifier (`verify_witness.py`).
- Cross-encoding controls: ctlx2b4 (4x20, --x2=4 window control) SAT 409,574
  conflicts; ctlgpA (4x20, g-pin control) SAT 240,930 — both decode to known-good
  witnesses, exercising the --x2 and g-pin encoders used by the split.
- Second verification (x2-split-verification-20261115.json): CNF regeneration md5
  matches for 4 sampled buckets (c0k3p1b7, c0k3p1b2, c0k3p0b1, c0k3p1b8);
  sample reruns of c0k3p0b1 and c0k3p1b8 reproduce the records bit-exactly
  (1,969,663 / 721,355 conflicts, both UNSATISFIABLE). The six pre-outage c0k3p1
  buckets b2..b7 (whose raw logs were lost to the 16:05Z execution-environment
  outage) were rerun post-reset from regenerated CNFs; all six reproduce their
  recorded conflict counts bit-exactly (977,786 / 1,082,095 / 1,023,149 / 810,664 /
  829,408 / 752,372). The recorded cnf_md5 of b4/b6 turned out to be one-character
  transcription slips of the true deterministic generation md5s (from the
  pre-outage records repair); the verdicts and conflict counts are unaffected and
  the regenerated md5s are recorded as authoritative in the same JSON.
- Erratum: the first published verification JSON recorded
  `m21_deciding_total_conflicts = 126,692,917`, which double-counts the 37 x2
  bucket conflicts (102,380,271 + 24,312,646). The correct deciding total from
  records.jsonl is **102,380,271**; the corrected value and the erratum note are
  recorded in the same JSON.
- Determinism/operational notes: sat4.js CNF generation is deterministic (idempotent
  md5); kissat 4.0.4 is deterministic per CNF. The c0k3p1b2 record was reconstructed
  from its raw run log after a records-repair incident (documented in the README);
  the post-reset rerun now reproduces it bit-exactly. Driver v2.1 uses comma-anchored
  resume keys to prevent prefix-collision silent skips.

## Scope

Finite machine verification up to the correctness of the K0810 census, the class-split
/ krow / minpos / x2 encodings and kissat 4.0.4; not a number-theoretic proof.
Persistence at m ≥ 22 remains open: exact M_{4,5} needs witness-free verification for
all widths up to U=140 or a universal tail argument. The 11x11 empty board,
two-stone root {49,60}, S2 {59,60} and their classes are unaffected and remain as
recorded. The 4x22 sweep is the next frontier (a strictly harder instance family;
the 4x21 experience — deep caps resisted by c0k3p0/c0k3p1 but the second-stone x2
split deciding each bucket in ≤ 185 s — suggests per-bucket splitting will decide it
too).
