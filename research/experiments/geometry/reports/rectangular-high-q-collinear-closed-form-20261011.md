# High-q collinear tuples in rectangular integer grids (2026-10-11)

For d>=1, integers n_i>=1, and q>=2 with 2(q-1)>max(n_i)-1, let B be the product of intervals [0,n_i-1]. The exact number H_q of collinear q-subsets is

H_q = (1/2) sum_{k=q}^{max n_i} binom(k-2,q-2) [ prod_i(n_i+2 max(n_i-k+1,0)) - prod_i n_i ].

**Proof (unbounded).** Each q-subset has a unique primitive direction and two extremal endpoints separated by k-1 primitive steps, k>=q. The hypothesis forces every coordinate of the direction to belong to {-1,0,1}. A direction with nonzero support S admits prod_{i in S} max(n_i-k+1,0) prod_{i not in S} n_i ordered endpoint pairs. Each nonzero support has 2^{|S|-1} normalized sign choices. Summing all supports via distributivity gives half the product difference above. For fixed endpoints there are binom(k-2,q-2) ways to select the interior points. Each subset has unique endpoints, so the sum is exact.

For an n-by-...-by-n cube, the bracket is (3n-2k+2)^d-n^d. In particular H_n=((n+2)^d-n^d)/2 (n>=2), and H_3(3,d)=(5^d-3^d)/2.

Independent finite check: all 521 tested box/q conditions in dimensions 1..4 matched a separate enumerator that constructs maximal integer lines from point pairs. This is not a result about circles, hyperplanes, or game winners.
