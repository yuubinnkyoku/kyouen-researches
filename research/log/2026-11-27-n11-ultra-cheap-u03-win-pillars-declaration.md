# n11 ultra-cheap u03 WIN-row pillars: single-owner declaration (publish-then-execute)

- Date: 2026-11-27 (declared before execution; executed after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly sessions: do not run the u03 key (`1153202979851993088:272`) at any budget or in any implementation; this declaration claims the u03 WIN-row pillar verification.

## Scope (exactly this one key, both pillars)

| id | key | class_index | legal | s5_index | escalation row |
|----|-----|-------------|-------|----------|----------------|
| u03 | 1153202979851993088:272 | 16371 | 78 | 550879 | WIN(1) nodes 2,909,040 @15M (n11-ultra-cheap-u03-escalation-15m-20261127, kit commit 36f0cd2c) |

- Pillar 1 (C++ second-implementation scrutiny gate): gate source `kyouen_dfpn_root.cpp` sha256 `9193f5b6...` with headers `kyouen_residual_micro.hpp` `5976935d...` and `n11_s5_quarantine.hpp` `2e36d694...` (byte-verified against the published u02 pillars kit), zig 0.13.0 build (tarball pin `d45312e6...`), fresh-cold pair per row (one process per pass), expected replay row pinned from the published escalation raw: `78,15000000,1,2909040`. Anchors (published-raw-pinned, run in the same kit): anchor-at2m expected `98,2000000,0,2000000` (budget 2M), anchor-aj001 expected `84,30000000,2,5156075` (budget 30M), anchor-af039 expected `89,30000000,2,19234232` (budget 30M). Tamper battery 4/4 fail-closed (pin flip / raw nodes edit / phantom row / head append).
- Pillar 2 (third-implementation corroboration): third_impl.js sha256 `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` (byte-verified, not republished here), `--row=u03 --stones=5 --legal=78 --lo=1153202979851993088 --hi=272 --cap=400000000 --wallcap=260 --memo-power=22`, two independent cold passes; expected verdict-level result WIN(1); expansions are MEASURED by this Part (not pre-registered).
- Head basis: 82b52577 (merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache, 6,892 rows WIN 210 / LOSS 6,682, 288,677 bytes), sha256-verified; u03 verified absent (fresh); u01/u02 WIN rows verified present.

## Pre-declaration disclosures

- No u03 run in any implementation or at any budget was performed before this declaration beyond the published escalation kit itself (whose declaration 37f1e9f6/u03u04 declaration fd41e986 covers those runs).
- The gate binary in this lane's work tree was rebuilt from the pinned source in a prior Part and its anchor rows re-verified there; this Part re-runs every row fresh-cold and re-verifies the anchors.

## Status guard

Pillar bookkeeping only. The u03 row stays single-implementation-until-adopted cache bookkeeping: this Part does NOT adopt it, does NOT consume any verdict, and a u03 adoption additionally requires the standing WIN-side flip-census review (class 16371 completion would be Board-verified free_now at adoption time). Nodes/expansions are bookkeeping, never evidence. The standard 11x11 empty board, the two-stone root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
