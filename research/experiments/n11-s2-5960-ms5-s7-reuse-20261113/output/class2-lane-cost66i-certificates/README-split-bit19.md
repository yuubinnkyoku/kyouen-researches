# certificate split for n11_s7_00000000000000801226000000080000.cert

The bit-19 WIN7 certificate (1,478,743 bytes) exceeds the single-run push
transport limit, so it is stored as two parts:

- `n11_s7_00000000000000801226000000080000.cert.part1of2` (739,395 bytes, md5 9c053b5563ce5965c675d6b6af5037b1)
- `n11_s7_00000000000000801226000000080000.cert.part2of2` (739,348 bytes, md5 62dd849f15686af6df397ff6e2b64830)

Recombine (line-boundary split, no bytes added or removed):

    cat n11_s7_00000000000000801226000000080000.cert.part1of2 \
        n11_s7_00000000000000801226000000080000.cert.part2of2 \
        > n11_s7_00000000000000801226000000080000.cert

Concatenation md5: 084bc1f4d0244ca1fc1ee769977060fd
Concatenation sha256: f87df551ab38f73fb34d756fc4be287de42f1538735e7daf6006deb05749b0ac
