# 2026-11-17 n11 class2-lane: cost78c WIN7 certificates BigInt third-implementation independent bytes re-verification (11/11 PASS, manifest cross-agreement)

## Scope

The parallel certificate-extraction lane has published all 11 WIN7-D10
certificates of the cost-78c band (child `00000000000000403800000008000008`,
s6_s7_edge_cost 78, census v11 rank-1 row; sweep: 11 WIN7-D10 / 67 REFUTED-D10
/ 0 capped) as per-bit commits `b359756fef` (bit 69, extraction pipeline start)
through `97650e276e` (bit 116 part 3of3), then landed the in-band manifest
`class2-lane-cost78c-win7-certificates-20261117.json` (git blob
`b7fe519e923c6170e836f71e3f084f73219319d5`) plus `stats.json` (blob
`70813ca75d3216d1836e408183c5d0db883e6cbc`) and `det-reextraction.json`
(blob `07e150ede079deb7d70a734d41ea5d1a49b00fea`) with claim v4
(`3ed406e339ef82e8fdb7aadcb2e8da0ddd26189a`), and the current-main claim v5
(`1687397338a89a489263c12f41780e1182f18b9c`, git blob
`1850832186ba9c8715624094f05d67aa4eb10f0b`, a provenance-only correction
over v4 whose certificates block is byte-identical). The claim v4/v5
next_action names as optional follow-up the "BigInt independent
third-implementation re-verification of the 11 certificates"; this session
implemented exactly that follow-up (the 73j 16/16, 73k 22/22, 73l 32/32
pattern) and publishes the batch here: 11/11 PASS.

No new sweep, no new verdict, no certificate bytes changed, no manifest row
closed. The 11x11 empty board, the two-stone roots {49,60} and {59,60},
S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN.

## What was done

1. **Mirror with GitHub-listing pins.** All 59 band files (56 certificate
   band files + manifest + stats.json + det-reextraction.json) were mirrored
   from the commit-pinned raw CDN and each file asserted against the GitHub
   API contents listing of the band dir at the pin commit
   `1687397338a89a489263c12f41780e1182f18b9c` (name|git blob sha|size)
   embedded verbatim as `PINS_TABLE` in the script: 59/59 byte-exact (the
   listing is identical at `eb157af2be0f35f58446ab1f5923c1c712dc1043` where
   stats/det landed). The sweep claim v5 is the 60th pin and the superseded
   claim v4 (blob `5cd0591a0676494965a02460dff7246c1d3aa885`) the 61st. The
   BigInt verifier (`verify_win7_certificate_bigint_independent.mjs`, git
   blob `62b5d9413daafb172f6e10249976ee6808f7b454`) and the nine earlier
   BigInt batch outputs used for disjointness (blobs `ceb79e97`,
   `5b916672`, `91e9f539`, `c24224ea`, `0978ed78`, `1fa6d465`, `34dd4504`,
   `6a07426a`, `547fe617`) are all blob-pinned inline and were re-fetched and
   asserted.

2. **Manifest + claim structural cross-agreement.** The manifest (schema
   `n11-class2-lane-cost78c-win7-certificates-20261117-v1`, basis pinned to
   the sweep claim v3 blob `d3105b3a6c6cac68c35d84f2ebca8b10e7b72228`) was
   asserted: 11 records in bit order [1,4,9,30,49,69,75,79,100,114,116],
   every record verdict WIN7 / depth 10 / fbt_drops 0 / fatal null /
   subroots == subroots_pass == loser_mobility / union 0/0 / terminal stone
   range [13,17], every root == child | (1 << bit), and the totals
   (11 certificates / 614,003 rows / 77,967,826 extraction nodes /
   22,223,603 published bytes / 0 fbt_drops_total / 0 capped_per_move_total)
   equal to the per-record sums. The claim v5 was asserted: schema v5,
   win7_d10_bits == the 11 bits, certificate_extraction and
   certificate_verification COMPLETE, certificates.status complete,
   certificates.manifest_blob_sha == the manifest blob,
   certificates.totals == the manifest totals, determinism_sample_bits
   [69,116], and the next_action optional follow-up sentence present; the
   pinned claim v4 blob's certificates block is asserted identical to v5's.

3. **Third-implementation verification per certificate.** For each of the
   11 certificates: the parts' git blob shas and sizes were asserted, the
   parts recombined as exact concatenations (bit 116 is the three-part
   split: part1of3/part2of3/part3of3 with boundaries 946728 and 1893416 per
   its README; the other ten are two-part splits), the joined md5 asserted
   against the README-split md5 AND the manifest record md5, the joined
   sha256 against the manifest record sha256, the 2-line header and the
   data-row count against the rootcheck rows AND the manifest rows AND the
   stats rows, and then the BigInt verifier (BigInt 3x3 cofactor expansion
   of the exact lifted determinant [x^2+y^2,x,y,1], no floating point,
   third implementation beyond the extractor's own Bareiss
   verify_bit7_win7_cert.ts) was run once per certificate with the rootcheck
   loserMobility as the expected mobility. The independently computed D4
   canon of each root was asserted equal to the manifest d4_canon_root and
   raw_is_canon fields (bits 75/79/100/114/116 are non-canonical roots).

4. **stats.json + det-reextraction.json cross-agreement.** Per bit the
   stats record (root/rows/nodes/moves/md5/sha256/size/fbt_drops) agrees
   with the manifest record and the bytes recomputed here, including
   nodes == manifest extraction_nodes and size == joined bytes. The
   det-reextraction record's published fresh-process determinism md5s
   (bit 69 `33e4bcac5cdc270becf2db0b44c8cfc1`, bit 116
   `7a0694f61e0bcf6ded606161c1e0a907`) equal the joined md5s recomputed
   here from the pinned certificate bytes.

5. **Sidecar aggregate cross-agreement.** For all 11 certificates the
   subroots.jsonl per-loser-first-move stats (Bareiss-generated) sum exactly
   to the BigInt verifier output: sum(seen) == visited_states_across_subroots,
   sum(terminals) == terminal_count, sum(opponentEdges) == loser_reply_edges,
   m-key count == subroots_passed == loser_mobility == manifest
   loser_mobility == stats moves, and every per-move stone range lies within
   [13,17]. rootcheck stones == 7 and loserMobility == verifier root_mobility
   on all 11.

## Results (11/11 PASS, deterministic)

- verifier 11/11 PASS, verifier_fail 0, union_missing 0 / union_extra 0 on
  all 11, rows sorted-unique on all 11, terminal range [13,17] on all 11.
- manifest cross-agreement 11/11, stats cross-agreement 11/11,
  det-reextraction cross-agreement True, claim v4/v5 certificates block
  identical.
- rows per bit (rootcheck == verifier == manifest == stats):
  bit1 65,094; bit4 65,807; bit9 71,021; bit30 48,923; bit49 43,147;
  bit69 34,293; bit75 36,342; bit79 48,729; bit100 54,460; bit114 67,593;
  bit116 78,594. Total 614,003 rows, equal to the manifest totals.rows and
  the claim v5 certificates.totals.rows.
- total sub-roots independently re-verified 653; total certificate bytes
  rehashed 22,223,603 (== manifest published_bytes); total extraction
  nodes agreed with the manifest 77,967,826; per-bit loser mobility
  {1:60, 4:58, 9:64, 30:54, 49:57, 69:53, 75:52, 79:63, 100:60, 114:66,
  116:66}. Every per-bit row count equals the count stated in the
  corresponding per-bit publication commit message.
- **Cross-batch disjointness**: the 11 root_hex are distinct in-batch, each
  root == child | (1 << bit), and disjoint (root and independently computed
  D4 canon) from the 183 earlier BigInt-verified records (single-file 43 +
  split-part bands 18 + split-part sweepbands 24 + 66j/69j 15 + 63cd 2 +
  72d 11 + 73j 16 + 73k 22 + 73l 32). The 11 D4 canons are also disjoint
  from the claim's 12 confirmation root canons (the claim's
  winner_canons_distinct_from_confirmation_canons statement re-derived
  independently).
- **Bytes-re-verified population**: 381 + 11 = 392 records (72d/73k batch
  bookkeeping).
- Determinism: two consecutive runs produced byte-identical output
  (md5 `0f4301b2d5b227b470a1c5b707e1bb39`); the script has no timestamps or
  wall-clock fields.

## Interpretation guard

- A WIN7-D10 certificate proves only that its individual 7-stone root is a
  first-player win within depth 10. The 67 REFUTED-D10 bits of the sweep are
  NOT LOSS proofs of those roots.
- The cost-78c receipt fold stays pending behind the 66i/66j/69j/71e/72d/
  73i/73j/73k/73l folds managed by their own lanes; no manifest row is
  closed by this re-verification.
- 11x11 empty board: UNKNOWN. Two-stone roots {49,60} and {59,60}: UNKNOWN.
  S2 {59,60}: UNKNOWN. Classes 1, 2 and 4: UNKNOWN.

## Resume

- The claim v4/v5 next_action optional follow-up (BigInt third-implementation
  re-verification of the 11 certificates) is now done and published as this
  batch; the output JSON pins the manifest/stats/det/claim blobs it agreed
  with, so any later in-band file republication can be diffed against it.
- 73i certificates remain unpublished on main as of this session's checks;
  the 73i BigInt reverification stays prohibited until that publication.
- The cost-78c receipt fold remains queued behind the pending folds. The
  presweep census v12 has since landed (commit
  `56d81b077362e71a2cb0ec232470b25c4fd06ca9`: the 78c row is swept as the
  15th verdict map with the 11 published WIN7-D10 certificates, receipt fold
  pending); the next target per the claim v5 next_action is the census v11
  runner-up (cost 79, open 69).
