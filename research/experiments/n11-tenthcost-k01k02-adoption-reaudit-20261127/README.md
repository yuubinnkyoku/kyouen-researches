# n11 tenth-cost k01/k02 adoption flip-census + reaudit refresh kit

Kit of the FOLLOW-UP Part declared in the tenth-cost k01/k02
canonical adoption completion log (commit b4cefa42, restated in the
adoption manifest status_guard field): the BASE (47280073..., the
ninth-cost 12-row head of record, 6,887 rows WIN 206 / LOSS 6,681) vs
SCENARIO (16b34014..., the adopted tenth-cost k01/k02 head of record,
6,889 rows WIN 207 / LOSS 6,682) class-status census measurement and
the reaudit refresh of the new canonical head.

## Files

- reaudit/scripts/refresh_adoption_tenthcost2.py - byte-clone of the
  published ninth-cost 12-row refresh c9a7372a... (itself the
  disclosed clone chain eighth-cost k01 7e11a316... <- SZ wave E
  d8b14697... <- SV fd2e799e... <- ST 02987d1c... <- SQ 60dfb1a1...
  <- SP 82ddb89c... <- sixthwin5 92a884c9... <- EM 7f379b71... <- EV
  f2edac3e... <- EU 6dc24c15...), differing in EXACTLY the three
  regions (docstring, CACHE path, expected cache sha); every
  computation byte is identical.  sha256
  280d706227d02e13a6f6b9b2f14f17ecc4b78a588503a266ce4177548ee1ac53.
- reaudit/output/refresh-summary.json - refreshed class census against
  the adopted tenth-cost head.  sha256
  40268a5e235851d798df9b59e0fd7622b2f667ae05cd447e5d4c1544c539ffef.
- reaudit/output/closure-classes.csv - refreshed closure ladder (804
  data rows).  sha256
  d7ae77ddd05d433c0a59555f86efb009e64a5651ad6b918407682bdc5f3178f0 -
  BYTE-IDENTICAL to the published ninth-cost BASE side (measured: no
  unknown_now churn, no rank churn, no entered/left; unlike the
  ninth-cost 12-row adoption the two adopted tenth-cost rows sit
  outside every closure-ladder class).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  8cc804bb31fcc29393ee4e06c79e9eb407f10917a7996440c6116e78df5aa670 -
  BYTE-IDENTICAL to the published ninth-cost BASE side (measured: no
  greedy re-route on any of the 20 roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (3,715,222 bytes, sha256
  b9f3f1a370974fe1cd895304b8a328d1863656725718b2b938bc2aa2d48a3d33);
  UNPUBLISHED per size policy, pin recorded in the census json and
  MANIFEST.  Same size as the BASE pin (3,715,222 bytes) but different
  content sha (the two adopted keys replace different worklist rows);
  the row count stays 64,272.
- scripts/measure_census_deltas_tenthcost2.py - fresh measurer
  (structural adaptation of the ninth-cost 12-row measurer d81113df...,
  fresh 2-row expectations, WIN-side flip audit).  sha256
  7e50308060eb6142d0c097ca678578c88721a10c21379d01c4808c12f7634a0f.
- output/census-deltas-tenthcost2-adoption.json - the flip-census
  measurement record.  sha256
  7cb90af4539b978abdeecd17cc9f925067d2a6bf1ce7c356235c0ac8517df492.

## Inputs (all published-byte-verbatim, sha-verified in-script)

base head 4728007306598298f7fdb43d0368bc4e5fbd6c9435a38f8d1732d1df
8368a622 (ninth-cost 12-row adoption merged cache); adopted head
16b340146fe8a01667ae31fc2f0534a8a3977e56b7c701803d621edc23312ef3
(tenth-cost k01/k02 adoption merged cache); increment 9a1c672b...;
adoption manifest 391dbd44...; frozen dependency graph 54f9c364...;
update8 plan b658290a...; evidence policy 78655e94...; quarantine
registry 81d23160...; board source 954d3a10...; merger 90711961...
(Part SV kit); BASE-side reaudit outputs ffce222f... / d7ae77dd... /
8cc804bb... (ninth-cost 12-row reaudit kit); BASE-side worklist regen
pin 396c05ae... / 3,715,222 bytes (from the published ninth-cost
census json 3ea6491f...).

## Run record (this host, Python 3.12; execution preceded
publication, disclosed; the Part itself was pre-declared in the
adoption completion log b4cefa42 before any run)

- refresh: three runs, all four outputs byte-identical each time
  (refresh-summary.json 40268a5e..., closure-classes.csv
  d7ae77dd..., per-root-coverage.csv 8cc804bb..., probe-worklist.csv
  b9f3f1a3...; stdout c121ed9b... x3), ~71s/run.  An initial
  three-way PARALLEL launch attempt was OOM-killed twice on this
  host (disclosed); all published bytes come from the sequential
  re-runs only.
- measurer: three runs byte-identical (census json 7cb90af4... x3),
  all fail-closed gates PASS.
- tamper battery 5/5 fail-closed (scratch edits, restored, clean
  control re-PASS byte-identical): T1 scen summary census unknown
  value flip -> recount gate; T2 increment k02 WIN->LOSS verdict flip
  -> sha-pin/win-key gates; T3 scen closure unknown_now value flip ->
  churn-measurement gate (byte-identity must hold); T4 phantom
  excluded_now census count -> recount gate; T5 phantom appended
  closure row -> closure byte-identity gate.  The first T5 harness
  attempt truncated the file to zero rows and was caught by the
  804-row count gate (a disclosed harness defect, redone properly
  with byte-verified append).

## Measured flip-census results (deltas of the tenth-cost k01/k02
adoption)

- Class census BASE -> SCEN: unknown 34,393 -> 34,391; excluded_now
  127 -> 129; free_now 39 -> 39 (Board-verified both sides, zero
  rejections); excluded 390 -> 390.
- WIN-side status flips (Part EW/EM win-hit mechanism), MEASURED:
  exactly 2 classes, the owner-class union of the single adopted WIN
  row k02 (s5 index 95628): class 2310 (the tenth-cost serving class
  1297036692683751424:131072, cost-unknown 100 -> 98, both adopted
  rows owned here) and class 16665 (1152921504607895552:96), each
  unknown -> excluded_now.  No other flip direction occurs; no class
  flips to free_now; the owner histogram is {"2": 1, "3": 1} (k01
  three owner classes, k02 two).
- The LOSS row k01 (s5 index 95304) flips nothing: its other owner
  classes 2287 and 12891 keep their unknown status (both adopted rows
  sit outside every closure-ladder class, so no ladder consumption
  occurs either).
- Closure ladder: 804 -> 804 rows, entered [], left [], NO
  unknown_now churn, NO rank churn; the CSV is byte-identical to the
  BASE side (unlike the ninth-cost 12-row adoption, this 2-row
  adoption does not re-rank the ladder).
- Per-root coverage: byte-identical to the BASE side; free_now/
  uncovered identical on all 20 roots; NO individual greedy re-route
  is measured.
- update8 refresh: both adopted s5 indices (95304, 95628) sit
  OUTSIDE the frozen baseline requirement, so resolved 282 -> 282,
  remaining_now 31,444 -> 31,444, groups_free_now 131 -> 131; the
  win-hit group set is unchanged (25 groups, neither flipped class
  is an update8 plan group class).
- Joint greedy: 37,398 -> 37,398 (identical).  Probing worklist row
  count: 64,272 -> 64,272 (regen sha b9f3f1a3... differs from the
  BASE pin 396c05ae..., same size 3,715,222 bytes).

## Meaning and non-meaning

Adopting the two published tenth-cost rows changes solver-trusted S5
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
  the adoption completion log b4cefa42 and in the adoption manifest
  status_guard field before any run); this matches the disclosed
  ninth-cost 12-row reaudit precedent.
- Single implementation (the published refresh byte-clone plus this
  measurer); no solver search was run in this Part; no new S5 raws
  were produced.
- The measurer expectations were machine-derived from the first
  measurement run (owner classes, flips, serving-class arithmetic,
  closure/per-root byte-identity) before the two determinism runs;
  no hand-written expectation was violated (no ninth-style churn-map
  bug arose because the measured churn sets are empty this time).
