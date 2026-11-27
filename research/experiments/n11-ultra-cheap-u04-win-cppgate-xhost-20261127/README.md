# n11 ultra-cheap u04 WIN-row C++ gate - independent cross-host replication

Independent cross-host replication (XHOST) of the published u04
WIN-row C++ scrutiny gate kit
`research/experiments/n11-ultra-cheap-u04-win-cppgate-20261127`
(commit `378ec332`, declaration `55918c0d`).  Declaration for this
Part: `research/log/2026-11-27-n11-ultra-cheap-u04-cppgate-xhost-declaration.md`
(commit `7c2c4af6`, publish-then-execute; every expected value was
pre-pinned fail-closed before any run).

## Results - XHOST-PASS 4/4

- **u04 GATE-PASS `85,15000000,1,9149084`** (fresh-cold pair
  node-identical, node-exact vs the published raw; wall_s 18/18 vs
  published 17/18, host wall-clock only).
- Anchors 3/3 GATE-PASS node-exact: at2m
  `98,2000000,0,2000000` (wall 3/3), aj001
  `84,30000000,2,5156075` (wall 9/9 vs published 10/10), af039
  `89,30000000,2,19234232` (wall 39/38 vs published 38/37).
- Raw-level cross-host determinism: of the 8 fresh raws, 3 are
  byte-identical to the published kit raws (at2m p1/p2, u04 p2) and
  the remaining 5 differ ONLY in the wall_s field (verified by
  field-wise diff; my af039.p2 sha256 equals the published
  af039.p1).  All 8/8 raws are node-exact: (legal,budget,result,
  nodes) identical to the published values, fail-closed pre-pinned.
- Gate binary rebuilt from scratch on a fresh host: source
  `kyouen_dfpn_root.cpp` sha256
  `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`
  + headers `5976935dcfccb9b5...`/`2e36d69481fafcde...`
  (byte-fetched from the published tenth-cost k01k02 cppgate kit,
  sha256-verified), zig 0.13.0 (tarball pin `d45312e6...`),
  `zig c++ -std=c++20 -O2`.

## Honest disclosures

- The published kit's README claim "anchor raws reproduce the
  published raw sha256 values exactly" holds on this host only
  where wall_s coincides (at2m x2; u04.p2).  Raw sha equality is
  wall_s-fragile; the robust cross-host invariant is node-exactness,
  which holds 8/8 here and in the owner lane's u03-anchor runs.
- The inputs are byte-clones of the published u04 cppgate kit inputs
  (sha256-pinned in input/gate-rows.json, verified against its
  MANIFEST at commit `378ec332`).  The runner script is the published
  kit's `gate_runner.sh` byte-clone (not republished here; pin
  `f2ebcc3e...` in the published kit MANIFEST).
- Deviation from the declaration text: the declaration said anchor
  raw outputs "reproduce the published kit raw sha256 values";
  measured: only wall_s-coincident raws do.  Recorded as an
  experimental fact; node-exactness (the substantive assertion)
  holds unconditionally.
- This Part consumed no verdict and adopted nothing.  It is disjoint
  from the u04 adoption flip-census reaudit Part (declaration
  `34b3c559`, another lane).

## Files

- input/gate-rows.json - machine pin of rows/expectations (byte-copy
  of the published kit's, which records the u03-head basis
  `c5082866`; this Part only replays published rows).
- input/*.input.csv - byte-clone probe inputs.
- output/raw/*.out - the eight fresh-cold raws.
- output/gate-status.log - runner status lines.
- output/xhost-summary.json - machine summary (schema
  n11-ultra-cheap-u04-win-cppgate-xhost-summary-v1).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping,
never evidence.  The standard 11x11 empty board, the two-stone root
{60,27} and its remaining third moves 100/108 stay UNKNOWN.
