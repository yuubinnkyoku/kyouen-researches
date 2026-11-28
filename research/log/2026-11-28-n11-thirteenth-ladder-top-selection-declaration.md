# Declaration: n11 thirteenth ladder-top selection (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
execution. Any parallel lane must not select, probe or resolve the
ladder-top candidates below until this Part's completion log appears.

## Scope

The closure-ladder top-candidate re-selection (the "thirteenth"
selection Part) under the CURRENT canonical head of record
`beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544`
(`merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache`, 6,894
rows WIN 212 / LOSS 6,682, ultra-cheap u04 adoption). Basis ladder:
the published ultra-cheap u04 adoption reaudit closure ladder
`ef3447481abb14af3c56a64251d86e63b178c7fb57b0ce8898e67303c24dc3e2`
(800 data rows, SCEN side, commit `d11e74c3`).

## Method

A fresh selector (`select_thirteenth_ladder_top.py`, structural
adaptation of the published ultra-cheap census instrument
`ultra_cheap_census.py` sha256 `c5e7b88e...`: head pin, closure-ladder
pin, top-candidate gates, claim-set machinery, dual-implementation
legal derivation added; the refresh machinery itself is NOT read or
executed) recomputes the per-class `unknown_now` for ALL 800 ladder
rows from the frozen dependency graph `54f9c364...` + head `beecb024`
+ update8 receipts `b658290a...` (the same trust boundary as the
refresh), fail-closed, 3 cold runs byte-identical + a 5-case tamper
battery fail-closed + clean control.

## Pre-registered expectations (fail-closed gates)

1. 800/800 recomputed `unknown_now` exactly match the published ladder.
2. Ladder top-5 by class_rank: class 16757
   (`1153204079095185408:65536`) unknown_now 2, class 5804
   (`6053400849139367936:0`) 4, class 20421
   (`1155173304420536320:131072`) 5, class 34269
   (`1152921504624672768:68719476736`) 11, class 12264
   (`1152921504606848033:0`) 33.
3. Selection rule: the first ladder class (by class_rank) whose
   remaining unknown S5 keys are ALL unclaimed (vs focus_35 / cert_38 /
   third_39 / fourth_41 / fifth_44 / sixth_43 / seventh_42 / eighth_43 /
   ninth_45 / tenth_44 / eleventh_46 / twelfth_51 / sbd_101 / parked_6
   and the adopted ultra-cheap 4), fresh vs the head, quarantine-free,
   5-stone, D4-canonical and canonical-safe.
4. Expected selection: class 16757 with exactly the 2 unknown keys
   `1153204147814662144:65536` (s5_index 556117) and
   `1152922672837951488:65792` (s5_index 558553); neither is in the
   probe-13 supply (legal/proxy re-derived live: Board legal and an
   independent integer 4x4-determinant concyclicity implementation
   must agree; proxy null). Expectation recorded from a local
   pre-computation on the same pinned inputs; the selector's machine
   output is authoritative and any deviation aborts (rc=1).

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
- The concurrent twelfth-cost takeover lane (declaration commit
  `768d2e5a`) owns the twelfth-51 batch; the selected keys are
  disjoint from it by gate.
- All pinned inputs are fetched fresh and sha-verified in-script
  before the run.
