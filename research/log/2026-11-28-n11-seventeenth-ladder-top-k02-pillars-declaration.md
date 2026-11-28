# Declaration: n11 seventeenth ladder-top k02 WIN pillars (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published
BEFORE any run of this Part. The Part scrutinises the k02 WIN
row produced by the seventeenth ladder-top escalation (declaration
`207339c8`, kit `bd63d669`): k02 `1156299204327378944:131072`
(class 20421, legal 73, s5_index 543795, WIN(1) nodes 4,997,146
@15M, cold pair node-identical) against the canonical head
`dbc1d950...` (6,901 rows WIN 219 / LOSS 6,682, target absent).

## Pillar 1: C++ scrutiny gate (second implementation)

Byte-clone of the published sixteenth k01 cppgate kit
(`n11-sixteenth-ladder-top-k01-win-cppgate-20261128`, runner
`f2ebcc3e`, summary maker `8b36a397`), differing only in the
comment block, the gate-rows target (k02, expected quad
`73,15000000,1,4997146`, input pin `67526707...`), the escalation
basis (seventeenth kit `bd63d669`, raws `85154222`/`322ebd94`),
the head basis (`dbc1d950...`, 6,901/219/6,682) and the schema
names. Gate binary rebuilt this session from the pinned gate
source (`9193f5b6`/`5976935d`/`2e36d69`, zig 0.13.0, tarball pin
`d45312e6`) - the same binary bytes already GATE-PASSED the k01
gate this session. Fresh-cold pair for the target and all three
anchors (at2m `98,2000000,0,2000000`, aj001
`84,30000000,2,5156075`, af039 `89,30000000,2,19234232`,
input pins re-verified); anchors disclosed as scratch-opened this
session (same anchor inputs, byte-identical to the published k01
gate kit pins). Acceptance: pair determinism + expected-quad
equality on all four rows (G0/G1/G2/G3 fail-closed) + external
tamper battery 4/4 fail-closed + clean control.

## Pillar 2: third-implementation corroboration

`third_impl.js` (sha256 `08ea958f...`, the pinned standing third
implementation, byte-verified local copy) with
`--row=k02 --stones=5 --legal=73 --lo=1156299204327378944
--hi=131072 --cap=400000000 --wallcap=260 --memo-power=22`,
two cold passes; acceptance: identical (result, expansions,
nodes, quads, ttOverwrites) on both passes and result consistency
with the 15M WIN(1) row (CORROBORATION-PASS at result level;
nodes/expansions are not required to match across
implementations).

## Non-meaning / status guard

Pillar bookkeeping only: NO verdict is consumed. Even a
two-pillar PASS is NOT an adoption: adoption of the k02 WIN row
requires a separate single-owner declaration (increment +
merger + tamper battery + flip-census/reaudit with the
shared-owner pre-exclusion caveat; owner union k02 [16104,
16132, 16656, 20421]). Class 20421 is NOT complete (k03-k05
remain stage-1 2M UNKNOWN). The standard 11x11 empty board, the
19 central-reply roots, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN. Nodes, expansions
and wall_s are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.
- The gate binary is not rebuilt between the k01 and k02 gate
  runs within this session (same pinned source, same toolchain);
  the k01 gate kit pins its build, and this Part re-verifies the
  binary by the anchor rows' expected quads (any binary drift
  fails closed on the anchors before the target row runs).
