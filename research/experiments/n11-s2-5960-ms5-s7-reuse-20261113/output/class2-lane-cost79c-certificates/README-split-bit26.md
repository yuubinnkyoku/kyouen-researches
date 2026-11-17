# split certificate bit 26 (cost-79c)

root `00000000000000c09002000204000000`

`n11_s7_00000000000000c09002000204000000.cert` is 2138264 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000204000000.cert.part1of2 n11_s7_00000000000000c09002000204000000.cert.part2of2 > n11_s7_00000000000000c09002000204000000.cert
md5sum n11_s7_00000000000000c09002000204000000.cert   # 65284e22f8c2f227a9ba8cea0ccf806b
```

The split is at line boundaries (byte 1069997); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
