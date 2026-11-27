# n11 Part SZ wave E kit: seventh-cost 42-row adoption census + reaudit refresh

Kit of the Part SZ wave A declaration's pre-registered wave E
follow-up (restated in
research/log/2026-11-27-n11-seventhcost-sz-adoption-completion.md):
the BASE (42dbb58f..., the Part SV head of record, 6,832 rows WIN
201 / LOSS 6,631) vs SCENARIO (5b6e77f7..., the adopted seventh-cost
head of record, 6,874 rows WIN 202 / LOSS 6,672) census measurement
and the reaudit refresh of the new canonical head.

## Files

- reaudit/scripts/refresh_adoption_seventhcost42.py - byte-clone of
  the published Part SV refresh fd2e799e... (itself the disclosed
  clone chain ST 02987d1c... <- SQ 60dfb1a1... <- SP 82ddb89c... <-
  sixthwin5 92a884c9... <- EM 7f379b71... <- EV f2edac3e... <-
  EU 6dc24c15...), differing in EXACTLY the three regions
  (docstring, CACHE path, expected cache sha); every computation
  byte is identical.  sha256 d8b14697...
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted head.  sha256 3944bf1c...
- reaudit/output/closure-classes.csv - refreshed closure ladder
  (804 rows).  sha256 ae1d0a7f...
- reaudit/output/per-root-coverage.csv - refreshed per-root
  coverage (20 roots).  sha256 81b17904...
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (3,715,383 bytes, sha256 2987300a...); UNPUBLISHED per size
  policy, pin recorded in the census json and MANIFEST.
- scripts/measure_census_deltas_seventhcost42.py - fresh wave E
  measurer (structural adaptation of the Part SV measurer
  2695e618..., fresh 42-row expectations, WIN-side flip audit).
  sha256 29317c93...
- output/census-deltas-seventhcost42-adoption.json - the wave E
  census measurement record.  sha256 33563471...

## Inputs (all published-byte-verbatim, sha-verified in-script)

base head 42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e1421
2055bdc4; adopted head 5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8
b817e5d560f95499fcdde2; increment 959ae2dd...; adoption manifest
14ef4fc2...; frozen dependency graph 54f9c364...; update8 plan
b658290a...; evidence policy 78655e94...; quarantine registry
81d23160...; board source 954d3a10...; merger 90711961...;
BASE-side reaudit outputs 451c1e36... / 0eb19c89... / 1828d7f7...
(Part SV kit); BASE-side worklist regen pin b946ed06...
(3,715,960 bytes, from the published Part SV census json
dc3d4e3c...).

## Run record (this host, Python 3.12)

- refresh: three runs, all four outputs byte-identical each time
  (refresh-summary.json 3944bf1c..., closure-classes.csv
  ae1d0a7f..., per-root-coverage.csv 81b17904...,
  probe-worklist.csv 2987300a...; stdout f26de9c0... x3), ~56s/run.
- measurer: two runs byte-identical (census json 33563471... x2),
  all fail-closed gates PASS.
- tamper battery 5/5 fail-closed (scratch copies, restored and
  clean control re-PASS byte-identical): T1 scen summary census
  value flip, T2 increment k05 WIN->LOSS verdict flip, T3 scen
  closure unknown_now value flip, T4 phantom excluded_now census
  count, T5 phantom appended closure row (row-count gate 804).
  Disclosure: the first T5 attempt used a sed append that silently
  did not apply (rc=0 with no tamper present); the harness bug was
  fixed with an explicit echo append and the gate then failed
  closed as designed.

## Measured wave E results (census deltas of the adoption)

- Class census BASE -> SCEN: unknown 34,405 -> 34,403;
  excluded_now 115 -> 117; free_now 39 -> 39 (Board-verified both
  sides, zero rejections); excluded 390 -> 390.
- WIN-side status flips (Part EW/EM win-hit mechanism), MEASURED:
  exactly 2 classes, both owner classes of the single adopted WIN
  row k05 1152921504607932416:536870912 (s5 index 114754):
  class 3291 (the seventh-cost serving class
  1306043891938492416:0, cost-unknown 100 -> 58, all 42 adopted
  rows owned here) and class 25463 (1152921504607932416:0), each
  unknown -> excluded_now.  No other flip direction occurs; no
  class flips to free_now; the flip list equals the WIN row owner
  class set exactly.
- Owner histogram of the 42 adopted rows: 1 owner x1, 2 owners x2,
  3 owners x38, 4 owners x1.
- update8 refresh: exactly one adopted LOSS row
  (1306044991450120192:0, s5 index 111999) sits inside the frozen
  baseline requirement: resolved 281 -> 282, remaining_now 31,445
  -> 31,444; the WIN key sits OUTSIDE the requirement; the win-hit
  group set is unchanged (25 groups, both owner classes are not
  update8 plan group classes).
- Closure ladder churn (measured, non-empty): 804 -> 804 rows,
  entered [1579], left [13970], unknown_now churn at 25462
  (97 -> 96) and 25489 (104 -> 103), 45 classes change rank.
- Per-root coverage: free_now/uncovered identical on all 20
  roots; individual greedy re-route on roots 14 (4,538 -> 4,537)
  and 15 (5,990 -> 5,977); joint greedy 36,789 -> 37,398.
- Probing worklist: 64,275 -> 64,273; regen sha256 2987300a...
  (3,715,383 bytes, unpublishable per size policy).

## Meaning and non-meaning

Adopting the 42 published seventh-cost rows changes solver-trusted
S5 cache bookkeeping ONLY.  The WIN-side flips are class-status
bookkeeping inside the scheduling machinery (the EW/EM win-hit
mechanism): they exclude no root, free no root, consume no root
verdict, and change no coverage claim.  The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27}, its
remaining third moves {100,108}, S2 and all closure classes remain
UNKNOWN.  A WIN(1) or LOSS(2) S5 raw is not a class closure claim,
not a root verdict, and transfers nothing.  Nodes and expansions
are bookkeeping, never verdicts.
