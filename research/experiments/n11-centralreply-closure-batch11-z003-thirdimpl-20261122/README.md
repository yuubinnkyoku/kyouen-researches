# n11 central-reply closure: third-implementation cross-verification of batch-11 (class 8785) z003 + LOSS spots (2026-11-22)

Part AA of the central-reply 19-root closure grind (K0415/K0417 line). The
scope was pre-registered in advance of execution as a note Part AA amendment
(single-owner note, declaration published before the first solver run);
batch 11 was probed under Part Z.

## What this is

Batch 11 (`research/experiments/n11-centralreply-closure-class8785-batch11-20261122/`)
probed class 8785 (renewed rank 8, Part Z declared / takeover published) and
stopped at the pre-registered WIN-HALT in its very first wave on **z003**
(s5_index 198530, key `[1225542323476103168, 1]`, legal 82, probe_order 334;
replica result 1 (WIN), 11,601,265 nodes, 2-pass fresh cold node-exact; the
declaring host's value was re-reproduced node-exact by the takeover host and
both raw sets are published). The three in-flight LOSS rows of the same wave
(z001/z002/z004) completed and were disclosed honestly. Batch-11 probed
4/51 keys; z005-z051 are untouched. Because the batch halted in the first
wave, there is no separate "stratified LOSS sample" - **the target set of this
experiment is the entire probed row set**: the WIN row z003 plus all three
probed LOSS rows. Following the Part G / K / O / P / T / W precedents, this
experiment runs the **third implementation** (`third_impl.js`: non-df-pn AND/OR
minimax with a D4-canonical completion memo and slab TT; pinned bytes sha256
`08ea958f...`, identical to the published experiments) as **verdict-level**
cross-verification.

**It consumes and changes no corpus verdict. All gates and the canonical
chain cache (6,027 rows, sha256 `95e868d6...`) are untouched. The standard
11x11 empty board, the 19 central-reply roots, class 8785 (and every closure
class) remain UNKNOWN. Nodes/expansions are not verdicts. The z003 WIN
remains unconsumed pending the scrutiny owner (C++ second-implementation
gate precedent, pinned `9193f5b6...`).**

## Sources (published bytes only, machine-verified)

- `sources/raw/{z001,z002,z003,z004}.{p1,p2}.out`: byte-copies of the
  published declaring-host batch-11 raws (8 files) and
  `sources/raw/*.takeover.out`: the takeover-host fresh-cold cross-host
  reproduction rows (8 files); both sets republished together by the batch-11
  takeover commits (fetched from main at those commits via the raw CDN,
  commit-pinned; NOT republished here).
- `sources/batch-keys.json`: published batch-11 input declaration (51 keys,
  lo/hi as decimal strings), sha256
  `8ef2206986a87f3859aa0a4b25f9936ffa82001d1fd3214013dc6351ecf8b08b`,
  scaffold commit `3cc96099` (pinned and enforced fail-closed by
  `make_inputs_batch11.py`; NOT republished here).
- `sources/status.log` (declaring-host runner log) and
  `sources/status.takeover.log` (takeover-host reproduction log): every
  target row must match its published `PASS 15000000,<result>,<nodes>` line
  in BOTH logs (per-pass for the takeover log), the `z003 WIN-HALT` stop line
  is asserted present, and - unlike batch-8, whose runner wrote no stop lines
  - batch-11's `RUNNER-STOP`/`RUNNER-EXIT` lines are asserted PRESENT
  (schema honesty for this batch's actual log shape).
- Inputs `input/*.input.csv` and `input/rows.json` are derived from those
  sources by `scripts/make_inputs_batch11.py` (fail-closed: source passes
  must be 2-pass node-exact on legal/result/nodes/lo/hi, the takeover-host
  twins must agree field-for-field, key/legal cross-checked against the
  published batch-keys.json, and both status logs must agree).

## Targets (machine-derived, no hand transcription)

- 1 batch-11 WIN row: z003 (expected WIN 1 by the published replica)
- 3 batch-11 LOSS rows: z001, z002, z004 (expected LOSS 2) - the complete
  probed row set of the batch
- 2 published third-implementation anchors reproduced on this host:
  k02a (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy l1a (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175
  ttHits) - the same anchors as Part G/K/O/P/T/W
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02
  stones 6)

## Protocol

Identical to Part K/O/P/T/W: solver `scripts/third_impl.js` (byte-pinned),
one process per row, `--cap=300000000 --wallcap=240 --memo-power=22`, 2 runs
(a/b) per row; runner `scripts/run_thirdimpl.sh`; status log
`output/status.log` (rows executed with at most 4 concurrent solver
processes; this 2-core host ran pairs). Rule-engine gate before any target
run (`scripts/verify_tbl.js`, forbidden-quad count 95,670 == replica; TBL==wob
on 195,044 deterministic triples, mismatches 0), captured in
`output/rules-gate.txt`. Determinism gate per row on
(result, expansion, ttHits, reason). Clean verdict agreement only is a
verification claim; a wall/cap `runlimit` is an honest wall-inconclusive
(not a verdict); a clean divergence would be recorded as divergence
evidence and would NOT rewrite any verdict or the canonical cache here.

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py` (fail-closed, schema `batch11-z003-thirdimpl-audit-v1`,
run twice byte-identical): **71/71 gates PASS**. Verdict agreements (third
implementation vs published pinned-replica verdicts): **z003 WIN 1 agrees,
3/3 LOSS rows agree, 0 divergences, 0 wall-inconclusive**, all a/b run pairs
identical on (result, expansion, ttHits, reason).

Anchors on this host: k02a WIN 9,106,337 expansions / 4,991,527 ttHits and
l1a LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
third-implementation values (and the Part G/K/O/P/T/W host reproductions).
Negative gates: ng1/ng2 GATE_FAIL with the published messages.
Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0 mismatches.

## Row table (machine-generated; replica columns from the published raws)

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| z003 | WIN 1 (11,601,265) | **WIN 1** (13,781,596; ttHits 7,500,476) | a/b identical |
| z001 | LOSS 2 (3,146,511) | **LOSS 2** (3,594,991; ttHits 2,074,770) | a/b identical |
| z002 | LOSS 2 (2,256,914) | **LOSS 2** (2,547,371; ttHits 1,564,994) | a/b identical |
| z004 | LOSS 2 (6,424,054) | **LOSS 2** (7,426,794; ttHits 4,192,144) | a/b identical |

With this row the eight closure-batch WINs are all third-implementation
corroborated at the spot level (z003 here; b018 Part K, d002/e002/f017
Part G, g018 Part K, j033 Part T, h045 Part W).

## Honesty record

The batch-11 rows are NOT consumed into any canonical cache. This
verification creates corroborating literature only: no verdict is consumed,
no cache is modified, no closure/coverage/root claim is made or changed.
The z003 WIN stays scrutiny-owner-blocked like b018/d002/e002/f017/g018/
j033/h045 (8th unconsumed closure WIN). The standard 11x11 empty board, the
19 central-reply roots, class 8785 (batch 11 halted at z003, z005-z051
untouched) and all remaining S5 keys remain UNKNOWN throughout. Expansions
and node counts are not verdicts.
