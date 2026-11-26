# n11 seventh-cost ladder pre-audit instrument pre-registered (2026-11-26)

The seventh-cost single-owner lane (declaration 8d8c3c5c, selection kit
2098c3ea) is running the k01..k42 exclusive ladder and will publish raw
checkpoints incrementally. This lane pre-registered, before any ladder raw
was published, a fail-closed independent audit instrument for those raws:

`research/experiments/n11-seventhcost-ladder-preaudit-20261126/scripts/audit_seventh_ladder.py`

- pins the selection JSON (c395fe03...) and the canonical head cache
  (42dbb58f...) fail-closed before any raw is read;
- per raw row: schema, stones, key provenance (key equals the selection's
  kNN key AND the filename k-index matches the selection order), legal
  count, stage budget (2M/15M/50M), result domain, nodes<=budget,
  UNKNOWN-implies-full-budget;
- stage policy of the pre-registered stopping rules: 2M-resolved keys need
  an identical second cold 2M run; 15M/50M rows require a 2M UNKNOWN; 15M
  cold pairs must be identical;
- WIN stopping rule: no raw beyond the first WIN key;
- coverage report only, consumes no verdict, no class status, no cache row.

Self-test with synthetic fixture rows (never published, deleted after the
battery): clean control rc=0 (6,959 gates), tamper battery 6/6 fail-closed
(determinism pair mismatch / filename-order provenance / WIN-stopping
violation / budget mismatch / out-of-selection key / stage violation), with
a post-battery restore and clean re-run. See the kit README and
output/selftest-fixture.json for the full disclosure.

The instrument has not yet been run against any real ladder raw; the first
real run belongs to whichever execution next sees published checkpoints.
No verdict is claimed, implied or consumed here. The standard 11x11 empty
board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root {60,27}:
UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN
unless a published Part says otherwise.
