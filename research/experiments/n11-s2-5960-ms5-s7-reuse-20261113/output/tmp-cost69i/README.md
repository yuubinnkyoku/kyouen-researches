# tmp-cost69i (reconstructed 2026-11-15)

Working directory for `recompute_frontier_cost69i_receipts_20261115.py`.

The cost-69i lane (commit 79d866f8) published its fold script but not this
working directory, so the fold script could not be re-run end-to-end from
main alone. This directory was reconstructed by
`scripts/reconstruct_tmp_cost69i_20261115.py` exclusively from artifacts that
are on main, using the published independent verifiers:

- `bit{21,29,97,100}.cert-receipt.json`: recomputed from the published
  certificate bytes (whole files for bit21/bit97; row-boundary
  part1of2/part2of2 joins for bit29/bit100, CRLF -> LF, exactly as the fold
  script joins them). md5/rows/bytes match the published head JSON records
  (`class-frontier-cost69i-receipts-recompute-20261115.json`).
- `legal-moves.json`: legal loser first moves at each 7-stone root,
  recomputed with exact-integer Bareiss 4x4 determinants; mobility
  56/56/46/58 equals the published `sub_roots_pass`.
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
  full certificate row set (asserted by the fold script and by the
  reconstruction script).

Provenance note: these are reconstruction-session outputs of the same
published verifiers, not the original lane's files (which were lost with
that lane's local environment). Every value that the fold script asserts on
is independently re-derived here and re-checked by re-running the published
fold script end-to-end: after this repair it reproduces the head
1273/6574/519179/4844/382902 and all three published outputs byte-identical
(head JSON blob 8692a7a6..., ranking CSV 7ce2e616..., top-candidates CSV
945f6556...).

The intermediate joined certificate files (`c69i-bit*.cert`) are not part of
the published set; the reconstruction script regenerates them from the
`class2-lane-cost69i-certificates/` parts.

Reproduce everything from main with:

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost69i_20261115.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69i_receipts_20261115.py
```
