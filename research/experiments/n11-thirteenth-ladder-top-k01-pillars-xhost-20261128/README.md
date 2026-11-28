# n11 thirteenth k01 pillars independent cross-host replication (XHOST-PASS)

Third-party execution kit of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k01-pillars-xhost-declaration.md`
(commit `958232d2`, publish-then-execute, single owner): an independent
cross-host replication of BOTH verification pillars of the thirteenth
ladder-top k01 WIN row `1153204147814662144:65536` (class 16757,
legal 72, WIN(1) nodes 2,678,305 @15M).  Precedent: the u04 C++ gate
cross-host replication kit (`580be905`, XHOST-PASS).  This Part is
disjoint from the k02 escalation/pillars declarations and from any
adoption Part; it runs only already-published evidence.

## Results (XHOST-PASS)

- **C++ gate (fresh zig 0.13.0 build on this host, gate source
  `9193f5b6...` + headers `5976935d...`/`2e36d694...` sha-verified,
  tarball pin `d45312e6` verified)**: k01 @15M cold pair
  **`72,15000000,1,2678305`** on both passes; both raws
  **byte-identical to the published cppgate kit raws** (`f1f5c49d`),
  including wall_s 5.  Pre-pinned expected matched exactly (fail-closed
  would have been recorded otherwise).
- **Anchors** (pre-declaration scratch, disclosed in the declaration):
  anchor-at2m `98,2000000,0,2000000` (raws byte-identical to
  published), anchor-aj001 `84,30000000,2,5156075` (p1 wall_s 11 vs
  published 10, node-exact; p2 byte-identical), anchor-af039
  `89,30000000,2,19234232` (wall_s 39 vs 38 both passes, node-exact).
  Host wall-clock jitter only, exactly the u04 xhost pattern.
- **third_impl.js `08ea958f...`** (standing pin, byte-fetched and
  sha-verified), `--row=k01 --stones=5 --legal=72
  --lo=1153204147814662144 --hi=65536 --cap=400000000 --wallcap=260
  --memo-power=22`, two fresh-cold passes: **result 1, expansions
  3,024,529, nodes 1,801,458, quads 95,670, ttOverwrites 44,704** on
  both passes (wall_s 9.01 / 8.91), field-identical to the published
  thirdimpl kit raws (8.94 / 8.90) except wall seconds.

Both pillars of the k01 WIN row now have a second host's
node-exact/field-exact confirmation.  NO verdict is consumed by this
kit: it is third-party replication bookkeeping of already-published
pillar evidence.

## Honest disclosures

- The three anchors were run as scratch before the declaration was
  pushed (disclosed in the declaration text itself, pre-pinned
  expected values, fail-closed comparisons).
- The k01 target row and the third_impl passes were run only after
  the declaration was on main.
- Nothing else was run in this Part: no k02 run, no head writing, no
  adoption.

## Files

- input/k01.input.csv, input/anchor-*.input.csv - sha-pinned probe
  inputs (byte-clones of the published escalation/cppgate kit inputs).
- output/raw/*.out - the eight fresh-cold gate raws.
- output/ti/k01.p1.txt, k01.p2.txt - the two third_impl passes.
- xhost-summary.json - machine summary (schema
  n11-thirteenth-ladder-top-k01-pillars-xhost-summary-v1).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Replication bookkeeping only; NO verdict consumed.  The standard 11x11
empty board, the 19 central-reply roots, the two-stone root {60,27}
and third moves 100/108 stay UNKNOWN.  Nodes, expansions and wall
seconds are bookkeeping, never verdicts.
