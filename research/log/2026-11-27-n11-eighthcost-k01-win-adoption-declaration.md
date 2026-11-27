# 2026-11-27 n11 eighth-cost k01 WIN row adoption: declaration (wave A)

Publish-then-execute pre-registration of the eighth-cost k01 WIN row
canonical adoption (Part SZ precedent, single-row form). HEAD pin at
declaration: 2613b11a055698f27162afb6e6317a3b53e7ab12 (main head of
record at the time of this commit's parent).

## What is adopted

Exactly ONE row: the eighth-cost k01 WIN row
(key 1297036692750860288:64, legal 84, replica WIN(1) nodes 8514427 at
the 15M stage, cold pair both raws sha256 3be9db9b...):

    s5verdict,1297036692750860288,64,5,1,8514427

The canonical head of record advances from BASE 5b6e77f7
(merged-exact-s5-chain-plus-seventhcost42-20261127.cache, 6,874 rows
WIN 202 / LOSS 6,672) by consuming exactly this one published row.
Expected merged head: 6,875 rows WIN 203 / LOSS 6,672, produced by the
pinned SV merger byte-clone (s5_union_merge.py 90711961...), 3
byte-identical runs, conflict-free union (WIN/LOSS conflict review:
the k01 pair is ABSENT from BASE - machine-verified - so the conflict
count must be 0; any conflict aborts fail-closed).

## Pillar eligibility (all three stand, all re-verified live by the maker)

1. Replica cold pair: published eighth-cost kit at15m pair (3be9db9b
   x2), batch-summary ledger 2379dbe0 with the WIN stopping rule.
2. C++ second-implementation scrutiny gate: kit
   n11-eighthcost-k01-win-cppgate-20261127 (this date, HEAD lineage),
   GATE-PASS 84,15000000,1,8514427, audit 31/31 gates live re-run.
3. Third-implementation corroboration: kit
   n11-eighthcost-k01-win-thirdimpl-corroboration-20261127,
   CORROBORATION-PASS (third_impl 08ea958f, WIN(1) expansions 9987963
   x2 identical).

## Pre-registered stop rules

- The maker re-verifies every pinned byte from published main before
  emitting the increment; any pin mismatch -> rc=1, no emit.
- The merger runs 3x; any non-identity -> HARD-STOP, nothing published
  as merged head of record.
- The 42 suppressed keys are NOT adopted (their escalations were
  suppressed by the pre-registered WIN stopping rule; they stay
  UNKNOWN-pair-at-2M only, fresh vs BASE).
- The adoption consumes the k01 S5 row ONLY as cache bookkeeping: NO
  root verdict, NO class freed, NO class excluded, NO coverage claim.
  The class-status flip review (win-hit mechanism, k05/Part-EM
  precedent: census measurement of the serving class
  1297036692750860288:0 owner set) is declared as the FOLLOW-UP
  measurement Part and is NOT part of this adoption.
- The standard 11x11 empty board, every central-reply root, the
  two-stone root {60,27}, its remaining third moves {100,108}, S2,
  class 1/2/4 and all closure classes stay UNKNOWN. Nodes are
  bookkeeping, never verdicts.
