# 2026-11-14 class2-lane: cost-68 full frontier recompute re-pushed (compact-record histogram corrected), cost-58 child swept, 3 WIN7 certificates

- Completed the cost-68 TODO from the previous run: regenerated `recompute_frontier_cost68.py`
  and pushed the full frontier recompute record + after-cost68 ranking CSVs. All staged controls
  reproduce exactly (baseline 638/7208/565500 ... after_cost65 786/7060/554836 open 5277/414843;
  after cost-68 804/7042/553474 open 5259/413481; addition covers=102 marginal=86 in-manifest=18).
  CORRECTION: the compact record's `demand_histogram_open_only` was stale after-cost61b values
  (sum 5314 != its own open_s6 5259); the full record's histogram sums to 5259 and matches the
  published after-cost65 histogram at the prior stage. All other compact values confirmed.
  bit87 cost-68 certificate confirmed present on main (64844 rows, md5 e93199b7...): the cost-68
  package is now complete with no pending files.
- Frontier after cost-68 (independently reproduced): class-2 blocker S5
  00000000000000003802000008000000 fully closed (absent from the ranking). Next best class-2
  S5: 00000000000000809082000000000000 (classes=3, 37 orbits, cost 2507); best class-4 unchanged
  00000000020000003800000080000000 (24 orbits, 1934).
- cost-58 sweep (main new result): the cheapest open S6 child of the new class-2 target,
  00000000000000809082000080000000 (cost 58, demand c1=2,c2=2,c4=0). 58 non-degenerate 7th-stone
  candidates enumerated as all legal moves of the child (independently re-derived: blocked=63,
  legal=58, matches the published edge cost). v15 engine (class4_child1_runner.ts), native Node,
  4 parallel workers, per-candidate JSONL persistence, 4 foreground batches.
  Result: **3 WIN7-D10 (bits 101, 111, 119) + 55 REFUTED-D10 + 0 capped, 171,484,029 nodes**.
  Controls: 16/16 pilot d6 = 5949 PASS; 5 candidates re-run fresh in separate processes
  (WIN7 101/111/119 + heaviest REFUTED 77/100) node-exact identical.
- 3 WIN7 certificates extracted blind (per-loser-first-move batches, sort -u merge):
  bit101 root 00000020000000809082000080000000 (16,631 rows, 3,024,309 extraction nodes),
  bit111 root 00008000000000809082000080000000 (15,475 rows, 4,354,791 nodes),
  bit119 root 00800000000000809082000080000000 (33,794 rows, 13,408,259 nodes).
  All independently verified with verify_bit7_win7_cert.ts (Bareiss det-4, engine-independent):
  root-check PASS (stones=7, loserMobility 40/37/48), ALL loser-first-move sub-roots
  (40/37/48 per root) PASS, consumed union == certificate row set exactly (0/0), terminals [13,17].
- Frontier effect of the 3 certificates (measured against the after-cost-68 solved set):
  19 covers, all 19 marginal, **10 marginal in manifest** (solved&manifest 804 -> 814 expected
  at the next full recompute; includes the swept child itself
  00000000000000809082000080000000, three more orbits of the class-2 target S5, and class-4-lane
  children such as 00000000020000003800000008080000 and 00000000020000821002000000080000).
  The class-2 target S5 00000000000000809082000000000000 drops by at least 4 orbits (37 -> <=33).
- Pushed: sweep record, 3 certificates, certificate record, this log. Next: formal frontier
  recompute with the cost-58 receipts (assert after-cost68 controls first), then the next cheapest
  child of the class-2 target (cost 61: 00000000000000809082200000000000) or the class-4 blocker
  cheapest child (cost 73: 000000000200000038000000c0000000).
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 lanes: UNKNOWN.
  WIN7-D10 certificates prove a win within depth 10 from their 7-stone roots only;
  REFUTED-D10 proves only absence of a depth-10 WIN7.
