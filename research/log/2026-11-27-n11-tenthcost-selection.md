# 2026-11-27 n11 tenth-cost class exclusive S5 probe selection

Selection log of the adaptive-coordinator tenth selection, issued
after the ninth-cost 12-row adoption + flip-census/reaudit Parts
closed (completion logs 5e8e8729 / 1fb65f45, canonical head of
record 47280073..., 6,887 rows WIN 206 / LOSS 6,681).  Kit:
`research/experiments/n11-tenthcost-class-s5-exclusive-probe-20261127/`
(commit 1ab5d6e1, 49 files, fetch-back sample 8/8 byte-identical).

## Selection

- Class 1297036692683751424:131072 (rank 10 of the published
  class-closure-priority table; the top-9 ranks are claimed by the
  focus-35 / cert-38 / third-39 / fourth-41 / fifth-44 / sixth-43 /
  seventh-42 / eighth-43 / ninth-45 lanes; the ninth-cost serving
  class 1297036692683751424:134217728 is excluded_now under the head
  and cannot be re-selected).
- Coverage third moves [47, 51, 100, 108].
- Re-validated under the CURRENT head 47280073...: s5 unknown before
  head 100, exclusive (single-live-parent) keys 44, shared 56,
  proxy_exclusive_sum_head 234,754,546, bands 5,041,585 x 6 /
  5,234,938 x 30 / 5,932,112 x 8.
- Selector: machine-derived structural adaptation of the published
  ninth selector (ff352e49...) - 234 fail-closed gates PASS, two runs
  byte-identical (output json 3d0f791e... x2, 44 input files
  byte-identical).  All 44 keys are fresh to the head, absent from the
  quarantine registry, and disjoint from every machine-read
  concurrent claim set (focus 35 / cert 38 / third 39 / fourth 41 /
  fifth 44 / sbd 101 / parked 2 / parked 4 / sixth 43 / seventh 42 /
  eighth 43 / ninth 45).

## Position and next work

The authoritative machine list is output/tenth-cost-exclusive-keys.json
(field exclusive_probe_order, 44 keys, first 1297036692683751424:131074,
last 10376293541461626880:268959744).  Next: the tenth-cost batch
stage-1 sweep (44 keys, 2M cap cold pairs, WIN-stopping rule active;
any WIN requires C++-gate + third-implementation pillars before any
adoption).  Selection and scheduling only: NO verdict is claimed or
implied, nodes and proxy values are never evidence of WIN or LOSS.
The standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
