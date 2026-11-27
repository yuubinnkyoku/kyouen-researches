# n11 ultra-cheap u02 WIN-row pillars: single-owner declaration (publish-then-execute)

- Date: 2026-11-27 (declared before execution; the official pillar runs execute after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly sessions: do not run the u02 gate or third-impl rows below.

## Target row

- u02 `1297036830121656320:131074` (class 2251, legal 80, s5 index 93815), replica WIN(1) nodes 3,167,121 at the 15M budget, published in `research/experiments/n11-ultra-cheap-u02-escalation-15m-20261127` (commit `82d41abc`), under canonical head `0ec4080d...` (6,891 rows WIN 209 / LOSS 6,682).

## Pre-registered expectations

- C++ second-implementation scrutiny gate (source `kyouen_dfpn_root.cpp` sha256 `9193f5b6...` + headers `5976935d...`, `2e36d694...`, byte-fetched from the published eleventh k01 cppgate kit and locally sha-verified; zig 0.13.0 tarball `d45312e6...`, -std=c++20 -O3): u02 expected `80,15000000,1,3167121` (two fresh-cold passes, node-exact with the published replica raw). Anchors (byte-clones of the published u01-pillars inputs): at2m `98,2000000,0,2000000`, aj001 `84,30000000,2,5156075`, af039 `89,30000000,2,19234232`. Tamper battery fail-closed 4/4.
- Third-implementation corroboration (standing `third_impl.js` sha256 `08ea958f...`, --row=u02 --stones=5 --legal=80 --lo=1297036830121656320 --hi=131074 --cap=400000000 --wallcap=260 --memo-power=22): expected result 1 (WIN), expansions 3,595,562, two fresh cold passes mutually identical (wall_s excluded), legal derived 80, reason clean.

## Pre-declaration disclosures

- Third_impl calibration pair (u02, disclosed here): both passes result 1, expansions 3,595,562, ttHits 2,114,848, legal 80 = 80, clean, mutually identical. The official pair is re-run fresh post-declaration.
- No other key or row will be run in this Part.

## Status guard

Pillar bookkeeping only. NO verdict is consumed; no class-status change; no adoption (adoption of u02 remains a SEPARATE future Part with its own declaration, WIN/LOSS conflict review, standing flip-census review, and merger). Nodes and expansions are bookkeeping, never evidence of WIN or LOSS. The standard 11x11 empty board, the two-stone root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
