# n11-tenthcost-k01k02-cppgate-20261127

Tenth-cost resolved-row C++ scrutiny gate (the two stage-2 15M
resolved rows k01/k02 of class 1297036692683751424:131072; replica
raws published in kit n11-tenthcost-batch-stage1-2m-20261127,
commits b8049d8b / 3485348c). Seventeenth execution of the C++ gate
lineage. Scope, protocol, pins and stop rules are pre-registered in
the wave A declaration
(research/log/2026-11-27-n11-tenthcost-k01k02-cppgate-declaration.md,
commit 506c5f16, publish-then-execute).

## Targets and result

- k01 `1297036692683751424:131074`: GATE-PASS
  `86,15000000,2,6783438` (expected == published replica 15M cold
  pair, node-exact).
- k02 `1297036692683751424:131136`: GATE-PASS
  `84,15000000,1,8799140` (WIN-side; 6th WIN-side gate row of the
  lineage).
- Anchors: anchor-at2m `98,2000000,0,2000000` / anchor-aj001
  `84,30000000,2,5156075` / anchor-af039 `89,30000000,2,19234232`
  (GATE-PASS, byte-clones of the SW kit anchor inputs).
- Official execution 14:22:50Z-14:25:48Z sequential in the
  pre-registered order (output/gate-status.log). Two-pass node bill:
  k01 13,566,876 / k02 17,598,280 + anchors 4,000,000 + 10,312,150 +
  38,468,464 (bookkeeping).

## Pins

- Gate source kyouen_dfpn_root.cpp @154f3b7a sha256 9193f5b6... with
  headers kyouen_residual_micro.hpp (5976935d...) and
  n11_s5_quarantine.hpp (2e36d694...) (all included in scripts/ and
  sha-verified before the build); toolchain zig 0.13.0 (tarball
  d45312e6...), `zig c++ -O2 -std=c++20`; binary not pinned.
- Runner: byte-clone of the published n11-ninthcost-parked3-l50m
  runner, comment-block-only transform, code lines machine-identical
  (asserted at assembly).
- Input pins: k01/k02 byte-clones of the published tenth-cost
  selection kit inputs (sha256 in input/gate-rows.json, verified
  against the selection kit MANIFEST); anchors byte-clones of the SW
  kit inputs.
- Freshness: both target [lo,hi] pairs ABSENT from the canonical head
  of record 47280073... (6,887 rows WIN 206 / LOSS 6,681; byte-copy
  included as head.cache, sha256-verified; absence machine-checked at
  assembly and re-verified by audit G6). Verdict-unconsumed at
  declaration, run and publication time.
- head.cache in this kit is a byte-copy of
  research/experiments/n11-ninthcost-12row-adoption-20261127/output/merged/merged-exact-s5-chain-plus-ninthcost12-20261127.cache
  (included so the audit is standalone re-runnable).

## Audit

- Fresh batch audit scripts/audit_gate.py (G0 input pins, G1 raw
  format, G2 pair equality, G3 expected equality, G4 status-log
  consistency, G5 SW anchors block, G6 head sha + rows + target
  absence): PASS, 3 runs byte-identical (output/audit_gate_run{1,2,3}.json,
  sha256 36d85e52...).
- Tamper battery 4/4 fail-closed on scratch copies (T1 expected-pin
  flip k01 -> G3 / T2 raw k01.p1 nodes edit -> G2+G3 / T3 phantom
  GATE-PASS -> G4 / T4 head byte append -> G6) + clean control rc=0
  (output/tamper-battery-stdout.log).

## Honest disclosures

- The audit's first implementation had a column-index bug (compared
  fields 1/3/4/5 = stones/is_or/budget/result instead of 2/4/5/6 =
  legal/budget/result/nodes); its own G3 gate failed closed on every
  row and the fixed audit was re-run 3x byte-identical. No raw was
  affected; the runner and raws predate the audit.
- The zig build happened before the wave A declaration push (disclosed
  in the declaration as environment preparation); no row was executed
  before the push.
- The replica and third-impl results this gate corroborates were
  produced and published earlier this session by this same lane.
- The runner's p1/p2 wall_s fields differ per pass; timing is not
  evidence.

## Pillar status after this Part

Both resolved tenth-cost rows (k01 LOSS, k02 WIN) have all three
implementation pillars (replica cold pair + C++ gate + third impl
08ea958f). Remaining for the batch: the separately declared adoption
Part (fresh single-owner declaration, WIN/LOSS conflict review,
merger 90711961, flip-census review for the k02 WIN row per the SZ/EM
precedent, BASE 47280073), and the 42 suppressed escalation keys
(k03..k44) which stay 2M-UNKNOWN bookkeeping.

This kit consumes NO verdict. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts.
