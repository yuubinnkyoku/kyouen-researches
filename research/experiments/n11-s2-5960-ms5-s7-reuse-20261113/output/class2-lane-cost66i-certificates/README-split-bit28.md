# certificate split for n11_s7_00000000000000801226000010000000.cert

The bit-28 WIN7 certificate (1,729,318 bytes) exceeds the single-run push
transport limit, so it is stored as two parts:

- `n11_s7_00000000000000801226000010000000.cert.part1of2` (864,694 bytes, md5 4fbeb10a47dd393c90a529e4ae2280b9)
- `n11_s7_00000000000000801226000010000000.cert.part2of2` (864,624 bytes, md5 23051dd97ed28550cf25ed48d2292a45)

Recombine (line-boundary split, no bytes added or removed):

    cat n11_s7_00000000000000801226000010000000.cert.part1of2 \
        n11_s7_00000000000000801226000010000000.cert.part2of2 \
        > n11_s7_00000000000000801226000010000000.cert

Concatenation md5: 3a50222b79a3b7bbaefe7d65e511de76
Concatenation sha256: e9639b2bf74abdf7a3d2a6f744a4c68acd316e6bf176a88b2617f01ce97cfd9a
