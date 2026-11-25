# 11x11 reduction-surface audit (2026-10-05)

**11x11 empty root: UNKNOWN.** This note audits four proposed reductions against the current solver before adding another expensive residual pass.

## Result

1. **Multi-class quotient.** K0344 already proves per-class quotient DAG equivalence, but the shared C++ exact solver does not materialize the residual quotient. This remains a genuine implementation/benchmark target.
2. **Residual connected components.** Already implemented and measured in `module_core.py` as `modules-components`; on the saved n11 late snapshots it reduces the aggregate memo count from 17,324 baseline to 9,341 together with K0344 modules. Do not count this again as a new reduction.
3. **Equivalent moves.** The production generator `gen_into` already computes the D4-canonical child key and drops duplicate children before search. Thus board-symmetry-equivalent moves are already merged at every df-pn/exact node.
4. **State canonicalization.** `exact_prop` keys both PnTT and exact-local memo by `canonical(state)`, so D4-equivalent occupied states are already shared. A new canonicalizer is useful only if it identifies residual-game isomorphisms beyond board D4.

## Consequence

The next non-duplicate experiment must target **residual isomorphism beyond D4** and/or a **count-vector quotient over several K0344 exchangeable classes**. Any implementation must be gated to exact handoff first: residual construction and canonical-label overhead must be included in wall time.

For a sound residual-isomorphism key, equality must cover the full minimal residual clutter (rank 2--4), not only the pair graph. Pair-only identification is refuted by K0336. Candidate keys may use refinement/hashing only as a filter; two states may be merged only after an exact isomorphism/canonical-label check.

The benchmark target is the existing 23 cold s5 replay roots. Record verdict, exact nodes, wall time, number of residual builds, quotient/canonical-label time, memo hits, and number of states merged beyond D4. Reject the optimization if verdicts differ or if wall time does not improve despite fewer nodes.
