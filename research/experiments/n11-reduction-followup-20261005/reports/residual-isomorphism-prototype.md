# Residual-isomorphism prototype

Date: 2026-10-05

The first sound prototype is now `scripts/residual_iso.py`.

It canonicalizes the **full minimal residual clutter**, including rank-2,
rank-3 and rank-4 edges.  Vertex/edge colour refinement is only a partitioning
step; unresolved colour cells are exhaustively permuted before a label is
accepted.  Therefore a returned equal label is an exact hypergraph
isomorphism, not a Weisfeiler--Leman/hash guess.

To keep the first integration safe, canonicalization is **gated**.  If the
product of unresolved-cell factorials exceeds a configurable bound, the
function returns `None`; a solver integration must then fall back to the
existing D4 key.  Thus hard symmetric states lose an optimization opportunity
rather than risking an unsound merge.

The self-test contains three regression obligations:

- rank-3 information distinguishes clutters with the same insufficient
  pair-level view;
- arbitrary vertex relabeling preserves the exact label;
- a high-symmetry case exceeding the gate is rejected rather than approximated.

This establishes the safe keying primitive needed for the next benchmark, but
does **not** yet establish a speedup.  The next measurement is the 23 cold s5
replay roots from `N11-DFPN-S5-BENCH.md`, with residual-build and
canonical-label wall time charged to the optimization.

The multi-class count-vector direction remains theorem-backed by K0344:
sequential class kernels are sound.  A production count-vector state encoding
is intentionally deferred until the residual-isomorphism benchmark tells us
how often non-D4 merges actually occur; otherwise it would add a second
representation before demonstrating reuse.

**11x11 empty root remains UNKNOWN.**
