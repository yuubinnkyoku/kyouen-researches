# Maximum terminal-length gaps for any number of forbidden sets (2026-11-01)

## Theorem A: abstract characterization

Let V be a finite board and let E_1,...,E_r be exactly r distinct nonempty forbidden subsets, r>=3. A legal set contains no E_i. Put N=|V|. Its terminal (inclusion-maximal legal) sets are complements of inclusion-minimal transversals of the E_i. The number of missing *integer* terminal lengths strictly between the shortest and longest possible terminal lengths is at most r-2.

Equality holds **if and only if** the forbidden subsets form a nontrivial sunflower: there is a nonempty core C and pairwise disjoint nonempty petals P_i such that E_i=C disjoint_union P_i, and no board point has any other positive incidence type. Points outside all E_i are permitted. In this case the complete terminal spectrum is {N-r,N-1}, with r-2 missing lengths, and the maximal-safe polynomial is

    |C| u^(N-1) + (product_i |P_i|) u^(N-r).

**Proof.** A transversal meets each E_i. For any inclusion-minimal transversal T, every x in T has a witness edge E_i with E_i intersect T = {x}. Distinct x need distinct witness edges, so |T|<=r. All transversals are nonempty. Therefore terminal lengths lie in [N-r,N-1], containing at most r-2 missing integers between the attained extremes.

If the maximum number r-2 is missing, the only terminal lengths are N-r and N-1. The one-point minimal transversal supplies a point c belonging to every E_i. Let T be a minimal transversal of size r. Its r distinct witness edges exhaust all E_i. Every edge meets T in exactly one point, and each point of T belongs to exactly one edge (otherwise another edge would meet T in two points). Hence every E_i has a private point p_i.

Suppose another point x has incidence degree d with 2<=d<=r-1. Then {x} together with the private p_i for the r-d edges not containing x is a minimal transversal of size r-d+1, strictly between 1 and r. Contradiction. Thus every point is outside all edges, belongs to exactly one edge, or belongs to all r edges. The latter constitute a nonempty core, the former private petals. Conversely, in such a sunflower every minimal transversal is either a singleton from the core or a set choosing exactly one point from each petal. This proves the spectrum and counting polynomial. QED.

## Theorem B: sharp integer-plane realization for every r and q

For integers r>=3, q>=4, consider finite integer point sets whose **complete** family of collinear-or-cocircular forbidden q-subsets consists of exactly r distinct subsets. If the terminal spectrum has the maximum r-2 missing lengths, the number of board points satisfies

    N >= r(q-2)+2.

Equality is attained for every r,q. At equality the maximal-safe polynomial is

    (q-2)^r u^(r(q-3)+2) + 2 u^(r(q-2)+1).

**Proof of lower bound.** Theorem A gives private points for all r forbidden q-subsets. If any line or circle carried at least q+1 selected points, its q+1 distinct q-subsets obtained by deleting one point would all be forbidden; none of these q-subsets has a private point relative to the complete forbidden family. Contradiction. Thus every forbidden subset has its own unique carrier line or circle, each with exactly q selected points. Distinct carriers meet in at most two planar points. Theorem A says all pairwise intersections among the forbidden subsets are precisely their common core C, so 1<=c=|C|<=2. Their union has c+r(q-c) points, giving N>=c+r(q-c)>=2+r(q-2). QED.

**Construction.** Take P=(0,0), Q=(1,0) and r distinct rational circles with centers (1/2,t_i), for distinct nonzero rational t_i. All contain P,Q and any two intersect exactly at P,Q. Each circle has infinitely many rational points, since it contains P and Q. Choose q-2 further rational points per circle, successively avoiding all other intended circles and all unintended lines through two already selected points and unintended circles through three noncollinear already selected points. At each step these are finitely many excluded points on the current circle; a previously determined circle identical to the current intended one is allowed. Thus the only collinear or cocircular quadruples lie on one intended circle. Each intended circle has exactly q selected points, so there are exactly r forbidden q-subsets. Scale all coordinates by a common denominator to obtain integer points. The core has size two and each petal size q-2, proving equality and the polynomial. QED.

## Small explicit witness in the standard 11x11 grid

For r=5,q=4, the sharp minimum is N=12. The following twelve integer points lie in {0,...,10}^2, in this order:

    [(0,0),(0,1),(9,1),(4,5),(3,3),(5,0),
     (10,5),(2,5),(8,0),(8,1),(1,3),(3,4)]

The only forbidden quadruples are

    (0,1,2,3), (0,1,4,5), (0,1,6,7),
    (0,1,8,9), (0,1,10,11).

Hence the terminal polynomial is 32u^7+2u^11, with missing lengths 8,9,10. The independent verifier uses the exact integer 3x3 lifted determinant for all C(12,4)=495 quadruples, enumerates all 4096 subsets (3315 safe), and recursively computes normal/misere mex values (1,0) at the empty position. The verifier also exhausts all 32,896 abstract 0/1 incidence-support families with r=3 or r=4, checking the iff criterion by direct minimal-transversal enumeration. Those finite checks are separate from the universal proof.

The 12-point subset is not the full 121-point standard 11x11 game; no claim about its root outcome follows.
