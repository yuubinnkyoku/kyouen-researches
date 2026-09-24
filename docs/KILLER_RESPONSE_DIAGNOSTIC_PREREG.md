# Killer-response diagnostic preregistration

Status: pre-data analysis plan. This file fixes the diagnostic before reading true response values for the seven blind-replication LOSS parents.

Provenance:

- branch: `probe-two-stone-subsets`
- blind-replication baseline: `b5172a4`
- preregistration parent HEAD: `a367b5764029de0b1838298b3306e7ace253fcab`
- semantic correction (pre-data): the blind fixed rule is the frozen **probe-score rule**, not immediate unique gain; the response-side gain ordering below is a separate diagnostic ordering
- blind LOSS parents: `2,9,33`, `4,9,33`, `9,12,33`, `9,19,33`, `9,23,33`, `0,31,36`, `0,36,44`

The two previously inspected maximum counterexamples (`4,9,33`, `9,19,33`) are calibration examples only. They must not be counted as fresh confirmation of any hypothesis below.

## Question

The frozen blind fixed rule ranks children by its preregistered probe score (for three-stone parents: final memo used at the 1,000,000-visited probe budget, descending, with the frozen tie-break). Some moves selected by that rule are nevertheless losing. The diagnostic tests a narrower downstream mechanism:

> after the frozen probe rule has selected a losing move, is that loss caused by one or a few opponent responses that look locally weak under an independent immediate-unique-gain ordering but are true minimax killers?

This is deliberately different from an average-response-strength hypothesis, and it does **not** claim that immediate unique gain is the original fixed rule. A parent may have many weak-looking responses while only one of them matters to minimax value.

## State/value convention

For each blind LOSS parent `S`:

1. Let `v_fixed` be the move selected by the already frozen blind probe rule, including its existing deterministic tie-break and original batch concatenation semantics.
2. Let `S1 = S + v_fixed`. It is now the opponent's turn.
3. Enumerate every legal opponent response `r` from `S1`.
4. Let `S2 = S1 + r`. It is now the original player's turn.
5. Solve `S2` exactly with the existing certified solver semantics.
6. `r` is a **killer response** iff `S2` is `LOSS` for the player to move. Thus the opponent can choose `r` and leave the original player in a losing state.

No probe estimate, memo size, timeout label, or heuristic value may substitute for the exact/certified outcome in the primary diagnostic.

## Frozen response-side diagnostic ranking

The opponent responses are **not** rerun through the blind probe rule. For every legal response `r`, compute its exact immediate unique gain at `S1`: the number of currently safe next candidates made unsafe by playing `r`.

Primary diagnostic order is `(unique_gain descending, move index ascending)`. This ordering is frozen here solely to ask whether minimax killers are hidden below locally attractive opponent replies; it is not described as production fixed-rule order.

For robustness against arbitrary ordering inside equal-gain ties, also record the gain-only competition rank

`gain_rank(r) = 1 + count{q : gain(q) > gain(r)}`.

The primary `best_killer_rank` uses `(gain desc, move asc)`; `best_killer_gain_rank` uses the tie-invariant competition rank.

## Per-parent outputs

Record:

- `response_count`
- `killer_count`
- `killer_fraction = killer_count / response_count`
- `best_killer_rank = min diagnostic-order rank among killers`
- `best_killer_gain_rank = min gain_rank among killers`
- `top1_has_killer`, `top3_has_killer`, `top5_has_killer` under the frozen diagnostic order
- `top1_gain_tier_has_killer`, `top3_gain_tiers_has_killer`, `top5_gain_tiers_has_killer`
- gain distribution for killers and non-killers separately
- for every response: state, move, gain, diagnostic rank, gain rank, exact outcome

If `killer_count == 0`, the parent/value convention or upstream selected-move reconstruction is inconsistent with the claim that `v_fixed` loses; treat this as a hard audit failure, not as a zero-valued observation.

## Predeclared interpretation

The "locally weak killer" hypothesis is supported only if killers systematically appear below the top of the response-side local ordering. With only seven fresh parents, do not fit a threshold post hoc. Report the seven raw `best_killer_gain_rank` values and the count with `best_killer_gain_rank > 5`.

Strong falsification: all or nearly all fresh parents have a killer in the top gain tier or within gain-rank 1--3. In that case the failure is not hidden in locally weak responses; shallow adversarial checking of the obvious high-gain replies is the better next hypothesis.

Positive signal: multiple fresh parents have no killer within the top five gain ranks while still having at least one exact killer. Then the immediate-gain response ordering is specifically hiding minimax-critical replies, motivating top-k forceability / adversarial-width experiments.

Do not use the two already inspected maximum counterexamples to choose a new cutoff after seeing these results.

## Audit guards

Before accepting results:

- reproduce `v_fixed` from the frozen blind probe rule and its original stored probe rows for every parent; do not substitute unique gain for this reconstruction;
- verify every enumerated response is legal and the response set has no duplicates;
- verify exact outcomes are invariant under D4 canonicalization for a deterministic sample plus every killer state used in the summary;
- rerun at least one killer and one non-killer child per parent through the certified path independently of any shared memo process;
- retain raw per-response rows so summary statistics are reconstructible.

This diagnostic is observational within already selected losing moves. It identifies where minimax-critical responses sit in a deliberately separate local ranking; it does not by itself prove that changing response order improves the full solver or game-playing policy.