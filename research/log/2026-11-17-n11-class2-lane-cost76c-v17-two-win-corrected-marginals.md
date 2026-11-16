# 2026-11-17 n11 class2-lane: cost76c v17 two-WIN correction and corrected manifest marginals

## Starting point and source review

The first main snapshot inspected in this session was `8719c6ea5922ac1a37b10786b0dba5a172c058f8`. Before the first write, main had advanced to `0dab7917365361f8ce357c4c6174c4f290dbbfe5`; all writes below were then made directly to main, without a branch or PR. The final main at this log's creation is recorded by the following commits: `6c28c90f`, `5d5f8424`, `f516dfe8`, `db56f81b`, and `05eb3c5e`.

Read the current `AGENTS.md`, `research/knowledge/README.md`, K0023, K0783, K0863, K0865 and K0868, plus the 2026-11-17 cost76c raw-sweep, v17 repair, candidate-marginal, head-1452 certificate-census and certificate-bytes re-verification logs. The knowledge boundary remains explicit: K0863 transfers only depth-10 verdicts under D4; REFUTED-D10 is not a LOSS proof; STERILE is not a game-theoretic loss.

## Independent v17 raw-batch reaggregation

Fetched and parsed all ten published cost76c v17 raw batches, checking each Git blob SHA against the v17 audit's pins. Independently compared the candidate set with the pinned claim-input legal list and each per-bit raw record with the v17 audit's per-bit table.

- Raw records: 86 = 76 candidate rows + 10 pilot rows.
- Candidate bits: 76/76 unique and exactly equal to the legal candidate set.
- WIN7-D10: bits **61 and 99**.
- REFUTED-D10: 74 candidates.
- Capped: 0.
- Candidate nodes: **144,218,750**.
- Pilots: 10/10, each loss=false at 3,402 nodes.
- Every candidate: `andclose=true`, terminal stone range [13,17], uncapped.
- Every raw candidate verdict and node count matches the v17 audit's per-bit record.
- v15 and v17, andclose=1, agree on bits 61/99/113: WIN7-D10, WIN7-D10, REFUTED-D10 respectively.

The repaired v17 runner's fallback computes and applies a triple's blocking mask directly when its FBT probe chain is exhausted. The published v16 result for bit 113 (WIN7-D10) is therefore withdrawn: v17 returns REFUTED-D10 in both tested orderings. The v17 audit records 28/76 candidates running under FBT saturation, one verdict flip, 27 same-verdict node-count changes, and 48 byte-identical unsaturated candidates.

## Corrected two-candidate manifest projection

The prior projection assumed three WIN candidates (61/99/113). Its ordered D4 marginal sequence was 5, 4, 4 orbits. The final four-orbit marginal of bit 113 is outside the manifest and adds no manifest row. Removing bit 113 therefore leaves:

| Quantity | Corrected value |
|---|---:|
| WIN candidates | 2 (bits 61, 99) |
| Distinct D4 S6 cover orbits | 15 |
| Intersection with manifest | 7 |
| Already covered manifest orbits | 6 |
| Currently open manifest rows | 1 |
| New orbits from the two candidates | 9 |
| Of those, manifest rows | 1 |
| Of those, outside-manifest orbits | 8 |
| Ordered manifest marginals (61 then 99) | **1 / 0** |

Both remaining roots individually touch the same open manifest row `00000000010000809002000001000000`. After bit 61 is folded, bit 99 adds four further D4 orbits but no new manifest row.

- bit 61 root: `0000000001000080b002000001000000`, 752,696 v17 nodes.
- bit 99 root canon: `00000000040000809002000000400800`, 4,140,409 v17 nodes (5.500772× bit 61).
- bit 113 root canon `00000000040000809002000000400008` is excluded; it is REFUTED-D10 under v17 and must not be extracted or folded.

Bit 61 remains the only extraction target for now; bit 99 is the sole fallback. The projected head after either one, if its certificate is extracted, independently verified and folded, remains **1453/174/6395/506068/4668/369982**. This is only a projection. The canonical head remains 1452/174/6396/506144/4669/370058.

The corrected projection is a set-theoretic restriction of the prior pinned three-candidate projection after removing bit 113's final four marginal orbits; it is **not** a new from-scratch geometric projection run.

## Certificate-extractor safety observation

Static inspection of `class4_child1_cert_extractor_exact_v16.ts` (blob `5518d375fc6b4a7a14c22a1a65586f0c1c5731c0`) found:

- FBT table size: 2^20 slots; linear-probe limit: 96.
- On probe exhaustion, `fbtDrops` is incremented; `extractBatch` returns `fatal: "fbt_saturation"`.
- The CLI writes `res.rows` whenever rows exist, without first checking `res.fatal`.

Thus a rows file can be emitted alongside a fatal result. Any extraction wrapper must reject the entire output if `fatal` is set or `fbt_drops > 0`; no rows from such a run may be used in a certificate or fold. This session did not patch the extractor itself.

## Published artifacts and active claim

- Reproducer: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76c_v17_corrected_candidate_marginals_20261117.py` (blob `49e4852757774002118461c6e21da8f958463513`).
- Corrected projection: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76c-v17-corrected-candidate-manifest-marginals-20261117.json` (blob `3469cf3649ae3ab859edb33bf944ff0f13f229b0`).
- v17 source audit: `class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json` (blob `235f964365a7ab33e33986c915fc7f6861e4d686`).
- Active claim updated in place: `class2-lane-cost76c-inflight-20261116.json` (blob `60090e7c36454e5ecda00d0ca5de5afa18bc5a19`), schema v4. It preserves the v16 execution as history, records v17 as the current result, marks v15 cross-engine agreement complete, excludes bit 113, and records the extractor fail-closed requirement.

The raw-batch reaggregation and assertions were executed directly against the fetched GitHub file contents in this audit session. The published Python reproducer was added for checkout-based reproduction but was not executed in a local clone: the container could not resolve github.com. CI and Knowledge integrity runs for the latest claim commit were queued at log time; no passing result is claimed.

## Current boundary and next action

No cost76c certificate has been extracted or independently verified, and no receipt has been folded. The next action is to blind-extract bit 61, reject any run with a fatal result or nonzero FBT drops, independently verify the certificate with BigInt and Bareiss, then rebase against the latest canonical head and check for verdict conflicts before folding. If extraction fails, try bit 99.

**The standard 11×11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.** WIN7-D10 proves only the individual seven-stone root; REFUTED-D10 is not a LOSS proof.
