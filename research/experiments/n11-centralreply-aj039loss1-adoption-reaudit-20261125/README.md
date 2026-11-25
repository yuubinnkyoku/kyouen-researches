# n11-centralreply-aj039loss1-adoption-reaudit-20261125 (Part EL)

Loss-only canonical adoption of the single fresh exact-LOSS row **aj039**
(key (1152922606282735616, 65536), legal 88, s5_index 897668), probed by the
published Part EK 30M re-probe kit (two-pass fresh-cold node-exact, budget
30,000,000 order 0, nodes 16,549,916 per pass, MISMATCH 0, resolved in
(15M, 30M] beyond the honest EXHAUSTED 15M history of batch-39 - not a
same-condition re-probe).  Declaration:
`research/log/2026-11-25-part-el-aj039loss1-adoption-declaration.md`.

- BASE: the published Part EI canonical merged cache
  `merged-exact-s5-chain-plus-b39loss46-20261125.cache` (6,712 rows, WIN 158
  / LOSS 6,554, sha256 73482be0...).
- Pool source: the published Part EK kit
  `research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125/`
  (MANIFEST-sha256 rev2 97574401..., 42 files, audit_ek.json d9aa8aab...,
  79/79 gates PASS).
- NOT consumed: aj030 (probe-level WIN 15,284,699 at 30M, WIN-HALT,
  scrutiny-owner C++ second-implementation gate 9193f5b6... exclusive, sits in
  NO cache); ai044/ai048 (Part EF claim-reserved, untouched); aj049/aj050
  (batch-39 probe-level WINs, sit in NO cache).
- Scripts: `scripts/make_increments_el_adoption.py` (sha
  910ede30d49251d88ee83b778aa65486609fc0b8937a0b237fdaaf6ed38d1d17,
  EI-maker fork adapted to the Part EK artifacts, fail-closed), and the
  byte-clone of the pinned fail-closed union merger
  `scripts/s5_union_merge.py` (sha 90711961..., identical to the published
  Part EE/EI merger bytes).
- Protocol: publish-then-execute.  Maker 3x byte-identical + tamper battery
  (T-EL1 raw sha drift / T-EL2 status.log kit sha drift / T-EL3 BASE cache
  sha drift, each rc=1 fail-closed) + restored clean control, then merger 3x
  byte-identical (cache + merge-audit).  Outputs: increment
  `output/increment-aj039loss1-20261125.cache` (1,254 B, sha 7838b081...),
  `output/increments-manifest.json` (schema
  `ek-aj039loss1-increments-manifest-v1`, sha 34439f4d...), merged chain head
  `output/merged-exact-s5-chain-plus-aj039loss1-20261125.cache` (6,713 rows,
  WIN 158 / LOSS 6,555, sha cf08e181...), merge-audits x3 (sha 0ab05a15...
  each).  Reaudit refresh fork + delta extractor follow as waves D/E.
- **This unit consumes NO WIN verdict, asserts NO root verdict, frees NO
  class and excludes NO class.  The standard 11x11 empty board stays
  UNKNOWN; nodes are bookkeeping, never verdicts.**

Run record: pending (waves C-F).
