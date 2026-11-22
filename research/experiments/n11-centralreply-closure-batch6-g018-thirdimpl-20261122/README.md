# n11 central-reply closure batch 6: third-implementation cross-verification of the g018 WIN (+ 3 stratified LOSS spots) (2026-11-22)

Follow-up of the batch-6 WIN-HALT (Part I, declared as an amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`;
this re-verification is recorded there as Part K). Re-applies the Part G
precedent
(`research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122/`)
to the batch-6 unconsumed packet.

## What this is

Batch 6 (class 5473, re-audit closure rank 6, first clean candidate) halted at
the pre-registered WIN-HALT on **g018** (s5_index 184684, key
`[1734519175235239936, 0]`, legal 78, 2-pass node-exact result 1,
5,936,863 nodes, pinned `jsreplay.js` replica @15M). The verdict is NOT
consumed (scrutiny owner pending, as b018/d002/e002/f017). The pre-registered
adoption gate remains the C++ second implementation
(`cpp/solvers/kyouen_dfpn_root.cpp`, pin `9193f5b6...`), which cannot run in
this lane's environment (no compiler). As strengthening evidence only, the
**third implementation** (non-df-pn AND/OR minimax `third_impl.js`, pinned
bytes sha256 `08ea958f...`, identical to the Part G publication) re-derives
the g018 verdict and three stratified batch-6 LOSS rows verdict-level.

**It consumes and changes no corpus verdict. The standard 11x11 empty board,
the 19 central-reply roots, and every closure class remain UNKNOWN.
Nodes/expansions are not verdicts.**

## Targets (machine-pinned inputs, no hand transcription)

- 1 WIN row: g018 `[1734519175235239936, 0]` (published replica: WIN 5,936,863)
- 3 LOSS spot rows: g001 `[1158058423066034176, 0]` (3,618,287),
  g011 `[1158058422931849216, 0]` (8,417,028),
  g016 `[1158058422965370880, 0]` (1,513,384)
- 2 anchors (published Part G third-implementation values): k02a WIN
  9,106,337 expansions / 4,991,527 ttHits; l1a LOSS 7,660,602 /
  3,951,175 (both reproduced node-exact in this experiment)
- 2 negative input gates (must GATE_FAIL): ng1 (k02a legal 88), ng2 (k02a
  stones 6)

Inputs: `input/rows.json` carries the exact 121-bit keys, declared legal counts
and replica references; `input/*.input.csv` are the CSV-string form consumed by
the runner (no JS Number round-trip - see the Part G operator erratum).

## Protocol

Identical to Part G: pinned scripts (third_impl `08ea958f...`,
verify_tbl `c8c52528...`, jsreplay `84585617...`), one process per row,
`--cap=300000000 --wallcap=240 --memo-power=22`, 2 runs (a/b) per row,
rule-engine gate (quads 95,670 == replica; 195,044 triples TBL==wob,
mismatches 0), fail-closed legal/stones gates, runner `scripts/run_thirdimpl.sh`,
audit `scripts/audit.py` recomputing every gate from raw outputs (run twice,
byte-identical).

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py`: **71/71 gates PASS**, run twice byte-identical.

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | a/b |
|---|---|---|---|
| g018 | WIN 1 (5,936,863) | **WIN 1** (6,776,591) | identical |
| g001 | LOSS 2 (3,618,287) | **LOSS 2** (4,143,095) | identical |
| g011 | LOSS 2 (8,417,028) | **LOSS 2** (9,926,469) | identical |
| g016 | LOSS 2 (1,513,384) | **LOSS 2** (1,690,556) | identical |

- Anchors: k02a WIN 9,106,337 expansions / 4,991,527 ttHits (27s both runs)
  and l1a LOSS 7,660,602 / 3,951,175 (23s both runs) - **exactly** the
  published third-implementation values.
- Negative gates: ng1 / ng2 GATE_FAIL with the published messages.
- All runs `clean`, quads=95,670 in every output line, 0 wall-inconclusive.

Interpretation: verdict-level corroboration of the batch-6 halt row (and 3
LOSS spots) by a second, independent implementation. NOT adoption; the
scrutiny owner decision and the C++ gate precedent are unchanged; no verdict
was consumed, no closure / coverage / root claim is made. The standard 11x11
empty board, the 19 central-reply roots and all classes remain UNKNOWN.

Operator note (honest disclosure): the targets finished after the repo
recovered from the 04:52Z-05:02Z unreachable window; anchor k02a a and the
negatives were verified before it. All script pins are identical to the
published Part G experiment; the audit recomputed every gate from the raw
outputs after completion and passed twice byte-identically. The Part K
amendment recording this scope was appended to the single-owner note at
publication time (same lane, verdict-not-consumed verifier work).
