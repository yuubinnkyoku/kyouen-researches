# n11 central-reply closure: third-implementation cross-verification of the unconsumed WINs (2026-11-22)

Part G of the central-reply 19-root closure grind (K0415/K0417 line), declared as an
amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

## What this is

The closure batches 1/3/4/5 left **four unconsumed WIN verdicts** (all 2-pass
node-exact at budget 15M from the pinned `jsreplay.js` replica, sha256
`84585617...`):

- b018 (batch 1, class 16757): key `[1153204079095189504, 65536]`, legal 60, WIN 3,549,602 nodes
- d002 (batch 3, class 20421): key `[3461016313634230272, 131072]`, legal 73, WIN 5,359,994 nodes
- e002 (batch 4, class 16371): key `[1153765929805414400, 16]`, legal 79, WIN 14,112,632 nodes
- f017 (batch 5, class 12264): key `[1188950301625810945, 70368744177666]`, legal 82, WIN 3,522,635 nodes

plus 21 two-pass LOSS rows, all awaiting the scrutiny owner. The pre-registered
adoption gate is the C++ second implementation (`cpp/solvers/kyouen_dfpn_root.cpp`,
pin `9193f5b6...`), which cannot run in this lane's environment (no compiler,
package installation forbidden). Following the precedent of
`research/experiments/n11-sixthcost-third-implementation-verdict-reverification-20261121/`,
this experiment runs the **third implementation** (`third_impl.js`: non-df-pn
AND/OR minimax with a D4-canonical completion memo and slab TT; pinned bytes
sha256 `08ea958f...`, identical to the published experiment) as **verdict-level**
cross-verification evidence for the owner's adoption decision.

**It consumes and changes no corpus verdict. All pre-existing gates are untouched.
The standard 11x11 empty board, the 19 central-reply roots, and every closure
class remain UNKNOWN. Nodes/expansions are not verdicts.**

## Targets (machine-derived, no hand transcription)

- 4 WIN rows: b018, d002, e002, f017 (full re-verification)
- 10 LOSS spot rows (stratified sample across batches 3/4/5):
  d001, d003, d004, e001, f001, f005, f009, f013, f016, f018
- 2 published third-implementation anchors reproduced on this host:
  k02 (WIN, legal 87, expected 9,106,337 expansions / 4,991,527 ttHits)
  and legacy L1 (LOSS, legal 116, expected 7,660,602 expansions / 3,951,175 ttHits)
- 2 negative input gates (must GATE_FAIL): ng1 (k02 legal 88), ng2 (k02 stones 6)

Inputs `input/*.input.csv` and `input/rows.json` are derived from the published
raws by `scripts/make_inputs.py` (fail-closed: source passes must themselves be
node-exact 2-pass rows, schema-checked).

## Protocol

- solver: `scripts/third_impl.js` (byte-pinned), one process per row,
  `--cap=300000000 --wallcap=240 --memo-power=22`, 2 runs (a/b) per row;
  runner `scripts/run_thirdimpl.sh`; status log `output/status.log`
- rule-engine gate before any target run: `scripts/verify_tbl.js`
  (forbidden-quad count 95,670 == replica `buildCompletionTable()`;
  TBL danger sets == replica `wob` on the deterministic triple sweep, mismatches 0),
  captured in `output/rules-gate.txt`
- `--legal` declared per row: the driver's derived legal count must equal it
  (fail-closed GATE_FAIL otherwise; negative gate ng1 exercises this)
- determinism gate: each row's (result, expansion, ttHits, reason) must be
  identical across a/b
- verdict agreement: a clean third-impl result must equal the published
  replica verdict (WIN rows -> 1, LOSS rows -> 2). A wall/cap `runlimit` is
  recorded as **wall-inconclusive** (honest negative, NOT a verdict). A clean
  divergence is recorded as divergence evidence - it never flips a verdict
  here; the adoption decision stays with the scrutiny owner.
- audit: `scripts/audit.py` recomputes every gate from the raw outputs
  (fail-closed, exit 1 on any gate failure) and writes
  `output/audit-summary.json`; run twice, outputs must be byte-identical.

## Sources (published, pinned)

- batch raws: `research/experiments/n11-centralreply-closure-class16757-batch-20261122/`
  and `-class20421-`, `-class16371-`, `-class12264-` (identical bytes mirrored in
  the lane kit `_19root-refresh-kit/batch*/output/raw/`)
- third-implementation anchor values: the published
  `n11-sixthcost-third-implementation-verdict-reverification-20261121`
  witness outputs (deterministic, host-independent counts)

## Status

see `output/status.log` and `output/audit-summary.json`.

The standard 11x11 empty board, the 19 central-reply roots and all classes
remain UNKNOWN throughout. Expansions and node counts are not verdicts.
