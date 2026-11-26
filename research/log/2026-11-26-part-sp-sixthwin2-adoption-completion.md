# Part SP completion log: sixthwin2 WIN-only canonical adoption (2026-11-26)

All waves landed.  Part SP closes complete; the canonical merged exact-S5
chain head of record formally advances from 16a12390 (the Part EW head of
record) to the sixthwin2 merged cache
research/experiments/n11-centralreply-sixthwin2-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache
(sha256 cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8,
6,799 rows, WIN 199 / LOSS 6,600, 284,127 bytes), published by THIS Part's
kit (no pre-declaration dossier existed for sixthwin2; unlike EW the
merged head is published here, wave C) and byte-reproduced by the
fail-closed merger from BASE 16a12390
(16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd,
6,797 rows WIN 197 / LOSS 6,600, published sixthwin5 dossier-side)
union-merged with the Part increment; it is the new BASE for every later
adoption / reaudit / extractor.  Freshness for any later adoption is
re-anchored against cc3694bb (superseding freshness vs 16a12390).

## Wave chain (each push preceded by a fresh main refetch; each verified
by fetch-back against the declared local bytes)

* A  declaration 85557762: all 17 kit byte pins + the measurement
  claims pre-registered before any kit byte was published (one commit;
  fetch-back blob sha + size verified);
* B  kit scripts 8ad9e7d2: 5/5 (merger 90711961 byte-clone, maker
  6e95f467 structural clone of the Part EW maker with the parked4
  ladder / SM gate / SL batch sources, measurer 062a071c, own
  fail-closed extractor 9feb2cbe, reaudit refresh fork 82ddb89c of
  92a884c9 differing in docstring / CACHE path / expected-sha only);
* C  adoption outputs 298647c3: the 11 files - increment 89bff217
  (39-line header + exactly 2 s5verdict WIN rows), manifest d97f1d5d
  (schema sixthwin2-adoption-increments-manifest-v1,
  canonical_head_published_by_this_part block), merged cache of record
  cc3694bb (6,799 rows WIN 199 / LOSS 6,600, 284,127 bytes),
  merge-audit-run1/2/3 all 5904693e (inputs recorded with the
  kit-relative path strings of record), census-deltas 030e36ed,
  decomp 16bb56a0 (schema sixthwin2-decomp-deltas-v1), reaudit refresh
  outputs 7a500a03 / 350e269a / 9c5b2774;
* D  close-out 8fa24b72: kit README b4cc840c + MANIFEST-sha256
  78245739 (17-entry byte pins incl. the merged head cc3694bb; README
  self-excluded per convention);
* F  completion log = this commit.

Every wave fetch-back compared the published git blob sha (+ file size)
against machine-computed local values for the identical bytes
(blob sha = sha1 of 'blob <size>\0' + content, computed live from the
staged files whose sha256 was first verified against the kit MANIFEST
pins); no scratch or temporary bytes were published.  The published
probe-worklist is NOT in the kit (size policy; regen pin 0818da81,
3,715,904 bytes, disclosed README-side).

## Execution record (this Part, all from published bytes; NO new solver
pass ran)

The kit extractor 9feb2cbe ran its full battery fail-closed over
published bytes only, twice, with byte-identical stdout and decomp
output: BOTH refresh forks (the published sixthwin5 dossier refresh
92a884c9 against BASE, and the kit's SCEN fork 82ddb89c) re-executed
byte-verbatim from scratch trees reproducing all published /
regen-pinned outputs (BASE side 295027cf / 350e269a / 9c5b2774 +
worklist regen 82f9e517, 3,715,904 B; SCEN side 7a500a03 / 350e269a /
9c5b2774 + worklist regen 0818da81, 3,715,904 B).  The maker 6e95f467
re-executed byte-verbatim from a scratch tree (rc=0, byte-identical
increment 89bff217 + manifest d97f1d5d), re-proving the adopt-eligibility
chain live from published bytes.  The merger 90711961 reproduced the
merged head cc3694bb in 3/3 byte-identical conflict-free runs (audits
5904693e x3, unique_rows 6,799, WIN 199 / LOSS 6,600); its recorded
inputs use the kit-relative path strings of record.  A 3-mode tamper
battery (increment row verdict flip / merge-audit unique_rows mutation /
manifest adopted_nodes_total mutation) all failed closed rc=1 with
byte-verified restore; recorded in the declaration, not published as
kit files.  The census measurement 030e36ed and the extractor's
independent recount agree EXACT on both cache identities, census
counts, the exact 2-flip set and all scheduling bookkeeping.

## State after the Part (all machine-verified by the battery)

* canonical head of record: cc3694bb... (6,799 rows WIN 199 /
  LOSS 6,600); the Part EW head 16a12390... remains published history
  and is the merge BASE of this Part;
* census: class_status_counts 34,409/111/39/390 ->
  34,407/113/39/390 with EXACTLY 2 flips, BOTH unknown ->
  excluded_now, win-hit only, and exactly the status-unknown-at-BASE
  owner classes of the 2 adopted keys: 2624 (1297600742147751936:0,
  owner of k19) and 30136 (1152921573327376384:0, owner of k13); the
  other owner classes 3077 (both keys, already excluded_now since Part
  EW) and 5184 (k19) keep their status; NO class is freed; 34,407 S4
  classes remain status-unknown;
* serving class 3077: status stays excluded_now on both sides (the
  win-hit Part EW; the SP adoption is not its first); cost-unknown
  95 -> 93 (exactly the 2 adopted keys, both owned there);
* closure-classes.csv 804 -> 804: ZERO rows enter or leave; ZERO
  unknown_now churn; rank churn EMPTY (0 re-ranked rows);
  groups_served churn 0;
* update8 frozen baseline: resolved_count 281 -> 281 (BOTH adopted s5
  indices 103319 (k19) and 112203 (k13) sit OUTSIDE the frozen baseline
  requirement: nothing newly resolves, measured, disclosed),
  remaining_now 31,445 static, groups_free_now 131, union baseline
  31,859 stale-equal; win_hit_groups 25 -> 25 IDENTICAL sets;
* per-root free_now/uncovered identical at all 20 roots (per-root
  coverage byte-identical on both sides); individual greedy union
  UNCHANGED at all 20 roots; joint greedy 35,155 -> 35,155 UNCHANGED;
  unique_groups 2,115 static; group_best_options_nonfree 2,101
  static; worklist 64,276 -> 64,276 (delta 0: both adopted keys are
  probe-worklist members but sit outside the frozen baseline
  requirement row set driving the worklist delta accounting).  All
  scheduling bookkeeping; no coverage claim anywhere.
* lane-era prediction superseded (disclosed): the parked4 halt-audit's
  if-adopted global-status prediction was computed against the pre-EW
  6e49dd84 head and is not the measurement of record; the full recount
  against the 16a12390 head additionally discovers class 30136.

## Verdict scope and guarantees (unchanged)

Consumed in this Part: exactly the 2 unconsumed parked4 L50M ladder
exact-WIN rows of the sixth-cost class 10376293541461626880:65536:
k13 1152921573327376384:536870912 (s5 index 112203, nodes 16,402,480)
and k19 10376293541461626880:65664 (s5 index 103319, nodes 15,379,062;
probe selection d5e9b059 exclusive_probe_order positions 13/19; budget
50,000,000 over the pinned 15,000,000 park-at-UNKNOWN baselines; per
key a cold two-pass node-exact 50M battery, a 32M budget-margin
re-proof and a voluntary third cold 50M verify run plus 4
validation-anchor honesty replays), C++-gated GATE-PASS by the Part SM
kit (2 fresh-cold passes each, audit 26/26 + tamper 3/3) and
third-implementation-corroborated by the Part SL batch audit 300c8c0a
(verdict-level WIN agreement, 3 identical cold runs each; k13
expansions 19,433,195 / k19 17,955,947; expansions legitimately differ
from replica node counts, different implementations).  Adopted node
total 31,781,542 (bookkeeping, never verdicts); no WIN regression ties
(both keys fresh to BASE 16a12390; win_ties = []); adopted-table digest
e7e2b30d5e5ee504f299ec1e64ecf2c252d9d3ca412299d38932628e8844bd83.
Consuming a WIN label asserts NO root verdict; owner classes leave
live status by the win-hit mechanism only; NO class is freed and NO
coverage claim is made anywhere.  NOT consumed and NOT emitted: the
parked4rest2 L50M WIN rows k20/k33 (their C++ scrutiny gate kit is
published wave-A/B-side as Part SN with the runner pending) and the 30
verified LOSS rows of the Part SL batch; all stay in NO cache.  No
batch key was re-searched at any condition.  The standard 11x11 empty
board and every central-reply root stay UNKNOWN; nodes are
bookkeeping, never verdicts; no free/secured-coverage or
root-resolution claim is made anywhere in this Part.  Next: any later
adoption Part takes cc3694bb as its BASE; with k13/k19 adopted the
sixth-cost serving class 3077 is excluded_now with cost-unknown 93
(k20/k33 among the standing unconsumed candidates pending their gate).

## Session honesty note

This Part continued after context compactions; the kit was re-staged
and every kit byte re-verified against the pre-registered pins before
the recorded runs.  The merged-cache sha was re-derived by machine (an
earlier hand-noted transcription differed; the machine-derived
cc3694bb... value is authoritative everywhere).  Two pre-push staging
checks during publication failed closed on transcription of expected
pins into a verification script and were redone machine-side (pins read
from the kit MANIFEST, not hand-copied); no remote commit was created
by any discarded attempt.  Staged working files outside the kit path
are not part of the kit.
