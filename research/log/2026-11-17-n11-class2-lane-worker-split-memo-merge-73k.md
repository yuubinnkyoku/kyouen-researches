# 2026-11-17 n11 class2-lane: worker-split memo merge measurement (K0909)

Lane: 11x11 class2-lane long-term (cost73k). Kind: measurement + verification.
Outcome: all gates pass; no verdict change; 11x11 remains UNKNOWN.

## Context

The lane's priority list includes "merge worker caches safely with immediate
WIN/LOSS conflict detection". The 2026-11-17 memo-capacity measurement
(band memo extraction, commit a3c27e9f / blob ce625db0) established the
capacity design (band-wide single table at MS=1<<24 lands at 64% load, where
cross-root sharing is nearly neutral), and the certificate row-set merge
analysis (commit 54cdcf18) established from published bytes that the
extractor's witness choice is root-independent. This session closes the loop
with an actual two-worker split, full memo dumps, an offline merge with
conflict detection, and a merged-seed band run.

An earlier session on 2026-11-17 ran the same measurement but its scripts
were lost to an environment reset; only three constants survived
(workers total 119,962,147 nodes, merge occupied_after 4,291,129,
conflicts 0). This session rebuilt the measurement from scratch
(`measure_worker_split_memo_merge_73k_20261117.py` +
`measure_worker_split_memo_73k.ts`) and re-ran it end to end.

## Design

- Workers: verbatim engine (blob 52bcaf50, both known memo bugs in place -
  K0907), MS=1<<23, band-wide memo within the worker, per-bit
  snapshot+clearRows so each certificate is reconstructed and byte-compared
  against the published certificate. Split at the natural gap:
  A = bits 0,7,11,15,35,39,41,44,58,62,73; B = bits 76,87,89,94,95,97,98,
  103,105,112,117.
- KYOENWM1 dump: after the last bit, every occupied memo slot is written
  (slot, k0..k3 as 8-digit hex, win, lose, nowin, nolose).
- Merge (sort-based, streaming, no sqlite): per-key combination with
  win=min, lose=min, nowin=max, nolose=max (255 = unbound); internal
  conflicts within a worker (among the signed-key bug's duplicate copies)
  and cross conflicts between workers are counted with sentinel-aware rules
  (a conflict needs BOTH values to be real bounds: win<255 & lose<255,
  win<255 & nowin<255 & nowin>=win, lose<255 & nolose<255 & nolose>=lose).
- Seedrun: verbatim engine at MS=1<<24 seeds its memo from the merged
  KYOENWM2 table (insertion in file order through the engine's own
  memoEntry, preserving verbatim probe semantics; high-bit keys stay inert
  duplicates exactly as in a verbatim run), then extracts all 22 bits
  band-wide in one process.
- Record-identity gate: distinct-combine the seedrun's final dump and
  require every seeded key to be present with equal-or-stronger combined
  values (win<=, lose<=, nowin>=, nolose>= when the seed bound exists).

## Results (all gates pass)

- worker A: 48,482,011 nodes, final occupied 5,263,320 slots; per-bit node
  counts equal the published band ms23 per-bit values exactly (fresh
  process reproduces the band prefix); 11/11 certificates byte-identical;
  wall 120s.
- worker B: 71,480,136 nodes, final occupied 6,242,804 slots; 11/11
  byte-identical; wall 164s.
- workers total 119,962,147 = 0.9899 of band ms23 (121,186,659): the split
  is slightly BETTER than the single process at ms23 (it avoids the
  late-bit pollution of the 85%-load table while keeping within-worker
  sharing). This reproduces the lost session's total bit-exactly.
- distinct pass: A 5,263,320 records -> 2,619,833 distinct keys
  (325,765 duplicated keys, max 64 copies); B 6,242,804 -> 2,554,155
  (428,403 duplicated, max 64 copies). All duplicated keys high-bit
  (the K0907 duplicate-insertion mechanism). Internal conflicts: 0 and 0.
- merge: shared distinct 882,089 (20.6% of each worker's keys are shared
  across the split); occupied_after 4,291,899; cross conflicts 0;
  second merge pass byte-identical (md5 e7c2c17e7a91d8ea17f433f3bb482f29).
- seedrun: seeded 4,291,899, inserted 4,290,451, failed 1,448 (0.034% -
  64-slot probe window saturation from verbatim hash clustering at 25.6%
  initial load; performance-only); 85,747,496 nodes = 80.2% of the unseeded
  band ms24 (106,861,135) and 79.0% of the fresh ms23 battery
  (108,499,241); final occupied 10,614,912 (load 63.3% - exactly the
  capacity design the band measurement prescribed); 22/22 certificates
  byte-identical; wall 234s. bit95 = 11,857,737 nodes in every
  configuration (memo-state-invariant root, consistent with K0907).
- record identity: present 4,290,451 (every inserted seed key survives),
  missing exactly the 1,448 failed inserts, value violations 0.
- prior-session cross-check: workers total matches the recorded
  119,962,147 exactly; occupied_after is 4,291,899 vs the recorded
  4,291,129 (+770, 0.018%) - the prior merge implementation is lost, so
  the delta is recorded as an implementation difference (this
  implementation computes occupied_after = distinctA + distinctB - shared
  exactly).

## Experimental facts recorded during the rebuild (implementation lessons)

1. combine_values tuple-index bug (crashed run 1; fixed).
2. The KYOENWM1 header line travels through `sort -k2,5` and crashed the
   record parser (fixed by skipping header lines in the distinct pass).
3. Chunked sort of the 630MB seedrun dump: the final `sort -m` was run
   WITHOUT `-k2,5`, producing a slot-ordered "sorted" file; the
   record-identity gate then reported 3.68M missing keys and caught the
   mistake. After re-merging the chunks with `sort -m -k2,5`, missing
   dropped to exactly the 1,448 failed seed inserts. The gate caught an
   implementation bug that per-record counting would not have.
4. Sentinel-aware conflict rules matter: with the verbatim engine the
   negative bounds are dead (nowin/nolose stay 255 everywhere), so a
   conflict definition that treats 255 as a bound reports millions of
   spurious "conflicts". Both-side-bound rules report the true zero.
5. The sandbox silently killed the orchestrator twice during the long
   single-pass sort of the 630MB dump (no traceback; killed mid-subprocess).
   Chunked sort + per-chunk resume + `sort -m` completed reliably. Long
   single-shot steps are fragile in this environment; resumable steps are
   not.
6. pgrep is unavailable; liveness polling scans /proc/*/cmdline.

## Interpretation guard

Measurement only. No new WIN/LOSS verdicts, no manifest row opened or
closed, certificate bytes unchanged. The repo-verbatim extractor is
unmodified in the repo (published determinism chains). WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof. The 11x11 empty board, both two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.

## Resume pointers

- The merged-seed design generalizes: N workers -> merge -> seed costs one
  sort-based pass plus a seed load at 0.034% loss; a production coordinator
  can merge worker dumps at the same 64%-load capacity point.
- The remaining extractor copies (sweep engine, chunk prover,
  FBT-saturation runners) are still unaudited (K0907 follow-up).
- The fold chain (76c->66i->66j->69j->71e->72d->73i) remains under the
  parallel claim lane's management; do not touch until published.
