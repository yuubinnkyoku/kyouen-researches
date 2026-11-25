# w=86 正制御レポート（2026-11-14 高速レーン）

## 概要

幅86・level 17・REST6 掃引を完走し、生残パターン全 10 種が機械 census（11050円の86幅34点窓 10窓）と完全一致することを確認した。予測プロトコル「ユニーク生残 ≥10・phantom 0」は **ユニーク生残ちょうど10** で完全に的中した（leaves は後述の二重計上で 11）。w83/w84/w85 に続き **4例目の正制御パス**。

## 掃引サマリ（state_w86.json 参照）

| 項目 | 値 |
|---|---|
| 総ノード数 | 4,250,048,258 |
| チャンク数 | 833（cap escalation 110） |
| unique masks | 3,487 |
| maximal masks | 3,300 |
| leaves（素朴計上） | **11** |
| ユニーク生残行集合 | **10** |

## 生残10パターンと11050円の窓対応

すべて mask として 126, 169, 456, 1376, 1909, 2612, 2696, 3052, 3119, 3249 に帰属（width83_survivor_probe.mjs による帰属確認済み）。10 パターンはすべて円 C11050: (2x−105)²+(2y−105)²=11050（48点）の86幅窓で直接実現：

| パターン | 窓 x範囲 | 円内点数 | 行数 |
|---|---|---|---|
| p3249 | [−3, 82] | 34 | 17 |
| p2696 | [−2, 83] | 34 | 17 |
| p2612 | [−1, 84] | 34 | 17 |
| p3119 | [0, 85] | 34 | 17 |
| p126 | [1, 86] | 34 | 17 |
| p1376 | [20, 105] | 34 | 17 |
| p3052 | [21, 106] | 34 | 17 |
| p169 | [19, 104] | 34 | 17 |
| p1909 | [22, 107] | 34 | 17 |
| p456 | [23, 108] | 34 | 17 |

窓開始 a = −3..1, 19..23 の10窓 = circle11050_window_census.mjs の w86 census（10窓）と完全一致。**certificate-phantom 0件**。

## leaves=11 vs ユニーク10: aborted chunk による二重計上

state 内で p3249 が2回計上されている。原因は chunk from=3239 が node cap で aborted した際、部分探索が leaf（p3249 の行集合）を1つ見つけて記録し、続く chunk from=3249 で同一 leaf を再探索・再計上したこと。node 数で既知だった現象（aborted chunk の再実行による部分重複）の leaf 版で、**本レーンで初観測**。生残数を素朴に chunk 合算で読む際の protocol accounting 上の注意として記録する（width_survivor_collect.mjs の survPats を unique 化すれば正しく 10）。

## REST16 再検査・実在性スキャン（width86_realizability_scan.mjs）

- REST16（16法）再検査: 10パターン全て allPass。
- 11050円直接検証: 10窓すべて points=34・行集合 equalsPattern=true。
- R' ≤ 1e6（1,964円・3形式 oo/it/mx）孤立性スキャン: 10パターンすべての realizer は **R'=5525 のみ**（control-11050、form oo）。他の R' による実現は 1e6 以下に存在しない。

### スキャン check の修正（w84/w85 版からの重要な変更）

旧 width84/85_realizability_scan.mjs の check は「窓先頭行 = 候補キー L 自身」を仮定しており、pattern[0] > 0 の窓（窓開始 x が円の行でないアラインメント）を数え落とす under-approximation だった。本版は窓開始 A = k0 − 2·pat[0] を全キーから試す修正 check を使用。修正版で **w84 生残4・w85 生残6 も再スキャン**した結果:

- w84: 4/4、w85: 6/6 とも realizer は 5525 のみ、他の R' ≤ 1e6 による実現なし。
- すなわち旧版の結論（5525 のみが realizer）は修正後も不変。数え落としは実在性の取りこぼし（偽陰性）方向のみで、過大主張は生じていなかった。

## 結論

- 予測「w86 ユニーク生残 ≥10・全て census 窓で実現・phantom 0」は**完全に的中**（ちょうど10）。
- 生残行集合の構造会計: 10生残 = 11050円の86幅34点窓 census 10窓と1:1。実在性は 11050円で直接証明済み、孤立性は R' ≤ 1e6 で数値的に裏付け。
- protocol 注記: aborted chunk 境界での leaf 二重計上が起こりうる。生残数の正確な値は survPats の unique 化で読むこと。

## 関連ファイル

- `research/experiments/width69-84-sweep-20261114/output/state_w86.json`（掃引 state・survPats 収集版）
- `scripts/width86_realizability_scan.mjs`（本実験のスクリプト・修正 check）
- `output/width86_positive_control.json`（REST16・witness・scan・w84/w85再スキャン出力）
- `research/log/2026-11-14-width86-positive-control.md`
