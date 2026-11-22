# Part BD: independent-host second verification of the Part BC batch-14residual (class 23101) 10-LOSS canonical adoption (2026-11-22)

Verifier part. The published Part BC adoption
(`n11-centralreply-class23101-residualloss10-adoption-reaudit-20261122/`,
publication commits `168a44ae` / `f2405c0e` / `1afbc6a7`, note amendment
`9165ae39`) was declared in the single-owner note and re-executed END-TO-END
on this independent host from published bytes only, then cross-checked with
self-written machinery that does not import any Part BC script.

## What was done

1. **Pipeline re-execution (x3 per stage, byte-verdicts against published shas)**
   - maker `make_increments_residual10.py` x3 -> increment `c3f201a6...`,
     manifest `f7287b7b...` (3/3 byte-identical).
   - merger `s5_union_merge.py` selftest + x3 -> canonical 6,182-row cache
     `0b594f7e...`, audits `6a9a53a3...` (3/3).
   - refresh `refresh_adoption_23101resid.py` x3 -> reaudit outputs
     `5f3a09c6...`/`52ec3d4b...`/`1f54065a...` + (unpublished, sha-recorded)
     worklist `fe71be60...` (3/3).
   - extractor `compare_deltas_batch14residual_adoption.py` x3 ->
     delta json `62de8c16...`, all gates PASS (3/3).
   - Table: `output/bd-rerun-shas.txt`.
2. **Minimal independent checker** `scripts/check_bd_minimal.py`
   (43 checks, 0 failures, rc=0; detail `output/bd-minimal-check-result.json`):
   raw 3-way re-derivation (p1/p2 vs status.log vs row-audit vs batch-keys),
   own increment re-render, cache set-arithmetic (6,172 BASE + 10 increment
   == 6,182 scenario, WIN 158 / LOSS 6,024 / conflict 0), graph s4_cost +
   scenario cache + update8 receipt recomputation: class 23101 scenario-unknown
   exactly {s5 745184 = unconsumed q042 key 1152921505747697664:1032}, holder
   subtraction (23101 10 own memberships, 27 classes 1 each), world classification
   (excluded 390 / excluded_now 23 / free_now 37 / unknown 34,499), update8
   resolved 80 invariant (both worlds), closure table 808 (churn out 22149 /
   in 23965; per-class unknown_now column reproduced for all 808 rows),
   worklist 64,888 -> 64,872 as a (key, serving_class) multiset churn
   (adopted keys fully expelled), per-root coverage (only the
   individual_greedy_union column moves).
3. **Joint greedy non-monotonicity decomposition**: instrumented copies
   (`scripts/refresh_adoption_2310*_instr.py`, exact 7-line diff against the
   published refresh scripts) re-ran BOTH worlds and re-produced every
   published output byte; traces `output/bd-greedy-trace-{base,scen}.json`
   show 1-pass union 49,361 -> 49,351 (down exactly by the 10 adopted LOSS
   keys) while the 6-pass-limit snapshot moves 35,645 -> 38,978: the joint
   greedy never stabilizes (improved=True at pass 6 in both worlds), so the
   published figure is a deterministic 6th-pass local-search snapshot, a plan
   estimate only, NOT a monotone quantity and NOT a coverage claim.
4. **Fail-closed tamper battery (7 runs, all against scratch copies)**:
   T1 maker raw-nodes -> ABORT (3-way gate); T2 merger conflict -> GATE
   FAILED, no output; T3a single verdict flip on a BASE-absent key -> the
   merger ALONE merges it (documented gate gap), T3b the tamper-merged cache
   IS captured downstream by the refresh cache-sha pin; T4 manifest
   row_counts -> GATE FAILED; T5 scenario-cache byte tamper -> sha pin; T6
   frozen policy input tamper -> sha pin. Log: `output/bd-tamper-battery.log`.
   Pristine trees re-verified after the battery (0 anomalies).

## Verified claims (machine-confirmed on this host, no new claims)

The Part BC canonical classification delta is independently reproduced:
class 23101's unknown cost children shrink from 11 to exactly
{745184}; the class stays unknown (its unconsumed q042 WIN child remains);
free_now stays 37; update8 resolved stays 80; probe worklist 64,888 ->
64,872; closure candidate table stays 808 with churn {22149 out, 23965 in}.

## Guards

Verdict consumption ZERO (verification only). The 17 unconsumed closure WINs
(read/write) untouched; the scrutiny owner C++ second-implementation gate pin
`9193f5b6...` unchanged. Class 23101 is NOT free. No root coverage, no class
closure, no WIN/LOSS verdict asserted anywhere. Standard 11x11 empty board and
all 19 central-reply roots remain UNKNOWN. nodes / worklist / greedy numbers
are bookkeeping, never verdicts.
