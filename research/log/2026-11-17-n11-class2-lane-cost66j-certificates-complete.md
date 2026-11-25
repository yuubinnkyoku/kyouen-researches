# 2026-11-17 n11 class2-lane: cost66j certificates complete — all nine WIN7-D10 roots extracted, independently verified and published

## Summary

Following the cost66j sweep (9 WIN7-D10 bits [7, 9, 30, 66, 78, 79, 92,
96, 114] + 57 REFUTED-D10, 0 capped, commit `020603f8`), all nine WIN7
certificates were extracted and verified:

* extraction: blind extraction with `class4_child1_cert_extractor_exact.ts`
  via the archived `cert_driver66j.ts` (empty kill table), fbt_drops=0 on
  all nine, no fatal, no capped per-move, extraction order
  [79, 78, 114, 92, 9, 7, 66, 96, 30] (heaviest-first scheduling)
* total certificate rows 372,824; total extraction nodes 96,962,144
* independent verification with `verify_bit7_win7_cert.ts` (engine-free,
  Bareiss 4x4): root-check stones=7 on every root, loserMobility equals
  the independent legal_candidates.py enumeration on the RAW root
  (53/60/46/56/53/51/56/50/59), all sub-roots PASS (subroots_pass ==
  loser mobility on every root), terminal stone range [13,17] everywhere,
  consumed-winner-state union vs the certificate row set 0 missing /
  0 extra in both directions on every root
* determinism: fresh-process re-extraction byte-identical (md5) on all
  nine roots
* newness: none of the nine roots (raw or D4-canon form) appears anywhere
  in the published tree before this push, and no canon is in the landed
  cost-64h fold receipts (asserted by the raw audit)

Coordinate convention carried over from the 66i lesson: loser defenses and
the certificate root use the RAW child|bit position. For bits
7/9/30/66/78/79/92 raw==canon; for bits 96 and 114 the raw root is a
non-canonical D4 image (d4_canon_root recorded per entry) and the defense
list is enumerated on the raw root; the verifier's root-header check
guards this.

## Interpretation guard

WIN7-D10 certificates prove a first-player win within depth 10 from the
individual 7-stone roots only. No manifest row is closed by publication.
The receipt fold of this row waits behind the pending cost-76c fold
(parallel lane, bit 61 certificate in flight) and the cost-66i receipt
fold.

**The 11x11 empty board remains UNKNOWN. The two-stone roots {49,60}
and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.**

## Files pushed

* `output/class2-lane-cost66j-certificates/` — nine certificates
  (bits 7/30/96 whole files; bits 9/66/78/79/92/114 split
  part1of2/part2of2 + README-split-bit{b}.md), per-bit
  `bit{b}-rootcheck.json` and `bit{b}-subroots.json` verification records
* `output/class2-lane-cost66j-win7-certificates-20261117.json` (record,
  v1 schema, nine entries with md5/sha256/rows/extraction_nodes)
* `output/class2-lane-cost66j-inflight-20261117.json` (claim v3,
  certificates-complete)
* `scripts/cert_driver66j.ts` (archived driver)
