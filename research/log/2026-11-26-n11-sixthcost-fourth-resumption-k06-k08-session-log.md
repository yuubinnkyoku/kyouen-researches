# n11 sixth-cost fourth resumption session log: k06 LOSS, k07 LOSS-at-2M, halt on the k08 WIN (2026-11-26)

Session record for the fourth resumption of the
`10376293541461626880:65536` exclusive s5 probe ladder (sixth-cost lane,
batch k06..k43). Pre-registered single-owner declaration at `e4cabc98`
(`research/log/2026-11-26-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-resume-k06-k43-single-owner-note.md`
+ `output/val-gate-summary-resume4-20261126.json`), executed in this
session's container (Node v22.20.0, Python 3.12.14, 2 cores, serial
foreground runs, no C++ toolchain - re-verified).

## What this session completed

1. Fetch-back verification of the resume4 declaration `e4cabc98` (both
   files byte-identical to the published raw at HEAD).
2. k06 `10376293541462675456:65536` (legal 89): 2M stage UNKNOWN
   (result 0, nodes 2,000,000, wall 9 s); 15M cold pair BOTH result 2
   (LOSS), identical expansions 8,182,231 (walls 44/43 s). Resolved LOSS
   under the registered rule (nonzero-and-identical pair). First
   LOSS-resolved row of the k06..k43 batch; second LOSS row of the whole
   ladder after k01. Checkpoint `585d99ef` (3 raws + status.log),
   fetch-back byte-verified.
3. k07 `10376293542535368704:65536` (legal 87): the first lane key
   resolved at the 2M STAGE - result 2, expansions 1,419,823 (wall 7 s).
   Registered rule for a nonzero 2M result requires a second independent
   2M cold run: identical (result 2, nodes 1,419,823, wall 7 s). A
   voluntary 15M cold pair was additionally run (both identical, walls
   6/6 s): FOUR identical runs total for k07. No third verify run (LOSS
   row, k01 precedent: verify runs are voluntary for WIN rows only).
   Checkpoint `3780887d` (4 raws + status.log), fetch-back byte-verified.
4. k08 `10376293610182148096:68719476736` (legal 89; first batch key with a
   non-65536 key_hi): 2M stage UNKNOWN (result 0, nodes 2,000,000, wall
   8 s); 15M cold pair result 1 (WIN), identical expansions 6,195,897
   (walls 30/30 s); voluntary third cold verify run identical (wall 28 s).
   Checkpoint `575a58fe` (4 raws + status.log), fetch-back byte-verified.
   Per the pre-registered stopping rule ("any WIN at any stage stops
   further claimed-key starts in THIS session"), the ladder HALTS at k08;
   k09..k43 are untouched and stay claimable by the next resumption.
5. Witness publication for the fresh WIN (published-after-execution),
   commit `0f4cbb85`:
   `scripts/analyze_win_finding_k08.py` - 285 fail-closed gates ALL PASS,
   two runs byte-identical, negative control T1 (verdict flip 1->2 in the
   k08 15M raw) fails closed at GATE `k08_15m_pair` (rc=1) with a
   byte-verified raw restore, then a clean T2 control run (rc=0); the
   analysis re-reads this lane's k01..k08 raw rows and re-verifies the
   ladder/determinism gates for all eight, plus the pinned bases
   (geometry `146be80b...`,
   probe-13 base `60e0dc34...`,
   chain increment base `bb4495e0...`,
   class-closure-priority `139eb0a0...`,
   selector JSON `d5e9b059...`) - and
   `output/win-finding-ifadopted-k08.json`.

## If-adopted summary (machine-checked, NOT adopted)

- Scenario A (k08 WIN only): TWO flips, both UNKNOWN->WIN: the
  sixth-cost class `10376293541461626880:65536` itself (coverage
  {80, 84, 100, 108}) and k08's NON-candidate membership class
  `1297037792194334720:0` (coverage {12, 20, 80, 84}; 106 children / 104
  unknown). k08's candidate membership class
  `1152921504742113280:68719476736` (coverage {12, 20, 100, 108}) is
  already base-stage WIN: no flip. Second probe-ladder WIN after k05
  whose non-candidate membership class flips in the k-only scenario.
- Scenario B (all EIGHT unconsumed rows k01..k08): FIVE flips, all
  UNKNOWN->WIN (the four earlier flip classes `FLIP_CLASS_A2` via k03,
  `FLIP_CLASS_B2` via k02, `FLIP_CLASS_C` via k05, plus k08's
  `FLIP_CLASS_D`, plus the sixth class); the fresh LOSS rows k06/k07 flip
  NO class (single LOSS children complete nothing; their UNKNOWN member
  classes keep 98/99 unknown children); the sixth-cost class would hold
  FIVE fresh WIN children (k02, k03, k04, k05, k08), unknown-children
  101 -> 93.
- BOTH scenarios: live candidate classes 62 -> 61; secured third-move
  coverage UNCHANGED 117/119, remaining {100, 108}; class census A
  {UNKNOWN 3079, WIN 274, LOSS 31}, B {UNKNOWN 3076, WIN 277, LOSS 31}.
  Neither is a coverage event or a route to the root certificate.

## Concurrency and honesty notes

- Concurrent z-strip-lane commits `25b294ad` and `d49b480a` (z=27..z=34
  frontier micro-kit) landed between this lane's checkpoints; all
  pushes here were clean fast-forwards on the then-current main (recorded
  in `status.log` per the declaration's concurrency rule); territories
  are disjoint from this lane's probe rows.
- One fetch-back verification invocation in this session initially
  omitted the experiment path prefix in the raw URL (the downloaded body
  was a 404 page, correctly reported as a byte MISMATCH by `cmp`); the
  retry with the correct URL was byte-identical. No published byte was
  ever in question; the local artifacts are the published bytes.
- The k07 2M determinism pair and the k07 voluntary 15M pair are labeled
  as such in `status.log` (`done 07 2m-run2`, `done 07 15m-run1`,
  `done 07 15m-run2`); the registered minimum was one 2M pair.
- Environment wall-times on this host: k06 15M runs 44/43 s, k07 6-7 s
  runs, k08 15M runs 30/30/28 s; all single-process foreground, one
  jsreplay per run.

## State left for the next run

- Batch ledger: k01 LOSS, k02/k03/k04/k05/k08 WIN, k06/k07 LOSS; all
  verdicts UNCONSUMED; no cache file modified; the k01..k08 C++
  delegated pinned-gate expectations are as published in
  `output/win-finding-ifadopted-k08.json`.
- k09..k43 (35 keys) remain; natural next step for a fourth-resumption
  continuation is k09 (`10377419441368469504:65536`, legal 87) under the
  same pre-registered rules, and the third-implementation program may
  extend to k06/k07/k08 with a fresh declaration.
- The standard 11x11 empty board, the two-stone root {60,27}, and its
  remaining third moves 100/108 remain UNKNOWN throughout. Nodes, budgets,
  expansions and solved counts are never verdicts.
