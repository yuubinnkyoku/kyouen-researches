# Eighth-cost ladder pre-audit (2026-11-27)

Post-hoc independent integrity audit instrument for the eighth-cost
exclusive S5 ladder
(research/experiments/n11-eighthcost-class-s5-exclusive-probe-1297036692
75860288-20261127): 88 published raws (43 at2m cold pairs + the k01 at15m
cold pair), the selection JSON (691dcd80), the batch-summary ledger
(2379dbe0) and the canonical head 5b6e77f7.

DISCLOSED: unlike the seventh-cost pre-audit instrument (pre-registered
before any ladder raw), this instrument was written AFTER the eighth-cost
raws and ledger were published (post-hoc integrity audit, the same
standing as the seventh-cost instrument's first real run). It is a fresh
implementation structurally modeled on the published seventh-cost
instrument revision 2 (audit_seventh_ladder.py 5b47ac7f, disclosed), not a
byte transform.

## What it checks (596 fail-closed gates, all PASS on the official run)

- P0 pins: selection sha/schema/class/head basis, batch-summary
  sha/schema/class/counters (43 keys, 1 WIN, 0 LOSS, 0 parked, WIN
  stopping rule fired), head cache sha + census (6,874 rows WIN202 /
  LOSS6672) and freshness of ALL 43 selection key pairs ABSENT from the
  head (verdict-unconsumed).
- P1 raw manifest: 88/88 raw byte-verified against the published
  MANIFEST-raw-sha256.txt; exactly 86 at2m rows + 2 at15m rows (k01
  only); the raw tree equals the manifest exactly (no stray files).
- P2 raw rows: key provenance (file kNN == selection order position NN),
  legal, stage budget (2M/15M), UNKNOWN-at-budget, k01 WIN(1) nodes
  8514427 inside budget.
- P3 determinism: 43 at2m cold pairs + the k01 at15m cold pair identical
  on every replay field except wall_s.
- P4 ledger cross-consistency: per_key pos/key match the selection order,
  every ledger stage1_2m row equals the published raw pair, k01's 15M
  resolution matches the raw pair, keys 2..43 are recorded suppressed and
  have no 15M raw.
- P5 WIN-stop content invariant: the official 15M raw set contains ONLY
  the WIN key (the pre-registered "1 WIN suppresses 42 keys" rule,
  modeled content-level), no 50M stage exists, and the k02 post-anchor
  15M pair lives only in the ledger's overreach_disclosure (values
  result 0 / nodes 15000000 / pair identical) with no official raw.
- P6 guards: status_guard UNKNOWN wording, single-implementation note,
  nodes_bookkeeping counters.

Temporal anchor disclosure (recorded in the output JSON): the
batch-summary ledger was git-published in the SAME commit (0005e5b1) as
the raws, so it is NOT a proven-preceding temporal anchor (unlike the
seventh-cost 50M case); the WIN-stop check is the content invariant
above.

## Verification

- Official run: rc=0, 596/596 gates PASS, 3 runs byte-identical
  (output/eighth-preaudit.json sha256 5c1781265cfaccd91cf7d4abb3e70629
  6e25f46aeb4130108af0f7bbc7c467c).
- Tamper battery 4/4 fail-closed on a scratch copy (output/
  tamper-battery-stdout.log): T1 raw k01 at15m nodes edit -> P1:manifest-
  sha-all + P2:k01:at15m-win + P3:k01:at15m-pair-identity / T2 phantom
  k02 15M raw in the tree only -> P1:raw-tree==manifest + P4:k02:no-
  15m-raw / T3 full phantom forgery (tree + manifest) -> P1:manifest-
  count + P1:manifest-at15m-only-k01 + P4 + P5 x2 / T4 ledger byte flip
  -> P0:batch-summary-sha + P0:batch-summary-counters; clean control
  rc=0 byte-identical to the official output.

The instrument consumes NO verdict and asserts NOTHING about class
status or coverage. The k01 WIN row stays UNCONSUMED until a separately
declared adoption Part (all three implementation pillars now stand:
replica pair, C++ gate, third-impl corroboration). The standard 11x11
empty board, every central-reply root, the two-stone root {60,27}, its
remaining third moves {100,108}, S2, class 1/2/4 and all closure classes
stay UNKNOWN. Nodes are bookkeeping, never verdicts.
