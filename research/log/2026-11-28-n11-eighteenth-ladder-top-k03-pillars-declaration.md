# Declaration: n11 eighteenth ladder-top k03 WIN pillars (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published
BEFORE any run of this Part. The Part scrutinises the k03 WIN
row produced by the eighteenth ladder-top escalation (declaration
`53749821`, kit `88e825d5`, completion `a49957f6`): k03
`1155173441859489792:131072` (class 20421, legal 73, s5_index
605961, WIN(1) nodes 5,266,012 @15M, cold pair node-identical,
raws byte-identical `a80c2dcb`) against the canonical head
`e56ca5ca...` (6,902 rows WIN 220 / LOSS 6,682, target absent,
host-measured 0 rows). Declaration published at main HEAD
`a49957f66d1325f6d608a79531cfb7da9720cc40`.

## Pillar 1: C++ scrutiny gate (second implementation)

Byte-clone of the published seventeenth k02 cppgate kit
(`n11-seventeenth-ladder-top-k02-win-cppgate-20261128`, runner
`5ad2422e`, summary maker `44add05e`), differing only in the
comment block, the gate-rows target (k03, expected quad
`73,15000000,1,5266012`, input pin `ff63ed29...`), the
escalation basis (eighteenth kit `88e825d5`, raws
`a80c2dcb`/`a80c2dcb`), the head basis (`e56ca5ca...`,
6,902/220/6,682) and the schema names. Gate binary rebuilt from
the pinned gate source (`9193f5b6`/`5976935d`/`2e36d694`,
zig 0.13.0, tarball pin `d45312e6`) - binary bytes already
GATE-PASSED the seventeenth k02 gate this session line. Fresh-cold
pair for the target and all three anchors (at2m
`98,2000000,0,2000000`, aj001 `84,30000000,2,5156075`, af039
`89,30000000,2,19234232`, input pins re-verified); anchors
disclosed as byte-identical to the published seventeenth k02 gate
kit pins. Acceptance: pair determinism + expected-quad equality
on all four rows (fail-closed) + external tamper battery 4/4
fail-closed + clean control.

## Pillar 2: third-implementation corroboration

`third_impl.js` (sha256 `08ea958f...`, the pinned standing third
implementation, byte-verified local copy) with
`--row=k03 --stones=5 --legal=73 --lo=1155173441859489792
--hi=131072 --cap=400000000 --wallcap=260 --memo-power=22`,
two cold passes; acceptance: identical (result, expansions,
nodes, quads, ttOverwrites) on both passes and result consistency
with the 15M WIN(1) row (CORROBORATION-PASS at result level;
nodes/expansions are not required to match across
implementations).

## Non-meaning / status guard

Pillar bookkeeping only: NO verdict is consumed. Even a
two-pillar PASS is NOT an adoption: adoption of the k03 WIN row
requires a separate single-owner declaration (increment + merger
+ tamper battery + flip-census/reaudit with the shared-owner
pre-exclusion caveat; owner union k03 [18136, 18143, 20128,
20421]). Class 20421 is NOT complete (k04-k05 remain stage-1 2M
UNKNOWN). The standard 11x11 empty board, the 19 central-reply
roots, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN. Nodes, expansions and wall_s are
bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.
- The gate binary is re-verified by the anchor rows' expected
  quads (any binary drift fails closed on the anchors before the
  target row runs).
