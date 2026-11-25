# n11 central-reply closure: third-implementation cross-verification of batch-13 (class 16930) WIN rows + probed LOSS (2026-11-22)

Part AG of the central-reply 19-root closure grind (K0415/K0417 line). The
scope was pre-registered in advance of execution as a note Part AG amendment
(single-owner note, declaration published as commit `e84242c8` before the
first solver run); batch 13 was probed under Part AE, batch 14 (class 23101)
was declared and is being probed under Part AF by a parallel session and is
not touched here.

## What this is

Batch 13 (`research/experiments/n11-centralreply-closure-class16930-batch13-20261122/`)
probed class 16930 (renewed rank 11, Part AE declared) and WIN-HALTED at 4/52
keys in its first probe wave with **two WIN rows in the same wave**: p003
first (s5_index 203419, key `[3458764514088976384, 272]`, legal 81;
2-pass fresh cold node-exact replica result 1 (WIN), 7,489,274 nodes), then
p002 (s5_index 185003, key `[1153484454828703744, 272]`, legal 85; result 1,
10,770,254 nodes). They are the **11th and 12th unconsumed closure WINs**
(b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003). The two
completed LOSS rows of the same wave (p001/p004) are disclosed honestly.
Batch-13 probed 4/52 keys; p005-p052 (48 keys) are untouched. Following the
Part G / K / O / P / T / W / AA / AD precedents, this experiment runs the
**third implementation** (`third_impl.js`: non-df-pn AND/OR minimax with a
D4-canonical completion memo and slab TT; pinned bytes sha256 `08ea958f...`,
identical to the published experiments) as **verdict-level**
cross-verification of the complete probed row set.

**It consumes and changes no corpus verdict. All gates and the canonical
merged cache (6,027 rows, sha256 `95e868d6...`) are untouched. The standard
11x11 empty board, the 19 central-reply roots, class 16930 (and every closure
class) remain UNKNOWN. Nodes/expansions are not verdicts. The p002/p003 WINs
remain unconsumed pending the scrutiny owner (C++ second-implementation gate
precedent, pinned `9193f5b6...`).**

## Sources (published bytes only, machine-verified)

- `sources/raw/p001..p004.{p1,p2}.out`: byte-copies of the published
  declaring-host batch-13 raws (8 files, chunk commit `b4b55ec8`, fetched from
  main at that commit via the raw CDN, commit-pinned; NOT republished here).
  Cross-checked against the parallel session's kit mirror on this shared
  knowledge volume: 10/10 byte-identical.
- `sources/batch-keys.json`: published batch-13 input declaration (52 keys,
  lo/hi as decimal strings), sha256
  `c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7`,
  scaffold commit `90ee1c87` (pinned and enforced fail-closed by
  `make_inputs_batch13.py`; NOT republished here).
- `sources/status.log` (declaring-host runner log): every target row must
  match its published `PASS 15000000,<result>,<nodes>` line; the
  `p003 WIN-HALT` and `p002 WIN-HALT` stop lines and the
  `RUNNER-STOP`/`RUNNER-EXIT` lines are asserted PRESENT.
- Inputs `input/*.input.csv` and `input/rows.json` are derived from those
  sources by `scripts/make_inputs_batch13.py` (Part AD's batch-12 script
  adapted: EXP/schema strings renamed to `batch13-wins-thirdimpl-*`,
  class_index pin 16930, target list p002/p003/p001/p004 per the Part AE
  template warning on stale template strings; fail-closed: source passes
  must be 2-pass node-exact on legal/result/nodes/lo/hi, key/legal
  cross-checked against the published batch-keys.json, status lines asserted
  against `sources/status.log`, and the freshly derived input CSV of every
  target row must be byte-identical to the published batch-13 input CSV).

## Targets (machine-derived, no hand transcription)

- 2 batch-13 WIN rows: p002, p003 (expected WIN 1 by the published replica)
- 2 batch-13 LOSS rows: p001, p004 (expected LOSS 2)
  - the complete probed row set of the batch
- 2 published third-implementation anchors reproduced on this host:
  k02a (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy l1a (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175
  ttHits) - the same anchors as Part G/K/O/P/T/W/AA/AD
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02
  stones 6)

## Protocol

Identical to Part K/O/P/T/W/AA/AD: solver `scripts/third_impl.js`
(byte-pinned), one process per row, `--cap=300000000 --wallcap=240
--memo-power=22`, 2 runs (a/b) per row; runner `scripts/runner-all-thirdimpl.sh`;
status log `output/status.log` (this 2-core host ran pairs, at most 2
concurrent solver processes). Rule-engine gate before any target run
(`scripts/verify_tbl.js`, forbidden-quad count 95,670 == replica; TBL==wob
on 195,044 deterministic triples, mismatches 0), captured in
`output/rules-gate.txt`. Determinism gate per row on
(result, expansion, ttHits, reason). Clean verdict agreement only is a
verification claim; a wall/cap `runlimit` is an honest wall-inconclusive
(not a verdict); a clean divergence would be recorded as divergence
evidence and would NOT rewrite any verdict or the canonical cache here.

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py` (fail-closed, schema `batch13-wins-thirdimpl-audit-v1`,
run twice byte-identical): **71/71 gates PASS**. Verdict agreements (third
implementation vs published pinned-replica verdicts): **p002 WIN 1 and p003
WIN 1 agree, 2/2 LOSS rows agree, 0 divergences, 0 wall-inconclusive**, all
a/b run pairs identical on (result, expansion, ttHits, reason).

Anchors on this host: k02a WIN 9,106,337 expansions / 4,991,527 ttHits and
l1a LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
third-implementation values (and the Part G/K/O/P/T/W/AA/AD host
reproductions). Negative gates: ng1/ng2 GATE_FAIL with the published
messages. Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob,
0 mismatches.

## Row table (machine-generated; replica columns from the published raws)

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| p002 | WIN 1 (10,770,254) | **WIN 1** (12,593,747; ttHits 7,021,485) | a/b identical |
| p003 | WIN 1 (7,489,274) | **WIN 1** (8,626,319; ttHits 4,959,871) | a/b identical |
| p001 | LOSS 2 (4,631,275) | **LOSS 2** (5,334,954; ttHits 3,020,029) | a/b identical |
| p004 | LOSS 2 (2,291,059) | **LOSS 2** (2,593,393; ttHits 1,571,815) | a/b identical |

With this experiment the **twelve** closure-batch WINs are all
third-implementation corroborated at the verdict level (b018/d002/e002/f017
Part G, g018 Part K, j033 Part T, h045 Part W, z003 Part AA, n005/n006
Part AD, p002/p003 here).

## Honesty record

The batch-13 rows are NOT consumed into any canonical cache. This
verification creates corroborating literature only: no verdict is consumed,
no cache is modified, no closure/coverage/root claim is made or changed.
The p002/p003 WINs stay scrutiny-owner-blocked like
b018/d002/e002/f017/g018/j033/h045/z003/n005/n006 (11th and 12th unconsumed
closure WINs). The standard 11x11 empty board, the 19 central-reply roots,
class 16930 (batch 13 halted at 4/52, p005-p052 untouched) and all remaining
S5 keys remain UNKNOWN throughout. Expansions and node counts are not
verdicts.

Execution disclosure: the runner chained the two negative gates with `&&`
after ng1, so ng1 (which exits rc=1 by design on GATE_FAIL) suppressed ng2
inside the runner; ng2 was executed immediately after the runner's exit on
this host, before any publish, and both negative outputs are audited by the
same fail-closed gate battery (`neg-ng1-failclosed`, `neg-ng2-failclosed`).
All target/anchor runs happened inside the runner (see `output/status.log`).
Wall times per solver run stayed far below the 240 s wallcap (max 76.75 s).

## Publication record (repo main, 2026-11-22)

Published as
`research/experiments/n11-centralreply-closure-batch13-wins-thirdimpl-20261122/`:
scaffold commit (README + pinned scripts 7 + machine-derived inputs 9) ->
targets commit (8 rows) -> completion commit (anchors 4 + negative 2 +
rules-gate + status.log + audit-summary.json + MANIFEST). Fetch-back
verification (commit-pinned raw URL + cmp): all published files byte-exact;
MANIFEST sha256 exact. Note Part AG publication status update published
afterward. All twelve unconsumed closure WINs
(b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003) now
third-implementation corroborated at the verdict level; verdicts remain
unconsumed; class status UNKNOWN throughout.
