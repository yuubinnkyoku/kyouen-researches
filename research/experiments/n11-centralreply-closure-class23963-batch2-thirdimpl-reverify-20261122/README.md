# n11 central-reply closure: third-implementation cross-verification of batch-2 (class 23963) rows (2026-11-22)

Part P of the central-reply 19-root closure grind (K0415/K0417 line), declared
as an amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(pre-registered before the first target run; publishes the declaration on main
ahead of the results).

## What this is

Batch 2 (`research/experiments/n11-centralreply-closure-class23963-batch-20261122/`)
probed all 48 pre-registered keys c001-c048 and settled **every row exact LOSS**
(2-pass node-exact at budget 15M, pinned replica `jsreplay.js` sha256
`84585617...`). Its 67-row fail-closed increment was merged into the chain
cache and class 23963 was certified as the **first Board-verified free class**
(33rd of the current 34) by the refresh re-audit - i.e. the corpus verdicts
were already consumed. Following the Part G (batches 1/3/4/5), Part K
(batch 6) and Part O (batch 7) precedents, this experiment runs the
**third implementation** (`third_impl.js`: non-df-pn AND/OR minimax with a
D4-canonical completion memo and slab TT; pinned bytes sha256 `08ea958f...`,
identical to the published experiments) as **verdict-level** cross-verification
of all 48 raw rows - a post-hoc corroboration of an already-consumed evidence
bundle.

**It consumes and changes no corpus verdict. All gates and the canonical
chain cache are untouched. The standard 11x11 empty board, the 19
central-reply roots, and every closure class remain UNKNOWN.
Nodes/expansions are not verdicts.**

## Sources (published bytes only, machine-verified)

- `sources/raw/c001..c048.{p1,p2}.out`: byte-copies of the published batch-2
  raws (96 files, refetched from main and compared byte-for-byte against the
  lane kit mirror - 96/96 identical; NOT republished here).
- `sources/batch-keys.json`: published batch-2 input declaration,
  sha256 `3b37c92387336407d6399a689befb2fad99e01520a390294a2370daa11e631e3`
  (pinned and enforced fail-closed by `make_inputs_batch2.py`).
- Inputs `input/*.input.csv` and `input/rows.json` are derived from those
  sources by `scripts/make_inputs_batch2.py` (fail-closed: source passes must
  be 2-pass node-exact on legal/result/nodes/lo/hi, key/legal cross-checked
  against the published batch-keys.json, replica verdict must be LOSS 2 on
  every row).

## Targets (machine-derived, no hand transcription)

- 48 batch-2 rows: c001-c048 (full coverage; every row expected LOSS 2)
- 2 published third-implementation anchors reproduced on this host:
  k02 (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy L1 (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175
  ttHits) - the same anchors as Part G/K/O
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02
  stones 6)

## Protocol

Identical to Part O: solver `scripts/third_impl.js` (byte-pinned), one
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

`scripts/audit.py` (fail-closed, run twice byte-identical): **511/511 gates
PASS**. Verdict agreements (third implementation vs published pinned-replica
verdicts): **48/48 LOSS 2, 0 divergences, 0 wall-inconclusive**, all a/b run
pairs identical on (result, expansion, ttHits, overwrites); third-impl
expansions 636,315-4,341,425 (replica df-pn nodes 579,880-3,815,424 on the
same rows).

Anchors on this host: k02 WIN 9,106,337 expansions / 4,991,527 ttHits and l1
LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
third-implementation values (and the Part G/K/O host reproductions).
Negative gates: ng1/ng2 GATE_FAIL with the published messages.
Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0 mismatches.

## Row table (machine-generated; replica columns from the published raws)

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| c001 | LOSS 2 (882,800) | **LOSS 2** (988,682; ttHits 621,536) | a/b identical |
| c002 | LOSS 2 (1,382,274) | **LOSS 2** (1,529,443; ttHits 996,420) | a/b identical |
| c003 | LOSS 2 (872,116) | **LOSS 2** (977,438; ttHits 613,693) | a/b identical |
| c004 | LOSS 2 (1,543,109) | **LOSS 2** (1,736,005; ttHits 1,054,581) | a/b identical |
| c005 | LOSS 2 (1,869,115) | **LOSS 2** (2,115,744; ttHits 1,254,415) | a/b identical |
| c006 | LOSS 2 (3,350,476) | **LOSS 2** (3,801,003; ttHits 2,278,186) | a/b identical |
| c007 | LOSS 2 (2,103,218) | **LOSS 2** (2,366,646; ttHits 1,454,298) | a/b identical |
| c008 | LOSS 2 (1,424,581) | **LOSS 2** (1,574,074; ttHits 1,042,070) | a/b identical |
| c009 | LOSS 2 (1,017,148) | **LOSS 2** (1,131,274; ttHits 712,990) | a/b identical |
| c010 | LOSS 2 (1,292,880) | **LOSS 2** (1,462,518; ttHits 867,348) | a/b identical |
| c011 | LOSS 2 (1,755,039) | **LOSS 2** (1,995,092; ttHits 1,166,420) | a/b identical |
| c012 | LOSS 2 (1,340,129) | **LOSS 2** (1,486,051; ttHits 976,177) | a/b identical |
| c013 | LOSS 2 (1,926,841) | **LOSS 2** (2,171,632; ttHits 1,317,072) | a/b identical |
| c014 | LOSS 2 (1,238,263) | **LOSS 2** (1,386,164; ttHits 858,105) | a/b identical |
| c015 | LOSS 2 (1,699,207) | **LOSS 2** (1,914,639; ttHits 1,150,664) | a/b identical |
| c016 | LOSS 2 (2,246,752) | **LOSS 2** (2,541,551; ttHits 1,514,849) | a/b identical |
| c017 | LOSS 2 (1,097,204) | **LOSS 2** (1,223,518; ttHits 770,049) | a/b identical |
| c018 | LOSS 2 (2,044,730) | **LOSS 2** (2,321,135; ttHits 1,361,832) | a/b identical |
| c019 | LOSS 2 (2,032,926) | **LOSS 2** (2,308,341; ttHits 1,364,366) | a/b identical |
| c020 | LOSS 2 (896,668) | **LOSS 2** (993,917; ttHits 639,746) | a/b identical |
| c021 | LOSS 2 (2,163,651) | **LOSS 2** (2,448,116; ttHits 1,460,322) | a/b identical |
| c022 | LOSS 2 (1,254,583) | **LOSS 2** (1,407,704; ttHits 874,240) | a/b identical |
| c023 | LOSS 2 (1,681,334) | **LOSS 2** (1,893,895; ttHits 1,156,634) | a/b identical |
| c024 | LOSS 2 (739,550) | **LOSS 2** (819,539; ttHits 529,772) | a/b identical |
| c025 | LOSS 2 (1,265,496) | **LOSS 2** (1,414,590; ttHits 890,494) | a/b identical |
| c026 | LOSS 2 (2,010,538) | **LOSS 2** (2,262,151; ttHits 1,376,957) | a/b identical |
| c027 | LOSS 2 (1,419,139) | **LOSS 2** (1,592,621; ttHits 981,800) | a/b identical |
| c028 | LOSS 2 (3,096,528) | **LOSS 2** (3,479,357; ttHits 2,105,439) | a/b identical |
| c029 | LOSS 2 (931,393) | **LOSS 2** (1,027,322; ttHits 671,132) | a/b identical |
| c030 | LOSS 2 (905,163) | **LOSS 2** (1,002,160; ttHits 655,633) | a/b identical |
| c031 | LOSS 2 (1,988,699) | **LOSS 2** (2,235,712; ttHits 1,352,580) | a/b identical |
| c032 | LOSS 2 (1,020,107) | **LOSS 2** (1,133,028; ttHits 720,068) | a/b identical |
| c033 | LOSS 2 (1,972,119) | **LOSS 2** (2,203,712; ttHits 1,382,824) | a/b identical |
| c034 | LOSS 2 (579,880) | **LOSS 2** (636,315; ttHits 425,961) | a/b identical |
| c035 | LOSS 2 (1,887,012) | **LOSS 2** (2,141,940; ttHits 1,268,983) | a/b identical |
| c036 | LOSS 2 (1,591,928) | **LOSS 2** (1,799,490; ttHits 1,079,838) | a/b identical |
| c037 | LOSS 2 (913,279) | **LOSS 2** (1,021,587; ttHits 636,693) | a/b identical |
| c038 | LOSS 2 (1,430,647) | **LOSS 2** (1,595,284; ttHits 996,306) | a/b identical |
| c039 | LOSS 2 (3,815,424) | **LOSS 2** (4,341,425; ttHits 2,544,990) | a/b identical |
| c040 | LOSS 2 (1,039,902) | **LOSS 2** (1,165,190; ttHits 712,822) | a/b identical |
| c041 | LOSS 2 (1,657,429) | **LOSS 2** (1,864,030; ttHits 1,147,009) | a/b identical |
| c042 | LOSS 2 (1,633,439) | **LOSS 2** (1,833,653; ttHits 1,115,186) | a/b identical |
| c043 | LOSS 2 (1,143,085) | **LOSS 2** (1,288,868; ttHits 784,205) | a/b identical |
| c044 | LOSS 2 (1,156,298) | **LOSS 2** (1,286,819; ttHits 821,072) | a/b identical |
| c045 | LOSS 2 (1,792,096) | **LOSS 2** (2,027,553; ttHits 1,215,194) | a/b identical |
| c046 | LOSS 2 (1,693,883) | **LOSS 2** (1,921,977; ttHits 1,132,158) | a/b identical |
| c047 | LOSS 2 (2,128,376) | **LOSS 2** (2,435,227; ttHits 1,393,273) | a/b identical |
| c048 | LOSS 2 (1,578,155) | **LOSS 2** (1,778,288; ttHits 1,078,977) | a/b identical |

## Honesty record

The batch-2 rows were already consumed into the canonical chain cache before
this experiment. This verification creates corroborating literature only:
no verdict is consumed, no cache is modified, no closure/coverage/root claim
is made or changed. The standard 11x11 empty board, the 19 central-reply
roots, class 2634 (batch 8, in progress under Part N) and all remaining S5
keys remain UNKNOWN throughout. Expansions and node counts are not verdicts.
