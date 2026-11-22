# n11 central-reply closure: third-implementation cross-verification of batch-8 (class 2634) h045 + LOSS spots (2026-11-22)

Part W of the central-reply 19-root closure grind (K0415/K0417 line). The
scope was pre-registered as open by note Part V (published commit
`267ead27`); execution followed in the same session and this experiment is
published together with its note amendment.

## What this is

Batch 8 (`research/experiments/n11-centralreply-closure-class2634-batch8-20261122/`)
probed class 2634 (rank 7, Part N declared / Part U takeover) and stopped at
the pre-registered WIN-HALT on **h045** (2-pass node-exact result 1,
6,366,900 nodes, s5_index 103558, key `[4035225266258182144, 64]`, legal 85,
probe_order 325), leaving rows h001-h044 (43 LOSS + the honest 15M
budget-exhaustion UNKNOWN h002) unconsumed and h046-h051 untouched.
Following the Part G / K / O / P / T precedents, this experiment runs the
**third implementation** (`third_impl.js`: non-df-pn AND/OR minimax with a
D4-canonical completion memo and slab TT; pinned bytes sha256 `08ea958f...`,
identical to the published experiments) as **verdict-level** cross-verification
of the batch-8 WIN row h045 plus three stratified LOSS spot rows (h018 /
h026 / h025, replica nodes 1.56M / 4.28M / 11.19M spanning nearly the full
batch-8 probed node range; h026 is the takeover rescue cross-check row,
h025 a declaring-host row).

**It consumes and changes no corpus verdict. All gates and the canonical
chain cache are untouched. The standard 11x11 empty board, the 19
central-reply roots, class 1518/2634 and every closure class remain UNKNOWN.
Nodes/expansions are not verdicts. The h045 WIN remains unconsumed pending
the scrutiny owner (C++ second-implementation gate precedent, pinned
`9193f5b6...`).**

## Sources (published bytes only, machine-verified)

- `sources/raw/{h018,h025,h026,h045}.{p1,p2}.out`: byte-copies of the
  published batch-8 raws (8 files, fetched from main at the batch-8
  WIN-HALT publication commit `1f127fb8` via the raw CDN, commit-pinned;
  NOT republished here).
- `sources/batch-keys.json`: published batch-8 input declaration (51 keys,
  lo/hi as decimal strings), sha256
  `5c42a950c687bbd1b8a9e25b1fdd5cffb4b7a19565a3d4372173a2001fcccc02`
  (pinned and enforced fail-closed by `make_inputs_batch8.py`; NOT
  republished here).
- `sources/status.log`: published batch-8 runner log (also fetched at
  `1f127fb8`); every target row must match its published
  `PASS 15000000,<result>,<nodes>` line, and the `h045 WIN-HALT` stop line
  is asserted present (the batch-8 runner writes no RUNNER-STOP line -
  asserted absent for schema honesty).
- Inputs `input/*.input.csv` and `input/rows.json` are derived from those
  sources by `scripts/make_inputs_batch8.py` (fail-closed: source passes must
  be 2-pass node-exact on legal/result/nodes/lo/hi, key/legal cross-checked
  against the published batch-keys.json and status.log).

## Targets (machine-derived, no hand transcription)

- 1 batch-8 WIN row: h045 (expected WIN 1 by the published replica)
- 3 batch-8 LOSS spot rows: h018, h025, h026 (expected LOSS 2)
- 2 published third-implementation anchors reproduced on this host:
  k02a (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy l1a (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175
  ttHits) - the same anchors as Part G/K/O/P/T
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02
  stones 6)

## Protocol

Identical to Part K/O/P/T: solver `scripts/third_impl.js` (byte-pinned), one
process per row, `--cap=300000000 --wallcap=240 --memo-power=22`, 2 runs
(a/b) per row; runner `scripts/run_thirdimpl.sh`; status log
`output/status.log` (rows executed with at most 4 concurrent solver
processes). Rule-engine gate before any target run
(`scripts/verify_tbl.js`, forbidden-quad count 95,670 == replica; TBL==wob
on 195,044 deterministic triples, mismatches 0), captured in
`output/rules-gate.txt`. Determinism gate per row on
(result, expansion, ttHits, reason). Clean verdict agreement only is a
verification claim; a wall/cap `runlimit` is an honest wall-inconclusive
(not a verdict); a clean divergence would be recorded as divergence
evidence and would NOT rewrite any verdict or the canonical cache here.

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py` (fail-closed, run twice byte-identical): **71/71 gates
PASS**. Verdict agreements (third implementation vs published pinned-replica
verdicts): **h045 WIN 1 agrees, 3/3 LOSS spots agree, 0 divergences,
0 wall-inconclusive**, all a/b run pairs identical on
(result, expansion, ttHits, overwrites).

Anchors on this host: k02a WIN 9,106,337 expansions / 4,991,527 ttHits and
l1a LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
third-implementation values (and the Part G/K/O/P/T host reproductions).
Negative gates: ng1/ng2 GATE_FAIL with the published messages.
Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0 mismatches.

## Row table (machine-generated; replica columns from the published raws)

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| h045 | WIN 1 (6,366,900) | **WIN 1** (7,348,868; ttHits 4,145,900) | a/b identical |
| h018 | LOSS 2 (1,556,298) | **LOSS 2** (1,756,741; ttHits 1,066,681) | a/b identical |
| h026 | LOSS 2 (4,284,312) | **LOSS 2** (4,938,236; ttHits 2,884,833) | a/b identical |
| h025 | LOSS 2 (11,192,861) | **LOSS 2** (13,169,795; ttHits 7,161,043) | a/b identical |

With this row the seven closure-batch WINs are all third-implementation
corroborated at the spot level: b018 (Part K), d002/e002/f017 (Part G),
g018 (Part K), j033 (Part T), h045 (Part W, this experiment).

## Honesty record

The batch-8 rows are NOT consumed into any canonical cache (the batch-8
increments exist only in the Part V if-adopted analysis caches, which are
analysis-only and explicitly non-canonical). This verification creates
corroborating literature only: no verdict is consumed, no cache is modified,
no closure/coverage/root claim is made or changed. The h045 WIN stays
scrutiny-owner-blocked like b018/d002/e002/f017/g018/j033. The standard
11x11 empty board, the 19 central-reply roots, class 2634 (batch 8, HALTed
at h045, h046-h051 untouched, h002 an honest exhaustion UNKNOWN not
re-searched at the same condition) and all remaining S5 keys remain UNKNOWN
throughout. Expansions and node counts are not verdicts.
