# 2026-11-13 n11 S2 {59,60} milestone-5: full independent S6→S7 geometry recount

Evidence level: **full independent geometry cost audit** of the published milestone-5 S6 manifest; **not** an independent S6 worklist derivation, S5/S6 verdict, or WIN/LOSS certificate.

Baseline main at audit start: `015e0068eebd0103778622abab5166438a0c0abc`. Read `AGENTS.md`, `research/knowledge/README.md`, `K0023`, the milestone-5 experiment README and the earlier 213-row sample audit. Obtained all six `ms5_s6_manifest_part*.csv` files directly via the GitHub connector. Each file had header `hex,cost,classes`.

## Independently implemented check

A fresh JavaScript routine (not the milestone-5 TypeScript generator and not its precomputed circle masks) parsed each hex key as a 128-bit `BigInt`, extracted occupied indices 0..120, and independently counted legal seventh placements. Each candidate unoccupied cell was tested against all 20 triples of the six occupied cells using integer arithmetic only.

For occupied triple A,B,C and candidate P, define `d=B-A`, `e=C-A`, `f=P-A`, `cross=det(d,e)`, `q1=|B|²-|A|²`, `q2=|C|²-|A|²`, `qp=|P|²-|A|²`.

- If `cross=0`, reject P when `det(d,f)=0` (four collinear).
- Otherwise reject P when `(q1*e_y-q2*d_y)*f_x+(d_x*q2-e_x*q1)*f_y=qp*cross` (four concyclic).
- Count candidates not rejected by any triple.

This equality follows from subtracting the circle equation at A from the equations at B,C,P. Coordinates are `(index % 11, floor(index / 11))`. The largest arithmetic values here are safely within JavaScript exact integer range; no floating point or approximate tolerance was used.

## Result

- All **7,867/7,867** published six-stone keys have six occupied cells; unique keys **7,867**, duplicates **0**.
- Independently recomputed legal S7 move counts match the CSV cost column on **all 7,867 rows**, mismatches **0**.
- Published cost sum and independently recomputed cost sum are both **615,497**.
- The combined CSV order is nondecreasing by cost.

Input Git blob SHAs (part1..6, in order):

```text
6b30ad1b224ead35ffc999e1358e2451446adeeb
8aff65fa2942e7be2ee1adf08ffea6a21a4a02c3
203b0fbd071bfe5f4da8a6cd34fcf3a65670df23
1ec608cc12842bd4472a3039fcc0514494e1960c
e2aad9cef9f9a4af3bc659043631558408b6672b
acc1a8b3869a9917be7dd1b55574c756b59b0351
```

The prior 213-row deterministic sample has now been superseded for the **geometry cost column only** by this full recount. This does **not** establish that the 7,867 keys are the complete necessary S6 set, that their `classes` bits are correct, or that any game verdict is proved. In particular, 11×11 empty root and S2 {59,60} remain **UNKNOWN**.
