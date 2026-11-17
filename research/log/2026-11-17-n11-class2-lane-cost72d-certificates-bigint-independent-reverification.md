# 2026-11-17 n11 class2-lane: cost-72d certificates third-implementation BigInt independent bytes re-verification

## Scope

The parallel lane published the cost-72d sweep and its 11 WIN7-D10
certificates (claim v2 `c64e28fd`, manifest
`class2-lane-cost72d-win7-certificates-20261117.json` inside the band dir,
21 certificate files: 10 split pairs + bit 75 whole, 522,517 rows /
18,850,168 bytes). After the 63cd regeneration pair this was the immediate
next un-re-verified candidate. This session executed the 72d batch: **11
certificates / 55 pinned files / 18,850,168 certificate bytes**, each
re-verified with the third-implementation BigInt independent verifier and
cross-agreed with the two sidecar record families. On top of the 300
records of the earlier batches this brings the bytes-level independently
re-verified population to **311 records** (cost-71e byte-audited
separately by the parallel lane, not counted here).

## Method

`reverify_cost72d_certificates_bigint_20261117.py`
(record sources all at main commit
`83b2958b64bbac06817c14480e215d63f312185d`, the parent of this batch's
own publication; before which every cost-72d file was last touched at
commit `39b52643` / earlier):

1. mirror all 54 files of the band dir plus the claim v2 file from
   commit-pinned raw URLs and assert each file's git blob sha and size
   against the authoritative GitHub directory listing at the pin
   (machine-extracted into pins72d.txt, 54/54 asserted + claim = 55/55);
2. assert the verifier's own git blob sha
   (`62b5d9413daafb172f6e10249976ee6808f7b454`);
3. structural pre-assertions on all 11 manifest records (verdict WIN7,
   depth 10, subroots == subroots_pass == loser_mobility, terminal range
   [13,17], union 0/0 documented, fbt_drops 0, no fatal) and manifest
   totals reproduced from the mirror (rows, extraction_nodes,
   published_bytes, fbt/capped zeros);
4. per certificate: whole file (bit 75) pinned directly; split
   certificates (10 of 11) reconstructed as exact part1+part2
   concatenations (part1 on a line boundary and exactly the manifest
   `split_cut_byte`), joined **md5 and sha256 both** asserted against the
   manifest; 2-line header asserted and data rows == manifest rows;
5. run `verify_win7_certificate_bigint_independent.mjs` once per
   certificate (a **third implementation** beyond the generator's own
   Bareiss `verify_bit7_win7_cert.ts` documented in the manifest), with
   the expected loser mobility as argv[3], and assert verdict /
   root_hex / stones 7 / root_safe / rows sorted-unique / union 0/0 /
   terminal range within 13..17 / strategy_rows == manifest rows /
   consumed_winner_rows == rows / subroots_passed == manifest
   subroots_pass / root_mobility == manifest loser_mobility;
6. sidecar cross-agreement: per-bit `rootcheck.json` (cost-72d format: a
   **two-line JSONL**, line 1 stones=7 + loserMobility, line 2 rows +
   empty stats) and per-bit `subroots.jsonl` (cost-72d format:
   **batched**, up to 8 loser-first-moves per line; the subroot count is
   the m-key count across lines, not the line count) sums reproduce the
   BigInt verifier output exactly on all 11 certificates:
   sum(seen) == visited_states_across_subroots, sum(terminals) ==
   terminal_count, sum(opponentEdges) == loser_reply_edges, m-key count
   == subroots_pass, every per-move range within [13,17];
7. README-split docs (10 split certificates) cross-checked: whole bytes,
   split boundary byte, md5, root line (no bit-75 README: it is a whole
   file);
8. **independent D4 canonicalization check**: a seventh, in-script
   implementation (min hex over the eight square symmetries) reproduces
   every record's `d4_canon_root`; `raw_is_canon` (True for 6 records,
   False for 5) verified as exactly root_hex == d4_canon_root; the 11
   D4 canons mutually distinct;
9. cross-batch disjointness from the 102 root_hex values of the five
   earlier independently re-verified batches (single-file 43 + split
   bands 18 + sweepbands 24 + 66j/69j 15 + 63cd 2; the five batch
   outputs blob-pinned inline), also D4-canon disjoint against the
   computed canons of all 102 earlier roots;
10. **claim v2 basis pin**: the mirrored claim file reproduces git blob
    `c64e28fdc91ba9ffaa3518dfbc9d764ec5663b05`, the exact sha stated in
    the manifest basis; schema v2, win7_d10_bits equal to the manifest
    bits, manifest path match;
11. deterministic JSON output, two runs byte-identical (md5
    `ad6e29023ceaef7bce2470cc64bac833`).

## Result

**11/11 PASS** (single-node ~20 s per run, 4 worker threads):

| bit | root | rows | storage | mobility |
|-----|------|------|---------|----------|
| 1 | 00000000000000403800000008004002 | 44,845 | split | 55 |
| 6 | 00000000000000403800000008004040 | 53,663 | split | 54 |
| 24 | 00000000000000403800000009004000 | 54,219 | split | 57 |
| 25 | 0000000000000040380000000a004000 | 41,052 | split | 54 |
| 43 | 00000000000000403800080008004000 | 56,270 | split | 58 |
| 49 | 00000000000000403802000008004000 | 41,769 | split | 59 |
| 75 | 00000000000008403800000008004000 | 32,192 | whole | 50 |
| 80 | 00000000000100403800000008004000 | 37,972 | split | 53 |
| 83 | 00000000000800403800000008004000 | 56,195 | split | 57 |
| 98 | 00000004000000403800000008004000 | 45,625 | split | 55 |
| 114 | 00040000000000403800000008004000 | 58,715 | split | 61 |

- verifier_fail 0, manifest md5 mismatch 0, manifest sha256 mismatch 0,
  pin blob sha mismatch 0, sidecar cross-agreement fail 0;
- total rows independently verified: **522,517** (== manifest totals);
- total sub-roots independently verified: **613**;
- total extraction nodes in manifest reproduced: **120,204,754**;
- total certificate bytes rehashed: **18,850,168** (== manifest
  published_bytes);
- rerun byte-identical (twice).

Example of the sidecar agreement (bit 114): subroots.jsonl has 8 lines
batching 61 per-loser-move keys, sum(seen) 123,782 == verifier
visited_states_across_subroots, sum(terminals) 21,070 ==
terminal_count, sum(opponentEdges) 109,970 == loser_reply_edges, and
the BigInt verifier independently confirms the Bareiss-documented
strategy from 58,715 rows.

## Position

- This upgrades the 11 certificates of the newly published cost-72d band
  from manifest+sidecar documentation to bytes-level, third-implementation
  independently re-verified evidence, cross-agreeing the generator Bareiss
  verification and the BigInt .mjs verifier field by field via the two
  sidecar record families. It does not change any frontier number and
  closes no manifest row; the cost-72d receipt fold stays pending behind
  the 76c/66i/66j/69j/71e folds handled by their own lanes.
- The bytes-re-verified population now stands at 311 records (33 + 82 +
  83 + 43 + 18 + 24 + 15 + 2 + 11); cost-71e (13 records) was
  byte-audited by the parallel lane. Remaining candidates: any newly
  published certificate bands (the parallel lane's cost-73i sweep is
  in flight).
- **solved 1452 / head 1472 are manifest cover bookkeeping. A WIN7-D10
  certificate proves only that its individual 7-stone root is a
  first-player win within depth 10. The 61 REFUTED-D10 bits of the
  cost-72d sweep are NOT LOSS proofs. 11x11 empty board, two-stone roots
  {49,60} and {59,60}, S2 {59,60}, class 1, class 2 and class 4 all
  remain UNKNOWN.**

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_cost72d_certificates_bigint_20261117.py`
- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72d-certificates-bigint-independent-reverification-20261117.json`
- this log
