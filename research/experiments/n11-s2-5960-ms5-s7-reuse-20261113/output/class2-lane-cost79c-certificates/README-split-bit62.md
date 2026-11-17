# split certificate bit 62 (cost-79c)

root `00000000000000c0d002000200000000`

`n11_s7_00000000000000c0d002000200000000.cert` is 2180176 bytes and is published as two parts:

```
cat n11_s7_00000000000000c0d002000200000000.cert.part1of2 n11_s7_00000000000000c0d002000200000000.cert.part2of2 > n11_s7_00000000000000c0d002000200000000.cert
md5sum n11_s7_00000000000000c0d002000200000000.cert   # aa1016f9516ed1c51ce4e3215cef476f
```

The split is at line boundaries (byte 1091584); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
