# 2026-11-14 n11 class2 cost-56a WIN7 certificate: independent BigInt audit

Audit base: main = ea5061d6fd33574345927451c05ea64f08890bed.

The latest main commit adds the strategy certificate for root
00000000020000803202020000000000 (the cost-56 S6 child
00000000000000803202020000000000 plus bit 89). The certificate was not
accompanied by a verification manifest or run log, so this audit supplies an
independent record before using it in the shared receipt set.

## Independent verification

Source certificate:

- Path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost56a-certificates/bit89-root-00000000020000803202020000000000.cert
- Git blob SHA-1: 74d0b7dcbdc10bd01cbb3f069602de0be3bb07ab
- 1,004,863 bytes; 27,819 nonempty lines; 27,817 strategy rows.
- Header: n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS.

The verification core was run in a separate V8 execution context without importing
the search engine or repository verifier. Geometry used a BigInt 3x3-minor
Laplace expansion of det([x^2+y^2,x,y,1]), rather than the repository
verifier's Number/Bareiss implementation. No floating point or verdict cache was
used. The checker recomputed legal moves from all triples, enumerated every
opponent reply, checked every winner move, and compared the union of consumed
winner states with the complete strategy-row set.

Results:

- Root: 7 stones; all 35 four-point subsets pass the exact determinant safety check.
- Root loser mobility: 43; all 43/43 eight-stone sub-roots PASS.
- Sum of visited states across the 43 sub-root traversals: 68,320 (this is a
  per-sub-root sum, not a globally deduplicated state count).
- Winner-state visits: 44,609; unique consumed winner states: 27,817.
- Terminal leaves: 9,142; opponent edges: 65,546.
- Terminal stone range: 13–17.
- Strategy-row union: missing 0, extra 0.
- Exact geometry work: 12,812 distinct triples cached; 1,511,816 BigInt
  determinant evaluations.

The committed standalone Node script is
research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost56a_bigint_certificate.mjs.
It also recomputes the seven D4-canonical one-stone-deletion parents against the
six-stone milestone-5 manifest. The verification core above was executed in this
run; the checked-in Node CLI itself has not yet been run under Node 22 here.

## Six-stone parent lifts

Deleting each of the seven stones from the WIN7 root and D4-canonicalizing gives
three parents in the published S6 worklist:

| Winning move from parent | Canonical S6 parent | Worklist cost | Class |
|---:|---|---:|---:|
| 41 | 00000000000000803202000000800000 | 63 | 2 |
| 61 | 00000000000080809002000080000000 | 63 | 2 |
| 89 | 00000000000000803202020000000000 | 56 | 2 |

The other four deletion parents are not entries in the published S6 worklist.
For each listed parent, the removed stone is a legal move to the certified
seven-stone WIN7 root, so the parent is a first-player win. The cost-56 parent is
the cheapest unswept child of S5
00000000000000803202000000000000; the after-cost-62a frontier still lists that
S5 with 41 remaining S6 orbits and edge cost 2,776. This certificate removes
that one child locally: 41 -> 40 orbits and 2,776 -> 2,720.

The two cost-63 parents are additional worklist incidences, but their marginal
status has not been compared against the complete existing receipt union. They
are not counted as new closures here.

## Frontier and interpretation guard

A subsequent full manifest-level recomputation,
class-frontier-cost56a-recompute-20261114.json, has now incorporated this
receipt. It confirms that all three S6 worklist parent lifts listed above are
marginal. The global frontier moves from the after-cost-62a baseline
(924 solved-in-manifest, 6,923 remaining S6 orbits, cost 544,799) to
**927 solved-in-manifest, 6,920 remaining S6 orbits, cost 544,617**;
open-class demand falls from 5,193 / 408,522 to **5,190 / 408,340**.
For S5 00000000000000803202000000000000, two covered children (costs 56 and 63)
reduce the local remaining count from 41 / 2,776 to **39 / 2,657**. The third
cost-63 parent contributes to another worklist parent.

This is a verified WIN7 root and local S6 first-player wins, not a verdict for
any five-stone parent. Standard 11x11 empty root, two-stone root {49,60},
S2 {59,60}, class 2, and class 4 remain UNKNOWN.

## Artifacts

- Certificate: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost56a-certificates/bit89-root-00000000020000803202020000000000.cert
- Independent verifier: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost56a_bigint_certificate.mjs
- Machine-readable result: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost56a-independent-audit-20261114.json
- Global frontier recomputation: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost56a-recompute-20261114.json
- Frontier reproduction script: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost56a_20261114.py
