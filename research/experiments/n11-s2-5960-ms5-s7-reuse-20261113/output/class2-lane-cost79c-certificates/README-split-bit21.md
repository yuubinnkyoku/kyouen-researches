# split certificate bit 21 (cost-79c)

root `00000000000000c09002000200200000`

`n11_s7_00000000000000c09002000200200000.cert` is 1760977 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000200200000.cert.part1of2 n11_s7_00000000000000c09002000200200000.cert.part2of2 > n11_s7_00000000000000c09002000200200000.cert
md5sum n11_s7_00000000000000c09002000200200000.cert   # ef4593eb0935142d46bfcd930de8da1d
```

The split is at line boundaries (byte 881366); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
