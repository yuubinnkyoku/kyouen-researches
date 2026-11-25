# class2-lane cost-73h WIN7 certificates

Child S6: `00000000200000083800000000000200` (6 stones [9,59,60,61,67,93]; edge cost 73; open parents: the second coverable class-2 target S5 `00000000000000801202000000200000` (19 rows / 1463) and class-2 S5 `00000000000000003800200008000000` (67 rows / 5182) at the head-1249 chain; demand c1=0,c2=2,c4=0). Sweep: 4 WIN7-D10 (bits 45/48/82/96) / 69 REFUTED / 0 capped — see `../class2-lane-cost73h-sweep-audit-20261115.json`.

- bit 45: split at a line boundary into two parts (815,509 + 814,405 bytes):
  - `class2-lane-cost73h-certificates/bit45-root-00000000200000083800200000000200.cert.part1of2` (md5 `60e418d0d59ceee95802a79ea78e7bda`, git blob `1d0f6a4bbf21cb4d6d842dad0838f6ee747d5d7a`)
  - `class2-lane-cost73h-certificates/bit45-root-00000000200000083800200000000200.cert.part2of2` (md5 `db1aa1e9b3dc6096721bcca1597b0cb0`, git blob `0fe43fec9d9164ab924a844936e9fc41eff78445`)
  - Rejoin: `cat class2-lane-cost73h-certificates/bit45-root-00000000200000083800200000000200.cert.part1of2 class2-lane-cost73h-certificates/bit45-root-00000000200000083800200000000200.cert.part2of2 > bit45.cert` (md5 must equal `8f238da2fee832be53dcb6f0ee85ee44`); 44,989 strategy rows, loser mobility 56, extraction nodes 11,046,694.
- bit 48: split at a line boundary into two parts (633,532 + 631,244 bytes):
  - `class2-lane-cost73h-certificates/bit48-root-00000000200000083801000000000200.cert.part1of2` (md5 `2727152f8bafe2d779920167f587c120`, git blob `fa53dbabad90f693183cce1679616a62ad4aada1`)
  - `class2-lane-cost73h-certificates/bit48-root-00000000200000083801000000000200.cert.part2of2` (md5 `681762001148e91be6b82b37882385f8`, git blob `e4e3b066288831b730a117f141e3c3a51d7baa25`)
  - Rejoin: `cat class2-lane-cost73h-certificates/bit48-root-00000000200000083801000000000200.cert.part1of2 class2-lane-cost73h-certificates/bit48-root-00000000200000083801000000000200.cert.part2of2 > bit48.cert` (md5 must equal `6caab3ffd54613666c476b791f3ffe8a`); 34,929 strategy rows, loser mobility 56, extraction nodes 3,638,354.
- bit 82: split at a line boundary into two parts (812,049 + 807,665 bytes):
  - `class2-lane-cost73h-certificates/bit82-root-00000000200400083800000000000200.cert.part1of2` (md5 `ea794babfd3850f893c02a4f7b5c9c68`, git blob `cca89b12bfff1fa911793619954c889f6d0b7694`)
  - `class2-lane-cost73h-certificates/bit82-root-00000000200400083800000000000200.cert.part2of2` (md5 `1391f23b14f247ea0e5602ba4f159c10`, git blob `d21bf57579258a35769e7c43a234fff552f0af81`)
  - Rejoin: `cat class2-lane-cost73h-certificates/bit82-root-00000000200400083800000000000200.cert.part1of2 class2-lane-cost73h-certificates/bit82-root-00000000200400083800000000000200.cert.part2of2 > bit82.cert` (md5 must equal `503cb3c726944fac447e7405aec0f36a`); 44,836 strategy rows, loser mobility 59, extraction nodes 4,175,255.
- bit 96: split at a line boundary into two parts (936,786 + 933,225 bytes):
  - `class2-lane-cost73h-certificates/bit96-root-00000001200000083800000000000200.cert.part1of2` (md5 `71b5ce8a6ad6941d6fe0bf8f76818678`, git blob `274fbfda2dd2fc400d73d3b308c5f3416e7130a8`)
  - `class2-lane-cost73h-certificates/bit96-root-00000001200000083800000000000200.cert.part2of2` (md5 `fdadd9610c0dc27b9b6fdb25f6aa0802`, git blob `3d9e7372737df25cda6c4aba4f9bfb50285cb6e5`)
  - Rejoin: `cat class2-lane-cost73h-certificates/bit96-root-00000001200000083800000000000200.cert.part1of2 class2-lane-cost73h-certificates/bit96-root-00000001200000083800000000000200.cert.part2of2 > bit96.cert` (md5 must equal `f68543a00d5797950da63a2a045089ea`); 51,697 strategy rows, loser mobility 63, extraction nodes 9,284,460.

Totals: 4 certificates, 176,451 strategy rows, 28,144,763 extraction nodes. Every certificate is double-verified (BigInt cofactor verifier and Python Bareiss replay verifier, union missing/extra 0/0 on all 4; per-bit verify records `../class2-lane-cost73h-bit*-bigint-verify` and `../class2-lane-cost73h-bit*-bareiss-verify` records). Manifest: `../class2-lane-cost73h-win7-certificates-20261115.json`.

Interpretation guard: these certificates prove a winner win within depth 10 from the individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; they do not close the child orbit and do not decide either open class-2 parent S5. The 11x11 empty root, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 2 and class 4 remain UNKNOWN.
