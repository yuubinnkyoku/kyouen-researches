# n11 ultra-cheap u01 WIN-row pillars: single-owner declaration

**Declaration (publish-then-execute).** This lane declares the two
standing pillars for the ultra-cheap batch u01 WIN row
(`1153485622925590528:0`, class 1849, legal 88, replica 15M WIN(1)
nodes 4,893,014, published in
`research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127`,
commit `a99be0f8`): the C++ second-implementation scrutiny gate and
the third-implementation corroboration.  Kit:
`research/experiments/n11-ultra-cheap-u01-win-pillars-20261127`.

## Protocol

1. **C++ gate**: gate source `kyouen_dfpn_root.cpp` (canonical pin
   `9193f5b6...` @`154f3b7a`, byte-fetched from the eleventh k01
   cppgate kit and sha-verified locally) + headers
   `kyouen_residual_micro.hpp` (`5976935d...`) and
   `n11_s5_quarantine.hpp` (`2e36d694...`), compiled with zig 0.13.0
   (tarball sha256 `d45312e6...`), `-std=c++20`.  Runner
   `scripts/gate_runner.sh` is a comment-block-only transform of the
   published SW/SX runner.  Two fresh-cold passes for the target and
   the three standing anchors (at2m/aj001/af039), expected quadruples
   pre-registered in `input/gate-rows.json`:
   u01 `88,15000000,1,4893014`; anchors `98,2000000,0,2000000`,
   `84,30000000,2,5156075`, `89,30000000,2,19234232`.
2. **Third implementation**: standing `third_impl.js`
   (`08ea958f...`, byte-fetched from the ninth k12 corroboration kit,
   sha-verified), cap 400,000,000, wallcap 260, memo-power 22, two
   fresh cold passes, expected result 1 (WIN); expansions
   pre-registered at 5,646,148 from the disclosed calibration pair.
3. Nothing else runs in this Part.

## Pre-declaration calibration (disclosed)

A pre-declaration calibration pair of third_impl.js on u01 was executed
(result 1 in both passes, expansions 5,646,148 mutually identical,
ttHits 3,187,475, legal derived 88 = 88, reason clean, cap 400M,
wallcap 260).  It is used only to pre-register the expansion count; the
official pair of this Part is re-run fresh after this declaration and
the calibration raws are not part of the official pair.  No C++ gate
row was run before this declaration (binary build and `--help` sanity
only).

## Freshness gate

Canonical head of record `1e2eeda2...` (6,890 rows WIN 208 / LOSS
6,682, fetched and sha256-verified from the eleventh k01 adoption kit):
the u01 key `1153485622925590528:0` is ABSENT from the head
(machine-checked, fresh).

## Pillar policy

These pillars make the u01 WIN row adoption-eligible (3/3 pillars:
replica cold pair + C++ gate + third implementation), but adoption is a
SEPARATE future Part requiring a fresh single-owner declaration, the
WIN/LOSS conflict review, the standing flip-census review (class 1849
completion would be Board-verified free_now at adoption time), and the
merger.  The verdict is NOT consumed by this Part.

## Meaning and non-meaning

The standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  The two-stone root {60,27} and its remaining third moves
100/108: UNKNOWN.  All closure classes: UNKNOWN.  Nodes and expansions
are bookkeeping, never evidence of WIN or LOSS.

This lane runs without access to the user's computer (scheduled task);
publication via the GitHub API only.
