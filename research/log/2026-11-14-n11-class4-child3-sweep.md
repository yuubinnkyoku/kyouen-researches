[object Object],[object Object]

---

# 2026-11-14 n11 class4-batch3 child#4 sweep (session 19, continued)

Next cheapest remaining S6 child of the class-4 lane target after bit 37.

## Target

- S6 child `00000000020000003800000084000000` (cost 69, demand c1=0,c2=0,c4=3)
- 69 non-degenerate 7th-stone candidates, ordered by root mobility ascending.

## Sweep result

- **66 candidates REFUTED-D10, 3 candidates WIN7-D10 (bits 94/80/86), 0 capped.**
- bit 94: root `00000000420000003800000084000000`; bit 80: root
  `00000000020100003800000084000000`; bit 86: root
  `00000000024000003800000084000000`.
- Total 171,686,664 nodes over 69 candidates, 0 capped.
- bit 77 gave the first observed 11-stone terminal (stones [11,17]) in this
  batch; recorded as an experimental fact, no verdict implied.
- Controls: pilot d6=5,949 PASS; fresh re-solves of 6 candidates node-exact.

## WIN7 certificates (12th-14th verified overall)

| bit | rows | sub-roots PASS | union |
|-----|------|----------------|-------|
| 94  | 14,435 | 38/38 | exact (missing 0 / extra 0) |
| 80  | 19,922 | 47/47 | exact |
| 86  | 33,994 | 53/53 | exact |

All verified by the independent verifier (TS port of
verify_five_terminal_loss7.py, exact Bareiss, no engine import); root checks
PASS (7 stones, no 4-cocircular subset, loser mobility 49/47/53).

- Records: `output/class4-batch3-child4-sweep.json`,
  `output/class4-batch3-win7-certificates-20261114.json`.

## Frontier effect (local, exact)

bit 94/80/86 cover 3 more remaining children of the class-4 lane target:
costs 69, 72, 80.

**Class-4 lane target: remaining 30 -> 27 S6 orbits, cost 2385 -> 2234.**
(Combined with child#3: 32 -> 27 orbits, 2530 -> 2234 cost this session.)
Next cheapest remaining S6 child:
`00000000020000003800000080001000` (cost 72).

## Status

WIN7 certificates prove only a win within depth 10 from their 7-stone root;
REFUTED-D10 entries negate only WIN7-within-depth-10. class 4, S2 {59,60},
two-stone root {49,60}, and the 11x11 empty root remain **UNKNOWN**. The bit7
400-node aggregation discrepancy reserve remains open and unrelated.
