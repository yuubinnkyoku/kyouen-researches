# 2026-11-14 w=86 正制御（高速レーン）

## 実施内容

幅86・level 17・REST6 掃引を完走（width_sweep.mjs / width_survivor_collect.mjs、総ノード 4,250,048,258・833チャンク・unique 3,487・maximal 3,300）し、生残パターンの帰属・実在性・孤立性を検証した。

## 結果

1. **生残は leaves 11 計上・ユニーク行集合 10**。ユニーク10は、11050円 (2x−105)²+(2y−105)²=11050 の86幅34点窓 census（10窓・a=−3..1, 19..23）と完全一致。**事前予測「ユニーク生残 ≥10・phantom 0」はちょうど10で完全的中**。w83/w84/w85 に続き4例目の正制御パス。
2. **leaves=11 の正体**: mask 3249 の leaf が aborted chunk 境界で二重計上（chunk from=3239 が cap 超過で abort した時の部分探索で1 leaf → from=3249 で再探索して同一 leaf を再計上）。node 数で既知の aborted-chunk 再実行現象の leaf 版・初観測。生残数は survPats を unique 化して読むのが正しい（protocol accounting 注記として記録）。
3. **REST16 再検査**: 10パターン全て allPass。**11050円10窓の直接検証**: すべて points=34・equalsPattern。**R' ≤ 1e6 孤立性スキャン**（1,964円・3形式）: realizer は R'=5525 のみ。
4. **スキャン check のバグ修正**: 旧 width84/85_realizability_scan.mjs の check は窓先頭行 = キー L 自身を仮定し、pattern[0]>0 の窓を数え落とす under-approximation だった。修正 check（窓開始 A = k0 − 2·pat[0] を全キーから試行）で w84 生残4・w85 生残6 を再スキャン: いずれも realizer は 5525 のみで、旧結論は不変（誤りは偽陰性方向のみ・過大主張なし）。

## 意味

- 予測プロトコル（機械 census による事前予測 → 掃引で検証）が3幅連続で完全的中。census = 生残の全単射対応が w84/85/86 で確立。
- 実在性は11050円で構成的に証明済み、孤立性は R' ≤ 1e6 の数値スキャンによる裏付け（全称主張ではない）。

## ファイル

- state: `research/experiments/width69-84-sweep-20261114/output/state_w86.json`
- スクリプト: `research/experiments/width84-positive-control-20261114/scripts/width86_realizability_scan.mjs`
- 出力: `research/experiments/width84-positive-control-20261114/output/width86_positive_control.json`
- レポート: `research/experiments/width84-positive-control-20261114/report-w86.md`

## 次のタスク（次回実行へ）

- w=87..91 の36点窓（18行）census に基づく事前予測の登録（w87: 34点窓12窓 → ユニーク生残 ≥ 10 + 2×18 = 46、全て実現可能・census 超過は phantom、leaves は aborted chunk 二重計上に注意）。w87..91 の36点窓 census は w87=2, w88=4, w89=6, w90=8, w91=10 窓（各36点18行）。
- w=87 掃引（~5G nodes・重いので次回レーンで検討）。
