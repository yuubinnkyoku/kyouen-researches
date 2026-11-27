# n11-eleventhcost-k01-win-thirdimpl-corroboration-20261127

Third-implementation corroboration pillar for the eleventh-cost k01
WIN row (key `1297036696978718720:64`, legal 88, replica stage 15M
WIN(1) nodes 12,755,963, published eleventh-cost batch kit, commit
aaeb282c).  Declared in
research/log/2026-11-27-n11-eleventhcost-k01-win-thirdimpl-corroboration-declaration.md
(commit 83804e01).

## Result: CORROBORATION-PASS (verdict-level)

- third_impl.js (pinned standing implementation, sha256 08ea958f...,
  byte-clone of the published ninth-cost k12 corroboration kit copy)
  reported **result 1 (WIN)** for k01 in both fresh cold passes,
  expansions 15,339,759 mutually identical (ttHits 8,124,169, quads
  95670, memoPower 22, legal derived 88 = legalIn 88, reason clean,
  cap 400,000,000, wallcap 260, node_rc=0 in both raws).
- Replica (jsreplay 84585617) had reported WIN(1) nodes 12,755,963,
  cold pair node-identical (published batch kit raws).
- Verdict-level agreement: the third implementation agrees with the
  replica that k01 is WIN(1).  Node and expansion counts are
  bookkeeping and are not expected to match across implementations.

## Honest disclosures

- No lower-cap exploratory pass was needed: both published passes
  resolved clean at the first attempt (the k12 precedent's 15M
  runlimit INDET observation does not apply here; both passes were
  run at cap 400,000,000 from the start).
- The wall_s field differs per pass (42.97 / 43.28); timing is not
  evidence.
- This is one of the two pillars required before any adoption of the
  k01 WIN row.  The C++ second-implementation scrutiny gate (Part
  SW/SX/tenth-gate pattern, expected quadruple 88,15000000,1,12755963)
  remains pending.
- The verdict is NOT consumed: no cache increment, no class-status
  change, no coverage claim, no adoption.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Files

- scripts/third_impl.js: byte-clone of the pinned third implementation
  (sha256 08ea958f...).
- output/raw/k01.p1.txt, output/raw/k01.p2.txt: the two cold-pass raws
  (each with node_rc=0 trailer captured by the shell in the same
  command).
- MANIFEST-sha256.txt: kit manifest.

## Guards

The standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair {100,108}:
UNKNOWN.  Every closure class: UNKNOWN unless a published Part says
otherwise.  A third-implementation WIN(1) agreement is not a class
closure claim, not a root verdict, and transfers nothing.
