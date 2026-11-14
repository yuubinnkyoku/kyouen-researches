# cost-58b WIN7 bit120 certificate (line-boundary 2-part split)

root: 01000000000000803202000000002000 (7 stones)

The certificate is stored as:

- bit120-root-01000000000000803202000000002000.cert.part1of2 (756,812 bytes, md5 d3f549b5aa6ddc7e429c36a7c3cb4da2)
- bit120-root-01000000000000803202000000002000.cert.part2of2 (756,627 bytes, md5 8ee13607fc9cf5f83d00f770d9ce474c)

Rejoin with:

cat bit120-root-01000000000000803202000000002000.cert.part1of2 bit120-root-01000000000000803202000000002000.cert.part2of2 > bit120-root-01000000000000803202000000002000.cert

Joined file: 1,513,439 bytes, md5 3db43cd61598091d29f51417e6de9bf3 (41,969 sorted rows + 2 header lines).
All verification PASS: root-check 7 stones / loserMobility 51 = independent enumeration, 51/51 sub-roots, union 0 missing / 0 extra, terminal range [13,17].
