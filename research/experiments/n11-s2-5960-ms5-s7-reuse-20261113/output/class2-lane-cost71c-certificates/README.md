# class2-lane cost-71c WIN7 certificates

Child S6: `00000000000000801202000080200000` (6 stones [21,31,49,57,60,71]; edge cost 71 from the second coverable class-2 target S5 `00000000000000801202000000200000`; demand c1=0,c2=2,c4=0; both parents class 2). Sweep: 2 WIN7-D10 (bits 24/112) / 69 REFUTED / 0 capped — see `../class2-lane-cost71c-sweep-audit-20261115.json`.

- bit 24: `bit24-root-00000000000000801202000081200000.cert` — 7 stones (child + bit 24), 22,196 rows, md5 `9e63e160ba08a7edc827b81dbf9067a5`, git blob `8d9b4459f489b3224c64b4f6bbd37b8ff2dd23e3`, single file.
- bit 112: split at a line boundary into two parts (30,194 + 30,214 lines):
  - `bit112-root-00010000000000801202000080200000.cert.part1of2` (md5 `8ae38925c2878839dda65ada0ca8831a`, git blob `494ed0532f688d96e9a678720728bf4ba31039b1`)
  - `bit112-root-00010000000000801202000080200000.cert.part2of2` (md5 `832120f7a84086f6249716556c73f1d6`, git blob `c84955f6fbc183f92be5df379aa587acbe3442b1`)
  - Rejoin: `cat bit112-root-00010000000000801202000080200000.cert.part1of2 bit112-root-00010000000000801202000080200000.cert.part2of2 > bit112.cert` (md5 must equal `e38d80cfd89ccc8e48264c36a9e7701a5`).
- Verification (this session series, both certificates verified independently twice):
  - `verify_win7_certificate_bigint_independent.mjs` — BigInt 3x3 cofactor expansion of the exact lifted determinant. bit24: 47/47 sub-roots PASS, union missing/extra 0/0, terminal [13,17]. bit112: 56/56 sub-roots PASS, union 0/0, terminal [13,17].
  - `verify_cost71c_win7_bareiss_independent.py` — Python stdlib Bareiss 4x4 replay, full loser-reply expansion with incremental exact forbidden masks, strategy-union closure. bit24: 47 sub-roots, 71,252 visited winner states, union 0/0, terminal {13,15,17}. bit112: 56 sub-roots, 194,567 visited winner states, union 0/0, terminal {13,15,17}.
  - Verify records: `../class2-lane-cost71c-bit24-bigint-verify-20261115.json`, `../class2-lane-cost71c-bit112-bigint-verify-20261115.json`, `../class2-lane-cost71c-bit24-bareiss-verify-20261115.json`, `../class2-lane-cost71c-bit112-bareiss-verify-20261115.json`.
- Determinism: after an environment reset the certificates were re-extracted from the raw sweep and reproduced byte-identical md5s.
- Extraction: repo-verbatim `class4_child1_cert_extractor_exact.ts` (git blob `52bcaf509ea12fad4c936501d30d26b5b66c0085`) via `cert_driver71c.ts`; blind (empty kill table), FBS 1<<20, fbt_drops 0. Extraction nodes: bit24 4,163,765; bit112 20,475,566.
- These certificates prove a winner win within depth 10 from the individual 7-stone roots only. REFUTED-D10 is not a LOSS proof. 11x11 empty root / {49,60} / {59,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN.
