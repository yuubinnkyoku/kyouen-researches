# Six-row q=7, 6x23 class {2} minpos sweep: single-owner declaration (2026-11-28 fast lane)

Declaration-time HEAD: `f6d29d167ee2f35ee97ce8d86c19eb06841aae83`.

## Claimed scope (single owner)

The (6,7) frontier width 6x23, sub-instance class {2}, krow=2:5, minpos
P = 0..5 and 9..18 (15 instances; P = 6/7/8 were published INDET in
`six-row-q7-m22-class-split-20261127`). All runs with the pinned kissat
4.0.4 linux-amd64 binary (sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`),
262 s SIGTERM cap per run, `sat3.js`/`sat2.js`/`sat.js` byte-clones of the
published m22 kit.

V-mirror: class {2} covers class {3} (6-row V mirror maps row 2 <-> 3),
so no other lane needs to sweep class {3} at this width.

## Method

- Encode: `node sat3.js 6 23 7 --class=2 --krow=2:5 --minpos=P <out>.cnf`.
- Solve: `timeout 262 kissat <out>.cnf` (full stdout captured as raw).
- SAT -> decode + dual verification (sat.js verifyConfig + fresh Python
  Fraction verifier `verify_frac.py`); if a witness exists at 6x23 then
  M_{6,7} >= 24 and the frontier moves to 6x24.
- INDET -> honest negative, no absence claim.

## Pre-declaration calibration (disclosed)

6x20 q=7 class {2} krow=2:5 positive control: SAT (consistent with the
published 641,859-conflict control in the m22 kit; this host's run with
`-q` produced a SAT model immediately).

## Non-claims

No absence claim at any width. Standard 11x11 empty board, 19
central-reply roots, two-stone root {60,27}, third move {100,108}, S2,
all closure classes: UNKNOWN at all times; verdicts not consumed;
conflicts/nodes are bookkeeping.
