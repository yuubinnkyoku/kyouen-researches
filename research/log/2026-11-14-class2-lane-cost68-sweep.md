# 2026-11-14 class2-lane: cost-65 reproduced (parallel push), cost-68 completed, class-2 blocker closed

- cost-65 child 00000000000000003802000008000010: 65 candidates, 7 WIN7-D10 (bits 0,12,52,72,73,84,90)
  + 58 REFUTED, 0 capped, 135,869,766 nodes; 7 certificates (247,077 rows) all verified PASS.
  The parallel lane had already pushed the full cost-65 package (numbers identical) - 4th
  same-subject collision, no duplicate push. After cost-65: 786/7060/554,836, open 5277/414,843.
- cost-68 child 00000000000000801a02000080000000: 68 candidates, 17 WIN7-D10 (bits
  0,4,7,8,9,12,20,24,40,42,50,52,78,87,96,110,112) + 51 REFUTED, 0 capped, 363,926,743 nodes;
  17 certificates (685,723 rows, extraction 199.8M nodes) all verified PASS (root-check,
  48-61 sub-roots per root, exact union).
- Frontier recompute with all staged controls reproduced: after cost-68 solved 804,
  unique remaining 7042, sum cost 553,474, open 5259/413,481. COST-68 MARGINAL COVERS (102
  covers / 86 marginal / 18 in-manifest) also cover the cost-75 child 00000000000000801a02040000000000,
  so the long-standing class-2 S5 blocker 00000000000000003802000008000000 is now ABSENT from the
  ranking: fully closed by WIN7 certificates. Next best class-2: 00000000000000809082000000000000
  (37/2507); best class-4 unchanged 24/1934.
- Pushed: sweep record, 16/17 certificates (bit87 = 64,844 rows = 2.34MB exceeds the
  run_typescript 16MiB recording limit - pending; local verification PASSed), certificate
  record, compact frontier recompute record. The execution environment went down before the
  recompute script, full recompute JSON, after-cost68 CSVs and this log could be pushed from
  local files; the compact record carries all values. Next run: re-push the remaining cost-68
  files (check for parallel pushes first), then attack 00000000000000809082000000000000 or the
  class-4 blocker.
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 lanes: UNKNOWN.
