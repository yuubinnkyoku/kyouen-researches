# n11 thirteenth owner-union precheck (class 16757 adoption pre-registration)

Read-only pre-registration kit for a future class-16757 adoption Part:
the graph owner-class unions of the thirteenth ladder-top k01/k02 WIN
rows, derived from the frozen dependency graph with the published u04
zero-deviation flip as a method control.

## Results (PRECHECK-PASS, 3 runs byte-identical, tamper 4/4 fail-closed)

- **k01** `1153204147814662144:65536` (s5 index 556117, WIN(1) nodes
  2,678,305 @15M): owner classes **[16612, 16757, 30542]**.
- **k02** `1152922672837951488:65792` (s5 index 558553, WIN(1) nodes
  3,485,963 @15M, published by the parallel lane): owner classes
  **[16740, 16757, 30542]**.
- **Combined owner union: [16612, 16740, 16757, 30542]**
  (serving class 16757 owns both rows).
- **Method control**: the u04 s5 index 745184 derives exactly the
  published zero-deviation flip set [23092, 23101, 23115, 23938]
  (census `2092e7a8`), validating the `idx in s4_cost[ci]` owner probe
  (the list-indexed children arrays; `e[0]` misreading is the known
  false-owner trap).
- **Ladder status** (closure ladder `ef344748`, 800 rows): class 16757
  is rank 1 with unknown_now 2 (both keys unknown there); 16612, 16740
  and 30542 are not ladder rows.
- **Freshness**: both keys verified absent from the head of record
  `beecb024` (6,894 rows WIN 212 / LOSS 6,682, sha-verified).
- **Pre-registered census prediction for a combined k01+k02 adoption**
  (if all four union classes are unknown on the BASE side): unknown
  34,376 -> 34,372, excluded_now 144 -> 148, free_now 39 -> 39, with
  class 16757 leaving the 800-row ladder.  Standing caveats
  (u03 serving-class pre-exclusion; u04 zero churn) are recorded in the
  output json; measurement always replaces prediction.

## Honest disclosures

- This kit runs no solver and consumes no verdict; it is pure
  pre-registration bookkeeping (ultra-cheap legal-precheck pattern).
- The graph (16,001,318 B) and the head of record (288,770 B) are too
  large for single-shot publication and are pinned by sha256 only in
  the output json (`dependency-graph.json.gz` =
  `54f9c364...`, published at
  `n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz`;
  head = `beecb024...`, published in the u04 win adoption kit).
- The k02 WIN row's pillars were still OPEN when this precheck ran
  (declared `177b1086`, owned by the parallel lane); the prediction
  covers a combined adoption only and forbids nothing.

## Files

- scripts/derive_owner_union.py - fresh fail-closed script (G0 pins,
  G1 graph shape, G2 batch-summary cross-pins, G3 owner derivation +
  u04 control, G4 ladder status, G5 freshness; writes nothing on
  failure).
- input/closure-classes.csv, input/thirteenth-batch-summary.json,
  input/k01.input.csv, input/k02.input.csv - sha-pinned inputs
  (byte-clones of the published pins).
- output/owner-union-precheck.json - machine summary (schema
  n11-thirteenth-owner-union-precheck-v1), 3 runs byte-identical.
- output/tamper-battery.log, output/runs.log.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Pre-registration bookkeeping only; NO verdict consumed.  Class 16757
is NOT complete and no free_now flip is claimed.  The standard 11x11
empty board, the 19 central-reply roots, the two-stone root {60,27}
and third moves 100/108 stay UNKNOWN.
