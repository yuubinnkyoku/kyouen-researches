# split certificate bit 31 (cost-79c)

root `00000000000000c09002000280000000`

`n11_s7_00000000000000c09002000280000000.cert` is 1506445 bytes and is published as two parts:

```
cat n11_s7_00000000000000c09002000280000000.cert.part1of2 n11_s7_00000000000000c09002000280000000.cert.part2of2 > n11_s7_00000000000000c09002000280000000.cert
md5sum n11_s7_00000000000000c09002000280000000.cert   # cf61f6bfdbb6e67981560812d4edd402
```

The split is at line boundaries (byte 754193); the parts are byte-exact sections of the certificate, with the two-line certificate header at the top of part 1 of 2.
