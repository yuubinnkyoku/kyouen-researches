# n11 reply27 two-target S5 probe #1 (JS replica): 1306114260682670080:0 = LOSS

Increment of the reply27 two-target S5 lane declared in
`research/log/2026-11-21-n11-reply27-s5-probe-js-replica-single-owner.md`
(single-owner declaration, HEAD `00868775` at 11:58Z, commit `4e944105`).

## Result

- Target S5 key `1306114260682670080:0` (legal 88, 2 live parent classes,
  lowest truncated-cost proxy 5,041,585 among the 4,575-task supply).
- Cold run, fresh TT (2^22) per row, one worker, publish=ALL, exact-order=count:
  - at 2,000,000 nodes: UNKNOWN (budget exhausted, 2,000,000 nodes).
  - at 15,000,000 nodes: **LOSS** at exactly 10,070,489 nodes (done twice on
    this host, identical node count).
- Semantics per the pinned source (`exact_replay`: 0 UNKNOWN, 1 WIN, 2 LOSS,
  fixed first player). This is a **solver-trusted exact** verdict produced by
  the JS replica of the pinned C++ path, NOT an independent terminal minimax.

## Validation gate (declaration acceptance condition 1) — PASSED

The replica reproduces **all four** published raw replay rows of
`research/experiments/n11-two-target-design-20261010/output/raw` with
identical `stones/legal/is_or/budget/result/nodes` (only `wall_s` differs):

| target | budget | published | replica |
|---|---|---|---|
| 1152921504606851072:536870946 | 2,000,000 | 0 / 2,000,000 | 0 / 2,000,000 |
| 1188950301626860544:536870912 | 2,000,000 | 0 / 2,000,000 | 0 / 2,000,000 |
| 1152921504606851072:536870946 | 15,000,000 | 2 / 3,651,923 | 2 / 3,651,923 |
| 1188950301626860544:536870912 | 15,000,000 | 2 / 5,040,200 | 2 / 5,040,200 |

The replica (`scripts/jsreplay.js`) is a line-faithful Node.js port of the
exact-replay path of `cpp/solvers/kyouen_dfpn_root.cpp` at commit `154f3b7a67`
(file SHA-256 `9193f5b6...`, the source that generated the published raws).
A 64-bit xor-shift composition bug (`x>>30` low word built as
`(lo>>>30)|((hi&3)<<30)` instead of `(lo>>>30)|(hi<<2)`) was the only defect
found; after the fix, 20,000 random mix64 values match a BigInt reference
exactly and all four published rows reproduce node-exactly.

## Ledger effect (frozen 3,384-class geometry)

- `1297107061427929088:0` (coverage 26,28,100,108): unknown 101 -> 100,
  loss 7 -> 8. Still UNKNOWN.
- `1306043891938492416:0` (coverage 100,103,105,108): unknown 102 -> 101,
  loss 6 -> 7. Still UNKNOWN.
- `1306114260681621504:0` (coverage 26,28,103,105): already WIN; loss 0 -> 1,
  unknown 99 -> 98 (bookkeeping only).
- No class changes status. Candidate status counts stay **62 UNKNOWN / 53 WIN**.
- Secured coverage unchanged; remaining third moves of the ordered root
  {60,27} stay {100, 108}. The post-probe active supply shrinks
  4,575 -> 4,574 keys (two-live-parent keys 1,887 -> 1,886).

## Cache increment

- Base (byte-pinned, not duplicated here):
  `research/experiments/n11-two-target-design-20261010/output/merged-exact-s5.cache`
  (5,743 rows, SHA-256 `24e97b74...`).
- New: `output/merged-exact-s5-after-js-probe-1.cache` (5,744 rows,
  SHA-256 `6ab46ac6c11ada0c2f45fceeda8304852052e09c27db4ed1989c4041d74afcd2`),
  = base bytes + exactly one inserted row
  `s5verdict,1306114260682670080,0,5,2,10070489` at its sorted position
  (roundtrip-verified: removing that one line yields the base file byte-exactly;
  deterministic reconstruction recipe: insert that line between rows
  `1306079076443750400,0` and `1306114260815839232,0` of the byte-pinned base).
- Publication note: the increment is published in a single commit; fetch-back
  byte verification against `output/manifest-sha256.json` is performed on the
  pushed files. `output/post-probe/shared-s5-tasks.csv` (554,248 bytes) is
  published in full and regenerable with
  `python3 research/experiments/n11-two-target-s5-task-geometry-audit-20261121/scripts/analyze.py --cache <this>/output/merged-exact-s5-after-js-probe-1.cache --out <this>/output/post-probe`
  (csv module output CR-stripped to LF). `strategy-analysis.json` and
  `candidate-classes.csv` are published in full.

## Verification

- `scripts/audit_probe.py`: 30 fail-closed gates, all PASS
  (raw row consistency, input pinning, independent integer geometry of
  `n11-independent-exact-audit-20261010/scripts/independent.py`
  [byte-identical, SHA-256 `954d3a10...`]: 5 stones, D4 canonical, safe,
  legal 88 re-derived; frozen-geometry parent membership; quarantine and
  base-cache absence; one-row increment; no duplicate keys; class status
  invariance; remaining third moves {100,108} unchanged).
- `output/probe-audit.json` holds the full audit record;
  `output/manifest-sha256.json` pins every published file.
- `output/post-probe/` regenerates the frozen-geometry analysis
  (analyze.py from `n11-two-target-s5-task-geometry-audit-20261121/scripts/`)
  over the new cache.

## Reproduction

```sh
node scripts/jsreplay.js --exact-replay=input/at2m-s5-1306114260682670080-0.input.csv  --exact-replay-budget=2000000
node scripts/jsreplay.js --exact-replay=input/at15m-s5-1306114260682670080-0.input.csv --exact-replay-budget=15000000
python3 scripts/audit_probe.py   # 30 gates, fails closed
```

## Status guard

Nodes, solved counts, and proxy values are never verdicts. This increment
establishes exactly one S5 LOSS (replica solver-trusted exact with node-exact
validation against the published C++ raws). No S4 class closure, no third-move
coverage claim. **The standard 11x11 empty board, the two-stone root {60,27},
and its remaining third moves 100/108 remain UNKNOWN.** The repo's pinned
C++ binary remains the reference implementation; any later C++ reproduction
disagreeing with this row fails closed (the increment is discarded).
