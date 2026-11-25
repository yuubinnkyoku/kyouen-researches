# 2026-11-14 class2-lane: cost-65i sweep — 3 WIN7-D10 (all 3 certified, zero unverified WIN7 bits), merged 65h+65i frontier 979 -> 991

Long-term lane session 12, continuing directly from the cost-65g result on the
same lane (after-cost-65g frontier solved 979; commits `c5bcedf9` +
`85c4c1e8`). Sweep target: the cost-65 child `00000000000000803202000000080000`
of the second class-2 target S5 `00000000000000803202000000000000`, named
cost-65i (cost-65 / -65b (sterile) / -65c / -65d / -65e / -65f / -65g occupied;
sibling `...00001000` claimed by the parallel lane as cost-65h at commit
`42bb27ec`).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `0572a93d`):
  `class2-lane-cost65i-inflight-20261114.json`, 65 candidates bit-exact with
  the published edge cost 65 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (18 orbits / 1,277 after cost-65g; cost-65 band
  pair) and its non-empty demand (c1=0, c2=2, c4=2) were re-verified from
  `class-frontier-top-candidates-s6-after-cost65g-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner, agreement-gated in cost-56a and the sweep engine for
  cost-58b / cost-60b / cost-61d / cost-61e / cost-61f / cost-63e / cost-64b /
  cost-65g. Pilot d6 control loss=false at exactly 3,402 nodes in all 9 batch
  invocations.

## Sweep result

**65/65 candidates: 3 WIN7-D10 + 62 REFUTED, 0 capped, 41,416,752 v16
nodes** (9 batches 8x8+1, raw JSONL pushed per batch, commit `fbf680ff`;
terminal range [13,17] on every candidate).

- WIN7 bits: 7, 43, 99.
- Heaviest candidates: bit 75 (3,902,572, REFUTED), bit 43 (2,525,331), bit 110
  (2,520,358, REFUTED), bit 32 (2,301,063, REFUTED), bit 42 (2,071,487,
  REFUTED), bit 98 (1,770,902, REFUTED).
- Determinism: bits 43, 75 and 99 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost65i-v16-determinism-rerun-20261114.jsonl`, commit
  `ca27bfab`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 7/43/99 all loss=true at
  1,924,575 / 7,259,474 / 1,931,010 nodes and bit 75 loss=false at 9,590,469
  nodes — verdicts identical to v16
  (`class2-lane-cost65i-v15-crosscheck-20261114.jsonl`, same commit).

## All three WIN7 certificates — all verification PASS

Every WIN7 candidate of this sweep was extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union). **This is the first sweep of the lane with
zero unverified WIN7 bits.**

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 7 | `00000000000000803202000000080080` | 26,034 | 2,762,105 | 45 | 45/45 | 0/0 | `5e110597...` |
| 43 | `00000000000000803202080000080000` | 44,467 | 12,145,724 | 53 | 53/53 | 0/0 | `b593b35d...` |
| 99 | `00000008000000803202000000080000` | 30,066 | 3,795,698 | 50 | 50/50 | 0/0 | `f417de98...` |

- All three landed byte-exact with full paged reads (commits `32932157` /
  `f15461ba` / `e5f4b5d9`; the bit-43 push hit the 16 MiB sandbox record limit
  AFTER the push call completed — verified landed); remote md5 verified.
- Root absence: GitHub code search 0 hits each (all 3 WIN7 roots checked; the
  cost-61e bit-1 cross-child duplicate pattern does not occur here).
- Terminal ranges within [13,17] on all three.
- **Extraction stdin recipe fix (operational)**: the historical
  `legal_candidates.py | head -2 | LC_ALL=C sort -u` recipe mis-orders lines
  when the candidate-bits line starts with `0,` (it then sorts before the
  root-hex line and the driver's last-line pick takes the wrong line — hit on
  bit 43, whose candidate line starts `0,1,2,...`). The failed first attempt
  produced moves=1/NaN and was discarded without writing a certificate.
  Replaced with `sed -n 2p`, which feeds exactly the candidate-bits line; the
  bit-43 certificate is from the fixed recipe. Recorded in both records.

## Merged frontier recompute after cost-65h + cost-65i

The parallel lane completed cost-65h (13 WIN7-D10 bits 4,7,14,24,33,40,43,67,
99,102,109,117,118 + 52 REFUTED, 0 capped, 57,639,642 v16 nodes; receipts bits
7/109/24; records commit `0c772f2c`) before this lane's cost-65i records, so a
single merged recompute `recompute_frontier_cost65h_65i_20261114.py` (direct
runpy extension of the published cost-65g script) adds BOTH lanes' receipts:
every staged control through after-cost-65g reproduced exactly (asserted 979 /
6,868 / 541,041 / 5,138/404,764), the completed cost-65h sweep/claim/receipts
and cost-65i sweep/claim/receipts are asserted, both children's
remaining-memberships and demands are re-derived and asserted (65i's demand
re-derived from the after-cost-65h intermediate state: c1=0,c2=2,c4=2
unchanged).

- after-cost-65h intermediate: solved 983 · unique remaining 6,864 ·
  sum 540,758 · open 5,134/404,481 (65h receipts marginal: bits 7/109/24 each
  6/2).
- cost-65i additions (covers / marginal / in-manifest): bit 7: 7/6/3, bit 43:
  7/7/4, bit 99: 7/6/3.
- **after cost-65h+65i: solved 991 · unique remaining 6,856 · sum 540,177 ·
  open 5,126 / 403,900** (net in-manifest +12 from 979).
- Second class-2 target S5 `00000000000000803202000000000000`: 18 -> 15 orbits
  (1,277 -> 1,072), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records completed and pushed (commit `4bc5d66f`). Merged frontier recompute
  + script + rankings pushed in commit `e8f5037a`, remote md5 verified. Two
  consecutive recompute runs byte-identical (JSON + both CSVs).

## Operational notes

- Next cheapest remaining children of the second class-2 target after the
  cost-65 band pair: `00000000000000803202000020000000` (67, c1=0,c2=2,c4=0),
  `00000000000000803202000400000000` (68, c1=0,c2=1,c4=0),
  `00000000000000803202000000008000` (69, c1=0,c2=2,c4=0) (per
  `class-frontier-top-candidates-s6-after-cost65h-65i-20261114.csv`; verify
  membership + demand again before claiming; check band-name collisions).
- Session-12 lane totals (this lane): cost-56a (1 WIN7), cost-58b (3), cost-60b
  (25), cost-61d (14), cost-61e (13), cost-61f (11), cost-63e (8), cost-64b
  (20), cost-65g (9), cost-65i (3) on the second class-2 target's children;
  frontier 924 -> 991 across the session's receipts (107 WIN7-D10 verdicts
  incl. the parallel lane's cost-65h, 33 certificates verified incl. 65h's 3).
- Warm candidates: cost-60b 19 · cost-61d 11 · cost-61e 9 · cost-61f 8 ·
  cost-63e 5 (bits 42,73,100,116,120) · cost-64b 17 · cost-62a 10 · cost-65g 6
  (bits 0,15,44,52,75,105) · cost-65h 10 (bits 4,14,33,40,43,67,99,102,117,118)
  · cost-65i 0.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
