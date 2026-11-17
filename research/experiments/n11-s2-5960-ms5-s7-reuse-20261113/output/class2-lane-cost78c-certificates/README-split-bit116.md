# split certificate bit 116 (cost-78c)

root `00100000000000403800000008000008`

`n11_s7_00100000000000403800000008000008.cert` is 2840107 bytes and is published as three parts:

```
cat n11_s7_00100000000000403800000008000008.cert.part1of3 n11_s7_00100000000000403800000008000008.cert.part2of3 n11_s7_00100000000000403800000008000008.cert.part3of3 > n11_s7_00100000000000403800000008000008.cert
md5sum n11_s7_00100000000000403800000008000008.cert   # 7a0694f61e0bcf6ded606161c1e0a907
```

The splits are at line boundaries (bytes 946728 and 1893416); all parts are byte-exact pieces of the certificate. Three parts instead of two because of the publication transport size limit.
