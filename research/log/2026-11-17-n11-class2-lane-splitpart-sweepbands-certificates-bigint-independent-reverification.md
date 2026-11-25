# 2026-11-17 n11 class2-lane: split-part sweep bands (72c/73g/73h/83d) certificates BigInt independent bytes re-verification

## Scope

The five-band split-part session (log `8859cd17`, 18 records) left, per the
remaining-band certificate bytes survey, the four sweep bands that store
**all** their certificates as split parts: **72c (9) + 73g (8) + 73h (4) +
83d (3) = 24 certificates / 48 part files / 38,211,650 bytes**. This
session executed exactly that batch. On top of the earlier 33 (cost-58c,
`427e29fa`) + 82 (warm/multiband, `7693da2a`) + 83 (receipts-recompute
bands, `aded350b`) + 43 (single-file bands, `375c98af`) + 18 (five-band
split-part, `8859cd17`) records, this brings the bytes-level independently
re-verified population to **283 records**, and it **exhausts the 85
survey-identified remaining-band certificate records** of this experiment
(43 single-file + 18 five-band split + 24 sweep split).

Record source nuance: 72c/73g/73h have win7-certificates manifests
(per-bit md5/bytes/strategy_rows, per-part blob shas/md5s/bytes, full
`verify.bigint` field set, `join_md5_equals_whole`, joined
`repo_blob_sha`) cross-agreed with their receipts-recompute files; the 73h
receipts document md5 null for all 4 bits, so the manifest md5 is the
whole-file documentation for 73h. **83d has no README and no manifest**;
its records rest on the receipts-recompute file (md5/rows/sub_roots_pass/
root_hex/d4_canonical_hex), and the per-part pins rest on the authoritative
GitHub directory listing of the pinned commit.

## Method

`reverify_splitpart_sweepbands_certificates_bigint_20261117.py`
(record sources all at main commit `8859cd17b174dbb50a5d8233ddd5a30f3dd0e24d`;
the mirror's receipts files carry a local `rec-` name prefix, verified
byte-identical to the repo paths by cmp):

1. mirror all 48 part files from commit-pinned raw URLs and assert each
   part's git blob sha and size against the authoritative GitHub
   directory listing of the pinned commit (48/48 PINS table embedded,
   machine-extracted; asserted again 42/42 against the manifest
   `part_blob_shas`/`part_md5s`/`part_bytes` for 72c/73g/73h,
   machine-parsed, guarding the pin transcription);
2. assert the verifier's own git blob sha
   (`62b5d9413daafb172f6e10249976ee6808f7b454`);
3. reconstruct each certificate as the exact part1+part2 concatenation
   (part1 asserted to end on a line boundary) and assert the joined md5
   against the record; for 72c/73g/73h additionally joined bytes, and the
   manifest `repo_blob_sha` against the recomputed joined git blob sha
   (new cross-check for this batch);
4. run `verify_win7_certificate_bigint_independent.mjs` once per joined
   certificate and assert verdict / root stones 7 / root_safe / rows
   sorted-unique / union 0/0 / terminal range within 13..17 /
   strategy_rows == record rows / subroots_passed == record sub_roots_pass
   / root_hex == record root_hex;
5. cross-checks:
   - full `verify.bigint` field agreement for the 21 manifest records
     (root_mobility/subroots_passed/terminal_range/terminal_count/
     visited_states_across_subroots/loser_reply_edges), plus manifest
     `loser_first_moves` == verifier `root_mobility`;
   - receipts totals (rows/bytes/sub_roots per band) and, for 72c/73g/73h,
     manifest totals (`strategy_rows`/`bytes`/`bytes_parts`) equal to the
     verifier sums per band;
   - **independent D4 canonicalization check**: a fifth, in-script
     implementation (min hex over the eight square symmetries of the
     11x11 board) reproduces every record's `d4_canonical_hex` for all
     24 certificates;
   - all 24 root_hex distinct in-batch and disjoint from the 61 root_hex
     values of the two earlier band batches (asserted against the two
     published batch outputs at load time);
   - joined sha256 and git blob sha recorded for all 24 as new bytes-level
     documentation; for 83d the whole-file bytes/sha256/blob-sha
     documentation beyond the receipts md5 is new here (83d has no
     README/manifest);
6. deterministic JSON output, two runs byte-identical.

## Result

**24/24 PASS** (single-node ~70 s per run, 4 worker threads):

| band | records | bits | notes |
|------|---------|------|-------|
| 72c | 9 | 1/7/24/39/59/64/67/72/96 | manifest per-part metadata + receipts cross-agreement |
| 73g | 8 | 31/54/56/62/69/81/89/113 | manifest per-part metadata + receipts cross-agreement |
| 73h | 4 | 45/48/82/96 | receipts md5 null; manifest md5 is the whole-file documentation |
| 83d | 3 | 16/51/82 | receipts only (no README/manifest); per-part pins rest on the listing |

- verifier_fail 0, record md5 mismatch 0, pin blob sha mismatch 0, part
  line boundary violation 0;
- total rows independently verified: **1,057,962**
  (72c 321,781 + 73g 343,092 + 73h 176,451 + 83d 216,638);
- total sub-roots independently verified: **1,346** (474 + 450 + 234 + 188);
- total certificate bytes rehashed: **38,211,650** (sum of the 48 parts);
- rerun byte-identical (twice).

Combined with the two earlier band batches (43 + 18 records), the seven
band batches cover 85 records / 3,741,288 rows / 4,730 sub-roots /
135,063,157 bytes; the overall bytes-re-verified population stands at
**283 records**.

## Position

- This upgrades the 24 split-part certificates of the four sweep bands
  from manifest/receipt documentation to bytes-level independently
  re-verified evidence and **exhausts the 85 survey-identified
  remaining-band certificate records** of this experiment. It does not
  change any frontier number; the solved-1452 bookkeeping is untouched.
- The remaining bytes-re-verification candidates are the newly published
  66j/69j/71e certificate bands (71e manifest published at `a7c24610`)
  and the 63c/63d extractor regeneration.
- **solved 1452 (and the landed 64h fold projection 1472) are manifest
  cover bookkeeping. A WIN7-D10 certificate proves only that its
  individual 7-stone root is a first-player win within depth 10.
  REFUTED-D10 entries are not LOSS proofs. 11x11 empty board, two-stone
  root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain
  UNKNOWN.**

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_splitpart_sweepbands_certificates_bigint_20261117.py`
- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-splitpart-sweepbands-certificates-bigint-independent-reverification-20261117.json`
- this log
