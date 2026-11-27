# pg2q9-s2-cone-spectrum-20261127 — single-owner declaration

PG(2,9) s=2 cap game: complete Grundy spectrum via the cone + double-counting
method (K1353/K1354 projective version). This lane claims the computation and
publication of the full distribution (all 128,917,712 arcs), Grundy(empty),
and the maximal-size class counts, as the fill-in for the "PG(2,9) s=2 complete
distribution not computed" gap in docs/FINITE_RING_STATUS.md.

- Disjoint from: K1354 lane (AG-side general q), the s=3 parity-table lane
  (K1355-K1358), all declared SAT/sweep lanes (6x26/6x23, three-row q4 m=28/29,
  ultra-cheap u02/u03/u04, five-row q7 band 35..157, (4,24,5) m24, seven-row w70).
- Method: fix one non-collinear triple F, enumerate the full cone (arcs
  containing F), mex DP inside the cone, then N_m(g) = N_3 * T_m(g) / C(m,3)
  by PGL(3,9) transitivity on non-collinear triples; same identity for the
  maximal classes.
- Pre-registered anchors (from published main): total arcs 128,917,712;
  N_3 = 110,565 all G=1; N_4 = 1,769,040 all G=0; N_5 = 14,859,936;
  complete 6/7/8/10-arcs 707,616 / 2,021,760 / 5,307,120 / 58,968;
  maximal sizes exactly {6,7,8,10}; calibration q=3/q=4 cone == naive full DP
  and q=4 == published PG(2,4) s=2 row.
- Verification: dual board construction, GF(9) distributivity sweep,
  three different cones (F-invariance), 3-run determinism, 300-position
  child/mex audit with a fresh safety predicate, tamper battery 5/5 fail-closed.
- Verdict status: this is the s-parameter cap game on PG(2,9); no 11x11 root
  verdict is consumed or transferred (11x11 UNKNOWN).
