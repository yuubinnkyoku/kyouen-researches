# split certificate bit 70 (cost-63d)

root `00000000000000c09082000000080000` (D4 canon `00000000000000c09082000000080000`)

`n11_s7_00000000000000c09082000000080000.cert` is 1415650 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09082000000080000.cert.part1of2 n11_s7_00000000000000c09082000000080000.cert.part2of2 > n11_s7_00000000000000c09082000000080000.cert
md5sum n11_s7_00000000000000c09082000000080000.cert   # 63a3cb44f1cfc7262509214a9f24d3ca
```

The split is at a line boundary (byte 707859); both parts are byte-exact halves of the certificate.
sha256 of the whole certificate: 46acdf5eab5f37b0298fe353b419f33971d2a2164ff3d5d1ddcda6658d8a73dd

Regeneration note (2026-11-17): this certificate was first extracted on 2026-11-14
with the extractor CLI (`class4_child1_cert_extractor_exact.ts`) whose default
KILL_BIT7 session-6 preference table was active; the bytes were regenerated
byte-identically on 2026-11-17 from a different environment (see
`regenerate_verify_cost63cd_certificates_20261117.py`).
