# 2026-11-27 n11 ninth-cost parked-3 L50M rows C++ scrutiny gate: single-owner declaration (wave A)

## Claim

This lane claims the C++ second-implementation scrutiny gate (Part
SR/SW/SX pattern) for the three ninth-cost stage-3 L50M resolved rows
k02 / k04 / k07 (wave B commit 41b331d1, `output/batch-summary-l50m.json`
of the ninth-cost exclusive-probe kit, schema
n11-ninthcost-parked3-l50m-summary-v1). Sixteenth execution of the C++
gate lineage.

Single-owner: no other lane has declared or published a C++ gate kit for
these three rows (main HEAD at push time is 2e8aed6a, commit list
machine-checked; the concurrent lanes' 4loss / 4lossrest / k12 gate kits
are disjoint targets). The third-implementation corroboration for the
same three rows is ALREADY PUBLISHED by this lane (kit
n11-ninthcost-parked3-l50m-thirdimpl-corroboration-20261127, commit
a8867e6a, CORROBORATION-PASS verdict-level); a GATE-PASS here brings
k02/k04/k07 to implementation-pillar parity (replica cold pair + C++
gate + third impl) and the whole ninth-cost ladder into the
adoption-eligible state.

Publish-then-execute: this declaration is pushed before any official
gate pass of k02/k04/k07 at budget 50000000 starts on this host.

## Targets (expected quadruples machine-derived from the published L50M cold pairs)

| key | s5 state (lo,hi) | expected (legal,budget,result,nodes) |
| --- | --- | --- |
| k02 | 1297036692683751424, 201326592 | 87,50000000,1,18123017 |
| k04 | 1152921504607903744, 536903680 | 98,50000000,2,24309957 |
| k07 | 1152923703765368832, 68719476736 | 96,50000000,1,27621128 |

## Pre-registered execution policy

- Gate source: `cpp/solvers/kyouen_dfpn_root.cpp` @ commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6..., with
  header pins kyouen_residual_micro.hpp 5976935d... and
  n11_s5_quarantine.hpp 2e36d694... (all byte-verified on this host).
  Built with zig 0.13.0 (tarball sha256 d45312e6..., byte-verified),
  `zig c++ -std=c++20 -O2` (std::popcount/countr_zero requirement);
  the binary is not pinned.
- Inputs: `input/k02.input.csv` (8c2a0438...), `input/k04.input.csv`
  (dc3bfeb4...), `input/k07.input.csv` (928a1b98...) byte-clones of the
  published ninth-cost kit inputs (pins == the L50M ledger `inputs`
  block, byte-verified); anchors anchor-at2m / anchor-aj001 /
  anchor-af039 byte-clones of the published SW kit anchor inputs
  (pins ecc0299b... / 2f6daea5... / e51a3c9d..., byte-verified), with
  the SW kit anchors block quadruples.
- Execution order (pre-registered): anchor-at2m, anchor-aj001,
  anchor-af039, then k02, k04, k07 at budget 50000000. Two fresh-cold
  passes per row (one process per pass). Acceptance per row: p1 == p2
  on every replay field except wall_s AND p1 == expected quadruple
  (GATE-PASS); any mismatch, crash, or published-row disagreement:
  HARD-STOP, fail-closed, no interpretation.
- Runner: `scripts/gate_runner.sh` is a byte-clone of the published
  n11-ninthcost-4loss-cppgate runner (comment-block-only transform;
  code lines machine-identical, asserted at assembly).
- Audit: batch fail-closed audit, DISCLOSED ADAPTATION of the published
  n11-ninthcost-4lossrest-cppgate batch audit (target pins, budgets,
  key-pairs and schema names changed to the parked3-L50M values; G0-G6
  semantics unchanged, canonical-head freshness re-verification G6 via
  N9_HEAD, no skip). Tamper battery: 4-mode adaptation (T1 expected-pin
  flip k02 / T2 raw k02.p1 nodes edit / T3 phantom GATE-PASS / T4 head
  byte append), scratch copies only.

## Freshness basis

Canonical head of record at declaration time: sha256
0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4
(`merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache`, 6,875 rows
WIN 203 / LOSS 6,672, 287,808 bytes), fetched and byte-verified on this
host. Machine-checked: all three (lo,hi) pairs are ABSENT from the head
cache (3/3). No ninth-cost adoption Part has been published on main;
verdict-unconsumed at declaration, run and publication time.

## Disclosed pre-declaration host sanity runs (published budgets only)

- anchor-at2m @2M (published anchor budget): observed
  98,2000000,0,2000000 - node-exact vs the SW kit anchor quadruple.
- Gate binary built and `--help` smoke-tested; no target-row or anchor
  30M pass has been run by this lane before this push.

## Guards

Verdict NOT consumed. The three rows stay gate-verified UNCONSUMED
labels; a WIN(1)/LOSS(2) gate result is only a verdict-level agreement
of the second implementation with the published first-implementation
L50M cold pairs. The standard 11x11 empty board: UNKNOWN. All 19
central-reply roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN unless
a published Part says otherwise. Nodes are bookkeeping, never verdicts.
S5 raws are not class closure claims and not routes to the root
certificate.
