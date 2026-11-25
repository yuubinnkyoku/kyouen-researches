# 2026-11-21 five-row q6/q5 m=23/m=27 sd<=6 frontier surgery — single-owner declaration

Declaration time: 2026-11-21T21:32Z (declaration-time main HEAD `bab006adc73935d143e9f7e603046beef6ded68c`).

## Scope (single owner, this lane only)

Two bounded-neighborhood complete final-state surgery campaigns around the
published five-row frontier witnesses, extending the published sd<=2 negatives
to the (<=3 addition, <=3 removal) class:

1. `(5,6)` target `5x23`, seed = the published 24-stone m=22 witness
   (five-row-q6-m22-witness-20261115, rows (4,5,5,5,5), K0852).
2. `(5,5)` target `5x27`, seed = the published 19-stone m=26 witness
   (five-row-q5-m26-extend-20261115, rows (3,4,4,4,4)).

Machinery: the published bounded-edit surgery machine `surgery4.js`
(four-row-q4-m35-surgery-20261115, md5 `7dc40fc0f08150692d64241d0c6c4029`)
with `sat.js` (md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`) and
`census4_check.js` (md5 `dadbeae1b02ad2a9650c6ce86021fb9c`), fetched from
main and md5-verified. Seeds are re-verified on their home boards before use.

Placement grid: for each seed, all four row-preserving images (id/H/V/HV of
the bounding box) x all bounding-box translations that fit the target board
(the finer bbox grid; subsumes the published window grids):
4x3 placements for 5x23 (span 21), 4x8 placements for 5x27 (span 20).
Budgets: maxP=3, maxRm=3, targetMax = full capacity minus 1
(24 for (5,6) q=6, since a 5x23 safe config holds at most 5 stones per row;
19 for (5,5) q=5), so every emitted maximal safe configuration is
automatically row-deficient.

## Acceptance conditions

1. Census completeness gates: `census4_check.js` all-triples == buildCensus4
   must PASS at (5,23,6) and (5,27,5) (plus small boards) before any surgery run.
2. Seed sanity: both published seeds re-verified on their home boards
   (sat.js verifyConfig + an independent Python exact-geometry verifier).
3. Positive control: self-completion (seed minus 2 stones, home board,
   budget (2,2)) must re-find the exact published witness among emitted
   finals, byte-comparable stone set.
4. Determinism: every published run reproduced twice, byte-identical output.
5. Exact class statement: the enumerated class is precisely
   {(A,R): |A|<=3, |R|<=3, R subset of stones on deficit curves of A,
   final size <= targetMax} (the published machine's design). Free-removal
   deposits outside deficit curves are out of scope by the machine's design
   and are NOT claimed absent; no global absence claim at 5x23/5x27 either way.
6. Any witness found at 5x23/5x27: three independent integer verification
   systems before any bound statement; M lower bound update published only
   with a verified witness. mwq_stabilization.csv unchanged otherwise
   (K1201/K1209/K1211 precedent).

## Non-goals

- No SAT/kissat, no 11x11 work, no class-split territory
  (`five-row-q6-m22-class-split` IN FLIGHT instances untouched).
- No work on (4,4) m=35/36 (K1208 collision territory), no (5,4) m>=41 or
  six-row q4 m52 work (declared by other lanes at 18:46Z/21:28Z).
- checked counts / leaf counts / seconds are not cited as win/loss verdicts.
