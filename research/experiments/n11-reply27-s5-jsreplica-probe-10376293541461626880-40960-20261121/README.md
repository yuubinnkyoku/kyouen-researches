# n11 reply27 two-target S5 probe #13 (JS replica): 10376293541461626880:40960 = LOSS

Thirteenth increment of the reply27 two-target S5 lane declared in
`research/log/2026-11-21-n11-reply27-s5-probe-js-replica-single-owner.md`
(single-owner declaration, HEAD `00868775` at 11:58Z, commit `4e944105`).
Follows the published recipe of probes #1-#12
(probe #11 = commit `0c3045a2`, probe #12 = commit `81e6d802`;
earlier commits as cited in those READMEs).

## Result

- Target S5 key `10376293541461626880:40960` (legal 110; 3 geometry parents,
  all live under the probe-12 cache, 2 of them reply27 candidate classes;
  lowest truncated-cost proxy 5,069,670 of the 4,563-task post-probe-12
  supply, a two-live-parent key per the post-probe-12 shared task list).
- Cold run, fresh TT (2^22) per row, one worker, publish=ALL, exact-order=count:
  - at 2,000,000 nodes: UNKNOWN (budget exhausted, 2,000,000 nodes).
  - at 15,000,000 nodes: **LOSS** at exactly 6,237,108 nodes (done twice on
    this host, identical node count; second raw row published).
- Semantics per the pinned source (`exact_replay`: 0 UNKNOWN, 1 WIN, 2 LOSS,
  fixed first player). This is a **solver-trusted exact** verdict produced by
  the JS replica of the pinned C++ path, NOT an independent terminal minimax.

## Validation gate — PASSED

The replica reproduces **all four** published raw replay rows of
`research/experiments/n11-two-target-design-20261010/output/raw` with
identical `stones/legal/is_or/budget/result/nodes` (only `wall_s` differs),
re-run fresh in this session:

| target | budget | published | replica |
|---|---|---|---|
| 1152921504606851072:536870946 | 2,000,000 | 0 / 2,000,000 | 0 / 2,000,000 |
| 1188950301626860544:536870912 | 2,000,000 | 0 / 2,000,000 | 0 / 2,000,000 |
| 1152921504606851072:536870946 | 15,000,000 | 2 / 3,651,923 | 2 / 3,651,923 |
| 1188950301626860544:536870912 | 15,000,000 | 2 / 5,040,200 | 2 / 5,040,200 |

The replica (`scripts/jsreplay.js`, byte-identical to the probe-1-#12
publications, SHA-256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`)
remains the line-faithful Node.js port of the exact-replay path of
`cpp/solvers/kyouen_dfpn_root.cpp` at commit `154f3b7a67`
(file SHA-256 `9193f5b6...`, the source that generated the published raws).

## Ledger effect (frozen 3,384-class geometry)

- `10376293541461626880:8192` (coverage 100,108,113,117; candidate class):
  unknown 105 -> 104, loss 9 -> 10. Still UNKNOWN.
- `10376293541461626880:32768` (coverage 91,95,100,108; candidate class):
  unknown 105 -> 104, loss 6 -> 7. Still UNKNOWN.
- `1297047687798980608:0` (coverage 91,95,113,117; non-candidate class,
  bookkeeping only): unknown 112 -> 111, loss 2 -> 3. Still UNKNOWN.
- No class changes status. Candidate status counts stay **62 UNKNOWN / 53 WIN**.
- Secured coverage unchanged (117); remaining third moves of the ordered root
  {60,27} stay {100, 108}. The active supply shrinks 4,563 -> 4,562 keys
  (two-live-parent keys 1,875 -> 1,874).

## Cache increment

- Base (byte-pinned, not duplicated here):
  `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-34359742464-20261121/output/merged-exact-s5-after-js-probe-12.cache`
  (5,755 rows, SHA-256 `0e4016ae...`).
- New: `output/merged-exact-s5-after-js-probe-13.cache` (5,756 rows,
  SHA-256 `60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6`),
  = base bytes + exactly one inserted row
  `s5verdict,10376293541461626880,40960,5,2,6237108` at its sorted
  position (roundtrip-verified: removing that one line yields the base file
  byte-exactly; deterministic reconstruction recipe: insert that line between
  rows `10376293541461626880,32832` and `10376293541461626880,65538`
  of the byte-pinned base).
- Publication note: the increment is published in a single commit; fetch-back
  byte verification against `output/manifest-sha256.json` is performed on the
  pushed files. `output/post-probe/shared-s5-tasks.csv` is published in full
  and regenerable with
  `python3 research/experiments/n11-two-target-design-20261010/scripts/analyze.py --cache <this>/output/merged-exact-s5-after-js-probe-13.cache --out <this>/output/post-probe`
  (csv module output CR-stripped to LF). `strategy-analysis.json` and
  `candidate-classes.csv` are published in full.

## Verification

- `scripts/audit_probe.py`: 32 fail-closed gates, all PASS (raw row
  consistency incl. the twice-run 15M determinism gate, input pinning,
  independent integer geometry of `n11-independent-exact-audit-20261010/scripts/independent.py`
  [byte-identical, SHA-256 `954d3a10...`]: 5 stones, D4 canonical, safe,
  legal 110 re-derived; frozen-geometry parent membership; quarantine and
  base-cache absence; one-row increment; no duplicate keys; class status
  invariance; remaining third moves {100,108} unchanged).
- `output/probe-audit.json` holds the full audit record;
  `output/manifest-sha256.json` pins every published file.
- `output/post-probe/` regenerates the frozen-geometry analysis
  (analyze.py from `n11-two-target-design-20261010/scripts/`)
  over the new cache.

## Reproduction

```sh
node scripts/jsreplay.js --exact-replay=input/at2m-s5-10376293541461626880-40960.input.csv  --exact-replay-budget=2000000
node scripts/jsreplay.js --exact-replay=input/at15m-s5-10376293541461626880-40960.input.csv --exact-replay-budget=15000000
python3 scripts/audit_probe.py   # 32 gates, fails closed
```

## Status guard

Nodes, solved counts, and proxy values are never verdicts. This increment
establishes exactly one more S5 LOSS (replica solver-trusted exact with
node-exact validation against the published C++ raws). No S4 class closure,
no third-move coverage claim. **The standard 11x11 empty board, the two-stone
root {60,27}, and its remaining third moves 100/108 remain UNKNOWN.** The
repo's pinned C++ binary remains the reference implementation; any later C++
reproduction disagreeing with this row fails closed (the increment is
discarded).
