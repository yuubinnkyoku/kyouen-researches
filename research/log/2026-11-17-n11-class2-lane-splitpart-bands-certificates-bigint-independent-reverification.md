# 2026-11-17 n11 class2-lane: split-part bands (72b/74d/77c/77d) certificates BigInt independent bytes re-verification

## Scope

The single-file bands session (log `375c98af`, 43 records) deferred the
split-part half of the five-band certificate bytes re-verification to a
dedicated batch with per-part blob sha pins and defined concatenation
semantics. This session executed exactly that batch: **72b (6) + 74d (6) +
77c (1) + 77d (5) = 18 certificates / 36 part files / 39,054,407 bytes**
(the 74d bit 91 D4 duplicate has no own bytes and was already handled in
the single-file batch). On top of the earlier 33 (cost-58c, `427e29fa`) +
82 (warm/multiband, `7693da2a`) + 83 (receipts-recompute bands,
`aded350b`) + 43 (single-file bands, `375c98af`) records, this brings the
bytes-level independently re-verified population to **259 records**, and
it completes the five bands 63g/72b/74d/77c/77d end to end (61 records).

## Method

`reverify_splitpart_bands_certificates_bigint_20261117.py`
(record sources all at main commit `063031b67a74f568f3207e2934715e405d00afd8`):

1. mirror all 36 part files from commit-pinned raw URLs and assert each
   part's git blob sha and size against the authoritative GitHub
   directory listing of the pinned commit (36/36 PINS table embedded; the
   table was machine-extracted from the listing, see incident below);
2. assert the verifier's own git blob sha
   (`62b5d9413daafb172f6e10249976ee6808f7b454`);
3. per-part manifest agreement for 72b/74d: bytes/md5/git_blob_sha (plus
   line counts for 72b) against the `storage.parts` metadata;
   part1 asserted to end on a line boundary (`\n`);
4. reconstruct each certificate as the exact part1+part2 concatenation and
   assert the joined md5 against the record (72b: manifest cross-agreed
   with receipts; 74d: manifest, the receipts record only root_hex for
   these bits; 77c/77d: receipts); for 72b/74d additionally joined
   bytes/sha256/whole_git_blob_sha against the manifest
   (`joined_md5_equals_whole_md5` documented true for all 12);
5. run `verify_win7_certificate_bigint_independent.mjs` once per joined
   certificate and assert verdict / root stones 7 / root_safe / rows
   sorted-unique / union 0/0 / terminal range within 13..17 /
   strategy_rows == record rows / subroots_passed == record sub_roots_pass /
   root_hex == record root_hex;
6. cross-checks:
   - full per-bit manifest field agreement for the 12 72b/74d bits
     (terminal_count/range, winner/loser states, loser_reply_edges,
     visited_states, root_check.loser_mobility vs the verifier output);
   - the 13-record 72b and 15-record 74d manifest totals re-summed and
     asserted (rows 636,225 / 723,630; sub_roots 729 / 883);
   - **independent D4 canonicalization check**: a fourth, in-script
     implementation (min hex over the eight square symmetries of the
     11x11 board) reproduces every record's `d4_canonical_hex` for all
     18 certificates (72b receipts, 74d manifest, 77c/77d receipts);
   - the joined sha256 and git blob sha of the 6 77c/77d certificates
     are recorded in the output as new bytes-level documentation (the
     receipts only document md5/rows/sub_roots_pass);
7. deterministic JSON output, two runs byte-identical.

## Result

**18/18 PASS** (single-node ~43 s per run, 4 worker processes):

| band | records | bits | notes |
|------|---------|------|-------|
| 72b | 6 | 2/21/66/95/100/106 | manifest per-part metadata + receipts cross-agreement; band now fully bytes-verified (13/13 records) |
| 74d | 6 | 2/28/102/109/112/116 | manifest per-part metadata; band now fully handled (8 single + 6 split + bit 91 duplicate) |
| 77c | 1 | 10 | band now fully bytes-verified (8/8 records) |
| 77d | 5 | 58/66/78/108/111 | band now fully bytes-verified (12/12 records) |

- verifier_fail 0, record md5 mismatch 0, pin blob sha mismatch 0, part
  line boundary violation 0;
- total rows independently verified: **1,082,147**;
- total sub-roots independently verified: **1,112**;
- total certificate bytes rehashed: **39,054,407** (sum of the 36 parts);
- all 18 root_hex distinct across bands and disjoint from the 43
  single-file batch roots (asserted);
- rerun byte-identical (twice).

Batch cross-consistency (new in this session): the split-part and
single-file batch row sums reproduce the band manifest totals exactly:
72b 280,757 + 355,468 = 636,225 rows and 729 sub-roots (13/13 records);
74d 328,337 + 355,343 + 39,950 (bit 91 own-extraction rows, no own bytes)
= 723,630 rows. Five-band combined bytes-verified population: **61
records / 2,683,326 rows / 3,384 sub-roots / 96,851,507 bytes**.

Incident worth recording: during mirror setup two pin lines were
hand-retyped with a single wrong hex digit each (74d bit2 part2 and 77d
bit108 part2). The pin-vs-mirror assertions caught both, but the initial
suspicion fell on the repository data (possible truncation repair).
Investigation resolved both as pure transcription errors: each file has
exactly one publication commit (no later repair), the 77d bit108 part2
listing value machine-re-fetched from the publication commit matches the
mirrored bytes exactly, and the 74d bit2 part2 manifest `storage.parts`
git_blob_sha matches the mirrored bytes exactly. **No data difference
exists anywhere in the 36 parts.** Hex values must always be
machine-copied; this batch's PINS table was generated by machine
extraction from the listing, not by hand.

## Position

- This upgrades the 18 split-part certificates of the five bands from
  receipt/manifest documentation to bytes-level independently re-verified
  evidence, completing the five-band certificate bytes re-verification
  begun in the single-file session. The bytes-re-verified population now
  stands at 259 records (33 + 82 + 83 + 43 + 18). It does not change any
  frontier number; the head-1472 frontier bookkeeping is untouched.
- The remaining bytes-re-verification candidates are the 24 split-part
  certificates of bands 72c/73g/73h/83d (83d has no README; per-part
  record sources must be identified first), the newly published 66j/69j/
  71e certificate bands, and the 63c/63d extractor regeneration.
- **solved 1452 (and the landed 64h fold projection 1472) are manifest
  cover bookkeeping. A WIN7-D10 certificate proves only that its
  individual 7-stone root is a first-player win within depth 10.
  REFUTED-D10 entries are not LOSS proofs. 11x11 empty board, two-stone
  root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain
  UNKNOWN.**

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_splitpart_bands_certificates_bigint_20261117.py`
- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117.json`
- this log
