# 2026-11-14 class2-lane: cost-61 child (00000000000000809082200000000000) swept, 1 WIN7 certificate

- Frontier after cost-58 was 814/7032/552,811, open 5256/413,283; the class-2 target S5
  00000000000000809082000000000000 stood at 33 orbits / 2245 cost. This run swept its
  second-cheapest open child S6 00000000000000809082200000000000 (cost 61, demand c1=2,c2=2,c4=0).
- 61 non-degenerate 7th-stone candidates (independently re-derived: blocked=60, legal=61,
  matches the published edge cost). Same protocol as cost-58: v15 engine
  (class4_child1_runner.ts), native Node, 4 parallel workers, per-candidate JSONL
  persistence, 4 foreground batches.
- Result: **1 WIN7-D10 (bit 15) + 60 REFUTED-D10 + 0 capped, 235,036,039 nodes**.
  Controls: 16/16 pilot d6 = 5949 PASS; 4 candidates (WIN7 bit15 + heaviest REFUTED
  26/116/117) re-run fresh node-exact identical.
- bit15 certificate: root 00000000000000809082200000008000, 39,782 rows
  (12,334,803 extraction nodes, blind). Independently verified (verify_bit7_win7_cert.ts,
  Bareiss det-4): root-check PASS (stones=7, loserMobility=47), all 47 loser-first-move
  sub-roots PASS, consumed union == certificate rows exactly (0/0), terminals [13,17].
- Frontier effect vs the after-cost58 solved set: 7 covers, 5 marginal, 2 marginal in
  manifest (solved&manifest 814 -> 816 expected at the next full recompute; includes the
  swept child itself 00000000000000809082200000000000). The class-2 target S5 drops
  33 -> 32 orbits (2245 -> 2184 expected).
- Pushed: sweep record, certificate, certificate record, this log. Next: formal frontier
  recompute with the cost-61 receipts (assert after-cost58 controls first), then the next
  cheapest child of the class-2 target (cost 63: 00000000000000809082000000000800).
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 lanes: UNKNOWN.
  WIN7-D10 certificates prove a win within depth 10 from their 7-stone roots only;
  REFUTED-D10 proves only absence of a depth-10 WIN7.
