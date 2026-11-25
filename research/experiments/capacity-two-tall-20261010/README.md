# Two-tall unequal-capacity top-two game: complete terminal sizes and Grundy formula

**Status:** Mathematical proof for all `r>=2`, `1<=s<=r`, `k>=1`; two independently organized finite checks. This is an **abstract** capacity game. No geometric realization as a standard 2D kyouen board is claimed.

## Definition

There are `k+2` labelled columns with capacities `(r,s,1,...,1)` (the final `k` capacities are 1). A state `x=(a,b,z_1,...,z_k)` is safe when the sum of its **two largest occupancies** is at most `r`. A move increments one coordinate by 1, remaining within its capacity and safety bound. Let `t=sum(z_i)` and `N=a+b+t`.

## Theorem (all parameters, all safe states)

The terminal states are **exactly**:

1. `(r,0,0,...,0)`;
2. if `s=r`, also `(0,r,0,...,0)`;
3. all `(a,b,1,...,1)` with `a>=1`, `b>=1`, `a+b=r`, and `b<=s`.

Consequently the **set of terminal stone counts is exactly `{r,r+k}`**. The `k-1` intermediate sizes are absent; for arbitrary `k` the terminal-size gap is unbounded.

The Sprague-Grundy value of every safe state is

```
g(x) = 0                           if (a,b,t)=(r,0,0)
     = 0                           if s=r and (a,b,t)=(0,r,0)
     = 2                           if k odd and (a,b,t)=(r-1,0,0)
     = 2                           if k odd, s=r, and (a,b,t)=(0,r-1,0)
     = (r+k-N) mod 2               otherwise.
```

The cases above are mutually exclusive for `r>=2`. In particular, `g(x)<=2` for **all** parameters; the maximum Grundy value is 1 when `k` is even and 2 when `k` is odd. The empty state is P iff `r+k` is even. The result does not depend on `s` except for the availability of the symmetric exceptional states when `s=r`.

## Proof of the terminal classification

If `a,b>=1`, then adding an unoccupied short column never increases the sum of the two largest occupancies beyond `a+b<=r`; therefore terminality requires `t=k`. If `a+b<r`, the first tall column can still be increased (as `b>=1` ensures `a<r`), so terminality also requires `a+b=r`. Conversely these conditions give terminal states.

If `a>=1,b=0,t>0`, safety implies `a<=r-1`, and adding one to the second tall column is safe since `s>=1` and `a+1<=r`. The symmetric argument holds when `a=0,b>=1,t>0`: adding to the first tall column is safe. If `a=b=0,t>0`, adding to the first tall column is safe because `r>=2`. Thus no state with `t>0` and a zero tall column is terminal.

If `t=0,b=0,a>0`, incrementing `a` is safe until `a=r`, which is terminal. If `t=0,a=0,b>0`, incrementing `a` is safe unless `b=r`; the latter is possible only if `s=r`, and is terminal. The empty state is not terminal. This proves the list and both sizes are attainable (choose `b=1`, `a=r-1` for the second size).

## Proof of the Grundy formula

**Parity lemma.** In any finite game whose moves increase the total occupancy by one, if all terminal descendants of a state have the same parity of total occupancy `T`, then every descendant `y` has `g(y)=(T-|y|) mod 2`. Indeed terminal states have `g=0`, and induction makes every child of a nonterminal state have the opposite parity, whose mex is the required bit.

When `k` is even, both terminal sizes `r` and `r+k` have the same parity. The parity lemma proves the displayed formula, including the alleged exceptional states (the `g=2` cases are disabled).

Suppose `k` is odd. Any safe state with at least one short column occupied or with **both tall columns positive** has only terminal descendants of size `r+k`. This also holds for states with `a=0, 1<=b<=s<r, t=0`: they cannot reach either lone-full terminal state. By the parity lemma all these states have value `(r+k-N) mod 2`.

Consider the first tall axis `(a,0,0^k)`. At `a=r` it is terminal, hence `g=0`. At `a=r-1`, the move to `a=r` has value 0, while either a move to the second tall column or to any short column has value `k mod 2=1`; thus `g=mex{0,1}=2`. At `a=r-2`, the axis child has value 2 and each off-axis child has value 0, so `g=mex{0,2}=1`, matching `(r+k-(r-2)) mod 2`. For all `a<=r-3`, the axis child and every off-axis child have the same value `(r+k-a-1) mod 2`; induction gives `g=(r+k-a) mod 2`. If `s=r`, the second tall axis is symmetric and obeys the same rule. Otherwise it is covered by the parity lemma.

Finally, at the empty state, when `r>=3` every first move has value `(r+k-1) mod 2`, giving `g=(r+k) mod 2`. When `r=2` and `k` is odd, the first-tall child has value 2 (and so does the second-tall child if `s=r`), whereas a short-column child has value 0; the remaining possible child has value 0. Thus `g(empty)=mex{0,2}=1=(r+k) mod 2`. This closes the induction and proves the formula for all `r>=2`.

## Finite audits

Run the two scripts independently:

```
python research/experiments/capacity-two-tall-20261010/verify_labelled.py
python research/experiments/capacity-two-tall-20261010/verify_quotient.py
```

- `verify_labelled.py`: full **labelled occupancy** enumeration and recursive mex with a fresh safety test. `2<=r<=9`, `1<=s<=r`, `1<=k<=8`: 352 parameter triples, **561,416** safe labelled states, 0 mismatches; all terminal sizes checked.
- `verify_quotient.py`: independent **bottom-up** mex on compressed `(a,b,t)` states; `2<=r<=20`, `1<=s<=r`, `1<=k<=16`: 3,344 parameter triples, **2,894,536** safe quotient states, 0 mismatches; all terminal sizes checked.

The enumerations independently support the proof but do **not** establish the unbounded result by themselves.

## Relationship to earlier work

The special case `s=1` is the previously studied one-tall family with `k+1` unit columns. The genuinely new part is `s>=2`: surprisingly, increasing the second tall capacity does not change the general Grundy formula or the two terminal sizes. The result does **not** contradict equal-capacity column theorems: the remaining `k` columns still have capacity 1. It also does not settle the unrestricted unequal-capacity Grundy bound or the standard 2D game.
