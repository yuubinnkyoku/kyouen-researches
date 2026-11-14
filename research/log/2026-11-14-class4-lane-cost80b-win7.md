# 2026-11-14 class4-lane cost-80b sweep: 1 WIN7-D10 (bit 50), certificate verified

## Context

Second cost-80 S6 child of the best class-4 blocker-candidate S5
`00000000020000003800000080000000` (after-cost78b ranking: 19 orbit / cost 1540).
Same session as the cost-80 (child 1) sterile sweep. Main HEAD at push:
the cost-80 commit from this lane.

## Sweep (child: `00000000020000003800040080000000`, c4=3)

Protocol identical to cost-74a/b/75/78/78b/79/79b/80: v15 engine verbatim,
per-candidate freshEngine, close-first AND at depth>=8, cap 1e9, depth 10
single-run, foreground batches with per-batch JSONL durability.

- Enumeration: `legal_candidates.py` independently derives 80 legal candidates;
  matches the published edge cost 80.
- **Result: 1 WIN7-D10 (bit 50) + 79 REFUTED-D10, 0 capped, 298,938,737 nodes
  total, terminal [13,17].**
- Controls: pilot d6 6/6 at 5,949 nodes; heaviest bits 99/17/0 and WIN7 bit 50
  re-run fresh: node-exact identical.

## WIN7 certificate (bit 50, root `00000000020000003804040080000000`)

- Extraction: `class4_child1_cert_extractor_exact.ts`, blind kill table,
  2 move-batches, total 19,497,704 extraction nodes, fbt_drops=0, fatal=null.
- Certificate: 61,565 rows, md5 1ca210fee08212ba79632b5de46372ca,
  `output/class4-lane-cost80b-certificates/n11_s7_00000000020000003804040080000000.cert`.
- Independent verification (verify_bit7_win7_cert.ts, engine-independent Bareiss):
  root-check stones=7, loserMobility=65 (matches independent enumeration);
  all 65 loser first-move sub-roots PASS; consumed winner-state set == row set
  exactly (0/0); terminal range [13,17].

## Interpretation

NOT sterile: one depth<=10 WIN7 root exists in this child. Its covers contribute
to the class-4 frontier through the next recompute (cost-80b additions measured
against the through-cost78b solved set). Cost-80 band: child 1 sterile, child 2
done (1 WIN7), child 3 `00000000020000003800200080000000` (c4=1) remains.

## Guard

WIN7-D10 proves a winner win within depth 10 from the 7-stone root only
(loser to move); REFUTED-D10 is only the negation of such a win. No statement
about the S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11
empty board. **11x11 remains UNKNOWN.**
