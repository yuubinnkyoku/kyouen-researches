# Branching-tree terminal polynomial: exact finite extension (2026-11-03)

**Evidence class: finite exhaustive enumeration, not a universal theorem.**

Extends the earlier audit of all non-path unlabelled trees of orders 4–8 to **orders 9 and 10**. For each tree and each `r=q-3` in `{1,2,3,4,5}` (thus `q=4..8`), calculate the center-containing terminal polynomial by direct enumeration of admissible cores under K0648. Determine the number of negative real roots by SymPy's exact real-root counting, not floating-point approximations.

- Order 9: **46** branching nonisomorphic trees, **230** tree/parameter cases.
- Order 10: **105** branching nonisomorphic trees, **525** cases.
- **755** additional cases checked, **zero real-rooted branching examples**.
- Together with the previous 200 cases for orders 4–8, this gives **955** checked tree/parameter cases for orders 4–10.

Reproduce: `python verify.py` (requires networkx and sympy). The program asserts each polynomial has fewer negative real roots than its degree. Every polynomial has positive coefficients, so any real roots would have to be negative.

This supports the conjecture that branching trees never have a real-rooted center-containing terminal polynomial for `q>=4`, but **does not prove it** for arbitrary order or q. K0664 proves the path case, and K0665 proves the star obstruction.
