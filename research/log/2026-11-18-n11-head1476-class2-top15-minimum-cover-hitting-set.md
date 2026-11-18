# 2026-11-18 N11 head-1476 class-2: membership-ranked minimum-cover prefix fully closed at 15 roots

## Result

For the best own-closable class-2 parent `00000000000000403800000008000000`, the published candidate universe has 757 D4-canonical roots and 359,610 minimum covers of size 6. The prior elimination analysis published the exact survival curve only through the top 12 membership-ranked roots, leaving 14,625 minimum covers.

A single reverse suffix 0/1 dynamic program now extends the exact curve through the first zero:

| Excluded prefix k | Surviving minimum 6-root covers | Killed |
|---:|---:|---:|
| 0 | 359,610 | 0 |
| 1 | 301,200 | 58,410 |
| 2 | 256,800 | 102,810 |
| 3 | 213,330 | 146,280 |
| 4 | 177,180 | 182,430 |
| 5 | 141,225 | 218,385 |
| 6 | 105,315 | 254,295 |
| 7 | 69,675 | 289,935 |
| 8 | 34,125 | 325,485 |
| 9 | 29,250 | 330,360 |
| 10 | 23,400 | 336,210 |
| 11 | 19,500 | 340,110 |
| 12 | 14,625 | 344,985 |
| 13 | 9,750 | 349,860 |
| 14 | 4,875 | 354,735 |
| 15 | **0** | **359,610** |

Thus the first 15 roots in the exact ranking (membership descending, root hex ascending for ties) form a hitting set for every minimum 6-root cover in this candidate universe. This is only a prefix result; no claim is made that 15 is the globally minimum hitting-set size.

## Exact residual partition after excluding the top 12

The remaining 14,625 minimum covers split into three disjoint classes:

| Rank | Root | Membership in all covers | Residual covers forced to include it |
|---:|---|---:|---:|
| 13 | `00000000200040003801000000100000` | 44,280 | 4,875 |
| 14 | `00000000000021801202000000100000` | 43,980 | 4,875 |
| 15 | `00000000000000c09002000000001200` | 43,920 | 4,875 |

Every pairwise joint count among these three roots, conditioned on avoiding ranks 1–12, is zero. Their forced-inclusion counts sum to 14,625. Therefore every residual minimum cover contains exactly one of ranks 13–15.

All three roots cover the common target row `00000000000000c09002000000001000`; their pairwise co-occurrence is impossible in a 6-root cover of 11 rows because two such roots would use two roots to cover at most three distinct rows, leaving only four roots to cover the remaining eight rows plus the common row.

## Method and checks

- Input membership table: blob `ab1e655f4a89a677e57515cdbacfe56894323013`.
- Prior k=0..12 elimination output: blob `5f6185483f7a6458535b8e38a73483a23db2ef29`.
- Roots sorted by membership descending, then bytewise lowercase-hex ascending.
- Reverse suffix DP over 2^11 row masks and root count 0..6 computes every prefix survival count in one pass.
- The published prior curve k=0..12 is reproduced exactly.
- Membership identity: sum of all 757 root memberships = 6 × 359,610.
- Forced-inclusion DP verifies each of ranks 13–15 contributes 4,875 residual covers; all three pairwise intersections and the triple intersection are zero.
- 19 checks pass in the in-memory run. The computation used the pinned GitHub file contents in the available V8 execution environment. The published `.mjs` is a local reproduction script; it was not executed from a repository checkout in this run.

## Interpretation boundary

This is exact planning combinatorics for minimum-size 6-root covers only. It does not rank by measured search cost and does not establish that any root is WIN7-D10. If all top 15 roots are unavailable to depth-10 receipts, no minimum 6-root plan remains, but larger covers may still exist. No new verdict, certificate, receipt fold, or S5 closure was produced.

REFUTED-D10 and STERILE are not LOSS proofs. The standard 11×11 empty board, the two-stone roots `{49,60}` and `{59,60}`, S2 `{59,60}`, and classes 1/2/4 remain **UNKNOWN**.
