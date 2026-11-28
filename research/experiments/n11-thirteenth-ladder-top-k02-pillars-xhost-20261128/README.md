# n11 thirteenth k02 pillars independent cross-host replication (XHOST-PASS)

Third-party execution kit of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k02-pillars-xhost-declaration.md`
(commit `5e85409f`, publish-then-execute, single owner): an independent
cross-host replication of BOTH verification pillars of the thirteenth
ladder-top k02 WIN row `1152922672837951488:65792` (class 16757,
legal 72, WIN(1) nodes 3,485,963 @15M), pillar-verified by the parallel
lane (declaration `177b1086`, completion `7ebf903e`).  Pattern
precedent: the k01 xhost kit (`eb542121`, this lane).

## Results (XHOST-PASS)

- **C++ gate** (same fresh zig 0.13.0 build as the k01 xhost Part;
  source `9193f5b6...` + headers, tarball pin `d45312e6`, sha-verified):
  k02 @15M cold pair **`72,15000000,1,3485963`** on both passes,
  matching the pre-pinned expected value exactly, and both raws are
  **byte-identical to the published k02 cppgate kit raws**, including
  wall_s 8.
- **third_impl.js `08ea958f...`** (standing pin), pinned invocation,
  two fresh-cold passes: **result 1, expansions 3,910,009, nodes
  2,425,008, quads 95,670, ttOverwrites 268,071** both passes
  (wall_s 12.88 / 12.61), field-identical to the published thirdimpl
  kit raws (12.14 / 12.04) except wall seconds.
- Anchors were not re-run in this Part: this host's full anchor
  evidence (all three node-exact) is published in the k01 xhost kit
  and was disclosed in the declaration.

Both pillars of the k02 WIN row now carry a second host's independent
confirmation, symmetric with k01.  NO verdict is consumed by this
kit.

## Files

- input/k02.input.csv - sha-pinned probe input (byte-clone of the
  published escalation kit input).
- output/raw/k02.p1.out, k02.p2.out - the fresh-cold gate pair.
- output/ti/k02.p1.txt, k02.p2.txt - the two third_impl passes.
- xhost-summary.json - machine summary (schema
  n11-thirteenth-ladder-top-k02-pillars-xhost-summary-v1).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Replication bookkeeping only; NO verdict consumed.  The standard 11x11
empty board, the 19 central-reply roots, the two-stone root {60,27}
and third moves 100/108 stay UNKNOWN.  Nodes, expansions and wall
seconds are bookkeeping, never verdicts.
