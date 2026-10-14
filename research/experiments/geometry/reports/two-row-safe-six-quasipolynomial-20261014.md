# 2×m q=4: safe six-stone counts

For every m>=0, let e=m mod 2 and d=1 if 3 does not divide m, otherwise d=0. The number of safe six-stone subsets is

 a6(m)=(m^6-12m^5+55m^4-132m^3+199m^2-162m)/36 + e*(m^2-6m+8)/4 + 2*d/3.

This follows by counting disjoint pair-sum sets of two triples, using inclusion-exclusion over the 1, 2, and 3 common sums. The full proof and independent determinant audit are prepared separately; knowledge promotion requires regenerating indices.
