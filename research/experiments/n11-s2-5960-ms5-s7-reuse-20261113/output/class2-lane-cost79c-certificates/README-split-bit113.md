# split certificate bit 113 (cost-79c)

root `00020000000000c09002000200000000`

`n11_s7_00020000000000c09002000200000000.cert` is 2063501 bytes and is published as two parts:

```
cat n11_s7_00020000000000c09002000200000000.cert.part1of2 n11_s7_00020000000000c09002000200000000.cert.part2of2 > n11_s7_00020000000000c09002000200000000.cert
md5sum n11_s7_00020000000000c09002000200000000.cert   # 0b99c1844d12083b15a5162873bb92a1
```

The split is at line boundaries (byte 1033173); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
