# 2026-11-14 class4-lane cost-78: 2 WIN7 certificates + sterile-heavy sweep

## Sweep (S6 `00000000020000003800000080000040`, cost-78, c4=3)

- **2 WIN7-D10 (bits 70, 116)** + 76 REFUTED-D10, 0 capped,
  294,967,960 nodes total. Foreground batches 13+15+16+17+17.
- Controls: pilot d6 5/5 = 5949; heaviest candidates 53/108 and both WIN7
  bits 70/116 re-run fresh, node-exact identical
  (14,092,446 / 12,669,509 / 5,129,117 / 9,562,415).
- 78 legal candidates re-derived by exact integer Bareiss (truelegal.py),
  matching the published edge cost 78.
- Record: `output/class4-lane-cost78-sweep-20261114.json`;
  raw batches: `class4-lane-cost78-raw-batch1..5-20261114.jsonl` (pushed per batch).

Operational: one environment reset hit mid-sweep (before any batch was pushed
in the first attempt; batches 1-4 of that attempt were lost locally). The
sweep was re-run cleanly from the start; cross-run node-exact agreement was
observed for bits 21/48/78 before/after the reset. Batches are now pushed to
main immediately on completion (durability protocol already used by the
class-2 lane).

## WIN7 certificates (independently verified, on main)

| bit | root | sub-roots | rows | extraction nodes | md5 |
|----|------|-----------|------|------------------|-----|
| 70 | 00000000020000403800000080000040 | 60 | 51,058 | 12,060,637 | 696cad4a710d9650f8efd9096aeaea6e |
| 116 | 00100000020000003800000080000040 | 62 | 52,068 | 19,741,688 | 31e5f483d21f59866712ae766bef55a6 |

Total 103,126 rows, 31,802,325 extraction nodes, fbt_drops=0, fatal=null.
All sub-roots verified PASS by `verify_bit7_win7_cert.ts` (engine-independent
exact Bareiss det4), union diff 0/0, terminal range [13,17]. bit116 was
extracted twice in separate processes with identical row sets (diff 0).
Both remote files verified md5-identical to local via commit-pinned raw fetch
(trailing newline intact this time).

Certificates in `output/class4-lane-cost78-certificates/`, record:
`output/class4-lane-cost78-win7-certificates-20261114.json`.

Interpretation guard: each certificate proves only a winner win within depth 10
from the individual 7-stone root (loser to move). **No statement about the S5/S6
orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board — all
remain UNKNOWN.**

## Next

- Remaining unswept class-4 child of the same S5: cost-78
  `00000000020000003800001080000000` (cost-78 band, second child).
- Frontier recomputation over the cost-74b (6) + cost-78 (2) WIN7 covers is
  pending; needs the latest frontier receipt set from main.
