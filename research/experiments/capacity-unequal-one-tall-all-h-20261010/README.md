# One tall column, unit short columns: complete all-parameter capacity game

**Status:** mathematical proof for all integers `h>=2, r>=0, k>=0`, with a fully labelled independent mex audit. This concerns an **abstract unequal-capacity occupancy game**, not a geometric realization of the ordinary two-dimensional game.

## Definition

There are `k+1` labelled columns with individual capacities `(r,1,...,1)`. A vector is safe if the sum of its largest `h` entries (or all entries when fewer than `h` columns exist) is at most `r`. A legal move increments one entry without violating either condition. Write `ell` for the tall-column occupancy and `a` for the number of occupied unit columns. All labelled vectors with the same `(ell,a)` have isomorphic continuation games.

Put `b=h-1`, `u=k-b`, `L=r-b`, `T=r+u`, `E(a)=r-2*b+1+a`.

## Theorem: exact Grundy function and terminal-size spectrum

**Degenerate range:** If `r<h` **or** `k<b`, the safety condition is equivalent to `ell+a<=r`, and every maximal vector has exactly `r` stones. Every safe state satisfies

```
g(ell,a) = (r-ell-a) mod 2.
```

There are `sum_{a=0}^{min(k,r)} binom(k,a)` labelled terminal vectors, and the maximum Grundy value is `0` for `r=0`, otherwise `1`.

**Nondegenerate range:** If `r>=h` and `k>=b`, the safe quotient states are exactly

```
0<=a<b:   0<=ell<=r-a
b<=a<=k:  0<=ell<=L.
```

The terminal quotient states are `(r-a,a)` for `0<=a<b`, and `(L,k)`; the terminal-size spectrum is **exactly** `{r,r+u}`. There are `sum_{a=0}^{b-1} binom(k,a)+1` labelled terminal vectors. For `u>=2`, the interval strictly between these two sizes contains exactly `u-1=k-h` unattainable terminal sizes. At every fixed `h`, the number of missing sizes is unbounded as `k` grows.

The complete Sprague–Grundy function is:

```
if u is even:
    g(ell,a) = (r-ell-a) mod 2
else:
    if a>=b:           g(ell,a) = (T-ell-a) mod 2
    elif ell==E(a):    g(ell,a) = 2
    elif ell<E(a):     g(ell,a) = (E(a)-ell) mod 2
    else:              g(ell,a) = (r-ell-a) mod 2
```

The `ell=E(a)` branch is empty when `E(a)<0`. Thus **every state in this family has Grundy value at most 2**. The value 2 occurs if and only if `r>=h` and `k>=h` with `k-h+1` odd; one explicit witness is `(ell,a)=(L,b-1)`.

## Proof

If `k<b`, the number of columns is less than `h`, so the top-`h` sum is the total occupancy. If `r<h`, any vector with total occupancy exceeding `r` has top-`h` sum exceeding `r`: either it has fewer than `h` positive entries, in which case the top sum is the total, or it has at least `h` positive entries, in which case the top sum is at least `h>r`. Thus in either degenerate case safety is exactly `ell+a<=r`. Any such state can be extended to total `r` by increasing the tall column (its remaining capacity is at least `r-ell-a`). All terminal vectors have size `r`, so backwards induction gives the parity formula and the terminal count follows by choosing the occupied short columns.

Now assume `r>=h` and `k>=b`. For `a<b`, the top-`h` sum is `ell+a`; for `a>=b`, safety is equivalent to `ell<=L` (including `ell=0`, since `r>=h`). For `a<b`, both move types are legal whenever `ell<r-a`, while at `ell=r-a` neither is. For `a>=b`, the tall and short coordinates can independently increase up to `L` and `k`. Hence the terminal states and sizes are as stated. The only possible distinct child types are tall and short, so mex is at most 2.

If `u` is even, the two terminal sizes have the same parity. All legal moves increase `ell+a` by one. Induction from terminals yields `g=(r-ell-a) mod 2` everywhere.

Suppose `u` is odd. In the rectangle `a>=b`, the remaining number of moves is fixed at `(L-ell)+(k-a)=T-ell-a`, giving its parity formula. For `a<b`, let `U_a=r-a` and `E_a=r-2b+1+a`. Then `U_a-E_a=2(b-a)-1` is positive and odd. We use descending induction in `a=b-1,...,0`, and within each row descending induction in `ell=U_a,...,0`.

At `ell=U_a` there is no move and the claimed last branch gives 0. At `ell<U_a`, the children are `(ell+1,a)` and `(ell,a+1)`, both safe. In row `a=b-1`, `E_a=L`, `U_a=L+1`: at `ell=E_a` the tall child is terminal with Grundy 0, and the short child has Grundy `u mod 2=1`, giving mex 2. Below the defect, the ordinary parity recursion applies, except immediately below it, where the child values are `{2,0}` and the mex is 1, again matching the formula.

For `a<b-1`, note `E_{a+1}=E_a+1`, `U_{a+1}=U_a-1`. At `ell=E_a>=0`, the tall child is just above the defect in its row and has value 0; the short child is just below the defect in the next row and has value 1. Hence mex is 2. Above the defect, both child values are the opposite parity to `(U_a-ell) mod 2`, except at `ell=E_a+1`, where they are `{1,2}`, giving mex 0. Below the defect, both children have the opposite parity to `(E_a-ell) mod 2`, except at `ell=E_a-1`, where they are `{2,0}`, giving mex 1. If `E_a<0`, the defect and the lower branch do not occur, and the same above-defect parity induction applies. This proves the formula for every safe state. For `u` odd, `(L,b-1)` lies at its defect `E(b-1)=L`, proving sharpness.

## Reproduction and trust boundary

Run `python research/experiments/capacity-unequal-one-tall-all-h-20261010/verify_one_tall_full.py` from the repository root. The script independently computes mex for fully labelled occupancy bitmasks using a sorted top-`h` legality test, and for the two-coordinate quotient using explicit inequalities. It compares both recursions against the formula, independently identifies all terminal states by absence of legal moves, and checks the terminal-size spectrum and counts.

Default audit: `2<=h<=7`, `0<=r<=h+5`, `0<=k<=min(h+4,11)`: **616 parameter cases**, **293,660 labelled safe states**, **38,574 labelled terminal states**, zero mismatches. Case digest SHA-256: `e762fefff89ee904d27fa0aee8a9507974b20642066e4625cda277c39609456f`. This is finite supporting evidence; the general result follows from the proof above, not from extrapolating the audit.

## Scope and earlier work

The `h=2, r>=2, k>=1` special case is in `research/experiments/capacity-unequal-terminal-gap-20261010/README.md`. The prior all-`h` proof for `r>=h, k>=h-1` is extended here to **every** `r>=0, k>=0` and supplied with a broader independent audit. The equal-capacity classification in `research/knowledge/items/K0352-general-dimensional-parallel-columns.md` is not contradicted. Neither a geometric realization nor a general bound for arbitrary unequal capacities is asserted.
