# class2-lane cost-62a WIN7 certificate

Root: `00000000000000809102000001000800` (7 stones; S6 child `00000000000000809102000001000000` + bit 11; child of the next class-2 target S5 `00000000000000809102000000000000`, the cheapest unswept child cost 62 after the uncoverability audit declared the previous best class-2 S5 receipt-unclosable).

- Full certificate: 24,730 lines (2 header lines + 24,728 rows), md5 `173c3987a63035f2a1722887314af11a`, sha256 `45ec61197dd6f449f186f74c21f73a05adb9e4273f91af559a52135ca85f87e5`.
- Split at a line boundary into two parts (12,365 / 12,365 lines):
  - `bit11-root-00000000000000809102000001000800.cert.part1of2` (md5 `2a20b64fe74e5c1220dc3eb24875614a`)
  - `bit11-root-00000000000000809102000001000800.cert.part2of2` (md5 `eb4f17da6011a2e18fd468a810ddcaea`)
- Rejoin: `cat bit11-root-00000000000000809102000001000800.cert.part1of2 bit11-root-00000000000000809102000001000800.cert.part2of2 > bit11.cert` (md5 must equal `173c3987a63035f2a1722887314af11a`).
- Verification (this session): root-check stones=7 loserMobility=47 (independent legal_candidates.py enumeration); 47/47 sub-roots PASS (all seen>0, terminals>0, terminal ranges within [13,17]); union of consumed winner states equals the 24,728-row set exactly (0 missing / 0 extra); extraction via `cert_driver68.ts` over the repo-verbatim `class4_child1_cert_extractor_exact.ts` (blind kill table, FBS=1<<20, drop-counter): 5,152,966 extraction nodes, fbt_drops=0, fatal=null, all 47 per-move extractions ok and uncapped; rows sorted (no duplicates) before verification per the established extractor note.
- WIN7 verdict cross-checked: sweep batch 2 (2,557,437 nodes), determinism fresh re-run in a separate process (node-exact), the FBS=1<<20 instrumented engine `runner_fbs20.ts` (node-exact, fbtDrops=0), and the parallel raw audit (`research/log/2026-11-14-n11-class2-cost62a-partial-raw-audit.md`) which independently confirmed the root's 7 stones / 35 four-point subsets / 0 zero determinants and D4-distinctness among all 62 candidate roots.
- The completed sweep found 11 WIN7-D10 candidates in this child (bits 1, 11, 32, 66, 86, 89, 95, 105, 109, 112, 118); this bit-11 certificate is the first fully verified receipt for the child (the other ten remain search verdicts).
- This certificate proves a winner win within depth 10 from the individual 7-stone root only. 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN.
