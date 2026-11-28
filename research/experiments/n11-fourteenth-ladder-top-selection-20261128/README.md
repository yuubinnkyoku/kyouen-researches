# n11 fourteenth closure-ladder top-candidate selection (2026-11-28)

Execution kit of the selection declared in
`research/log/2026-11-28-n11-fourteenth-ladder-top-selection-declaration.md`
(publish-then-execute, declaration commit `235b7056`, single owner).
Under the canonical head of record `d772f73c...`
(`merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`, 6,896
rows WIN 214 / LOSS 6,682) and the published thirteenth k01k02 adoption
reaudit closure ladder (`be8bcff1...`, 799 data rows).

## Result (PASS, rc=0, 43 gates, 3 cold runs byte-identical)

All 799 published closure-ladder rows have their `unknown_now`
independently recomputed from the frozen dependency graph `54f9c364...`
+ head `d772f73c...` + update8 receipts `b658290a...` (fresh
re-implementation of the refresh's trust boundary; the refresh
machinery itself is NOT read or executed): **799/799 exact match**.

Top-5 ladder rows gated exactly as pre-registered: class 5804 (4) /
20421 (5) / 34269 (11) / 12264 (33) / 5343 (46).

**Selection: class 5804** (`6053400849139367936:0`, `class_rank` 1,
exactly **4 remaining unknown S5 keys**), the first ladder class whose
remaining unknown keys are ALL unclaimed, fresh, quarantine-free,
5-stone, D4-canonical and canonical-safe:

| # | key | s5_index | legal (Board / fresh det) | probe-13 supply |
|---|---|---|---|---|
| k01 | 6053401124017274880:0 | 198576 | 86 / 86 | absent (proxy null) |
| k02 | 6053682324116078592:0 | 207094 | 82 / 82 | absent (proxy null) |
| k03 | 6052837899185946628:128 | 212115 | 87 / 87 | absent (proxy null) |
| k04 | 6053400849139367936:128 | 212536 | 92 / 92 | absent (proxy null) |

All four keys' legal move counts were re-derived by two independent
implementations (the repo `independent.py` Board and a fresh integer
4x4-determinant concyclicity implementation inside the selector) and
agree. Resolving all four keys would complete class 5804 (a candidate
free_now flip, Board-verified at adoption time).

Scanned candidates: ladder ranks 1-12 are ALL fully available (no
blocked keys among ranks 1-12; the first 12 classes carry 4/5/11/33/
46/50/50/51/51/51/51/51 unknown keys respectively); class 5804 wins by
class_rank order.

## Claim status

All four selected keys are UNCLAIMED against focus_35, cert_38,
third_39, fourth_41, fifth_44, sixth_43, seventh_42, eighth_43,
ninth_45, tenth_44, eleventh_46, twelfth_51, sbd_101, parked_6, the
adopted ultra-cheap 4 and the adopted thirteenth 2 (new in this
Part); all are fresh vs the head; none is in the 2-entry quarantine
registry.

## Files

- `scripts/select_fourteenth_ladder_top.py` - fresh selector, a
  structural adaptation of the published thirteenth selection
  instrument `select_thirteenth_ladder_top.py` (sha256 `e2986020...`):
  head pin d772f73c, closure-ladder pin be8bcff1 (799 rows),
  pre-registered top-5 and selection gates, claim-set machinery
  extended with the adopted thirteenth_2 (and the thirteenth
  in-head gate), dual-implementation legal derivation kept.  sha256
  `eb776f38...`
- `input/k01-k04.input.csv` - the 4 selected keys as cold-pair probe
  inputs (legal column pre-filled from the dual-implementation
  derivation; the escalation Part re-derives independently).
- `output/run1-3.json`, `output/stdout-run1-3.txt` - 3 cold runs,
  byte-identical (run json sha256 `40d50b7d...`).
- `MANIFEST-sha256.txt` - sha256 of every kit file.

## Verification

3 cold runs byte-identical; 43 fail-closed gates PASS; tamper battery
5/5 fail-closed (T1 closure rank-1 unknown_now flip w/ pin patched ->
P2 recomputation + top-5; T2 head row deletion w/ pin patched ->
P1 head-shape; T3 claim duplicate w/ pin patched -> P3 claim-sizes;
T4 graph s4_cost UNKNOWN-child removal w/ pin patched -> P2 + P4;
T5 update8 receipt deletion w/ pin patched -> P1 + P2); clean control
re-PASS byte-identical.  Disclosure: a first T4 attempt that removed a
KNOWN child of class 5804 legitimately passed (rc=0) - the
unknown-count recomputation is invariant to known-child edits - and
was replaced by the UNKNOWN-child removal above; both runs are
recorded as calibration facts.

## Non-meaning

Selection and scheduling only: NO verdict is claimed or consumed.
Nodes, proxy and legal counts are bookkeeping, never evidence of WIN
or LOSS. The standard 11x11 empty board, all 19 central-reply roots,
the two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN. Resolving the selected keys requires a separate single-owner
escalation declaration and, before any adoption, the standing
cold-pair + C++-gate + third-implementation pillars.
