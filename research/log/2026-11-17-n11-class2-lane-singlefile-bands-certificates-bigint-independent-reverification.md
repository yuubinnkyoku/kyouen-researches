# 2026-11-17 n11 class2-lane: single-file bands (63g/72b/74d/77c/77d) certificates BigInt independent bytes re-verification

## Scope

The remaining-band certificate bytes survey
(`class2-lane-remaining-band-certificate-bytes-survey-20261117.json`,
log `2d0ea164`) identified 117 published certificates across 31 remaining
bands and proposed the next bytes-re-verification batch: the single-file
population of five bands, **63g (14) + 74d (8) + 77c (7) + 77d (7) + 72b (7)
= 43 certificates / 57,797,100 bytes**. This session executed exactly that
batch. On top of the earlier 33 (cost-58c, `427e29fa`) + 82
(warm/multiband, `7693da2a`) + 83 (receipts-recompute bands, `aded350b`)
records, this brings the bytes-level independently re-verified population
to 241 records.

## Method

`reverify_singlefile_bands_certificates_bigint_20261117.py`
(record sources all at main commit `063031b67a74f568f3207e2934715e405d00afd8`):

1. mirror all 43 certificate files from commit-pinned raw URLs and assert
   each file's git blob sha and size against the authoritative GitHub
   directory listing of the pinned commit (43/43 PINS table embedded);
2. assert the verifier's own git blob sha
   (`62b5d9413daafb172f6e10249976ee6808f7b454`);
3. assert record md5 for every record (43/43 documented an md5; the 74d
   records additionally document sha256, both asserted);
4. run `verify_win7_certificate_bigint_independent.mjs` once per
   certificate and assert verdict / root stones 7 / root_safe / rows
   sorted-unique / union 0/0 / terminal range within 13..17 /
   strategy_rows == record rows / subroots_passed == record sub_roots_pass /
   root_hex == record root_hex;
5. cross-checks against the band documentation:
   - cost-63g win7 manifest (certificates keyed by bit): md5/sha256/bytes/
     whole_git_blob_sha/sub_roots_total/root_check.loser_mobility/
     terminal_range per bit; verifier sums == manifest and receipts totals
     (rows 419,398 / sub_roots 667 / bytes 15,142,573);
   - cost-72b win7 manifest: full per-bit field agreement for the 7
     single-file bits (incl. winner/loser/terminal/edges/visited) plus the
     13-record manifest totals re-summed (rows 636,225 / sub_roots 729 /
     visited 1,378,650 / terminal 224,802 / edges 1,241,817 / extraction
     nodes 200,029,509);
   - cost-74d win7 manifest: full per-bit field agreement for the 8
     single-file bits plus receipts-recompute root_hex and
     opponent_legal_replies agreement; 15-record manifest totals re-summed
     (rows 723,630 / sub_roots 883); **bit 91 is a documented D4 duplicate
     of cost72b bit 85** (its own-coordinate md5 refers to the bit-91
     extraction, not to the 72b file bytes; the backing certificate blob
     sha asserted to be the verified 72b bit85 pin, and the D4-duplicate
     claim machine-checked via the independent canonicalizer);
   - **independent D4 canonicalization check (new in this session)**: a
     third, in-script implementation (min hex over the eight square
     symmetries of the 11x11 board) reproduces every record's
     `d4_canonical_hex` for all 43 certificates, and
     canon(74d bit91 root) == canon(72b bit85 root);
6. deterministic JSON output, two runs byte-identical.

## Result

**43/43 PASS** (single-node ~64 s per run, 4 worker processes):

| band | records | notes |
|------|---------|-------|
| 63g | 14 | all 14 WIN bits of the band are single-file; manifest+receipts totals reproduced |
| 72b | 7 | single-file bits 11/30/31/36/47/85/97 of 13 (6 split-part bits deferred) |
| 74d | 8 | single-file bits 12/66/68/69/80/92/100/118 of 15 (6 split-part bits and the bit 91 D4 duplicate handled separately) |
| 77c | 7 | single-file bits 40/50/54/58/95/96/111 of 8 (bit 10 split) |
| 77d | 7 | single-file bits 7/12/39/62/64/94/96 of 12 (5 split-part bits deferred) |

- verifier_fail 0, record md5 mismatch 0, pin blob sha mismatch 0;
- total rows independently verified: **1,601,179**;
- total sub-roots independently verified: **2,272**;
- total certificate bytes rehashed: **57,797,100**;
- all 43 root_hex distinct across bands (asserted);
- rerun byte-identical (twice).

Process fact worth recording: two certificate file names (72b bit97 and
several 77d bits) were initially hand-retyped into the pin table with wrong
root hexes; the pin-vs-mirror assertion caught them (404 fetches / sha
mismatch) and they were corrected from the authoritative listing. File
names and hex values must always be machine-copied.

## Position

- This upgrades the 43 single-file certificates of the five bands from
  receipt-cert/manifest documentation to bytes-level independently
  re-verified evidence. The bytes-re-verified population now stands at
  241 records (33 + 82 + 83 + 43). It does not change any frontier number;
  the head-1472 frontier bookkeeping is untouched.
- The remaining bytes-re-verification candidates are the 24 split-part
  certificates of bands 72c/73g/73h/83d plus the 20 split-part bits of
  these five bands (deferred to a split-part batch with per-part blob sha
  pins and defined concatenation semantics), the newly published 66j/69j/
  71e certificate bands, and the 63c/63d extractor regeneration.
- **solved 1452 (and the landed 64h fold projection 1472) are manifest
  cover bookkeeping. A WIN7-D10 certificate proves only that its
  individual 7-stone root is a first-player win within depth 10.
  REFUTED-D10 entries are not LOSS proofs. 11x11 empty board, two-stone
  root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain
  UNKNOWN.**

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_singlefile_bands_certificates_bigint_20261117.py`
- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117.json`
- this log
