# n11 ultra-cheap u04 WIN-row pillars: single-owner declaration (publish-then-execute, third-implementation corroboration only)

- Date: 2026-11-27 (declared before execution; executed after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly sessions: do not run this key's pillar verification; this declaration claims the third-implementation corroboration of the single row below.

## Scope (exactly this one row, one pillar)

| id | key | class_index | legal | s5_index | escalation result |
|----|-----|-------------|-------|----------|-------------------|
| u04 | 1152921505747697664:1032 | 23101 | 85 | 745184 | WIN(1) nodes 9,149,084 @15M (kit n11-ultra-cheap-u04-escalation-15m-20261127, commit 24c5b85f) |

- Third implementation: third_impl.js sha256 08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998 (byte-fetched from published main and sha256-verified; the same pinned script as the u01/u02/u03 pillar kits). Non-df-pn AND/OR minimax with completion-memo, independent of the jsreplay replica.
- Invocation: --row=u04 --stones=5 --legal=85 --lo=1152921505747697664 --hi=1032 --cap=400000000 --wallcap=260 --memo-power=22. Two fresh-cold passes (separate processes).
- Acceptance: both passes return result 1 (A wins) with identical expansion counts; expansions are MEASURED by this Part (not pre-registered), mirroring the u03 pillar kit.
- Expected verdict corroboration: result 1 consistent with the WIN(1) escalation row. If either pass returns 0 or 2, or the passes disagree, that is a HARD-STOP corroboration failure recorded as an experimental fact.

## Honest disclosure: the C++ scrutiny gate pillar is NOT claimed here

This environment has no C/C++ toolchain and package installation is forbidden, so the C++ second-implementation scrutiny gate (source 9193f5b6..., previously built via zig 0.13.0, tarball pin d45312e6) CANNOT be executed in this session. The gate pillar remains REQUIRED and OPEN: no adoption of the u04 row may proceed until a GATE-PASS kit for this row exists. This Part claims only the third-implementation corroboration pillar; it does not weaken the two-pillar requirement in any way.

## Pre-declaration disclosures

- No u04 pillar run of any kind was performed before this declaration. The only runs performed under the head c5082866 in this session are the published escalation cold pair (after its own declaration 236db1b7).
- No other key will be run at any budget in this Part.

## Status guard

Verification bookkeeping only. The u04 WIN row stays single-adoption-blocked: adoption requires BOTH the C++ gate GATE-PASS and this third-implementation corroboration, plus the standing WIN-side flip-census review after adoption. No verdict is consumed; nodes/expansions are bookkeeping, never evidence. The standard 11x11 empty board, the two-stone root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
