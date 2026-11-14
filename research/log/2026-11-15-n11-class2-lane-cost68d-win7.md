# n11 class2-lane: cost-68d sweep complete (7 WIN7-D10 + 61 REFUTED), all 7 candidates certified; warm band hygiene batch (62a complete 11/11, 63a 8/10, 71b bit-1); frontier 1109 → 1117

Long-term lane session (2026-11-15 JST), continuing after the warm multiband
frontier recompute (chain head 1109/6738/531295/5008/395018,
`class-frontier-warm-multiband-recompute-20261115.json`) and the cost-68d
inflight claim (commit 6175d233, remote md5 verified). The parallel lane was
running the warm multiband batch-2 certificate push, so this lane took the
cost-68d sweep plus the warm band hygiene receipts instead of competing for
the same greedy-40 candidates.

## Sweep

Child `00000000000000809122000000000000` (cost 68, demand c1=0,c2=2,c4=0),
the cheapest remaining unswept child of the third class-2 coverable target
S5 `00000000000000809102000000000000`. Membership and demand were verified
before the claim in both post-batch-2 fold scenarios (all-greedy-40 and
self-29-only); the child was genuinely still remaining when swept.

- legal_candidates.py independent Bareiss 4x4 enumeration: 68 candidates,
  bit-exact with the published edge cost 68.
- Sweep complete: **7 WIN7-D10 (bits 18, 26, 29, 34, 47, 103, 108) +
  61 REFUTED + 0 capped, 61,325,518 v16 nodes**, all 10 batch pilots
  (9 batches + the determinism rerun invocation) loss=false at exactly
  3,402 nodes.
- Determinism rerun node-exact: batch1's 8 candidates (bits 0,1,2,3,4,6,
  7,9) were accidentally run twice through a batch-numbering slip; the
  duplicate invocation is byte-identical per line on every search-result
  field (only wall-clock `ms` differs) and is preserved as
  `class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl` (10th identical
  pilot control included). The original raw-batch2..10 files were renumbered
  to raw-batch2..9; no data was lost or rewritten.
- v15 cross-engine anchors on **all 7** WIN7 bits: loss=true at
  12,656,791 (bit 18) / 9,249,234 (26) / 5,720,958 (29) / 9,724,149 (34) /
  4,112,662 (47) / 4,220,738 (103) / 2,528,832 (108) v15 nodes, pilots
  5,949. Refuted anchors bits 0 / 120 / 13 (lightest, mid, heaviest
  REFUTED): loss=false at 5,225,527 / 1,124,734 / 16,699,066.

## Certificates (all 7 WIN7 candidates)

All seven extracted with the repo-verbatim blind extractor (empty kill
table, FBS=1<<20, fbt_drops=0, rows LC_ALL=C sorted-unique) and fully
verified (root-check stones=7 with loser mobility = independent enumeration,
all sub-roots PASS, union 0/0, rows sorted unique) — every certificate also
passes the independent BigInt cofactor-expansion verifier. Total 268,572
strategy rows / 82,180,565 extraction nodes:

- bit 18: root `00000000000000809122000000040000`, 56,442 rows, 22,442,960
  extraction nodes, 60 loser moves (2-part split, joined md5
  8aeaf2b687bc033bbbdab2781d91471c).
- bit 26: root `00000000000000809122000004000000`, 40,031 rows, 17,544,277,
  51 loser moves.
- bit 29: root `00000000000000809122000020000000`, 34,356 rows, 8,861,104,
  52 loser moves.
- bit 34: root `00000000000000809122000400000000`, 49,328 rows, 15,777,994,
  61 loser moves.
- bit 47: root `00000000000000809122800000000000`, 29,618 rows, 6,423,355,
  51 loser moves.
- bit 103: root `00000080000000809122000000000000`, 31,183 rows, 6,704,119,
  53 loser moves.
- bit 108: root `00001000000000809122000000000000`, 27,614 rows, 4,426,756,
  53 loser moves.

GitHub code search before the push: 0 hits for all 7 root hexes (no prior
certificate anywhere in the repo). Every pushed file was verified byte-exact
on the remote by its git blob sha.

## Warm band hygiene batch (6 receipts, frontier-invariant)

Certificate gaps left open by the batch-1 warm multiband push and the
parallel-lane pushes, extracted and verified the same way (marginal 4 per
receipt, marginal_in_manifest 0 — no frontier number changes; ledger
hygiene only):

- cost-62a bit 1: root `00000000000000809102000001000002`, 55,447 rows,
  17,549,688 nodes, 55 loser moves (2-part split). With bit 89 this
  **completes the cost-62a band: 11/11 WIN7 bits certified**.
- cost-62a bit 89: root `00000000020000809102000001000000`, 32,471 rows,
  6,191,788 nodes, 50 loser moves.
- cost-63a bit 11: root `00000000000000809102000800000800`, 24,243 rows,
  7,160,965 nodes, 45 loser moves. cost-63a moves to **8/10** (bits 96/97
  remain claimed by the parallel lane).
- cost-63a bit 109: root `00002000000000809102000800000000`, 38,853 rows,
  14,320,132 nodes, 52 loser moves.
- cost-71b bit 1: root `00000000000000803202000000400002`, 42,499 rows,
  7,256,121 nodes, 51 loser moves. Closes the first item of the parallel
  lane's cost-71b remaining_win7_bits list [1,14,32,74,94,117]; with the
  batch-1 bits 14/32 and the parallel bits 109/21/105, cost-71b is 6/9
  (74/94/117 remain).
- cost-61d bit 22: the same root re-extracted independently —
  **byte-identical md5** (positive cross-child duplicate cross-check); the
  certificate is pushed once under cost-71b and serves both listings.

## Frontier recompute

`recompute_frontier_cost68d_20261115.py` reproduces the 1109 chain head by
runpy (byte-identical), re-derives the cost-68d child membership and demand
with string keys, re-sums the sweep from the 9 published raw batches,
asserts the determinism rerun and the v15 anchors, then folds the 13
receipts in published record order. Output byte-identical across two runs.

New chain head: **solved S6 1,117 / unique remaining 6,730 / remaining cost
530,739 / open demand 5,000 / 394,462** (was 1109/6738/531295/5008/395018).
Total marginal 56, of which 8 in manifest — all 8 from the cost-68d
receipts (the child orbit itself plus 7 further manifest orbits: two in the
bit-18 receipt, one each in 29/34/103/108, two in 47); the 6 hygiene
receipts contribute marginal 20 outside the manifest (mim 0) and the 61d
duplicate contributes 0 by construction.

The third class-2 coverable target S5 `00000000000000809102000000000000`
drops from 17 remaining orbits / cost 1,220 to **13 orbits / 937**.
Bottlenecks unchanged: audit-blocked class-2
`00000000000000809082000000000000` (10 orbits / 698, receipt-unclosable) and
class-4 `00000000020000003800000080000000` (18 / 1,460). The parallel
batch-2 certificates pushed since 19:49Z are not folded here and stay with
the parallel lane's fold.

Artifacts: [sweep record](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68d-sweep-20261115.json),
[certificate manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68d-win7-certificates-20261115.json),
[hygiene manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-warm-band-hygiene-certificates-20261115.json),
[frontier recompute](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost68d-recompute-20261115.json),
[recompute script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost68d_20261115.py).

Session notes: two pushes tripped the execution sandbox memory limit after
the GitHub write had already landed (bit-34 and 71b bit-1) — both were
verified byte-exact on the remote by git blob sha rather than re-pushed;
one fast-forward conflict (concurrent seven-row lane commits) was retried
successfully after re-fetching main.

Interpretation guard: solved counts measure manifest coverage, not the
game-theoretic value of the 11x11 empty board. REFUTED-D10 sweeps prove only
the absence of WIN7-D10 candidates; WIN7 certificates prove a win within
depth 10 from the individual 7-stone root only. **The 11x11 empty board,
the two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all remain
UNKNOWN.**
