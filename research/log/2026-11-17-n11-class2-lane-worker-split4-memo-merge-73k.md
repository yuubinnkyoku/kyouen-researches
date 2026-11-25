# 2026-11-17 n11 class2-lane: 4-worker N-way memo merge + fault-injection validation of the conflict detector (K0909 update)

Lane: 11x11 class2-lane long-term (cost73k). Kind: measurement + verification.
Outcome: 4-way measurement 13/14 gates (seed-insert rate gate exceeded,
recorded as fact; record identity closes), fault-injection test 7/7 gates.
No verdict change; 11x11 remains UNKNOWN.

## Context

The K0909 2-worker measurement (same day) proved the worker-split memo
merge is conflict-free and that the merged seed cuts the band ms24 run to
80.2%, but left two gaps on the lane's priority list (safe worker-cache
merge with immediate WIN/LOSS conflict detection):

1. The detector had never fired (zero natural conflicts), so its own
   correctness was unproven; "no conflicts observed" is not "conflicts
   would be detected".
2. The N-worker generalization (merge cost, per-worker load, union
   completeness as the split gets finer) was measured only at N=2.

This session closes both gaps on the same band, same verbatim engine
(blob 52bcaf50, both known memo bugs in place - K0907), same published
22-bit certificate set.

## Design

- 4-way split, node-count balanced at MS=1<<23 from the published
  band/fresh per-bit values: W1 = bits 0,7,11,15,35,39,41 (= the band
  ms23 prefix, so W1 doubles as a reproduction anchor),
  W2 = 44,58,62,73,76,87, W3 = 89,94,95,97,98, W4 = 103,105,112,117.
  Band-wide memo within each worker, per-bit snapshot+clearRows,
  byte-identity gate against the published certificate for every bit.
- Merge: per-worker KYOENWM1 dump -> external `sort -S 200M -k2,5` ->
  streaming distinct pass -> heapq N-way merge-join of the sorted
  distinct tables (key incidence histogram, sentinel-aware conflict
  detection, merged KYOENWM2 table). All streaming; no table is ever
  fully resident.
- Seedrun: verbatim engine at MS=1<<24 seeds from the merged table
  (insertion in file order through the engine's own memoEntry), then
  extracts all 22 bits band-wide. Record-identity gate on the final dump.
- Fault-injection test (separate script): deterministic synthetic
  corruptions in copies of the real dump/distinct tables,
  scenarios F1 (internal duplicate record, lose=3 appended to a copy of
  W2's raw dump), F2 (cross lose injection on a W1&W2 shared key),
  F3 (cross win injection on a W3&W4 shared key), F4 (nowin:=win on a
  W4-only incidence-1 key), F5 (nowin:=4 / nolose:=2 on W1&W3 shared
  keys - expected absorbed by the other workers' 255 sentinels).
  Gates: detections must be exactly the injected keys (zero false
  positives via exact totals and samples), F5 keys must not fire and
  their fault-merged records must be byte-identical to the clean
  merged records, and the fault merge must keep the clean structural
  counts (occupied_after / shared_total / incidence histogram).

## Results

- workers: W1 29,193,572 nodes / occupied 3,816,312 / 7 certs
  byte-identical; W2 30,417,638 / 4,026,734 / 6; W3 31,104,578 /
  4,605,832 / 5; W4 22,025,713 / 3,358,092 / 4. Total 112,741,501
  = 0.940 of the 2-worker total (119,962,147) and 0.930 of band ms23
  (121,186,659): finer splits keep shrinking the worker total
  (lower per-worker table load, less late-bit pollution).
  W1 equals the band ms23 per-bit prefix exactly.
- distinct: W1 1,979,858 / W2 1,793,658 / W3 1,544,867 / W4 1,565,935;
  internal conflicts 0 in every worker.
- 4-way merge: occupied_after 4,985,986 (+694,087 = +16.2% vs the 2-way
  4,291,899), shared_total 1,592,504, incidence histogram
  {1: 3,393,482, 2: 1,306,914, 3: 265,352, 4: 20,238}, cross conflicts 0,
  deterministic. The union GROWS with finer splits: at N=2 each worker's
  table ran at 62-74% load and 64-slot probe-window saturation dropped
  keys from the dumps; at N=4 the loads are 40-55% and fewer keys are
  lost, so the merged table is more complete. A bigger, more complete
  seed is worth more than the merge cost.
- seedrun4 (MS=1<<24, seed = the 4,985,986-record merged table,
  md5 7b098aeb625f722e5bfb13fcc615652a): 76,903,818 nodes
  = 0.897 of the 2-way seedrun (85,747,496), 0.720 of the unseeded band
  ms24 (106,861,135), 0.709 of the fresh ms23 battery (108,499,241);
  final occupancy 10,526,730 (load 62.7%); 22/22 certificates
  byte-identical; bit95 = 11,857,737 nodes again unchanged in every
  configuration (memo-state-invariant root, consistent with K0907).
- seed insertion: 4,985,986 seeded, 4,969,849 inserted, 16,137 failed
  (0.324% at 29.7% initial load; the 2-way seed failed 0.034% at 25.6%).
  The pre-registered <0.1% gate therefore FAILS (13/14 gates pass).
  The failure-rate growth is strongly superlinear in seed size
  (1.16x keys -> ~11x failures) - verbatim hash clustering saturates
  64-slot windows in cascade. The record-identity gate still closes:
  present 4,969,849 (every inserted key survives, value violations 0),
  missing exactly the 16,137 failed inserts. Soundness unaffected;
  the gate threshold is a performance budget, and 0.1% is not the right
  constant for larger seeds.
- fault-injection test: 7/7 gates pass. F1 -> exactly 2 internal
  win_and_lose (samples exactly the injected keys); cross merge ->
  exactly {win_and_lose: 4, win_le_nowin: 2} with samples exactly the
  F2+F3 resp. F4 keys, zero false positives; F5 keys do not fire and
  their fault-merged records are byte-identical to the clean merged
  records (W1's positive bounds kept verbatim, injected negative bounds
  absorbed to 255 by the max-combine); fault merge structural counts
  equal the clean merge exactly (corruptions changed values only).
  The merge-time detection catchment is thereby characterized:
  logical contradictions in the COMBINED values (win-vs-lose, and
  win<=nowin / lose<=nolose when both sides are real bounds) are
  detected exactly; a single worker's negative bound is absorbed under
  other workers' unbound 255 sentinels by design (it is not a logical
  contradiction - "not detectable" here means "not a contradiction",
  which is the intended semantics of the sentinel-combine merge).

## Experimental facts recorded during the build (implementation lessons)

1. The sandbox cgroup memory limit is ~1 GiB. The first fault-test
   implementation loaded all four distinct tables into Python lists and
   was OOM-killed twice with NO traceback and NO output (silent SIGKILL
   mid-run; confirmed only via dmesg oom-kill lines and memory.events).
   Lesson: a background job that produces zero output may be dead, not
   busy; check /proc and dmesg, and design streaming from the start.
2. `cd dir && setsid ... & echo; tail dir/file` - the `&` binds the cd
   too, so the foreground `tail` ran in the wrong cwd and made the log
   look missing. Background a `bash -c 'cd ... && exec ...'` instead.
3. The F5 scenario as first designed ("W3 record with all four values
   255") selected 0/2 keys: real distinct tables never contain fully
   unbound records (every stored record carries a win or lose bound).
   Since verbatim nowin/nolose are always the 255 sentinel (K0907),
   injecting a negative bound into an arbitrary W3 record is always
   well-posed; the scenario was relaxed accordingly.
4. The first cross-merge gate comparison failed on a pure type
   mismatch (Python int histogram keys vs JSON string keys); normalize
   before comparing.

## Interpretation guard

Measurement and synthetic-corruption tests only. No new WIN/LOSS
verdicts, no manifest row opened or closed, certificate bytes unchanged,
the natural merged seed is not affected by the fault test. The
repo-verbatim extractor is unmodified in the repo (published determinism
chains). WIN7-D10 proves a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 is not a LOSS proof. The
11x11 empty board, both two-stone roots {49,60} and {59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

## Resume pointers

- The merge+seed pipeline is now validated end to end at N=4 (safety,
  determinism, completeness, detection exactness). A production
  coordinator can merge worker dumps at the 64%-load capacity point
  with the sentinel-combine rules as written.
- Seed-insert failure rate is seed-size dependent (0.034% at 4.29M,
  0.324% at 4.99M); if larger seeds are planned, re-budget the probe
  window or the failure gate, or seed into a bigger table.
- The fold chain (66i/66j/69j/71e/72d/73i...) remains under the
  parallel claim lane's management; do not touch until published. The
  73i certificate publication was still pending at session start;
  do not touch it either.
- The remaining extractor copies (sweep engine, chunk prover,
  FBT-saturation runners) are still unaudited (K0907 follow-up).
