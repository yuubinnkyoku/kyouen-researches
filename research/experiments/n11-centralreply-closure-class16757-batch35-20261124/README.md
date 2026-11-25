# n11 central-reply closure class 16757 batch-35: clean 28-key probe (2026-11-24, Part DV)

Declared in
`research/log/2026-11-24-part-dv-batch35-class16757-declaration.md`
(commit `63028eea`, observed HEAD `d8b849e5`; Part DU + DU-b direct successor).

Batch-35 of the central-reply 19-root closure grind (K0415/K0417 line):
the latest published closure table
(`../n11-centralreply-class34908-b33loss45-adoption-reaudit-20261124/reaudit/output/closure-classes.csv`,
sha256 `6cc33dd7...`) has classes ranked 1-6 fully occupied by honest-labeled
but unconsumed rows (WIN rows awaiting the scrutiny owner C++ gate, or
EXHAUSTED rows), so the highest-ranked class with clean (never-probed)
unknown children is **class 16757** (rank 7, mask
`[1153204079095185408, 65536]`, unknown_now 29). The 29 = b018 (batch-1
WIN, unconsumed) + the 28 clean keys `b021..b048` taken from the published
batch-1 packet `not_probed_unknown` set
(`../n11-centralreply-closure-class16757-batch-20261122/`).

## Protocol (publish-then-execute, single owner)

- kit: scripts (pinned replica `jsreplay.js` sha256 `84585617...` + runner
  `runbatch.sh` sha256 `f591f8c2...`, both byte-clones of the batch-33/34
  kits, plus the new fail-closed maker `make_batch35_keys.py`), sources 7
  (batch-1 packet 3 + refresh-summary `38fc4e19` + closure-classes
  `6cc33dd7` + canonical cache `973bcd19` + quarantine `81d23160`),
  val-gate 8 (published batch-34 kit byte-clones), input 29 (28 target CSV
  + `batch-keys-b35.json`, maker outputs).
- maker gates G1-G6 (source sha pins / batch-1 packet integrity + not_probed
  == {b021..b048} + status-log row parsing / closure rank-anchor + 29 == 1+28
  accounting / exact-pair absence in the canonical cache / quarantine absence /
  worklist_first probe_order 28..40 field match): declared-time local runs
  ALL GATES PASS 3x byte-identical; tamper battery 6/6 + control all ABORT on
  the pre-registered gate (T1 pin-G1, T2 not_probed-G2, T3 cache-hit-G4, T4
  quarantine-hit-G5, T5 rank-drift-G3, T6 worklist-drift-G6). The T5 battery
  round initially hit the known sed no-op trap (rank-6 line has no `,29,`);
  the substitution was asserted before re-running - pre-publication
  correction, no effect on published bytes.
- execution: from the published bytes (fetch-back byte-verified kit), the
  maker was re-run (byte-identical outputs), then the published val-gate 4
  rows were reproduced fresh-cold on this host - **4/4 node-exact**
  (`at2m` x2 budget 2M result 0 nodes 2,000,000; `first-15m`
  15000000,2,3651923; `second-15m` 15000000,2,5040200; full replay line
  equal except wall_s).
- drives: 28 keys, one solver per row, 2 fresh cold passes at budget
  15,000,000, sequential, `output/status.log` append-only,
  `output/raw/$k.p1.out`+`.p2.out` per key with the `# replay_done`
  terminal-line guard. **WIN-CONTINUE pre-registered** (the class already
  had the unconsumed WIN b018, so an all-LOSS closure is impossible at this
  budget; the aim is complete honest labeling). No 15M same-condition
  re-search; result 0 (exhaustion) would be honest UNKNOWN.

## Status (complete: ALL 28 keys probed to completion, 2026-11-24T21:38-21:51Z)

- **26 rows result 2 (LOSS), 2-pass node-exact**, per-key nodes in
  `output/status.log` and `output/batch-audit.json` (loss_keys)
- **2 rows result 1 (WIN), 2-pass node-exact honest labels - not consumed**:
  - **b032** key [1153204147814662144, 65536] (legal 72, s5 556117), nodes
    2,678,305 both passes
  - **b048** key [1152922672837951488, 65792] (legal 72, s5 558553), nodes
    3,485,963 both passes
- EXHAUSTED 0, MISMATCH 0, TRUNCATED 0. Independent full-line (ex-wall)
  two-pass agreement sweep: 28/28. Total nodes (both passes): 147,515,318.
- verdicts are **not consumed** by this Part: the 26 LOSS rows are adoption
  candidates only (a future adoption Part through the pinned fail-closed
  merger); the 2 WIN rows additionally require third-implementation
  cross-verification and the scrutiny owner C++ second-implementation gate
  (`cpp/solvers/kyouen_dfpn_root.cpp`, pin `9193f5b6...`), which this
  execution environment still cannot compile (no C++ toolchain; package
  installation prohibited - unchanged since 2026-11-22 Part G).

## No claims

**No coverage, no closure, no class-freeness, no root, and no board claim.**
Class 16757, the 19 central-reply roots, the two-stone roots {49,60}/{59,60},
S2 {59,60}, and the standard 11x11 empty board remain **UNKNOWN** at every
point of this Part. The closure table and worklist are scheduling
bookkeeping. Nodes counts are bookkeeping, not verdicts or distances.

## MANIFEST

`MANIFEST-sha256.txt` pins every published file in this directory (109
entries; README and MANIFEST self-excluded). Every wave was verified by
fetch-back raw comparison against the pinned commit bytes before the next
wave started (kit 47/47, outputs 61/61 byte-identical).
