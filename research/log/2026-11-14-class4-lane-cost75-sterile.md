# 2026-11-14 class4-lane cost-75: sterile child (4th)

## Sweep

S6 `00000000020000003800020080000000` (cost-75, c4=3 demand), the next
cheapest unswept S6 child of the best class-4 blocker-candidate S5
`00000000020000003800000080000000` after cost-73/74a/74b.

- **75/75 candidates REFUTED-D10, 0 WIN7, 0 capped** — no depth<=10 WIN7 exists
  from any root in this child. **Sterile child (4th**, after cost-73, cost-74a,
  and the cost-74b-`88000000` family**)**. Frontier impact: none (its c4 demand
  must be covered through other roots' certificates).
- 274,758,378 nodes total. Foreground batches 13+13+16+16+17.
- Controls: pilot d6 5/5 = 5949; heaviest candidate bit86 (9,051,336 nodes)
  re-run fresh in a separate process, node-exact identical.
- Candidate enumeration: 75 legal moves re-derived independently by exact
  integer Bareiss (truelegal.py protocol; matches the published edge cost 75).
  This child has 6 occupied stones, so the pre-fix legal_candidates.py
  enumeration was already correct for it.
- Record: `output/class4-lane-cost75-sweep-20261114.json`,
  raw: `output/class4-lane-cost75-raw-20261114.jsonl`
  (md5 98e080c1109e36359aea577978d87353, remote-verified).

Interpretation guard: REFUTED-D10 is only the negation of a winner win within
depth 10 from each 7-stone root (loser to move). **No statement about deeper
play, the S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11
empty board — all remain UNKNOWN.**

## Next

- Next cheapest unswept class-4 children: cost-78
  `00000000020000003800000080000040` and
  `00000000020000003800001080000000`.
- The cost-74b 6 WIN7 certificates' frontier recomputation is still pending
  (needs the latest frontier receipt set from main).
