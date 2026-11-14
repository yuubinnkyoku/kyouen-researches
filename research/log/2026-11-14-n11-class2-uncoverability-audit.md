# n11 class2-lane: uncoverability audit — the best class-2 S5 target is receipt-unclosable (all 10 remaining children sterile-swept)

Session 11 continuation. Starting point: the after-cost-73a frontier (solved 921 /
unique remaining 6,926 / sum 544,995 / open 5,196/408,718; best class-2 S5
`00000000000000809082000000000000` at 10 remaining orbits / 698), pushed and
verified earlier in this session. No newer class-2 frontier state exists on main;
the parallel class4-lane was mid-flight on cost-86c (raw batches up to 55/86, all
REFUTED-D10 so far — an in-flight sweep, not a verdict).

## Motivation

The cost-73 band (73a takeover with WIN7 bit81, then 73b/73c/73d/73e/74 from
parallel sessions) left the best class-2 S5 with only swept children. A completed
sweep of an S6 child enumerates **all** legal S7 candidates of that child
(bit-exact enumeration asserted in every published sweep record) and resolves each
at depth 10. If such a sweep ends 0 WIN7-D10 and 0 capped, then every possible
WIN7-D10 receipt root for that S6 orbit has been individually refuted at depth 10:
**no future WIN7-D10 receipt can ever cover that orbit.** If ALL remaining
children of an S5 are in that state, the S5 can never reach 0 remaining inside
the WIN7-D10 receipt framework — it is *receipt-unclosable*, and further sweeps
aimed at it are wasted compute. This audit makes that structural claim rigorous
and machine-checked instead of anecdotal.

## Method

`scripts/audit_uncoverability_20261114.py` (pushed with this log):

1. Reproduces the after-cost-73a frontier first (runpy of
   `recompute_frontier_cost73a_20261114.py`; every published staged control is
   asserted inside it, including after-cost73d 920/6,927/545,068 and
   after-cost73a 921/6,926/544,995/5,196/408,718).
2. Builds a sweep map from all 49 published class2/class4-lane sweep records
   (both old and new record schemas; duplicate sweeps of the same child must
   agree on sterility or the audit aborts).
3. Classifies every remaining S6 child of the best class-2 and best class-4 S5
   as sterile-swept (permanently uncoverable) or unswept (still coverable).
   A remaining orbit claimed by a swept child that produced WIN7 would abort
   the audit (the frontier recompute would already have covered it) — that
   consistency assertion passes.
4. Emits a coverable-child inventory for the next 12 class-2 targets.

Determinism: two consecutive runs produce a byte-identical JSON (md5
`8d18411f504ac63a787d562e2a30aca7`).

## Result

- **Best class-2 S5 `00000000000000809082000000000000`: 10 remaining = 10
  sterile-swept + 0 unswept.** Each of the 10 is tied to a published sterile
  sweep record (cost70, 73b, 73c, 65b, 69b, 66a, 66b, 74, 73e, 69d —
  see the audit JSON for the exact record/child/cost mapping; total unclosable
  cost 698 = exactly its remaining edge cost). **Conclusion: this S5 is
  receipt-unclosable and exhausted as a sweep target; the frontier ranking must
  treat it as blocked, not as the cheapest next move.** Class-2 progress within
  the receipt framework moves to the next S5 candidate
  `00000000000000809102000000000000` (40 orbits / 2,850, cheapest unswept child
  cost 62: `00000000000000809102000001000000`), or outside it via a direct S5
  refutation (SECOND_WIN route).
- Best class-4 S5 `00000000020000003800000080000000`: 18 remaining = 12
  sterile-swept (unclosable cost 958) + 6 unswept (coverable; cheapest unswept
  cost 73, plus the cost-86 band where the class4-lane parallel is mid-flight on
  cost-86c). Still closable in principle, but 12 of its 18 children are already
  dead weight for it.
- Next class-2 targets all have 0 sterile children so far: 40 unswept (cost
  2,850), 41 (2,776), 56 (4,066), 58 (4,162), 59 (4,403) — full inventory with
  cheapest unswept child per target in the audit JSON.

## Status guard

Bookkeeping over published receipts and sweep records only; no new verdicts were
computed. REFUTED-D10 is the absence of a winner win within depth 10 in that
subtree only. The 11x11 empty root, the two-stone root {49,60}, S2 {59,60},
class 2, and class 4 all remain **UNKNOWN**.

## Artifacts

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_uncoverability_20261114.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-uncoverability-audit-20261114.json`

