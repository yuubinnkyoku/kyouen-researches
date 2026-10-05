# Residual endgame micro-solver integration

Date: 2026-10-05

**11x11 empty root remains UNKNOWN.**

`scripts/micro_solver.py` now composes the three sound residual reductions in
the order suggested by the activation audits:

1. exact K0344 sequential exchangeable-class reduction;
2. full-incidence connected-component splitting with Grundy xor;
3. exact full-clutter residual-isomorphism memoization only below a configurable
   small-legal gate (default `legal<=6`).

The isomorphism stage is conservative.  If exact canonical labelling exceeds
its permutation work bound, the solver uses the raw residual state key.  No
heuristic colour/hash collision can determine a game value.

The implementation exposes counters for module vertices removed, component
splits, isomorphism attempts/hits/gate-outs, raw memo hits, and both memo sizes.
This is the instrumentation required for the cold s5 replay benchmark.

A small deterministic self-test compares the composed solver against the
existing theorem-backed `modules-components` reference on rank-2--4 residual
clutters.  This is a code regression guard, not evidence for 11x11 outcome.

## Benchmark acceptance rule

Production C++ integration should be accepted only if all 23 existing cold s5
replay roots preserve their exact verdict and aggregate wall time improves.
Node/memo reduction alone is insufficient.  Compare at least iso gates
`0, 4, 5, 6, 7`; gate 0 gives the module+component control.  Charge residual
construction and canonical-label time to the candidate.

The saved-snapshot audits predict that isomorphism above legal 6 is unlikely to
pay, while K0344 reductions remain occasionally active through legal 12.
Therefore module/component reduction may deserve a looser gate than residual
isomorphism in a native implementation.
