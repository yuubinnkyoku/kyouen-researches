# split certificate bit 2 (cost-79c)

root `00000000000000c09002000200000004`

`n11_s7_00000000000000c09002000200000004.cert` is 2359753 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000200000004.cert.part1of2 n11_s7_00000000000000c09002000200000004.cert.part2of2 > n11_s7_00000000000000c09002000200000004.cert
md5sum n11_s7_00000000000000c09002000200000004.cert   # a50f5bc03604d3a11140c6ffc923d129
```

The split is at line boundaries (byte 1181307); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
