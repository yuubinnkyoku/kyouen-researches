# Binary 4-cube six-point affine-circuit pair codegrees (2026-11-07)

## Finite exhaustive result

For any distinct vertices x,y of {0,1}^4 at Hamming distance h, the number of six-element minimal affinely dependent sets containing both is:

| h | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| circuits per fixed pair | 100 | 154 | 154 | 100 |
| circuits containing 0 and any vertex of weight h | 400 | 924 | 616 | 100 |

There are exactly 408 such circuits through 0 and 1088 in total, agreeing with the previous d=4 six-circuit total. The check identity is 400+924+616+100 = 5*408 = 2040, and 16*408/6 = 1088.

## Two independent exhaustive checks

Enumerate all C(15,5)=3003 six-subsets containing 0. For each set, construct the 6-by-5 augmented coordinate matrix (constant 1 and four binary coordinates). It is a six-point affine circuit iff its rank is exactly 5 and every one of its six five-row deletions has rank 5.

First implementation: Gaussian elimination modulo 101, with rank calculated for each candidate and deletion. This is exact over Q: every nonzero maximal minor is an integer determinant of a 0,+1,-1 matrix of order at most 4 (subtract the first row), bounded by Hadamard by 4^2=16<101.

Second implementation: independently enumerate the same subsets and use SymPy Matrix.rank() over Q for the six-row matrix and all five-row deletions. Both yielded exactly 408 circuits through 0 and distance buckets [400,924,616,100].

Coordinate permutations act transitively on vertices at each Hamming distance from 0; coordinate reflections and permutations act transitively on all ordered pairs at the same distance. Divide each bucket by C(4,h) to obtain the per-pair figures.

## Scope and relevance

This is a **finite exhaustive d=4 result**, not a general d formula. Together with the already recorded d=5 six-circuit pair codegrees, it provides another independent regression target for the binary-cube affine-circuit generator used in the K6 investigation. It does not prove K6 <= 9 and does not enumerate the remaining full-support d=6 six-circuits.
