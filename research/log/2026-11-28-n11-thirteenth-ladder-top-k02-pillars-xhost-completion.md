# 2026-11-28 n11 thirteenth k02 pillars cross-host replication completion

Completion log of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k02-pillars-xhost-declaration.md`
(declaration commit `5e85409f`, single owner, publish-then-execute).
Kit: `research/experiments/n11-thirteenth-ladder-top-k02-pillars-xhost-20261128/`.

## Result: XHOST-PASS (both pillars, second host, node-exact)

- **C++ gate** (same fresh zig 0.13.0 build as the k01 xhost Part,
  source `9193f5b6...` + headers sha-verified, tarball pin
  `d45312e6`): k02 `1152922672837951488:65792` @15M cold pair returns
  **`72,15000000,1,3485963`** on both passes, matching the pre-pinned
  expected value exactly, and both raws are **byte-identical to the
  published k02 cppgate kit raws** (commit `7ebf903e`), including
  wall_s 8.
- **third_impl** `08ea958f...` (standing pin), pinned invocation, two
  fresh-cold passes: **result 1, expansions 3,910,009, nodes
  2,425,008, quads 95,670, ttOverwrites 268,071** both passes
  (wall_s 12.88 / 12.61), field-identical to the published thirdimpl
  kit raws (12.14 / 12.04) except wall seconds.
- Anchors were not re-run (this host's full anchor evidence is
  published in the k01 xhost kit `eb542121` and was disclosed in the
  declaration).

Both verification pillars of BOTH thirteenth WIN rows (k01 and k02)
now carry a second host's independent node-exact/field-exact
confirmation.

## Honest disclosures

- The k02 target gate and third_impl runs happened only after the
  declaration was on main.
- This Part ran nothing else: no anchor re-run, no head writing, no
  adoption.

## Claim status

Replication bookkeeping only; NO verdict consumed.  The class-16757
adoption (single-owner declaration, standing WIN-side flip-census
review, owner-union pre-registration kit `fdb704d7`) remains a separate
future Part; class completion claims additionally require
Board-verified free_now at adoption time.  The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
third moves 100/108 stay UNKNOWN.  Nodes are bookkeeping, never
verdicts.
