# n11 central-reply closure: third-implementation cross-verification of batch-12 (class 8106) WIN rows + probed LOSS (2026-11-22)

Part AD of the central-reply 19-root closure grind (K0415/K0417 line). The
scope was pre-registered in advance of execution as a note Part AD amendment
(single-owner note, declaration published before the first solver run);
batch 12 was probed under Part AC.

## What this is

Batch 12 (`research/experiments/n11-centralreply-closure-class8106-batch12-20261122/`)
probed class 8106 (renewed rank 10, Part AC declared) and WIN-HALTED at 8/52
keys in its second probe wave with **two WIN rows in the same wave**: n006
first (s5_index 219608, key `[1152926194711134208, 128]`, legal 78;
2-pass fresh cold node-exact replica result 1 (WIN), 3,695,373 nodes), then
n005 (s5_index 188395, key `[1153489144664555520, 0]`, legal 82; result 1,
12,863,268 nodes) - the first closure batch to surface two WIN rows. They
are the 9th and 10th unconsumed closure WINs. The two completed LOSS rows
of the same wave (n007/n008) and the all-LOSS wave 1 (n001-n004) are
disclosed honestly. Batch-12 probed 8/52 keys; n009-n052 (44 keys) are
untouched. Because the batch halted in the second wave, there is no separate
"stratified LOSS sample" - **the target set of this experiment is the entire
probed row set**: the two WIN rows n005/n006 plus all six probed LOSS rows
(n001-n004/n007/n008). Following the Part G / K / O / P / T / W / AA
precedents, this experiment runs the **third implementation**
(`third_impl.js`: non-df-pn AND/OR minimax with a D4-canonical completion
memo and slab TT; pinned bytes sha256 `08ea958f...`, identical to the
published experiments) as **verdict-level** cross-verification.

**It consumes and changes no corpus verdict. All gates and the canonical
chain cache (6,027 rows, sha256 `95e868d6...`) are untouched. The standard
11x11 empty board, the 19 central-reply roots, class 8106 (and every closure
class) remain UNKNOWN. Nodes/expansions are not verdicts. The n005/n006 WINs
remain unconsumed pending the scrutiny owner (C++ second-implementation
gate precedent, pinned `9193f5b6...`).**

## Sources (published bytes only, machine-verified)

- `sources/raw/n001..n008.{p1,p2}.out`: byte-copies of the published
  declaring-host batch-12 raws (16 files, chunk commits `eca35f3c` /
  `ace92d84`, fetched from main at those commits via the raw CDN,
  commit-pinned; NOT republished here).
- `sources/batch-keys.json`: published batch-12 input declaration (52 keys,
  lo/hi as decimal strings), sha256
  `de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2`,
  scaffold commit `d333bb2c` (pinned and enforced fail-closed by
  `make_inputs_batch12.py`; NOT republished here).
- `sources/status.log` (declaring-host runner log): every target row must
  match its published `PASS 15000000,<result>,<nodes>` line, the
  `n005 WIN-HALT` and `n006 WIN-HALT` stop lines and the
  `RUNNER-STOP`/`RUNNER-EXIT` lines are asserted PRESENT.
- Inputs `input/*.input.csv` and `input/rows.json` are derived from those
  sources by `scripts/make_inputs_batch12.py` (fail-closed: source passes
  must be 2-pass node-exact on legal/result/nodes/lo/hi, key/legal
  cross-checked against the published batch-keys.json, status lines asserted
  against `sources/status.log`, and - a check available because the
  declaring session published its input CSVs in the scaffold commit - the
  freshly derived input CSV of every target row must be byte-identical to
  the published batch-12 input CSV).

## Targets (machine-derived, no hand transcription)

- 2 batch-12 WIN rows: n005, n006 (expected WIN 1 by the published replica)
- 6 batch-12 LOSS rows: n001, n002, n003, n004, n007, n008 (expected LOSS 2)
  - the complete probed row set of the batch
- 2 published third-implementation anchors reproduced on this host:
  k02a (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy l1a (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175
  ttHits) - the same anchors as Part G/K/O/P/T/W/AA
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02
  stones 6)

## Protocol

Identical to Part K/O/P/T/W/AA: solver `scripts/third_impl.js`
(byte-pinned), one process per row, `--cap=300000000 --wallcap=240
--memo-power=22`, 2 runs (a/b) per row; runner `scripts/run_thirdimpl.sh`;
status log `output/status.log` (rows executed with at most 4 concurrent
solver processes; this 2-core host ran pairs). Rule-engine gate before any
target run (`scripts/verify_tbl.js`, forbidden-quad count 95,670 == replica;
TBL==wob on 195,044 deterministic triples, mismatches 0), captured in
`output/rules-gate.txt`. Determinism gate per row on
(result, expansion, ttHits, reason). Clean verdict agreement only is a
verification claim; a wall/cap `runlimit` is an honest wall-inconclusive
(not a verdict); a clean divergence would be recorded as divergence
evidence and would NOT rewrite any verdict or the canonical cache here.

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py` (fail-closed, schema `batch12-wins-thirdimpl-audit-v1`,
run twice byte-identical): **111/111 gates PASS**. Verdict agreements (third
implementation vs published pinned-replica verdicts): **n005 WIN 1 and n006
WIN 1 agree, 6/6 LOSS rows agree, 0 divergences, 0 wall-inconclusive**, all
a/b run pairs identical on (result, expansion, ttHits, reason).

Anchors on this host: k02a WIN 9,106,337 expansions / 4,991,527 ttHits and
l1a LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
third-implementation values (and the Part G/K/O/P/T/W/AA host
reproductions). Negative gates: ng1/ng2 GATE_FAIL with the published
messages. Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0
mismatches.

## Row table (machine-generated; replica columns from the published raws)

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| n005 | WIN 1 (12,863,268) | **WIN 1** (15,280,890; ttHits 8,220,782) | a/b identical |
| n006 | WIN 1 (3,695,373) | **WIN 1** (4,233,764; ttHits 2,394,370) | a/b identical |
| n001 | LOSS 2 (6,471,615) | **LOSS 2** (7,693,366; ttHits 4,108,116) | a/b identical |
| n002 | LOSS 2 (3,083,301) | **LOSS 2** (3,554,378; ttHits 1,980,011) | a/b identical |
| n003 | LOSS 2 (4,560,719) | **LOSS 2** (5,243,307; ttHits 3,022,331) | a/b identical |
| n004 | LOSS 2 (3,710,926) | **LOSS 2** (4,271,858; ttHits 2,406,756) | a/b identical |
| n007 | LOSS 2 (2,905,330) | **LOSS 2** (3,359,814; ttHits 1,856,397) | a/b identical |
| n008 | LOSS 2 (3,442,689) | **LOSS 2** (3,976,246; ttHits 2,188,728) | a/b identical |

With this experiment the ten closure-batch WINs are all third-implementation
corroborated at the spot level (n005/n006 here; z003 Part AA, b018 Part K,
d002/e002/f017 Part G, g018 Part K, j033 Part T, h045 Part W).

## Honesty record

The batch-12 rows are NOT consumed into any canonical cache. This
verification creates corroborating literature only: no verdict is consumed,
no cache is modified, no closure/coverage/root claim is made or changed.
The n005/n006 WINs stay scrutiny-owner-blocked like
b018/d002/e002/f017/g018/j033/h045/z003 (9th and 10th unconsumed closure
WINs). The standard 11x11 empty board, the 19 central-reply roots, class
8106 (batch 12 halted at 8/52, n009-n052 untouched) and all remaining S5
keys remain UNKNOWN throughout. Expansions and node counts are not
verdicts.
