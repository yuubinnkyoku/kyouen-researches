---
id: K0848
title: "6x22..6x59 q=8 row-deficient maximal nonexistence band (all 3 row-mirror rowY classes UNSAT per width) — witness-free width set of (6,8) extends to {19,...,59}, M_{6,8} = 19 or >= 61"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) and the sequential-counter/maximality core used verbatim (sat.js / sat2.js); the rowfixed unit clause is the only addition, exactly as in K0829"
- type: depends_on
  target: K0815
  note: "41-stone deficient-maximal witness at 6x18 (rows 7,6,7,7,7,7) is the lower bound M_{6,8} >= 19 and the positive-control board (row-mirror rows 7,7,7,7,6,7 rediscovered bit-exactly by the 6x18 def-OR control of this lane, 492,432 conflicts)"
- type: depends_on
  target: K0818
  note: "6x19 witness-free (35-class complete enumeration); first element of the witness-free set beyond the witness band 9..18"
- type: depends_on
  target: K0819
  note: "6x20 witness-free (same 35-class machinery); the K0819/K0818 items plus K0829 hold widths 19..21, this item extends the free set 22..59 with the cheaper 3-class rowY split"
- type: depends_on
  target: K0829
  note: "6x21 witness-free by the same rowfixed rowY split (3 mirror classes); this lane reproduces both its calibrations bit-exactly (6x21 rowY=1 UNSAT 2,862,649; 6x18 def-OR SAT 492,432) and generalizes the split across the band m=22..59"
- type: depends_on
  target: K0822
  note: "row-mirror canonical class logic (y -> 5-y pairs the 6 rows into 3 mirror classes), brute-force-validated there"
- type: depends_on
  target: K0825
  note: "rowY fixed-row split technique, applied on the UNSAT side with all mirror classes swept per width"
- type: depends_on
  target: K0318
  note: "substitution upper bound U_{6,8} = 371 (via K0806; K0024): witnesses cannot exist for m >= 371, so a witness-free sweep of 19..370 would close M_{6,8} = 19 exactly; this item carries the sweep to m=59"
- type: generalizes
  target: K0829
  note: "the same row-split proposition extended from the single width 6x21 to the band 6x22..6x59; witness-free width set {19,20,21} -> {19,...,59}"
artifacts:
- path: research/experiments/six-row-q8-m22-row-split-20261115/README.md
  role: proof
  note: "claim, per-width coverage argument (deficient config has a deficient row y captured by rowfixed(y); row-mirror soundness y<->5-y reduces 6 rows to 3 classes), full band results table m=22..59 (conflicts/process-time per instance, lex=H cross-checks, deciding totals), calibrations (K0829 bit-exact m=21 rowY=1 and 6x18 def-OR control, m=26 CNF regeneration byte-identical, cross-environment-reset re-runs of m=45..47 bit-exact), honest negatives, the m=53 V8-heap and m=60 RAM generation walls, scope and limits"
- path: research/experiments/six-row-q8-m22-row-split-20261115/output/records.jsonl
  role: data
  note: "155 records: per width m=22..59, the 3 rowY class UNSAT records (conflicts, wallMs, sat2.js encoding meta) + 1 lex=H cross-encoding UNSAT record each; plus the m=21 calibration, m=18 positive control, m=24 def-OR honest-negative INDET record; deciding totals noted per width in the lex=H record note"
- path: research/experiments/six-row-q8-m22-row-split-20261115/output/r6x22q8_rowY1.txt
  role: data
  note: "band-hardest raw kissat log (m=22 rowY=1: 2,162,296 conflicts UNSAT / 127.19 s); all 152 band raw logs r6x{22..59}q8_rowY{0,1,2}+rowY1_lexH.txt and the calibration/control logs are siblings in the same directory, all pushed with remote git blob shas verified against local sha1"
- path: research/experiments/six-row-q8-m22-row-split-20261115/scripts/decode_verify.js
  role: solver
  note: "kissat model decoder + census-free js verifyConfig runner used for the 6x18 positive-control witness dual verification (with verify_witness.py, Python Fraction)"
scope: "'finite machine verification (kissat 4.0.4: 38 widths x 3 rowY UNSAT instances + 38 lex=H cross-encoding re-checks + positive control; widths 6x22..6x59 q=8 only; widths 19..21 from K0818/K0819/K0829, witnesses 9..18 from K0808..K0815).'"
evidence: "'complete-coverage-by-row-mirror-split per width (verification: deterministic-machine + independent-encoding-cross-check per width + positive control rediscovering the K0815 board + cross-reset bit-exact calibration). See the experiment README.'"
---

# 6x22..6x59 q=8 row-deficient maximal nonexistence band — 3 row-mirror rowY classes UNSAT per width

## Claim

1. On the 6xm integer grid with q=8, for every width m in {22,...,59} and each
   of the 3 row-mirror-canonical row classes y ∈ {0,1,2} (covering all 6
   rows via the V mirror y -> 5-y), the rowfixed SAT instance — row y holds
   at most 6 stones (unit ¬rowGe[y]), other rows free, safety ≤ 7 stones per
   row (a row is a line of length m ≥ q) and per census curve, maximality
   (every empty cell covered by a ≥7-stone curve) — is **UNSAT** (kissat
   4.0.4, exit 20; sat2.js K0810 census + sequential counter + maximality
   encoding). Per width a lex=H cross-encoding re-check of the rowY=1
   class is also UNSAT. 0 SAT, 0 INDET among the deciding instances.
2. Coverage (identical to K0829, applied per width): every deficient maximal
   safe configuration has some row with ≤ 6 stones and appears as a solution
   of the rowfixed(y) instance for that row; the V mirror y <-> 5-y is a
   board symmetry, so rowfixed(y) is equisatisfiable with rowfixed(5-y) and
   y ∈ {0,1,2} covers all 6 rows. Hence **no row-deficient maximal safe
   configuration exists on 6xm for any m in {22,...,59}**; every maximal
   safe configuration on those boards has 42 stones.
3. Combined with K0818 (6x19 free), K0819 (6x20 free), K0829 (6x21 free) and
   K0815 (41-stone deficient maximal at 6x18, least witness width 18 — the
   lower bound M_{6,8} ≥ 19): the witness-free width set of (6,8) is
   **{19, 20, ..., 59}**, so **M_{6,8} ∈ {19,...,59} or M_{6,8} ≥ 61**,
   sharpened per the K0821-audit convention to **M_{6,8} = 19 or
   M_{6,8} ≥ 61**. The upper bound 371 (K0318/K0806 substitution) is
   unchanged. The witness-search frontier moves to 6x60.

## Method

Same machinery as K0829 (sat2.js verbatim, kissat 4.0.4 official
linux-amd64), swept across the band: per width, 3 rowY instances + 1 lex=H
cross-encoding. Difficulty collapsed across the band: the hardest-class
(rowY=1 through m=43) conflict series fell from 2,862,649 (m=21, K0829) to
54,643 (m=43) — a factor of ~52; deciding totals fell from 4,291,607 (m=22)
to a local minimum 149,978 (m=48), then levelled off in the
149,978..235,196 range through m=59 with the hardest class alternating
between y=0 and y=1. From m=53 the CNF generation needed
`--max-old-space-size` above the V8 default (~512 MB census heap); at m=60
generation hits the environment RAM cap (kernel kill; heap 900 marginal,
1400 instant kill, 800 JS-OOM) — a generation wall, not a solver wall:
**sat2.js band frontier m=59; m ≥ 60 is the territory of the parallel IN
FLIGHT experiment `six-row-q8-band-closure-22-370-20261114`** (genfast3.js
chord-pair census, valid q ≥ w+2, already calibrated there: CNF
byte-identity vs sat2.js on 6 samples, instance-identity 2/2). A full
witness-free sweep 19..370 would close M_{6,8} = 19 exactly (with U=371).

## Verification

- Calibrations, all bit-exact: 6x21 rowY=1 UNSAT 2,862,649 (K0829 record,
  reproduced twice in-lane); 6x18 def-OR positive control SAT 492,432,
  decoded 41-stone witness rows [7,7,7,7,6,7] element-identical to the
  K0829 control board, js census-free verifyConfig + Python Fraction
  verify_witness.py both PASS (reproduced twice); m=26 CNF regeneration
  after the sweep byte-identical (cmp PASS).
- Environment-reset crossing: a hard reset wiped the local workdir
  mid-band (after m=45..47, before their logs were pushed); machinery was
  re-fetched from this repo and hash-verified (sat.js 6c3262d6, sat2.js
  edfae1d2, verify_witness.py ea7203a3, decode_verify.js ef5390509b, kissat
  md5 3a5eba830aa6008a604fcc9bbe99a325) and m=45, 46, 47 were re-run with
  every conflict count bit-exact vs the pre-reset runs.
- Honest negatives: 6x24 def-OR INDET at the 140 s cap (3,248,777
  conflicts) — nonexistence for m=24 rests on the rowY split; m=60
  generation OOM/kill records are transport/infrastructure negatives, not
  mathematical ones.
- All 155 records and all raw logs pushed with remote git blob shas
  verified against local sha1.

## Scope

Finite machine verification up to the correctness of the K0810 census, the
rowfixed encoding (mirror soundness brute-force-validated in K0818), and
kissat 4.0.4; not a number-theoretic proof (same evidence level as
K0818/K0819/K0829). Persistence at m ≥ 60 remains open: exact M_{6,8}
needs witness-free verification for all widths up to the K0318/K0024 bound
U=371 (claimed by the band-closure lane) or a universal tail argument in
the spirit of K0342. The 11x11 empty board, two-stone root {49,60}, S2
{59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
