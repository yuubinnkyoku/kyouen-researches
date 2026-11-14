# 2026-11-14 class4-lane cost-80b frontier recompute: solved 875 -> 878, class-4 target 19 -> 18 orbit

`recompute_frontier_cost80b.py` (direct extension of recompute_frontier_cost78b.py)
recomputes the full manifest-level class-2/4 frontier over ALL published WIN7
receipts on main. Every published staged control is reproduced with asserts
before the new addition is measured:

- baseline 638 / 7208 / 565500 through after-cost63d 855 / 6992 / 549862 /
  5232 / 411408, then after-cost78b **875 / 6972 / 548362 / 5212 / 409908**:
  all reproduced exactly.
- sterile sweeps confirmed receipt-free by assert: cost-79, cost-79b, and
  this session's cost-80 child 1 (80/80 REFUTED-D10).

cost-80b addition (1 WIN7 root, bit 50, root 00000000020000003804040080000000):
**7 covers / 6 marginal / 3 in-manifest** (marginal manifest hexes:
00000000000000003801000400800000, 00000000000040403800000080000000,
00000000020000003800040080000000 - the swept child's own orbit is now solved).

**Frontier after cost-80b: solved_s6_in_manifest 878 - unique_remaining_s6 6969 -
sum_remaining_cost 548122 - open 5209 s6 / 409668 cost.**
Best class-4 blocker-candidate S5 `00000000020000003800000080000000`:
**19 -> 18 orbit, cost 1540 -> 1460**. Best class-2 unchanged (23 / 1601,
S5 `00000000000000809082000000000000`). Best class-4 next unswept child per
after-cost80b top-candidates CSV: cost-80 band child 3
`00000000020000003800200080000000` (c4=1), then cost-81
`00000000020000003800000080008000` (c4=3).

Artifacts: recompute script, frontier JSON (18ab4d57e0857f8294570995436d26ca),
ranking CSV (b533d5057866a39726340dec822313df), top-candidates CSV
(6acae367926d84374f8d0f4d448e4564). Two consecutive runs byte-identical.

## Guard

Bookkeeping over published receipts only. WIN7 certificates prove a winner win
within depth 10 from the individual 7-stone root; REFUTED-D10 sweeps prove only
the absence of such a win. No statement about the S5/S6 orbits beyond the
solved-set bookkeeping, the two-stone root {49,60}, S2 {59,60}, or the 11x11
empty board. **11x11 remains UNKNOWN.**
