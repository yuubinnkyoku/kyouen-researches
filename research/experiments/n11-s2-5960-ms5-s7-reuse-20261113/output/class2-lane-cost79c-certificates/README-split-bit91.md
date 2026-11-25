# split certificate bit 91 (cost-79c)

root `00000000080000c09002000200000000`

`n11_s7_00000000080000c09002000200000000.cert` is 1745898 bytes and is published as two parts:

```
cat n11_s7_00000000080000c09002000200000000.cert.part1of2 n11_s7_00000000080000c09002000200000000.cert.part2of2 > n11_s7_00000000080000c09002000200000000.cert
md5sum n11_s7_00000000080000c09002000200000000.cert   # 74b66545f375f19473b81bd185aee18b
```

The split is at line boundaries (byte 874651); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
