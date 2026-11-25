# cost-80b WIN7 certificates (split transport note)

The bit 50 certificate (root `00000000020000003804040080000000`) is 2,223,980
bytes / 61,567 lines (2 header + 61,565 rows), which exceeds the lane's
single-file push transport ceiling (~1.7 MB per commit operation). It is
therefore stored as two parts split at a line boundary:

- `n11_s7_00000000020000003804040080000000.cert.part1of2` - lines 1..30000
  (1,085,298 bytes, md5 e468dbb803470cb16dd739947aa1cba7)
- `n11_s7_00000000020000003804040080000000.cert.part2of2` - lines 30001..61567
  (1,138,682 bytes, md5 bcce5c0edb96630997e8fb69cd1fc2f4)

Reassemble and check:

    cat n11_s7_00000000020000003804040080000000.cert.part1of2 n11_s7_00000000020000003804040080000000.cert.part2of2 > n11_s7_00000000020000003804040080000000.cert
    md5sum n11_s7_00000000020000003804040080000000.cert
    1ca210fee08212ba79632b5de46372ca

Verification protocol (identical to the other class4-lane certificates) is in
the record JSON `class4-lane-cost80b-win7-certificates-20261114.json` and the
log `research/log/2026-11-14-class4-lane-cost80b-win7.md`:
verify_bit7_win7_cert.ts with --root 00000000020000003804040080000000,
--root-check and all 65 loser first-move sub-roots with --consumed-out.

The split is a transport artifact only: the two parts concatenated in order are
byte-identical (md5 above) to the locally verified certificate whose 65/65
sub-roots PASS with consumed union == row set (0/0).
