# cost73l sweep 完走: 34 WIN7-D10 / 39 REFUTED-D10 / 0 capped（2026-11-17）

## 背景

head-1473 presweep census v8（commit `43838dec`）で選定した rank-1 行
`00000000000000c09002000000400000`（cost 73・parent `00000000000000403800000008000000`・
demand c2=2）を **cost-73l** として、claim v1（同コミット）に基づき fresh v17
depth-10 sweep を実行した。66 open bits（7×9 + 1×3 の8バッチ）+ 7 confirmation bits
[65, 86, 90, 94, 97, 106, 110]（batch 9）。初回実行であり、sandbox reset・
並走同一childの重複実行は存在しない。

## 実行

- engine: class4_child1_runner_v17.ts（blob `c132cc64`）・depth 10・cap 1e9/bit・
  andclose 1・bitごとにfresh state。9/9バッチで pilot_d6 = 3402 厳密一致。
- 2並列worker（2CPU上限遵守）で9バッチ+det 2本+v15 4本を完走。
- 検証: (1) stdlib raw audit（`audit_cost73l_raw_batches_20261117.py`）全PASS、
  (2) det rerun batch1/batch4（最重bit 47, 6,045,349 nodes 含む）は全非ms field一致、
  (3) v15 cross-engine（blob `8744fc65`）で34 WIN bit全て loss=true・4/4 pilot 5949・
  0 capped・node total 286,284,260。

## 結果

- **WIN7-D10: 34 bits** [1,2,3,4,6,8,9,18,21,23,25,28,29,32,34,41,42,44,47,53,54,
  61,62,64,66,80,95,105,106,110,112,113,116,119]（candidate nodes 133,895,305 +
  9 pilot controls = 133,925,923 total）。
- **REFUTED-D10: 39 bits**・capped 0。bit 91 は 13-15 石で早期決着（24,376 nodes、
  他72 bitは 13-17 石）。
- **confirmation 7/7 予測どおり**: 106 = cost73j bit 118（WIN・出版証明書で被覆済み）、
  110 = cost73k bit 98（WIN・同）、65 = cost69j bit 118・86 = cost72d bit 118・
  90 = cost76c bit 48・94 = cost73i bit 118（以上 REFUTED）、97 = pre-64h harvest。
- **bit 97 の harvest 源を特定**: pre-64h の出版 raw batch 全数から D4 canon 照合し、
  **cost64d bit 118**（REFUTED・768,078 nodes・raw batch8 blob `ce86d0fb`）が唯一の
  canon一致源。claim v1 の "pre-64h harvest" が concrete lane に解決された。
- **転送7件の canon 等価を独立再導出**: census v8 スクリプト（blob `c86171ba`）の
  D4 canon 関数を verbatim 転写し、canon(source_child|source_bit) ==
  claim root_canon == canon(73l_child|bit) を 7/7 で検証（raw-identical は 0件、
  node数はlabeling差）。
- 73k比でWIN密度が顕著に高い（34/73 vs 25/73）。root側需要の偏りを示唆するが、
  行の fold は保留のまま。

## 制限

- REFUTED-D10 は LOSS 証明ではない。capped 0 でも depth 10 以外の勝敗は語らない。
- WIN7-D10 証明書は個別 7 石 root の first-player win（depth 10 以内）のみを証明。
- 本sweepは manifest 行を 1つも閉じない。receipt fold は 66i/66j/69j/71e/72d/
  73i/73j/73k fold の後ろで pending。
- **11x11 空盤、二石 root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はいずれも UNKNOWN**。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ev73l_batches_20261117.sh`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost73l_raw_batches_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/update_claim73l_v2_20261117.py`
- raw batch 9本 + det 2本 + v15 crosscheck 4本 + raw sweep audit + claim v2
  （`class2-lane-cost73l-*`・`output/` 以下）

## 次の一手

- 32個の新規 WIN bit（106/110除く）の盲証明書抽出（per-bit fresh MS=1<<23 処方）→
  BigInt 独立検証 → manifest 付き出版。bit 106/110 は出版済み 73j bit 118 /
  73k bit 98 証明書で被覆済みのため抽出不要。
- 並走管轄には手を出さない: 66i receipt fold（bit19）、73i 証明書出版。
