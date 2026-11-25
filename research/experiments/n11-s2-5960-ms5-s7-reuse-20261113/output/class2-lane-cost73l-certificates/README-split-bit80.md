# split certificate bit 80 (cost-73l)

root `00000000000100c09002000000400000`

`n11_s7_00000000000100c09002000000400000.cert` is 1357356 bytes and is published as two parts:

```
cat n11_s7_00000000000100c09002000000400000.cert.part1of2 n11_s7_00000000000100c09002000000400000.cert.part2of2 > n11_s7_00000000000100c09002000000400000.cert
md5sum n11_s7_00000000000100c09002000000400000.cert   # 29ccacbb30872331c7edf99fdfea87ca
```

The split is at a line boundary (byte 678676); both parts are byte-exact halves of the certificate.
