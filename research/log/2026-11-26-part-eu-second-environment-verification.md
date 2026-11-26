# Part EU full second-environment verification (2026-11-26)

Closes the OPEN item recorded by the EU wave-F completion (76835aa8:
"Part EU full second-environment verification stays OPEN; SPOT
re-execution recorded cf699df2").  The published post-repair kit bytes
were fetched from main, byte-verified against every pin, and the full
fail-closed extractor battery was executed to rc=0 twice consecutively
in this fresh container - the first FULL second-environment completion
of the Part EU kit (the earlier cf699df2 record was an honest scoped
SPOT re-execution: one battery run, observation only, artifacts lost
to a sandbox reset before a second run).

Nothing was consumed and no repo byte was modified by the verification
itself (the scratch tree is local-only; no push of kit bytes).  The
verdict scope of Part EU is unchanged exactly as wave F recorded: the 2
ET-C++-gate-verified WIN rows ai007/ai040 of closure class 30345 stay
the only EU consumption; the standard 11x11 empty board and every
central-reply root stay UNKNOWN; nodes are bookkeeping.

## Fetch record (published bytes only)

All files fetched from main pinned at commit
b81464150231d7e40cec8fb999ed0f947c42116a (HEAD at verification time),
commit-pinned raw fetches:

* EU kit `research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125/`:
  all 14 MANIFEST-sha256 entries fetched, sha256+size verified 14/14
  (merger 90711961, maker f2ae97a1, repaired extractor 9bc5f06a,
  disclosed-repair refresh fork 6dc24c15, increment d9365d80,
  manifest 793f68c5, merged cache 3ba48608, merge-audits x3 9f807c95,
  decomp 8d4a5743, refresh outputs 2b70bb55/59a4c85f/cfc2bfe1);
* the 24 extractor input pins fetched byte-exact: BASE-side Part ER kit
  members (refresh script 6c91e0ce, merged BASE cache 9c4dd94e 6,765
  rows, ER increment 4f6b7797, refresh-summary a6b8d082,
  closure-classes 4c03f965, per-root-coverage 1bf6c25a), the frozen
  pins (dependency-graph 54f9c364, update8 b658290a, Board source
  954d3a10, policy 78655e94, quarantine 81d23160) and the b38 SSOT
  batch-keys 29807104;
* the extracted input pin table inside compare_deltas_eu_adoption.py
  (24 entries) was re-verified against all fetched bytes BEFORE the
  battery ran - zero drift (byte-for-byte equal to the published kit,
  no local surgery performed; the D0 repair bytes 9bc5f06a/6dc24c15 are
  used exactly as published).

## Battery execution (this environment, container-fresh)

* run1: rc=0, wall 2m0.9s (real 2m0.874s; user 1m56.8s);
* run2: rc=0, wall 1m59.3s (real 1m59.316s; user 1m57.9s);
* stdout run1 vs run2: byte-identical (cmp), exactly:

  `EU decomp OK: flips=6 caches=6765->6767 win=186->188 closure_left=[] greedy=36619->36619 decomp_sha=8d4a574359dd8f5c8e1bc140fbd4fefc533fcf71049bc80f9d06a9fdc8dcba00`

* inside EACH run the battery fail-closed re-executed BOTH refresh forks
  byte-verbatim in isolated scratch trees (BASE: the published Part ER
  refresh 6c91e0ce; SCEN: the disclosed-repair Part EU fork 6dc24c15)
  and verified all EIGHT regenerated outputs against their
  publication/regen pins (2b70bb55 / 59a4c85f / cfc2bfe1 / 397a4379 and
  a6b8d082 / 4c03f965 / 1bf6c25a / 78e499dd) - zero drift, zero
  conflicts;
* the regenerated decomposition was byte-identical to the pristine
  published `output/decomp-deltas-euwin2-adoption.json` pin 8d4a5743
  after run1 AND after run2 (cmp against a preserved pristine copy;
  sha256 re-verified 8d4a5743... both times) - the same decomp sha the
  wave-D0 close-out and the cf699df2 SPOT run observed, now reproduced
  in a THIRD independent execution environment;
* the battery re-derived machine-verified, inside each run: the 24 pin
  table, the manifest decomposition (schema euwin2-increments-manifest-v1)
  with the ER regression tie (18 rows WIN in BASE, not re-adopted),
  SCEN == BASE + exactly the 2 increment rows (6,767 rows WIN 188 /
  LOSS 6,579), the independent full-class census (34,436/84/39/390 ->
  34,430/90/39/390, EXACTLY 6 UNKNOWN->excluded_now flips
  {12846, 12875, 13801, 30282, 30308, 30326}, 30345 NOT double-flipping),
  the Board class arithmetic (30345: 51-raw/50-cost unknown 7->5;
  30354 untouched 96->96), closure 805->805 zero churn with the only
  rank swap {30345: 8->7, 20421: 7->8}, update8 static (260/31,505/131,
  union 31,859), win_hit groups unchanged (the 10 class-30354 quartets),
  Board verification 39/39 both sides, per-root greedy changes only at
  roots 12 (2850->2848) and 36 (3007->3005), joint greedy 36,619
  static, worklist 64,309 -> 64,307.

## Cross-environment invariants (measurement discipline)

The battery's stdout and decomposition carry NO wall-clock fields, so
unlike the Part ET/EV audit JSONs (where per-pass wall_s verbatim
quoting makes cross-environment byte-identity impossible by design),
the full Part EU battery output IS byte-identical across environments:
stdout pair byte-identical here, decomp byte-identical to the published
pin, deterministic content across three execution environments (wave-D
declaring session, cf699df2 SPOT, this verification).  Wall-time
differences are disclosed above and carry no verification weight.

## Honest scope

* this log records ONLY the verification; it adopts nothing, consumes
  nothing, changes no kit byte;
* the NOT-consumed set is unchanged: the 21 unconsumed closure-batch
  LOSS rows (EM-pattern territory), k04 sixth-cost WIN, b018/d002/e002/
  f017 are EV-consumed (Part EV closed, BASE of record 63f33c4f
  6,771 rows WIN 192 / LOSS 6,579), every other unconsumed probe-level
  WIN stays unconsumed;
* the Part EU OPEN item recorded in the EV completion log is now
  CLOSED by this log; the canonical BASE of record 63f33c4f... is
  unchanged by this verification;
* standard 11x11 empty board, all 19 central-reply roots, the
  two-stone roots, S2 and every closure class: UNKNOWN; no coverage
  claim anywhere.
