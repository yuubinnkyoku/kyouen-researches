# 2026-11-27 six-row q=7, 6x23 class {2} minpos-rest decomposition sweep: single-owner declaration (fast lane)

## Claim

Single-owner lane. No other lane is currently executing or has declared the
6x23 q=7 class {2} krow=2:5 minpos-rest sweep. HEAD at declaration time:
`9b4cdaaccb8e2ab2f19added518d59331801a57b` (machine-checked immediately
before this push).

## Target

The (6,7) unresolved frontier is 6x23 (M_{6,7} in [23, 402] after the 6x22
witness, kit `six-row-q7-m22-class-split-20261127`). The published extension
probes covered class {2}, krow=2:5, minpos 6/7/8 (all INDET at 262s caps).
This lane sweeps the remaining minpos values of the same sub-instance:

- probes: 6x23, class {2}, krow=2:5, minpos P in {0,1,2,3,4,5,9,10,11,12,13,14,15,16,17,18}
  (minpos <= 18 is the range bound for k=5 stones in a 23-wide row;
  6/7/8 already INDET in the m22 kit, not repeated)
- machinery: byte-verified clones of the published m22 kit scripts
  (sat3.js `e04581eb...`, sat2.js `14ceb854...`, sat.js `fcc0cfd8...`),
  kissat 4.0.4 official linux-amd64 binary sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`
  (re-downloaded and sha-verified this session).
- cap policy: 262s wall cap per probe, one kissat invocation per command
  (m22 kit convention). CNFs regenerated, not published (size policy).

## Pre-registered interpretation

- Positive control: 6x20 class {2} must reproduce SAT at 641,859 conflicts
  bit-exact (published value). Calibration runs before the declared probes.
- SAT in any probe => a 6x23 deficient maximal witness exists in class {2}:
  decode, dual-verify (sat.js verifyConfig + fresh Fraction verifier
  byte-clone of the m22 kit `verify_frac.py`), negative controls
  (remove -> non-maximal, add -> rejected), then M_{6,7} >= 24 and the
  (6,7) range becomes [24, 402]; frontier moves to 6x24.
- All INDET => honest negative at these caps, NOT absence; frontier stays
  6x23; M_{6,7} in [23, 402] unchanged.
- Verdicts not consumed; standard 11x11 empty board, roots, closure classes
  UNKNOWN at all times; conflict counts are bookkeeping.
- publish-then-execute: all official probe raw logs will be generated after
  this declaration commit lands on main.
