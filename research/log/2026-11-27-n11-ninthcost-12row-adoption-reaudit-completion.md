# 2026-11-27 n11 ninth-cost 12-row adoption flip-census + reaudit completion

Completion log of the ninth-cost 12-row adoption flip-census /
reaudit Part (pre-declared in the adoption completion log 5e8e8729
and in the adoption manifest interpretation_guard). Commit chain:
adoption declaration 7780e2f8 -> adoption kit 6da937d9 -> adoption
completion 5e8e8729 -> flip-census + reaudit kit
`research/experiments/n11-ninthcost-12row-adoption-reaudit-20261127/`
(55fcc97e, 8 files + unpublished worklist pin, fetch-back 8/8
byte-identical).

## What was done

- Reaudit refresh: byte-clone of the published eighth-cost k01 refresh
  7e11a316... (3-region change only: docstring, CACHE path, expected
  sha 47280073...), run THREE times, all four outputs byte-identical
  each time (~71s/run): refresh-summary.json ffce222f...,
  closure-classes.csv d7ae77dd..., per-root-coverage.csv 8cc804bb...,
  probe-worklist.csv 396c05ae... (3,715,222 bytes, unpublished per
  size policy).
- Measurer: fresh structural adaptation of the eighth-cost k01
  measurer 9c1b79a7... with fresh 12-row expectations, TWO runs
  byte-identical (census json 3ea6491f... x2), all fail-closed gates
  PASS. Tamper battery 5/5 fail-closed + clean control re-PASS
  byte-identical.

## Measured results (BASE 0935c94c -> SCEN 47280073)

- Class census: unknown 34,400 -> 34,393; excluded_now 120 -> 127;
  free_now 39 -> 39 (Board-verified both sides, zero rejections);
  excluded 390 -> 390.
- WIN-side flips MEASURED: exactly 7 classes, the owner-class union
  of the three adopted WIN rows k12 (s5 index 78950), k02 (62804),
  k07 (37372), each unknown -> excluded_now: 735
  (1152921539100807168:0), 1347 (1152921539117580288:0), 1780
  (1153203014077513728:0), 1845 (the ninth-cost serving class
  1297036692683751424:134217728, cost-unknown 99 -> 87, owns all 12
  adopted rows), 16293 (1152921504607895552:32832), 31179
  (1152921505144766464:68719476736), 31563
  (1152921504607895552:67141632).  No other flip direction; no
  free_now change.
- The nine LOSS rows flip nothing: class 1792
  (1297036692716388352:0, a LOSS-row owner class) drops cost-unknown
  100 -> 99 - the closure ladder's single unknown_now churn; rank
  churn 22 (1792: 537 -> 516, 21 band classes shift down by one);
  per-root coverage: exactly one greedy re-route (root 26, 5,229 ->
  5,228); joint greedy 37,398 -> 37,398; probing worklist 64,273 ->
  64,272.
- update8 refresh: all twelve adopted s5 indices sit OUTSIDE the
  frozen baseline requirement, so resolved 282 -> 282, remaining_now
  31,444 -> 31,444, groups_free_now 131 -> 131; win-hit group set
  unchanged (25 groups; none of the seven flipped classes is an
  update8 plan group class).

## Honest disclosures

- Execution preceded kit publication (Part pre-declared in 5e8e8729);
  matches the disclosed eighth-cost k01 reaudit precedent.
- One measurer self-bugfix caught fail-closed BEFORE any PASS run: a
  hand-written |rank delta| == 1 expectation violated by the measured
  class-1792 leapfrog (537 -> 516); replaced with the measured churn
  map and re-run from scratch.
- Single implementation (published refresh byte-clone + this
  measurer); no solver search, no new S5 raws in this Part.

## Meaning and position

The Part consumed no root verdict, freed no class, excluded no class,
and changed no coverage claim: everything above is class-status
bookkeeping inside the scheduling machinery (the EW/EM win-hit
mechanism) driven by the adopted solver-trusted S5 rows.  The
canonical head of record remains
merged-exact-s5-chain-plus-ninthcost12-20261127.cache (47280073...,
6,887 rows WIN 206 / LOSS 6,681).  The standard 11x11 empty board,
all 19 central-reply roots, the two-stone root {60,27}, its remaining
third moves {100,108}, S2 and all closure classes remain UNKNOWN.
Nodes and expansions are bookkeeping, never verdicts.  Next: worklist
regen consumption / tenth-cost selection (fresh selector, BASE =
47280073...).
