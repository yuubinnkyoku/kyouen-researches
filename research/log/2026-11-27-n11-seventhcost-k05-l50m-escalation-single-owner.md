# seventh-cost k05 L50M escalation - single-owner declaration (2026-11-27)

Lane: long-term lane (11x11), autonomous session; the user's PC was
unreachable this session (GitHub API publishing only). The seventh-cost
ladder checkpoint (waves 928dc19b / 64a46b4c / 24f40b8b, checkpoint log
03b954e9) pre-registered the parked key k05
`1152921504607932416:536870912` as the L50M escalation candidate. The
seventh-cost lane itself listed the C++ scrutiny gate and the
third-implementation corroboration as its next Parts; this declaration
claims ONLY the k05 L50M escalation so the two efforts cannot collide.
Any concurrent lane that sees this declaration must stand down on k05.

## Pre-registered execution plan (publish-then-execute)

- Target: k05 `1152921504607932416:536870912`, legal 90, coverage-relevant
  key of the seventh-cost exclusive selection (selection JSON sha256
  c395fe03..., canonical head basis 42dbb58f...).
- Instrument: the published byte-clone `scripts/jsreplay.js`
  (sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df,
  git blob 12eac695) - verified byte-identical on this host before the run.
- Input: `input/k05.input.csv` (sha256
  a73a6c70a221619b94ce29c188434d24a1f8af43653b37c1019a3286ba2ddb91, git blob
  db9a2753) - byte-identical fetch verified.
- Stage: at50m, budget 50,000,000 (the pre-registered ladder escalation
  budget; the pre-published pre-audit instrument already gates at50m*
  stage budgets).
- Cold determinism pair: two fresh cold runs (`at50m-run1`, `at50m-run2`),
  each a fresh solver (empty PnTT), node counts must be identical for a
  resolution; result 0 with nodes==budget means parked UNKNOWN@50M.
- Host validation BEFORE this declaration was pushed: the published val-gate
  reproduced 4/4 node-exact on this host (2M x2 result 0 / nodes 2000000;
  15M x2 result 2 / nodes 3651923 and 5040200), jsreplay sha pinned above.
- Prerequisite gate (pre-registered stage policy): k05 has a published 2M
  UNKNOWN (at2m-k05) and a published 15M UNKNOWN cold pair
  (at15m-run1/run2-k05, nodes 15,000,000 both) - the 50M stage is legal only
  after a 15M UNKNOWN, which is satisfied by the published raws.
- Raw naming: `output/raw/at50m-run1-k05.out.csv` and
  `output/raw/at50m-run2-k05.out.csv` in the seventh-cost kit
  `research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/`,
  following the existing at15m-run* pattern.

## Stopping rules (pre-registered, unchanged)

- result 2 at 50M with an identical cold pair: k05 becomes a loss-resolved
  row of the batch (single implementation; the C++ gate and
  third-implementation corroboration remain separate future Parts before
  any adoption).
- result 0 at 50M in both runs: k05 remains parked UNKNOWN@50M; no further
  escalation is implied or claimed by this Part.
- No WIN expectation is claimed; nodes are bookkeeping only.

## Status guard

Nothing here claims, implies or consumes any verdict. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class:
UNKNOWN unless a published Part says otherwise.
