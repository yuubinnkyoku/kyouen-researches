# Part EV completion log: evwin4 fourth WIN canonical adoption (2026-11-26)

All waves landed.  Part EV closes complete; the canonical merged exact-S5
chain head of record formally advances to the EV merged cache
`research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-evwin4-20261126.cache`
(sha256 63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0,
6,771 rows, WIN 192 / LOSS 6,579), already published dossier-side and
byte-reproduced here by the fail-closed merger from BASE + the Part
increment; it is the new BASE for every later adoption / reaudit /
extractor.

## Wave chain (each push preceded by a fresh main refetch; each verified by
commit-pinned fetch-back against the regenerated local bytes)

* A  declaration 10fea2ee
  (research/log/2026-11-26-part-ev-win4-adoption-declaration.md):
  all kit byte pins pre-registered before any kit byte was published;
* B  kit scripts 3/3: 511e0feb (merger 90711961 byte-clone /
  selftest battery) then 06df8b0e (maker 4ddbc831 + extractor
  70a5b207); fetch-back 2/2 byte-identical;
* C  adoption outputs a46c3a14 (6 files): increment 7f125610,
  increments-manifest f013a8f5 (schema evwin4-increments-manifest-v1),
  merge-audit-run1/2/3 all d9713aed, decomp-deltas c05f11cd - all
  byte-matched the declared pins; fetch-back 6/6 byte-identical;
* D  close-out c3433eb5: kit README + MANIFEST-sha256 (9 published kit
  members byte-pinned sha+size, README/MANIFEST self-excluded per
  convention); fetch-back 2/2 byte-identical;
* F  completion log = this commit.

NOT republished in this Part (deliberate, recorded in the kit MANIFEST
header): the merged scenario cache copy (byte-identical to the
published dossier file 63f33c4f; regenerable from BASE pin 3ba48608
via the kit merger + increment), the probe-worklists (BASE regen pin
397a4379, 3,717,712 B; SCEN regen pin ca50cb68, 3,717,416 B; size
policy), the dossier census json ab97fba9 (published dossier-side).
All Part kit bytes were published from the declaration-pinned local
artifacts; every wave was fetch-back byte-verified against the
pre-registered pins.

## Execution record (this Part, all from published bytes)

The kit extractor 70a5b207 ran its full battery rc=0 TWICE
consecutively (wall about 2m04s each), stdout byte-identical, decomp
sha byte-identical (c05f11cd); the merger reproduced the dossier merged
head 63f33c4f 3/3 byte-identical conflict-free runs (audits d9713aed);
both published refresh forks (Part EU kit 6dc24c15 against BASE, dossier
kit f2edac3e against SCEN) re-executed byte-verbatim in isolated
scratch trees reproducing all 8 published/regen-pinned outputs
(2b70bb55 / 59a4c85f / cfc2bfe1 / 397a4379 and 1fafd081 / 6ba51faa /
d9eee976 / ca50cb68).  Tamper battery fail-closed 3/3: increment-sha
pin mutation, b018 adopted-node expectation mutation, census
after-count expectation mutation - each ABORT rc=1 with the recorded
message, clean rerun restored the byte-identical decomp.

## State after the Part (all machine-verified by the extractor battery)

* canonical BASE of record: 63f33c4f... (6,771 rows WIN 192 /
  LOSS 6,579); the Part EU head 3ba48608... remains published history
  and is the merge BASE of this Part;
* census: class_status_counts 34,430/90/39/390 -> 34,417/103/39/390
  with EXACTLY 13 UNKNOWN->excluded_now flips {4864, 4903, 5255, 5282,
  5613, 6030, 12264, 12327, 14776, 15640, 16371, 16757, 20421} - the
  adopted keys' BASE-unknown owner classes; class 30345 NOT
  double-flipping (Part EP/EU chain already excluded_now, cost-unknown
  5 -> 4 on the 51-raw/50-cost Board boundary); class 30354 untouched
  (97/97, 96 static, its 10 BASE win_hit groups unchanged);
* closure-classes.csv 805 -> 805, zero rows left/entered, zero
  groups_served churn; unknown_now churn exactly {16371: 2->1,
  16757: 3->2, 30345: 5->4, 20421: 6->5, 12264: 51->50}; rank churn
  exactly the 7-row set {23101: 1->2, 1849: 2->3, 2251: 3->4,
  16371: 4->1, 13342: 11->12, 30118: 12->13, 12264: 13->11};
* update8 frozen baseline: resolved_count 260 -> 263, remaining_now
  31,505 -> 31,445, groups_free_now 131 -> 131, union 31,859;
  win_hit_groups 10 -> 25 (the 10 BASE class-30354 quartets identical;
  exactly 15 new groups: classes 12264 x 6 / 16757 x 5 / 20421 x 4;
  zero removed); Board verification 39/39 both sides, zero rejections;
  per-root free_now/uncovered identical at all 20 roots + baseline;
  individual greedy deltas only at roots {0: 2980->2789, 36:
  3005->2951, 12: 2848->2846, 48: 2895->2893, 5: 2884->2883, 37:
  3620->3619}; joint greedy 36,619 -> 36,618;
  group_best_options_nonfree 2,105 static; worklist 64,307 ->
  64,302.  All re-selection bookkeeping; no coverage claim anywhere.

## Verdict scope and guarantees (unchanged)

Consumed in this Part: exactly the 4 EV-gate-verified closure-batch WIN
rows b018 (class 16757, s5_index 528497, nodes 3,549,602), d002 (class
20421, s5_index 197253, nodes 5,359,994), e002 (class 16371, s5_index
183566, nodes 14,112,632), f017 (class 12264, s5_index 415095, nodes
3,522,635); adopted node total 26,544,863; 15M two-pass fresh-cold
node-exact replica raws, third-impl a/b corroboration, C++
second-implementation scrutiny gate 7/7 GATE-PASS (audit 0327dad8, gate
source 9193f5b6 at 154f3b7a); no batch key re-searched at any
condition.  Consuming a WIN label asserts NO root verdict.  NOT
consumed: the 21 unconsumed closure-batch LOSS rows (EM-pattern
loss-adoption territory), the k04 sixth-cost WIN, every other
unconsumed probe-level WIN, and the Part EU rows (regression tie: both
sit WIN in BASE, NOT re-adopted).  The standard 11x11 empty board and
every central-reply root stay UNKNOWN; nodes are bookkeeping; no
free/secured-coverage claim is made anywhere.  Next natural steps
recorded by the lanes: the Part EU full second-environment
verification stays OPEN (SPOT re-execution recorded cf699df2), the
EM-pattern loss-adoption Part may take the 21 unconsumed closure-batch
LOSS rows, the k04 sixth-cost lane remains, and any later adoption
Part takes 63f33c4f as its BASE.
