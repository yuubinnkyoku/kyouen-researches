# 2026-11-15：cost-71c sweep 完成（2 WIN7-D10 / 69 REFUTED）と両証明書の blind 抽出・二重独立検証・byte-exact push

開始時main: cost-70e receipts fold 済みの canonical head `1233/6614/522131/4884/385854`。本セッションは前半（claim `class2-lane-cost71c-inflight-20261115.json` の IN FLIGHT push、9バッチ sweep 完走、v16 determinism rerun、v15 crosscheck、両証明書の blind 抽出と BigInt 独立検証、環境リセット1回・bit-exact 復元）からの続きである。AGENTS.md、research/knowledge/README.md、11×11関連claim・logを確認した。

## 成果1：第二独立検証器（Python/Bareiss）で両証明書 PASS

`verify_cost71c_win7_bareiss_independent.py`（Python stdlibのみ・Bareiss 4×4整数行列式・インクリメンタル forbidden mask・**全loser応手展開**・戦略行集合の厳密閉包をassert）を書き直した。初版はwinner着手後に増える三組をloserの禁手maskへ反映しておらず unreachable position で missing row FAIL となったが、修正後は両rootとも PASS（検証器の網が機能した記録として残す）。

- **bit24** root `00000000000000801202000081200000`: 47 sub-roots PASS・22,196行・union missing/extra 0/0・terminal {13,15,17}・71,252 winner states。
- **bit112** root `00010000000000801202000080200000`: 56 sub-roots PASS・60,406行・union 0/0・terminal {13,15,17}・194,567 winner states。
- BigInt検証器 `verify_win7_certificate_bigint_independent.mjs`（remote blob `62b5d9413daafb172f6e10249976ee6808f7b454`）も両rootで再実行 PASS（bit24 47/47 sub-roots・bit112 56/56・union 0/0・terminal [13,17]）。検証記録4件（bigint/bareiss × bit24/bit112）をpush。

## 成果2：証明書2件の byte-exact push

- bit24: 単一ファイル `bit24-root-00000000000000801202000081200000.cert`（804,827B・md5 `9e63e160ba08a7edc827b81dbf9067a5`・git blob `8d9b4459…`）。
- bit112: 行境界2分割（part1: 30,194行/1,089,744B md5 `8ae38925…`、part2: 30,214行/1,089,688B md5 `832120f7…`）。**join md5 == whole md5 `e38d80cfd89ccc8e48264c36a9e7701a5`** を着地後の remote part 連結で再確認。
- 着地確認は raw CDN md5 照合（API rate limit 中も代替手段として有効）。

## 成果3：独立 raw-sweep 監査

`audit_cost71c_raw_sweep_20261115.py`（70e監査スクリプト流用・Python stdlib・Bareiss整数行列式）をpush・実行し `class2-lane-cost71c-sweep-audit-20261115.json` を反映した。

- 71 legal candidates を独立再列挙し claim と bit-exact 一致。child stones [21,31,49,57,60,71]・child safe。
- aggregate 再導出: **2 WIN7-D10（bits 24/112・win nodes 457,250/3,985,676）・69 REFUTED・0 capped・総nodes 94,128,613**。9バッチの bit 列は claim の batch_bits 計画と完全一致、pilot 3402×9 PASS。
- determinism rerun（batch5）node-exact、v15 cross-engine（bits 24/112 loss=true 2,695,796/14,334,967・アンカー 75/113/116 loss=false・pilot 5949）一致。
- 一石削除 D4 lift: del31 = parent1 `00000000000000801202000000200000` bit-exact（28行/2119）、del21 → 第2開親 `00000000000000801202000080000000`（43行/3268）、残り4削除は head-1233 ranking CSV に存在しない閉行。
- D4 duplicate scan: 49個の公開 win7-certificates manifest・126 canonical roots と比較し **0重複**（両WIN rootは新規coverage）。
- head-1233 ranking（175開行）・top-candidates CSV の parent 行・demand 行（c1=0,c2=2,c4=0・edge cost 71）cross-check PASS。

## 成果4：manifest・README・claim v2

- `class2-lane-cost71c-win7-certificates-20261115.json`: bits 24/112、総82,602 rows・extraction nodes 24,639,331・fbt_drops 0、bigint/bareiss両検証記録、**fold PENDING** 明記。
- `class2-lane-cost71c-certificates/README.md`（rejoin手順・md5・検証境界）をpush。
- claim を v2 として更新（status: completed, fold pending）。remote md5 照合済み。

## 検証・統制メモ

- 環境リセット越えで証明書抽出を2回行い同一 md5（determinism control）。
- v16/v15 cross-engine・batch5 determinism rerun・D4 disjointness・独立監査で三重の engine-level 統制。
- **REFUTED-D10 は LOSS 証明ではない**。2証明書は個別7石rootの深さ10以内の先手勝ちのみを証明し、fold前はどのfrontier数も変えない。
- 標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-sweep-audit-20261115.json)、[certificate manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-win7-certificates-20261115.json)、[claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-inflight-20261115.json)、[certificates README](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-certificates/README.md)。
