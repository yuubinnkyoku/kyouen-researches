# certificate split for n11_s7_00000000000000801626000000000000.cert

The bit-58 WIN7 certificate (1,366,065 bytes) exceeds the single-run push
transport limit, so it is stored as two parts:

- `n11_s7_00000000000000801626000000000000.cert.part1of2` (683,037 bytes, md5 2fc0579f39286cd067485882aa84a6e8)
- `n11_s7_00000000000000801626000000000000.cert.part2of2` (683,028 bytes, md5 8c362042898dd5052d5added7d5f509a)

Recombine (line-boundary split, no bytes added or removed):

    cat n11_s7_00000000000000801626000000000000.cert.part1of2 \
        n11_s7_00000000000000801626000000000000.cert.part2of2 \
        > n11_s7_00000000000000801626000000000000.cert

Concatenation md5: 058f1b2bb8af3f3b3b9c05849a8ebcfe
Concatenation sha256: 7bc9d4780e8f200bab20946453c972fc065bc5b754a1a73461bbc6a7d83acd86
