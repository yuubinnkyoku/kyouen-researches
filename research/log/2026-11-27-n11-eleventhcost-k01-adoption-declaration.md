# 2026-11-27 n11 eleventh-cost k01 WIN row canonical adoption (single-owner declaration)

Wave A declaration, publish-then-execute.  Scope: adopt exactly the
one published eleventh-cost resolved row into the canonical head of
record.

## Adopted row (3/3 pillars, all verdict-level WIN(1))

- k01 `1297036696978718720:64`, result WIN(1), nodes 12,755,963
  (bookkeeping).
  - Replica pillar: jsreplay 84585617 15M cold pair node-identical
    (kit n11-eleventhcost-batch-stage1-2m-20261127, commit aaeb282c).
  - C++ gate pillar: GATE-PASS `88,15000000,1,12755963` node-exact
    (kit n11-eleventhcost-k01-win-cppgate-20261127, commit 25cef9e9).
  - Third-impl pillar: CORROBORATION-PASS verdict-level, WIN,
    expansions 15,339,759 x2 identical
    (kit n11-eleventhcost-k01-win-thirdimpl-corroboration-20261127,
    commit 26c7b04d).

## Pre-registered merged shape

- BASE: canonical head of record
  merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache (sha256
  16b34014..., 6,889 rows WIN 207 / LOSS 6,682).
- Increment: 1 row (k01 WIN).  Expected merged shape: 6,890 rows,
  WIN 208, LOSS 6,682 (6,889+1 / 207+1 / 6,682+0).
- Merger: s5_union_merge.py pin 90711961..., 3 runs required
  byte-identical with audits; WIN/LOSS conflict review vs BASE
  (same [lo,hi] with different verdict aborts); freshness (the row
  must be ABSENT from BASE - it is fresh by construction, verified
  by the selector and gate audit G6); quarantine-free and
  canonical-safe per s5_evidence_policy (78655e94...).
- Maker: machine-derived structural adaptation of the published
  tenth-cost adoption maker (c153f6f2...): single row, eleventh-cost
  kit paths/commits, BASE/OUT shapes; live re-run of the published
  C++ gate audit as in the tenth maker.

## After this Part

The flip-census/reaudit review of the serving class
`1297036696978718720:0` owner set is a separate follow-up Part (SZ/
EM/ninth/tenth precedent).  The 45 suppressed keys (k02..k46) stay
2M-UNKNOWN bookkeeping.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO class excluded.  The standard 11x11 empty board: UNKNOWN.
All 19 central-reply roots: UNKNOWN.  Two-stone root {60,27}:
UNKNOWN.  Third-move pair {100,108}: UNKNOWN.  This lane runs
without access to the user's computer (scheduled task); publication
is via the GitHub API only.
