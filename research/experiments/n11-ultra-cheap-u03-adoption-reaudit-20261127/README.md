# n11-ultra-cheap-u03-adoption-reaudit-20261127

Kit of the FOLLOW-UP Part declared in this kit's DECLARATION.md
(publish-then-execute, declaration commit 7446f225): the BASE
(82b52577..., the ultra-cheap u02 head of record, 6,892 rows WIN 210 /
LOSS 6,682) vs SCENARIO (c5082866..., the adopted ultra-cheap u03 head
of record, 6,893 rows WIN 211 / LOSS 6,682) class-status census
measurement and the reaudit refresh of the new canonical head.

## Files

- DECLARATION.md - the single-owner declaration, published BEFORE
  execution (commit 7446f225).  sha256
  f5cc66f8bb6873c42805e46280e154d8a3f005a7eaac470542197cc0a2adcba2.
- reaudit/scripts/refresh_adoption_ultra_cheap_u03.py - byte-clone
  of the published ultra-cheap u02 refresh 525a130d... (clone chain
  ultra-cheap u01 refresh d0fa1762... <- eleventh-cost k01 refresh
  0355d7fb... <- tenth-cost k01/k02 refresh 280d7062... <- ninth-cost
  12-row c9a7372a... <- eighth-cost k01 7e11a316... <- SZ wave E
  d8b14697... <- SV fd2e799e... <- ST 02987d1c... <- SQ 60dfb1a1...
  <- SP 82ddb89c... <- sixthwin5 92a884c9... <- EM 7f379b71... <- EV
  f2edac3e... <- EU 6dc24c15...), differing in EXACTLY the three
  regions (docstring, CACHE path, expected cache sha); every
  computation byte is identical (machine-verified before
  publication: line diff = only the two CACHE/SHA config lines).
  sha256 84304650fd365c9c3a58dbc0a0efc85fe2c76056b167eaa4c59fcac60fb8fe2e.
  The declaration commit placed this file at scripts/ (byte-identical
  copy, same sha256; disclosed in the u01/u02 precedent kits and kept
  here).
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted ultra-cheap u03 head (6,893 rows WIN 211 / LOSS
  6,682; census unknown 34,380 / excluded_now 140 / free_now 39 /
  excluded 390).  sha256
  7cd448790d19181b38895766e948b63cad7d3b355920348f60f6dc89c6deab51.
  Three determinism runs byte-identical (fresh cold, ~63-68 s each).
- reaudit/output/closure-classes.csv - refreshed closure ladder (801
  data rows).  sha256
  137cc49bab8e44dcb18611b07e3fdcec9bd63e78345862e9ea207a0936ec63e0 -
  NOT byte-identical to the BASE side: the serving class 16371 LEAVES
  the ladder (802 -> 801 rows, left [16371], entered []), class 16930
  loses one unknown child (unknown_now 52 -> 51, the only unknown_now
  churn) and the ladder re-ranks (797 rank-churn cells).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  4e27453acbf7f463ab92b4b81dba08ba118a7e578f68c09713e14a26cce5b3a2 -
  NOT byte-identical to the BASE side: exactly two rows differ, root
  48's individual greedy union grows 2,893 -> 2,980 and root 26's
  drops 5,228 -> 5,227 (measured greedy re-routes;
  free_now/uncovered identical on all 20 roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (64,266 data rows, 3,714,889 bytes, sha256
  ece167236cb3d6d76c9ab8c5c8a8fa20c324dff11a4368bc50bbe70c65438ef5)
  - UNPUBLISHED per size policy (smaller than the BASE pin
  9fec423a.../3,715,002 bytes: the adopted key's TWO membership rows
  - serving classes 16371 and 16930 - leave the worklist); pinned
  here.
- scripts/measurer_adoption_ultra_cheap_u03.py - the flip-census
  measurer, a disclosed structural adaptation of the published
  ultra-cheap u02 measurer e3df6a73... (all expectations measured
  from the first execution run before publication; includes a
  fail-closed tamper battery 4/4).  sha256
  a86cf188a852bb758a307bb65d00bef8bccf111ab99abfbe8f0bdd804edaa767.
- output/census-deltas-ultra-cheap-u03-adoption.json - the
  measurement record.  sha256
  98208ad97bc3e4d55c9f7e3c0ca23962044f86221f8f7777aafbc32cf66472d7.
  Three determinism runs byte-identical.

## Measured result (win-hit Part EW/EM mechanism)

- The single adopted row (u03 `1153202979851993088:272` WIN(1),
  s5 index 550879, serving class 16371) flips exactly TWO of its
  THREE owner classes from unknown to excluded_now: 16404
  (`1154047404580798464:64`, cost-unknown 98 -> 97) and 16930
  (`1152921504875282432:272`, 52 -> 51).
- The serving class 16371 (`1153202979851993088:16`) was ALREADY
  excluded_now on the BASE head (another of its 52 cost children is
  a known WIN in the u02 head, so the win-hit predates the u03
  adoption); the adopted row resolves its LAST unknown cost child
  (1 -> 0, the class leaves the closure ladder 802 -> 801) without
  changing its census status.
- Census: unknown 34,382 -> 34,380, excluded_now 138 -> 140,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- The closure ladder loses the serving class and re-ranks (797
  cells); one unknown_now churn (16930: 52 -> 51).
- Per-root: two individual greedy re-routes (root 48: 2,893 ->
  2,980; root 26: 5,228 -> 5,227); joint greedy UNCHANGED at 43,830
  (a scheduling quantity, NOT a coverage claim); probing worklist
  64,268 -> 64,266 rows.
- update8: the adopted s5 index 550879 sits OUTSIDE the frozen
  baseline requirement (resolved 284 -> 284, remaining_now 31,332 ->
  31,332, groups_free_now 131 -> 131); the win-hit group set is
  UNCHANGED (35 -> 35, no added or removed groups).

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered the graph-derived THREE-owner union
flip prediction (16371, 16404, 16930 all unknown -> excluded_now,
census unknown 34,382 -> 34,379, excluded_now 138 -> 141).  The
MEASURED flip count is TWO (16404 and 16930 only), because the
serving class 16371 was already excluded_now on the BASE head; the
measured census unknown 34,380 / excluded_now 140 supersedes the
prediction.  The declaration itself provides that "a deviation is
recorded as an experimental fact, not silently adjusted"; the
measured values supersede the prediction everywhere in this kit.

## Honest disclosures

- The declaration commit placed the refresh script at scripts/
  (byte-identical copy of the canonical reaudit/scripts/ placement;
  same sha256 84304650...).
- The BASE-side kit inputs (u02 reaudit reaudit/output trio and
  output census json, and the u02 head cache 82b52577..., plus the
  u03 adoption manifest f09075f0... and increment 0796a210...) were
  byte-fetched from published main and sha-verified before the
  measurement; the local work tree copies are byte-identical.  The
  BASE-side worklist pin 9fec423a.../3,715,002 bytes was additionally
  reproduced by a temporary (unpublished) BASE-variant refresh run
  whose regen output matched the published pin sha byte-for-byte.
- The measurer transform from the u02 measurer was machine-verified
  (unique-count assertions on every replacement); the full assertion
  chain of the u02 measurer was preserved with the u03 measured values
  substituted, then run three times fresh cold from the
  published-byte-verbatim inputs.  One config slip (BASE worklist pin
  left at the u01-side value) was fail-closed by the pin assertion
  before any output was written.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
