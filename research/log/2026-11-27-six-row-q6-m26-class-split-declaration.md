# 2026-11-27 Six-row q=6, 6x26: class {2} krow/minpos decomposition sweep — declaration

## Status

Single-owner declaration (publish-then-execute). Declaration-time HEAD `f45869dd70d86d6b2c873fcb6b9cd1674dec5efb` (main, 2026-11-27T11:11:41Z). No other lane has declared (6,6) 6x26 SAT-side work (the six-row q6 6x26 two-edit surgery closed at `81703981` on 2026-11-27; the eighth-q10 8x26 lane `76df588e` and the ninth-cost lane `59db0d52` are disjoint).

## Motivation

The same krow/minpos decomposition resolved the (6,7) 6x22 frontier today (declaration `d35234a7`, kit `03487c4b`: the plain class {2} 280s/5.04M INDET collapsed to SAT at krow=2:5 minpos=7, 2,050,424 conflicts, witness verified -> M_{6,7} >= 23). The (6,6) frontier 6x26 has the same shape of published records: plain class {2} INDET, class {1} krow INDET, two-edit surgery of the m=25 K1217 witness NEGATIVE, right-shift/translation one-stone-short structure.

## Target

6x26 q=6, **class {2}, krow=2:4** (single-deficiency, 29 stones, deficient row 2 with 4 stones as in the m=24/m=25 witness family) with `--minpos=P` for P in 0..22 (disjoint exhaustive split), prioritized around the m=25 witness geometry (its row-2 leftmost stone at x=11). If time permits: class {1} krow=1:4 minpos probes and unswept classes.

Decoding conventions: SAT in any deciding sub-instance => a 6x26 deficient-maximal witness exists => **M_{6,6} >= 27** (range 27..495). All sub-instances UNSAT => class {2} k=4 witness-free at 6x26 (partial absence). INDET at cap => honest negative, not absence.

## Engine and calibration plan

- Same byte-cloned machinery as the 6x22 kit (sat3.js/sat2.js/sat.js, K0818/K0810 core) and kissat 4.0.4 official linux-amd64 (sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`).
- Positive control before the new measurements: reproduce the published 6x25 class {2} krow=2:4 minpos=11 SAT value (K1217: 3,574,244 conflicts) bit-exactly. This control runs after this declaration commit and is recorded in the kit.

## Scope and non-claims

Witness existence only. No absence claim at any width. Any SAT result is dual-verified (sat.js verifyConfig + the fresh Python Fraction verifier published in the 6x22 kit) before any claim. Standard 11x11 empty board, two-stone roots, third move, S2, closure classes: UNKNOWN at all times; verdicts not consumed.
