# PG(2,13) s=2 cone pre-assessment + arc census layers m<=7 (2026-11-27)

## What this is

Pre-assessment for a future PG(2,13) s=2 complete Grundy spectrum (next-step 3 of
K1363's log), plus exact new census values as a by-product.

## Method

Cone method (K1353/K1359/K1363 family): fix a non-collinear triangle F;
PGL(3,13) is transitive on triangles, so the cone (all arcs containing F)
represents every arc class uniformly. Canonical DFS over added points in
increasing index order enumerates each cone arc exactly once.

- T_m = #arcs of size m containing F (complete enumeration, m = 3..7).
- N_m = N_3 * T_m / C(m,3) by triple double counting.
- N_3 = C(183,3) - 183*C(14,3) = 938,119.

## Results (exact, complete enumeration of layers m<=7)

| m | T_m (cone) | N_m (all PG(2,13) m-arcs) |
|---:|---:|---:|
| 4 | 144 | 33,772,284 |
| 5 | 7,920 | 742,990,248 |
| 6 | 192,720 | 9,039,714,684 |
| 7 | 1,942,560 | 52,067,212,704 |

Layer growth: x55 (4->5), x24 (5->6), x10.08 (6->7), decelerating;
peak layer estimated at m~9-10 with >=10^7 states.

## Gates (fail-closed, all PASS, rc=0)

- G1 board axioms (v=183, 183 lines x 14 pts, pair->line unique).
- G2 T_4 = 183 - 3 - 3*12 = 144 (points off the triangle's 3 side lines).
- G3 divisibility N_3*T_m % C(m,3) == 0 for every m.
- G4 two different triangles give identical T_m tables.

## Pre-assessment verdict

Full cone (all sizes, up to 14) is estimated at 10^7-10^8 states with layers
>=10^7 around m=8-10: **pure-Python single-command (300s cap) infeasible**.
A full PG(2,13) s=2 spectrum needs a C/bitset port of the cone DP
(the q=11 cone was 708,761 states; q=13 is ~100x larger).

## Files

- scripts/q13_cone_layers.py (sha256 a0f8573d5e000f5c08bd3ed0cc14566dd557e2aad956cc33b56daa67130425f2)
- output/out_q13.json (sha256 dc1b79b95bef86463c746e4c28f278edff8928bde4fb0b09f060fd8d2aafa6fc)

Depends on the published board builder in
research/experiments/pg2q-s2-cone-spectrum-family-20261127/scripts/pg2q9_cone_spectrum.py.
11x11 root verdict: UNKNOWN (unchanged; this is an independent s=2 parameter-board computation).
