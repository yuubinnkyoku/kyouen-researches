# 2026-11-17 n11 class2-lane: receipts-recompute bands (60c/63h/63i/63j/65m/67d/69e/70g) certificates BigInt independent bytes re-verification

## Scope

Head-1452 census v3 (`0c486e53`) closed the certificate-coverage census at
775/775 certified (tier V 250 / tier R 525) and the two follow-up sessions
bytes-re-verified the cost-58c block (34 files, `427e29fa`) and the
warm/multiband bands (82 records, `7693da2a`). This session completes the
next-largest remaining receiptcert-only population: the eight
receipts-recompute bands whose certificate bytes exist in their band
certificate directories, 60c / 63h / 63i / 63j / 65m / 67d / 69e / 70g,
**83 certificates / 83 records in total**.

Record sources (all at main commit `b27c0b5d2efbaa3dc4d471e59ffc27807fe0015e`):

- receipts-recompute per-entry records (rows/md5/sub_roots_pass):
  60c (1), 63h (1), 63i (18), 63j (29), 65m (8), 67d (1);
- `class2-lane-cost69e-win7-certificates-20261114.json` (10 records, md5 +
  sha256; bit 116 documents the hashes of the UNCOMPRESSED certificate,
  published as `base64(gzip-9)` in `bit116-root-...cert.gz.b64`);
- cost-70g: win7 manifest `class2-lane-cost70g-win7-certificates-20261115.json`
  (8 records: strategy_rows / verify.subroots_passed / repo_blob_sha, no md5
  documented) + `class-frontier-cost70g-receipts-recompute-20261116.json`
  (7 records with md5) = 15.

## Method

`reverify_receipts_recompute_bands_certificates_bigint_20261117.py`:

1. mirror all 83 certificate files from commit-pinned raw URLs;
2. assert each file's git blob sha and size against the authoritative
   GitHub directory listing of the pinned commit (83/83, embedded PINS table);
3. assert record md5 where documented (75/75 match; the eight 70g-manifest
   records document no md5, their computed md5 is recorded as a new
   independent datum); 69e bit 116 additionally: base64-decode + gunzip,
   assert uncompressed bytes == 2,670,116, md5 and sha256 vs record;
4. run `verify_win7_certificate_bigint_independent.mjs` (git blob
   `62b5d9413daafb172f6e10249976ee6808f7b454`, local copy byte-exact)
   once per certificate and assert verdict / root stones 7 / root_safe /
   rows sorted-unique / union 0/0 / terminal range within 13..17 /
   strategy_rows == record rows / subroots_passed == record sub_roots_pass /
   root_hex == record root_hex;
5. cross-checks: cost-60c manifest published_cert (whole_bytes/whole_md5/
   whole_sha256/git_blob_sha, sub_roots, terminal_count/range); cost-70g
   manifest loser_first_moves + verify blocks (terminal_range/
   terminal_count/visited_states/loser_reply_edges) for the 8 manifest
   bits; cost-70g receipts-recompute-20261115 rows/sub_roots_pass for the
   same 8 bits; cost-69e 10cert python independent audit totals
   (strategy_rows 411,114 / subroots 535) against per-record verifier sums;
6. deterministic JSON output, two runs byte-identical.

## Result

**83/83 PASS** (single-node ~2 min per run, 4 worker processes):

| band | records | notes |
|------|---------|-------|
| 60c | 1 | bit 92; manifest cross-check reproduced |
| 63h | 1 | bit 89 |
| 63i | 18 | |
| 63j | 29 | |
| 65m | 8 | |
| 67d | 1 | bit 97 |
| 69e | 10 | incl. bit 116 base64(gzip-9) restored + uncompressed-hash exact |
| 70g | 15 | 8 manifest + 7 receipts-recompute-20261116 |

- verifier_fail 0, record md5 mismatch 0, pin blob sha mismatch 0;
- total rows independently verified: **3,143,252**;
- total sub-roots independently verified: **4,327**;
- total certificate bytes rehashed: **113,445,096**;
- all 83 root_hex distinct across bands (asserted);
- rerun byte-identical (published-path script, twice).

## Cross-lane agreement with the cost-60c/69e/70g run (commits 1514699b / c45ad66f)

The same-day parallel lane independently bytes-re-verified 19 of the 83
certificates covered here (60c bit 92; 69e bits 21/76/84/87/89/90/94/99/
108/116; 70g manifest bits 9/20/29/34/62/70/76/119) and published
`class2-lane-cost60c69e70g-certificates-bigint-reverification-20261117.json`
(artifacts commit `1514699b`, log placed at `c45ad66f`).

A machine comparison of the two published JSONs
(`cross_lane_agreement_check_20261117.py`, comparing per pair: git blob
sha, published bytes, md5 (bit 116: uncompressed bytes/md5), expected
rows, root_hex, verifier rows / subroots_passed / root_mobility /
terminal_count / terminal_range / visited_states / loser_reply_edges /
union_missing / union_extra, verifier_status):

- pairs compared: **19/19**, field comparisons **284**, mismatches **0**,
  all_agree **true**.

The two independently produced runs therefore agree on every overlapping
certificate. The remaining 64 records of this run (63h/63i/63j/65m/67d,
70g receipts-recompute-20261116 7) are outside the parallel coverage and
are new evidence from this run alone.

Process fact worth recording: an initial hand-transcribed copy of the
parallel JSON produced an apparent single-hex-digit md5 mismatch on 69e
bit 94; a byte-exact raw fetch of the pinned commit showed the mismatch
was a typo introduced by the hand transcription itself. Both lanes, the
69e manifest and the actual certificate bytes all record
`4dc6076b96edc3a472b4b23f38739451`. Hex values must always be
machine-copied (or regenerated with `f"{x:032x}"`), never hand-retyped.

## Position

- This upgrades the 83 certificates of these eight bands from receiptcert
  (tier R) documentation to bytes-level independently re-verified evidence,
  on top of the earlier 33 (58c) + 82 (warm/multiband) = 115 records. The
  remaining tier-R bytes-re-verification candidates are the other
  receipts-recompute groups without a dedicated band certificate directory
  (e.g. 63f/63g/67c/69f/69h/69i/70e/70f/71c/72b/72c/73g/73h/74d/74g/75d/76a/76b/77a-d/78a/79a/80d/82c/83a-d/84a),
  where the census v3 documentation is receiptcert/manifest-level only.
- **solved 1452 is manifest cover bookkeeping of the head-1452 frontier. A
  WIN7-D10 certificate proves only that its individual 7-stone root is a
  first-player win within depth 10. REFUTED-D10 entries are not LOSS proofs.
  11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 1, class 2
  and class 4 all remain UNKNOWN.**

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_receipts_recompute_bands_certificates_bigint_20261117.py`
- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-receipts-recompute-bands-certificates-bigint-independent-reverification-20261117.json`
- cross-lane agreement script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cross_lane_agreement_check_20261117.py`
- cross-lane agreement output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cross-lane-agreement-cost60c69e70g-20261117.json`
- this log
