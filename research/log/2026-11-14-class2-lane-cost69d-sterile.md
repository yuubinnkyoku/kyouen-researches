# 2026-11-14 class2-lane cost-69d sweep — all 69 REFUTED, 0 WIN7, 0 capped (sterile child)

## Target

`000000000000008090c2000000000000` (cost 69, demand c1=2,c2=2,c4=0), parent S5
`00000000000000809082000000000000` — the last-listed child of the cost-69 band of the
best class-2 blocker-candidate S5 after the after-cost69a frontier recompute (the
parallel class2-lane's declared next pick was `00000000000000809082000000400000`, so
this child was chosen to stay clear of it).

## Method

- Candidates: `legal_candidates.py` (Bareiss 4x4) → 69 legal candidates, bit-exact with
  the published s6_s7_edge_cost 69.
- Engine: repo-verbatim `class4_child1_runner.ts` (v15 exact rules, close-first AND at
  depth >= 8, cap 1e9), 69 candidates in 8-bit chunks over 2 parallel workers; each chunk
  persisted as a raw JSONL batch.
- Controls: pilot d6 (loss=false, 5,949 nodes, PASS); fresh re-run of the 3 heaviest
  candidates (bits 114/20/34) node-exact.

## Result

- **All 69 REFUTED-D10, 0 WIN7, 0 capped, 296,122,077 nodes — sterile child** (the
  class-2 target's first cost-69 sterile child; frontier bookkeeping unchanged, since
  sterile sweeps contribute no receipts).
- Heaviest: bit 114 at 15,008,348 nodes. Terminal stone range over all 69: [13, 17].

## Files

- `output/class2-lane-cost69d-sweep-20261114.json`
- `output/class2-lane-cost69d-raw-batch1..9-20261114.jsonl`
- `output/class2-lane-cost69d-determinism-rerun-20261114.jsonl`

## Scope

A sterile sweep proves only the absence of WIN7-D10 from this S6 child; it does not
close the child's remaining-orbit bookkeeping. 11x11 empty board, two-stone root
{49,60}, S2 {59,60}, class 2 and class 4 all remain UNKNOWN.
