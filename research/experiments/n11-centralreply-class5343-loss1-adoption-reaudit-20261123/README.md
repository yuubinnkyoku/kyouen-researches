# n11 central-reply closure batch-28 (class 5343) 1-LOSS canonical adoption re-audit (Part CH, 2026-11-23)

Part CH (declaration appended to
research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md,
publish-then-execute): fail-closed canonical adoption of the single resolved
LOSS row of batch-28 (class 5343, key aa003: s5verdict 1152921504741064704,4228,
5,2,4070373) into the Part BZ canonical 6,293-row cache
(sha256 9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e)
via the pinned byte-copy fail-closed union merger (scripts/s5_union_merge.py,
sha256 907119610034...).

Adopted row is 2-pass node-exact result 2 at budget 15M (pinned jsreplay
replica), re-derived from the published batch-28 drive-2 kit (96 files, all
sha256-verified against the published MANIFEST-sha256.txt of the kit;
status.log 343097c2..., row-audit-winhalt 3e86a32b...). The batch is NOT a
complete enumeration book: the 4 WIN rows aa001/aa002 (Part CC third-implementation
cross-verified) and aa006/aa007 (Part CG cross-verification lane declared,
pending output) are honest labels, NOT adopted (verdict unconsumed; scrutiny
owner C++ second-implementation gate pin 9193f5b6... remains the only WIN
adoption route; batch-14residual q042 / batch-26 l028 precedents). The 2
EXHAUSTED rows aa004/aa005 are honest UNKNOWN bookkeeping (budget 15M
exhaustion on both passes, no same-condition re-probe). The 47 fileless keys
(aa008..aa054) are UNPROBED and untouched.

## Pipeline (all deterministic, every step byte-reproduced this host)

1. scripts/make_increments_b28loss1.py: kit integrity (96 files, per-file
   sha), 2-way p1/p2 node-exact + '# replay_done' completeness, status.log
   17-line picture (WIN-HALT 4 pairs + EXHAUSTED 2 + TRUNCATED-RETRY sidecar
   absence), row-audit winhalt picture agreement, batch-keys legal/(lo,hi)
   agreement, adopted-row node sum 4,070,373 on both passes, zero BASE
   overlap, quarantine 0. Output: output/increment-b28loss1-20261123.cache
   (1 row) + output/increments-manifest.json (schema
   b28loss1-increments-manifest-v1, full_packet_eq_loss_only false).
   x4 byte-stable.
2. scripts/s5_union_merge.py (byte-copy, pin 90711961..., selftest PASS):
   union merge BASE (Part BZ canonical 6,293-row cache, sha 9115be9e...) +
   increment with the WIN/LOSS conflict gate. x3 byte-identical;
   merge-audit-run1/2/3.json identical (5e8d6909...). Output: the 6,294-row
   scenario cache (WIN 158 / LOSS 6,136).
3. reaudit/scripts/refresh_adoption_b28loss1.py: full 19-root refresh
   (per-root coverage, closure-classes, probe-worklist, frozen update8 plan)
   against the scenario cache. x3 byte-identical + isolated run (env -i,
   separate tree) byte-identical. Outputs:
   reaudit/output/{refresh-summary.json, closure-classes.csv,
   per-root-coverage.csv} (+ regenerated probe-worklist.csv, worklist not
   published by design).
4. scripts/compare_deltas_b28loss1_adoption.py: fail-closed deltas BASE ->
   scenario (11 sha pins + manifest semantic gates; increments-manifest
   row_counts adopted 1 / WIN 4 / EXHAUSTED 2 / fragment 0 / fileless 47;
   independent 2-pass raw re-verification of all 7 probed keys). x4 + isolated
   byte-identical. Output: output/decomp-deltas-b28loss1-adoption.json:
   class 5343 unknown_now 54->53 (rank 27->19, pure ranking churn: rank
   19..26 classes shift +1, closure table membership unchanged left=[]
   entered=[]), flips=[], new_free=[], free_now 38->38, update8 resolved +1
   (== {104943} only), joint greedy 38,295 unchanged, probe-worklist
   64,747->64,746, per-root free/uncovered unchanged, individual greedy
   movers roots {4, 49} (2811->2810, 5978->5977).

Tamper battery (scratch tree): 12/12 detected + post-restore green, two
layers demonstrated: (a) pin layer (increment/status.log/BASE-cache/batch-keys
tamper caught by sha gates; raw tamper caught by the kit MANIFEST sha in the
maker), (b) semantic layer with attacker-repinned sha constants (verdict
flip 2->1 -> "non-LOSS verdict", BASE append -> "scenario cache row count !=
BASE + 1", batch-keys class flip -> row-audit picture disagreement,
manifest WIN-row node +1 / full!=loss flip / resolved_ids drop caught by the
manifest bookkeeping gates), including the extractor's independent 2-pass
raw mismatch display. Control: post-restore maker + extractor both green.

## UNKNOWN guarantee

The standard 11x11 empty board, the 19 central-reply roots, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, class 10968, class 23964 and
class 5343 (all 54 keys, aa001..aa007 included) remain UNKNOWN at every point
of this Part. Node counts are bookkeeping, never verdicts. This Part makes
no root-coverage/closure/secured/root-outcome claim: class 5343 keeps its 4
unadopted WIN children, 2 EXHAUSTED honest-UNKNOWN children and 47 fileless
unprobed keys, so it does NOT free; closure churn left=[]/entered=[] is only
the machine record that the class set is unchanged; joint greedy 38,295 and
worklist 64,746 are bookkeeping, not outcomes.
