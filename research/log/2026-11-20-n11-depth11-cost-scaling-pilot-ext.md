# 2026-11-20 n11 depth-11コスト測定パイロット標本拡張

## 着手判断

単一オーナー宣言ノート（commit 742bacf75a・先行出版）に従い実施。36-root sweep本体は
掃引オーナーレーン実行中・結果未出版であり、本拡張は出版済みK1069正本の REFUTED-D10 38根から
決定論的規則（hex昇順index {0,12,24,36}）で選んだ4根のみを対象とし、他レーン作業と衝突しない。

## 入力と方法

- K1069正本（SHA-256 22953ae1…）classification REFUTED-D10 38根、index {0,12,24,36}の4根
  `00000000000000003800000008001220`（bit 5）・`00000000000000801202000000880100`（bit 8）・
  `00000000000000889042000080000000`（bit 31）・`00000010000000801202000000400400`（bit 10）。
- runner v17 repo原本固定コピー（git blob c132cc64…）・cap 30M・timeout 280s・両AND順序・
  pilot_d6制御必須・逐次・計16 probe。深度10と11の両方を測定。
- assemble はK1069正本を引数に取り、対象4根のmembership・分類ラベル・SHA pinを機械検証する。

## 結果（16/16完走・capped 0・error 0・gate 6/6 PASS）

| label | ordering | D10 nodes | D11 nodes | 倍率 |
| --- | --- | --- | --- | --- |
| idx0 | ac1 | 671,421 | 684,989 | 1.0202 |
| idx0 | ac0 | 815,057 | 837,946 | 1.0281 |
| idx12 | ac1 | 331,659 | 333,456 | 1.0054 |
| idx12 | ac0 | 443,007 | 445,323 | 1.0052 |
| idx24 | ac1 | 2,950,904 | 3,087,215 | 1.0462 |
| idx24 | ac0 | 638,671 | 643,518 | 1.0076 |
| idx36 | ac1 | 5,720,576 | 6,056,617 | 1.0587 |
| idx36 | ac0 | 687,760 | 702,056 | 1.0208 |

- depth-10側は8/8でREFUTED-D10分類と整合（両順序loss=false・uncapped）。D10 node数
  （331,659〜5,720,576）はここで初測定（K1069では非出版）。
- **倍率バンドは+0.52%〜+5.87%**。パイロット（1a2021979b）2根と併せて**6 root・12 probe・
  D10 331k〜14.2M nodes の帯で倍率1.0004〜1.0587**（node単位・機種非依存）。
-観察: 倍率はD10 node数が大きいrootで高め（14.2M root 1.0220、5.7M root 1.0587、0.33M root
  1.0054）の傾向があり、大型rootのdepth-11はやや不利の可能性を残余リスクとして明記。

## 供給判断への含意（提案・実行はしない)

36-root sweepが全REFUTEDの場合、当該root族のdepth-11再掃引はdepth-10掃引の概ね+6%以内の
計算量と見込まれる。ボトルネックは計算量ではなく depth-saturation の意味論と coordinator の
延長判断。ただし36 fresh witness自体は別root族であり、外挿は保証しない。

## 成果物

- `research/experiments/n11-depth11-cost-scaling-pilot-ext-20261120/`（README・scripts・output・
  runner固定コピー・生probe記録）
- 正本 `output/depth11-cost-scaling-pilot-ext-20261120.json`（SHA-256
  8a584be6a145665c6230169bdc7edb51d453e9429dafe0ab9fd8fc0e579c7aa1）は別cwd・別プロセスの
  assemble で byte-identical（2回確認）。

## 解釈規約

コスト測定のみ。行を閉じず、判定を変えず、depth-11掃引の着手宣言でもない。depth-11の
loss=falseはREFUTED-D11分類ではない。REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
