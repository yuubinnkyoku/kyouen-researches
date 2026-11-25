# 2026-11-14 class2-lane: cost-73a sweep in flight + raw-batch remote integrity audits (session 9)

Long-term lane, 9th session. Started from the after-cost70b frontier (solved 913,
remaining 6,934, class-2 target 13 orbits / 915). The hourly parallel lane completed
cost-70b and cost-71 during this session (cost-71: 2 WIN7-D10, bits 9 and 70; frontier
after-cost71: solved 917, remaining 6,930, sum 545,301, open 5,197/408,868).

## cost-73a sweep (claimed by this session, in flight)

- S6 child `00000000000000809082000000000010` (cost 73, demand c1=2,c2=2,c4=0) of the
  best class-2 target S5 `00000000000000809082000000000000`. Independent enumeration
  (legal_candidates.py): 73 legal candidates, matching the published edge cost.
- 57/73 candidates done in 8 local batches (A-H) before the execution environment went
  unavailable: **1 WIN7-D10 so far (bit 81, 5,530,773 nodes)**, 56 REFUTED, 0 capped,
  324,426,606 nodes, pilot d6 control 5,949 in all 8 invocations, terminal range [13,17].
- Remaining bits: 110,111,112,113,116,117,118,119,120 (batch I, not yet run).
- WIN7 bit 81 root hex (independently recomputed, child | (1<<81)):
  `00000000000200809082000000000010`. Cross-checked the same arithmetic against the
  known bit103/bit37 roots - exact reproduction.
- Claim + full per-bit partial results pushed as
  class2-lane-cost73a-inflight-20261114.json (commit 240fcf2f).

## Remote integrity/accounting audits (all PASS)

While the execution environment was unavailable, this session audited the pushed raw
sweep artifacts remotely (fetch + strict per-line JSON.parse + sum/uniqueness checks):

- cost-69c: 69 rows, sum 440,238,688 == record, WIN7 {103}, determinism node-exact.
- cost-69d: 69 rows, sum 296,122,077 == record, WIN7 none, determinism node-exact.
- cost-70: 70 rows, sum 380,930,330 == record, WIN7 none, determinism node-exact.
- cost-70b: 70 rows, sum 404,797,576 == record, WIN7 {37}, root hex reproduced, plus a
  cross-lane node-exact reproduction of bits 12/13/110/37 from this session's own
  independent local run (all four identical to the pushed raw rows).
- cost-71: 71 rows, sum 385,100,613 == record, WIN7 {9,70}, root hexes reproduced,
  determinism node-exact.
- cost-69b: audited twice. A web-text-extraction fetch made three rows appear
  line-wrapped; a first record claimed corruption. Correction: fetching via the GitHub
  Contents API shows the stored files were always intact - the wraps were an artifact of
  the extraction tool. API-based audit: 69 rows, sum 305,754,861 == record, 0 parse
  failures, WIN7 none. The correction record supersedes the false alarm
  (commits 26ca437b -> d137dd5b).

Operational lesson (now recorded in the audit files): remote JSONL integrity checks must
fetch through the Contents API (or raw bytes), never through extracted web text, which
can insert soft line wraps mid-token.

## Resume

1. Finish batch I of cost-73a (bits 110,111,112,113,116,117,118,119,120), then
   determinism rerun of the heaviest bits and the WIN7 bit 81.
2. Extract, verify, and push the WIN7 bit81 certificate
   (root `00000000000200809082000000000010`), same procedure as bit103/bit37.
3. Raw batches A-I + sweep record + log; frontier recompute after-cost73a (assert the
   after-cost71 control: solved 917 / remaining 6,930 / sum 545,301 / open 5,197/408,868,
   extended by cost-71's and cost-73a's receipts).
4. Next unclaimed class-2 children after cost-73a: the remaining cost-73 band
   (`...82000000000040`, `...82000000000080`, `...82000000004000`, `...82002000000000`)
   then cost-74 `...82000100000000`.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (WIN7 certificates prove only that individual
7-stone roots are first-player wins within depth 10; sterile children decide nothing.)
