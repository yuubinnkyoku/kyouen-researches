# n11 ninth-cost 12-row adoption flip-census + reaudit refresh kit

Kit of the FOLLOW-UP Part declared in the ninth-cost 12-row canonical
adoption completion log (commit 5e8e8729, restated in the adoption
manifest interpretation_guard field): the BASE (0935c94c..., the
eighth-cost k01 head of record, 6,875 rows WIN 203 / LOSS 6,672) vs
SCENARIO (47280073..., the adopted ninth-cost 12-row head of record,
6,887 rows WIN 206 / LOSS 6,681) class-status census measurement and
the reaudit refresh of the new canonical head.

## Files

- reaudit/scripts/refresh_adoption_ninthcost12.py - byte-clone of the
  published eighth-cost k01 refresh 7e11a316... (itself the disclosed
  clone chain SZ wave E d8b14697... <- SV fd2e799e... <- ST
  02987d1c... <- SQ 60dfb1a1... <- SP 82ddb89c... <- sixthwin5
  92a884c9... <- EM 7f379b71... <- EV f2edac3e... <- EU 6dc24c15...),
  differing in EXACTLY the three regions (docstring, CACHE path,
  expected cache sha); every computation byte is identical.  sha256
  c9a7372ad4c6ff0abf49ef18ea72e8f9563ead88d3c1606dbbcfcb8ab1655812.
- reaudit/output/refresh-summary.json - refreshed class census against
  the adopted ninth-cost head.  sha256
  ffce222f9ede0563dc5dc56e196ed5a97b0a417e98e9332a3feb7f1579210d06.
- reaudit/output/closure-classes.csv - refreshed closure ladder (804
  rows).  sha256
  d7ae77ddd05d433c0a59555f86efb009e64a5651ad6b918407682bdc5f3178f0 -
  differs from the published eighth-cost BASE side (measured churn:
  class 1792 unknown 100 -> 99, rank 537 -> 516; 21 band classes
  516..536 shift down by one; no entered/left).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  8cc804bb31fcc29393ee4e06c79e9eb407f10917a7996440c6116e78df5aa670 -
  differs from the BASE side in exactly one row (root 26 individual
  greedy union 5,229 -> 5,228; free_now/uncovered identical on all 20
  roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (3,715,222 bytes, sha256
  396c05ae7936ba9df6e3da767f5fa710512ccf91c347bb619fe0cbcc69687f42);
  UNPUBLISHED per size policy, pin recorded in the census json and
  MANIFEST.
- scripts/measure_census_deltas_ninthcost12.py - fresh measurer
  (structural adaptation of the eighth-cost k01 measurer 9c1b79a7...,
  fresh 12-row expectations, WIN-side flip audit).  sha256
  d81113df34c6ac74e35976291e8c0675681fec172f0d5e7196b91b4ed48afd6b.
- output/census-deltas-ninthcost12-adoption.json - the flip-census
  measurement record.  sha256
  3ea6491f19c258e5b400b0da01dd5ee4f60f7bb9bbb9ec17c74a5a5cacba832a.

## Inputs (all published-byte-verbatim, sha-verified in-script)

base head 0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d5
90e9ca4 (eighth-cost k01 adoption merged cache); adopted head
4728007306598298f7fdb43d0368bc4e5fbd6c9435a38f8d1732d1df8368a622
(ninth-cost 12-row adoption merged cache); increment 72eac70c...;
adoption manifest db43c1a5...; frozen dependency graph 54f9c364...;
update8 plan b658290a...; evidence policy 78655e94...; quarantine
registry 81d23160...; board source 954d3a10...; merger 90711961...
(Part SV kit); BASE-side reaudit outputs ff5c1586... / ae1d0a7f... /
81b17904... (eighth-cost k01 reaudit kit); BASE-side worklist regen
pin 76b77442... / 3,715,383 bytes (from the published eighth-cost
census json 9f25fd99...).

## Run record (this host, Python 3.12; execution preceded
publication, disclosed; the Part itself was pre-declared in the
adoption completion log 5e8e8729 before any run)

- refresh: three runs, all four outputs byte-identical each time
  (refresh-summary.json ffce222f..., closure-classes.csv
  d7ae77dd..., per-root-coverage.csv 8cc804bb..., probe-worklist.csv
  396c05ae...; stdout b0f8c330... x3), ~71s/run.
- measurer: two runs byte-identical (census json 3ea6491f... x2,
  stdout a4cfee82... x2), all fail-closed gates PASS.
- tamper battery 5/5 fail-closed (scratch edits, restored, clean
  control re-PASS byte-identical): T1 scen summary census unknown
  value flip, T2 increment k12 WIN->LOSS verdict flip, T3 scen
  closure unknown_now value flip, T4 phantom excluded_now census
  count, T5 phantom appended closure row (row-count gate 804).

## Measured flip-census results (deltas of the ninth-cost 12-row
adoption)

- Class census BASE -> SCEN: unknown 34,400 -> 34,393;
  excluded_now 120 -> 127; free_now 39 -> 39 (Board-verified both
  sides, zero rejections); excluded 390 -> 390.
- WIN-side status flips (Part EW/EM win-hit mechanism), MEASURED:
  exactly 7 classes, the owner-class union of the three adopted WIN
  rows k12 (s5 index 78950), k02 (62804) and k07 (37372), each unknown
  -> excluded_now: classes 735 (1152921539100807168:0), 1347
  (1152921539117580288:0), 1780 (1153203014077513728:0), 1845 (the
  ninth-cost serving class 1297036692683751424:134217728,
  cost-unknown 99 -> 87, all twelve adopted rows owned here), 16293
  (1152921504607895552:32832), 31179 (1152921505144766464:68719476736)
  and 31563 (1152921504607895552:67141632).  No other flip direction
  occurs; no class flips to free_now; every adopted row's owner
  histogram is {"3": 12} and the serving class 1845 owns all 12 rows.
- The nine LOSS rows flip nothing: their owner classes keep their
  status; class 1792 (1297036692716388352:0, a LOSS-row owner class)
  merely drops cost-unknown 100 -> 99 - the closure ladder's single
  measured unknown_now churn.
- Closure ladder: 804 -> 804 rows, entered [], left [], exactly one
  unknown_now churn (class 1792, 100 -> 99) and 22 rank churns (1792:
  537 -> 516; the 21 passed classes 516..536 shift down by one); the
  CSV differs from the BASE side (unlike the single-row eighth-cost
  adoption, this 12-row adoption re-ranks the ladder).
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  exactly one individual greedy re-route is measured (root 26,
  5,229 -> 5,228).
- update8 refresh: all twelve adopted s5 indices sit OUTSIDE the
  frozen baseline requirement, so resolved 282 -> 282, remaining_now
  31,444 -> 31,444, groups_free_now 131 -> 131; the win-hit group set
  is unchanged (25 groups, none of the seven flipped classes is an
  update8 plan group class).
- Joint greedy: 37,398 -> 37,398 (identical).  Probing worklist:
  64,273 -> 64,272 (regen sha 396c05ae... differs from the BASE pin
  76b77442..., size 3,715,222 vs 3,715,383).

## Meaning and non-meaning

Adopting the twelve published ninth-cost rows changes solver-trusted
S5 cache bookkeeping ONLY.  The WIN-side flips are class-status
bookkeeping inside the scheduling machinery (the EW/EM win-hit
mechanism) and the LOSS-side churn is closure-ladder bookkeeping:
they exclude no root, free no root, consume no root verdict, and
change no coverage claim.  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, its remaining third
moves {100,108}, S2 and all closure classes remain UNKNOWN.  A WIN(1)
or LOSS(2) S5 raw is not a class closure claim, not a root verdict,
and transfers nothing.  Nodes are bookkeeping, never verdicts.

## Honest disclosures

- Execution preceded kit publication (the Part was pre-declared in
  the adoption completion log 5e8e8729 and in the adoption manifest
  interpretation_guard field before any run); this matches the
  disclosed eighth-cost k01 reaudit precedent.
- The measurer adaptation had one wrong hand-written expectation
  (a |rank delta| == 1 assertion that the measured class-1792
  leapfrog 537 -> 516 violates); caught by the assertion itself
  BEFORE any PASS run, replaced with the measured churn map (1792
  537 -> 516 plus 21 single-step shifts), re-run from scratch.  The
  final published bytes are the fixed version only.
- Single implementation (the published refresh byte-clone plus this
  measurer); no solver search was run in this Part; no new S5 raws
  were produced.
