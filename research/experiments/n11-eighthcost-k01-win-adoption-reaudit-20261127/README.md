# n11 eighth-cost k01 WIN adoption flip-census + reaudit refresh kit

Kit of the FOLLOW-UP Part declared in the eighth-cost k01 WIN row
canonical adoption completion log (commit d108bae0, restated in the
adoption manifest `follow_up_declared` field): the BASE
(5b6e77f7..., the Part SZ head of record, 6,874 rows WIN 202 /
LOSS 6,672) vs SCENARIO (0935c94c..., the adopted eighth-cost k01
head of record, 6,875 rows WIN 203 / LOSS 6,672) class-status census
measurement and the reaudit refresh of the new canonical head.

## Files

- reaudit/scripts/refresh_adoption_eighthcost_k01.py - byte-clone of
  the published Part SZ wave E refresh d8b14697... (itself the
  disclosed clone chain SV fd2e799e... <- ST 02987d1c... <- SQ
  60dfb1a1... <- SP 82ddb89c... <- sixthwin5 92a884c9... <- EM
  7f379b71... <- EV f2edac3e... <- EU 6dc24c15...), differing in
  EXACTLY the three regions (docstring, CACHE path, expected cache
  sha); every computation byte is identical.  sha256 7e11a316...
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted eighth-cost head.  sha256 ff5c1586...
- reaudit/output/closure-classes.csv - refreshed closure ladder
  (804 rows).  sha256 ae1d0a7f... - BYTE-IDENTICAL to the published
  Part SZ wave E BASE-side output (measured, no churn at all).
- reaudit/output/per-root-coverage.csv - refreshed per-root
  coverage (20 roots).  sha256 81b17904... - BYTE-IDENTICAL to the
  published Part SZ wave E BASE-side output (measured).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (3,715,383 bytes, sha256 76b77442...); UNPUBLISHED per size
  policy, pin recorded in the census json and MANIFEST.
- scripts/measure_census_deltas_eighthcost_k01.py - fresh measurer
  (structural adaptation of the Part SZ wave E measurer 29317c93...,
  fresh single-row expectations, WIN-side flip audit).
  sha256 9c1b79a7...
- output/census-deltas-eighthcost-k01-adoption.json - the flip-census
  measurement record.  sha256 9f25fd99...

## Inputs (all published-byte-verbatim, sha-verified in-script)

base head 5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f9549
9fcdde2 (Part SZ adoption merged cache); adopted head
0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4
(eighth-cost k01 adoption merged cache); increment 8e649a0a...;
adoption manifest 09cf869e...; frozen dependency graph 54f9c364...;
update8 plan b658290a...; evidence policy 78655e94...; quarantine
registry 81d23160...; board source 954d3a10...; merger 90711961...
(Part SV kit); BASE-side reaudit outputs 3944bf1c... / ae1d0a7f... /
81b17904... (Part SZ wave E kit); BASE-side worklist regen pin
2987300a... (3,715,383 bytes, from the published Part SZ wave E
census json 33563471...).

## Run record (this host, Python 3.12; execution preceded
publication, disclosed; the Part itself was pre-declared in the
adoption completion log d108bae0 before any run)

- refresh: three runs, all four outputs byte-identical each time
  (refresh-summary.json ff5c1586..., closure-classes.csv
  ae1d0a7f..., per-root-coverage.csv 81b17904...,
  probe-worklist.csv 76b77442...; stdout d96dbef4... x3), ~55s/run.
- measurer: two runs byte-identical (census json 9f25fd99... x2,
  stdout byte-identical), all fail-closed gates PASS.
- tamper battery 5/5 fail-closed (scratch edits, restored, clean
  control re-PASS byte-identical): T1 scen summary census unknown
  value flip, T2 increment k01 WIN->LOSS verdict flip, T3 scen
  closure unknown_now value flip, T4 phantom excluded_now census
  count, T5 phantom appended closure row (row-count gate 804).

## Measured flip-census results (deltas of the eighth-cost k01
adoption)

- Class census BASE -> SCEN: unknown 34,403 -> 34,400;
  excluded_now 117 -> 120; free_now 39 -> 39 (Board-verified both
  sides, zero rejections); excluded 390 -> 390.
- WIN-side status flips (Part EW/EM win-hit mechanism), MEASURED:
  exactly 3 classes, all owner classes of the single adopted WIN row
  k01 1297036692750860288:64 (s5 index 91779, graph-derived owner
  set, fresh to BASE): class 2182 (1154117773392084992:0), class
  2197 (the eighth-cost serving class 1297036692750860288:0,
  cost-unknown 100 -> 99, the adopted row owned here) and class
  16914 (1152921504675004416:64), each unknown -> excluded_now.  No
  other flip direction occurs; no class flips to free_now; the flip
  list equals the WIN row owner class set exactly (owner histogram
  {"3": 1}).
- update8 refresh: the single adopted s5 index 91779 (WIN) sits
  OUTSIDE the frozen baseline requirement; resolved 282 -> 282,
  remaining_now 31,444 -> 31,444; the win-hit group set is unchanged
  (25 groups, none of the three owner classes is an update8 plan
  group class).
- Closure ladder: 804 -> 804 rows, entered [], left [], unknown_now
  churn [], rank churn 0, and the CSV is BYTE-IDENTICAL to the BASE
  side (measured; unlike the seventh-cost 42-row adoption this
  single-WIN adoption re-ranks nothing).
- Per-root coverage: byte-identical on all 20 roots; no greedy
  re-route (greedy delta []).  Joint greedy 37,398 -> 37,398.
- Probing worklist: 64,273 -> 64,273 (total identical; regen sha
  76b77442... differs from the BASE pin 2987300a..., same size).

## Meaning and non-meaning

Adopting the single published k01 WIN row changes solver-trusted S5
cache bookkeeping ONLY.  The WIN-side flips are class-status
bookkeeping inside the scheduling machinery (the EW/EM win-hit
mechanism): they exclude no root, free no root, consume no root
verdict, and change no coverage claim.  The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27}, its
remaining third moves {100,108}, S2 and all closure classes remain
UNKNOWN.  A WIN(1) or LOSS(2) S5 raw is not a class closure claim,
not a root verdict, and transfers nothing.  Nodes are bookkeeping,
never verdicts.

## Honest disclosures

- Execution preceded kit publication (the Part was pre-declared in
  the adoption completion log d108bae0 and in the adoption manifest
  follow_up_declared field before any run); this matches the
  disclosed Part SZ wave E precedent.
- The measurer adaptation had two path-region slips (BASE_CACHE and
  MERGER path constants pointed at the wrong kit directories) and
  one hand-typed sha typo (at15m pair pin), each caught by
  fail-closed gates or FileNotFoundError BEFORE any PASS run; fixed
  and re-run from scratch.  The final published bytes are the fixed
  version only.
- Single implementation (the published refresh/merger byte-clones
  plus this measurer); no solver search was run in this Part; no new
  S5 raws were produced.
