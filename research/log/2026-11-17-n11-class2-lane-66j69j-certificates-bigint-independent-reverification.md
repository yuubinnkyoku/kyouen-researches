# 2026-11-17 n11 class2-lane: cost-66j/69j certificates third-implementation BigInt independent bytes re-verification

## Scope

The sweep-bands session (log `d8fc41c7`, 24 records) exhausted the 85
survey-identified remaining-band certificate records, leaving the two
newly published certificate bands cost-66j (9 records) and cost-69j
(6 records) as the immediate next candidates; the parallel lane has
independently byte-audited cost-71e
(`audit_cost71e_published_bytes_20261117.sh`, re-fetch sha256/md5/bytes
vs manifest pins). This session executed the 66j/69j batch and went one
step further than a bytes audit: **66j (9) + 69j (6) = 15 certificates /
67 pinned files / 24,291,939 certificate bytes**, each re-verified with
the third-implementation BigInt independent verifier and cross-agreed
with the two sidecar record families. On top of the 283 records of the
five earlier batches this brings the bytes-level independently
re-verified population to **298 records** (cost-71e byte-audited
separately by the parallel lane, not counted here).

## Method

`reverify_66j69j_certificates_bigint_20261117.py`
(record sources all at main commit `d8fc41c7c9c2307a5392511b9435400a4c79c84f`,
before which every 66j/69j file was last touched on 2026-11-16):

1. mirror all 67 files of the two band dirs from commit-pinned raw URLs
   and assert each file's git blob sha and size against the authoritative
   GitHub directory listings at the pin (machine-extracted into
   pins66j69j.txt, 67/67 asserted); the two manifests re-fetched at the
   pin and byte-compared against main;
2. assert the verifier's own git blob sha
   (`62b5d9413daafb172f6e10249976ee6808f7b454`);
3. structural pre-assertions on all 15 manifest records (verdict WIN7,
   depth 10, subroots == subroots_pass, loser_mobility == subroots_pass,
   terminal range [13,17], union 0/0 documented);
4. per certificate: whole files pinned directly; split certificates
   (11 of 15) reconstructed as exact part1+part2 concatenations
   (part1 on a line boundary), joined **md5 and sha256 both** asserted
   against the manifest (these manifests document sha256 in addition to
   md5; new check for this batch family);
5. run `verify_win7_certificate_bigint_independent.mjs` once per
   certificate (a **third implementation** beyond the generator's own
   Bareiss `verify_bit7_win7_cert.ts` documented in the manifests) and
   assert verdict / root_hex / stones 7 / root_safe / rows sorted-unique
   / union 0/0 / terminal range within 13..17 / strategy_rows ==
   manifest rows / consumed_winner_rows == rows / subroots_passed ==
   manifest subroots_pass / root_mobility == manifest loser_mobility;
6. sidecar cross-agreement (new in this batch): per-bit `rootcheck.json`
   (stones=7, loserMobility == manifest == verifier) and per-bit
   `subroots.json` (per-loser-first-move stats from the Bareiss
   verification) sums reproduce the BigInt verifier output exactly on
   all 15 certificates: sum(seen) == visited_states_across_subroots,
   sum(terminals) == terminal_count, sum(opponentEdges) ==
   loser_reply_edges, key count == subroots_pass, every per-move
   range within [13,17];
7. README-split docs (11 split certificates) cross-checked: whole
   bytes, split boundary byte, md5, root line (66j READMEs additionally
   document the D4 canon; 69j READMEs do not, so the canon check applies
   only where documented);
8. **independent D4 canonicalization check**: a sixth, in-script
   implementation (min hex over the eight square symmetries) reproduces
   every record's `d4_canon_root`; `raw_is_canon` (True for 6 records,
   False for 9) verified as exactly root_hex == d4_canon_root; the 15
   D4 canons mutually distinct;
9. cross-batch disjointness from the 85 root_hex values of the three
   earlier band batches (asserted at load against the three published
   outputs); joined sha256 and git blob sha recorded for all 15 as new
   bytes-level documentation;
10. deterministic JSON output, two runs byte-identical.

## Result

**15/15 PASS** (single-node ~75 s per run, 4 worker threads):

| band | records | bits | whole/split | notes |
|------|---------|------|-------------|-------|
| 66j | 9 | 7/9/30/66/78/79/92/96/114 | 3 whole + 6 split | 9 rootcheck+subroots sidecars, 6 README-splits |
| 69j | 6 | 1/52/75/109/110/114 | 1 whole + 5 split | 6 rootcheck+subroots sidecars, 5 README-splits |

- verifier_fail 0, manifest md5 mismatch 0, manifest sha256 mismatch 0,
  pin blob sha mismatch 0, sidecar cross-agreement fail 0;
- total rows independently verified: **673,364** (66j 372,824 + 69j 300,540);
- total sub-roots independently verified: **814** (484 + 330);
- total certificate bytes rehashed: **24,291,939** (13,447,266 + 10,844,673);
- rerun byte-identical (twice).

Example of the sidecar agreement (66j bit 7): subroots.json has 53
per-loser-move keys, sum(seen) 75,095 == verifier
visited_states_across_subroots, sum(terminals) 12,773 == terminal_count,
sum(opponentEdges) 66,519 == loser_reply_edges, and the BigInt verifier
independently confirms the Bareiss-documented strategy from 32,244 rows.

## Position

- This upgrades the 15 certificates of the newly published cost-66j and
  cost-69j bands from manifest+sidecar documentation to bytes-level,
  third-implementation independently re-verified evidence, and it is the
  first batch that cross-agrees two independent verification
  implementations (generator Bareiss vs BigInt .mjs) field by field via
  the subroots sidecars. It does not change any frontier number and
  closes no manifest row; the receipt folds of these rows remain behind
  the pending 76c/66i/66j folds handled by the parallel lane.
- The bytes-re-verified population now stands at 298 records (33 + 82 +
  83 + 43 + 18 + 24 + 15); cost-71e (13 records) was byte-audited by
  the parallel lane. Remaining candidates: the 63c/63d extractor
  regeneration and any newly published certificate bands.
- **solved 1452 (and the landed 64h fold projection 1472) are manifest
  cover bookkeeping. A WIN7-D10 certificate proves only that its
  individual 7-stone root is a first-player win within depth 10. The 63
  REFUTED-D10 bits are NOT LOSS proofs. 11x11 empty board, two-stone
  root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain
  UNKNOWN.**

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_66j69j_certificates_bigint_20261117.py`
- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-66j69j-certificates-bigint-independent-reverification-20261117.json`
- this log
