# tmp-cost83a (completed by reconstruction 2026-11-15)

Working directory for `recompute_frontier_cost83a_receipts_20261115.py`.

The cost-83a lane (fold commit 4cc183ce) published its fold script, its four
WIN7 certificates and a partial checkpoint of this directory (bit12/58/72
`.rows` + `.rows.summary.json` + `legal-moves.json`, commit 477a5199), but
not the extraction-receipt / verifier files the fold script reads, so the
published fold script could not be re-run end-to-end from main alone. This
directory was completed by
`reconstruct_tmp_cost83a_20261115.py` (in this experiment's `scripts/`) exclusively from artifacts
that are on main, using the published independent verifiers:

- `bit{12,58,72,95}.cert-receipt.json`: recomputed from the published
  certificate bytes (whole files for bit12/58/72; the row-boundary
  part1of2/part2of2 join for bit95, per-part CRLF -> LF, exactly as the
  fold script joins them). md5/rows match the published head JSON records
  (`class-frontier-cost83a-receipts-recompute-20261115.json`,
  `cost83a_addition`: rows 40,417/41,891/36,293/58,190).
- `legal-moves.json`: the lane's published file, kept as published; the
  legal loser first moves recomputed with exact-integer Bareiss 4x4
  determinants equal it exactly (mobility 60/58/57/68 == published
  `sub_roots_pass`).
- the published partial `.rows` files (bits 12/58/72) are cross-checked by
  the reconstruction: their row sets equal the certificate row sets and
  their `.rows.summary.json` nRows equal the published rows
  (bit95.rows is not on main and is not read by the fold script, which
  takes the rows directly from the certificates).
- `bit*.bigint.json`: fresh runs of the published independent verifier
  `scripts/verify_win7_certificate_bigint_independent.mjs` (BigInt 3x3
  cofactor expansion). All four: union_missing=0, union_extra=0,
  terminal_range [13,17].
- `bit*.tsverify.json`: fresh runs of the published independent verifier
  `scripts/verify_bit7_win7_cert.ts` (Number-Bareiss). Line 1 is the
  `--root-check` output, line 2 the `--subroots` output over the full legal
  first-move list. All four: loserMobility == sub_roots_pass, every
  sub-root range within [13,17].
- `bit*.consumed.txt`: the consumed winner-state keys emitted by the same
  TS verifier runs (`--consumed-out`); the set of consumed keys equals the
  full certificate row set (asserted by the reconstruction script, the
  fold script and the second-verification script).

Provenance note: these are reconstruction-session outputs of the same
published verifiers, not the original lane's files (which were lost with
that lane's local environment). Every value that the fold script asserts
on is independently re-derived here and re-checked by re-running the
published fold script end-to-end: after this repair it reproduces the head
1309/6538/516477/4808/380200 and all three published outputs
byte-identical (head JSON blob 74e35f22..., ranking CSV 70eab6c4...,
top-candidates CSV fad56f79...).

Publication status of `bit*.consumed.txt`: only `bit72.consumed.txt`
(1,757,415 bytes, remote blob byte-verified via the raw CDN, 36,293
consumed winner-state keys) is pushed, as a format witness of the TS
verifier's consumed-winner-key emission. The bit12/bit58/bit95 emissions
(1.77/1.96/2.48 MB) are regenerated locally by the reconstruct script -
it re-runs the TS verifier with `--consumed-out` and asserts
`len(set(consumed)) == rows` for every bit before the fold script
re-checks the same files. The fold script therefore expects the
reconstruct step to have run (see the reproduce block below); after that
it runs from main alone.

The intermediate joined certificate files (`c83a-bit*.cert`) are not part of
the published set; the reconstruction script regenerates them from the
`class2-lane-cost83a-certificates/` parts.

Reproduce everything from main with:

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost83a_20261115.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83a_receipts_20261115.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost83a_fold_second_independent_20261115.py
```

The third command is the second independent verification of the whole
cost-83a fold (see
`output/class2-lane-cost83a-fold-second-verification-20261115.json`); it
executes the reconstruction and the fold script itself as subprocesses and
re-derives the sweep, the certificates (third-system rational geometry),
the D4 marginals and the 596-root inventory with independent code.
