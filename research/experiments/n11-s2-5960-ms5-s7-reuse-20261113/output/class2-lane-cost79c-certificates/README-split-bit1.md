# split certificate bit 1 (cost-79c)

root `00000000000000c09002000200000002`

`n11_s7_00000000000000c09002000200000002.cert` is 2109554 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000200000002.cert.part1of2 n11_s7_00000000000000c09002000200000002.cert.part2of2 > n11_s7_00000000000000c09002000200000002.cert
md5sum n11_s7_00000000000000c09002000200000002.cert   # 61797ef8c0a06c4b5e276d6556ed49a4
```

The split is at line boundaries (byte 1055919); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
