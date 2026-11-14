# 2026-11-14 — n11: sweep-engine fbt cache saturation audit (session 11)

## Context

Session 10 completed the cost-73e (73/73 REFUTED, 355,978,631 nodes) and cost-74
(74/74 REFUTED, 490,965,731 nodes) sterile sweeps and then ran a first fbt
saturation audit locally, but the execution environment reset before the audit
outputs could be pushed; all local evidence (instrumented runner, 21-row counter
data, 6-row drop-free data, manifest) was lost. Session 11 rebuilt the audit from
scratch.

## What was done (session 11)

1. Fetched the canonical runner from main (commit 6ebceabb) and rebuilt both
   variants: `runner_instr.ts` (FBS=1<<17 + fbtDrops/fbtInserts/fbtMaxProbe
   counters in fbtOR; behavior-identical) and `runner_fbs20.ts` (FBS=1<<20).
   Pilot d6 control passed at exactly 5,949 nodes in all 16 invocations.
2. Re-ran the full 20-row audit set (8 published WIN7 rows + 6 saturated heaviest
   REFUTED rows + 6 heavy clean rows) plus the 6 drop-free re-solves. Roughly
   472M nodes total, ~520k nodes/s single-threaded, all rows under the per-batch
   time budget.
3. Cross-checked all 20 rows against the published raw batches fetched at commit
   6ebceabb: **20/20 node-exact, verdict-exact, capped-exact, terminal-range-exact**.
4. Re-ran the cost-73e / cost-74 remote accounting audit (26 raw files + 2
   determinism reruns + 2 sweep records + 2 inflight records): strict JSON
   parse of every line, 0 parse failures, candidate sets bit-exact vs inflight
   records, node totals exactly 355,978,631 / 490,965,731, heaviest-bit tables
   exact, determinism reruns node-exact, all pilot controls 5,949. One wording
   discrepancy recorded: the cost-74 sweep record says "14 batch invocations"
   but the 13 raw files hold 13 control lines (the determinism-rerun file holds
   3 more); substance unaffected.

## Results (identical to the lost session-10 audit — bit-exact reproduction)

- All 8 audited WIN7 rows: `fbtDrops = 0` (cost-67 bits 18/34/101/118, cost-71
  bits 9/70, cost-73a bit81, cost-73d bit48).
- Saturation found on 6 REFUTED rows; drop counts reproduced exactly:
  cost-73c bit32: 834,047; cost-73b bit18: 646,356; cost-73c bit120: 58,092;
  cost-74 bit70: 16,034; cost-71 bit110: 10,298; cost-70 bit112: 9,046.
- All 6 saturated rows re-solved with FBS=1<<20 (fbtDrops=0 required):
  verdicts survive (loss=false), drop-free node counts reproduced exactly
  (26,220,909 / 19,910,958 / 19,632,308 / 19,178,789 / 24,937,173 / 21,014,094).
- Saturation onset between 87,159 and 90,616 total inserts (66.5%–69.1% of
  131,072 slots); `fbtMaxProbe` hits the ceiling exactly on saturated rows.
- Insert-count convention documented: session-11 `fbtInserts` excludes the
  C(7,3)=35 root-triple pre-insertions (session-10 numbers are +35 per row).

## Consequences

- No published verdict, frontier number, or certificate changes. The certificate
  layer is already drop-guarded (extractor: FBS=1<<20, fbt_drops=0 required).
- New operational rule recorded: sweep candidates expected above ~19M nodes run
  with the drop counter; saturated verdicts confirmed with FBS=1<<20 before reuse.
- Canonical runner stays byte-identical for raw comparability.

## Artifacts

- `research/experiments/n11-fbt-saturation-audit-20261114/` (scripts, output, README)
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73e-cost74-remote-audit-20261114.json`
- K0783 dated section: sweep-engine fbt cache saturation audit

## Interpretation guard

REFUTED-D10 is the absence of a winner-win-within-depth-10 in a 7-stone subtree;
it is not a refutation of the child. **11x11 empty board, two-stone root {49,60},
S2 {59,60}, class 2, class 4: UNKNOWN.**

## Follow-up (same session): full class2-lane closure

Scanned all 19 published class2-lane sweep records and enumerated every raw row
>= 19M nodes (6 unaudited) plus every remaining WIN7 row (11 unaudited); re-solved
all 17 deduplicated rows with the instrumented runner (17/17 node-exact vs the
published raw batches) and re-solved the 3 newly found saturated rows drop-free.

- New saturated rows: cost-69c bit110 (13,151 drops, 95,315 occupancy), cost-69c
  bit68 (208,479 drops, 106,411 occupancy), cost-70 bit86 (5,703 drops, 94,547
  occupancy). All three survive the FBS=1<<20 drop-free re-solve (loss=false).
- All 11 follow-up WIN7 rows are clean (0 drops), completing the class2-lane
  WIN7 coverage: 19/19 WIN7 rows audited, all with 0 drops.
- Clean 28.8M/24.8M/22.3M-node rows with only 71k-85k occupancy show node count
  alone does not predict saturation; occupancy does.
- Combined: 37 rows audited, 9 saturated, 9/9 confirmed drop-free, 0 verdict
  flips. Frontier numbers and certificates unchanged. 11x11 remains UNKNOWN.

Artifacts: `output/instrumented-runs-followup.jsonl`,
`output/drop-free-reresolve-followup.jsonl`, updated `output/runs-manifest.json`.

## Follow-up 2 (same session): cost-73a rows

The parallel lane's cost-73a sweep record (1 WIN7 bit81 + 72 REFUTED, 0 capped, 383,290,602 nodes; frontier recompute after cost-73a: solved 921) was audited row-wise with the instrumented runner. The two heaviest REFUTED rows and the WIN7 row all reproduced node-exact against the record.

- cost-73a bit92 (20,603,022 nodes): **1,384 fbtDrops at 87,984 total inserts (67.1%)** — new saturated row; tightens the onset bracket to [87,159 clean; 87,984 saturated] of 131,072 slots.
- cost-73a bit23 (18,497,705 nodes): **1,761 drops at 97,145 (74.1%)** — new saturated row.
- cost-73a bit81 WIN7 (5,530,773 nodes): fbtDrops=0 (55,402 occupancy, maxProbe 16) — third independent node-exact reproduction of the WIN7 row; distinct class2-lane WIN7 rows stay 19/19 clean.
- Correction: fbtMaxProbe is not a saturation indicator — dropped 48-step probe walks never update the counter (bit92 saturates with recorded maxProbe=43).
- The FBS=1<<20 drop-free re-solves of bits 92/23 are **confirmed**: the parallel lane's crosscheck (class2-lane-cost73a-runner-fbs20-crosscheck-20261114.jsonl, bits 92/23/48/81) reports fbtDrops=0 on every row with verdicts unchanged and node counts bit-exact identical to the canonical rows. Both rows are saturated-but-confirmed-surviving; combined audit state: 11 saturated rows, 11/11 confirmed drop-free, 0 verdict flips. No published verdict, frontier number, or certificate changes. The certificate layer stays drop-guarded (extractor FBS=1<<20, fbt_drops=0 required; the bit81 certificate was extracted drop-free by the parallel lane).
- v15 context: the parallel lane's v16 memo-key repair means v15 search-time fbt insert patterns (hence the onset bracket) are v15-specific; the audit variants stay v15-derived for comparability and must be re-measured under v16 before reuse.

Artifacts: `output/instrumented-runs-followup2.jsonl`,
`output/runs-manifest-followup2.json`. 11x11 remains UNKNOWN.
