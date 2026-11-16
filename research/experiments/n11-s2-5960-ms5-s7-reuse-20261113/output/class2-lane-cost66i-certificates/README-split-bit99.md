# certificate split for n11_s7_00000008000000801226000000000000.cert

The bit-99 WIN7 certificate (1,494,354 bytes) exceeds the single-run push
transport limit, so it is stored as two parts:

- `n11_s7_00000008000000801226000000000000.cert.part1of2` (747,182 bytes, md5 4e2e6525d1d353d2750af1a46f4758d9)
- `n11_s7_00000008000000801226000000000000.cert.part2of2` (747,172 bytes, md5 2ee93e409b07b3feaf1c645155c7c881)

Recombine (line-boundary split, no bytes added or removed):

    cat n11_s7_00000008000000801226000000000000.cert.part1of2 \
        n11_s7_00000008000000801226000000000000.cert.part2of2 \
        > n11_s7_00000008000000801226000000000000.cert

Concatenation md5: 5b566ba91ca6ee57e897f4bd15df29c1
Concatenation sha256: 5d0a683d12da3dbb87631a02e788e1bd6394e8157a80cbfbc0fd60a86af1f144
