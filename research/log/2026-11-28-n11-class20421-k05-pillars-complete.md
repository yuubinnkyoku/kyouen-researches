# 2026-11-28 n11 class-20421 k05 WIN pillars COMPLETE

Completion log for the two implementation pillars of the
class-20421 k05 WIN row (`1152921642046849024:68719477248`,
class 20421, s5 index 625899, legal 78), declared in
`research/log/2026-11-28-n11-class20421-k05-pillars-declaration.md`
(commit `772c04bc`, publish-then-execute, single owner), executed
after publication on main.

## Results

- **C++ scrutiny gate: GATE-PASS `78,15000000,1,2007513`.** The
  fresh-cold C++ pair (pinned source `9193f5b6`/`5976935d`/
  `2e36d694`, zig 0.13.0 pin `d45312e6`) is node-exact against
  the published class20421-k05 escalation raws (k05 WIN(1)
  nodes 2,007,513 @15M, kit `9a87750e`), 2-pass determinism.
  Anchors 3/3 node-exact against the published nineteenth k04
  cppgate kit raws (wall_s-only cross-host difference).
  Tamper battery 4/4 fail-closed (T1/T2 abort at G0, T3/T4 abort
  at G2, all inputs restored sha-verified) + clean control
  SUMMARY-PASS. Kit
  `research/experiments/n11-class20421-k05-win-cppgate-20261128/`
  (commit `c34e82ee`,
  fetch-back 21/21 byte-identical, commit-pinned raw CDN).
- **Third implementation: CORROBORATION-PASS.** `third_impl.js`
  (sha256 pin `08ea958f...`) with `--row=k05 --stones=5 --legal=78
  --lo=1152921642046849024 --hi=68719477248 --cap=400000000
  --wallcap=260 --memo-power=22`: result 1 on both cold passes,
  expansions 2,292,427, nodes 1,279,838, quads 95,670,
  ttOverwrites 3,031 - identical both passes (wall_s 7.09/7.27
  host timing only). Kit
  `research/experiments/n11-class20421-k05-thirdimpl-20261128/`
  (fetch-back 5/5 byte-identical, commit-pinned raw CDN; total 26/26).

**Two-pillar requirement for the k05 WIN row is COMPLETE:**
verdict-level WIN(1) agreement across all three implementations
(jsreplay replica, C++ gate, third implementation).

## Status guard

NO verdict consumed. The k05 WIN(1) row is NOT adopted by this
Part; adoption requires a separate single-owner declaration
(canonical merge head `8cc87263` 6,904/222/6,682 + k05 WIN row ->
expected 6,905 rows WIN 223 / LOSS 6,682, merger `90711961`,
maker + tamper), followed by the WIN-side flip-census/reaudit
measuring the class-20421 closure-ladder EXIT (owner union
[18683, 18710, 20421], serving class 20421 rank 1 unknown_now
1 -> 0 expected, standing pre-exclusion caveat on the serving
class). Class 20421 is NOT complete until that chain closes.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 remain UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts. This lane runs
without access to the user's computer (scheduled task);
publication is via the GitHub API only.
