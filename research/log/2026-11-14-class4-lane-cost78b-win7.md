# 2026-11-14 class4-lane cost-78b (second cost-78 child): 2 WIN7, 1 new certificate, 1 cross-child root reuse

## Sweep (S6 `00000000020000003800001080000000`, cost-78, c4=3)

- **2 WIN7-D10 (bits 48, 113)** + 76 REFUTED-D10, 0 capped,
  312,168,246 nodes total. Foreground batches 16+16+16+17+13, per-batch raw
  pushed to main (`class4-lane-cost78b-raw-batch1..5-20261114.jsonl`).
- Controls: pilot d6 5/5 = 5949; heaviest candidates 16/104/75 and both WIN7
  bits 48/113 re-run fresh, node-exact identical
  (17,995,012 / 16,147,864 / 12,010,089 / 9,877,894 / 6,388,802).
- Record: `output/class4-lane-cost78b-sweep-20261114.json`.

## WIN7 certificates

- **bit113** (root `00020000020000003800001080000000`): **new certificate**,
  55,171 rows, 12,843,269 extraction nodes, fbt_drops=0, fatal=null; all 64
  sub-roots verified PASS, union diff 0/0, terminal range [13,17]. Pushed to
  `output/class4-lane-cost78b-certificates/`, remote md5 verified bit-exact
  (0e45cacf6d5b561497ff3fbc9089f977).
- **bit48** (root `00000000020000003801001080000000`): **same 7-stone root as
  cost-74b bit36**, reached from a different S6 child
  (`...80001080000000` + stone 48 == `...01000080000000` + stone 36).
  A fresh extraction from this child reproduced the cost-74b bit36
  certificate bit-exact (identical full-file md5
  8d9a68e3db5f93248406459b43874f6d), so the existing certificate on main is
  reused and no duplicate file was pushed. First observed cross-child WIN7 root
  sharing in the class-4 lane.
- Record: `output/class4-lane-cost78b-win7-certificates-20261114.json`.

Interpretation guard: each certificate proves only a winner win within depth 10
from the individual 7-stone root (loser to move). **No statement about the S5/S6
orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board — all
remain UNKNOWN.**

## Next

- Frontier recomputation over all new class-4 WIN7 covers (cost-74b 6 +
  cost-78 2 + cost-78b 1 new; bit48 duplicates the cost-74b cover) is pending;
  pull the latest frontier receipt set from main first.
- Next cheapest unswept class-4 children per the after-cost63 ranking CSV.
