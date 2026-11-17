# split certificate bit 100 (cost-79c)

root `00000010000000c09002000200000000`

`n11_s7_00000010000000c09002000200000000.cert` is 1957583 bytes and is published as two parts:

```
cat n11_s7_00000010000000c09002000200000000.cert.part1of2 n11_s7_00000010000000c09002000200000000.cert.part2of2 > n11_s7_00000010000000c09002000200000000.cert
md5sum n11_s7_00000010000000c09002000200000000.cert   # ab375956b7d026343e9635500b4fecb8
```

The split is at line boundaries (byte 980303); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
