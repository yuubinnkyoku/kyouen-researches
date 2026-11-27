# 2026-11-27 n11 eleventh-cost k01 WIN row C++ scrutiny gate (single-owner declaration)

Wave A declaration, publish-then-execute.  Target: the eleventh-cost
batch k01 WIN row, key `1297036696978718720:64` (legal 88, replica
jsreplay 84585617 stage 15M WIN(1) nodes 12,755,963 cold pair
node-identical, kit commit aaeb282c; third-implementation
corroboration CORROBORATION-PASS, kit commit 26c7b04d).  This is the
C++ second-implementation pillar; eighteenth execution of the C++
gate lineage (EN/EO/EQ/ET/SW/SX/SY/SR/ninth-k01k02-parked3-L50M/
tenth-k01k02 lineage).

## Pre-registered protocol

- Expected quadruple (SSOT = published replica raw): k01
  `88,15000000,1,12755963` (WIN-side row).
- Gate source kyouen_dfpn_root.cpp @154f3b7a sha256 9193f5b6... with
  headers kyouen_residual_micro.hpp (5976935d...) and
  n11_s5_quarantine.hpp (2e36d694...) - byte-clones fetched from main
  and sha-verified on this host; toolchain zig 0.13.0 (tarball sha256
  d45312e6... verified), `zig c++ -O2 -std=c++20`; binary not pinned.
- Runner: byte-clone of the published tenth-cost k01/k02 gate runner.
  Audit: byte-clone of the published tenth-cost batch audit
  (G0-G6 fail-closed), with head basis 16b34014 (6,889 rows WIN 207 /
  LOSS 6,682) and the single eleventh-cost target row.
- Anchors (byte-clones of the SW kit anchor inputs), pre-registered
  order and expectations: anchor-at2m `98,2000000,0,2000000` /
  anchor-aj001 `84,30000000,2,5156075` / anchor-af039
  `89,30000000,2,19234232`.
- Input pins: k01.input.csv = byte-clone of the published eleventh-cost
  selection kit input (sha256 in input/gate-rows.json); head.cache =
  byte-copy of the canonical head of record
  merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache
  (16b34014..., 6,889 rows), target [lo,hi] absent (freshness
  machine-checked).
- Acceptance: two fresh-cold passes per row, pair equality on
  (legal,budget,result,nodes), equality to the expected quadruple;
  any mismatch/crash = HARD-STOP, fail-closed.  Audit 3 runs
  byte-identical + tamper battery 4/4 fail-closed + clean control.

## Honest disclosures

- The zig 0.13.0 download and the gate binary build happened before
  this wave A push (environment preparation, per the tenth-cost gate
  precedent); no row was executed before the push.
- The replica and third-impl results this gate corroborates were
  produced and published earlier this session by this same lane.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Gate bookkeeping only: NO verdict is consumed.  The standard 11x11
empty board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN.  Third-move pair {100,108}: UNKNOWN.
Nodes are bookkeeping, never verdicts.
