# n11 class2-lane: cost-75c sweep complete (12 WIN7-D10 + 63 REFUTED), all 12 candidates certified; cost-72 bit-111 receipt folded; frontier 1049 → 1062; second class-2 target S5 fully closed

Long-term lane session (2026-11-15 JST), continuing after the cost-75b
frontier recompute (1049, commit c6941de2) and the cost-75c inflight claim
(commit f7a6d53b). Session note: the execution environment was reset twice
during the session; all artifacts were re-derived from the published raw
batches and every pushed certificate part was verified byte-exact on the
remote by its git blob sha (a stronger check than the raw-md5 route).

## Sweep

Child `00000000000000803202000000004000` (cost 75, demand c1=0,c2=2,c4=0),
one of the two remaining unswept children of the second class-2 target
(parent at 2 orbits / 147 after the cost-75b frontier; membership and
demand re-verified before the claim). The child was genuinely still
remaining when swept — no mid-flight closure.

- legal_candidates.py independent Bareiss 4x4 enumeration: 75 candidates,
  bit-exact with the published edge cost 75 (named cost-75c; cost-75b is
  the completed sibling sweep on `...0008`).
- Sweep complete: **12 WIN7-D10 (bits 8,12,22,66,84,89,96,97,98,100,108,
  111) + 63 REFUTED + 0 capped, 138,240,690 v16 nodes**, all 10 batch
  pilots loss=false at exactly 3,402 nodes.
- Determinism rerun node-exact: bit 66 (heaviest overall AND heaviest
  WIN7, 10,845,926), bit 75 (heaviest REFUTED, 8,628,305), bit 111
  (lightest WIN7, 1,611,883).
- v15 cross-engine anchors on **all 12** WIN7 bits: loss=true at
  8,372,581 / 7,865,566 / 14,083,030 / 21,096,647 / 7,350,763 / 7,039,706 /
  4,292,180 / 9,304,101 / 8,165,861 / 7,067,263 / 5,643,984 / 3,568,856
  v15 nodes, pilots 5,949 ×3.

## Certificates (all 12 WIN7 candidates)

All twelve extracted and fully verified (root-check stones=7 with loser
mobility = independent enumeration, all sub-roots PASS, union 0/0, rows
sorted unique) — every certificate also passes the independent BigInt
cofactor-expansion verifier. Total 713,378 strategy rows / 165,017,710
extraction nodes:

- bit 8: root `00000000000000803202000000004100`, 66,236 rows, 13,452,039
  extraction nodes, 66 loser moves (2-part split).
- bit 12: root `00000000000000803202000000005000`, 60,023 rows, 12,936,955,
  57 loser moves (2-part split).
- bit 22: root `00000000000000803202000000404000`, 78,999 rows, 22,433,703,
  63 loser moves (2-part split).
- bit 66: root `00000000000000843202000000004000`, 86,401 rows, 31,224,950,
  62 loser moves (3-part split).
- bit 84: root `00000000001000803202000000004000`, 59,056 rows, 12,031,200,
  59 loser moves (2-part split).
- bit 89: root `00000000020000803202000000004000`, 60,677 rows, 11,714,155,
  58 loser moves (2-part split).
- bit 96: root `00000001000000803202000000004000`, 42,471 rows, 6,589,016,
  55 loser moves (2-part split).
- bit 97: root `00000002000000803202000000004000`, 55,851 rows, 15,206,431,
  55 loser moves (2-part split).
- bit 98: root `00000004000000803202000000004000`, 68,738 rows, 13,729,984,
  66 loser moves (2-part split).
- bit 100: root `00000010000000803202000000004000`, 48,859 rows, 10,758,610,
  58 loser moves (2-part split).
- bit 108: root `00001000000000803202000000004000`, 42,639 rows, 8,310,219,
  57 loser moves (2-part split).
- bit 111: root `00008000000000803202000000004000`, 43,428 rows, 6,630,448,
  54 loser moves (2-part split).

**unverified_win7_bits is empty** — every WIN7-D10 candidate is certified
at record time. All 25 pushed parts verified byte-exact on the remote by
git blob sha (join with `cat`; joined md5/sha256 in the certificates
README and record).

**Duplicate-folds (2):** the bit-12 root duplicates the cost-65h bit-14
win7_roots listing (cost-65h certified bits 7/109/24 only) and the bit-22
root duplicates the cost-71b bit-14 win7_roots listing (cost-71b certified
bits 109/21/105 only). Both are the first published certificates for their
roots and close the respective warm entries. The other ten roots had
0 hits.

## Frontier recompute

`recompute_frontier_cost75c_20261115.py` reproduces the after-cost-75b
baseline by runpy (asserted 1049/6798/535812/5068/399535), re-derives the
cost-75c child membership, then folds the published **cost-72 bit-111
partial receipt** first (root `00008000000000803202000000000200`, 46,160
rows, 54 sub-roots PASS, union 0/0, git blob sha `b0fee80a...` asserted
from the record; marginal 6, in-manifest 2 — the cost-72 child itself and
`00000008000000003800000008200000`; the cost-72 bit-52 candidate remains
uncertified and that sweep record remains in-flight, so nothing else from
it is folded), then asserts the cost-75c sweep from the 10 published raw
batches, the determinism and v15 control JSONLs, the two duplicate roots
against the cost-65h/71b records, and all twelve receipts
(rows/sub-roots/extraction-nodes/union/md5/sha256/roots), adding them in
the published record order with per-bit marginals re-derived from the
growing union (all covers 7):

- bits 8/12/22/66/84/89/96/97/98/100/108: marginal 5 each, in-manifest 1
  each (bit 8 claims the child `00000000000000803202000000004000`; the
  others add one new manifest member each, e.g. bit 97
  `00000000020000809002000000040000`, bit 98
  `00000000010000809002000000040000`).
- bit 111: marginal 4, in-manifest 0 (its manifest members were already
  covered by the earlier receipts in the union).

**After cost-75c: solved 1062 / unique remaining 6,785 / sum 534,768 /
open 5,055/398,491.** The cost-75c child is closed by its own receipts
(covered by all 12 bits). Two runs byte-identical (recompute JSON + both
CSVs).

## Ranking effect / next targets

**The second class-2 target S5 `00000000000000803202000000000000` is fully
closed by receipts** — after the cost-72 fold only the cost-75c child
remained, and after the twelve receipts the parent has 0 remaining
manifest children (remaining S5 orbits 176 → 175). The best class-2 row is
now the audit-blocked S5 `00000000000000809082000000000000` (classes 3,
10 orbits / 698); the best receipt-coverable class-2 S5 is
`00000000000000809102000000000000` (35 orbits / 2,525). Best class-4
unchanged (`00000000020000003800000080000000`, 18/1,460).

Warm entries closed by this session: cost-65h bit-14 (bit-12 root),
cost-71b bit-14 (bit-22 root). Not folded here: the cost-72 bit-52 candidate (its certificate parts
were being published by the parallel lane during this session; the
completed-sweep record and its fold belong to the cost-72 lane), the warm multiband
certificates published by the parallel lane after the after-cost-75b
baseline (cost-62a/cost-63a/cost-65e — their fold belongs to a canonical
merged recompute), and the older warm rebuild candidates (cost-61d bit-22
= cost-71b bit-1 root, cost-71b remaining WIN7 bits 1/32/74/94/117, ...).

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. WIN7 certificates prove a win within depth 10 from the
  individual 7-stone roots only; REFUTED-D10 sweeps prove only the absence
  of such a win in that subtree; closing the second class-2 target S5 by
  receipts covers exactly its manifest children and does not decide the
  class-2 demand in general; this recompute is bookkeeping over published
  receipts and proves no new game outcome.
