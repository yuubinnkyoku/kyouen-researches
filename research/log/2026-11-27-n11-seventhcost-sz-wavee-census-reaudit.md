# 2026-11-27 n11 Part SZ wave E: seventh-cost adoption census measurement + reaudit refresh completed

Part SZ wave E (the follow-up pre-registered in the Part SZ wave A
declaration and restated in the completion log) is complete.  Kit:
research/experiments/n11-seventhcost-sz-reaudit-20261127.

The BASE (42dbb58f..., the Part SV head of record, 6,832 rows WIN
201 / LOSS 6,631) vs SCENARIO (5b6e77f7..., the adopted seventh-cost
head of record, 6,874 rows WIN 202 / LOSS 6,672) census measurement
was taken with a fresh measurer (structural adaptation of the
published Part SV measurer 2695e618..., fresh 42-row expectations),
and the reaudit refresh of the new canonical head was run with a
byte-clone of the published Part SV refresh fd2e799e... (differing
in exactly the three regions: docstring, CACHE path, expected cache
sha; every computation byte identical, diff verified).

## Measured results (all fail-closed gate verified, rc=0)

- SCEN cache equals BASE rows + exactly the 42 increment rows
  (41 LOSS + 1 WIN), every adopted row fresh to BASE, verdicts and
  nodes byte-matched to the increment; adoption manifest pins all
  re-verified (schema seventhcost42-adoption-manifest-v1, frozen
  pins graph 54f9c364 / quarantine 81d23160 / policy 78655e94 /
  merger 90711961, freshness 42, conflicts 0).
- Class census BASE -> SCEN: unknown 34,405 -> 34,403;
  excluded_now 115 -> 117; free_now 39 -> 39 (Board-verified 39/39
  both sides, zero rejections); excluded 390 -> 390.  The recount
  reproduces the published refresh summaries exactly on both
  sides.
- WIN-side status flips (Part EW/EM win-hit mechanism), MEASURED:
  exactly 2 classes, both owner classes of the single adopted WIN
  row k05 1152921504607932416:536870912 (s5 index 114754):
  class 3291 (the seventh-cost serving class
  1306043891938492416:0, cost-unknown 100 -> 58, all 42 adopted
  rows owned here) and class 25463 (1152921504607932416:0), each
  unknown -> excluded_now.  The flip list equals the WIN row owner
  class set exactly; no other flip direction occurs; no class
  flips to free_now.  This is the first WIN-side flip set since
  the WIN-side adoption series; it is class-status bookkeeping
  only.
- update8 refresh: exactly one adopted LOSS row
  (1306044991450120192:0, s5 index 111999) sits inside the frozen
  baseline requirement (resolved 281 -> 282, remaining_now
  31,445 -> 31,444); the WIN key sits OUTSIDE the requirement;
  the win-hit group set is unchanged (25 groups).
- Closure ladder churn (measured, non-empty): 804 -> 804 rows,
  entered [1579], left [13970], unknown_now churn at 25462
  (97 -> 96) and 25489 (104 -> 103), 45 rank churn rows.  Both
  flipped classes are outside the ladder on both sides.
- Per-root coverage: free_now/uncovered identical on all 20
  roots; individual greedy re-route on roots 14 (4,538 -> 4,537)
  and 15 (5,990 -> 5,977); joint greedy 36,789 -> 37,398; probing
  worklist 64,275 -> 64,273 (regen sha256 2987300a...,
  3,715,383 bytes, unpublishable per size policy; BASE side pin
  b946ed06... re-verified from the published Part SV census json
  dc3d4e3c...).

## Verification

- Determinism: refresh three runs, all four outputs byte-identical
  each time (refresh-summary 3944bf1c..., closure-classes
  ae1d0a7f..., per-root-coverage 81b17904..., probe-worklist
  2987300a...; stdout f26de9c0... x3); measurer two runs
  byte-identical (census json 33563471... x2).
- Tamper battery 5/5 fail-closed on scratch copies with restore
  and clean-control re-PASS (T1 scen census value flip, T2
  increment k05 WIN->LOSS verdict flip, T3 scen closure
  unknown_now value flip, T4 phantom excluded_now census count,
  T5 phantom appended closure row caught by the 804 row-count
  gate).  Disclosed: the first T5 attempt used a sed append that
  silently did not apply (rc=0 with no tamper actually present);
  the harness bug was fixed with an explicit echo append and the
  gate then failed closed as designed.
- All 16 pinned inputs byte-verified on this host before any run
  (base head 42dbb58f..., adopted head 5b6e77f7..., increment
  959ae2dd..., manifest 14ef4fc2..., graph 54f9c364..., update8
  b658290a..., policy 78655e94..., quarantine 81d23160..., board
  954d3a10..., merger 90711961..., SV refresh-summary
  451c1e36..., SV closure 0eb19c89..., SV per-root 1828d7f7...,
  SV census json dc3d4e3c..., SV refresh runner 9500cc66..., SV
  measurer 2695e618...).

## Meaning and non-meaning

The wave E measurement records the scheduling-bookkeeping effect
of the already-published seventh-cost adoption.  NO root verdict
is consumed, no root freed, no root excluded, no coverage claim
made or changed.  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, its remaining
third moves {100,108}, S2 and all closure classes remain UNKNOWN.
A WIN(1) or LOSS(2) S5 raw is not a class closure claim, not a
root verdict, and transfers nothing.  Nodes and expansions are
bookkeeping, never verdicts.

## Frozen pins (wave E kit)

- refresh: d8b146977e8ec907ae49799597bdb237bec80251f7d5f1ba4dc112864f18cadf
- measurer: 29317c934b9ced15446f4702933ee114d8b8a18f5df136e6c86e32e5f90ab2f5
- refresh-summary: 3944bf1c5353abdf5772230774d56c4be7c67569080505364ef9ed793c0d05f1
- closure-classes: ae1d0a7f32b02db148c3123c9fb6b57610beb4754ba8e491a3d145f199110533
- per-root-coverage: 81b17904ec3ba8a530a54e4f315e1e225191ef5c1d62b6fb4b648bbe797775ff
- probe-worklist (unpublished, pin only): 2987300a57e3ed1594c5058221e5b81cf24af27447d43f627bd59bae4e65e8eb
- census json: 335634710a577fa1fa3bbbbd1bc6507fc418d3ac46b951ab85ce6897b087a24f
- README: 648270e86eb95402a68382c062406f16d86f25b887d8587bb053c4a7eb02e6e3
- MANIFEST-sha256.txt: 551bdda6924c339391fc94445e941488a4a2af887cfea7aed27332acb889d279

## Next

- The canonical head of record is 5b6e77f7... (6,874 rows WIN 202
  / LOSS 6,672); the serving class 3291 is now excluded_now with
  cost-unknown 58, so the adaptive coordinator's next selection
  proceeds from the refreshed worklist (64,273 entries) against
  the adopted head.
- 11x11 stays UNKNOWN; every root verdict stays UNKNOWN.
