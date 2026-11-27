# n11 ultra-cheap u01 WIN-row pillars (C++ scrutiny gate + third-implementation corroboration)

Pillar kit declared in
`research/log/2026-11-27-n11-ultra-cheap-u01-pillars-declaration.md`
for the ultra-cheap batch u01 WIN row
(`1153485622925590528:0`, class 1849, legal 88, replica WIN(1) nodes
4,893,014 at the 15M budget).  Status at publication: **DECLARED,
execution in progress**.

## Pre-registered expectations

- C++ gate target u01: `88,15000000,1,4893014` (two cold passes);
  anchors at2m `98,2000000,0,2000000`, aj001 `84,30000000,2,5156075`,
  af039 `89,30000000,2,19234232`.
- third_impl.js (`08ea958f...`): result 1 (WIN), expansions
  5,646,148, two cold passes, cap 400M, wallcap 260, memo-power 22.

## Files (wave A: declaration scaffold)

- input/u01.input.csv - byte-clone of the batch kit input row.
- input/anchor-at2m/aj001/af039.input.csv - the three standing anchor
  rows (byte-clones of the eleventh cppgate kit anchors).
- input/gate-rows.json - pre-registered expectations (schema
  n11-ultra-cheap-u01-win-pillars-rows-v1).
- scripts/gate_runner.sh - comment-block-only transform of the published
  SW/SX gate runner.
- Gate source and third_impl.js are NOT republished here; they are
  pinned by sha256 and byte-fetched from the published kits on main
  (eleventh k01 cppgate kit; ninth k12 corroboration kit), locally
  sha-verified before execution.

## Meaning and non-meaning

Pillar bookkeeping only: NO verdict is consumed, no class-status
change, no adoption.  Nodes and expansions are never evidence of WIN or
LOSS.  The standard 11x11 empty board, the two-stone root {60,27} and
its remaining third moves 100/108 stay UNKNOWN.
