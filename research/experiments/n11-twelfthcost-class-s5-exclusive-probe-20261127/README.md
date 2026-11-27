# n11 twelfth-cost class exclusive single-live-parent S5 probe selection

Adaptive-coordinator twelfth selection after the eleventh-cost k01
canonical adoption closed the eleventh-cost batch stage-1 sweep
(1 row adopted: 1 WIN k01; canonical head of record 1e2eeda2...,
6,890 rows WIN 208 / LOSS 6,682; flip-census + reaudit refresh
published in kit n11-eleventhcost-k01-adoption-reaudit-20261127,
commit 2cd58330).

## Selected class (rank 12 of the published class-closure-priority
table; the top-11 ranks are claimed by the focus-35 / cert-38 /
third-39 / fourth-41 / fifth-44 / sixth-43 / seventh-42 / eighth-43 /
ninth-45 / tenth-44 / eleventh-46 lanes)

- class: 10376293541461626880:16777216, coverage third moves
  [100, 108, 112, 118]
- published priority row (probe-13 basis): s5_children 114,
  s5_unknown 101, unknown_exclusive 44, unknown_shared 57,
  proxy_total 571,078,241, proxy_exclusive_sum 252,985,393,
  proxy_shared_sum 318,092,848, bin_prior_all_loss_index 0.880651
- re-validated against the CURRENT canonical head 1e2eeda2...:
  s5_unknown_before_head 100, unknown_exclusive_head 51,
  unknown_shared_head 49, proxy_exclusive_sum_head 293,115,829,
  bands 5,041,585 x 1 / 5,069,670 x 1 / 5,234,938 x 11 /
  5,932,112 x 38
- 270 fail-closed gates PASS; head basis rows 6,890 WIN 208 / LOSS
  6,682; the eleventh-cost serving class 1297036696978718720:0
  is excluded_now under the head (a measured win-hit flip of the
  eleventh-cost adoption reaudit), so it cannot be re-selected.

## Files

- scripts/select_twelfth_exclusive.py - fresh selector, machine-derived
  structural adaptation of the published eleventh-cost selector
  select_eleventh_exclusive.py (431e3f55...): docstring, HEAD path+sha
  (1e2eeda2...), ELEVENTHKEYS claim input + sha, ELEVENTH_CLASS claimed
  constant, eleventh46 machine-read claim block, top11/rank-12 gates,
  head rows 6,890/208/6,682, output schema
  n11-twelfthcost-exclusive-selection-v1.  Every other byte identical.
  sha256 ea2b8331db3ba9be99b2880230c7a2f70c9576ddbbff6fd16e6e7686feb81024.
- scripts/jsreplay.js - byte-clone of the published eleventh-cost kit
  jsreplay.js (sha256 84585617...), unchanged.
- output/twelfth-cost-exclusive-keys.json - the authoritative machine
  selection list (schema n11-twelfthcost-exclusive-selection-v1, field
  exclusive_probe_order, 51 keys; first 1152921504607895556:603979776,
  last 14987979559889014784:16777216).  sha256
  1119d01bb2a4c0a02222414ae0506aa61a307334b263e619fdfed9b3eddc0878.
- input/k01..k51.input.csv - the 51 probe input rows generated from
  the authoritative list (target,0,5,lo,hi,legal,...; legal
  cross-checked against the shared-s5 supply and independently
  re-derived by the Board inside the selector).

## Run record (this host, Python 3.12)

- run1: ALL GATES PASS (270 gates), selection as above.
- run2, run3: byte-identical output JSON, byte-identical 51 input
  files (determinism PASS).

## Concurrent claims respected (machine-read from published pinned
sources, all sha-verified in-script)

focus 35, cert 38, third 39, fourth 41, fifth 44, sbd 101, parked 2,
parked 4, sixth 43, seventh 42, eighth 43, ninth 45, tenth 44,
eleventh 46; disjointness of the 51 selected keys from every claim
set gate PASS; quarantine absent; head absent (all 51 keys fresh to
the head 1e2eeda2...).

## Meaning and non-meaning

Selection and scheduling only: NO verdict is claimed or implied.
Nodes and proxy values are never evidence of WIN or LOSS.  The
standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.  The 51 exclusive keys
are the twelfth lane's probe batch; any WIN found in batch stops the
escalation per the standing WIN-stopping rule and requires the
C++-gate + third-implementation pillars before any adoption.

## Honest disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- All pinned inputs were present locally byte-verified against the
  published sha256 pins before the run.
