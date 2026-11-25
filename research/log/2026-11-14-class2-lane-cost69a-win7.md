# 2026-11-14 class2-lane cost-69a sweep — 3 WIN7-D10 (bits 48, 70, 103), 66 REFUTED, 0 capped

## Target

Cheapest unswept S6 child of the best class-2 blocker-candidate S5 after the after-cost68b
frontier recompute: `00000000000000809082000000000400` (cost 69, demand c1=2,c2=2,c4=0),
parent S5 `00000000000000809082000000000000`. Named **cost-69a** (first of the four
cost-69 children).

## Method

- Candidates: `legal_candidates.py` (Bareiss 4x4) → 69 legal candidates, bit-exact with the
  published s6_s7_edge_cost 69. `--bits` lists taken from this enumeration.
- Engine: repo-verbatim `class4_child1_runner.ts` (v15 exact rules, close-first AND at
  depth >= 8, cap 1e9), 69 candidates in 8-bit chunks over 2 parallel workers, each chunk
  persisted and pushed immediately (environment reset mid-sweep cost one 24-candidate
  batch, which was redone deterministically).
- Controls: pilot d6 (loss=false, 5,949 nodes, PASS); fresh re-run of the 3 heaviest
  candidates (bits 68/53/117) and all 3 WIN7 bits (48/70/103) node-exact.
- Raw-batch-1 caveat: the first batch was started with hardcoded bits 0,1,2,3 (after the
  reset, before re-enumeration); bit 3 is NOT a legal candidate of this child (its
  REFUTED-D10 line stays in the raw file only, excluded from the record); bits 0,1,2 are
  legal and counted once.

## Result

- **3 WIN7-D10 (bits 48, 70, 103) + 66 REFUTED-D10, 0 capped, 360,149,635 nodes**
  (heaviest: bit 68 at 16,771,990 nodes).
- Terminal stone range over all 69 candidates: [13, 17].

## WIN7 certificates (all three fully verified)

| bit | root | rows | extraction nodes | sub-roots | union missing/extra | loser mobility | md5 |
|-----|------|------|------------------|-----------|--------------------|----------------|-----|
| 48 | `00000000000000809083000000000400` | 42,596 | 13,368,996 | 54/54 PASS | 0/0 | 54 | 24997fa018e2c89cbcd65b3a006c8183 |
| 70 | `00000000000000c09082000000000400` | 36,472 | 10,623,218 | 51/51 PASS | 0/0 | 51 | b733bc366bc2380d7333372bf6f8e19f |
| 103 | `00000080000000809082000000000400` | 29,047 | 8,466,041 | 48/48 PASS | 0/0 | 48 | 4e11f676c6a67c457be19ca4ac2a3691 |

Blind extraction (repo-verbatim `class4_child1_cert_extractor_exact.ts`, FBS=1<<20,
probe 96, empty kill table, `fbt_drops=0`, `fatal=null`); verification with repo-verbatim
`verify_bit7_win7_cert.ts`: root-check (7 stones, no 4-cocircular quadruple, loser mobility
54/51/48 = independent `legal_candidates.py` counts), every first-loser-move sub-root
verified independently with exact Bareiss determinants, consumed-winner-state union vs the
certificate row set empty in both directions (0 missing / 0 extra).

## Files

- `output/class2-lane-cost69a-sweep-20261114.json`
- `output/class2-lane-cost69a-raw-batch1..10-20261114.jsonl`
- `output/class2-lane-cost69a-determinism-rerun-20261114.jsonl`
- `output/class2-lane-cost69a-win7-certificates-20261114.json`
- `output/class2-lane-cost69a-certificates/n11_s7_<root>.cert` (3 files)

## Scope

WIN7 certificates prove a first-player win within depth 10 from the 7-stone root only.
11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all remain UNKNOWN.
