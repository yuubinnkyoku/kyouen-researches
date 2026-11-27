# 2026-11-27 Six-row q=7, 6x22: SAT-side class {2} krow/minpos decomposition sweep — declaration

## Status

Single-owner declaration (publish-then-execute). Declaration-time HEAD `a4ea02e4f2f370d96c690acfe9462d27f9c7b88` (main, 2026-11-27T10:31:23Z). No other lane has declared 6x22 SAT-side work (the six-row q7 6x22 two-edit surgery lane closed at `a48a7d77` and listed this SAT-side decomposition as its next candidate; the (8,10) 8x26 lane `17ddb2d5` and the (4,5) m=24 sweep lane are disjoint).

## Target

The (6,7) unresolved frontier width **6x22**. Published status: class {2} plain kissat 280s INDET at 5,038,264 conflicts (`six-row-q7-m21-class-split-20261114`); the other 34 canonical deficiency classes unswept; the complete two-edit surgery around the m=21 K0815 witness is NEGATIVE (kit `six-row-q7-m22-two-edit-surgery-20261127`).

Plan: krow/minpos decomposition of **class {2}** on 6x22 (q=7) with the published class-split machinery:

- `--class=2 --krow=2:5` (single-deficiency, 35 stones) with `--minpos=P` for P = 0..17 (disjoint exhaustive split of the leftmost-stone position of the deficient row; sound split, no symmetry assumption), prioritized around the m=21 family geometry (m=21 witness row-2 leftmost stone at x=7).
- If time permits: krow 2:4 and 2:3 sub-instances, and first plain probes of unswept classes.

Decoding conventions (K0821-audit): SAT in any deciding sub-instance => a 6x22 deficient-maximal witness exists => **M_{6,7} >= 23** (frontier advance, range becomes 23..402). All sub-instances UNSAT => class {2} is witness-free at 6x22 (first decided class at this width; partial absence only, other classes open). INDET at cap => honest negative, not absence.

## Engine and calibration (disclosed preliminary work)

- Scripts byte-cloned from the published kit `research/experiments/six-row-q7-m21-class-split-20261114/scripts/` (sat3.js on sat2.js/sat.js K0810 core), fetched from main.
- kissat 4.0.4 official linux-amd64 release binary, sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`.
- **Prelinary calibration run before this declaration (disclosed)**: 6x20 q=7 class {2} positive control reproduced the published value bit-exactly — SAT, 641,859 conflicts (`six-row-q7-m21-class-split-20261114` reports 641,859 / 29.1s). All NEW measurements (6x22 sub-instances) run after this declaration commit.

## Scope and non-claims

- Witness existence search only. Any SAT result is a witness existence claim at 6x22 (=> M_{6,7} >= 23); UNSAT/INDET are local absence/negative records only. No claim about M_{6,7} exact value; upper bound 402 unchanged.
- Determinism: kissat conflict counts from completed runs; SAT decodes dual-verified (sat.js verifyConfig census-free + independent Python Fraction verifier) before any claim.
- Standard 11x11 empty board, two-stone roots, third move, S2, closure classes: UNKNOWN at all times; verdicts not consumed.
