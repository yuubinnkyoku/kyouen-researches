# n11 sixth-cost second resumption k04 WIN checkpoint: session log (2026-11-22)

Lane: the n11 long-term lane. Session: continuation of the second resumption of the
sixth-cost exclusive S5 probe batch (declaration
`research/log/2026-11-22-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-resume-k04-k43-single-owner-note.md`,
commit `65f7a3f8`; scope: resume the halted ladder at k04..k43, no new keys claimed).

## Pre-ladder gates on this host (per the declaration)

- D1 selector re-execution (`scripts/select_sixth_exclusive.py`): ALL 229 fail-closed
  gates PASS under the sha-pinned inputs fetched at HEAD `d5371854`; the regenerated
  selection JSON is byte-identical to the published one (sha256
  `d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87`); all 43
  regenerated k01..k43 batch input CSVs are byte-identical to the published batch
  inputs (43/43 cmp).
- D2 validation gate (`input/val-gate/` 4 rows, pinned Node.js replica jsreplay.js
  sha256 `84585617...`): 4/4 node-exact PASS on this host; published as a NEW file
  `output/val-gate-summary-resume2-20261122.json` (this host's wall_s 9/9/17/24 s vs
  the published first-host summary 9/9/18/25; result/nodes/legal exact on all four
  rows; at2m x2 result 0 / nodes 2,000,000 / legal 98, 99; 15M rows result 2 /
  nodes 3,651,923 and 5,040,200 / legal 98, 99).

## Ladder result: THIRD fresh exclusive WIN, verdicts unconsumed

- k04 `10376293541461626888:65536` (stones 5, legal 83; machine order position 4;
  band-1 truncated-cost proxy 5,041,585): stage 2M UNKNOWN (result 0, nodes
  2,000,000), then 15M **WIN(1) nodes 9,433,024** on both independent cold runs
  (47 s / 48 s wall), plus the voluntary third cold verification run at 15M with
  identical (result, nodes) (48 s wall), per the k02/k03 precedent.
- Pre-registered WIN stopping rule (1) fired: no further claimed-key starts this
  session; k05..k43 NOT started. The WIN checkpoint raws
  (`at2m-k04.out.csv`, `at15m-run1-k04.out.csv`, `at15m-run2-k04.out.csv`,
  `at15m-run3-verify-k04.out.csv`) and the status.log append were published at
  commit `cb7ffe05`.
- All batch verdicts remain unconsumed: no cache increment, no class-status
  change, no coverage claim. The batch now has FOUR unconsumed rows (k01 LOSS
  10,369,650; k02 WIN 7,717,432; k03 WIN 9,255,414; k04 WIN 9,433,024), three of
  them fresh WIN children of the sixth-cost class.

## Third-implementation cross-verification (evidence only)

- Declared `d33d752b` (single-owner addendum note extending today's k01/k03
  third-implementation program to the fresh k04 WIN row) and published at
  `bcc39add` in `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-`
  `reverification-20261122/` (k04 addendum: input, 3 cold outputs, replica raws,
  audit_k04.py 31/31 fail-closed gates with fail-closed tamper controls,
  2-run byte-identical audit output, MANIFEST 30 entries re-hashed, README
  addendum section).
- Result: third_impl.js reproduces WIN(1) with identical result / expansions
  11,020,407 / ttHits 6,092,599 on two full cold runs plus one verify-legal run
  (31.05 / 30.82 / 54.92 s wall). Honest audit note (published in that README):
  the auditor's original determinism expression was malformed and fixed BEFORE
  execution; the raws were never edited.
- Standing: additional evidence only; adoption stays with the scrutiny owner.

## This push: k04 witness publication (rule (1), k02/k03 precedent)

- `scripts/analyze_win_finding_k04.py` (150 fail-closed gates) +
  `output/win-finding-ifadopted-k04.json` (run twice, byte-identical, sha256
  `06041fcda040e2c83c8a99a51ef3556ba8eb93e3013bcd4754004615de80571b`).
  Tamper controls all fail closed (rc=1): k04 run1 nodes 9,433,024 -> 9,433,025
  detected at `k04_15m_pair`; k04 2M result 0 -> 1 detected at `k04_2m_unknown`;
  a selector order row dropped detected at `order_43`.
- Scenarios (machine-checked, NOT adopted): (A) k04-only: exactly ONE class flips
  UNKNOWN->WIN, the sixth-cost class `10376293541461626880:65536` (coverage
  {80, 84, 100, 108}); k04's two other membership classes `1297036692683751552:0`
  (coverage {77, 87, 100, 108}) and `10376293541461622792:65536` (coverage
  {77, 80, 84, 87}) are already base-stage WIN. (B) all four unconsumed rows:
  three classes flip (adding `1297319267171041280:0` via k03 and
  `1297037792211107840:0` via k02). In BOTH: live candidate classes 62 -> 61,
  secured third-move coverage UNCHANGED at 117/119 (remaining {100, 108}), no class
  becomes LOSS. NOT a coverage event, NOT a route to the root certificate.
- `output/val-gate-summary-resume2-20261122.json` (the D2 rows, new file, no
  overwrite), README checkpoint section append, and this session log.

## Delegated C++ gate (unchanged, scrutiny owner)

- `cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...`.
- k04 `target,0,5,10376293541461626888,65536,83,0,0,0,0,0` @15,000,000:
  expected result 1, nodes 9,433,024.
- k01 `target,0,5,1297036692683751424,1114112,87,0,0,0,0,0`: expected result 2,
  nodes 10,369,650. k02 `target,0,5,1297036692683751424,68157440,87,0,0,0,0,0`:
  expected result 1, nodes 7,717,432. k03
  `target,0,5,10376293541461626880,65792,81,0,0,0,0,0`: expected result 1,
  nodes 9,255,414.
- No C++ toolchain in this sandbox (re-verified); any later C++ disagreement fails
  closed in favor of discarding the row.

## Concurrency (honest log)

- This session's pushes touched only this lane's claimed paths. Between the k04
  checkpoint publication `cb7ffe05` and the k04 addendum publication `bcc39add`,
  the sibling n11-s4bd lane pushed (`378a98f5` -> `9e49cd1e` -> `973c480e` ->
  `3b6c23b3`, pass2 checkpoints and merge-layout/session-log addenda; disjoint).
- HEAD observed immediately before this push: `bc11e28b` (six-row lane single-owner
  declaration; disjoint from all paths written here). Push-side conflict checks on
  the shared probe README passed (current blob re-fetched at staging time).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves 100/108 remain UNKNOWN throughout. The sixth-cost class is NOT closed
by this batch (58 shared children remain outside this lane's claim); any
class-level statement will only be made machine-checked against the full
108-child set. Nodes, budgets, expansions, proxy values and solved counts are
never verdicts.


## Post-push reexecution check (commit `1ccbe303`)

- All five files published by the witness commit `1ccbe303` re-downloaded at the
  fixed commit and byte-identical (sha256) to the local staged originals:
  scripts/analyze_win_finding_k04.py `fa7943a8...`,
  output/win-finding-ifadopted-k04.json `06041fcd...`,
  output/val-gate-summary-resume2-20261122.json `ebc40f53...`, the probe README
  (diff vs the pre-push base = title update + k04 checkpoint section insertion
  only), and this session log `167e5f6e...`.
- Re-execution on the pushed state: the published script, the published selector
  (re-downloaded, byte-identical, sha256 `d5e9b059...`), and all 15 published
  batch raw rows re-downloaded at `1ccbe303`; `analyze_win_finding_k04.py` run
  twice: 150/150 fail-closed gates PASS both times, output byte-identical to the
  published JSON on both runs (`06041fcd...`).
