# Cached-LOSS prefix memo causal ablation

## Motivation

The provenance counters preregistered on this branch answer an observational
question: are memo entries first created inside a blind-order prefix reused
after that prefix exits?

That is not yet the causal quantity needed for the mechanism claim.  A tagged
entry can have zero direct later hits but still alter later search indirectly,
and a later hit can occur on a path that would disappear if the prefix-created
memo were absent.  `later_reuse_any` and `later_reuse_outside_prefix` therefore
remain diagnostics, not estimates of saved work.

## Causal intervention

Add a paired blind-order run, identical to the ordinary blind solver except for
one intervention:

1. When outer cached-LOSS-prefix depth changes `0 -> 1`, start one ownership
   event, using the already-preregistered owner bookkeeping.
2. Every memo slot first inserted while that outer event is active is marked as
   owned by the event.  Nested prefixes share the outer owner.
3. On the matching outer exit (`1 -> 0`), invalidate exactly the memo entries
   still occupying slots owned by that event.
4. Do not undo visited work, counters, or memo entries that predate the event.
   Do not invalidate slots that have been cleared/reused since their tagged
   insertion.
5. Continue the search normally.  Future consequences of the invalidation,
   including changed paths and changed later memo creation, are intentionally
   retained.

Call this condition **blind-prefix-forget** (`BPF`).  The ordinary blind run is
`B`.

The intervention is deliberately at outer exit rather than at insertion: work
inside the prefix is kept identical for as long as possible.  The contrast
therefore targets the *future value of memo state produced by that prefix*, not
the immediate cost of traversing the prefix.

## Primary causal quantity

For each frozen parent, report

```
future_memo_value = visited(BPF) - visited(B)
relative_future_memo_value = (visited(BPF) - visited(B)) / visited(B)
```

Positive values mean that prefix-created memo pays back later; zero means no
net future value at visited-node resolution.  Negative values are allowed and
would mean the retained memo state is, on balance, harmful to the subsequent
search order/cache trajectory.

This quantity includes downstream cascades.  That is intentional: it is the
causal effect of retaining the prefix-produced memo state, not a sum of direct
memo hits.

## Relationship to the loss-first gain

Keep the existing loss-first run `L` unchanged.  For each parent also report

```
immediate_plus_trajectory_gain = visited(B) - visited(L)
```

Do **not** assert the identity

```
visited(B) - visited(L)
  = prefix_visited - future_memo_value
```

because loss-first changes the prefix itself and therefore the later search
trajectory.  BPF is a mechanism probe, not an additive decomposition of the
B-vs-L endpoint.

The useful interpretation is narrower:

- if `future_memo_value` is tiny while B->L is large, the hypothesis that blind
  prefixes are valuable mainly as memo investment is weakened;
- if `future_memo_value` is substantial and positive, the memo-investment
  counterforce is real and a trajectory/DAG analysis is justified.

## Frozen cohort and reporting

Use the same 12-parent frozen cohort and solver settings as the existing
loss-first confirmatory endpoint.  Do not select parents based on provenance
results.  Report all 12 paired B/BPF values, median relative effect, total
visited effect, and the sign count (BPF > B / = / <).

No new pass/fail threshold is introduced here.  The previously preregistered
`later hits / put < 0.05` rule remains unchanged and applies only to its stated
observational diagnostic.  BPF is a separate causal follow-up.

## Required safety checks before the 12-parent run

1. Instrumentation/ablation disabled reproduces the existing blind endpoint
   exactly.
2. A synthetic single outer prefix with one inserted entry invalidates that
   entry at outer exit.
3. A nested prefix does not invalidate at inner exit.
4. A pre-existing memo entry touched inside the prefix survives outer exit.
5. A tagged slot cleared/reused before outer exit is not used to invalidate the
   replacement entry.
6. A run containing no cached-LOSS prefix is bit-for-bit/endpoint identical
   between B and BPF.

## Priority

Implement BPF only after the owner-state model tests already on this branch
pass.  It has higher inferential value than adding more direct-hit counters,
because it measures the downstream consequence of prefix-produced memo rather
than treating observed reuse as a proxy for that consequence.
