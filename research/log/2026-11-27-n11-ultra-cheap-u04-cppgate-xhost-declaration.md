# Declaration: n11 ultra-cheap u04 C++ gate independent cross-host replication: single-owner declaration

**Declaration (publish-then-execute).** This lane declares an
independent cross-host replication of the published u04 WIN-row C++
scrutiny gate kit
`research/experiments/n11-ultra-cheap-u04-win-cppgate-20261127`
(commit `378ec332`, GATE-PASS `85,15000000,1,9149084`).  Kit:
`research/experiments/n11-ultra-cheap-u04-win-cppgate-xhost-20261127`.

## Protocol

1. **Fresh host, fresh toolchain**: gate source
   `kyouen_dfpn_root.cpp` sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`
   + headers `5976935dcfccb9b5...`/`2e36d69481fafcde...`
   byte-fetched from the published tenth-cost k01k02 cppgate kit and
   sha256-verified against the standing pins; zig 0.13.0 (tarball pin
   `d45312e6...`), `-std=c++20 -O2`, per the standing build recipe.
   Nothing from the owner lane's build is reused.
2. **Rows**: the u04 target row and the three published anchors
   (at2m `98,2000000,0,2000000`, aj001 `84,30000000,2,5156075`,
   af039 `89,30000000,2,19234232`) with inputs byte-verified
   against the published u04 cppgate kit MANIFEST (commit
   `378ec332`).  Two fresh-cold passes per row, one process per
   pass, fail-closed on any disagreement with the pre-pinned
   expected values (the published raws are the SSOT).
3. **Cross-check assertions**: u04 pair (legal,budget,result,nodes)
   == published raw node-exact; anchor raw outputs reproduce the
   published u04 cppgate kit raw sha256 values (cross-host
   determinism, u03-precedent extended to the u04 kit).
4. Nothing else runs in this Part.  No other key at any budget.

## Pre-registered expectation (disclosed before execution)

u04 GATE-PASS `85,15000000,1,9149084` (wall_s host-dependent,
disclosed not pinned); anchors 3/3 PASS with raw sha256 equal to
the published kit raws.  Any mismatch is a HARD-STOP and is
published as an experimental fact.

## Standing UNKNOWN notice

Pillar bookkeeping only; NO verdict consumed.  The standard 11x11
empty board, the two-stone root {60,27} and its remaining third
moves 100/108 stay UNKNOWN.  This Part does not adopt anything and
does not touch the separately declared u04 adoption flip-census
reaudit Part (declaration `34b3c559`, owned by another lane).
