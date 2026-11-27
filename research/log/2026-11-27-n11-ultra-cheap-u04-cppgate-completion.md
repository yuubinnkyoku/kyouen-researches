# Completion: n11 ultra-cheap u04 WIN-row C++ scrutiny gate (last open pillar closed)

Declaration `55918c0d` -> kit `n11-ultra-cheap-u04-win-cppgate-20261127`
(commit `378ec332`, fetch-back 19/19 byte-identical vs MANIFEST-sha256).

## Results

- **u04 GATE-PASS `85,15000000,1,9149084`** - fresh-cold pair
  node-identical, node-exact vs the published escalation raw (kit
  `24c5b85f`), wall_s 17 vs 18 only.  Gate source `9193f5b6...` +
  headers `5976935d...`/`2e36d694...` sha256-verified, zig 0.13.0
  (tarball pin `d45312e6...`), -std=c++20.
- Anchors 3/3 GATE-PASS (at2m/aj001/af039), pairs node-identical;
  anchor raws reproduce the published u03 pillars kit raw sha256
  values exactly (cross-host determinism).
- Tamper battery 4/4 fail-closed (T1 rc=43, T2 rc=42, T3 rc=2,
  T4 summary-gate G1 rc=1) + clean control re-PASS.
- **The two-pillar requirement for the u04 WIN row is COMPLETE**:
  escalation replica + C++ gate (this Part) + third-impl
  corroboration (kit `2691ac04`, CORROBORATION-PASS expansions
  10,728,035 x2).  Verdict-level WIN(1) agreement across three
  implementations.

## Honest disclosures

- This session's environment unexpectedly provided network + a
  usable toolchain (unlike the third-impl session), so the build and
  runs happened before the declaration was published; the declaration
  discloses this and all expectations are fail-closed pre-pins from
  the published raw.
- A comment-dedup fix on the runner (u03 comment-block-only transform,
  code region machine-verified identical) caused one extra u04
  runner invocation recorded in output/gate-status.log (fifth line,
  23:05:27Z, GATE-PASS unchanged; raws reused, not overwritten).
- No u04 adoption is performed by this Part; adoption requires the
  standing WIN-side flip-census review in a separate declared Part.

## Status guard

Pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping.
The standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
