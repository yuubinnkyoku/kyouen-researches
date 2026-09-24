# D9 one-shot read-mask: decision-leverage decomposition

Status: analysis plan frozen before D9LM1R/D9WM1R cohort execution.

## Mechanistic hypothesis

A LOSS-valued child and a WIN-valued child are not symmetric facts for the parent search.
In the production negamax-style loop, a cached child value avoids recursion in either case,
but a cached LOSS child additionally proves the current parent WIN and can terminate the
remaining sibling scan immediately. A cached WIN child only proves that this particular
move is not a winning witness for the parent; search continues.

This gives a concrete alternative to the vague statement that "LOSS memo entries are more
valuable": the excess value may be **decision leverage** (probability of causing an immediate
parent cutoff), rather than greater computational cost to recompute a LOSS state itself.
The existing loss-first-only endpoint strongly motivates this decomposition: promoting only
the B-earliest cached LOSS recovered the full cache-aware visited reduction on all 12 frozen
parents, while cached-WIN demotion contributed no residual visited benefit.

## Frozen measurements

For every selected D9LM1R / D9WM1R key, record the following without changing selection:

1. `first_consumption_site`: `entry` or `child_prefetch`.
2. `first_prefetch_parent_rank` and the child's sibling index in that parent's actual order.
3. `siblings_remaining_at_first_consumption` immediately after that child.
4. `first_consumption_causes_parent_cutoff`: true iff consuming the memo value makes that
   parent return WIN without examining another sibling.
5. `recompute_visited`: number of newly visited nodes attributable to the frame that is
   entered because this key is masked, measured from frame entry to its own return.
6. `post_recompute_parent_cutoff`: whether the recomputed value causes the same immediate
   parent cutoff at that consumption site.
7. `masked_key_reuses_before_retirement`: number of suppressed reads of the same epoch-0
   fact before its genuine recomputation retires the mask.

Instrumentation must be observational: no ordering, memo bytes, occupancy, mask selection,
or retirement rule may depend on these measurements.

## Frozen summaries

Report LOSS and WIN separately for:

- fraction first consumed by child-prefetch;
- fraction whose first consumption causes an immediate parent cutoff;
- median and total `recompute_visited`;
- median `siblings_remaining_at_first_consumption`;
- median suppressed reads before retirement.

Then stratify the one-shot treatment effect by `first_consumption_causes_parent_cutoff` using
only the baseline / pre-intervention consumption classification where available. Do not
reselect keys from treatment traces.

## Interpretation

- If LOSS has much larger cutoff incidence but comparable `recompute_visited`, the primary
  mechanism is decision leverage: LOSS facts are valuable because they terminate parent
  search, not because LOSS states are intrinsically more expensive to solve.
- If cutoff incidence is comparable but LOSS `recompute_visited` is much larger, intrinsic
  recomputation cost is the stronger explanation.
- If both are larger for LOSS, report both mechanisms; do not collapse them into a single
  "LOSS value" claim.
- If neither differs materially while D9LM1R still exceeds D9WM1R, the remaining candidate
  is reuse topology / downstream path divergence and requires a separate decomposition.

## Important asymmetry in causal interpretation

`first_consumption_causes_parent_cutoff` is partly determined by the memo value itself, so it
is a mechanism variable, not a pretreatment covariate suitable for a clean subgroup causal
claim. The stratified treatment-effect table is descriptive only. The primary causal
contrast remains the preregistered matched one-shot LOSS-vs-WIN intervention; this document
only decomposes why that contrast may differ.
