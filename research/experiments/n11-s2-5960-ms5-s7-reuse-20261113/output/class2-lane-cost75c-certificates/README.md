# cost-75c WIN7 certificates (child 00000000000000803202000000004000)

All 12 WIN7-D10 candidates of the cost-75c sweep have published certificates.
Eleven bits are stored as 2-part splits and bit 66 as a 3-part split (line
boundary). Rejoin each with `cat <name>.cert.part1of2 <name>.cert.part2of2 >
<name>.cert` (bit 66: concat parts 1-3); the joined md5/sha256 are listed below.

| bit | root | rows | sub-roots | joined md5 | joined sha256 | parts (bytes, md5) |
|-----|------|------|-----------|------------|---------------|--------------------|
| 8 | 00000000000000803202000000004100 | 66,236 | 66 PASS | 635d1fda7ef0afa43d480fb787edc0e3 | c32d6f1a17d8df25ebaa08c10eea0db20f7cdad15974b92d3d38473fcb66388e | part1of2 1,196,029 (5bd222881bbbcfa96fde95e9c6679547), part2of2 1,196,018 (5342ed238b34c91d4019784ed44e5f62) |
| 12 | 00000000000000803202000000005000 | 60,023 | 57 PASS | 5293ef1e140eea8bc048c22fc2a83e76 | 7fe951160cfd247520b9e8a8bbda7f788c76caba0b32cf64294e9005294e7ee0 | part1of2 1,082,715 (8f35edd6c00d07920d9f3cb5d9843fbc), part2of2 1,082,714 (cea6d9817d61f5adce0eef0c6765d1e9) |
| 22 | 00000000000000803202000000404000 | 78,999 | 63 PASS | aaa837e0ef6e75890f2bfbaa6d2b4f52 | 5b4cfab235e4c1ffff6683ef974566f15996ae7203b80a0bd2c21b72b31c3261 | part1of2 1,423,852 (ff3b95c01e319d426894de191784266b), part2of2 1,423,821 (638170915ed9d081470eadfd43c7d6d4) |
| 66 | 00000000000000843202000000004000 | 86,401 | 62 PASS | 07800808777f60a21df188b6a3db7481 | d71328839310757ef75f42acd3289d2776c9a9603f8d873b4998d83732c6f583 | part1of3 1,038,655 (dd694498a0a4dc24620978b9e98d9444), part2of3 1,038,633 (647bb70a1519fa9d3b7d5b2887c8f7a5), part3of3 1,038,612 (300b9b80b1b0505f52d235ed44c5ef81) |
| 84 | 00000000001000803202000000004000 | 59,056 | 59 PASS | 7548731a2cf010bd908b68f89cb09985 | 9a3b94aa7bf358061eab24c9e277938c1a90014d88308c3b70bd1c957badf244 | part1of2 1,064,423 (585a4454e03c7b1db875eeb3612aa68f), part2of2 1,064,366 (cba25a9b2f081262c9083f53fe66f2dd) |
| 89 | 00000000020000803202000000004000 | 60,677 | 58 PASS | 87b6683334d46ef1991db72f9259cfba | 351207ef894878858108ae8d2ce620b1f160f5ce5d16b842929cfcf617c85768 | part1of2 1,093,136 (5f9dab85589cdef3f98c7e72672e4049), part2of2 1,093,099 (0a356e092caf079d2124bb5800f200ae) |
| 96 | 00000001000000803202000000004000 | 42,471 | 55 PASS | dbf142eeb14d62c7c139185046eb7d0f | 7dee9026332ae4a7fd409e357d55d228f1c2b24cdfefba24a06b148c912ce388 | part1of2 765,243 (cee1c48cc8eee5ce589b0706a9e8e520), part2of2 765,232 (9245b68bb9cf1e48e057615e753b2ee6) |
| 97 | 00000002000000803202000000004000 | 55,851 | 55 PASS | 8d9e0917daaa30e01e85c86689ea49ee | 49912205820abcc315991768a61da3d8af0cace107505740d1982d2f3571692c | part1of2 1,006,415 (c133907dc6a1706c897d907c246a5eca), part2of2 1,006,398 (89ad08c0eef77cac10f7a327fe7e2927) |
| 98 | 00000004000000803202000000004000 | 68,738 | 66 PASS | 079a29e46784a5733e684815b48236fb | 185222550a31e835ebc353554fb2da24ca8d0182466047343702776513a3f9c1 | part1of2 1,239,022 (5e51fab075f334b92f4c5b637f91c475), part2of2 1,239,020 (83e8b6a2a810aff896d52732a8d1c50f) |
| 100 | 00000010000000803202000000004000 | 48,859 | 58 PASS | 6c0cf7159e73cfa37b2c310922bef707 | 9d969a138e2c267ab5b75da589aeea59d2411eab514db0ffaf7da71b5f81136b | part1of2 878,654 (8f675eea50a9d057c315540387bb5721), part2of2 878,616 (0266f6a240a61614395ed7c507d78f20) |
| 108 | 00001000000000803202000000004000 | 42,639 | 57 PASS | a703f79d3240322ed7ed5bba6f411765 | b8def7be901359b1cb574834cec4cd9f8bb763d52d5140bb8d8bcd2932309d63 | part1of2 768,931 (33d80b4b3909e6ae0050bdb6e4a8aae8), part2of2 768,889 (8cc2ce971a8f51713d33662e7951366a) |
| 111 | 00008000000000803202000000004000 | 43,428 | 54 PASS | 643a8fc92a0327075d00acea390ea9fc | 4dc436e4201953ef2df1389d079dc7f7465504c9edd42dc446b0e8d6725b1edf | part1of2 781,118 (a92725a9ea3a6af5cfd988e8127f52f8), part2of2 781,107 (daa7f0820a5436238dde13f8c16ed713) |

Example rejoin:

cat bit8-root-00000000000000803202000000004100.cert.part1of2 bit8-root-00000000000000803202000000004100.cert.part2of2 > bit8-root-00000000000000803202000000004100.cert

Verification summary (all 12 PASS): each joined file has 2 header lines
(`n11-terminal-strategy-v1 ...` / `root <hex>`) plus the listed sorted unique
strategy rows; root check 7 stones with loser mobility equal to the independent Bareiss 4x4 enumeration (66/57/63/62/59/58/55/55/66/58/57/54); all sub-roots
PASS; union 0 missing / 0 extra; terminal stone range [13,17]; independent
BigInt cofactor-expansion audit PASS. Every pushed part was verified
byte-exact on the remote by its git blob sha. Two roots are cross-child
duplicates of uncertified win7_roots listings - bit 12 (cost-65h bit-14) and
bit 22 (cost-71b bit-14) - so these are the first published certificates for
those roots and close the respective warm entries. 11x11 empty board remains
UNKNOWN; these certificates prove only individual 7-stone roots within depth 10.
