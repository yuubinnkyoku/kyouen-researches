# certificate split for n11_s7_00000000010000801226000000000000.cert

The bit-88 WIN7 certificate (2,234,562 bytes) exceeds the single-run push
transport limit, so it is stored as two parts:

- `n11_s7_00000000010000801226000000000000.cert.part1of2` (1,117,299 bytes, md5 6aa0d1598aa6001c97e35cf637f53794)
- `n11_s7_00000000010000801226000000000000.cert.part2of2` (1,117,263 bytes, md5 567a6d3f4fd0cc43197247afbac8b867)

Recombine (line-boundary split, no bytes added or removed):

    cat n11_s7_00000000010000801226000000000000.cert.part1of2 \
        n11_s7_00000000010000801226000000000000.cert.part2of2 \
        > n11_s7_00000000010000801226000000000000.cert

Concatenation md5: 012c0e0e47811825f3214b4cff9e0837
Concatenation sha256: b442ecd155925dc5bed338a50470243908c99702f0cdcc9990282c3e702b1b2a
