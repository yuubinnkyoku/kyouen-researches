# n11 class2-lane presweep census v15: 79e行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost79e sweep完了（0 WIN7-D10 / 79 REFUTED-D10 / 0 capped・74,450,533 candidate
nodes・raw 12ファイル + audit + claim v2はcommit `4bc11450`で出版・audit blob
`4e10e477`・claim v2 blob `f80e6025`）を受け、head-1473 presweep censusをv14から
v15に更新した。v15は18番目のverdict map（cost79e: 0 WIN / 79 REFUTED / 0 capped）
をoverlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v15_20261118.py`
  （v14スクリプト blob `2980675e` を基盤に、79e raw batch 12ファイル / audit /
  claim v2の入力を追加し、18番目のverdict map `cost79e` を構築）。
- 79e生バッチ12ファイル（9 sweep + det1/det8 + v15 crosscheck）を独立再監査
  （9×3402 + 1×5949 pilot・79/79 per-bit REFUTED-D10・node sum 74,450,533・
  audit per_bitのroot_canon == D4 canon(child|bit) を全79bitで検証・det1/det8は
  ms以外全field同一・v15 cross-engine 7/7一致）。
- claim v2との一致: counts {0, 79, 0}・batches_run 9・open 72/72・
  receipt_fold "not needed"・confirmation 7/7がcensus v14 overlay予測と一致
  （root_canon転移元: pre-64h harvest ×2（bits 30/115）・cost74i ×2（27/93）・
  cost75f ×1（79）・cost79d ×2（46/74））。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。18 map構築は内部conflict 0・
  harvestとのcross-agree 42 canons（79e map由来 +2）。
- 39 family行を再計算し、v14のpublished countsを39/39で再現
  （`family_row_v14_newly_covered_counts_reproduced`・
  `family_row_open_v14_minus_79e_only_reproduced`: 差分は79e map由来のみ）。
- 二重実行byte-identical（110,098 bytes）。

## 結果

- 79e行（`00000000020000003800000880000000`）をswept扱いのexcluded行として
  記録（open 0・known 79・newly_covered_by_eighteen_maps 77・完全反証・
  証明書なし・receipt fold不要）。4つ目の完全反証行（74i・75f・79dに次ぐ）。
  fully swept childrenは18に増加。
- 次ターゲット: **`00000000020000003800000180000000`（cost 80・open 68・
  confirmation 12・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:2}）**。census v14 runner-up。v14時点のopen 70のうち
  2 bits（35/85）が79e mapのcanon等価で新規被覆され、open 68に減少。
  confirmation 12 bits（5/27/30/35/41/46/74/79/85/90/93/115）は全て
  REFUTED-D10（pre-64h harvest ×4・cost74i ×2・cost79e ×2・cost75f ×2・
  cost79d ×2）で、sweepでfreshに再実行する。legal_candidates.py独立列挙と
  80bit（68 open + 12 confirmation）で一致。
- runner-up: `00000000020000003800200080000000`（cost 80・open 68）。
  ranking top-10の10行はすべてparent
  `00000000020000003800000080000000`（cost 80〜86・open 68〜74）。
  v14 rankingの非swept 9行は全てv15 top-10に残留（9/9）。
- cross_checks新規（79e系）: refuted bits claim/audit一致 79/79・
  raw batch再監査 12ファイル（9×3402 + 1×5949 pilot・node sum 74,450,533）・
  confirmation 7/7（root_canonはcensus v14 transfer canonsと一致）・
  v15 cross-engine 7/7 loss=false・det再実行field-identical・receipt fold
  "not needed (0 win bits)"・証明書 "not applicable (0 win bits)"。

## 出版

- census v15 JSON: `class2-lane-next-target-presweep-1473-v15-20261118.json`
  （git blob `dfb61db5bec195f3f98442815753ba88d9e96fff`）
- スクリプト: git blob `5a53528f4cfe269412dd20437e34f5e5d1ba605f`

## 制限

- censusはsearch-plan bookkeepingのみで、verdictを新規作成しない。
  REFUTED-D10はLOSS証明ではない。11×11空盤、二石root {49,60}/{59,60}、
  S2 {59,60}、class 1/2/4はいずれも **UNKNOWN** のまま。
