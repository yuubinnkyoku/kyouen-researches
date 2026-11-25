# n11 central-reply closure: third-implementation cross-verification of batch-9 (class 1518) j033 + LOSS spots (2026-11-22)

Part T of the central-reply 19-root closure grind (K0415/K0417 line), declared
as an amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(pre-registered before the first target run; the declaration was pushed to
main ahead of the results).

## What this is

Batch 9 (`research/experiments/n11-centralreply-closure-class1518-batch9-20261122/`)
probed class 1518 (rank 8 clean candidate) and stopped at the pre-registered
WIN-HALT on **j033** (2-pass node-exact result 1, 4,718,280 nodes, s5_index
69347, key `[1153484455030030336, 0]`, legal 80, probe_order 364), leaving
rows j001-j033 raw (32 LOSS + 1 WIN) unconsumed and j034-j051 untouched.
Following the Part G / K / O / P precedents, this experiment runs the
**third implementation** (`third_impl.js`: non-df-pn AND/OR minimax with a
D4-canonical completion memo and slab TT; pinned bytes sha256 `08ea958f...`,
identical to the published experiments) as **verdict-level** cross-verification
of the batch-9 WIN row j033 plus three stratified LOSS spot rows
(j001 / j016 / j027, replica nodes 7.9M / 9.1M / 1.3M spanning nearly the
full batch-9 node range).

**It consumes and changes no corpus verdict. All gates and the canonical
chain cache are untouched. The standard 11x11 empty board, the 19
central-reply roots, class 1518/2634 and every closure class remain UNKNOWN.
Nodes/expansions are not verdicts. The j033 WIN remains unconsumed pending
the scrutiny owner (C++ second-implementation gate precedent, pinned
`9193f5b6...`).**

## Sources (published bytes only, machine-verified)

- `sources/raw/{j001,j016,j027,j033}.{p1,p2}.out`: byte-copies of the
  published batch-9 raws (8 files, refetched from main at the batch-9
  publication commit `a321bfb2` and compared byte-for-byte against the lane
  kit mirror - 8/8 identical; NOT republished here).
- `sources/batch-keys.json`: published batch-9 input declaration (51 keys,
  lo/hi as decimal strings), sha256
  `8f2035d17b3c987c8e5c848b23b6849ad5f3508a51d64002c1fef0e8c5ed7e9e`
  (pinned and enforced fail-closed by `make_inputs_batch9.py`; NOT
  republished here).
- `sources/status.log`: published batch-9 runner log (also byte-verified at
  `a321bfb2`); every target row must match its published
  `PASS 15000000,<result>,<nodes>` line, and the j033 WIN-HALT / RUNNER-STOP
  rc=45 stop lines are asserted present.
- Inputs `input/*.input.csv` and `input/rows.json` are derived from those
  sources by `scripts/make_inputs_batch9.py` (fail-closed: source passes must
  be 2-pass node-exact on legal/result/nodes/lo/hi, key/legal cross-checked
  against the published batch-keys.json and status.log).

## Targets (machine-derived, no hand transcription)

- 1 batch-9 WIN row: j033 (expected WIN 1 by the published replica)
- 3 batch-9 LOSS spot rows: j001, j016, j027 (expected LOSS 2)
- 2 published third-implementation anchors reproduced on this host:
  k02a (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy l1a (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175
  ttHits) - the same anchors as Part G/K/O/P
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02
  stones 6)

## Protocol

Identical to Part O/P: solver `scripts/third_impl.js` (byte-pinned), one
process per row, `--cap=300000000 --wallcap=240 --memo-power=22`, 2 runs
(a/b) per row; runner `scripts/run_thirdimpl.sh`; status log
`output/status.log`. Rule-engine gate before any target run
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
verdicts): **j033 WIN 1 agrees, 3/3 LOSS spots agree, 0 divergences,
0 wall-inconclusive**, all a/b run pairs identical on
(result, expansion, ttHits, overwrites).

Anchors on this host: k02a WIN 9,106,337 expansions / 4,991,527 ttHits and
l1a LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
third-implementation values (and the Part G/K/O/P host reproductions).
Negative gates: ng1/ng2 GATE_FAIL with the published messages.
Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0 mismatches.

## Row table (machine-generated; replica columns from the published raws)

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| j033 | WIN 1 (4,718,280) | **WIN 1** (5,392,392; ttHits 3,146,601) | a/b identical |
| j001 | LOSS 2 (7,908,824) | **LOSS 2** (9,103,477; ttHits 5,229,527) | a/b identical |
| j016 | LOSS 2 (9,112,205) | **LOSS 2** (10,556,205; ttHits 6,292,586) | a/b identical |
| j027 | LOSS 2 (1,255,316) | **LOSS 2** (1,401,488; ttHits 875,684) | a/b identical |

## Honesty record

The batch-9 rows are NOT consumed into any canonical cache (the batch-9
increment exists only in the Part R if-adopted analysis caches, which are
analysis-only and explicitly non-canonical). This verification creates
corroborating literature only: no verdict is consumed, no cache is modified,
no closure/coverage/root claim is made or changed. The j033 WIN stays
scrutiny-owner-blocked like b018/d002/e002/f017/g018. The standard 11x11
empty board, the 19 central-reply roots, class 1518 (batch 9, HALTed at
j033, j034-j051 untouched), class 2634 (batch 8, in progress under Part N)
and all remaining S5 keys remain UNKNOWN throughout. Expansions and node
counts are not verdicts.
