# 2026-11-27 Six-row q=6, 6x26: multi-deficiency two-deficient-row classes k=4:4 — declaration

## Status

Single-owner declaration (publish-then-execute). Declaration-time HEAD
`07937d74` (main, 2026-11-27T17:54:15Z), re-fetched immediately before this
push. No measurement of the targets below has been run in this session
before this declaration; the only pre-declaration work is machinery
verification (disclosed below).

## Non-intersection with parallel lanes (checked at declaration time)

- class {0} krow=0:4 minpos 0..11 (declaration `a9dde1d3`, completed
  all-INDET kit `94103471`), class {1} krow=1:4 (declaration `f9a982d2`),
  class {2} krow=2:4 minpos-REST (declaration `e61acf82`), class {2}
  deep-deficiency k<=3 (declaration `bba3d32c` lane) — all SINGLE-deficient
  row classes; this lane's TWO-deficient-row classes are disjoint
  (the class {1} declaration explicitly lists "multi-class" as 対象外).
- (6,7) lanes: 6x23 class {2} minpos-REST sweep (declaration `50bb4468`),
  6x23 surgery3, 6x22 lanes — different q and width, disjoint.
- seven-row q4 w69/w70, kit-20 strip m55/m56, REMO cap16, four-row m24,
  W_24 dodecad, PG(2,9), n11 cost lanes — disjoint.
- 6x27 is NOT claimed by this lane.

## Target

6x26 q=6, **two-deficient-row classes** D = {a,b} (both rows pinned to
exactly 4 stones via krow a:4,b:4; all other rows forced FULL at exactly
q-1 = 5 stones; 28 stones total), split soundly by the minpos (leftmost
stone position P of row a = D[0]) H-split P = 0..11.

Canonical classes under V (row i -> 5-i; H preserves rows), all 15 pairs
covered by 9 canonical representatives, swept in this priority order:

1. {0,5} (also covers {0,5} self-mirror)
2. {0,1} (covers {4,5})
3. {1,4} (self-mirror)
4. {0,4} (covers {1,5})
5. {1,3} (covers {2,4})
6. {2,3} (self-mirror)
7. {0,3} (covers {2,5})
8. {1,2} (covers {3,4})
9. {0,2} (covers {3,5})

Soundness of the split: row a has exactly 4 stones, so
min(x1, 25-x4) <= 11 (if x1 >= 12 then x4 >= x1+3 >= 15, 25-x4 <= 10);
H (column reflection) preserves rows and the class D, so every witness
(or its H-image) falls in exactly the swept range P=0..11. Splitting by
row a only (row b left free) is a complete enumeration of the class.
Same convention as the published m26 kits (`sat3.js --class=a,b
--krow=a:4,b:4 --minpos=P`, lex=[] as in all published m26 probes).

12 probes per class, 108 sub-instances total for the full k=4:4 layer.
This session sweeps the priority order above under the session budget;
every swept sub-instance is published with its raw log; unswept
sub-instances remain bookkeeping-open and are NOT absence claims.

## Decoding convention

SAT in any deciding sub-instance => a 6x26 two-deficient-row
(k=4:4, 28-stone) deficient-maximal witness exists => **M_{6,6} >= 27**
(range update [27, 495]); witness decoded and dual-verified
(sat3.js decode/verifyConfig + verify_frac.py independent Fraction
verifier) plus negative controls (remove one stone -> non-maximal, add
one stone -> rejected) and a cold-pair rerun before any claim.
All swept sub-instances UNSAT => this k=4:4 layer is witness-free in the
swept classes at 6x26 (partial absence, no width-level absence claim).
INDET at cap => honest negative, not absence.

## Engine and calibration

- `sat3.js`/`sat2.js`/`sat.js`/`verify_frac.py`: byte-clones of the
  published m26 class-split kit, sha256-verified before this
  declaration: `e04581eb`/`14ceb854`/`fcc0cfd8`/`837fe24b`.
- Encoder calibration (disclosed, pre-declaration, no target touched):
  regenerated 6x26 class {0} krow=0:4 minpos=0 CNF meta
  vars 58,722 / clauses 205,663 == published
  `meta_6x26q6_c0k4p0.json` bit-exact.
- kissat 4.0.4 official linux-amd64, binary sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`,
  unpacked from the official rel-4.0.4 asset zip sha256
  `63282e51…` (both sha-verified before this declaration).
- Positive control (acceptance, run AFTER this declaration): 6x25 q=6
  class {2} krow=2:4 minpos=11 must reproduce the published K1217 value
  **SAT 3,574,244 conflicts bit-exact**.
- Per-probe cap 272 s (SIGTERM), one kissat invocation per probe, one
  probe per shell call (environment-reset avoidance), raw kissat log +
  encoder meta json per sub-instance, CNFs regenerable and not
  published (size policy).

## Bookkeeping

11x11 empty board, all 19 central-reply roots, two-stone root {60,27},
third move {100,108}, S2, all closure classes: UNKNOWN at all times;
no verdict consumed by this lane; conflicts/nodes are bookkeeping.
