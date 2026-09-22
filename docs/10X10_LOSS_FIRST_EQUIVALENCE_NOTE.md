# Structural equivalence of loss-first-only and full cache-aware ordering

Base: `224f0dae89f95bfafa20290e872d96b9567dc6d7`

The confirmatory endpoint at `ec2d69f` found exact `visited` equality between
loss-first-only (L) and full cache-aware (F) on all 12 frozen parents.  This
note records a stronger observation: for the current solver semantics, the
relevant equality is structural rather than merely an empirical property of
that cohort.

## Definitions

At a below-root nonterminal node, let B be the blind total order
`(legal_move_count, canonical_key)`.

- L sorts by B, finds the B-earliest child whose prefetched memo value is LOSS,
  and rotates that one child to index 0.
- F partitions children by cached class `LOSS < unknown < WIN` and sorts each
  class by the same B key.

Therefore, whenever at least one cached LOSS exists, L and F have the same
first child: the B-minimum cached LOSS.

## Lemma

For a visited nonterminal node with at least one prefetched cached-LOSS child,
L and F perform the same work at that node and return WIN immediately.

Reason: the common first child already has cached outcome LOSS.  The child loop
uses the prefetched value instead of recursion.  On `!cw`, the solver records
the winning result and returns immediately, so no second child is inspected.
Thus the relative order of the remaining cached LOSS, unknown, and cached WIN
children is observationally irrelevant to `visited` and to the returned
outcome at that node.

If there is no cached LOSS, L is exactly B.  F may still differ from B by
moving unknown children before cached WIN children.  Consequently the only
possible source of an F-vs-L `visited` difference is a node with **zero cached
LOSS and at least one cached WIN whose placement relative to unknown children
changes subsequent recursive work**.

## Consequence for the 12-parent endpoint

The result `L == F` for 12/12 parents does not by itself show that
"multi-LOSS ordering" was empirically unimportant: under these solver
semantics, ordering among cached LOSS children cannot matter after the first
cached LOSS is selected.  The informative residual question is narrower:

> Does cached-WIN demotion ever save visited work at nodes with no cached LOSS?

The frozen cohort answers "not detectably here" because L and F are exactly
equal end-to-end, but the multi-LOSS part is eliminated analytically rather
than statistically.

## Highest-value follow-up

Before adding expensive parent-to-child DAG logging, existing instrumentation
can test the only remaining residual mechanism.  Add/derive counts at each
depth for nodes satisfying:

1. no prefetched cached LOSS;
2. at least one prefetched cached WIN;
3. at least one unknown child;
4. F changes the first recursively-entered unknown child or the amount of work
   before cutoff relative to B/L.

If condition (1)-(3) is rare or absent in the frozen 12-parent traces, L==F is
explained without invoking a broader DAG-convergence hypothesis.  If it is
common yet still contributes zero delta, inspect those nodes before designing
new heavy cohorts.

This refinement does not alter any frozen endpoint or success criterion.