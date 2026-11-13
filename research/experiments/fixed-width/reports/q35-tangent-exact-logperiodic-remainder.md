# 3×m, q=5: exact logarithmic-periodic formula and signed remainder

Status: mathematical consequence of the previously proved tangent-family classification; not a claim about all five-point circles.

Let λ=3+2√2, C=4+3√2, D=4−3√2 (<0). The tangent-family chord spans satisfy
a_j=C λ^j+D λ^(−j), j≥0, with a_0=8, a_1=48 and a_(j+2)=6a_(j+1)−a_j.

For every integer m≥9 put x=log_λ(m/C), θ={x}, N=floor(x)+1. Then

T_5(m)=2m log_λ(m/C)+m H(θ)+4+2D λ^(1−N)/(λ−1),

where H(θ)=2(1−θ)−2λ^(1−θ)/(λ−1). In particular the remainder after the displayed periodic main expression and constant 4 is **strictly negative**, of order O(1/m), and is given exactly, not just asymptotically.

## Proof

The established tangent classification gives T_5(m)=2 Σ_(a_j<m)(m−a_j). Since −1<D<0 and λ>1, for j≥0 we have a_j=Cλ^j+Dλ^(−j), with 0<Cλ^j−a_j<1. As a_j is an integer, a_j<m for integer m iff Cλ^j<m. For m≥9 this yields precisely j=0,…,N−1, with N=floor(log_λ(m/C))+1 (none of the Cλ^j is an integer).

The finite geometric sum is

Σ_(j=0)^(N−1) a_j = C(λ^N−1)/(λ−1)+D λ(1−λ^(−N))/(λ−1).

The identity C−Dλ=4+4√2=2(λ−1) reduces the exact count to

T_5(m)=2Nm−2Cλ^N/(λ−1)+4+2Dλ^(1−N)/(λ−1).

Substitute N=x+1−θ and Cλ^N=mλ^(1−θ). This proves the formula. Since D<0 the last term is negative. Also λ^N>m/C, so its magnitude is bounded by 2|D|λ C/((λ−1)m).

## Independent arithmetic check

An integer-only check for every m=9,…,100000 compared direct finite summation 2Σ max(0,m−a_j) with the independently rearranged recurrence identity

T_5(m)=2Nm−(a_N−a_(N−1)−8)/2.

All 99992 cases agreed. This tests the recurrence algebra, but does not independently establish the geometric tangent classification.

## Scope

The statement concerns only tangent-type circles in 3×m with five lattice points. It does not determine the growth of the complete F_5(m), and the formula is conditional on the previously proved classification of tangent families.
