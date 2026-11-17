# n11 class2-lane cost78c WIN7証明書band完了: 11証明書の抽出・独立検証・出版 (2026-11-17)

## 背景

cost78c sweep完了（log `2026-11-17-n11-class2-lane-cost78c-sweep-complete.md`・claim v3・
commit `e1456625`）で確定した11 WIN7-D10 bits [1, 4, 9, 30, 49, 69, 75, 79, 100, 114,
116]に対し、73l-bandと同一のpipeline（盲抽出 → engine-free独立検証 → 出版）を
実行した。78cはpresweep-1473 bandで初のWIN付き行であり、証明書が必要な
初の78c成果。

## 実行

- 抽出: `scripts/extract78c_all_20261117.sh`（root = child|1<<bit を
  `legal_candidates.py` に通し、`cert_driver78c.ts`（73l driverの複製・argv駆動）が
  repo-verbatim `extractor_exact_ms23`（MS=1<<23単行置換・engine v15内蔵・kill table空）
  で抽出。bit毎にfresh process・行は重複排除してsort。
- 検証: `scripts/verify_cost78c_one.sh`（73l orchestratorの複製）が
  `verify_bit7_win7_cert.ts`（Bareiss 4x4・engine不使用）で (1) root-check
  （stones=7・loser mobilityが独立 `legal_candidates.py` 列挙と一致）、
  (2) 全loser初手指しをbatchでsub-root検証、(3) consumed winner-state unionと
  証明書行集合の両方向比較、を実施。
- 決定性: bits 69, 116（サイズ範囲両端・1,240,643 / 2,840,107 bytes）を
  fresh processで再抽出しbyte-identical（md5）。

## 結果: 11/11 証明書 完全出版

- 全11 bitで fbt_drops=0・fatalなし・per-move cappedなし。抽出node数合計
  77,967,826・行数合計 614,003・出版bytes合計 22,223,603。
- 検証は11/11でPASS: root-check stones=7・loser mobility一致
  （bit毎52〜66手）、全sub-root PASS、union 0 missing / 0 extra。
- per-bit明細（bit: rows / extraction nodes / 出版bytes / 分割）:
  1: 65,094 / 7,895,087 / 2,357,106 / 2分割
  4: 65,807 / 11,679,047 / 2,385,176 / 2分割
  9: 71,021 / 7,989,656 / 2,576,151 / 2分割
  30: 48,923 / 5,685,074 / 1,771,135 / 2分割
  49: 43,147 / 3,526,805 / 1,562,547 / 2分割
  69: 34,293 / 3,780,908 / 1,240,643 / 2分割
  75: 36,342 / 4,603,333 / 1,314,119 / 2分割
  79: 48,729 / 5,658,601 / 1,766,556 / 2分割
  100: 54,460 / 5,520,973 / 1,967,414 / 2分割
  114: 67,593 / 8,455,172 / 2,442,649 / 2分割
  116: 78,594 / 13,173,170 / 2,840,107 / 3分割（出版transportサイズ上限のため）
- 出版はband commits `b359756f`..`97650e27`（21 commits・23 part files全部
  raw CDNでbyte-exact着地確認済み）。manifest
  `class2-lane-cost78c-win7-certificates-20261117.json`（blob `b7fe519e`）に
  per-bit明細・md5/sha256・D4 canon rootを記録。
- claim v4（blob `5cd0591a`）でsweep+証明書の完了状態を記録。

## 制限

- 証明書が証明するのは「個別7石rootからdepth 10以内の先手勝ち」のみ。
  manifest行は本bandでは閉じない。receipt foldは
  66i/66j/69j/71e/72d/73i/73j/73k/73l fold完了後。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v12で78c行をswept扱い（11 WIN7-D10・証明書出版済み・67 REFUTED-D10）
  として更新し、次ターゲット（census v11 runner-up cost 79・open 69）を選定。
- 並走管轄のまま手を出さないもの: 66i receipt fold、73i証明書の出版、
  cost73k測定系。必要ならBigInt第三実装による再検証も候補。
