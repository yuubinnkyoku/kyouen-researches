# Part DY: class 16371 batch-37 probe complete (2026-11-25)

Complement to the declaration at commit `d5229dca`
(`research/log/2026-11-25-part-dy-batch37-class16371-declaration.md`).
Full protocol, kit pins and per-file hashes:
`research/experiments/n11-centralreply-closure-class16371-batch37-20261125/README.md`
and `MANIFEST-sha256.txt` in the same directory.

## Outcome

- 47/47 clean keys of class 16371 (rank 10 closure, mask
  `[1153202979851993088, 16]`) probe-complete: **46 LOSS + 1 WIN
  (e042 = dual-class packet key of batch-13 p028), 0 EXHAUSTED,
  0 determinism mismatch**. Total nodes 99,204,059/pass (2-pass fresh
  exact replay, budget 15,000,000).
- e042 WIN `15000000,1,2909040` is node-exact across passes and carries
  the pre-registered WIN-HALT marker; verdict is **unconsumed** by this
  batch (scrutiny-owner C++ gate `9193f5b6...` only; not runnable in this
  environment, no C++ compiler).
- batch-4's earlier unconsumed labels are untouched: e001 LOSS
  `15000000,2,882800` (adoptable by a future pinned-merger `90711961`
  adoption Part from the published batch-4 raw), e002 WIN
  `15000000,1,14112632` (scrutiny gate only).

## Publish chain (all push-then-fetch-back byte-verified)

`d5229dca` declaration (observed HEAD `46e02d0e`) -> `1851e79c` kit
scripts -> `b792ea4a` sources (7, incl. batch-4 packet, closure-classes
`b7241eb0...` refresh table, worklist extract) -> `2db78cba` input (48)
-> `cfdda701` val-gate (12; 4 fresh dy-host runs node-exact vs
published baselines) -> increments `4b2e5a44` / `bdce74c4` /
`72c0a7b4` / `31101a5d` / `52432c4d` / `630f4980` (47 raw outputs, 94
files incl. 2nd pass) -> `8b7e7bc8` output status.log + batch-audit.json
(`8ce0b9fb...` / `ac76cb74...`) -> this README + MANIFEST push.

Environment reproduced the Part DW reaudit regen byte-exactly (4/4
output shas incl. closure table `b7241eb0...`) before making keys; maker
`make_batch37_keys.py` (`2c2c8c3a...`) gates G1-G6+G4b (e022=q007
adopted-row pin), 3x byte-identical output, tamper battery 10/10
fail-closed.

## Honest-label accounting for class 16371 after this batch

49 unknown_now = 2 batch-4 unconsumed (e001/e002) + 47 clean probed
here, all raw and audit rows published. Class 16371 itself remains
UNKNOWN: honest labels are not merged verdicts; the 46 LOSS rows become
adoptable raw for the next adoption Part (pinned merger `90711961`),
e042 and e002 WINs stay behind the scrutiny C++ gate, which this lane
cannot run.

11x11 empty board: FORWARD/UNKNOWN - no outcome claim, no coverage
claim, nothing consumed.

## Resume notes (next runs)

1. After Part DX (batch-36 / class 20421) completes its own completion
   publishing, the next adoption Part can pick up: batch-4 e001 LOSS,
   batch-37's 46 LOSS rows (and batch-36's LOSS rows if adopted set
   merges), via the pinned merger with conflict checks against the
   canonical cache.
2. Next clean-class selection should re-run the closure-table rank scan
   against the post-adoption refresh (ranks 1-10 will shift once the
   46 LOSS honest labels are adopted; expect class 16371 to move up).
3. C++ gate for e002/e042 WINs requires a compiler-capable host; until
   then both stay unconsumed and the class cannot close.
