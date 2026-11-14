# class2-lane cost-73d WIN7 certificate

Root: `00000000000000809083000000004000` (7 stones; S6 child `00000000000000809082000000004000` + bit 48).

- Full certificate: 66,682 lines (2 header lines + 66,680 rows), md5 `9b1456eda973db529091a34cc559fb53`.
- Split at a line boundary into two parts (33,341 lines each):
  - `bit48-root-00000000000000809083000000004000.cert.part1of2` (md5 `08a9c12b4c8ff0730f33d756a0e6328f`)
  - `bit48-root-00000000000000809083000000004000.cert.part2of2` (md5 `b42590001391e3b236a5c2a9d0ae473d`)
- Rejoin: `cat bit48-root-00000000000000809083000000004000.cert.part1of2 bit48-root-00000000000000809083000000004000.cert.part2of2 > bit48.cert` (md5 must equal `9b1456eda973db529091a34cc559fb53`).
- Verification (this session): root-check stones=7 loserMobility=59 (independent enumeration); 59/59 sub-roots PASS; union 0/0; extraction 25,261,945 nodes, fbt_drops=0, fatal=null; sweep-record receipt in `../class2-lane-cost73d-sweep-20261114.json`.
- This certificate proves a winner win within depth 10 from the individual 7-stone root only. 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN.
