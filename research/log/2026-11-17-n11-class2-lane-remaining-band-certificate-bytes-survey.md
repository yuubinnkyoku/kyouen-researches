# 2026-11-17 n11 class2-lane: remaining-band certificate bytes survey (117 published certificates across 31 bands identified)

## Scope

Follow-up to the 2026-11-17 receipts-recompute 83-certificate bytes
re-verification session (`aded350b` log line). That session's Position
section described the remaining tier-R bytes-re-verification candidates as
"receipts-recompute groups without a dedicated band certificate directory".
This session probed all 31 remaining candidate bands directly and found
that **all of them have published certificate bytes**; the earlier
description was wrong and is corrected here.

## Method

GitHub contents API directory listings of
`research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost<band>-certificates`
for each candidate band (63f/63g/67c/69f/69h/69i/70e/70f/71c/72b/72c/73g/
73h/74d/74g/75d/76a/76b/77a/77b/77c/77d/78a/79a/80d/82c/83a/83b/83c/83d/84a),
single `.cert`/`.gz.b64` files and `.cert.partNofM` split parts counted
with sizes. Process note: a first parallel probe reported false "no-dir"
answers for several bands (connector concurrency); all listings were
re-taken sequentially, and the artifact contains only sequentially
confirmed listings.

## Result

- **117 published certificates across 31 bands, 172,924,127 bytes total**:
  - 93 single-file certificates across 27 bands (134,712,477 bytes);
  - 24 split-part certificates (`.cert.part1of2`/`.part2of2`) across
    4 bands: 72c (9), 73g (8), 73h (4), 83d (3), 38,211,650 bytes of parts.
- Largest populations: 63g (14), 74d (8), 72b (7), 77c (7), 77d (7),
  72c (9 parts), 73g (8 parts).
- 72c/73g/73h directories carry a README.md; 83d does not.

## Position

- This is filesystem-level survey bookkeeping: it identifies where
  published bytes exist, not which records are already verified. The next
  bytes-re-verification batch must first cross-reference the census v3
  (commit `0c486e53`) tier classification and the coverage of the earlier
  sessions (cost-58c `427e29fa`, warm/multiband `7693da2a`, the 83-record
  session) and locate per-record documentation (win7 manifests /
  receipts-recompute / inflight files) for each band before asserting
  rows/md5/sub_roots against the verifier.
- Split-part certificates need defined concatenation semantics and both
  part blob shas pinned; treat them as a separate later batch after the
  single-file population.
- Candidate next batch (single-file, largest first): 63g (14) + 74d (8) +
  77c (7) + 77d (7) + 72b (7) = 43 certificates, ~58.0 MB.
- **No new certificate was verified in this survey. solved 1452 is
  manifest cover bookkeeping. WIN7-D10 certificates prove only individual
  7-stone first-player wins within depth 10; REFUTED-D10 is not a LOSS
  proof. 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
  classes 1/2/4 all remain UNKNOWN.**

## Artifacts

- output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-remaining-band-certificate-bytes-survey-20261117.json` (git blob `e5cb92360fd08fb729286756a2d1b5277ee56ebe`)
- this log
