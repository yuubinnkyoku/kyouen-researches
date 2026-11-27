# 2026-11-27 n11 eighth-cost ladder pre-audit instrument: first real run

Post-hoc independent integrity audit of the eighth-cost exclusive S5
ladder checkpoint (kit n11-eighthcost-class-s5-exclusive-probe-
1297036692750860288-20261127): published as
research/experiments/n11-eighthcost-ladder-preaudit-20261127/.

DISCLOSED: this instrument was written after the eighth raws/ledger were
published (post-hoc, unlike the seventh-cost instrument which was
pre-registered before its raws). Fresh implementation structurally
modeled on the seventh-cost instrument revision 2 (5b47ac7f), not a byte
transform.

## Result

rc=0, 596/596 fail-closed gates PASS on the official 88-raw checkpoint:
- 88/88 raw bytes verified against MANIFEST-raw-sha256.txt (43 at2m cold
  pairs + k01 at15m cold pair); raw tree == manifest; kNN key provenance
  == selection order (691dcd80, 43 keys); budgets 2M/15M; all 2M rows
  UNKNOWN-at-budget; k01 WIN(1) nodes 8514427 inside budget.
- All 44 determinism pairs identical on every replay field except
  wall_s.
- Ledger (2379dbe0) cross-consistency: per_key 43, pos/key == selection
  order, stage1_2m == raw pairs, k01 15M resolution == raw pair, keys
  2..43 recorded "suppressed_by_win_stopping_rule" with no 15M raw.
- WIN-stop content invariant: official 15M raws exist ONLY for the WIN
  key; no 50M stage; the k02 post-anchor 15M pair (UNKNOWN, nodes
  15000000, pair identical) lives only in overreach_disclosure with no
  official raw.
- Freshness: ALL 43 selection key pairs ABSENT from the canonical head
  5b6e77f7 (6,874 rows WIN202/LOSS6672, sha-verified) - verdict-
  unconsumed.
- Temporal anchor disclosure (weaker than seventh-cost): the ledger was
  git-published in the SAME commit (0005e5b1) as the raws, so the WIN
  stop check is content-level, not git-temporal.

Verification: 3 runs byte-identical (output/eighth-preaudit.json sha256
5c1781265cfaccd91cf7d4abb3e70629d6e25f46aeb4130108af0f7bbc7c467c);
tamper battery 4/4 fail-closed on a scratch copy (T1 raw k01 nodes
edit, T2 phantom tree raw, T3 full phantom forgery with manifest, T4
ledger byte flip) + clean control rc=0 byte-identical.

This audit consumes NO verdict and asserts nothing about class status,
coverage or secured coverage. The k01 WIN row stays UNCONSUMED; its
three implementation pillars (replica cold pair 3be9db9b x2, C++ gate
GATE-PASS 84,15000000,1,8514427, third-impl CORROBORATION-PASS) now
stand, and adoption is a separately declared future Part with WIN/LOSS
conflict review. The standard 11x11 empty board, every central-reply
root, the two-stone root {60,27}, its remaining third moves {100,108},
S2, class 1/2/4 and all closure classes stay UNKNOWN. Nodes are
bookkeeping, never verdicts.
