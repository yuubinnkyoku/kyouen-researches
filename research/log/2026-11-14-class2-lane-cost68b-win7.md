# 2026-11-14 class2-lane cost-68b sweep — 2 WIN7-D10 (bits 23, 118), 66 REFUTED, 0 capped

## Target

Cheapest unswept S6 child of the best class-2 blocker-candidate S5 after the after-cost67
frontier recompute: `00000000000000809082000040000000` (cost 68, demand c1=2,c2=2,c4=0),
parent S5 `00000000000000809082000000000000`. Named **cost-68b** because the record name
`class2-lane-cost68` is already taken by the closed former blocker's child
`00000000000000801a02000080000000` (record-name collision lesson from cost-61b/c).

## Method

- Candidates: `legal_candidates.py` (Bareiss 4x4) → 68 legal candidates, bit-exact with the
  published s6_s7_edge_cost 68. The `--bits` list was taken from this enumeration.
- Engine: repo-verbatim `class4_child1_runner.ts` (v15 exact rules, close-first AND at
  depth >= 8, cap 1e9), 68 candidates in 6 chunks over 2 parallel workers, every chunk
  persisted as a raw JSONL batch and pushed before the record was assembled.
- Controls: pilot d6 (loss=false, 5,949 nodes, PASS); fresh re-run of the 3 heaviest
  candidates (bits 18/112/33) and both WIN7 bits (23/118) node-exact against the batch runs.

## Result

- **2 WIN7-D10 (bits 23, 118) + 66 REFUTED-D10, 0 capped, 323,716,265 nodes**
  (heaviest: bit 18 at 16,511,913 nodes).
- Terminal stone range over all 68 candidates: [13, 17].

## WIN7 certificates (both fully verified)

| bit | root | rows | extraction nodes | sub-roots | union missing/extra | loser mobility | md5 |
|-----|------|------|------------------|-----------|--------------------|----------------|-----|
| 23 | `00000000000000809082000040800000` | 30,623 | 8,447,296 | 49/49 PASS | 0/0 | 49 | 8abe922a2f07eb3dd464227985028811 |
| 118 | `00400000000000809082000040000000` | 33,285 | 11,292,258 | 52/52 PASS | 0/0 | 52 | 9400ac2d9ac6750fa86ea2eb5f5d8c74 |

Blind extraction (repo-verbatim `class4_child1_cert_extractor_exact.ts`, FBS=1<<20,
probe 96, empty kill table, `fbt_drops=0`, `fatal=null`); driver `cert_driver68.ts`.
Verification with repo-verbatim `verify_bit7_win7_cert.ts`: root-check (7 stones, no
4-cocircular quadruple, loser mobility 49/52 = independent `legal_candidates.py` count),
every first-loser-move sub-root verified independently with exact Bareiss determinants
(sub-roots 49 and 52, all PASS), consumed-winner-state union vs the certificate row set
empty in both directions (0 missing / 0 extra). Extractor row output is unsorted; the
certificate rows are sorted before push and the verifier's unsorted-row check passes.

## Files

- `output/class2-lane-cost68b-sweep-20261114.json`
- `output/class2-lane-cost68b-raw-batch1..6-20261114.jsonl`
- `output/class2-lane-cost68b-determinism-rerun-20261114.jsonl`
- `output/class2-lane-cost68b-win7-certificates-20261114.json`
- `output/class2-lane-cost68b-certificates/n11_s7_<root>.cert` (2 files)
- `scripts/cert_driver68.ts`

## Scope

WIN7 certificates prove a first-player win within depth 10 from the 7-stone root only.
11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all remain UNKNOWN.
