# n11 central-reply closure: third-implementation cross-verification of batch-7 (class 10324) rows (2026-11-22)

NOTE (publish-time lettering): this amendment ships on main as **Part O**.
It was staged during the 2026-11-22 repo-outage window under the kit-local
letter "Part M" (timestamp 2026-11-22T05:58Z); on repo recovery the letters
M (class-10324 closure merge + re-audit) and N (batch 8, class 2634) were
issued first, so the kit lettering is not used on main. The declaration is
an amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

## Publish-time status note (2026-11-22, publishing session)

At publication time the fail-closed merge + refresh re-audit this experiment
anticipated is already on main (note Part M: class 10324 certified as the
34th Board-verified free class; merged canonical cache 5,975 rows
`a998f4c0...`). This experiment therefore stands as a post-hoc
cross-implementation corroboration of the published class-10324 evidence
bundle; it still consumes no verdict and re-runs no corpus pipeline.

## What this is

Batch 7 (`research/experiments/n11-centralreply-closure-class10324-batch7-20261122/`)
probed all 51 pre-registered keys h001-h051 and settled **every row exact LOSS**
(2-pass node-exact at budget 15M, pinned replica `jsreplay.js` sha256
`84585617...`), making class 10324 the second closure candidate after 23963.
Following the Part G (batches 1/3/4/5) and Part K (batch 6) precedents, this
experiment runs the **third implementation** (`third_impl.js`: non-df-pn AND/OR
minimax with a D4-canonical completion memo and slab TT; pinned bytes sha256
`08ea958f...`, identical to the published experiments) as **verdict-level**
cross-verification of all 51 raw rows, hardening the closure evidence bundle
before any merge/re-audit step.

**It consumes and changes no corpus verdict. All pre-existing gates are untouched.
The standard 11x11 empty board, the 19 central-reply roots, and every closure
class remain UNKNOWN. Nodes/expansions are not verdicts.**

## Declaration circumstance (honest disclosure)

The repository public endpoints (api.github.com, raw CDN, github_app connector)
returned 404 throughout this window (since 2026-11-22 ~04:52Z; recorded in the
lane kit `batch5473-note.md`). The declaration was staged with a
timestamp (`2026-11-22T05:58Z`, single-owner note amendment, kit-local letter
"Part M" - see the publish-time lettering note above) in the lane kit
before the first target run and ships together with the results on repo
recovery - the same deviation already disclosed by Part K/Part L.

## Targets (machine-derived, no hand transcription)

- 51 batch-7 rows: h001-h051 (full coverage; every row expected LOSS 2)
- 2 published third-implementation anchors reproduced on this host:
  k02 (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy L1 (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175 ttHits)
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02 stones 6)

Inputs `input/*.input.csv` and `input/rows.json` are derived from the batch-7
raws by `scripts/make_inputs_batch7.py` (fail-closed: source passes must be
2-pass node-exact on legal/result/nodes/lo/hi, key/legal cross-checked against
`batch10324/input/batch-keys.json`, replica verdict must be LOSS 2 on every
row - the Part L pre-registered expectation).

## Protocol

- solver: `scripts/third_impl.js` (byte-pinned), one process per row,
  `--cap=300000000 --wallcap=240 --memo-power=22`, 2 runs (a/b) per row;
  runner `scripts/run_thirdimpl.sh`; status log `output/status.log`
- rule-engine gate before any target run: `scripts/verify_tbl.js`
  (forbidden-quad count 95,670 == replica; TBL==wob on the deterministic
  triple sweep, 195,044 triples, mismatches 0), captured in
  `output/rules-gate.txt`
- `--legal` declared per row: the driver's derived legal count must equal it
  (fail-closed GATE_FAIL otherwise; ng1/ng2 exercise this)
- determinism gate: each row's (result, expansion, ttHits, reason) must be
  identical across a/b
- verdict agreement: a clean third-impl result must equal the published
  replica verdict (all rows -> LOSS 2). A wall/cap `runlimit` is an honest
  wall-inconclusive (NOT a verdict). A clean divergence is recorded as
  divergence evidence - it never flips a verdict here; the closure decision
  stays with the independent merge + refresh re-audit.
- audit: `scripts/audit.py` recomputes every gate from the raw outputs
  (fail-closed) and writes `output/audit-summary.json`; run twice,
  outputs byte-identical.

## Operational note (honest)

One environment restart (remote sandbox synch failure) interrupted the target
runs between h009.a and h009.b; the lane kit (resilient storage) kept all
completed runs and the batch resumed exactly at h009.b. All 51 a/b pairs are
complete; no run is missing.

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py` (fail-closed, run twice byte-identical): **541/541 gates
PASS**. Verdict agreements (third implementation vs published pinned-replica
verdicts): **51/51 LOSS 2, 0 divergences, 0 wall-inconclusive**, all a/b run
pairs identical on (result, expansion, ttHits, overwrites), third-impl
expansions 2,436,068-8,744,134.

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| h001 | LOSS 2 (5,416,882) | **LOSS 2** (6,270,073; ttHits 3,520,241) | a/b identical |
| h002 | LOSS 2 (2,321,870) | **LOSS 2** (2,645,373; ttHits 1,522,490) | a/b identical |
| h003 | LOSS 2 (4,483,207) | **LOSS 2** (5,218,322; ttHits 2,881,953) | a/b identical |
| h004 | LOSS 2 (3,542,126) | **LOSS 2** (4,089,523; ttHits 2,239,859) | a/b identical |
| h005 | LOSS 2 (3,883,214) | **LOSS 2** (4,474,459; ttHits 2,503,935) | a/b identical |
| h006 | LOSS 2 (2,658,806) | **LOSS 2** (3,028,243; ttHits 1,732,496) | a/b identical |
| h007 | LOSS 2 (4,926,684) | **LOSS 2** (5,689,589; ttHits 3,244,181) | a/b identical |
| h008 | LOSS 2 (4,285,733) | **LOSS 2** (4,962,203; ttHits 2,734,191) | a/b identical |
| h009 | LOSS 2 (7,430,631) | **LOSS 2** (8,744,134; ttHits 4,691,417) | a/b identical |
| h010 | LOSS 2 (3,768,833) | **LOSS 2** (4,356,817; ttHits 2,412,339) | a/b identical |
| h011 | LOSS 2 (4,144,900) | **LOSS 2** (4,787,863; ttHits 2,646,909) | a/b identical |
| h012 | LOSS 2 (5,941,344) | **LOSS 2** (6,863,824; ttHits 3,791,375) | a/b identical |
| h013 | LOSS 2 (2,962,991) | **LOSS 2** (3,382,736; ttHits 1,918,051) | a/b identical |
| h014 | LOSS 2 (2,810,013) | **LOSS 2** (3,216,194; ttHits 1,830,575) | a/b identical |
| h015 | LOSS 2 (3,151,719) | **LOSS 2** (3,608,106; ttHits 2,036,218) | a/b identical |
| h016 | LOSS 2 (3,560,829) | **LOSS 2** (4,064,816; ttHits 2,365,986) | a/b identical |
| h017 | LOSS 2 (3,640,695) | **LOSS 2** (4,187,400; ttHits 2,326,549) | a/b identical |
| h018 | LOSS 2 (2,951,139) | **LOSS 2** (3,363,804; ttHits 1,908,276) | a/b identical |
| h019 | LOSS 2 (2,169,285) | **LOSS 2** (2,465,860; ttHits 1,428,419) | a/b identical |
| h020 | LOSS 2 (3,369,443) | **LOSS 2** (3,828,056; ttHits 2,237,596) | a/b identical |
| h021 | LOSS 2 (3,749,044) | **LOSS 2** (4,322,473; ttHits 2,393,636) | a/b identical |
| h022 | LOSS 2 (2,599,772) | **LOSS 2** (2,940,153; ttHits 1,749,087) | a/b identical |
| h023 | LOSS 2 (5,228,790) | **LOSS 2** (6,136,914; ttHits 3,316,250) | a/b identical |
| h024 | LOSS 2 (3,505,384) | **LOSS 2** (4,004,724; ttHits 2,280,608) | a/b identical |
| h025 | LOSS 2 (4,286,982) | **LOSS 2** (5,064,834; ttHits 2,786,583) | a/b identical |
| h026 | LOSS 2 (3,371,276) | **LOSS 2** (3,850,639; ttHits 2,196,148) | a/b identical |
| h027 | LOSS 2 (4,053,495) | **LOSS 2** (4,691,727; ttHits 2,539,014) | a/b identical |
| h028 | LOSS 2 (3,135,250) | **LOSS 2** (3,602,661; ttHits 2,005,958) | a/b identical |
| h029 | LOSS 2 (3,898,718) | **LOSS 2** (4,505,150; ttHits 2,487,781) | a/b identical |
| h030 | LOSS 2 (2,133,491) | **LOSS 2** (2,436,068; ttHits 1,383,959) | a/b identical |
| h031 | LOSS 2 (7,025,561) | **LOSS 2** (7,996,669; ttHits 4,316,887) | a/b identical |
| h032 | LOSS 2 (2,928,628) | **LOSS 2** (3,346,830; ttHits 1,917,494) | a/b identical |
| h033 | LOSS 2 (4,574,888) | **LOSS 2** (5,328,382; ttHits 2,906,230) | a/b identical |
| h034 | LOSS 2 (3,275,966) | **LOSS 2** (3,723,274; ttHits 2,170,998) | a/b identical |
| h035 | LOSS 2 (6,870,991) | **LOSS 2** (8,101,279; ttHits 4,335,862) | a/b identical |
| h036 | LOSS 2 (6,606,579) | **LOSS 2** (7,621,517; ttHits 4,174,855) | a/b identical |
| h037 | LOSS 2 (3,246,295) | **LOSS 2** (3,722,693; ttHits 2,089,023) | a/b identical |
| h038 | LOSS 2 (4,439,289) | **LOSS 2** (5,145,960; ttHits 2,891,265) | a/b identical |
| h039 | LOSS 2 (2,891,243) | **LOSS 2** (3,286,479; ttHits 1,930,463) | a/b identical |
| h040 | LOSS 2 (5,111,982) | **LOSS 2** (5,892,739; ttHits 3,354,765) | a/b identical |
| h041 | LOSS 2 (6,908,062) | **LOSS 2** (7,989,930; ttHits 4,378,926) | a/b identical |
| h042 | LOSS 2 (3,293,703) | **LOSS 2** (3,779,551; ttHits 2,125,694) | a/b identical |
| h043 | LOSS 2 (3,236,939) | **LOSS 2** (3,708,422; ttHits 2,097,198) | a/b identical |
| h044 | LOSS 2 (6,866,951) | **LOSS 2** (8,136,795; ttHits 4,380,360) | a/b identical |
| h045 | LOSS 2 (2,652,272) | **LOSS 2** (2,999,221; ttHits 1,781,689) | a/b identical |
| h046 | LOSS 2 (3,237,819) | **LOSS 2** (3,709,203; ttHits 2,088,756) | a/b identical |
| h047 | LOSS 2 (2,318,951) | **LOSS 2** (2,648,045; ttHits 1,511,184) | a/b identical |
| h048 | LOSS 2 (2,639,850) | **LOSS 2** (3,007,505; ttHits 1,723,214) | a/b identical |
| h049 | LOSS 2 (3,873,970) | **LOSS 2** (4,451,223; ttHits 2,518,572) | a/b identical |
| h050 | LOSS 2 (3,490,354) | **LOSS 2** (3,984,000; ttHits 2,304,522) | a/b identical |
| h051 | LOSS 2 (4,644,922) | **LOSS 2** (5,420,316; ttHits 2,922,353) | a/b identical |

- Anchors on this host: k02 WIN 9,106,337 expansions / 4,991,527 ttHits and l1
  LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
  third-implementation values (and the Part G/K host reproductions).
- Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0 mismatches.
- Negative gates: ng1 / ng2 GATE_FAIL with the published messages.
- Batch-7's closure-evidence bundle is now cross-implementation verified
  end-to-end: 51 replica 2-pass LOSS rows + 51 third-implementation
  agreements, all fail-closed audited.

The standard 11x11 empty board, the 19 central-reply roots, class 10324 and
all remaining S5 keys remain UNKNOWN throughout; class 10324's closure remains
pending the published fail-closed merge + independent refresh re-audit.
Expansions and node counts are not verdicts.
