# n11 eleventh-cost class exclusive single-live-parent S5 probe selection

Adaptive-coordinator eleventh selection after the tenth-cost 2-row
canonical adoption closed the tenth-cost batch (2 rows adopted: 1
LOSS k01 + 1 WIN k02; canonical head of record 16b34014..., 6,889
rows WIN 207 / LOSS 6,682; flip-census + reaudit refresh published in
kit n11-tenthcost-k01k02-adoption-reaudit-20261127, commit a50dc1af).

## Selected class (rank 11 of the published class-closure-priority
table; the top-10 ranks are claimed by the focus-35 / cert-38 /
third-39 / fourth-41 / fifth-44 / sixth-43 / seventh-42 / eighth-43 /
ninth-45 / tenth-44 lanes)

- class: 1297036696978718720:0, coverage third moves [100, 108, 112, 118]
- published priority row (probe-13 basis): s5_children 108,
  s5_unknown 103, unknown_exclusive 41, unknown_shared 62,
  proxy_total 569,915,147, proxy_exclusive_sum 220,947,901,
  proxy_shared_sum 348,967,246, bin_prior_all_loss_index 0.484744
- re-validated against the CURRENT canonical head 16b34014...:
  s5_unknown_before_head 102, unknown_exclusive_head 46,
  unknown_shared_head 56, proxy_exclusive_sum_head 249,214,113,
  bands 5,041,585 x 7 / 5,234,938 x 25 / 5,932,112 x 14
- 246 fail-closed gates PASS; head basis rows 6,889 WIN 207 / LOSS
  6,682; the tenth-cost serving class 1297036692683751424:131072
  is excluded_now under the head (a measured win-hit flip of the
  tenth-cost adoption reaudit), so it cannot be re-selected.

## Files

- scripts/select_eleventh_exclusive.py - fresh selector, machine-derived
  structural adaptation of the published tenth-cost selector
  select_tenth_exclusive.py (0a45a650...): docstring, HEAD path+sha
  (16b34014...), TENTHKEYS claim input + sha, TENTH_CLASS claimed
  constant, tenth44 machine-read claim block, top10/rank-11 gates,
  head rows 6,889/207/6,682, output schema
  n11-eleventhcost-exclusive-selection-v1.  Every other byte identical.
  sha256 431e3f55d3a980d50446887c2924b0e3d02ec206d7e7204a80ff976cad24278a.
- scripts/jsreplay.js - byte-clone of the published tenth-cost kit
  jsreplay.js (sha256 84585617...), unchanged.
- output/eleventh-cost-exclusive-keys.json - the authoritative machine
  selection list (schema n11-eleventhcost-exclusive-selection-v1, field
  exclusive_probe_order, 46 keys; first 1297036696978718720:64, last
  10376293541465821184:268435456).  sha256
  5a29b5be27430eb0f19221234b7d001a92a7f02be577a30d169c5e011da14bd5.
- input/k01..k46.input.csv - the 46 probe input rows generated from
  the authoritative list (target,0,5,lo,hi,legal,...; legal
  cross-checked against the shared-s5 supply and independently
  re-derived by the Board inside the selector).

## Run record (this host, Python 3.12)

- run1: ALL GATES PASS (246 gates), selection as above.
- run2: byte-identical output JSON, byte-identical 46 input files,
  byte-identical stdout (determinism PASS).

## Concurrent claims respected (machine-read from published pinned
sources, all sha-verified in-script)

focus 35, cert 38, third 39, fourth 41, fifth 44, sbd 101, parked 2,
parked 4, sixth 43, seventh 42, eighth 43, ninth 45, tenth 44;
disjointness of the 46 selected keys from every claim set gate PASS;
quarantine absent; head absent (all 46 keys fresh to the head
16b34014...).

## Meaning and non-meaning

Selection and scheduling only: NO verdict is claimed or implied.
Nodes and proxy values are never evidence of WIN or LOSS.  The
standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.  The 46 exclusive keys
are the eleventh lane's probe batch; any WIN found in batch stops the
escalation per the standing WIN-stopping rule and requires the
C++-gate + third-implementation pillars before any adoption.
