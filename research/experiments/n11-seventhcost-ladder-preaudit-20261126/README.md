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

## Revision 2: 50M-stage modeling (2026-11-27)

Revision 1 (script sha256 89e816dc..., superseded) audited 2M/15M raws only:
it had no pair_50m determinism gate, did not resolve or park keys at the
50M stage, and its WIN stopping rule compared ladder key order, which
false-fails once the k05 50M WIN raws (published in d08d4ddd, after the
15M raws of k06..k42) are integrated: key order is not temporal order.

`scripts/audit_seventh_ladder.py` (revision 2, fail-closed) adds:

- pin: batch-summary checkpoint sha256 6881eaaf... (the ledger; git-published
  in wave C3 commit 24f40b8b, strictly BEFORE any 50M raw existed) plus
  schema/class/head-basis/counter gates and ledger-vs-raw cross-consistency
  (every ledger stage1_2m equals the published at2m raw; every ledger
  resolution 2M/15M matches the raw pair rows; every ledger park matches
  raw 15M UNKNOWN pairs);
- unconditional gate: every raw 15M start must be accounted for by the
  ledger (a 15M raw for a key the ledger does not account is a post-anchor
  start and fails);
- 50M stage: rows only for keys the ledger parked UNKNOWN at 15M, only
  after the 15M pair exists, with a mandatory identical cold pair
  (pair_50m); result 1 resolves WIN, 2 resolves LOSS, 0 parks at 50M
  (nodes==budget already gated);
- temporal WIN stopping rule (replaces the key-order rule): if any WIN is
  resolved at any stage, then all keys with raws, all 15M starts and all 50M
  escalations must predate the ledger anchor or descend from ledger-parked
  keys; no key-order comparison is made. The ledger pin (git publication
  order) is the temporal anchor.

Second real run (revision 2, 2026-11-27, published raws at HEAD d08d4ddd):
rc=0, 9,211 gates passed, checkpoint=full. `output/ladder-preaudit.json`
(sha256 28e4f9244fc4598728843225bfc7b8ee009098196a147e8a995fb7642c605ad0):
126 raws audited (124 MANIFEST raws + 2 at50m raws), 42 keys with raws,
42 resolved keys (41 exact LOSS + k05 exact WIN at 50M), 0 parked keys,
escalated_50m_keys=[k05], determinism pairs present for all 42 keys (2M
pairs k16/k17, 15M pairs for the 40 keys, pair_50m for k05). Determinism: 3
runs byte-identical. Tamper battery on the real raws (scratch copy, deleted):
6/6 fail-closed (pair_50m nodes edit; phantom 50M escalation of non-parked
k06; batch-summary byte tamper; phantom post-anchor 15M start for k16; 50M
budget flip; missing 50M pair); post-restore clean control rc=0
byte-identical. Inputs re-pinned from scratch: selection JSON c395fe03...,
head cache 42dbb58f..., batch-summary 6881eaaf..., 124/124 raws byte-matched
against the kit's MANIFEST-raw-sha256.txt, at50m pair byte-identical
(ff750cc6... x2). Full record:
`research/log/2026-11-27-ladder-preaudit-50m-modeling-revision.md`.

The WIN row of k05 is single-implementation (Node replica) at audit time;
this instrument checks integrity and stopping-rule consistency only, and
consumes or implies no verdict.

## Status guard

Audit instrument only; nothing here claims, implies or consumes any verdict.
Nodes and proxy values are never evidence of WIN or LOSS. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class:
UNKNOWN unless a published Part says otherwise.
