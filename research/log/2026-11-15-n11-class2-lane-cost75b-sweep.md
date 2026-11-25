# n11 class2-lane: cost-75b sweep complete (7 WIN7-D10 + 68 REFUTED), all 7 candidates certified; frontier 1045 → 1049; parent S5 down to 2 orbits / 147

Long-term lane session (2026-11-15 JST), continuing after the merged
cost-60bwarm+cost-71b frontier recompute (1045, baseline commit ada63968)
and the inflight claim (commit 8cba4498).

## Sweep

Child `00000000000000803202000000000008` (cost 75, demand c1=0,c2=2,c4=0),
one of the three remaining unswept children of the second class-2 target
(parent at 3 orbits / 222 after the merged frontier; membership and demand
re-verified before the claim). The child was genuinely still remaining when
swept — no mid-flight closure.

- legal_candidates.py independent Bareiss 4x4 enumeration: 75 candidates,
  bit-exact with the published edge cost 75 (named cost-75b; the sibling
  cost-75 child `...04000` of the same parent remains unswept).
- Sweep complete: **7 WIN7-D10 (bits 7,51,54,84,89,99,116) + 68 REFUTED +
  0 capped, 139,705,045 v16 nodes**, all 10 batch pilots loss=false at
  exactly 3,402 nodes.
- Determinism rerun node-exact: bit 7 (lightest WIN7, 2,971,923), bit 86
  (heaviest REFUTED, 10,402,959), bit 116 (heaviest WIN7, 10,699,729).
  v15 cross-engine anchors on **all 7** WIN7 bits: loss=true at
  5,462,984 / 3,050,228 / 8,568,846 / 9,025,519 / 5,605,094 / 3,953,206 /
  18,631,277 v15 nodes, pilots 5,949.

## Certificates (all 7 WIN7 candidates)

All seven extracted and fully verified (root-check stones=7 with loser
mobility = independent enumeration, all sub-roots PASS, union 0/0, rows
sorted unique) — every certificate also passes the independent BigInt
cofactor-expansion verifier, re-run PASS on the remote-rejoined bytes after
landing. Total 352,672 strategy rows / 80,915,182 extraction nodes:

- bit 7: root `00000000000000803202000000000088`, 47,257 rows, 8,706,242
  extraction nodes, 57 loser moves (2-part split).
- bit 51: root `0000000000000080320a000000000008`, 32,508 rows, 4,703,026,
  51 loser moves (single file).
- bit 54: root `00000000000000803242000000000008`, 50,955 rows, 11,537,642,
  63 loser moves (2-part split).
- bit 84: root `00000000001000803202000000000008`, 55,484 rows, 13,021,801,
  61 loser moves (2-part split).
- bit 89: root `00000000020000803202000000000008`, 45,501 rows, 8,793,296,
  55 loser moves (2-part split).
- bit 99: root `00000008000000803202000000000008`, 40,056 rows, 6,172,262,
  55 loser moves (2-part split).
- bit 116: root `00100000000000803202000000000008`, 80,911 rows, 27,980,913,
  64 loser moves (2-part split).

**unverified_win7_bits is empty** — the first sweep in this series published
with every WIN7-D10 candidate certified at record time. The bit-7 extraction
was additionally re-run fresh in this session and reproduced the raw
certificate byte-for-byte (extraction-order identical; sorted output md5
`2e20e75c305962b4bc46045185778d14`).

**Duplicate-fold:** the bit-54 root duplicates the cost-70c bit-3
win7_roots listing (cost-70c certified bits 94/20/23 only, no prior
certificate for this root). This is the first published certificate for the
root and it closes the cost-70c bit-3 warm entry. The other six roots had
0 code-search hits.

## Frontier recompute

`recompute_frontier_cost75b_20261115.py` reproduces the after-merged
baseline by runpy (asserted 1045/6802/536131/5072/399854), asserts the
sweep from the 10 published raw batches (nodes/pilots/heaviest bits), the
determinism and v15 control JSONLs, and all seven receipts
(rows/sub-roots/extraction-nodes/union/md5/roots), then adds them in the
published record order with per-bit marginals re-derived from the growing
union:

- bit 7: covers 7, marginal 5 (in-manifest 1: the child
  `00000000000000803202000000000008` itself)
- bit 51: covers 7, marginal 4 (in-manifest 0)
- bit 54: covers 7, marginal 4 (in-manifest 0)
- bit 84: covers 7, marginal 5 (in-manifest 1:
  `00000000000100003800080008000000`)
- bit 89: covers 7, marginal 5 (in-manifest 1:
  `00000000000000003800000208080000`)
- bit 99: covers 7, marginal 4 (in-manifest 0)
- bit 116: covers 7, marginal 5 (in-manifest 1:
  `00000000000000043800080008000000`)

**After cost-75b: solved 1049 / unique remaining 6,798 / sum 535,812 /
open 5,068/399,535.** The cost-75b child is closed by its own receipts
(covered by all 7 bits; the bit-7 receipt claims the marginal). Two runs
byte-identical (recompute JSON + both CSVs + full logs).

## Ranking effect / next targets

The second class-2 target S5 `00000000000000803202000000000000` drops to
**2 remaining S6 orbits / 147 edge cost**: the parallel-lane cost-72 child
`00000000000000803202000000000200` (in flight; raw batches + bit-111
certificate published, no completed record yet — certificates without
records are not receipts) and the sibling cost-75 child
`00000000000000803202000000004000`, both demand c1=0,c2=2,c4=0. The
audit-blocked S5 `00000000000000809082000000000000` holds at 10/698. Best
class-4 unchanged (18/1,460).

Warm entries closed by this session: cost-70c bit-3 (bit-54 root). Warm
rebuild candidates still outstanding: cost-61d bit-22 (= cost-71b bit-1
root), cost-71b remaining WIN7 bits 1/14/32/74/94/117, and other
unverified WIN7 bits of earlier bands.

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. WIN7 certificates prove a win within depth 10 from the
  individual 7-stone roots only; REFUTED-D10 sweeps prove only the absence
  of such a win in that subtree; this recompute is bookkeeping over
  published receipts and proves no new game outcome.
