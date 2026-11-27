# n11-seventhcost-ladder-preaudit-20261126

Pre-registered independent audit instrument for the seventh-cost exclusive S5
ladder raws of kit
`research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/`
(the single-owner lane declared in 8d8c3c5c and published its selection kit in
2098c3ea; the ladder checkpoints land incrementally in that kit's
`output/raw/`). This kit was written and self-tested by an independent lane
(the same lane that published the selection cross-check 8bad4b41) BEFORE any
ladder raw was published, so it can serve as a ready-made, fail-closed
verifier for every future checkpoint of the ladder.

## Instrument

`scripts/audit_seventh_ladder.py` (fail-closed, no verdict logic) audits
whatever raw rows exist under the ladder kit's `output/raw/`:

- pins: selection JSON sha256 c395fe03... and canonical head cache sha256
  42dbb58f... (fail-closed before anything else);
- per raw file: jsreplay row schema (11 columns), stones=5, key provenance
  (the raw key must be the selection's kNN key AND the file's k-index must
  match the selection order), legal count equals the selection legal,
  budget equals the stage budget (at2m*=2,000,000, at15m*=15,000,000,
  at50m*=50,000,000), result in {0,1,2}, nodes<=budget, and result 0
  (UNKNOWN) implies nodes==budget;
- stage policy per the pre-registered stopping rules: a 2M-resolved key
  requires an identical second cold 2M run (determinism pair); 15M/50M rows
  require a 2M UNKNOWN; a 15M cold pair must have identical (result, nodes);
- WIN stopping rule: no raw may exist for any ladder key beyond the first
  WIN key;
- coverage report: resolved / parked / pair-present key lists, partial vs
  full checkpoint;
- consumes nothing: no class status, no cache increment, no verdict.

Run it any time against the current main checkout
(`python3 scripts/audit_seventh_ladder.py` from this kit); it writes
`output/ladder-preaudit.json`.

## Self-test (fixture battery, disclosed)

`output/selftest-fixture.json`: synthetic jsreplay-format fixture rows over
the published k01..k05 keys exercised the instrument end to end (clean
control rc=0 with 6,959 gates; tamper battery 6/6 fail-closed: determinism
pair mismatch, filename/key-order provenance, WIN-stopping violation, budget
mismatch, out-of-selection key, 15M-after-resolution stage violation, plus
post-battery restore with a clean control re-run). The fixture rows were
synthetic, were never pushed to the seventh-cost kit, and were deleted after
the battery; the instrument had NOT been run against any real ladder raw at
publication time.

## First real run (2026-11-27, published raws)

Executed against the published full checkpoint (waves 928dc19b / 64a46b4c /
24f40b8b at HEAD 9ac8e079): rc=0, 8,699 gates passed, checkpoint=full.
`output/ladder-preaudit.json`
(sha256 232e42eca776738a51d653946a4a749e329a1a2f8ff1ad4b1172f56baf4cb18d):
124 raws audited, 42 keys with raws, 41 resolved keys (k05 parked
UNKNOWN@15M), 0 WIN keys, determinism pairs present for all 42 keys.
Determinism: 3 runs byte-identical. Tamper battery on the real raws (scratch
copy, deleted): 3/3 fail-closed (nodes edit -> pair_15m_01; phantom
out-of-selection k43 raw -> raw_kidx_at15m; parked-key nodes without full
budget -> raw_unknown_full_at15m); post-restore clean control rc=0
byte-identical. Inputs re-pinned from scratch (selection JSON c395fe03...,
head cache 42dbb58f..., 124/124 raws byte-matched against the kit's
MANIFEST-raw-sha256.txt). Full record:
`research/log/2026-11-27-n11-seventhcost-ladder-preaudit-first-real-run.md`.
Coverage numbers are bookkeeping only; no verdict is consumed or implied.

## Status guard

Audit instrument only; nothing here claims, implies or consumes any verdict.
Nodes and proxy values are never evidence of WIN or LOSS. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class:
UNKNOWN unless a published Part says otherwise.
