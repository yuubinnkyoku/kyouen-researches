# split certificate bit 30 (cost-79c)

root `00000000000000c09002000240000000`

`n11_s7_00000000000000c09002000240000000.cert` is 1294259 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000240000000.cert.part1of2 n11_s7_00000000000000c09002000240000000.cert.part2of2 > n11_s7_00000000000000c09002000240000000.cert
md5sum n11_s7_00000000000000c09002000240000000.cert   # 760993f6989afeed93ef4b801f05ae52
```

The split is at line boundaries (byte 648172); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
