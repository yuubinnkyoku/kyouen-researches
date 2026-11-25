# split certificate bit 28 (cost-79c)

root `00000000000000c09002000210000000`

`n11_s7_00000000000000c09002000210000000.cert` is 2202771 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000210000000.cert.part1of2 n11_s7_00000000000000c09002000210000000.cert.part2of2 > n11_s7_00000000000000c09002000210000000.cert
md5sum n11_s7_00000000000000c09002000210000000.cert   # 71db1787e2dac355391a42e997f4b512
```

The split is at line boundaries (byte 1102396); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
