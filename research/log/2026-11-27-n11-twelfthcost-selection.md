# 2026-11-27 n11 twelfth-cost class selection

Selection log.  Kit:
`research/experiments/n11-twelfthcost-class-s5-exclusive-probe-20261127/`
(56 files).

## Selected (rank 12, first unclaimed live rank under the head 1e2eeda2)

- class 10376293541461626880:16777216, coverage [100, 108, 112, 118]
- head basis: merged-exact-s5-chain-plus-eleventhcost-k01 (1e2eeda2...,
  6,890 rows WIN 208 / LOSS 6,682)
- s5_unknown_before_head 100, unknown_exclusive_head 51,
  unknown_shared_head 49, proxy_exclusive_sum_head 293,115,829
- bands: 5,041,585 x 1 / 5,069,670 x 1 / 5,234,938 x 11 / 5,932,112 x 38
- selector select_twelfth_exclusive.py sha256 ea2b8331..., a
  machine-derived structural adaptation of the eleventh selector
  431e3f55... (single-occurrence replacements; every other byte
  identical); 270 fail-closed gates PASS; 3 runs byte-identical
  (output JSON + 51 input rows).
- output twelfth-cost-exclusive-keys.json sha256 1119d01b...
  (schema n11-twelfthcost-exclusive-selection-v1).
- Concurrent claims respected (focus 35 / cert 38 / third 39 /
  fourth 41 / fifth 44 / sbd 101 / parked 2+4 / sixth 43 / seventh 42
  / eighth 43 / ninth 45 / tenth 44 / eleventh 46); the 51 keys are
  disjoint from every claim set, quarantine absent, all fresh to the
  head.  The eleventh-cost serving class 1297036696978718720:0 is
  excluded_now under the new head and cannot be re-selected.

## Next work

- Batch stage-1 sweep of the 51 keys at 2M cold pairs (WIN-stopping
  rule; escalation 15M on UNKNOWNs).

## Guards

Selection and scheduling only: NO verdict is claimed or implied.  The
standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair
{100,108}: UNKNOWN.  Nodes and proxy values are bookkeeping, never
verdicts.
