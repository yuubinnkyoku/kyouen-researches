# 2026-11-17 n11 class2-lane: cost73j sweep + certificates complete — census v6 rank-1 row swept (16 WIN7-D10 + 57 REFUTED-D10) and all sixteen WIN7 certificates extracted, independently verified and published

## Summary

The cost-73 row `00000000000000403800000408000000` (stones [27, 34, 59, 60,
61, 70], demand c2=2, legal 73), selected as rank-1 of the head-1472
presweep census v6 (git blob `c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb`)
after the completed 71e/72d/73i sweeps, was fully swept and certified in one
lane pass:

* sweep: fresh v17 depth-10 sweep of all 73 bits (66 open + 7 confirmation),
  168,445,380 candidate nodes, 9 batches, 9/9 pilot controls exact
  (loss=false at exactly 3,402 nodes), 0 capped
* verdicts: 16 WIN7-D10 bits [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91,
  98, 100, 110, 118] + 57 REFUTED-D10
* confirmation transfers: all 7 predicted REFUTED-D10 transfers re-run fresh
  and confirmed (bit 5 = cost69j bit 34, bit 14 = cost72d bit 34, bit 20 =
  cost64h bit 34, bit 46 = cost73i bit 34, bit 97 = cost71e bit 106, bit 103
  = cost66i bit 14, bit 108 = cost66j bit 106); bits 5/14/20/46 turned out
  raw-identical to their transfer sources (identical node counts), bits
  97/103/108 canon-equal only; every source raw file was pin-verified
  against its published audit JSON or the pinned census v4 script
* determinism: batch 1 (WIN bits 0, 1, 6 and the heaviest search bit 3,
  11,476,946 nodes) and batch 6 (heaviest WIN bit 98, 8,801,472 nodes)
  re-run in separate processes, field-identical on every non-ms field
* cross-engine: independent v15 runner (blob
  `8744fc65b6b7cac6bd561403ce4c749e01c51359`) re-checked all 16 WIN bits,
  16/16 loss=true, pilot 5,949 exact, 0 capped
* raw audit: stdlib `audit_cost73j_raw_batches_20261117.py` all checks
  passed (internal canon collisions 0, transfer canons 7/7, no
  WIN/REFUTED canon overlap within the child, source pins 7/7)
* certificates: all 16 WIN7-D10 roots blindly extracted
  (`class4_child1_cert_extractor_exact.ts` via the archived
  `cert_driver73j.ts`, empty kill table), 726,778 rows total, 166,238,087
  extraction nodes, 26,236,851 published bytes, fbt_drops=0 on all sixteen,
  no fatal, no capped per-move; independently verified engine-free with
  `verify_bit7_win7_cert.ts` (Bareiss 4x4): root-check stones=7 on every
  root, loser mobility equals the independent legal_candidates.py
  enumeration on the RAW root (48-62 per root), all sub-roots PASS,
  terminal stone range within [13,17], consumed-winner-state union vs the
  certificate row set 0 missing / 0 extra on every root (re-verified from
  the saved certkeys/consumed artifacts when building the manifest)
* determinism of extraction: fresh-process re-extraction of the heaviest
  WIN bit 98 (64,451 rows) byte-identical (md5
  `0d8124b781d6d98878125abdb1a7ce76`)
* publication: bits 69/82 published whole (within the 1,200,000-byte
  whole-file threshold), the other fourteen split at line boundaries into
  part1of2/part2of2 with README-split per bit; all 30 certificate files
  landed byte-exact on main (reassembled split md5s match the manifest);
  manifest `class2-lane-cost73j-win7-certificates-20261117.json` (git blob
  `e88710b5a2d4848be77a03ae5104e46aefc1279a`)
* newness: the census v6 recorded this row as open 73 with 0 harvested
  (not one of the 16 bit-table children), so none of the 16 WIN root
  canons can appear in the published tree before this sweep; the raw
  audit additionally found no WIN/REFUTED canon overlap within the child

## Execution notes

* one mid-run execution-environment reset destroyed a `for b in 1 0 6`
  extraction triple before any of its outputs were written; the affected
  bit-1 partial artifacts were removed and bits 1/0/6 were re-run
  individually from scratch (the completed certificates are from the
  clean re-runs only)
* all push transports of large certificate parts succeeded despite
  run_typescript MemoryLimitError reports at the two-file boundary; every
  landing was confirmed by directory listing with exact byte sizes and a
  final raw-CDN pinned byte-exact fetch of all 30 files with reassembled
  md5 comparison
* the raw-identical transfer discovery (4/7 confirmation bits raw-equal to
  their sources, 3/7 canon-equal only) is recorded per transfer in the
  raw sweep audit; raw-equality gives identical engine node counts,
  canon-equality only preserves the verdict

## Interpretation guard

WIN7-D10 certificates prove a first-player win within depth 10 from the
individual 7-stone roots of this child only. REFUTED-D10 is NOT a LOSS
proof. No manifest row is closed by this sweep or these certificates. The
receipt fold of this row stays pending behind the 76c/66i/66j/69j/71e/72d/73i
folds (managed by their own lanes). The 11x11 empty board remains UNKNOWN;
the two-stone roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4
remain UNKNOWN.
