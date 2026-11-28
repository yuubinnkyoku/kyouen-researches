# 2026-11-28 n11 thirteenth k01 pillars cross-host replication completion

Completion log of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k01-pillars-xhost-declaration.md`
(declaration commit `958232d2`, single owner, publish-then-execute).
Kit:
`research/experiments/n11-thirteenth-ladder-top-k01-pillars-xhost-20261128/`.

## Result: XHOST-PASS (both pillars, second host, node-exact)

- **C++ gate**: fresh zig 0.13.0 build (tarball pin `d45312e6`
  sha-verified, source `9193f5b6...` + headers `5976935d...`/
  `2e36d694...` sha-verified), k01 `1153204147814662144:65536` @15M
  cold pair returns **`72,15000000,1,2678305`** on both passes,
  matching the pre-pinned expected value exactly, and both raws are
  **byte-identical to the published cppgate kit raws** (commit
  `f1f5c49d`), including wall_s 5.
- **Anchors** (scratch, disclosed in the declaration): all three
  reproduce published values node-exactly (at2m byte-identical raws;
  aj001 p1 wall_s 11 vs 10; af039 wall_s 39 vs 38) - host wall-clock
  jitter only, the u04 xhost pattern.
- **third_impl** `08ea958f...` (standing pin), pinned invocation,
  two fresh-cold passes: **result 1, expansions 3,024,529, nodes
  1,801,458, quads 95,670, ttOverwrites 44,704** both passes
  (wall_s 9.01 / 8.91), field-identical to the published thirdimpl
  kit raws (8.94 / 8.90) except wall seconds.

Both verification pillars of the thirteenth k01 WIN row now carry a
second host's independent confirmation (four total implementations of
the evidence chain across two hosts: jsreplay escalation, C++ gate,
third_impl, and this cross-host replication of gate + third_impl).

## Honest disclosures

- Anchors were run as scratch before the declaration push (disclosed
  inside the declaration, pre-pinned, fail-closed).  The k01 gate
  target and the third_impl passes were run only after the declaration
  was on main.
- This Part ran nothing else: no k02 run at any budget, no head
  writing, no adoption, no selection change.

## Claim status

Replication bookkeeping only; NO verdict consumed.  The k01 WIN row
remains cache bookkeeping pending a declared adoption Part (standing
WIN-side flip-census review required); class 16757 completion needs
k02 resolution (owned by the parallel lane's k02 Part) and
Board-verified free_now at adoption time.  The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
third moves 100/108 stay UNKNOWN.  Nodes are bookkeeping, never
verdicts.
