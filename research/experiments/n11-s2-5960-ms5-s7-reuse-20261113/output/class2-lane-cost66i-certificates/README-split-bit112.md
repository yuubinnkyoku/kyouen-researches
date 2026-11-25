# certificate split for n11_s7_00010000000000801226000000000000.cert

The bit-112 WIN7 certificate (1,548,417 bytes) exceeds the single-run push
transport limit, so it is stored as two parts:

- `n11_s7_00010000000000801226000000000000.cert.part1of2` (774,225 bytes, md5 109dd3e07b46b5b49fe8025d602b995a)
- `n11_s7_00010000000000801226000000000000.cert.part2of2` (774,192 bytes, md5 a9f1241264141ff7313e51fdd9311cfa)

Recombine (line-boundary split, no bytes added or removed):

    cat n11_s7_00010000000000801226000000000000.cert.part1of2 \
        n11_s7_00010000000000801226000000000000.cert.part2of2 \
        > n11_s7_00010000000000801226000000000000.cert

Concatenation md5: c3ecf967f79faaf0930d320d5fbcc0f1
Concatenation sha256: c41358679be873aa1a10915e572d884602664fca32e60d6f8b714aa567952617
