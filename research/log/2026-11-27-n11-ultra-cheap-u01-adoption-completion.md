# n11 ultra-cheap u01 WIN-row canonical adoption: completion log (2026-11-27)

Execution Part of the single-owner declaration
`research/log/2026-11-27-n11-ultra-cheap-u01-adoption-declaration.md`
(commit `7fe17f62`).  Kit:
`research/experiments/n11-ultra-cheap-u01-win-adoption-20261127`.

## Result

- **New canonical head of record:
  `merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache` sha256
  `0ec4080da825a344a8dbbe0835da80dd506b06fa45f9f926b401d2387f3ed1e5`,
  6,891 rows WIN 209 / LOSS 6,682** - exactly the pre-registered shape
  6,890+1 / 208+1 / 6,682+0.
- Increment (1 row, sha256 `5d2d89dd...`): u01
  `1153485622925590528:0` WIN(1) nodes 4,893,014 (bookkeeping).
- Fresh maker (structural descendant of the eleventh k01 adoption
  maker), 3 runs byte-identical (MAKER-PASS x3): G0 pins (merger
  `90711961`, policy `78655e94`, quarantine `81d23160`, BASE
  `1e2eeda2`, gate source `9193f5b6` + headers, both source kit
  MANIFESTs byte-fetched and fully re-verified), G1 LIVE re-run of the
  published gate_runner.sh on a scratch copy (2 fresh-cold C++
  passes, quadruple `88,15000000,1,4893014`, raw node-exact vs
  published), G2 re-parse of the three pillars, G3 freshness +
  duplicate + WIN/LOSS conflict review (none), G4 quarantine-free +
  canonical-safe, G6 merger 3 runs byte-identical with audits
  (`38ee5236...` x3).

## Honest disclosures

- The G1 live gate re-run is this lane's disclosed adaptation of the
  eleventh G1 (this lane's pillar kit ships the runner + raws + tamper
  battery instead of a separate audit script).
- The gate binary is the one built this session by this lane from the
  sha-verified pinned source (zig 0.13.0 `d45312e6`, -std=c++20 -O3);
  provenance is by disclosure plus the live node-exact re-run, not a
  rebuild inside the maker.
- The maker's G4 quarantine lookup used the policy script's
  parents[4]-relative registry path; the pinned quarantine file was
  staged there as a byte-identical copy.
- The replica, C++ gate and third-impl results this adoption consumes
  were produced and published earlier this session by this same lane.
- The merged cache is published via the chunked-read machine path
  (288,628 bytes); fetch-back verification below.

## What this does NOT mean

Adoption bookkeeping only.  NO root verdict is consumed, NO class
freed, NO class excluded: the class-1849 completion (free_now) would be
claimed only by the follow-up flip-census/reaudit Part under its own
declaration.  Nodes are bookkeeping, never verdicts.  The standard
11x11 empty board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.
The two-stone root {60,27} and its remaining third moves 100/108:
UNKNOWN.  All closure classes: UNKNOWN.

Next Part (candidate, fresh declaration required): u01 adoption
flip-census + reaudit refresh (BASE `1e2eeda2` vs SCEN `0ec4080d`,
measurer + refresh byte-clone of the eleventh reaudit kit
`2cd58330` template), then the next selection under the new head.
