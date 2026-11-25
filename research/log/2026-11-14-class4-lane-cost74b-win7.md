# 2026-11-14 class4-lane cost-74b: 6 WIN7 certificates + legal_candidates.py bugfix

## cost-74b sweep (S6 `00000000020000003801000080000000`, c4=3 demand)

Full 74-candidate sweep of the second cost-74 S6 child:
- **6 WIN7 (depth 10): bits 36, 53, 70, 72, 104, 117**; 68 REFUTED-D10, 0 capped.
- 240,391,562 nodes total. Controls: pilot d6 6/6 = 5949; bits 117/36 re-solved fresh node-exact.
- Record: `output/class4-lane-cost74b-sweep-20261114.json`.

## WIN7 certificates (independently verified, all on main)

Extracted from each 7-stone root via `class4_child1_cert_extractor_exact.ts`
(exact integer Bareiss loser-first-move enumeration over ALL C(7,3) triples,
engine cross-checked bit-exact), verified by `verify_bit7_win7_cert.ts`
(engine-independent exact det4 replay). All 6: **independent verification PASS**,
fbt_drops=0, fatal=null, union diff 0/0, terminal range [13,17].

| bit | root | sub-roots | rows | md5 |
|----|------|-----------|------|-----|
| 36 | 00000000020000003801001080000000 | 58 | 50,433 | 8d9a68e3db5f93248406459b43874f6d |
| 53 | 00000000020000003821000080000000 | 57 | 41,689 | c7592aafe1c4411491f50be4372e8374 |
| 70 | 00000000020000403801000080000000 | 55 | 36,706 | 24c558db6d68e6ff116ca86b234e38ef |
| 72 | 00000000020001003801000080000000 | 50 | 19,814 | 5cf18914bee13c627aa00cc8c0c7ada2 |
| 104 | 00000100020000003801000080000000 | 63 | 51,865 | 442798d2fbb4eeb2a17edd6b6456c953 |
| 117 | 00200000020000003801000080000000 | 64 | 59,805 | f17ac9f54c8f8d6b08796029be3f9068 |

Total: 259,912 rows, 89,465,448 extraction nodes. Certificates in
`output/class4-lane-cost74b-certificates/`, record:
`output/class4-lane-cost74b-win7-certificates-20261114.json`.

bit117 md5 is the **remote** file (trailing newline lost in push transport —
known artifact, precedent cost-68 bit87); the fetched-back remote version was
independently re-verified: all 64 sub-roots PASS, union 0/0.

Interpretation guard: each certificate proves only a winner win within depth 10
from the individual 7-stone root (loser to move). **No statement about the S5/S6
orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board — all
remain UNKNOWN.**

## legal_candidates.py bug (fixed)

`scripts/legal_candidates.py` hardcoded the occupied-stone count to 6 in the
triple enumeration (`itertools.combinations(range(6), 3)`), so on a 7-stone
root it never inspected triples containing the last occupied stone and
**over-reported legal candidates** (e.g. 74 instead of the true 57 for the
bit53 root). Fixed to `range(len(st))`.

Impact: all 6-stone child sweeps (cost-58, 61c, 63, 74a, 74b) used correct
enumerations (bit-exact re-verified after the fix: 74/74 for the two cost-74
children). The six cost-74b 7-stone WIN7 roots re-verified bit-exact against
engine loser-mobility (57/58/64/50/55/63). The parallel lane's cost-63b
certificate used the correct 48-move list and is unaffected.

## Next

- Next cheapest unswept class-4 child: cost-75 `00000000020000003800020080000000`,
  then cost-78 `00000000020000003800000080000040` / `00000000020000003800001080000000`.
- Sterile children (cost-73, 74a, 74b...88000000) count as swept; frontier
  recomputation over the 6 new WIN7 covers is pending.
