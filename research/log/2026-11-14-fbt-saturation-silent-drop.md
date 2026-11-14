# fbt-cache saturation silently drops forbidden-cell ORs in class4_child1_cert_extractor / _runner (v15 verbatim); found while re-running cost-68/75 certificates

Date: 2026-11-14 (class2 long lane)
Scope: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor.ts, class4_child1_runner.ts (as verbatim-copied into the experiment scripts dir); root-cause line: the fbtOR helper (FBS = 1<<17, probe 48) which returns without OR-ing the three forbidden cells when all 48 probes of a cluster hit occupied slots.

## Finding

The forbidden-bit-table (fbt) used by the extractor/runner is a fixed-size (1<<17 slots, 48-probe) open-addressing table. When a 48-probe cluster is full, `fbtOR` returns silently without inserting/OR-ing the three forbidden cells. No error, no counter in the verbatim code. Consequences observed on real workloads:

- extractor (batched over all legal second moves in one process): cost-75 bit14, moves 0-4,6 measured via instrumented copy (extractor_diag.ts): **710 fbt drops, 90,849 entries**; move 6 finished with ok=false (fatal). A fresh single-move process performs the identical task with **0 drops**.
- runner (class4_child1_runner.ts): instrumented runner_diag.ts on cost-68 bit87 (17,457,204 nodes) shows **fbt_drops = 2,252** (entries 85,080) — the runner also drops on heavy candidates.

## Soundness analysis (why we re-ran instead of trusting)

- For the extractor, a dropped forbidden-cell OR only widens the *forbidden* set check for some positions; the direction of the resulting error depends on the check. In the observed batch cases it produced a fatal (ok=false) at move 6, so the failure was at least visible there; silent partial corruption within an ok=true run cannot be excluded in general.
- For the runner, REFUTED-D10 verdicts rely on the loser's mobility being fully counted; a dropped OR can only *shrink* the loser's legal reply set if forbidden cells were meant to exclude... in fact the drop makes the forbidden-set *smaller than intended* (cells never OR-ed in), which makes the loser's mobility *larger*, i.e. REFUTED verdicts stay conservative in that direction, but WIN7 verdicts could in principle be affected through the search's use of the same table.

## Mitigation / verification performed

- Built exact variants: `runner_exact.ts` and `extractor_exact.ts` (FBS = 1<<20, probe 96, explicit fbt_drops counter; no other change).
- Re-ran the two heaviest cost-68 candidates (bit87: 17,457,204 nodes, bit77: 15,798,996 nodes) with runner_exact: verdicts and node counts **bit-exact identical** to the published v15 sweep, fbt_drops = 0.
- Re-extracted the affected cost-75 certificates with extractor_exact (fresh-batch mode over all legal moves with the drop counter asserted to 0 and fatal asserted null): all moves complete ok=true, fbt_drops = 0; certificates verify PASS (root-check, all sub-roots, union_missing = 0, unconsumed = 0).
- CLI-name note: both repo scripts gate on `process.argv[1].endsWith(<original filename>)`; renamed instrumented copies must update this check (cost two failed runs to notice).

## Operating guidance (until the verbatim engine is patched upstream)

1. Certificate extraction: use extractor_exact (FBS 1<<20) or fresh-process-per-move; assert fbt_drops == 0 and fatal == null before trusting rows.
2. Runner verdicts: heavy candidates (>~10M nodes) should be spot-checked with runner_exact; the cost-68/75 heavy candidates all reproduced bit-exactly.
3. Node counts from the extractor are process-history dependent (memo occupancy) and are not comparable across runs; only verdicts are compared (consistent with existing repo knowledge).

## Status of the affected published results

- cost-68 sweep (17 WIN7-D10 + 51 REFUTED): heaviest two candidates re-verified bit-exact with runner_exact; certificate extraction for all 17 used fresh-per-move mode (0 drops by construction) — records stand.
- cost-75 sweep (19 WIN7-D10 + 56 REFUTED): all 19 certificates re-extracted with extractor_exact with fbt_drops = 0 asserted; the two heaviest candidates (118, 31) and bit77/88/32 re-run node-exact. No verdict change observed anywhere.

11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN.