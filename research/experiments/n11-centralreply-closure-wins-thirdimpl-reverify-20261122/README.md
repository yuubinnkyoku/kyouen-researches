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

## Operator erratum (honest disclosure): first runner version mangled 121-bit keys

The first version of `run_thirdimpl.sh` looked up `--lo`/`--hi` from
`input/rows.json` inside a Node helper. `JSON.parse` -> JS Number ->
String concatenation silently rounds mantissa-precision integers
(observed: k02 `1297036692683751424` was passed as `...1400`, flipping the
stone popcount 5 -> 20). The damage was caught immediately by the pinned
driver's own fail-closed gates (`stone count mismatch: bits=20 declared=5`
on the k02 anchor before any search ran) - no solver search ever ran on a
mangled key, and no verdict, anchor or target row was produced by the buggy
runner. The runner was fixed to read lo/hi/legal/stones from the
machine-derived input CSV strings (exact integer tokens, no JS Number
round-trip), and `scripts/audit.py` gained gate G0 asserting that every
published `input/*.input.csv` equals its `rows.json` row in exact Python
integers. All anchor/negative/target runs published from
`output/anchors|negative|targets/` were produced by the fixed runner.

## Status: COMPLETED - all gates PASS (2026-11-22)

`scripts/audit.py` (fail-closed, run twice byte-identical): **171/171 gates PASS**.
Verdict agreements (third implementation vs published pinned-replica verdicts):

| row | replica verdict (15M df-pn nodes) | third_impl verdict (expansions) | runs |
|---|---|---|---|
| b018 `[1153204079095189504, 65536]` | WIN 1 (3,549,602) | **WIN 1** (3,972,982) | a/b identical |
| d002 `[3461016313634230272, 131072]` | WIN 1 (5,359,994) | **WIN 1** (6,144,044) | a/b identical |
| e002 `[1153765929805414400, 16]` | WIN 1 (14,112,632) | **WIN 1** (16,384,711) | a/b identical |
| f017 `[1188950301625810945, 70368744177666]` | WIN 1 (3,522,635) | **WIN 1** (4,038,798) | a/b identical |
| d001 / d003 / d004 / e001 / f001 / f005 / f009 / f013 / f016 / f018 | LOSS 2 (all 2-pass node-exact) | **LOSS 2** all ten (977,037 / 2,402,323 / 14,008,003 / 988,682 / 3,186,168 / 3,209,420 / 2,530,636 / 5,473,893 / 4,681,879 / 4,146,243) | a/b identical |

- Anchors on this host: k02 WIN 9,106,337 expansions / 4,991,527 ttHits and l1
  LOSS 7,660,602 expansions / 3,951,175 ttHits - **exactly** the published
  third-implementation values (host-independent determinism confirmed).
- Rules gate: quads 95,670 == replica; 195,044 triples, TBL==wob, 0 mismatches.
- Negative gates: ng1 / ng2 GATE_FAIL with the published messages.
- All runs `clean`, all 2-run pairs identical on (result, expansion, ttHits,
  overwrites), quads=95,670 in every output line, 0 wall-inconclusive rows.

**Interpretation (verdict-level corroboration only, NOT adoption):** the four
unconsumed closure WINs (b018/d002/e002/f017) now have a second, independent
(non-df-pn) re-derivation agreeing verdict-level, and 10 of the 21 unconsumed
LOSS rows agree spot-wise. This is strengthening evidence for the scrutiny
owner's adoption decision; the pre-registered C++ second-implementation gate
(pin `9193f5b6...`) remains the adoption gate. No verdict was consumed, no
class closure / coverage / root claim is made, and the standard 11x11 empty
board, the 19 central-reply roots and all classes remain UNKNOWN.
