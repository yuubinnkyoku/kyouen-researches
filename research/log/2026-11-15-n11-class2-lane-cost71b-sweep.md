# n11 class2-lane: cost-71b sweep complete (9 WIN7-D10 + 62 REFUTED), the child closed by its own receipt; frontier 1022 → 1026; parent S5 down to 5 orbits / 372

Long-term lane session (2026-11-15 JST), continuing after the cost-70c frontier
(1022, commit 6f42af0d).

## Sweep

Child `00000000000000803202000000400000` (cost 71, demand c1=0,c2=2,c4=0),
claimed at the after-cost70c frontier as the cheapest remaining unswept child
of the second class-2 target (parent at 6 orbits / 443; membership re-verified
before the claim). Unlike cost-69e and cost-70c, **this child was genuinely
still remaining when swept** — no mid-flight closure.

- legal_candidates.py independent Bareiss 4x4 enumeration: 71 candidates,
  bit-exact with the published edge cost 71 (named cost-71b; cost-71 occupied
  by an earlier lane on another parent).
- Sweep complete: **9 WIN7-D10 (bits 1,14,21,32,74,94,105,109,117) + 62
  REFUTED + 0 capped, 87,586,636 v16 nodes**, all 9 batch pilots loss=false at
  exactly 3,402 nodes.
- Determinism rerun node-exact: bit 32 (heaviest WIN7, 8,488,319), bit 113
  (heaviest REFUTED, 9,070,237). v15 cross-engine anchors on **all 9** WIN7
  bits: loss=true (heaviest 32 at 18,454,344 v15 nodes), pilots 5,949 ×2.

## Certificates (bits 109/21/105)

Three certificates extracted (cheapest-first) and fully verified (root-check,
all sub-roots PASS, union 0/0, rows sorted unique) — and all three also pass
the repo-published **independent BigInt verifier**:

- bit 109: root `00002000000000803202000000400000`, 32,492 rows,
  5,123,247 extraction nodes, 51 loser moves.
- bit 21: root `00000000000000803202000000600000`, 29,242 rows,
  4,454,710 extraction nodes, 52 loser moves.
- bit 105: root `00000200000000803202000000400000`, 38,589 rows,
  5,374,108 extraction nodes, 54 loser moves.

**Cross-lane reproduction:** the bit-21 root duplicates the cost-60b bit-22
win7_roots listing, and the parallel lane independently warm-rebuilt that
exact certificate as cost-60b bit-22 (byte-identical file, md5
`0bca8499e98e1a0197db2a6f6bd2d6ab`) while this session was running — an
unplanned two-engine, two-lane reproduction of the same 7-stone root
certificate. The receipt enters the frontier here; the parallel cost-60b
bit-22 rebuild contributes 0 marginal by construction when folded into a
later recompute. The bit-1 root duplicates the cost-61d bit-22 listing (no
prior certificate; certified bits 30/74/94 only) — a warm-rebuild candidate
that would close the cost-61d bit-22 warm entry.

The remaining 6 WIN7 bits (1/14/32/74/94/117) stay warm certificate-rebuild
candidates; all 9 verdicts are v15-anchored.

## Frontier recompute

`recompute_frontier_cost71b_20261115.py` reproduces the after-cost-70c
baseline by runpy (asserted 1022/6825/537921/5095/401644), asserts the sweep
from the published raw batches, and adds the three receipts with per-bit
marginals re-derived from the growing union:

- bit 109: covers 7, marginal 6 (in-manifest 2: the child
  `00000000000000803202000000400000` itself and
  `00000000010000801202000000200000`)
- bit 21: covers 7, marginal 5 (in-manifest 1: `00000000000000801202000000600000`)
- bit 105: covers 7, marginal 5 (in-manifest 1: `00000000000000083800000008000100`)

**After cost-71b: solved 1026 / unique remaining 6,821 / sum 537,604 / open
5,091/401,327.** The cost-71b child is closed by its own bit-109 receipt —
the first sweep in this series whose target child was genuinely open at claim
time and is now closed (1022 + 4 = 1026). Two runs byte-identical.

## Ranking effect / next targets

The second class-2 target S5 `00000000000000803202000000000000` drops to
**5 remaining S6 orbits / 372 edge cost**: cost-72
`00000000000000803202000000000200` plus four cost-75 children
(`...00000008`, `...00000010`, `...00004000`, `...0100000000`), all demand
c1=0,c2=2,c4=0, none swept — the target remains receipt-coverable. The
audit-blocked S5 `00000000000000809082000000000000` holds at 10/698.
Best class-4 unchanged (18/1,460).

Outstanding receipts not yet in any frontier recompute (to be folded in a
later recompute by whoever runs it next): the parallel lane's cost-69e warm
bit-108 certificate and its growing set of cost-60b warm rebuilds (bits
22/106/87/100/108/32/114/43 published so far, all verified; bit-22 is the
same root as this session's cost-71b bit-21 and contributes 0 marginal
against the 1026 state).

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. WIN7 certificates prove a win within depth 10 from the
  individual 7-stone roots only; REFUTED-D10 sweeps prove only the absence of
  such a win in that subtree; this recompute is bookkeeping over published
  receipts and proves no new game outcome.
