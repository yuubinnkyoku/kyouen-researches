# 2026-11-14 class2-lane: cost-64 independently reproduced after environment reset

- Mid-sweep the execution environment reset (workspace lost). Rebuilt all tooling from main
  (runner/extractor/verify verbatim; cert_driver rebuilt kill-table-optional with pref=null;
  legalmoves.ts rebuilt from the engine's legality rule; 61/64-candidate counts re-validated
  against the published cost-61b child).
- Redone cost-64 sweep (child 00000000000000801a0a000000000000): 64 candidates, cap 50M, d10,
  2 workers, pilot 5949 x2 PASS: 24 WIN7-D10 + 40 REFUTED, 0 capped, 195,421,906 nodes.
  The pre-reset partial run had already given the identical 24-bit WIN7 set (its lower node
  total was only the 950k-cap intermediate pass on bits 3/6/86, all REFUTED when resolved).
- All 24 WIN7 certificates re-extracted + independently verified (root-check, all sub-roots
  43-56 per root, exact union): 904,966 rows total.
- Local frontier recompute: all staged controls through after_cost61b reproduced
  (749/7097/557548/5314/417555); after cost-64: solved 779, unique remaining 7067,
  sum cost 555,327, open 5284/415,334. Class-2 blocker 00000000000000003802000008000000
  now 4 orbit / 276 (children cost 65, 68, 68, 75).
- Pushing time: main already contained the full cost-64 package from the parallel lane
  (sweep 35394f4a with the bit-exact same node total, all 24 certificates, cert record,
  recompute script/record 4bc289dc, CSVs) — third same-subject collision, no duplicate push.
- Verdict-relevant state unchanged elsewhere. 11x11, {49,60}, S2 {59,60}, class 2/4: UNKNOWN.
