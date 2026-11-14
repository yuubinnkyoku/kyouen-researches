# 2026-11-14 class4-lane cost-78b: independent sweep (cross-lane reproduction) + frontier recompute 855 -> 875

## Independent cost-78b sweep (S6 `00000000020000003800001080000000`, cost 78, c4=3)

Run in parallel with another lane on the same resume item. Results agree bit-exact:

- **2 WIN7-D10 (bits 48, 113) + 76 REFUTED-D10, 0 capped, 312,168,246 nodes**
  (78 candidates re-derived independently via exact integer Bareiss
  `legal_candidates.py`; the other lane's published record reports the same
  WIN7 bits and the same per-candidate node counts, e.g. bit0 3,557,729 —
  cross-lane reproduction, 4th occurrence).
- Controls: pilot d6 5,949 in every batch; heaviest bit16 re-run fresh
  node-exact (17,995,012); both WIN7 bits re-run fresh node-exact
  (9,877,894 / 6,388,802).
- Raw JSONL batches pushed to `output/class4-lane-cost78b-raw-batch1..4-20261114.jsonl`
  (note: at the repo `output/` root, whereas the other lane's identical raw
  batches and sweep record live under
  `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/` — redundant
  but consistent copies; the experiment-dir copies are canonical).

## WIN7 certificates (independently extracted and verified here)

| bit | root | sub-roots | rows | extraction nodes | md5 |
|----|------|-----------|------|------------------|-----|
| 48 | 00000000020000003801001080000000 | 58 | 50,433 | 20,544,667 | 8d9a68e3db5f93248406459b43874f6d |
| 113 | 00020000020000003800001080000000 | 64 | 52,771 | 12,099,746 | ce47229f13966fd2983b135161886845 |

Blind extraction via `class4_child1_cert_extractor_exact.ts` (empty kill
table, FBS=1<<20, probe 96), fbt_drops=0, fatal=null; both roots re-extracted
in separate processes with identical sums/row counts. Verification by
`verify_bit7_win7_cert.ts` (engine-independent exact Bareiss det4):
root-check loserMobility 58/64 = independent enumerator counts, all sub-roots
PASS, consumed-union == row set exactly (0/0 both directions), terminal
[13,17]. bit113 was extracted twice with identical rows (diff 0).

- bit48 is the SAME 7-stone root as cost-74b bit36 (cross-child root reuse);
  its certificate content is md5-identical to the published cost-74b one.
- bit113 is a new root; certificate also pushed by the parallel lane
  (their record: 55,171 total rows across both roots — bit113 rows identical).
- Local copies of both certificates were additionally pushed under
  `output/class4-lane-cost78b-certificates/` (repo-root `output/`); the
  experiment-dir certificate files are canonical.

Interpretation guard: each certificate proves only a winner win within depth
10 from the individual 7-stone root (loser to move). **No statement about the
S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty
board — all remain UNKNOWN.**

## Frontier recompute after cost-78b (new, unique to this run)

`recompute_frontier_cost78b.py` (extension of `recompute_frontier_cost63cd.py`):
every published staged control baseline -> after-cost63d is asserted first
(638 -> ... -> 855 solved, all reproduced exactly), then the class4-lane
receipts not yet in the chain are added:

- cost-74b (6 roots): 34 covers / 30 marginal / **13 in-manifest** -> solved 868
- cost-78 (2 roots): 13 covers / 11 marginal / **5 in-manifest** -> solved 873
- cost-78b (2 roots, bit48 = reused root): 13 covers / 5 marginal / **2 in-manifest** -> solved 875
- sterile sweeps (cost-73, cost-74a, cost-75, cost-79) contribute nothing;
  cost-79's 0-WIN7/0-capped summary is asserted as a control.

**Frontier after cost-78b: solved_s6_in_manifest 875 (was 855), unique
remaining 6,972, sum cost 548,362, open 5,212/409,908.**
Best class-4 blocker-candidate S5 `00000000020000003800000080000000`:
**24 -> 19 remaining S6 orbits, cost 1,934 -> 1,540**. Best class-2
`00000000000000809082000000000000` unchanged (23/1,601). Re-run is
byte-identical; remote md5s of script/JSON/CSVs verified after push.

Outputs: `class4-lane-cost78b-frontier-recompute-20261114.json`,
`class-frontier-s5-ranking-after-cost78b.csv`,
`class-frontier-top-candidates-s6-after-cost78b.csv`
(under `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/`).

## Next

- The parallel lane has started a cost-79b sweep; its WIN7 receipts (if any)
  will need the next frontier recompute extension (assert after-cost78b
  875/6972/548362/5212/409908 first).
- Best class-4 target S5 remaining 19 orbits; next cheapest unswept children
  per the after-cost78b top-candidates CSV.
- fbt saturation patch proposal for the verbatim engine fbtOR remains open.

**11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4
all remain UNKNOWN** (WIN7 certificates are depth-10 wins from individual
7-stone roots only; REFUTED-D10 refutes only depth-10 wins).
