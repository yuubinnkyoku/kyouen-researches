# 2026-11-27 Six-row q=6, 6x26: class {2} krow=2:4 minpos-REST sweep — declaration

## Status

Single-owner declaration (publish-then-execute). Declaration-time HEAD
`1fcf7fee71bd706dd08794e1a4ad92507937ad61` (main, 2026-11-27T13:36:24Z).
No other lane has declared (6,6) 6x26 SAT-side work: the first minpos batch
(P = 10..13) closed at `c4d2e9dbb0`/`200158dc` (all INDET honest negatives);
the parallel (6,7) 6x23 minpos-rest sweep `f43cd66b` and the n11 tenth-cost
selection `238901e9` are disjoint lanes and are not touched.

## Target

6x26 q=6, **class {2}, krow=2:4**, `--minpos=P` for the remaining
**P in {0..9, 14..22}** (19 disjoint sub-instances completing the
P = 0..22 split; P = 10..13 are already published INDET). Same disjoint
exhaustive split convention as the declared 6x26 sweep `02e40e9e` and the
resolved 6x22 q=7 precedent `d35234a7`.

Decoding conventions: SAT in any deciding sub-instance => a 6x26
deficient-maximal witness exists => **M_{6,6} >= 27** (range 27..495).
All sub-instances UNSAT => class {2} k=4 witness-free at 6x26 (partial
absence). INDET at cap => honest negative, not absence.

## Engine and calibration plan

- Byte-cloned machinery from the published 6x26 kit
`research/experiments/six-row-q6-m26-class-split-20261127/`
(sat.js/sat2.js/sat3.js sha-verified against its MANIFEST; meta json of
P=10 to be reproduced first as encoder determinism control), kissat 4.0.4
official linux-amd64, binary sha256
`21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`
(verified byte-exact before this declaration).
- Per-probe cap 272 s (SIGTERM), one kissat invocation per probe,
  raw kissat log + meta json per sub-instance; two-core host, at most
  two concurrent invocations (separate processes, no shared state).
- Positive control before the new measurements: reproduce the published
  6x25 class {2} krow=2:4 minpos=11 SAT value (K1217: 3,574,244 conflicts)
  bit-exactly. This control runs after this declaration commit and is
  recorded in the kit.

## Scope and non-claims

Witness existence only. No absence claim at any width. Any SAT result is
dual-verified (sat3.js decode + verifyConfig, and the published fresh
Python Fraction verifier) before any claim. Standard 11x11 empty board,
two-stone roots, third move, S2, closure classes: UNKNOWN at all times;
verdicts not consumed; conflict counts are bookkeeping.
