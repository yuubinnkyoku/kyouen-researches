# 2026-11-18：cost81 v15/v17 cross-version audit

## Result

The same S6 child was swept by two engine generations:

- S6 child: `00000000020000003800000080008000`
- S5 parent: `00000000020000003800000080000000`
- legal seventh-stone roots: 81
- depth: 10
- per-root cap: 1,000,000,000
- v17 ordering: `andclose=1`

The historical class4-lane v15 aggregate and the fresh class2-lane v17 raw batches agree on the complete 81-bit set and on every D10 verdict.

| Measure | Historical v15 | Fresh v17 |
|---|---:|---:|
| Candidate roots | 81 | 81 |
| WIN7-D10 | 0 | 0 |
| REFUTED-D10 | 81 | 81 |
| Capped | 0 | 0 |
| Candidate nodes | 325,836,995 | 86,480,711 |

The v17 run used 239,356,284 fewer candidate nodes, a 73.45890358% reduction (3.76774186 times fewer nodes). Per-root v15/v17 node ratios ranged from 1.58083708 to 8.49010984, with median 4.74860418.

This is a **node-count comparison across v15 and v17**, not an apples-to-apples runtime benchmark. The v17 runner repairs the known `fbtOR` probe-exhaustion drop. The historical v15 run is retained only as a consistency baseline; it is not promoted to proof, and the node reduction is not attributed to a single optimization.

## Independent checks

The new audit was run in the dedicated Proxmox container `pve:199` with Node v22.23.5, one CPU and a 2 GiB memory limit. It reads pinned repository inputs and performs no game search.

- All 81 old and new bit IDs match; verdict agreement is 81/81.
- All v17 rows are uncapped, `andclose=true`, and have terminal stone range [13,17].
- Nine v17 pilot controls pass at exactly 3,402 nodes each.
- Deterministic reruns of batches 1 and 8 match all fields except elapsed milliseconds.
- The 15-bit v15 confirmation run reproduces the historical v15 node counts exactly, 15/15; its pilot is 5,949 nodes.
- A separate BigInt implementation recomputes all 81 D4 root canons; they match the existing v17 audit 81/81 and are all distinct.
- K0865's head-1410 census classifies the S5 parent as `all_remaining_sterile` (18 S6 rows, edge cost 1,460); this cost81 child is one of those 18 references.

The fresh v17 run therefore revalidates one historical K0865 STERILE prediction. It is **not a newly discovered S6 row** and does not increase the global sterile-row count.

## Evidence and reproduction

- Historical v15 aggregate: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost81-sweep-20261114.json` (Git blob `96d3ba0554af684d8f03f8a5008db8a88f24c6b3`).
- Fresh v17 claim: `output/class2-lane-cost81-inflight-20261118.json` (Git blob `5dc331070094343d803fe9d1e1b1222ea4e60b73`).
- Fresh v17 raw audit: `output/class2-lane-cost81-raw-batches-1-9-audit-20261118.json` (Git blob `f90bdccdc25e2f11cbb3af1b152318d994e5761a`).
- Cross-version audit script: `scripts/audit_cost81_v15_v17_crosscheck_20261118.mjs` (Git blob `09f04873573eaf7b48d79ea3b83ea387e1fcc905`).
- Cross-version audit output: `output/class2-lane-cost81-v15-v17-cross-version-audit-20261118.json` (Git blob `adb9e80f8672d6267cdb8ebb33b1b67ca7bc9cbb`; SHA-256 `5bbeeb649442d67c8663c71bb57d3998373694747278db0044014265bb1ca7e7`).
- K0865 census input: `research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json`.

Reproduce from the repository root:

```sh
node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost81_v15_v17_crosscheck_20261118.mjs
```

## Interpretation guard

`REFUTED-D10` means only that no first-player win was found within depth 10 from each individual seven-stone root. It is not a LOSS proof of the seven-stone position, the S6 child, its S5 parent, or the empty board.

There are no WIN7-D10 certificates in this row, so no receipt fold was needed and no S6 manifest row was newly closed. The standard 11×11 empty board, two-stone roots `{49,60}` and `{59,60}`, S2 `{59,60}`, and classes 1/2/4 remain **UNKNOWN**.

## Next target context

The v18 census selects cost82d child `00000000020000003800000080000800` (65 open bits + 17 confirmation bits). Its S5 parent is not among the five parents changed by the landed cost66i bit19 fold, so the target-parent row count is unaffected by the canonical head move 1473 → 1476. K0865 also lists cost82d among the same parent's 18 historical STERILE references; the old v15 aggregate records 82/82 REFUTED-D10. The cost82d claim is therefore a deliberate v17 revalidation of a historical prediction, not a fresh coverage claim. Its v17 run is being resumed separately; no cost82d verdict is claimed in this log.
