# Four forbidden sets: terminal spectra and sharp integer-plane witnesses (2026-11-01)

A safe set avoids containing any of the four forbidden sets E1,...,E4. Its complement is an inclusion-minimal hitting set exactly when the safe set is maximal. The theorems below concern **exactly four forbidden subsets**, not four curves that generate additional forbidden subsets.

## Theorem 1 (complete four-edge criterion with private points)

Assume each E_i has a private point, belonging to E_i and to no other E_j. Write I(x)={i:x in E_i} and d(x)=|I(x)|. Let T be the set of cardinalities of inclusion-minimal hitting sets. Then 4 belongs to T, and:

- 1 belongs to T iff some x has d(x)=4.
- 2 belongs to T iff some x has d(x)=3, **or** two degree-2 points have complementary incidence sets.
- 3 belongs to T iff some x has d(x)=2.

No other sizes occur. The terminal safe-set lengths are exactly {N-t:t in T}, where N is the number of board points (including points on no edge).

**Proof.** Choose a private point p_i from each E_i. The set of all four p_i is a minimal hitting set. If x belongs to exactly d>=1 edges, then {x} together with p_i for each edge not containing x is a minimal hitting set of size 5-d. This proves the direct implications.

Conversely, a one-point transversal must hit all four edges. A minimal two-point transversal either has a point of degree at least three, or consists of two complementary degree-2 points; a degree-4 point alone cannot be part of a minimal pair. In a minimal three-point transversal, each point must have its own witness edge not hit by either other point. A degree-3 or degree-4 point would leave at most one edge outside its incidence set, so the other two points could not both have distinct witnesses. Thus all three points have degree at most two; at least one has degree two because three degree-one points cannot cover four edges. Finally, any minimal transversal has at most four points because its points need distinct witness edges. QED.

## Corollary 2 (two gapped spectra)

The spectrum T={1,4} occurs **iff** some degree-4 point exists and no degree-2 or degree-3 point exists. The terminal lengths are N-4 and N-1, with two missing lengths.

The spectrum T={2,4} occurs **iff** some degree-3 point exists and no degree-2 or degree-4 point exists. The terminal lengths are N-4 and N-2, with one missing length.

Points outside all four forbidden sets are allowed and do not affect the transversal-size spectrum.

## Theorem 3 (sharp integer-plane q-point minimum)

For every q>=4, among finite sets of integer planar points whose **entire family** of forbidden q-point subsets (collinear or cocircular) consists of exactly four distinct subsets, the minimum N realizing the respective spectra is

    T={1,4}: N_min=4q-6,
    T={2,4}: N_min=4q-8.

Both bounds are attained for every q>=4. Their extremal maximal-safe polynomials are

    T={1,4}: (q-2)^4 u^(4q-10) + 2u^(4q-7),
    T={2,4}: (q-3)^4 u^(4q-12) + (4q-6)u^(4q-10).

**Lower bounds.** A curve with q+1 selected points generates at least q+1>=5 forbidden q-subsets, so the four distinct forbidden subsets lie on distinct lines/circles. Any two such curves meet in at most two points.

For T={1,4}, all points on forbidden edges are either common to all four edges or private. If c<=2 is the common-point count, then N>=c+4(q-c)=4q-3c>=4q-6.

For T={2,4}, all points on forbidden edges have degree one or three. If t is the number of degree-three points and p the number of degree-one points, 4q=p+3t. Each degree-three point contributes three to the sum of the six pairwise edge intersections, each at most two, so 3t<=12 and t<=4. Hence N>=p+t=4q-2t>=4q-8.

**Constructions and infinite-q proof.** For T={1,4}, take four distinct rational circles through two common rational points, then select q-2 additional rational points on each circle. For T={2,4}, take four rational points in general position, not all cocircular, and their four distinct circumcircles through the respective triples. Select q-3 additional rational points on each circle. Each of the four base points belongs to exactly three of the circles. Each rational circle has infinitely many rational points (parametrize using a rational point). At each selection step, the finitely many unwanted lines through two previous points and unwanted circles through three previous points exclude at most two points apiece on the current circle; circles coinciding with the intended circle impose no unwanted condition. Thus one can avoid all unintended collinear or cocircular quadruples and intersections with other intended circles. Scaling by a common denominator gives integer points, preserving incidences. The intended circles contain exactly q selected points, so there are precisely four forbidden q-subsets.

For T={1,4}, minimal hitting sets are either one common point (two choices), or one private point from each edge ((q-2)^4 choices). For T={2,4}, size-four minimal hitting sets choose one private point from each edge ((q-3)^4 choices); size-two minimal hitting sets choose two of the four triple points (six choices), or one triple point plus one private point on its missing edge (4(q-3) choices). Taking complements proves both polynomials. QED.

## Explicit q=4 integer witnesses, both inside the 11x11 grid

The 10-point T={1,4} witness, in index order:

    [(2,5),(8,5),(5,2),(5,8),(0,10),(10,10),
     (4,7),(8,3),(0,9),(1,6)]

Its only forbidden quadruples are (0,1,2,3), (0,1,4,5), (0,1,6,7), (0,1,8,9). It has 849 safe subsets, maximal-safe polynomial 16u^6+2u^9, and empty-board (normal Grundy, misere auxiliary mex)=(2,2).

The 8-point T={2,4} witness, in index order:

    [(4,3),(5,6),(10,9),(10,6),(9,10),(1,6),(4,4),(4,2)]

Its only forbidden quadruples are (0,1,2,7), (0,1,3,6), (0,2,3,5), (1,2,3,4). It has 209 safe subsets, maximal-safe polynomial u^4+10u^6, and empty-board (normal Grundy, misere auxiliary mex)=(0,1).

The verifier checks all 210 and 70 quadruples by exact integer lifted determinants, enumerates all safe subsets and recursively computes both mex values. It also independently enumerates all 2048 incidence-support families with four private singleton types and checks the criterion (including 1 and 15 supports with spectra {1,4} and {2,4}); extremal counting formulas are checked for q=4,5,6. These are **finite checks**, whereas the unrestricted q claims follow from the mathematical arguments above.

Neither selected-point witness determines the full standard 11x11 board winner. In a residual position with exactly four forbidden sets and private points in each, Theorem 1 gives terminal lengths directly from incidence degrees and complementary degree-two masks.
