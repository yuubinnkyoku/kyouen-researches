# 9x9 fixed-rule provenance audit

Date: 2026-09-23

## Finding

Do not use the historical `b5172a4` first-LOSS positions as evidence about the
geometric immediate-gain / candidate-conflict-degree heuristic.

Two different objects are currently adjacent in the research trail:

1. `docs/10X10_PROBE_BLIND_VALIDATION.md` defines the historical 3-stone fixed
   rule as **final memo used, descending, after a 1,000,000-visited probe**.
2. `docs/9X9_TWO_STONE_PROBE_RESEARCH_NOTES.md` develops a geometric heuristic
   where, for a 3-stone parent, immediate gain equals candidate-conflict degree
   exactly, and analyzes the large historical counterexamples `4,9,33` and
   `9,19,33` through that geometry.

Those analyses can describe the geometry of the same parents, but they do not
by themselves explain why the historical *memo-probe* ordering put the first
LOSS at positions 16 and 13.

There is a second, stronger provenance problem already recorded in
`docs/BLIND_PROBE_FRESHNESS_AUDIT.md`: the historical probe runner reused one
solver across children.  Its absolute memo count therefore accumulated roughly
1M per row, so sorting memo descending mostly reversed input order.  That audit
explicitly says `b5172a4` is not a valid blind validation of an independently
measured `memo desc @ 1M` rule.

## Consequence

The following quantities remain valid as an audit trail for the historical
batch0 run, but should not be used as predictive evidence for either a fresh
memo probe or the geometric gain heuristic:

- fixed first-LOSS median 3.0;
- random median 6.0;
- solver-default median 3.0;
- the 16 / 13 historical positions for `4,9,33` / `9,19,33`;
- verdict C attached to that historical ordering.

The exact child WIN/LOSS outcomes themselves remain useful; the confound is in
the probe-derived ordering.

## Frozen separation for future work

Keep three labels distinct in every later table:

- `historical_cumulative_memo_order`: the `b5172a4` ordering, audit only;
- `fresh_memo_order`: one fresh solver process per child, as required by
  `BLIND_PROBE_FRESHNESS_AUDIT.md`;
- `geometric_gain_order`: exact 3->4 immediate unique-gain / conflict-degree
  ordering, with its own tie rule fixed before evaluating outcomes.

Do not transfer a success/failure position from one label to another.

## Priority change

Before adding more post-hoc structure to the two large historical
counterexamples, the highest-value experiment is the already-frozen fresh
solver rerun on the same seven parents.  If fresh memo ordering reproduces the
same two failures, their geometry becomes relevant to explaining a real
memo-probe failure.  If it does not, the 16/13 examples should be treated as
artifacts of the cumulative-memo ordering and geometric modeling should be
validated independently against `geometric_gain_order`.

This audit changes no outcomes and introduces no new success threshold; it only
prevents causal/predictive claims from crossing between differently defined
orderings.
