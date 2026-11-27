# 2026-11-27 (7,6) 前線 7×32 two-edit surgery 負 (高速レーン)

単一オーナー宣言
[2026-11-27-seven-row-q6-m32-two-edit-surgery-declaration](2026-11-27-seven-row-q6-m32-two-edit-surgery-declaration.md)
(宣言時 HEAD `d108bae0`・出版 `6070fb03`)の下で実行。実験キット:
[seven-row-q6-m32-two-edit-surgery-20261127](../experiments/seven-row-q6-m32-two-edit-surgery-20261127/)。

## 結果

- **7×32 完全 two-edit surgery 負**: m=31 witness (34 石) を種に
T=(31,3) 遮断の完全最終状態場合分けで **2,224,675 一意候補・
safe かつ maximal 0 件**。m=31 witness の ≤2 編集近傍に 7×32 witness なし
(局所的負・不在主張ではない)。
- m=29→30 と同一の one-stone-short 負パターン。m=30 の場合はこの負の後に
class {3} SAT (2,670,296 conflicts/497s) が witness を発見した。7×32 では
本 sandbox の実行制約 (bash call ~290s・bg process は call 終了で kill) で
同等の深さに到達できなかった:
  - (7,32,6) class {3} plain CNF 156,185 変数/547,944 節 (md5 bc10c516…) 生成済み出版。
  - (7,32,6) class {3} krow=3:4 minpos=0: INDET 1,240,713 conflicts/260s。
  - 較正 (7,31,6) class {3} krow=3:4 (SAT 既知): INDET 1,279,251/250s。
    m=31 plain は出版どおり INDET 4,368,709/896s。
- **M_{7,6} ∈ [32, 862] 不変・前線 7×32 のまま**。CSV (7,6) 行 note 追記済み。

## 検証 (詳細は kit README)

- m=31 陽性対照: 出版 surgery_m31.py byte-clone + 出版 seed で出力 JSON が
出版 surgery-m31.json と byte-identical (候補 2,140,633・safe 1・witness 1)。
- 決定性 2 走 byte 同一 (sha256 5867e7de…)。
- probe/det/CNF 較正 3 点すべて出版値再現
((7,31,3) class{3} CNF md5 48eb715f… 含む)。

## 正直な開示

- 宣言後の実行。seed・検証器・符号器はすべて main から fetch した出版 byte
(pin: sat3.js md5 d03f908e…・sat2.js 282ae832…・sat.js 0cc6021a…・
kissat md5 3a5eba83…)。
- kissat の深い単一実行は本環境では不可能 (bg process は bash call 終了で
kill されることを実測確認・log 凍結 29.97s で検知)。長時間 cap が使える
次の実行環境で (7,32,6) class {3} (krow/minpos 分割含む) の決着を推奨。
- verdict 不消費。11×11 空盤・root・closure class は全時点 UNKNOWN。
nodes/conflicts/candidates は bookkeeping。

## 次の実行可能課題

1. **(7,32,6) class {3} SAT** (長時間 cap 環境・CNF 出版済み)。SAT なら
witness 帯 m=6..32・M_{7,6} ∈ [33, 862]。
2. 3 編集 surgery (five-row lane の surgery4.js deficit-curve 方式の 7 行移植)。
3. 他前線: (4,5) 4×24 class-split (m=23 完了・M=21 or ≥25 からの次步)。
