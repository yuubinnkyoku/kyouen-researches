# n11-eleventhcost-k01-win-cppgate-20261127

Eleventh-cost resolved-row C++ scrutiny gate (the single stage-15M
resolved row k01 WIN of class 1297036696978718720:0; replica raws
published in kit n11-eleventhcost-batch-stage1-2m-20261127, commit
aaeb282c; third-impl corroboration kit commit 26c7b04d). Eighteenth
execution of the C++ gate lineage. Scope, protocol, pins and stop
rules are pre-registered in the wave A declaration
(research/log/2026-11-27-n11-eleventhcost-k01-win-cppgate-declaration.md,
commit fa3c8681, publish-then-execute).

## Targets and result

- k01 `1297036696978718720:64`: **GATE-PASS `88,15000000,1,12755963`**
  (expected == published replica 15M cold pair, node-exact; WIN-side;
  7th WIN-side gate row of the lineage).
- Anchors: anchor-at2m `98,2000000,0,2000000` / anchor-aj001
  `84,30000000,2,5156075` / anchor-af039 `89,30000000,2,19234232`
  (GATE-PASS, byte-clones of the SW kit anchor inputs).
- Official execution 16:12:00Z-16:14:31Z sequential in the
  pre-registered order (output/gate-status.log). Two-pass node bill:
  k01 25,511,926 + anchors 4,000,000 + 10,312,150 + 38,468,464
  (bookkeeping).

## Pins

- Gate source kyouen_dfpn_root.cpp @154f3b7a sha256 9193f5b6... with
  headers kyouen_residual_micro.hpp (5976935d...) and
  n11_s5_quarantine.hpp (2e36d694...) (all included in scripts/ and
  sha-verified before the build); toolchain zig 0.13.0 (tarball
  d45312e6...), `zig c++ -O2 -std=c++20`; binary not pinned.
- Runner and audit: byte-clones of the published tenth-cost k01/k02
  gate kit runner and batch audit (G0-G6 fail-closed).
- Input pins: k01.input.csv byte-clone of the published eleventh-cost
  selection kit input (sha256 f8255dc7... in input/gate-rows.json);
  anchors byte-clones of the SW kit inputs.
- Freshness: the target [lo,hi] pair is ABSENT from the canonical
  head of record 16b34014... (6,889 rows WIN 207 / LOSS 6,682;
  byte-copy included as head.cache, sha-verified; absence
  machine-checked and re-verified by audit G6).
- head.cache in this kit is a byte-copy of
  research/experiments/n11-tenthcost-k01k02-adoption-20261127/output/merged/merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache
  (included so the audit is standalone re-runnable).

## Audit

- audit_gate.py (G0 input pins, G1 raw format, G2 pair equality, G3
  expected equality, G4 status-log consistency, G5 SW anchors block,
  G6 head sha + rows + target absence): PASS, 3 runs byte-identical
  (output/audit_gate_run{1,2,3}.json, sha256 dc22c062...).
- Tamper battery 4/4 fail-closed on scratch copies (T1 expected-pin
  flip k01 -> G3 / T2 raw k01.p1 nodes edit -> G2+G3 / T3 phantom
  GATE-PASS -> G4 / T4 head byte append -> G6) + clean control rc=0
  (output/tamper-battery-stdout.log, t{1..4}.out, clean.out).

## Honest disclosures

- The zig 0.13.0 download and gate binary build happened before the
  wave A declaration push (disclosed in the declaration as
  environment preparation); no row was executed before the push.
- The replica and third-impl results this gate corroborates were
  produced and published earlier this session by this same lane.
- The runner's p1/p2 wall_s fields differ per pass; timing is not
  evidence.

## Pillar status after this Part

The eleventh-cost k01 WIN row now has all three implementation
pillars (replica cold pair + C++ gate + third impl 08ea958f, all
verdict-level WIN(1)).  Remaining for the batch: the separately
declared adoption Part (fresh single-owner declaration, WIN/LOSS
conflict review, merger 90711961, flip-census review for the k01 WIN
row per the SZ/EM/ninth/tenth precedent, BASE 16b34014), and the 45
suppressed escalation keys (k02..k46) which stay 2M-UNKNOWN
bookkeeping.

This kit consumes NO verdict. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts.
