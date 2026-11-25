# n11 central-reply closure class 16371 batch-37: clean 47-key probe (2026-11-25, Part DY)

Declared in
`research/log/2026-11-25-part-dy-batch37-class16371-declaration.md`
(commit `d5229dca`, observed HEAD `46e02d0e`; Part DV/DW lane successor,
orthogonal to the sibling Part DX batch-36 lane).

Batch-37 of the central-reply 19-root closure grind (K0415/K0417 line).
The latest published closure table (`b7241eb0...`, 807 rows, Part DW reaudit)
has ranks 1-8 fully occupied by honest-labeled unconsumed rows and rank 9
class 20421's clean 45 keys owned by the in-flight Part DX, so the
highest-ranked class with clean (never-probed) unknown children available
to a new batch is **class 16371** (rank 10, mask
`[1153202979851993088, 16]`, unknown_now 49).

## Class accounting (machine-verified, no closure claim)

- 49 unknown_now = 2 probed honest-label unconsumed (batch-4, 2026-11-22:
  e001 LOSS `15000000,2,882800`, e002 WIN `15000000,1,14112632`, WIN-HALT
  stopped the batch) + **47 clean targets** (= published batch-4 packet
  keys e003..e050 minus e022).
- e022 (s5 546606) is the dual-class packet key probed as batch-14
  **q007** (class 23101 packet, PASS LOSS `15000000,2,1494975`) and already
  consumed into the canonical chain cache
  (`s5verdict,1153202979868770304,16,5,2,1494975`), hence excluded from
  the unknown set (maker gate G4b pins this row; G6 pins its absence from
  the worklist extract).
- e042 is the dual-class packet key declared (never probed) as batch-13
  **p028** (class 16930 packet); it was a clean target and probed here.

## Protocol (publish-then-execute, single owner)

- kit: scripts (pinned replica `jsreplay.js` sha256 `84585617...` and
  runner `runbatch.sh` sha256 `f591f8c2...`, byte-clones of the
  batch-33/34/35/36 kits, plus the new fail-closed maker
  `make_batch37_keys.py` sha256 `2c2c8c3a...`), sources 7 (batch-4 packet
  2: `70b8a4c8...` / `63c2d969...`; refresh-summary `5fe3e5ab...`;
  closure-classes `b7241eb0...`; canonical cache `23d40e36...`;
  quarantine `81d23160...`; worklist-class16371-extract `da813027...`,
  probe_order 126..174, 49 rows), input 48 (47 target CSV +
  `batch-keys-b37.json`), val-gate 12 (4 molecules x input /
  published-baseline byte-clones from the batch-36 kit + 4 fresh
  dy-host outputs).
- maker gates G1-G6 plus the batch-37-specific **G4b** (adopted e022 =
  q007 cache-row pin). Maker run 3x byte-identical; tamper battery
  10/10 fail-closed (T1 pin drift / T2+T2b packet field drift (pin and
  re-pin layers) / T3+T3b status drift / T4 target-pair cache hit /
  T5 quarantine hit / T6 closure rank drift / T7 worklist extract drift /
  T8 adopted-row nodes drift) + control PASS, all before declaration.
- environment reproduces the Part DW reaudit byte-exactly: the refresh
  regen run in this session reproduced all four outputs
  (`86767be9...` worklist / `b7241eb0...` closure / `5fe3e5ab...`
  summary / `f1abcd85...` per-root) sha256-identically.
- val-gate: 4 fresh dy-host runs, node-exact on (budget,result,nodes)
  against the published baselines (2,000,000,0,2000000 x2;
  15,000,000,2,3651923; 15,000,000,2,5040200).
- drive: 2-pass fresh-cold exact replay, budget 15,000,000,
  1 solver / row / process, sequential, single host (2-core);
  drive order = worklist probe_order = packet order e003..e050 minus
  e022; increments published every 8 keys (inc1 `4b2e5a44`,
  inc2 `bdce74c4`, inc3 `72c0a7b4`, inc4 `31101a5d`, inc5 `52432c4d`,
  inc6 `630f4980`; per-blob shas in MANIFEST-sha256.txt).

## Results (honest labels; verdicts NOT consumed anywhere by this batch)

- **47/47 keys probe-complete**: **46 LOSS + 1 WIN (e042) + 0 EXHAUSTED
  + 0 determinism mismatch**. Total nodes 99,204,059 per pass.
- e042 WIN: 2-pass node-exact `15000000,1,2909040`, pre-registered
  WIN-HALT marker, drive-level WIN-CONTINUE vacuous (e042 was the final
  key of the drive order). The WIN verdict is **unconsumed**: adoption
  only through the scrutiny-owner C++ second-implementation gate
  (`9193f5b6...`), which this environment cannot run (no C++ compiler).
- batch-4's older unconsumed labels remain as found: e001 LOSS
  (adoptable in a future adoption Part from the published batch-4 raw
  per the pinned merger discipline) and e002 WIN (scrutiny gate only).
- status.log sha256 `8ce0b9fb...` (47 PASS rows + 1 WIN-HALT row);
  batch-audit.json (machine audit, sha256 `ac76cb74...`) holds the
  per-key (probe_order, budget, result, nodes, ts) table and pins.

**No closure, coverage, secured-coverage, or root-outcome claim is made
anywhere in this batch. The standard 11x11 empty board, all 19
central-reply roots, the two-stone roots {49,60}/{59,60}, S2 {59,60},
classes 1/2/4, and class 16371 itself remain UNKNOWN at every point.
Nodes counts are bookkeeping, not outcomes or distances.**
