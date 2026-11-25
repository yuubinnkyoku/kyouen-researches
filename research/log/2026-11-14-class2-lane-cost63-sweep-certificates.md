# 2026-11-14 class2-lane: cost-63 child (00000000000000809082000000000800) swept, 4 WIN7 certificates

- Third-cheapest open child of the class-2 target S5 00000000000000809082000000000000
  (cost 63, demand c1=2,c2=2,c4=0). 63 non-degenerate 7th-stone candidates (independently
  re-derived: blocked=58, legal=63, matches the published edge cost). Same protocol as
  cost-58 / cost-61-c: v15 engine (class4_child1_runner.ts), native Node, 4 parallel
  workers, per-candidate JSONL persistence, 4 foreground batches.
- Result: **4 WIN7-D10 (bits 3, 20, 70, 119) + 59 REFUTED-D10 + 0 capped,
  273,397,914 nodes**. Controls: 16/16 pilot d6 = 5949 PASS; 4 candidates
  (WIN7 20/119 + heaviest REFUTED 7/14) re-run fresh node-exact identical.
- 4 WIN7 certificates extracted blind and independently verified
  (verify_bit7_win7_cert.ts, Bareiss det-4): root-check PASS (stones=7, loserMobility
  47/46/49/53), ALL loser-first-move sub-roots PASS, consumed union == certificate rows
  exactly (0/0), terminals [13,17]. Rows: bit3 43,752 / bit20 24,875 / bit70 29,632 /
  bit119 42,862 (extraction 45.7M nodes total).
- Frontier effect vs the after-cost61-c solved set: 25 covers, 20 marginal,
  **8 marginal in manifest** (solved&manifest 816 -> 824 expected at the next full
  recompute; includes the swept child itself 00000000000000809082000000000800).
- Naming note: the earlier cost-61b lane names (child 00000000000000801a02020000000000)
  were already taken; this session's second child is recorded as cost-61-c
  (class2-lane-cost61c-*), with its bit15 certificate stored under
  class2-lane-cost61b-certificates/ (file name = unique root hex).
- Pushed: sweep record, 4 certificates, certificate record, this log. Next: formal
  frontier recompute with the cost-61-c and cost-63 receipts (assert after-cost58
  controls first), then the next cheapest class-2 child (cost 63:
  00000000000000809082000000001000 / 000000000000008090a2000000000000 / cost 63
  00000000000000809082000000080000 band).
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 lanes: UNKNOWN.
  WIN7-D10 certificates prove a win within depth 10 from their 7-stone roots only;
  REFUTED-D10 proves only absence of a depth-10 WIN7.
