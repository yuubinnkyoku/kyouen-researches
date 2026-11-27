# n11-eleventhcost-k01-adoption-reaudit-20261127

Kit of the FOLLOW-UP Part declared in the eleventh-cost k01
canonical adoption completion log (restated in the adoption kit README
"next follow-up Part" disclosure and in the adoption manifest
status_guard field): the BASE (16b34014..., the tenth-cost k01/k02
head of record, 6,889 rows WIN 207 / LOSS 6,682) vs SCENARIO
(1e2eeda2..., the adopted eleventh-cost k01 head of record, 6,890
rows WIN 208 / LOSS 6,682) class-status census measurement and the
reaudit refresh of the new canonical head.

## Files

- reaudit/scripts/refresh_adoption_eleventhcost_k01.py - byte-clone
  of the published tenth-cost k01/k02 refresh 280d7062... (clone
  chain ninth-cost 12-row c9a7372a... <- eighth-cost k01 7e11a316...
  <- SZ wave E d8b14697... <- SV fd2e799e... <- ST 02987d1c... <- SQ
  60dfb1a1... <- SP 82ddb89c... <- sixthwin5 92a884c9... <- EM
  7f379b71... <- EV f2edac3e... <- EU 6dc24c15...), differing in
  EXACTLY the three regions (docstring, CACHE path, expected cache
  sha); every computation byte is identical.  sha256
  0355d7fbb1d13a573cbdaa97ae29c9ff838f8158456ced053864fd55f60ef111.
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted eleventh-cost head (6,890 rows WIN 208 / LOSS
  6,682; census unknown 34,388 / excluded_now 132 / free_now 39 /
  excluded 390).  sha256
  abaf62aadbdd4b41203d1bff7d362010ff83b4aae82114cdd0eaff67fab5b79e.
  Three determinism runs byte-identical.
- reaudit/output/closure-classes.csv - refreshed closure ladder (804
  data rows).  sha256
  d7ae77ddd05d433c0a59555f86efb009e64a5651ad6b918407682bdc5f3178f0 -
  BYTE-IDENTICAL to the published tenth-cost BASE side (measured: no
  unknown_now churn, no rank churn, no entered/left; the adopted row
  sits outside every closure-ladder class).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  03fd32f2ff8da948a5e8df825b049f6e890749105ab6370dbaef2595d0f1ea2c -
  NOT byte-identical to the BASE side: exactly one row differs, root
  2's individual greedy union drops 6,132 -> 6,131 (measured greedy
  re-route; free_now/uncovered identical on all 20 roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (64,272 data rows, 3,715,222 bytes, sha256
  407a340fdb9cc4db8b1d806fe13e4a2228b6783c974d1a54000029159475ff85)
  - UNPUBLISHED per size policy (same size as the BASE pin
  b9f3f1a3.../3,715,222 bytes, different content); pinned here.
- scripts/measure_census_deltas_eleventhcost_k01.py - the
  flip-census measurer, a disclosed structural adaptation of the
  published tenth-cost k01/k02 measurer 7e503080... (machine-derived
  single-occurrence replacements, all pre-registered expectations
  measured before publication).  sha256
  f286f1653d3a6365394b240a7070e0c184743ef26f2dd888002d6f8b3a888dd0.
- output/census-deltas-eleventhcost-k01-adoption.json - the
  measurement record.  sha256
  e1811434f169fce99979f23e21e432a35847a04a9ed28dd43e19a997c41e1510.
  Three determinism runs byte-identical.

## Measured result (win-hit Part EW/EM mechanism)

- The single adopted row (k01 `1297036696978718720:64` WIN(1), s5
  index 97250) flips exactly its THREE owner classes from unknown to
  excluded_now: 2376 (`1297036696977670144:64`, cost-unknown
  109 -> 108), 3288 (the eleventh-cost serving class
  `1297036696978718720:0`, cost-unknown 102 -> 101) and 17116
  (`1152921504607895808:64`, cost-unknown 99 -> 98).
- Census: BASE 34,391/129/39/390 -> SCEN 34,388/132/39/390
  (unknown/excluded_now/free_now/excluded).  No class flips to
  free_now; free_now stays 39 (Board-verified both sides).
- One individual greedy re-route is MEASURED: root 2's individual
  greedy union drops 6,132 -> 6,131 (free_now/uncovered identical on
  all 20 roots).
- Joint greedy stays 37,398 -> 37,398; probing worklist stays
  64,272 -> 64,272 rows.
- update8: resolved 282 -> 282, remaining_now 31,444 -> 31,444,
  groups_free_now 131 -> 131; the adopted s5 index sits outside the
  frozen baseline requirement; the win-hit group set is unchanged
  (25 groups; no flipped class is an update8 plan group class).
- Closure ladder byte-identical to BASE (804 rows, no churn).

## Guards

Class-status bookkeeping only: NO root verdict is consumed, NO class
freed at root level, NO coverage claim made or changed.  The standard
11x11 empty board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN.  Third-move pair {100,108}: UNKNOWN.
Nodes are bookkeeping, never verdicts.

## Honest disclosures

- All pillar inputs (tenth reaudit outputs, eleventh adoption kit,
  graph, update8, board source, policy, quarantine, merger) were
  re-fetched from main and sha-verified before the runs.
- The refresh is memory-heavy; the three determinism runs were
  executed strictly sequentially (no parallel launch).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
