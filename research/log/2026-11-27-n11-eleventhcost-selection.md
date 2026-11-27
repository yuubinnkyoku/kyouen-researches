# 2026-11-27 n11 eleventh-cost class exclusive S5 probe selection

Selection log of the adaptive-coordinator eleventh selection, issued
after the tenth-cost 2-row adoption + flip-census/reaudit Parts
closed (completion logs b4cefa42 / 31b6d110, canonical head of
record 16b34014..., 6,889 rows WIN 207 / LOSS 6,682).  Kit:
`research/experiments/n11-eleventhcost-class-s5-exclusive-probe-20261127/`
(kit commit, 50 files, fetch-back verified in the run record below).

## Selection

- Class 1297036696978718720:0 (rank 11 of the published
  class-closure-priority table; the top-10 ranks are claimed by the
  focus-35 / cert-38 / third-39 / fourth-41 / fifth-44 / sixth-43 /
  seventh-42 / eighth-43 / ninth-45 / tenth-44 lanes; the tenth-cost
  serving class 1297036692683751424:131072 is excluded_now under the
  head and cannot be re-selected).
- Coverage third moves [100, 108, 112, 118].
- Re-validated under the CURRENT head 16b34014...: s5 unknown before
  head 102, exclusive (single-live-parent) keys 46, shared 56,
  proxy_exclusive_sum_head 249,214,113, bands 5,041,585 x 7 /
  5,234,938 x 25 / 5,932,112 x 14.
- Selector: machine-derived structural adaptation of the published
  tenth selector (0a45a650...) - 246 fail-closed gates PASS, two runs
  byte-identical (output json 5a29b5be... x2, 46 input files
  byte-identical).  All 46 keys are fresh to the head, absent from the
  quarantine registry, and disjoint from every machine-read
  concurrent claim set (focus 35 / cert 38 / third 39 / fourth 41 /
  fifth 44 / sbd 101 / parked 2 / parked 4 / sixth 43 / seventh 42 /
  eighth 43 / ninth 45 / tenth 44).

## Position and next work

The authoritative machine list is output/eleventh-cost-exclusive-keys.json
(field exclusive_probe_order, 46 keys, first 1297036696978718720:64,
last 10376293541465821184:268435456).  Next: the eleventh-cost batch
stage-1 sweep (46 keys, 2M cap cold pairs, WIN-stopping rule active;
any WIN requires C++-gate + third-implementation pillars before any
adoption), declared separately.

Selection and scheduling only: NO verdict is claimed or implied.
Nodes and proxy values are never evidence of WIN or LOSS.  The
standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
