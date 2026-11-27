# Eighth-cost k01 WIN row canonical adoption (2026-11-27)

Single-row canonical adoption of the eighth-cost k01 WIN row
(s5verdict,1297036692750860288,64,5,1,8514427) into the canonical head
of record BASE 5b6e77f7 (6,874 rows WIN 202 / LOSS 6,672), Part SZ
precedent in single-row form. Publish-then-execute under the wave A
declaration
(research/log/2026-11-27-n11-eighthcost-k01-win-adoption-declaration.md,
commit d809f8d3).

## Pillar eligibility (maker-verified live, gates all PASS, 2 runs
byte-identical)

- G0 BASE: head sha 5b6e77f7 + census 6,874/WIN202/LOSS6672, k01 pair
  ABSENT (freshness 1/1, WIN/LOSS conflicts 0).
- G1 replica: batch-summary 2379dbe0 (schema/class/counters: 43 keys,
  1 WIN, 0 LOSS, 0 parked, WIN stopping rule fired), at15m cold pair
  3be9db9b x2, WIN(1) nodes 8514427 inside budget 15000000, at2m stage
  pair UNKNOWN@2M pinned.
- G2 C++ gate: published kit 24/24 byte-verified, gate-rows pins,
  expected 84,15000000,1,8514427, LIVE audit re-run rc=0 (audit_gate:
  PASS, 31/31 gates).
- G3 third impl: kit 4/4 byte-verified, third_impl.js pin 08ea958f,
  both raw rows WIN(1) expansions 9987963 mutually identical.
- G4 merger: byte-clone of the pinned SV merger s5_union_merge.py
  (sha256 90711961...).

Kit layout: scripts/ (maker + pinned merger), output/
(increment-eighthcost-k01-win-adoption-20261127.cache,
adoption-manifest.json, then merged head + merge-audit-run{1,2,3}.json
from the run waves).

## Run record

PENDING (wave B published; wave C = 3 merger runs on [BASE head,
increment], expected merged 6,875 rows WIN 203 / LOSS 6,672, any
non-identity HARD-STOPs the adoption).

## Scope guards

The adoption consumes the k01 S5 row ONLY as cache bookkeeping: NO
root verdict, NO class freed, NO class excluded, NO coverage claim.
The 42 WIN-stopping-rule-suppressed keys are NOT adopted (they stay
UNKNOWN-pair-at-2M only, fresh vs BASE). The class-status flip review
(win-hit census measurement of the serving class 1297036692750860288:0
owner set, k05/Part-EM precedent) is declared as the FOLLOW-UP
measurement Part and is NOT part of this adoption. The standard 11x11
empty board, every central-reply root, the two-stone root {60,27}, its
remaining third moves {100,108}, S2, class 1/2/4 and all closure
classes stay UNKNOWN. Nodes are bookkeeping, never verdicts.

Disclosure: the maker's first build had a replay-column offset bug
(legal=budget/result=nodes mis-indexed) caught by its own G1 gates
before any emit; fixed and re-run from scratch (2 byte-identical runs).
