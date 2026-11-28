# 2026-11-28 n11 class-20421 k05 WIN pillars declaration

Single-owner declaration (publish-then-execute) for the two
implementation pillars of the class-20421 k05 WIN row
(`1152921642046849024:68719477248`, class 20421, s5 index 625899,
legal 78, WIN(1) nodes 2,007,513 @15M, class20421-k05 escalation
kit `9a87750e`, declaration `ddff08ce`): the C++ second-implementation
scrutiny gate and the standing third-implementation corroboration.
This lane is the declared owner of this Part; the target runs
happen only after this declaration is on main.

## Pre-registered plan

- C++ scrutiny gate (source `kyouen_dfpn_root.cpp` sha256
  `9193f5b6...` + headers `5976935d`/`2e36d694`, byte-verified from
  commit `154f3b7a` raw CDN fetches; zig 0.13.0 tarball pin
  `d45312e6...` verified, `-std=c++20 -O2`):
  - Target: k05 at the published escalation probe condition, budget
    15,000,000, expected gate row `78,15000000,1,2007513` (pinned
    from the published class20421-k05 escalation kit raws, the
    SSOT; raw sha256 pins `53c8b8ac...`/`27c15679...`), fresh cold
    pair (two independent processes), FAIL-closed on any
    disagreement.
  - Anchors (same source/pins as every prior cppgate kit):
    at2m `98,2000000,0,2000000` (budget 2M),
    aj001 `84,30000000,2,5156075` (budget 30M),
    af039 `89,30000000,2,19234232` (budget 30M); input pins
    `ecc0299b`/`2f6daea5`/`e51a3c9d`; cross-kit byte-comparison of
    the anchor raws against the published nineteenth k04 cppgate
    kit raws is expected modulo wall_s (cross-host determinism).
  - External tamper battery 4/4 fail-closed (target-input
    byte-tamper, anchor-input byte-tamper, expected-row tamper,
    raw tamper - each aborting at its own pin) + clean control
    re-PASS.
  - make_summary fail-closed (G0 input pins, G1 status log, G2
    raw-vs-expected + pair determinism, G3 anchor raw sha
    cross-kit pins), schema `n11-class20421-k05-cppgate-summary-v1`.
- Third implementation: `third_impl.js` sha256 `08ea958f...` (the
  pinned standing third implementation, byte-verified local copy),
  `--row=k05 --stones=5 --legal=78 --lo=1152921642046849024
  --hi=68719477248 --cap=400000000 --wallcap=260 --memo-power=22`,
  two cold passes; CORROBORATION-PASS requires result 1 on both
  passes with all counter fields identical (expansions/nodes are
  bookkeeping and are NOT pre-registered).  Schema
  `n11-class20421-k05-thirdimpl-summary-v1`.
- Outputs: two kits (cppgate + thirdimpl) with MANIFEST-sha256 +
  fetch-back, then a completion log.  After both pillars are
  COMPLETE, the k05-only canonical adoption is a SEPARATE declared
  Part (head of record `8cc87263` 6904/222/6682 + k05 WIN row ->
  expected merged shape 6,905 rows WIN 223 / LOSS 6682, increment,
  merger `90711961`, maker + tamper), followed by the WIN-side
  flip-census reaudit measuring the class-20421 closure-ladder EXIT
  (owner union [18683, 18710, 20421], serving class 20421 rank 1
  with unknown_now 1 -> 0 expected, with the standing pre-exclusion
  caveat on the serving class).

## Claim status

Pillar bookkeeping only: NO verdict is consumed.  Even with all
three implementations agreeing WIN(1), the row is cache
bookkeeping until a separately declared adoption Part adopts it.
Class 20421 is NOT complete until the adoption chain closes its
last cost-unknown and the reaudit measures the ladder EXIT.  The
standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 remain UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts.  This lane runs
without access to the user's computer (scheduled task);
publication is via the GitHub API only.
