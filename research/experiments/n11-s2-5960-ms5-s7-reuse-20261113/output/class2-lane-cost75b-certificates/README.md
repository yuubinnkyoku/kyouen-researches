# cost-75b WIN7 certificates (child 00000000000000803202000000000008)

All 7 WIN7-D10 candidates of the cost-75b sweep have published certificates.
Bit 51 is a single file; the other six are stored as 2-part splits (line
boundary). Rejoin each with `cat <name>.cert.part1of2 <name>.cert.part2of2 >
<name>.cert`; the joined md5 is listed below.

| bit | root | rows | sub-roots | joined md5 | parts (bytes, md5) |
|-----|------|------|-----------|------------|--------------------|
| 7 | 00000000000000803202000000000088 | 47,257 | 57 PASS | 2e20e75c305962b4bc46045185778d14 | part1of2 855,879 (597e90442acab4a2f95b1a7a06f6cc02), part2of2 854,240 (36e3b929a9dc5311303f63684e94d588) |
| 51 | 0000000000000080320a000000000008 | 32,508 | 51 PASS | 6b78713f6af3b72817fca15194623873 | single file 1,175,778 |
| 54 | 00000000000000803242000000000008 | 50,955 | 63 PASS | ae02f4b95be3e50518ce7830d2083434 | part1of2 922,360 (1f9bf9e95d4b038e0b7562d9927f4f7a), part2of2 919,434 (28240192ba67d06c439e14d7fddd16e1) |
| 84 | 00000000001000803202000000000008 | 55,484 | 61 PASS | cdfbd1bede75265c774af02cba1c7e9f | part1of2 1,003,784 (92e930b603577c97f52a437fa5209c73), part2of2 1,001,619 (4b9e4e15190da3e83bb2233e22e911e9) |
| 89 | 00000000020000803202000000000008 | 45,501 | 55 PASS | bc52efa62fe7794ad121f3d295e627a8 | part1of2 823,069 (fb1ff9c35c9c0d1b794c6ba632bcc071), part2of2 821,830 (815f646e156d26c83cfdbe312c505369) |
| 99 | 00000008000000803202000000000008 | 40,056 | 55 PASS | 84e8444599ab0ba7d71989a88a9412bc | part1of2 724,959 (96b5b9dce8b1e250cc481ec7fcb9bf1d), part2of2 722,911 (3fdcf32362d09008baa1a4ac4f523c28) |
| 116 | 00100000000000803202000000000008 | 80,911 | 64 PASS | 85f01799e61b1f1fb402861924c4b2af | part1of2 1,461,526 (b929e14b256d7cbcd4c0f842cd5b3e0c), part2of2 1,459,159 (302f36543aa067001cd3bd17a54320c5) |

Example rejoin:

cat bit7-root-00000000000000803202000000000088.cert.part1of2 bit7-root-00000000000000803202000000000088.cert.part2of2 > bit7-root-00000000000000803202000000000088.cert

Verification summary (all 7 PASS): each joined file has 2 header lines
(`n11-terminal-strategy-v1 ...` / `root <hex>`) plus the listed sorted unique
strategy rows; root check 7 stones with loser mobility equal to the
independent Bareiss 4x4 enumeration (57/51/63/61/55/55/64); all sub-roots
PASS; union 0 missing / 0 extra; terminal stone range [13,17]; independent
BigInt cofactor-expansion audit PASS, including a re-run on the
remote-rejoined bytes after landing. The bit-54 root is a cross-child
duplicate of the uncertified cost-70c bit-3 win7_roots listing - this is the
first published certificate for that root and closes the cost-70c bit-3 warm
entry. 11x11 empty board remains UNKNOWN; these certificates prove only
individual 7-stone roots within depth 10.
