# split certificate bit 3 (cost-71e)

root `00000000000000c09002000000002008`

`n11_s7_00000000000000c09002000000002008.cert` is 1299200 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000000002008.cert.part1of2 n11_s7_00000000000000c09002000000002008.cert.part2of2 > n11_s7_00000000000000c09002000000002008.cert
md5sum n11_s7_00000000000000c09002000000002008.cert   # cf094e2df7b17d94a05b436eab8de09a
```

The split is at a line boundary (byte 649608); both parts are byte-exact halves of the certificate.
