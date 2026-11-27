# n11 ultra-cheap u02 WIN-row canonical adoption: single-owner declaration (publish-then-execute)

- Date: 2026-11-27 (declared before execution; the maker executes after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly sessions: do not consume the u02 row or advance the canonical head.

## Scope

Consume exactly 1 row into the canonical head of record:

- u02 `1297036830121656320:131074` (class 2251, legal 80, s5 index 93815), WIN(1) nodes 3,167,121 at the 15M budget.

Pillar status (all 3/3, published): replica cold pair
(`n11-ultra-cheap-u02-escalation-15m-20261127`, commit `82d41abc`,
byte-identical pair), C++ second-implementation scrutiny gate
GATE-PASS `80,15000000,1,3167121` and third-implementation
CORROBORATION-PASS WIN(1) expansions 3,595,562 x2
(`n11-ultra-cheap-u02-win-pillars-20261127`, commit `843b9da4`).

## Head basis and expected merged shape

- BASE: `0ec4080d...` (merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache, 6,891 rows WIN 209 / LOSS 6,682, 288,628 bytes), fetched from main and sha-verified; u02 verified fresh/absent from BASE.
- Expected merged shape: **6,892 rows WIN 210 / LOSS 6,682** (6891+1 / 209+1 / 6682+0). Output name `merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache`.
- Merger: standing `s5_union_merge.py` `90711961...`, 3 runs, byte-identical required. Increment: 1 WIN row.

## Maker gates (fail-closed, all must pass before any output)

G0 pin shas (merger/policy/quarantine/BASE/gate source+headers) + published kit MANIFEST self-verification (26 files); G1 LIVE re-run of the published gate_runner.sh on a scratch copy of the pillars kit (2 fresh-cold C++ passes, node-exact vs the published raws); G2 re-parse of the three pillars (replica pair, gate pair, third-impl pair, legal 80); G3 freshness + duplicate + WIN/LOSS conflict vs BASE; G4 quarantine-free + canonical-safe per s5_evidence_policy (policy `78655e94...`, quarantine `81d23160...`); G5 increment build; G6 merge x3 byte-identical + shape check.

## Status guard

Adoption bookkeeping only. The adopted row is cache bookkeeping, NOT a class closure, NOT a root verdict, transfers nothing; the WIN-side flip-census review of class 2251's owner-class union is a SEPARATE follow-up Part (declared after adoption, per the standing pattern). The standard 11x11 empty board, the two-stone root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
