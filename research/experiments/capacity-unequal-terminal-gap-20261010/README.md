# Unequal-capacity top-two game: unbounded terminal gaps and exact Grundy formula

**Status:** Unbounded mathematical proof; direct-mex audit for 2<=r<=8 and 1<=k<=11. This is an abstract capacity game; no geometric q-point realization is claimed.

## Theorem

Consider k+1 labelled columns with capacities c=(r,1,...,1), r>=2, k>=1. An occupancy vector is safe iff the sum of its two largest entries is <=r. Each move increases one entry by one, respecting both capacity and safety. Write ell for the tall column's occupancy and a for the number of occupied short columns.

The **only maximal occupancies** are (r,0,...,0) and (r-1,1,...,1). Their sizes are respectively r and T=r+k-1. Thus terminal sizes are **exactly {r,T}**, with k-2 missing integers strictly between them when k>=3. These gaps are unbounded. For r=3 (formal q=4 capacity), k=3 gives capacities (3,1,1,1), terminal sizes {3,5}, and no terminal size 4.

The **complete Sprague-Grundy function** is

```text
g(ell,a) = 0                 if ell=r, a=0
         = 2                 if ell=r-1, a=0, k even
         = (T-ell-a) mod 2   otherwise.
```

Consequently g(empty)=T mod 2. The maximum Grundy value is 2 when k is even, and 1 when k is odd.

## Proof

If ell=r, safety forces all short columns to be empty, giving the first terminal vector. For ell<=r-1, every empty short column can be filled safely: after such a move the top-two sum is <=max(2,ell+1)<=r (when ell=0, the sum is at most 2). Hence terminality requires all short columns full. With at least one occupied short column, the tall column can then be increased until ell=r-1, but not to r. This gives the second terminal vector. Both vectors are indeed terminal.

For a>=1, the remaining (r-1-ell)+(k-a) moves are all legal in any order, so g(ell,a) is their parity. For a=0 and ell=r, g=0. At (r-1,0), the two child Grundy values are 0 and (k-1) mod 2; their mex is 1 if k is odd, 2 if k is even.

For ell=r-2, the two children have values (1,1) if k is odd and (2,0) if k is even, giving mex 0 or 1 respectively, exactly (T-ell) mod 2. For each smaller ell, the children (ell+1,0) and (ell,1) both have the parity opposite to (T-ell) mod 2 by induction, and mex yields (T-ell) mod 2. This proves the closed form for every state.

## Independent audit

`verify_gap_family.py` enumerates all safe labelled occupancy vectors, evaluates legal moves using the original top-two constraint, computes Grundy by direct recursive mex, and compares every state to the closed form. It also checks the terminal-size set. Run:

```sh
python research/experiments/capacity-unequal-terminal-gap-20261010/verify_gap_family.py
```

77 parameter pairs (2<=r<=8, 1<=k<=11), 143,367 safe states, zero discrepancies. The finite audit is independent support, **not** the proof of the unbounded claim.

## Scope

K0352's no-holes terminal-threshold result assumes **equal** column capacities. The example shows this hypothesis cannot be dropped. It does not imply a terminal-size gap for the standard two-dimensional 4-point game. The formal identification r=q-1 alone does not establish geometric realizability.
