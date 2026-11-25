# n11 class2-lane: cost-70c sweep complete (13 WIN7-D10 + 57 REFUTED), 3 verified certificates, frontier 1019 → 1022; after-cost-69e CSV defect found and superseded

Long-term lane session (2026-11-15 JST), continuing after the merged frontier
(1012, commit a7f3fc97) and chained on the parallel lane's completed cost-69e
records (after-cost-69e frontier solved 1019 / unique remaining 6,828 / sum
538,143 / open 5,098/401,866, commits 53102729..7cec3e7e, d92f6479).

## Sweep

Child `00000000000000803242000000000000` (cost 70, demand c1=0,c2=2,c4=0),
claimed at the merged 1012 state as the cheapest remaining unswept child of
the second class-2 target (7 orbits / 513; claim commit fee1a57b, membership
re-verified before the claim per the cost-61e lesson).

- legal_candidates.py independent Bareiss 4x4 enumeration: 70 candidates,
  bit-exact with the published edge cost 70.
- Sweep complete: **13 WIN7-D10 (bits 3,8,11,20,23,24,40,42,86,92,94,103,105)
  + 57 REFUTED + 0 capped, 100,935,666 v16 nodes**, all 9 batch pilots
  loss=false at exactly 3,402 nodes.
- Determinism rerun node-exact: bit 86 (WIN7, 6,414,891), bit 66 (heaviest
  REFUTED, 8,291,296). v15 cross-engine anchors on **all 13** WIN7 bits:
  loss=true (heaviest 86 at 17,475,934 v15 nodes), pilot 5,949 ×2.

## Mid-flight manifest closure

While the sweep was in flight, the parallel cost-69e lane published its warm
rebuild certificates and recompute v2: the cost-69e warm bit-76 receipt (root
`00000000000010803202000000008000`) closed this child in the manifest (its
marginal_manifest included `00000000000000803242000000000000`). As with
cost-69e itself, the claim was correct in the state where it was made and the
sweep completed on an already-receipt-closed child; its certificates are pure
new-coverage additions.

## Certificates (bits 94/20/23)

Three certificates extracted (cheapest-first) and fully verified
(root-check stones=7 + loser mobility vs independent enumeration, all
sub-roots PASS, union missing/extra 0/0, rows sorted unique):

- bit 94: root `00000000400000803242000000000000`, 20,527 rows,
  1,593,393 extraction nodes, 46 loser moves.
- bit 20: root `00000000000000803242000000100000`, 32,576 rows,
  4,065,298 extraction nodes, 52 loser moves.
- bit 23: root `00000000000000803242000000800000`, 33,954 rows,
  3,763,880 extraction nodes, 54 loser moves.

All three also pass the repo-published **independent BigInt verifier**
(`verify_win7_certificate_bigint_independent.mjs`, BigInt 3x3 cofactor
expansion, no solver/cache/repo-verifier import; added by the parallel lane in
commits d98eec68/c0882013): root safe, rows sorted unique, all sub-roots
passed, union 0/0 (class2-lane-cost70c-bigint-independent-audit-20261115.json).

Duplicate-root check (GitHub code search over the repo, all 13 WIN7 roots):
12 roots 0 hits; the bit-20 root duplicates the cost-64b bit-54 win7_roots
listing but had no prior published certificate (cost-64b certified bits
73/7/99 only) — new coverage, and it also closes the cost-64b bit-54 warm
entry.

The remaining 10 WIN7 bits (3/8/11/24/40/42/86/92/103/105) stay warm
certificate-rebuild candidates; all 13 verdicts are v15-anchored.

## Frontier recompute

`recompute_frontier_cost70c_20261115.py` reproduces the after-cost-69e
baseline by runpy (asserted 1019/6828/538143/5098/401866), re-derives the
child membership, asserts the sweep from the published raw batches, and adds
the three receipts with per-bit marginals re-derived from the growing union:

- bit 94: covers 7, marginal 4 (in-manifest 1: `00000000000000849002000004000000`)
- bit 20: covers 7, marginal 4 (in-manifest 1: `00000000000000801242000000100000`)
- bit 23: covers 7, marginal 5 (in-manifest 1: `00000000000000801242000000800000`)

**After cost-70c: solved 1022 / unique remaining 6,825 / sum 537,921 / open
5,095/401,644.** Two runs byte-identical.

## Record defect found in the published after-cost-69e outputs

The published `class-frontier-top-candidates-s6-after-cost69e-20261115.csv`
was generated with `rem69[int(...)]` lookups against the string-keyed
remaining defaultdict, so **all four of its data sections are empty** and its
audit-blocked line reads remaining=0 cost=0 (real values: 10/698, matching
the uncoverability audit). The cost-69e script's own child-membership control
was vacuous for the same reason (its conclusion — the child was closed
mid-flight — is nonetheless correct and is re-verified with string keys in
this recompute). The new after-cost-70c top-candidates CSV supersedes it with
correct sections. The JSON record's frontier numbers are unaffected (they
never used the buggy lookups).

## Ranking effect / next targets

The second class-2 target S5 `00000000000000803202000000000000` stays at
**6 remaining S6 orbits / 443 edge cost**, still the smallest class-2 target.
Its 6 remaining children were each checked against all published sweep
records: **none has been swept** (no sweep record lists them), so the target
remains receipt-coverable. Cheapest next children:

- cost-71 `00000000000000803202000000400000` (demand c1=0,c2=2,c4=0)
- cost-72 `00000000000000803202000000000200`
- cost-75 band: `00000000000000803202000000000008`,
  `00000000000000803202000000000010`,
  `00000000000000803202000000004000`,
  `00000000000000803202000100000000`

The audit-blocked S5 `00000000000000809082000000000000` (classes 3) holds at
10 orbits / 698 (all remaining children sterile-swept; receipt-unclosable).
Best class-4 unchanged (18 orbits / 1,460).

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. WIN7 certificates prove a win within depth 10 from the
  individual 7-stone roots only; REFUTED-D10 sweeps prove only the absence of
  such a win in that subtree; this recompute is bookkeeping over published
  receipts and proves no new game outcome.
