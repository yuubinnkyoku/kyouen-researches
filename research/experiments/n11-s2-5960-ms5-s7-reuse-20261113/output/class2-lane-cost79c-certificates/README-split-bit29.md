# split certificate bit 29 (cost-79c)

root `00000000000000c09002000220000000`

`n11_s7_00000000000000c09002000220000000.cert` is 2126816 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000220000000.cert.part1of2 n11_s7_00000000000000c09002000220000000.cert.part2of2 > n11_s7_00000000000000c09002000220000000.cert
md5sum n11_s7_00000000000000c09002000220000000.cert   # 3e187722b7cbac0ac42df9005cfdf31c
```

The split is at line boundaries (byte 1064962); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
