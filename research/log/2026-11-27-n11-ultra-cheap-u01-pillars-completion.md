# n11 ultra-cheap u01 WIN-row pillars: completion log (2026-11-27)

Execution Part of the single-owner declaration
`research/log/2026-11-27-n11-ultra-cheap-u01-pillars-declaration.md`
(commit `616bec32`).  Kit:
`research/experiments/n11-ultra-cheap-u01-win-pillars-20261127`.

## Results

- C++ scrutiny gate (source `9193f5b6...` @`154f3b7a`, zig 0.13.0,
  -std=c++20): **u01 GATE-PASS `88,15000000,1,4893014`**, two
  fresh-cold passes node-exact with the published replica raw; anchors
  at2m/aj001/af039 GATE-PASS (`98,2000000,0,2000000`,
  `84,30000000,2,5156075`, `89,30000000,2,19234232`).  Tamper
  battery 4/4 fail-closed (T1 rc=43, T2 rc=42, T3 rc=2, T4 rc=1).
- Third implementation (`08ea958f...`, cap 400M, wallcap 260,
  memo-power 22): both fresh post-declaration cold passes **WIN(1)**,
  expansions 5,646,148 identical and equal to the pre-registered
  calibration value, legal 88 = 88, reason clean, node_rc 0 —
  **CORROBORATION-PASS (verdict-level)**.
- Head freshness: u01 absent from head `1e2eeda2...` (6,890 rows
  WIN 208 / LOSS 6,682).

The u01 WIN row now has 3/3 pillars (replica cold pair + C++ gate +
third implementation) and is adoption-eligible.  Adoption is a separate
future Part.

## Honest disclosures

- The pre-declaration third_impl calibration pair was disclosed in the
  declaration; the official pair was re-run fresh post-declaration and
  is expansions-identical.
- zig emits a glibc-version warning (host 2.41 vs provided 2.39); all
  rows ran to replay_done.
- The first tamper-battery recording pass ran on an already-tampered
  copy (T1 detected the stale p2 mismatch, rc=42); the battery was
  re-recorded on a fresh copy and that clean log is published.
- wall_s fields differ across passes; timing is not evidence.
- A run of the m=27 three-row SAT lane and other lanes' commits landed
  between this lane's pushes; no conflict with this Part's files.

## Meaning and non-meaning

Pillar bookkeeping only.  The verdict is NOT consumed: no cache
increment, no class-status change, no coverage claim, no adoption.
Nodes and expansions are never evidence of WIN or LOSS.  The standard
11x11 empty board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.
The two-stone root {60,27} and its remaining third moves 100/108:
UNKNOWN.  All closure classes: UNKNOWN.

Next Part (candidate, this lane, fresh declaration required): u01
adoption (BASE `1e2eeda2...`, increment 1 WIN row
`1153485622925590528:0` nodes 4,893,014 bookkeeping, expected shape
6,891 rows WIN 209 / LOSS 6,682, class 1849 completion Board-verified
free_now at adoption time, merger `90711961...`, then flip-census +
reaudit refresh).  Alternatively another lane may take it.
