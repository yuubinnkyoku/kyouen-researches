# 2026-11-16 n11 class2-lane cost-66c sweep (third-ranked open row of the shared parent at head 1441)

## Target and claim

- Row: S6 child `00000000000000003800000008002008` (stones [3,13,27,59,60,61]), cost 66,
  third of the `cheapest_open_rows_ranking` in the head-1441 census v4
  (`class2-lane-next-target-presweep-1441-20261116.json`, blob `3dcb7cb6`, commit `d5db5e3b`),
  behind the claimed cost-65n (completed `6e85762f`) and cost-65o (in flight `ba71a4cc`) rows.
  Single class-2 parent demand: the shared parent `00000000000000003800000008002000`
  (one-stone deletion of bit 3); the other five deletion parents are closed orbits at head 1441.
- IN FLIGHT claim v1 + pre-publication structural verification (8/8 PASS): commit `64e83dff`.
  Pre-sweep checks: 66 legal candidates re-enumerated bit-exact with `legal_candidates.py`
  (independent Bareiss), 66/66 census `root_canon` values reproduced with an independent D4
  implementation, 66 distinct candidate orbits, open 59 + transferred 7 partition,
  zero overlap with the 59 published cost-65n swept roots (57 REFUTED + 2 WIN),
  child canon not among the 13 receipt-covered S6 row orbits of the two cost-65n WIN receipts.

## Sweep

- v16 engine (`class4_child1_runner_v16.ts`, repo-verbatim; published test re-run PASS:
  pilot 3402, bit15 56791, bit0 121837), depth 10, `--andclose 1`, 8 batches (7x8+3), 2 parallel
  processes on 2 cores, ~390k nodes/s/process.
- **Verdict: NOT-STERILE. 7 WIN7-D10 (bits 73, 75, 79, 87, 96, 97, 112) + 52 swept REFUTED-D10
  + 7 transferred REFUTED-D10 = 66/66 determined, 0 capped after the cap-raise resolution.**
- Total definitive swept nodes 84,180,263; raw batches as run (including the capped attempt)
  81,605,344; all records terminalStoneRange [13,17], andclose true, pilot_d6 3402 x8.
- **Cap event (recorded as an experiment fact):** bit 112 hit the 10000000-node protocol cap
  (10,000,001 nodes, capped) in raw batch 7. Re-run at a raised cap of 80,000,000:
  **WIN7-D10 at 12,574,920 nodes**; fresh-process determinism rerun node-exact.
- Determinism: batch 5 (incl. WINs 96/97) rerun node-exact (8/8).
- v15 crosscheck (`class4_child1_runner.ts`, pilot 5949): anchors 73 WIN 3,128,502,
  96 WIN 5,027,518, 30 REFUTED 16,840,620, 83 REFUTED 653,399 - all verdicts agree with v16.
- Independent stdlib audit `scripts/audit_cost66c_raw_sweep_20261116.py`:
  **21/21 ALL PASS**, byte-identical on re-run (inline Bareiss legality, independent D4,
  independent one-stone-deletion parent analysis; engine not re-run).

## WIN7-D10 receipt roots (regenerated with `%032x`, canon-checked vs the census bit table)

| bit | root hex | D4 canon | sweep nodes |
|----:|----------|----------|------------:|
| 73 | `00000000000002003800000008002008` | `00000000000000203800000008080080` | 1,380,970 |
| 75 | `00000000000008003800000008002008` | `00000000000000083800000008080080` | 2,092,539 |
| 79 | `00000000000080003800000008002008` | `00000000000000801202000220800000` | 1,078,921 |
| 87 | `00000000008000003800000008002008` | `00000000000020003800000008080080` | 2,016,731 |
| 96 | `00000001000000003800000008002008` | `00000000020020801202000040000000` | 2,363,101 |
| 97 | `00000000002000003800000008002008` | `00000000020000003800000008080080` | 689,724 |
| 112 | `00010000000000003800000008002008` | `00000000000000801202000300800000` | 12,574,920 |

Hand-transcription note: the first draft of the claim results section had all seven root hexes
and one refuted bit wrong (68 vs 69); every value was regenerated programmatically and
canon-asserted before publication, per the standing lesson that 32-hex values must never be
hand-copied.

## Cross-row verdict watch item

- 66c bit 83 (root canon `00000000000000a09002080080000000`, REFUTED-D10; v16 269,856 nodes,
  v15 653,399 nodes) is D4-identical to the **in-flight cost-65o claim v1 open bit 43 candidate**
  (published overlap-audit input). The cost-65o completion update must either record this as a
  transferred REFUTED-D10 verdict (not re-sweep it) or flag a WIN/LOSS conflict for investigation.
  D4 orbit collisions of the 66c candidates with the cost-65n corpus: 0.

## Next steps

1. Certificate extraction for the 7 WIN7-D10 roots (extractor_exact_v16, empty kill table,
   whole or part1of2/part2of2), then BigInt union + Bareiss double verification.
2. Fold of the 7 certified receipts on the then-current head (the cost-65n fold receipt is
   in flight by a parallel session; head 1441 -> projected 1444 there) with the standard
   conflict census against the folded-roots corpus before the next ranking.
3. The 7 new WIN canons must be conflict-census-checked against the cost-65o sweep corpus
   when it lands (overlap watch: none of the 66c candidate canons overlaps the 65n corpus;
   the 65o corpus is not yet published).

## Interpretation guard

WIN7-D10 proves a first-player win within depth 10 from the individual 7-stone roots only.
REFUTED-D10 is NOT a LOSS proof. NOT-STERILE is not a game value for the row. Transferred
verdicts are D4-canonical identities of published depth-10 engine results. solved 1441 is
manifest-coverage bookkeeping. 11x11 empty board, two-stone roots {49,60} and {59,60},
S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
