# split certificate bit 46 (cost-63c)

root `000000000000008090a2400000000000` (D4 canon `000000000000008090a2400000000000`)

`n11_s7_000000000000008090a2400000000000.cert` is 1639652 bytes and is published as two parts:

```
cat n11_s7_000000000000008090a2400000000000.cert.part1of2 n11_s7_000000000000008090a2400000000000.cert.part2of2 > n11_s7_000000000000008090a2400000000000.cert
md5sum n11_s7_000000000000008090a2400000000000.cert   # 01bcaabc9d20d20e6215826e22c01181
```

The split is at a line boundary (byte 819839); both parts are byte-exact halves of the certificate.
sha256 of the whole certificate: 485fdea26c0b56685bd6443bc1c03b4fad34011be55063265f4338f02e27bba9

Regeneration note (2026-11-17): this certificate was first extracted on 2026-11-14
with the extractor CLI (`class4_child1_cert_extractor_exact.ts`) whose default
KILL_BIT7 session-6 preference table was active; the bytes were regenerated
byte-identically on 2026-11-17 from a different environment (see
`regenerate_verify_cost63cd_certificates_20261117.py`).
