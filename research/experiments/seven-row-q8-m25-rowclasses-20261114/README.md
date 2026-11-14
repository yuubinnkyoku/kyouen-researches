# seven-row-q8-m25-rowclasses-20261114

(7,8) witness 前線 7×25 の row 分解スイープ。K0825 は m=25 を rowY=3 分解のみ試して
250s cap で INDET（3,534,747 conflicts）と記録し、「他の3行クラスは未走査」と残していた。
本実験は V-鏡映で正規化した残り 3 クラス rowY ∈ {0,1,2} を同条件（genfast CNF + kissat 4.0.4・240s cap）で走査した。

## 手法

K0825/K0820 と同一: `scripts/genfast.js`（q=8=w+1 で適用可・K0825 が sat2.js とバイト一致再検証済み）の
`--deficient --rowY=Y` rowfixed 符号化。行 Y を欠損行と固定しても ∃行欠損の完全性は保たれる
（∀行の OR を Y=0..6 で列挙しており、V 対称で {0,1,2,3} が代表）。
`scripts/leanrow.sh` が1クラス1コマンドで CNF 生成 → kissat 240s → 記録（SAT なら decode + dual verify）。

## 較正（instance identity）

- (7,24,8) rowY=3 再生成: kissat **SAT 641,005 conflicts** — K0825 row-split record と bit-exact
  （`output/controls/s7x24q8_rowY3.kissat.txt`）。ツールチェーンが同レーンの実例を再現することを確認。

## 結果（正直な負記録）

7×25 q=8 の全4鏡映クラスが 240-250s cap で未決着（INDET）:

| rowY | conflicts | 判定 |
|---|---|---|
| 0 | 3,440,713 | INDET (240s) |
| 1 | 3,541,875 | INDET (240s) |
| 2 | 3,577,791 | INDET (240s) |
| 3 (K0825) | 3,534,747 | INDET (250s) |

クラス間の抵抗はほぼ一様（3.44M..3.58M）。**不在の主張ではない**（m=24 は同分解で 641k conflicts SAT）。
7×25 の決着には更なる予算（推定 ≫3.6M conflicts）か符号化改良が必要。M_{7,8} ∈ [25,651] 不変。
