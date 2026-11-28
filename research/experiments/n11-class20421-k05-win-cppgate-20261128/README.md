# n11 class-20421 k05 WIN cppgate

Execution kit of the C++ second-implementation scrutiny gate for
the class-20421 k05 WIN row
(`1152921642046849024:68719477248`, class 20421, s5 index 625899,
legal 78, WIN(1) nodes 2,007,513 @15M, class20421-k05 escalation
kit `9a87750e`, declaration `ddff08ce`), declared in
`research/log/2026-11-28-n11-class20421-k05-pillars-declaration.md`
(commit `772c04bc`, single owner, publish-then-execute), against
the canonical head of record `8cc87263...` (6,904 rows WIN 222 /
LOSS 6,682; target absent from the head).

## Result

GATE-PASS `78,15000000,1,2007513` - the fresh-cold C++ pair is
node-exact against the published class20421-k05 escalation raws
(k05 WIN(1) at 15M) on (legal, budget, result, nodes), with
2-pass determinism. Anchors 3/3: at2m `98,2000000,0,2000000`,
aj001 `84,30000000,2,5156075`, af039 `89,30000000,2,19234232`
(anchor inputs byte-identical to the published pins; the anchor
raw rows are node-exact against the published nineteenth k04
cppgate kit raws, wall_s-only difference, cross-host determinism,
disclosed in the declaration).

- G0 input pins: k05 `565a6505...` (byte-clone of the published
  class20421-k05 escalation kit input) + 3 anchor pins.
- G1 status log sanity: GATE-PASS lines for k05 and all anchors.
- G2 raw-vs-expected + fresh-cold pair determinism on all four
  rows.
- G3 anchor raw sha cross-kit pins (in gate-rows.json).
- External tamper battery 4/4 fail-closed (T1 target-input
  byte-tamper aborts at G0, T2 anchor-input byte-tamper aborts at
  G0, T3 expected-row tamper aborts at G2, T4 raw verdict flip
  aborts at G2; every probe's input restored byte-identical from
  backups, sha-verified) + clean control SUMMARY-PASS. The full
  battery outcome log is published as
  `output/tamper-battery-stdout.log`.
- With the companion third-implementation corroboration kit
  (`n11-class20421-k05-thirdimpl-20261128`, CORROBORATION-PASS,
  result 1, expansions 2,292,427 x2 identical), the two-pillar
  requirement for the k05 WIN row is COMPLETE: verdict-level
  WIN(1) agreement across all three implementations (jsreplay
  replica, C++ gate, third implementation). Adoption remains a
  separate declared Part (canonical merge to expected 6,905 rows
  WIN 223 / LOSS 6,682, merger `90711961`, maker + tamper) +
  WIN-side flip-census/reaudit measuring the class-20421
  closure-ladder EXIT (owner union [18683, 18710, 20421], the
  serving class 20421 rank 1 unknown_now 1 -> 0 expected, with
  the standing pre-exclusion caveat on the serving class).

## Honest disclosures

- The gate binary is the pinned-source zig 0.13.0 build (source
  `9193f5b6`/`5976935d`/`2e36d694`, tarball pin `d45312e6`).
- The anchors are byte-identical to the published anchor pins,
  and their raw quads reproduce the published expected values
  node-exactly (wall_s only differs, cross-host).
- The tamper battery outcome log records each probe's
  fail-closed abort point (G0/G2) and the clean-control
  re-PASS; it is the battery's honest execution record.
- This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.

## Files

- `input/` - k05.input.csv (published escalation input pin) +
  3 anchor inputs + gate-rows.json (kit schema
  `n11-class20421-k05-cppgate-rows-v1`).
- `scripts/gate_runner.sh` - the gate runner (machine-identical
  to the published prior-lane runners; only the comment block
  differs).
- `scripts/make_summary.py` - the fail-closed summary maker
  (machine-identical to the published prior-lane makers except
  docstring and schema name).
- `output/gate-status.log` - honest per-row status.
- `output/raw/*.out` - 8 cold-pass raws (k05 + 3 anchors, p1/p2).
- `output/cppgate-summary.json` - machine-readable summary
  (schema `n11-class20421-k05-cppgate-summary-v1`).
- `output/tamper-battery-stdout.log` - the tamper battery outcome
  log (4/4 fail-closed + clean control).
- `DECLARATION.md` - byte-copy of the published k05 pillars
  declaration.
- `MANIFEST-sha256.txt` - sha256 of every kit file.

## Status guard

Pillar bookkeeping only: NO verdict consumed. Even with the
two-pillar COMPLETE, the k05 WIN(1) row is NOT adopted by this
kit; adoption requires a separate single-owner declaration.
Class 20421 is NOT complete until the adoption chain closes its
last cost-unknown and the reaudit measures the ladder EXIT. The
standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts.
