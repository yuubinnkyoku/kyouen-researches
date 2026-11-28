# Declaration: n11 fourteenth ladder-top selection (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
execution. Any parallel lane must not select, probe or resolve the
ladder-top candidates below until this Part's completion log appears.

## Scope

The closure-ladder top-candidate re-selection (the "fourteenth"
selection Part) under the CURRENT canonical head of record
`d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec`
(`merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`, 6,896
rows WIN 214 / LOSS 6,682, thirteenth k01k02 adoption). Basis ladder:
the published thirteenth k01k02 adoption reaudit closure ladder
`be8bcff16a7a557d30703921d9a024a232b0fade5fab16afb015a07666fcdc62`
(799 data rows, SCEN side, commits `90147711`/`6387843d`). Declaration
HEAD pin: `14c0281b2163a98783863cc175a3fcac54920489`.

## Method

A fresh selector (`select_fourteenth_ladder_top.py`, structural
adaptation of the published thirteenth selection instrument
`select_thirteenth_ladder_top.py` sha256 `e2986020...`: head pin,
closure-ladder pin, pre-registered expectations, claim-set machinery
extended with the adopted thirteenth_2, dual-implementation legal
derivation kept; the refresh machinery itself is NOT read or executed)
recomputes the per-class `unknown_now` for ALL 799 ladder rows from
the frozen dependency graph `54f9c364...` + head `d772f73c` +
update8 receipts `b658290a...` (the same trust boundary as the
refresh), fail-closed, 3 cold runs byte-identical + a 5-case tamper
battery fail-closed + clean control.

## Pre-registered expectations (fail-closed gates)

1. 799/799 recomputed `unknown_now` exactly match the published ladder.
2. Ladder top-5 by class_rank: class 5804
   (`6053400849139367936:0`) unknown_now 4, class 20421
   (`1155173304420536320:131072`) 5, class 34269
   (`1152921504624672768:68719476736`) 11, class 12264
   (`1152921504606848033:0`) 33, class 5343
   (`1171516445255794688:0`) 46.
3. Selection rule: the first ladder class (by class_rank) whose
   remaining unknown S5 keys are ALL unclaimed (vs focus_35 / cert_38 /
   third_39 / fourth_41 / fifth_44 / sixth_43 / seventh_42 / eighth_43 /
   ninth_45 / tenth_44 / eleventh_46 / twelfth_51 / sbd_101 / parked_6 /
   the adopted ultra-cheap 4 / the adopted thirteenth 2), fresh vs the
   head, quarantine-free, 5-stone, D4-canonical and canonical-safe.
4. Expected selection: class 5804 with exactly the 4 unknown keys
   `6053401124017274880:0` (s5_index 198576, legal 86),
   `6053682324116078592:0` (s5_index 207094, legal 82),
   `6052837899185946628:128` (s5_index 212115, legal 87),
   `6053400849139367936:128` (s5_index 212536, legal 92); none is in
   the probe-13 supply (legal/proxy re-derived live: Board legal and an
   independent integer 4x4-determinant concyclicity implementation
   must agree; proxy null). Expectation recorded from a local
   pre-computation on the same pinned inputs (3 cold runs
   byte-identical); the selector's machine output is authoritative and
   any deviation aborts (rc=1).

## Non-meaning

Selection and scheduling only: NO verdict is claimed or consumed.
Nodes, proxy and legal counts are bookkeeping, never evidence of WIN
or LOSS. The standard 11x11 empty board, all 19 central-reply roots,
the two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN. Resolving the selected keys requires a separate future
single-owner escalation declaration and, before any adoption, the
standing cold-pair + C++-gate + third-implementation pillars.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The concurrent six-row/seven-row SAT lanes (declaration commits
  `14c0281b`, `3131cf9f`, `7d49c0e6`) own different corpora
  (mwq frontier cells); the selected keys are disjoint from them by
  construction (s5 corpus vs row-class SAT corpora).
- The pre-pass that recorded expectation 4 ran with the
  selection-expectation gates neutralised (measured, not asserted);
  the published selector asserts them fail-closed.
- All pinned inputs are fetched fresh and sha-verified in-script
  before the run.
