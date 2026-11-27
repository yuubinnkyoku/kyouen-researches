# 2026-11-27 n11 eighth-cost k01 WIN row C++ scrutiny gate: declaration (wave A)

Part of the eighth-cost lane (class 1297036692750860288:0 exclusive S5 probe).
Publish-then-execute pre-registration of the delegated pinned C++
second-implementation scrutiny gate on the SINGLE eighth-cost WIN row k01
(key 1297036692750860288:64, legal 84). This is the gate-lineage successor
of EN/EO/EQ/ET/EV/SK/SM/SN/SR/SW/SX (Part SX = the seventh-cost k05
L50M WIN row precedent, the closest structural template: single
WIN-side target + 3 calibration anchors).

HEAD pin at declaration: 25c61034a572ee07b426c236bf05cb49151f2333
(main head of record at the time of this commit's parent).

## Pre-registered target

- Target: k01 at exact-replay budget 15000000.
- Expected quadruple (machine-derived from the published at15m cold
  pair, both raws sha256 3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d
  6999f7bc9a0376075479062): legal=84, budget=15000000, result=1 (WIN),
  nodes=8514427.
- Published stage policy pinned: the at2m cold pair (UNKNOWN@2M,
  nodes=2000000) precedes the 15M escalation; the published batch
  summary records the WIN stopping rule firing after k01 (42 keys
  escalation suppressed) and the overreach disclosure for the
  post-WIN k02 15M pair (not official).
- Third-implementation corroboration: ALREADY PUBLISHED
  (CORROBORATION-PASS, third_impl 08ea958f, WIN(1) expansions 9987963
  x2 identical cold passes). If this gate PASSes, k01 reaches
  implementation-pillar parity with the k05 precedent (replica cold
  pair + C++ gate + third impl) and becomes adoption-eligible under a
  separately declared adoption Part with WIN/LOSS conflict review.

## Anchors (calibration, run before the target)

anchor-at2m / anchor-aj001 / anchor-af039: byte-clones of the
published Part SW kit inputs, expected quadruples equal to the SW kit
anchors block:
- anchor-at2m: 98,2000000,0,2000000
- anchor-aj001: 84,30000000,2,5156075
- anchor-af039: 89,30000000,2,19234232

## Pins

- Gate source: cpp/solvers/kyouen_dfpn_root.cpp @ 154f3b7a67b97e13
  acbaee8b04dc74ddca728d19 (sha256 9193f5b6065e0fbcad2ef7c65f386187
  701cafa1f5b718cc35a5cbb0d138f92e), headers kyouen_residual_micro.hpp
  5976935d..., n11_s5_quarantine.hpp 2e36d694... (same SW/SX lineage).
- Toolchain: zig 0.13.0 (tarball sha256 d45312e6...), zig c++ -O2
  (binary itself not pinned).
- k01 input: byte-clone of the published eighth-cost kit
  input/k01.input.csv (manifest pin a5a18d5e057d7ad87dca39dd17a28057
  c68554ebb16e40b02d080e50580f923b).
- Canonical head of record: 5b6e77f7 (merged-exact-s5-chain-plus-
  seventhcost42-20261127.cache, sha256 5b6e77f7d7832d4ce84cb1f080a93e06
  66eb052dcf8b817e5d560f95499fcdde2, 6,874 s5verdict rows WIN202 /
  LOSS6672). Freshness: the k01 [lo,hi] pair (1297036692750860288,64)
  is ABSENT from the head (verdict-unconsumed at declaration, run and
  publication time; machine-verified).
- Runner: the published SW/SX runner rev2 transform (comment block
  only), 2 fresh-cold passes per row, HARD-STOP on any mismatch.
- Audit: FRESH single-row fail-closed implementation (Part SS/SX
  precedent, disclosed), plus a 3-case tamper battery fail-closed
  check and a clean control.

## Stop rules

- Anchors first (pre-registered order at2m, aj001, af039), then the
  single k01 target. Any anchor disagreement = HARD-STOP, target not
  run.
- Acceptance: p1 == p2 on (legal,budget,result,nodes); both == the
  published quadruple. No interpretation of a partial or mismatching
  result (C5).
- This gate consumes NO verdict. The standard 11x11 empty board,
  every central-reply root, the two-stone root {60,27}, its remaining
  third moves {100,108}, S2, class 1/2/4 and all closure classes stay
  UNKNOWN. WIN(1) raw rows transfer nothing; nodes are bookkeeping.
