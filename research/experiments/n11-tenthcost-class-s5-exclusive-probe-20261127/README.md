# n11 tenth-cost class exclusive single-live-parent S5 probe selection

Adaptive-coordinator tenth selection after the ninth-cost 12-row
canonical adoption closed the ninth-cost batch (12 rows adopted: 9
LOSS + 3 WIN k12/k02/k07; canonical head of record 47280073..., 6,887
rows WIN 206 / LOSS 6,681; flip-census + reaudit refresh published in
kit n11-ninthcost-12row-adoption-reaudit-20261127, commit 55fcc97e).

## Selected class (rank 10 of the published class-closure-priority
table; the top-9 ranks are claimed by the focus-35 / cert-38 /
third-39 / fourth-41 / fifth-44 / sixth-43 / seventh-42 / eighth-43 /
ninth-45 lanes)

- class: 1297036692683751424:131072, coverage third moves [47, 51,
  100, 108]
- published priority row (probe-13 basis): s5_children 108,
  s5_unknown 102, unknown_exclusive 40, unknown_shared 62,
  proxy_total 568,359,432, proxy_exclusive_sum 213,117,620,
  proxy_shared_sum 355,241,812, bin_prior_all_loss_index 0.532945
- re-validated against the CURRENT canonical head 47280073...:
  s5_unknown_before_head 100, unknown_exclusive_head 44,
  unknown_shared_head 56, proxy_exclusive_sum_head 234,754,546,
  bands 5,041,585 x 6 / 5,234,938 x 30 / 5,932,112 x 8
- 234 fail-closed gates PASS; head basis rows 6,887 WIN 206 / LOSS
  6,681; the ninth-cost serving class 1297036692683751424:134217728
  is excluded_now under the head (a measured win-hit flip), so it
  cannot be re-selected.

## Files

- scripts/select_tenth_exclusive.py - fresh selector, machine-derived
  structural adaptation of the published ninth-cost selector
  select_ninth_exclusive.py (ff352e49...): docstring, HEAD path+sha
  (47280073...), NINTHKEYS claim input + sha, NINTH_CLASS claimed
  constant, ninth45 machine-read claim block, top9/rank-10 gates,
  head rows 6,887/206/6,681, output schema
  n11-tenthcost-exclusive-selection-v1.  Every other byte identical.
  sha256 0a45a65039bfdf751d31f64be2083266b869a05d531777e0c32e1aa6d30c3e40.
- scripts/jsreplay.js - byte-clone of the published ninth-cost kit
  jsreplay.js (sha256 84585617...), unchanged.
- output/tenth-cost-exclusive-keys.json - the authoritative machine
  selection list (schema n11-tenthcost-exclusive-selection-v1, field
  exclusive_probe_order, 44 keys; first 1297036692683751424:131074,
  last 10376293541461626880:268959744).  sha256
  3d0f791effe78d73697f8f627ab0111e1c58e7fefbc154d99935e5a6d9a3ba6e.
- input/k01..k44.input.csv - the 44 probe input rows generated from
  the authoritative list (target,0,5,lo,hi,legal,...; legal
  cross-checked against the shared-s5 supply and independently
  re-derived by the Board inside the selector).

## Run record (this host, Python 3.12)

- run1: ALL GATES PASS (234 gates), selection as above.
- run2: byte-identical output JSON and byte-identical 44 input
  files (determinism PASS).

## Concurrent claims respected (machine-read from published pinned
sources, all sha-verified in-script)

focus 35, cert 38, third 39, fourth 41, fifth 44, sbd 101, parked 2,
parked 4, sixth 43, seventh 42, eighth 43, ninth 45; disjointness of
the 44 selected keys from every claim set gate PASS; quarantine
absent; head absent (all 44 keys fresh to the head 47280073...).

## Meaning and non-meaning

Selection and scheduling only: NO verdict is claimed or implied.
Nodes and proxy values are never evidence of WIN or LOSS.  The
standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.  The 44 exclusive keys
are the tenth lane's probe batch; any WIN found in batch stops the
escalation per the standing WIN-stopping rule and requires the
C++-gate + third-implementation pillars before any adoption.
