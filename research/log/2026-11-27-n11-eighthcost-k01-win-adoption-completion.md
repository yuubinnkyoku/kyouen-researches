# 2026-11-27 n11 eighth-cost k01 WIN row adoption: completion log

Publish-then-execute adoption (Part SZ precedent, single-row form) of
the eighth-cost k01 WIN row into the canonical S5 head of record.
Declaration: research/log/2026-11-27-n11-eighthcost-k01-win-adoption-
declaration.md (wave A commit d809f8d3).

## Commit chain

- Wave A declaration `d809f8d3`: single adopted row
  s5verdict,1297036692750860288,64,5,1,8514427; BASE 5b6e77f7 (6,874
  rows WIN202/LOSS6672); expected merged 6,875 rows WIN203/LOSS6672;
  3-pillar eligibility; 42 suppressed keys NOT adopted; class-flip
  census declared as the follow-up Part.
- Wave B kit `5f0430a3`
  (research/experiments/n11-eighthcost-k01-win-adoption-20261127/):
  maker gates all PASS, 2 runs byte-identical (G0 BASE sha+census+k01
  absent; G1 replica batch-summary 2379dbe0 + at15m pair 3be9db9b x2 +
  WIN(1) 8514427; G2 C++ gate kit 24/24 + LIVE audit rc=0; G3
  third-impl kit 4/4 + third_impl 08ea958f + WIN(1) expansions 9987963
  x2; G4 merger byte-clone 90711961); single-row increment +
  adoption-manifest v1 emitted.
- Wave C merged head `62bf0241`: 3 byte-identical merger runs
  (07:19:09Z, conflict-free, dup_elided 0):
  **merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache, sha256
  0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4,
  6,875 rows WIN 203 / LOSS 6,672** - exactly the pre-registered
  expectation. Fetch-back byte-identical (merged cache 287,808 B +
  merge-audit-run{1,2,3}.json all 589617a6).
- Wave D: README run record + refreshed MANIFEST (9 files) + this log.

## Canonical state after this Part

The canonical head of record advances 5b6e77f7 -> **0935c94c** (6,875
rows WIN203/LOSS6672). All future selections, probes and adoptions use
0935c94c as BASE.

## Honest disclosures

- The maker's first build had a replay-column offset bug (budget/result
  mis-indexed) caught by its own G1 gates before any emit; fixed and
  re-run from scratch (disclosed in the README).
- The 42 WIN-stopping-rule-suppressed keys stay UNKNOWN-pair-at-2M
  only; nothing about them was adopted or resolved.
- The class-status flip review (win-hit census measurement of the
  serving class 1297036692750860288:0 owner set, k05/Part-EM precedent)
  is NOT done here; it is the declared follow-up measurement Part
  (SZ wave E precedent: census measurer + reaudit refresh against the
  new head).

## Status guards

NO root verdict is consumed: the adoption is S5 cache bookkeeping only.
The standard 11x11 empty board, every central-reply root, the two-stone
root {60,27}, its remaining third moves {100,108}, S2, class 1/2/4 and
all closure classes stay UNKNOWN. WIN(1) rows transfer nothing to roots;
nodes are bookkeeping, never verdicts. No coverage, secured-coverage or
class-freed claim is made.
