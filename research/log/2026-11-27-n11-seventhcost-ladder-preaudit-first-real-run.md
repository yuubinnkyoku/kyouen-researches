# 2026-11-27 n11 seventh-cost ladder pre-audit: first real run (published raws, full checkpoint)

Lane: long-term lane (self-run). HEAD at start: 9ac8e079afcb78a7e0d6497e89aa4e7053ed0c7a.

## What ran

The pre-registered instrument
`research/experiments/n11-seventhcost-ladder-preaudit-20261126/scripts/audit_seventh_ladder.py`
(published in 9b22aa9a, self-tested against synthetic fixtures before any raw
existed) was executed for the first time against the real published ladder
raws of kit `research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/`
(waves 928dc19b / 64a46b4c / 24f40b8b).

Result: rc=0, 8,699 gates passed, checkpoint=full. Output published at
`research/experiments/n11-seventhcost-ladder-preaudit-20261126/output/ladder-preaudit.json`
(sha256 232e42eca776738a51d653946a4a749e329a1a2f8ff1ad4b1172f56baf4cb18d).

Coverage as reported by the instrument (bookkeeping only, no verdicts):
124 raw files audited, 42 keys with raws, 41 resolved keys (k01..k42 minus
k05, matching the single-owner checkpoint log 03b954e9: 41 exact-LOSS rows),
0 WIN keys (WIN stopping rule never fired), k05 parked UNKNOWN@15M
(L50M raise candidate), determinism pairs present for all 42 keys.

## Verification

- Input pins re-verified from scratch: selection JSON
  c395fe032f87ee6764ee24777b90140ca0aa05002abe9038a7c67d6ca12e627 and canonical
  head cache 42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4
  re-downloaded from main HEAD and sha-matched inside the instrument (its own
  fail-closed pin gates). All 124 raws re-downloaded from main HEAD and
  byte-matched against the kit's published MANIFEST-raw-sha256.txt (124/124).
- Determinism: 3 runs of the instrument produced byte-identical stdout and
  byte-identical output JSON (sha256 232e42ec... each time).
- Tamper battery on a scratch copy of the full tree (3/3 fail-closed,
  real raws, never published, deleted after the battery):
  - T1: nodes edit in at15m-run1-k01 (2986255 -> 2986254) -> rc=1,
    gate `pair_15m_01`;
  - T2: phantom raw at15m-run1-k43 (out-of-selection k-index) -> rc=1,
    gate `raw_kidx_at15m`;
  - T3: parked-key k05 15M nodes 15000000 -> 14999999 (UNKNOWN without full
    budget) -> rc=1, gate `raw_unknown_full_at15m`;
  - post-restore clean control rc=0 with stdout byte-identical to run1.
- No file of the seventh-cost kit, the cross-check kit or the pre-audit kit
  was modified on main by this run.

## Honest disclosure

- The run environment had no git; the repo tree needed by the instrument was
  reconstructed locally from raw.githubusercontent.com at main HEAD
  9ac8e079 (selection JSON, canonical head cache, audit script, 124 raws),
  all byte-pinned as above. The instrument was run from the reconstructed
  kit path so its repo-relative ROOT resolution was authentic.
- The kit's MANIFEST-raw-sha256.txt uses a 3-column format
  (sha256, size, path) and is not directly consumable by `sha256sum -c`;
  the byte-match was done column-parsed. No content difference found.
- One execution-environment reset occurred mid-download (retry loop with
  per-file sleeps exceeded the wall budget); the download was redone with a
  parallel fetch and all 124 files were re-verified from scratch afterwards,
  so no published artifact was affected.
- Single implementation: this is the pre-registered instrument itself; the
  41 LOSS rows remain single-implementation (jsreplay replica) rows. The
  C++ scrutiny gate and third-implementation corroboration for the
  seventh-cost batch are still open Parts (see checkpoint log 03b954e9).

## Status guard

This audit consumes nothing: no verdict, no class status, no cache increment.
Nodes and proxy values are bookkeeping and never evidence of WIN or LOSS.
The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise.

## Resume

- Next Part for the seventh-cost batch (per checkpoint log 03b954e9):
  C++ scrutiny gate over the 41 exact-LOSS rows (Part SR/SS pattern,
  gate-rows schema n11-seventhcost-...-rows-v1, 3 anchors + 41 targets),
  then third-implementation corroboration, then adoption Part
  (BASE = head cache 42dbb58f, fresh declaration and WIN/LOSS conflict
  review required). k05 remains parked UNKNOWN@15M (L50M raise candidate).
- The instrument can be re-run after any future raw publish (e.g. a k05
  L50M pair) and rewrites output/ladder-preaudit.json fail-closed.
