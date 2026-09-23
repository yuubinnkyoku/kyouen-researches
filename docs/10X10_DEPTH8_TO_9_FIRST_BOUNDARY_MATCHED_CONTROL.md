# Depth-8 -> depth-9 first-boundary matched causal control

## Status

Preregistered before any D9LF/D9WF/D9LM/D9WM cohort execution. This supplements, and does not replace, the frozen full and count-matched interventions.

## Motivation

The count-matched D9LM/D9WM diagnostic equalizes deletion count only while the two variants share the same pre-boundary trace. After the first effective deletion, their search trajectories may diverge; later eligible sets and realized deletion counts are then endogenous consequences of earlier treatment. Aggregate D9LM versus D9WM therefore cannot be interpreted as a fully paired value-label contrast even when the first boundary is perfectly matched.

Use a one-shot intervention to isolate the first causal divergence.

## Frozen intervention

For each frozen parent, run baseline B until the first depth-8 producer-parent exit at which both live producer-owned depth-9 LOSS and WIN sets are non-empty. Call this boundary `t*`.

At `t*` only:

- let `L` and `W` be the eligible live producer-owned LOSS and WIN entries;
- let `k = min(|L|, |W|)`;
- `D9LM1`: invalidate exactly `k` LOSS entries using the already-frozen deterministic `(hash, canonical_key)` selection rule;
- `D9WM1`: invalidate exactly `k` WIN entries using the same rule.

After `t*`, perform no further experimental invalidation. Ordinary memo replacement and solver behavior continue unchanged.

If no boundary with `k > 0` exists, mark the parent `NO_ELIGIBLE_BOUNDARY`; do not substitute a later depth or relax the eligibility rule.

The two variants must be forked from the identical pre-`t*` physical memo-table state, not merely from an equivalent logical key/value map. The fork state includes every slot's key/value, live/tombstone state, owner metadata, and all occupancy/replacement bookkeeping that can affect later lookup or insertion behavior. Preferred implementation is an exact in-memory clone at `t*`. Independent replay is valid only when both logical and physical-state digests, plus the trace through `t*`, are verified identical. Rebuilding a fresh table from the logical map is not a valid fork because slot placement and replacement state may differ.

Thus the treatment dose is exactly matched at the moment of intervention and cannot be altered by treatment-induced trajectory divergence.

## Primary measurements

Per parent report:

- `t*` identity / deterministic boundary index;
- `k`;
- `visited(D9LM1) - visited(B)`;
- `visited(D9WM1) - visited(B)`;
- `visited(D9LM1) - visited(D9WM1)`;
- final outcome equality across B, D9LM1, D9WM1.

Across eligible frozen parents report total and median visited deltas plus the sign count of `visited(D9LM1) - visited(D9WM1)`. Do not divide visited delta by `k` and call it a per-entry effect: memo interactions are nonlinear.

## Interpretation

- `D9LM1 > D9WM1` consistently supports greater future causal value of the first matched batch of depth-9 LOSS memo than the corresponding WIN batch.
- Similar effects weaken the simple LOSS-label-specific explanation and suggest that deletion volume or generic memo investment explains the full-intervention contrast.
- A strong full D9LF/D9WF contrast with little first-boundary contrast implies that repeated interventions, later boundaries, or treatment-induced trajectory changes are important; the full contrast must not be attributed to a single matched LOSS batch.

This experiment estimates a one-shot boundary-level treatment contrast, not a global per-entry effect.

## Safety requirements

Before cohort execution require:

1. B, D9LM1, and D9WM1 have identical trace, logical memo-state digest, and physical memo-table digest immediately before `t*`. The physical digest must cover each slot's key/value, live/tombstone state, owner metadata, and all occupancy/replacement bookkeeping that can affect future behavior;
2. no variant may reconstruct its pre-`t*` table by reinserting the logical map into a fresh table; use an exact clone, or an independently replayed state satisfying requirement 1;
3. D9LM1 and D9WM1 delete exactly the same `k > 0` entries by count at `t*`;
4. no experimental invalidation occurs before or after `t*`;
5. selected key sets obey the frozen slot/order-independent hash rule;
6. non-target value entries at `t*` are untouched;
7. all three variants return the same game-theoretic outcome;
8. disabling the one-shot deletion reproduces B exactly, including visited count and the post-`t*` event trace.
