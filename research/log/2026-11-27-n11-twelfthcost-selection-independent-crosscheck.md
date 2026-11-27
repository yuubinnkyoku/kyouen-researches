# 2026-11-27 n11 twelfth-cost selection independent cross-check completion

Kit: `research/experiments/n11-twelfthcost-selection-independent-crosscheck-20261127/`
(7 files).  Result: **CROSSCHECK-PASS** (rc=0, 3 runs byte-identical,
fail-closed battery 5/5, clean control re-PASS byte-identical).

## What was cross-checked

The published twelfth-cost selection (kit
`n11-twelfthcost-class-s5-exclusive-probe-20261127`, commit `e588de1e`):
class `10376293541461626880:16777216` (rank 12), 51 exclusive keys,
head basis `1e2eeda2...` (6,890 rows WIN 208 / LOSS 6,682).

## Independent re-derivation (selector source not read, not executed)

A fresh Python implementation rebuilt the geometry parent map
(3,384 classes, 367,228 child edges) and re-derived the selection from
geometry + probe-13 candidate ledger + probe-13 supply + published
priority table + probe-13 base cache + canonical head + the 14 published
claim lists + the quarantine registry, all sha256-pinned (see kit README).

Calibration before comparison:

- independent live-parent rule reproduces the supply `live_parent_keys`
  column on ALL 4,562 rows, 0 mismatches;
- probe-13 split of the class reproduces the published priority row:
  114 / 101 / 44 / 57, proxy sums 571,078,241 / 252,985,393 / 318,092,848.

Head-side result: 114 children / 100 unknown before head / 51 exclusive /
49 shared / proxy_exclusive_sum_head 293,115,829 / bands
5,041,585x1, 5,069,670x1, 5,234,938x11, 5,932,112x38 — and the
re-derived 51-entry list (key, legal, proxy, order) is EXACTLY EQUAL to
the published `exclusive_probe_order`, entry by entry.

Additional gates, all PASS: top-11 priority rows = the 11 claimed serving
classes and the target is the first unclaimed class (rank 12) and live
under the head; eleventh-cost serving class `1297036696978718720:0`
excluded_now (cannot be re-selected); head freshness 51/51; claim-set
disjointness 14/14 (incl. sbd_101 = the 101 keymap targets, parked_2,
parked_4 halt-audit claimed_keys); quarantine absent; all 51 published
input CSVs byte-verified against the kit MANIFEST with target/legal
fields re-checked 51/51.

Fail-closed battery: T1 published-list key flip / T2 phantom head row /
T3 sixth-claim overlap / T4 CSV legal flip / T5 supply proxy +1000 —
all rc=1 fail-closed; clean control rc=0 byte-identical.  Disclosures
(T5 first attempt was a harness no-op NameError, re-applied and then
detected; full-repo tarball attempt abandoned for individual sha-verified
raw-CDN fetches) are recorded in the kit README.

## Coordination

The concurrent lane's twelfth-cost batch stage-1 sweep (single-owner
declaration commit `f6d29d16`) retains full ownership of the probe
execution.  This cross-check ran no twelfth-cost probe and changes no
verdict: it strengthens the selection the batch is consuming.  Selection
and scheduling only.

## Status guard

The standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  The two-stone root {60,27} and its remaining third moves
100/108: UNKNOWN.  Nodes and proxy values are bookkeeping, never
evidence of WIN or LOSS.
