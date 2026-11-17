# split certificate bit 96 (cost-79c)

root `00000001000000c09002000200000000`

`n11_s7_00000001000000c09002000200000000.cert` is 2319448 bytes and is published as two parts:

```
cat n11_s7_00000001000000c09002000200000000.cert.part1of2 n11_s7_00000001000000c09002000200000000.cert.part2of2 > n11_s7_00000001000000c09002000200000000.cert
md5sum n11_s7_00000001000000c09002000200000000.cert   # e7beda98ffee657d17d0d00e6b937357
```

The split is at line boundaries (byte 1161262); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
