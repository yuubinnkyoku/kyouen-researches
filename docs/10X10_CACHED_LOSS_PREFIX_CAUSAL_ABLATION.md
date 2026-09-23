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

## Invalidation implementation constraint

The owner-event sidecar is sufficient for provenance counting, but by itself it
does not provide an efficient way to enumerate every entry owned by one event
at outer exit.  Do **not** silently reintroduce an O(table-size) scan at every
outer exit merely to implement step 3 above.

Prefer lazy logical invalidation.  In BPF mode, after an outer event exits, a
lookup must behave as though any still-current entry with

```
origin_outer_event != 0 && origin_outer_event <= last_exited_outer_event
```

is absent.  A slot whose payload has been cleared/replaced must also have its
owner metadata cleared/replaced, so a later occupant is never rejected because
of an old owner id.

The production `Memo` in `cpp/solvers/kyouen_solver_verify.cpp` is linear
probing: `get` continues while `v[i] != 0` and stops at the first physically
empty slot; `put` likewise probes occupied slots and inserts only at a physical
empty slot.  It has no deletion/tombstone path.  Therefore merely suppressing a
forgotten slot as a hit while leaving it permanently occupied is **not** an
exact implementation of eager forgetting: forgotten entries would consume
capacity forever, lengthen later probe chains, and could change insertion
behaviour independently of the intended memo-state intervention.

For BPF, treat a logically forgotten slot as a tombstone with the following
frozen semantics:

- lookup: it is never a hit, but probing continues through it;
- insertion: remember the first logically forgotten slot encountered, continue
  probing far enough to preserve ordinary same-key/update semantics, and if no
  live copy of the key is found before the first true empty slot, insert into
  the remembered forgotten slot (or the true empty slot if there was none);
- replacement/reinsertion must write the new owner metadata from the *current*
  context: current outer event id when inside a prefix, otherwise zero.  It must
  never inherit the forgotten occupant's owner id;
- a stale copy of the same key is not a live existing memo entry.  Recomputing
  that state may make it live again, and the new value/owner must then be
  observable normally.

This gives forgotten slots the standard open-addressing tombstone role while
allowing their capacity to be reclaimed.  It is required for the lazy BPF table
to represent the same logical map as eager deletion without breaking collision
chains.  A permanently occupied stale-slot implementation is prohibited even
if its lookup hit/miss answers initially agree with an eager reference.

This is an implementation constraint, not a change to the intervention: BPF
must expose exactly the same memo state to subsequent solver logic as eager
invalidation would, modulo representation-internal tombstones/occupancy needed
to preserve lookup correctness.

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
7. For the production linear-probing table, construct a collision chain A -> B
   where A is prefix-owned and B is not; after A is forgotten, B must remain
   findable.
8. Force insertion after a forgotten A in a collision chain and verify that A's
   slot is reclaimable rather than permanently consuming capacity, while later
   colliding live entries remain findable.
9. Forget key A, recompute A, and insert it once outside a prefix and once inside
   a new prefix.  Both must become live again with owner zero / the new owner,
   respectively; the old owner must not survive.
10. Compare lazy invalidation against a small reference memo that eagerly
   removes forgotten entries over randomized insert/lookup/clear/outer-exit
   traces.  Compare not only hit/miss/value answers but also logical live-entry
   count; periodically force enough insertions to exercise stale-slot reuse.

## Priority

Implement BPF only after the owner-state model tests already on this branch
pass.  It has higher inferential value than adding more direct-hit counters,
because it measures the downstream consequence of prefix-produced memo rather
than treating observed reuse as a proxy for that consequence.
