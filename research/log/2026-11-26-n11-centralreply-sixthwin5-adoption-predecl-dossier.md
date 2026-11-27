# n11 central-reply sixthwin5 WIN-adoption pre-declaration dossier session log (2026-11-26)

Session lane: the recurring n11 long-term lane.  Scope: publish the
pre-declaration dossier for a hypothetical future EV-pattern WIN adoption of
5 unconsumed sixth-cost exact-WIN rows (k02/k03/k04/k05/k08, class 3077),
following the EV/EU/EM predecl dossier pattern.  This session created no
branch, no PR, declared no Part, and consumed no verdict.

## Chain

1. Fresh main check: kit name
   `research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126`
   free (missing on main, no commit references it); concurrent 2026-11-26
   lanes active (k09k43 third-impl batch 0f2440c8ca; m-ladder kit-2..kit-6
   commits up to HEAD 76c461dab37027680ae7566ee32d6d9037849029 at
   publication check time) - none touches any path written by this kit.
2. Correction carried into the dossier honestly: an earlier handoff note in
   this lane claimed k02 had NO third-implementation reproduction; the
   ea73c3e3 kit (2026-11-21) in fact contains a four-run k02 witness
   (bbce3433/a0eec80f/98e9427f/7a490ad4, 9,106,337 expansions, WIN(1)
   clean).  All 5 adopted rows are therefore verified at FOUR
   implementations (replica 2-pass + run3-verify / C++ Part SK gate /
   TI kit audit / ea73c3e3 witness).  This correction was found BEFORE any
   bytes were authored, from published repo material.
3. `scripts/make_increments_sixthwin5.py` written and run to completion
   (rc=0 twice, byte-identical outputs): probe-kit direct pins (20 raws +
   selection d5e9b059 + status SSOT 2a253d08 + win-finding ladder
   be662d23), C++ gate kit MANIFEST 8d84b1a5 verified 46/46 (178 gates
   PASS; audits ad139ece x3 identical), TI kit MANIFEST 538f8ec7 audits
   (k03 c24da5cd / k04 5116045c / k05 15373d06 / k08 6cb112f8),
   ea73c3e3 k02 witness x4, freshness vs BASE 6e49dd84
   (absent/quarantine-free 81d23160/canonical-safe 78655e94/s5_index
   round-trip on frozen graph 54f9c364).  Emits increment
   44c16a28 (5 rows), manifest 25defefa (schema
   sixthwin5-increments-manifest-v1, adopted-table digest b6ea1bcc,
   adopted nodes total 45,999,378 - bookkeeping only).
4. Fail-closed union merge: byte-clone of published merger 90711961,
   3 runs byte-identical (audit 2fcc1ce0 x3), scenario cache
   merged-exact-s5-chain-plus-sixthwin5 16a12390 (6,797 rows WIN 197 /
   LOSS 6,600, zero conflicts).  BASE head stays 6e49dd84.
5. Refresh fork `reaudit/scripts/refresh_adoption_sixthwin5.py`
   (92a884c9) = byte-clone of the published EM dossier fork cc01b3d8 with
   EXACTLY three diff regions (docstring/CACHE path/CACHE sha), run twice
   (~58s, one process at a time), outputs byte-identical: refresh-summary
   295027cf, closure-classes 350e269a, per-root-coverage 9c5b2774
   (BYTE-IDENTICAL to BASE), probe-worklist regen 82f9e517 (unpublished
   per size policy, pinned in the census json).
6. Measurer `scripts/measure_census_deltas_sixthwin5.py` (23869728), rc=0
   twice, byte-identical census json fd684d83.  Machine findings:
   census 34,417/103/39/390 -> 34,409/111/39/390 with EXACTLY 8 flips,
   all unknown -> excluded_now, set-equal to the adopted keys' owner
   classes that were unknown at BASE (774/1387/2169/2339/3077/16734/
   25845/30329); serving class 3077 unknown children 100 -> 95; update8
   resolved 280 -> 281 (+1 = k02 s5_index 64872, the only adopted key in
   the frozen baseline requirement - measured, the other four keys sit
   outside it); remaining 31,445 unchanged; joint greedy 35,155
   unchanged; worklist 64,277 -> 64,276 (-1); win-hit groups 25
   set-identical; closure ranking 804 rows with no enter/leave and no
   rank churn, unknown_now churn only in class 16734 (92 -> 91).
7. Kit README + MANIFEST-sha256.txt written (frozen-environment pins
   locally re-verified: graph 54f9c364, update8 b658290a, quarantine
   81d23160, policy 78655e94); kit + this log pushed to main directly
   (repo policy: no branch/PR), fetch-back byte-verified per file.

## Honest session notes

- One hand-modelled expectation was WRONG and is disclosed here: the first
  measurer draft assumed all 5 adopted keys would newly resolve in the
  frozen update8 baseline requirement.  The measured truth (resolved 280
  -> 281, exactly k02 only) required deriving the baseline requirement
  from update8's required_new_s5 (as the refresh fork itself does) and
  asserting set membership; the other four keys were probed after the
  baseline froze and are correctly outside it.  The corrected assertion is
  stronger than the original (machine-derived membership, not a hand
  list).
- The closure-churn reading needed a data check: only class 16734 of the 8
  flipped owner classes appears in the 804-row closure ranking; the other
  seven are not ranked closure candidates.  Recorded as-is, no claim.
- The environment lost an earlier draft of the measurer between compaction
  and this run; the published measurer was written new from the published
  pattern (EM measurer) - nothing else depended on the lost draft.
- Concurrency: HEAD re-checked immediately before the push; competing
  2026-11-26 lanes touched no path of this kit.  No verdict consumed; no
  cache on main modified; nothing adopted; the canonical head remains
  merged-exact-s5-chain-plus-emloss21 6e49dd84.

## Result summary (measurement only; nothing consumed)

The sixthwin5 pre-declaration dossier is published: a future EV-pattern
Part can declare the 5-WIN-row adoption entirely from published bytes.
Measured scenario effect of the unconsumed adoption: 8 owner classes leave
live status by the win-hit mechanism (unknown -> excluded_now), serving
class 3077 among them; exactly one baseline-requirement key (k02) newly
resolves; joint greedy, per-root coverage, free-now census and win-hit
groups are all unchanged.  No adoption was declared in this session.

## Status guard

The standard 11x11 empty board, the 19 central-reply roots, S2, the
two-stone root {60,27}, its remaining third moves {100,108} and every
closure class remain UNKNOWN throughout.  Node counts are bookkeeping and
never verdicts.  The 5 increment rows stay unconsumed honest WIN labels.
No K item was created and no knowledge README (repo) was touched.  This
session could not reach the user's own machines (scheduled task without
the desktop app); all publishing went through GitHub only.
