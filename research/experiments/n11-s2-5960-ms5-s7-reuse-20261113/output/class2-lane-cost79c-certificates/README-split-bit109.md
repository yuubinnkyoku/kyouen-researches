# split certificate bit 109 (cost-79c)

root `00002000000000c09002000200000000`

`n11_s7_00002000000000c09002000200000000.cert` is 2035216 bytes and is published as two parts:

```
cat n11_s7_00002000000000c09002000200000000.cert.part1of2 n11_s7_00002000000000c09002000200000000.cert.part2of2 > n11_s7_00002000000000c09002000200000000.cert
md5sum n11_s7_00002000000000c09002000200000000.cert   # 9918c5a9ca9f5f8afed0b601d9360ea0
```

The split is at line boundaries (byte 1018742); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
