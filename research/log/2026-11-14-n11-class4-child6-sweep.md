# 2026-11-14 n11 class4-batch3 child#6 sweep (session 19, continued)

Next cheapest remaining S6 child of the class-4 lane target after child#5.

## Target

- S6 child `000000000200000038000000c0000000` (cost 73)
- 73 non-degenerate 7th-stone candidates, ordered by root mobility ascending.

## Sweep result (v15 engine verbatim, native Node)

- **73 candidates REFUTED-D10, 0 WIN7-D10, 0 capped.**
- Total 214,167,492 nodes over 73 candidates in 3 foreground executions
  (cap 50M/candidate never reached).
- Pilot control PASS: lossAt(6)=false at exactly 5,949 nodes.
- Determinism controls: fresh re-solves of bits {29,74,112,33} node-exact;
  terminal stone range [13,17] on every candidate.

## Interpretation

No 7-stone root extending this S6 child admits a WIN7 within depth 10. This
child is **WIN7-D10-sterile**: it cannot be closed by a batch3-style
certificate rooted inside it. It remains coverable only via a WIN7 certificate
rooted in a different S6 parent sharing an S7 orbit (i.e. some other S6 child
whose candidate WIN7 root has this child among its drop-one parents), or by
deeper analysis.

This is the first fully-sterile swept child of the class-4 lane target in
batch3 (children swept so far: #3 cost 68 -> 1 WIN7, #4 cost 69 -> 3 WIN7,
#5 cost 72 -> 4 WIN7, #6 cost 73 -> 0 WIN7).

- Record: `output/class4-batch3-child6-sweep.json`.

## Status

REFUTED-D10 entries negate only WIN7-within-depth-10. class 4, S2 {59,60},
two-stone root {49,60}, and the 11x11 empty root remain **UNKNOWN**. The bit7
400-node aggregation discrepancy reserve remains open and unrelated.
