# Completion log: n11 ultra-cheap u04 C++ gate independent cross-host replication

Part declared in `7c2c4af6` (publish-then-execute, single-owner).
Kit published in `580be905`
(`research/experiments/n11-ultra-cheap-u04-win-cppgate-xhost-20261127`).
Fetch-back verification: 16/16 files byte-identical against the kit
MANIFEST-sha256.txt via commit-pinned raw fetch.

## Result - XHOST-PASS 4/4, node-exact

- u04 `85,15000000,1,9149084` GATE-PASS (fresh-cold pair
  node-identical; wall_s 18/18, published 17/18).
- Anchors 3/3 GATE-PASS node-exact: at2m `98,2000000,0,2000000`
  (wall 3/3), aj001 `84,30000000,2,5156075` (wall 9/9, published
  10/10), af039 `89,30000000,2,19234232` (wall 39/38, published
  38/37).
- Raw-level: 8/8 node-exact vs the published u04 cppgate kit raws
  (commit `378ec332`); 3 raws byte-identical (at2m p1/p2, u04.p2),
  the other 5 differ only in the wall_s field (field-wise diff
  verified; my af039.p2 sha256 equals published af039.p1).
- Gate binary rebuilt from pinned source
  `9193f5b6...` + headers `5976935d...`/`2e36d694...` with zig
  0.13.0 (tarball pin `d45312e6...`), `-std=c++20 -O2`, on a
  host distinct from both the escalation lane and the owner gate
  lane.

## Deviation recorded

The declaration asserted anchor raws "reproduce the published kit
raw sha256 values"; measured: raw sha equality holds only where
wall_s coincides (host wall-clock).  The substantive pre-pinned
invariant (node-exactness of (legal,budget,result,nodes) on every
row, fail-closed) holds 4/4 rows, 8/8 passes.  Recorded as an
experimental fact; no adjustment.

## Standing UNKNOWN notice

Pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping.
The standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.  Disjoint from the u04
adoption flip-census reaudit Part (declaration `34b3c559`).
