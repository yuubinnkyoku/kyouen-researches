# 2026-11-28 n11 thirteenth owner-union precheck completion

Read-only pre-registration kit (no declaration needed; no solver run,
no verdict consumed): graph owner-class unions of the thirteenth
ladder-top k01/k02 WIN rows for a future class-16757 adoption Part.
Kit:
`research/experiments/n11-thirteenth-owner-union-precheck-20261128/`.

## Results (PRECHECK-PASS, 3 runs byte-identical, tamper 4/4 fail-closed)

- k01 `1153204147814662144:65536` (s5 index 556117): owner classes
  **[16612, 16757, 30542]**.
- k02 `1152922672837951488:65792` (s5 index 558553): owner classes
  **[16740, 16757, 30542]**.
- Combined owner union **[16612, 16740, 16757, 30542]** (serving class
  16757 owns both rows; rank-1 ladder row, unknown_now 2 -> 0 at a
  combined adoption, ladder exit).
- Method control: u04 (745184) derives exactly the published
  zero-deviation flip [23092, 23101, 23115, 23938].
- Freshness: both keys absent from head `beecb024` (sha-verified,
  6,894 rows WIN 212 / LOSS 6,682).
- Pre-registered census prediction (all-4-unknown case): unknown
  34,376 -> 34,372, excluded_now 144 -> 148, free_now 39 -> 39, with
  the u03 pre-exclusion and u04 zero-churn caveats recorded in the
  output json.  Measurement replaces prediction at the adoption
  reaudit.

## Honest disclosures

- The 16 MB dependency graph and the 288 KB head of record are
  pin-only (sha256 in the output json), not republished here; all
  small inputs are byte-clones with published-pin shas.
- The k02 WIN row's pillars are owned by the parallel lane (declaration
  `177b1086`); this precheck changes no ownership and runs no solver.

## Status guard

Pre-registration bookkeeping only; NO verdict consumed.  Class 16757
is NOT complete; no free_now flip is claimed.  The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
third moves 100/108 stay UNKNOWN.  Nodes are bookkeeping, never
verdicts.
