# genff.js verification record (2026-11-14)

`genff.js` replaces genfast.js's per-point-pair circle census (O((2m)·n²), minutes at
m in the hundreds) with a **same-row-pair-pair enumeration**: a circle with q ≥ w+2
grid points has ≥ 2 same-row pairs; a same-row pair on a circle with center x u = U/2
is (row y, offset e) with points (U±e)/2, e ≡ U (mod 2); two pairs (y1,e1),(y2,e2)
determine the circle exactly:

    v = [4(y1²−y2²) + e1²−e2²] / [8(y1−y2)]

Candidates are pre-filtered in pure integer arithmetic (≥ EXTRA_ROWS_MIN =
min(3, w−2, ⌈(q−4)/2⌉) further rows carrying an in-grid point; no false negatives
since a true q-point circle has q−4 points outside the two pair rows, i.e. ≥
⌈(q−4)/2⌉ occupied further rows), then get the exact genfast-identical point-set
scan. **Correctness subtlety (found by the (6,20,8) control): for fixed rows y1 < y2
the offset pairs must be ORDERED** — (e1,e2) and (e2,e1) give different circles
(v is asymmetric in the assignment); an unordered {e1,e2} loop silently misses
circles (25 missing at (6,20,8)). i2 == i1 (equal offsets, cyclic rectangles) is
required and included. Lines for q > w are exactly the w horizontal rows (a
non-horizontal line meets each row in ≤ 1 point), built with the same lineABC /
onLine-scan / sort calls, byte-identical.

## CNF byte-identity (cmp, this session, node v22)

| sample | args | vs | bytes |
|---|---|---|---|
| (7,19,10) | --deficient | sat2.js | 130786 |
| (7,19,10) | --deficient --lex=H,V,HV | sat2.js | 167994 |
| (7,25,9) | --deficient | sat2.js | 188040 |
| (7,30,9) | --rowY=3 | sat2.js | 240742 |
| (7,30,9) | --cap=20 --counter=tot | sat2.js | 425302 |
| (7,34,9) | --deficient --lex=HV | sat2.js | 307347 |
| (6,20,8) | --deficient | sat2.js | 496408 |
| (7,40,10) | --deficient | sat2.js | 362447 |
| (7,45,9) | --deficient | genfast.js | 398044 |
| (7,52,10) | --deficient | genfast.js | 494685 |
| (7,100,9) | --deficient | genfast.js | 1027706 |
| (7,100,10) | --deficient | genfast.js | 1083420 |

All 12 `cmp`-identical (fail=0). The (6,20,8) row is the control that FAILS with an
unordered offset loop — it is what pinned the ordering requirement.

## kissat bit-exactness

kissat 4.0.4 (official binary, default mode) on genff's (7,100,10) def CNF:
**UNSAT, conflicts = 2388** — identical to the genfast-generated record already in
`output/q10-band/records.jsonl` (m=100 row), confirming verdict/conflict transfer.

## Speed (this container, node v22)

- (7,150,10): genfast ~69 s → genff **0.74 s**; (7,200,10): genff **1.5 s**.
- Estimated (7,586,10) ≈ 30–40 s, (7,612,9) similar (measured during the band run).

## Scope

Asserts q ≥ w+2, w ≤ 7 (covers the (7,9)/(7,10) and (6,8) bands). For q = w+1 or
w > 7 use genfast.js / sat2.js. Downstream encoding (counters, deficient clause,
lex-leader, DIMACS) is reused verbatim from sat2.js by the same monkey-patch as
genfast.js.
