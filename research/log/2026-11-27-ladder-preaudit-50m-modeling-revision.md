# 2026-11-27 ladder pre-audit instrument revision 2: 50M-stage modeling

Lane: pre-audit lane (independent of the seventh-cost owner lane).
Base: main HEAD d08d4ddd (2026-11-27T01:21:55Z), re-fetched immediately
before every push. No branch, no PR, direct-to-main per AGENTS.md.

## S1. Context and motivation

The published first real run of `audit_seventh_ladder.py` (revision 1,
sha256 89e816dcc9ea8f201e902a8cd46e721b8739551e66acf7368d658bc0f36b72af,
log `research/log/2026-11-27-n11-seventhcost-ladder-preaudit-first-real-run.md`)
disclosed a 50M-modeling gap: after the seventh-cost owner lane escalated
k05 (`1152921504607932416:536870912`, declaration e89e80aa, completion
d08d4ddd, at50m cold pair byte-identical, sha ff750cc6... x2, result
WIN(1), nodes 15,763,505), the instrument

- has no pair_50m determinism gate,
- does not resolve or park keys at the 50M stage (k05 stays reported as
  parked UNKNOWN@15M), and
- would false-fail its WIN stopping rule if the 50M WIN were integrated
  naively, because the rule compares ladder key order while the k05 50M
  escalation was published temporally AFTER the 15M raws of k06..k42
  (waves 64a46b4c / 24f40b8b precede d08d4ddd).

This Part closes that gap with a pre-registered revision of the instrument
plus a second real run against the published 126 raws.

## S2. Design (revision 2, script sha256 5b47ac7f64197bb4540662cd5d8ab56f2b4fefebec5d9296f3566f397563f2fc)

The temporal anchor is the published batch-summary checkpoint
(`output/batch-summary.json` of the seventh-cost kit, sha256
6881eaaf48e900c96d8816017a5d052054d5ebbf4f0b3dc9e621df732ce01c2b,
git-published in wave C3 commit 24f40b8b, strictly before any 50M raw
existed). Everything the ledger records provably precedes any 50M raw by
git publication order. New fail-closed gates:

1. pin_batch_summary + schema/class/head-basis/counters: the ledger's
   head basis must equal the pinned canonical head 42dbb58f...; per_key
   must cover exactly the 42 selection keys at the selection positions;
   resolved/parked counters and the two nodes-bookkeeping sums must equal
   the per_key derivation.
2. Ledger-vs-raw cross-consistency (unconditional): every ledger stage1_2m
   (result, nodes) must equal the published at2m raw; every ledger
   resolution (stage 2m or 15m) must match the raw rows with its pair
   present; every ledger park must match a raw 15M UNKNOWN pair
   (result 0, nodes 15,000,000).
3. Post-anchor 15M starts forbidden: any raw 15M row for a key the ledger
   does not account (resolved-at-15m or parked) fails
   stage2_15m_ledger_accounted.
4. 50M stage modeling: at50m rows only for ledger-parked keys
   (at50m_ledger_parked), only after a 15M UNKNOWN raw
   (at50m_after_parked15m), with a mandatory identical cold pair
   (pair_50m_required / pair_50m); result 1 resolves WIN, 2 resolves
   LOSS, 0 parks at 50M (nodes==budget already gated by
   raw_unknown_full).
5. Temporal WIN stopping rule (replaces the key-order rule): if any WIN is
   resolved at any stage, then (a) every key with any raw is covered by the
   ledger (win_all_raws_predate_anchor), (b) every 15M raw start is
   ledger-accounted (win_15m_starts_predate_anchor), (c) every 50M
   escalation is of a ledger-parked key (win_50m_escalations_from_parked),
   and (d) the ledger itself recorded no WIN and did not fire its stopping
   rule (win_ledger_consistent_pre_win). No key-order comparison is made.

Output schema bumped to n11-seventhcost-ladder-preaudit-v2 with the ledger
pin, escalated_50m_keys, parked_50m_keys and the stopping-rule model name.
All revision-1 gates are retained unchanged.

## S3. Verification (all on scratch copies; real raws never modified)

Inputs rebuilt from scratch and byte-pinned: selection JSON c395fe03...,
head cache 42dbb58f... (285,776 B), batch-summary 6881eaaf... (17,234 B),
124/124 raws byte-matched against the kit's MANIFEST-raw-sha256.txt
(3-column sha,size,path parsed), at50m pair byte-identical
(ff750cc63e3ead314a5c5a22b09cca5588f284a34dc08c5c4d1cc5716eda342c x2).

- Clean control (second real run, published raws at HEAD d08d4ddd):
  rc=0, 9,211 gates PASS, checkpoint=full. Output
  `output/ladder-preaudit.json` sha256
  28e4f9244fc4598728843225bfc7b8ee009098196a147e8a995fb7642c605ad0:
  126 raws, 42 keys with raws, 42 resolved (41 exact LOSS + k05 exact WIN
  at 50M), parked 0, escalated_50m_keys=[5], determinism pairs for all 42
  keys, resolved_win_keys=[5].
- Determinism: 3 runs byte-identical (output JSON and stdout).
- Tamper battery on real raws (scratch copy, deleted after the battery),
  6/6 fail-closed with the expected first-failing gate:
  T1 at50m-run2 nodes 15763505->15763506 -> pair_50m_05;
  T2 phantom at50m pair for non-parked k06 (key/legal rewritten to k06) ->
  at50m_ledger_parked_06;
  T3 batch-summary trailing byte -> pin_batch_summary;
  T4 phantom at15m raw for k16 (resolved at 2M in the ledger) ->
  stage2_15m_ledger_accounted_16;
  T5 at50m budget 50000000->40000000 -> raw_budget_at50m-run1-k05;
  T6 deleted at50m-run2-k05 -> pair_50m_required_05.
  Post-restore clean control rc=0, output byte-identical (28e4f924...).

## S4. Honest disclosure

- The revision was written and self-tested AFTER the k05 50M WIN raws were
  published (unlike revision 1, which preceded all ladder raws). The
  revision is fail-closed against the published bytes, but it is not a
  pre-registration of the k05 measurement itself; the k05 50M row remains
  single-implementation (Node replica) and this instrument's PASS is
  integrity bookkeeping only, never corroboration and never a verdict.
- The ledger anchor argument relies on git publication order (24f40b8b
  before d08d4ddd), which the instrument itself cannot verify from files
  alone; the pin records the anchor, and any tampering with the ledger
  fails pin_batch_summary.
- Fetch-back note: during input reconstruction the raw CDN returned
  "404: Not Found" bodies for the 124 pre-d08d4ddd raws when addressed by
  the full commit sha (stale/broken for those paths at fetch time); the
  same files fetched cleanly by the main ref and matched the kit's
  MANIFEST-raw-sha256.txt 124/124, and the two at50m raws matched the
  published sha ff750cc6... independently. No input was trusted without a
  byte pin.
- The revision-1 output (schema v1, sha 232e42ec...) is superseded by the
  revision-2 output at the same path; the revision-1 bytes remain in git
  history (commit dc95bc0e).
- The 41 LOSS rows and the 1 WIN row remain single-implementation; the
  C++ scrutiny gate and third-implementation corroboration Parts of the
  owner lane are unaffected and still pending.

## S5. Resume (re-fetch latest main before any work; hourly parallel runs)

- The instrument is re-runnable after every future raw publication (its
  output is fail-closed rewritten); for any FUTURE batch (eighth cost
  onward) a fresh ledger pin must be added.
- Owner-lane next Parts remain: 41 LOSS rows C++ scrutiny gate, k05 WIN
  row second/third-implementation corroboration, then the adoption Part
  (fresh declaration, WIN/LOSS conflict review). This instrument consumes
  nothing.
- Status guard: the standard 11x11 empty board, all 19 central-reply
  roots, the two-stone root {60,27}, the third-move pair {100,108} and
  every closure class remain UNKNOWN; no verdict is consumed or implied
  by anything in this kit.
