# 2026-11-27 Six-row q=6, 6x26: deep-deficiency families krow=2:{3,2,1,0} minpos full-split — declaration

## Status

Single-owner declaration (publish-then-execute). Declaration-time HEAD
`bba3d32c15a1f0e4c21cd8b53a7f0ecfc6d47b7f` (main, 2026-11-27T15:07:08Z),
re-fetched immediately before this push. No measurement of the targets below
has been run in this session before this declaration; the only pre-declaration
work is machinery verification (disclosed below).

## Non-intersection with parallel lanes (checked at declaration time)

- class {2} krow=2:4 minpos 10..13 INDET (kit `c4d2e9dbb0`) and minpos-REST
  P∈{0..9,14..22} (declaration `e61acf82`) — same class, DIFFERENT krow
  (k=4 exactly); k≤3 is disjoint and explicitly listed by those lanes as
  "残る未掃引 (本宣言対象外)" / "unswept".
- class {0} krow=0:4 (declaration `a9dde1d3`) and class {1} krow=1:4
  (declaration `f9a982d2`) — different deficient row, k=4.
- (6,7) 6x23 lanes (`f43cd66b`/`a8075223`), REMO cap16 (`7a100862`),
  four-row m24 (`855f52d8`), W_24 dodecad (`05b3aa52`), n11 cost lanes —
  disjoint. None of them touches 6x26 deep-deficiency rows.

## Target

6x26 q=6, **class {2} (single deficient row 2), deep-deficiency stone
counts krow=2:3, then 2:2, 2:1, 2:0**, each with the sound H-split minpos
full enumeration of the row-2 leftmost stone position P:

- k=3: P = 0..11 (12 sub-instances). Sound: if x1 ≥ 12 then
  x3 ≥ x1+2 ≥ 14 so 25−x3 ≤ 11, hence min(x1, 25−x3) ≤ 11 for every
  3-subset; H (column reflection, preserves rows and class) maps any
  position with min > 11 into the swept range.
- k=2: P = 0..12 (13). If x1 ≥ 13 then x2 ≥ 14 so 25−x2 ≤ 11 ≤ 12.
- k=1: P = 0..12 (13). min(x, 25−x) ≤ 12.
- k=0: one sub-instance (no minpos split).

39 disjoint sub-instances total. All other rows are forced FULL
(exactly q−1 = 5 stones) by the class encoding; row 2 is pinned to
exactly k stones by the krow chain pins (sat3.js byte-clone of the
published m26 kit).

Decoding conventions: SAT in any deciding sub-instance => a 6x26
deficient-maximal witness with a row of ≤3 stones exists =>
**M_{6,6} ≥ 27** (range update 27..495); witness decoded and dual-verified
(sat.js verifyConfig + verify_frac.py independent Fraction verifier)
before any claim. All sub-instances UNSAT => class {2} deep-deficiency
(k ≤ 3) witness-free at 6x26 (partial absence, no width-level absence
claim). INDET at cap => honest negative, not absence.

## Engine and calibration

- `sat3.js`/`sat2.js`/`sat.js`/`verify_frac.py`: byte-clones of the
  published m26 class-split kit (sha256 `e04581eb…`/`14ceb854…`/
  `fcc0cfd8…`/`837fe24b…`, sha-verified before this declaration).
- kissat 4.0.4 official linux-amd64, binary sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`,
  unpacked from the official release asset zip sha256 `63282e51…`
  (sha-verified before this declaration).
- Per-probe cap 272 s (SIGTERM), one kissat invocation per probe,
  raw kissat log + encoder meta json per sub-instance; at most two
  concurrent invocations (separate processes, no shared state).
- Positive control BEFORE the new measurements (after this declaration
  commit, recorded in the kit): reproduce the published 6x25 q=6
  class {2} krow=2:4 minpos=11 SAT value (K1217: 3,574,244 conflicts)
  bit-exactly. An encoder-determinism control (meta json vars/clauses)
  for one deep-deficiency instance is also recorded before the sweep.

## Scope and non-claims

Witness existence only. No absence claim at any width (partial absence
per sub-instance only). (6,q≠6), w-row families other than class {2},
Grundy, and the standard 11x11 empty board / two-stone roots / third
move / S2 / closure classes are untouched: UNKNOWN at all times,
verdicts not consumed; conflict counts are bookkeeping.
