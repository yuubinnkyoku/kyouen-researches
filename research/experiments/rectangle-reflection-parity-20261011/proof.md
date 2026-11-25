# Rectangle reflection parity: all q, explicit q=4 formula (2026-10-11)

## Scope and status

**Theorem (mathematical proof).** Let `P_{w,h}={0,...,w-1}×{0,...,h-1}` with positive integers `w,h`. For `q≥4`, let `C_q(w,h)` and `H_q(w,h)` denote the numbers of distinct q-element subsets lying on a genuine circle and on a line, respectively. Collinear q-subsets are **not** counted as cocircular. All congruences below are modulo 2.

This note gives formulas for every `q` and a closed form for `q=4`, without enumerating forbidden subsets. This is not a claim about Grundy numbers or game winners.

## D2 orbit theorem for circles

Write centered doubled coordinates `X=2x-(w-1), Y=2y-(h-1)` and `R=X²+Y²`. For each `R>0`, let

* `u_R` be the number of **distinct** pairs `(abs(X),abs(Y))` realized by board points with `X≠0,Y≠0` and squared radius `R`. Each such pair gives a 4-point orbit under horizontal and vertical reflection.
* `v_R` be the number of such pairs with **exactly one** of `X,Y` zero. Each gives a 2-point orbit. (Necessarily `0≤v_R≤2`.)

Then, for every `q≥4`,

```
C_q(w,h) ≡ Σ_{R>0} [t^q] (1+t^4)^{u_R}(1+t²)^{v_R} (mod 2).
```

In particular `C_q(w,h)` is even for every odd `q`.

**Proof.** The two reflections generate a group of order 4. On its action on the set of cocircular q-subsets, every nontrivial orbit has even size; therefore the parity of the total is the parity of the number of subsets fixed by both reflections. A fixed subset `S` with at least 3 points determines a unique circle. Both reflections preserve `S` and hence preserve that circle; its center must be the intersection of the two reflection axes, i.e. the board center. The center point itself is not on a genuine circle centered there. Thus `S` is a union of the indicated 4- and 2-point point-orbits of a *single* positive radius `R`. Choosing the point-orbits independently gives the displayed generating polynomial. Conversely every such choice is a cocircular q-subset fixed by both reflections. No circle is counted twice because at least three noncollinear points determine its center and radius. ∎

The same orbit argument holds for any finite planar point set invariant under two perpendicular reflections, with `u_R,v_R` defined from its point-orbits.

## D2 orbit theorem for lines

Set `a=floor(w/2), b=floor(h/2)` and adopt `binom(n,k)=0` if `k>n` or `k<0`. For `q=2k≥4`,

```
H_{2k}(w,h) ≡ [h odd] binom(a,k) + [w odd] binom(b,k) (mod 2).
```

For `q=2k+1≥5`,

```
H_{2k+1}(w,h) ≡ [w odd AND h odd] (binom(a,k)+binom(b,k)) (mod 2).
```

**Proof.** A collinear subset of at least two distinct points determines its line uniquely. If fixed by both reflections, that line must itself be invariant under both; the only such lines are the two central axes. The horizontal central line has board points only if `h` is odd. They consist of `a` symmetric pairs and, when `w` is odd, the center point. An even-size invariant subset chooses `k` pairs without the center; an odd-size invariant subset chooses `k` pairs plus the center. The vertical axis is analogous. For `q≥4` the two axes cannot yield the same q-subset, because their intersection has at most one point. All other line-subsets occur in even-sized group orbits. ∎

## Closed four-point formulas

Taking the coefficient of `t^4` above gives

```
C_4(w,h) ≡ floor(w/2)*floor(h/2)
             + [w odd AND h odd]*min(floor(w/2),floor(h/2))  (mod 2),
H_4(w,h) ≡ [h odd]*binom(floor(w/2),2)
             + [w odd]*binom(floor(h/2),2)                   (mod 2).
```

**Why this simplification is exact.** A reflection-invariant cyclic four-set is either (i) one four-point off-axis orbit, the four corners `(±X,±Y)` of a rectangle centered at the board center; there are `floor(w/2)*floor(h/2)` choices, or (ii) two on-axis antipodal pairs of the same radius. Such a pair must use one horizontal and one vertical pair, and exists for each positive radius whose coordinates occur on both axes. The number of these is `min(floor(w/2),floor(h/2))` when both side lengths are odd and zero otherwise.

Thus the parity of the **total forbidden quadruple count** `F_{w,h}=C_4+H_4` is obtained by adding the two expressions. For a square `w=h=n`, the line term vanishes and

```
F_{n,n} is odd  iff  n ≡ 2 (mod 4).
```

This recovers the square-board parity as a special case, while also covering non-square rectangles and all q-point versions.

## Independent audit and limitations

`verify.py` constructs all lines from point pairs and all circles from noncollinear triples, using canonical **integer** equations. It then counts q-subsets on each unique line/circle via binomial coefficients, for all 49 boards `1≤w,h≤7` and `4≤q≤8` (245 `(w,h,q)` conditions). This is independent of the reflection-orbit calculation, which only inspects squared distances to the center. For all 25 boards `1≤w,h≤5`, the q=4 counts are additionally checked by brute-force four-subset enumeration and an independent 4×4 determinant. All comparisons pass.

No finite audit is used to prove the unbounded formulas. The proof is the group action and the uniqueness of a circle or line through the indicated points. For `q<4` circle/line overlap and the intended forbidden-family convention may differ; such cases are excluded.

Reproduce: `python verify.py` (standard library only).
