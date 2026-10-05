# Native residual micro-kernel integration boundary

Date: 2026-10-05

**11x11 empty root remains UNKNOWN.**

A native theorem-backed kernel now exists at
`cpp/solvers/kyouen_residual_micro.hpp`.  It implements the residual-clutter
semantics already proved/audited in K0344:

- inclusion-minimal residual edges;
- exact exchangeable-class detection by transposition automorphisms;
- sequential K0344 class reduction;
- connected-component splitting with Grundy xor;
- exact mex recursion with a residual-state memo;
- conversion of the residual Grundy P/N result back to df-pn exact_prop's
  fixed proposition "the original first player wins" using stone-count parity.

`cpp/tests/test_kyouen_residual_micro.cpp` exhaustively compares the optimized
kernel with a direct uncompressed mex solver for every edge-family candidate on
up to four vertices.  This source-level regression is deliberately independent
of board geometry.

## Why it is not wired into exact_prop yet

The remaining trust boundary is board -> residual clutter construction.
K0344 is a theorem about the **exact inclusion-minimal residual hypergraph**.
Feeding it a pair-only graph, a nonminimal approximation, or an edge family
that contains a currently impossible point would invalidate the optimization.

Therefore the production integration is staged:

1. implement a board-to-residual builder for a small legal frontier;
2. regression-check every residual move against the existing
   `legal_for/added_bans` transition;
3. only then allow `exact_prop` to return the native kernel verdict;
4. run the fixed cold replay gate benchmark and require all verdicts to match.

This is intentionally stricter than inserting the kernel immediately: the
historical pair-graph counterexample in K0336 shows that an approximate
residual identity is not a safe solver key.

## Expected gate

The incidence audit supports a module/component construction gate around
legal<=12 and an exact residual-isomorphism gate around legal<=6.  The native
kernel currently implements the first two pieces.  Arbitrary residual
isomorphism remains a later optional memo layer and must earn its wall cost in
the cold replay benchmark.
