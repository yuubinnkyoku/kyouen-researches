# class2-lane cost-73a WIN7 certificate

Root: `00000000000200809082000000000010` (7 stones; S6 child `00000000000000809082000000000010` + bit 81).

- Full certificate: 37,311 lines (2 header lines + 37,309 rows), md5 `ecf3ab773961f877c3044862ba2ad7b7`.
- Split at a line boundary into two parts (18,656 / 18,655 lines):
  - `bit81-root-00000000000200809082000000000010.cert.part1of2` (md5 `e6763b1de133c50bfc04a6f314249264`)
  - `bit81-root-00000000000200809082000000000010.cert.part2of2` (md5 `02dcc3845c431ec851ccef6fc75a6686`)
- Rejoin: `cat bit81-root-00000000000200809082000000000010.cert.part1of2 bit81-root-00000000000200809082000000000010.cert.part2of2 > bit81.cert` (md5 must equal `ecf3ab773961f877c3044862ba2ad7b7`).
- Verification (this session, takeover re-run): root-check stones=7 loserMobility=51 (independent legal_candidates.py enumeration); 51/51 sub-roots PASS (all seen>0, terminals>0, terminal ranges within [13,17]); union of consumed winner states equals the 37,309-row set exactly (0 missing / 0 extra); extraction via `class4_child1_cert_extractor_exact.ts` (repo-verbatim, blind kill table, FBS=1<<20, drop-counter): 8,777,255 extraction nodes, fbt_drops=0, fatal=null; rows sorted (no duplicates) before verification per the established extractor note.
- WIN7 verdict cross-checked three ways: session-9 inflight run (5,530,773 nodes), this session's fresh re-run (node-exact), and the FBS=1<<20 instrumented engine `runner_fbs20.ts` (node-exact, fbtDrops=0).
- This certificate proves a winner win within depth 10 from the individual 7-stone root only. 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN.