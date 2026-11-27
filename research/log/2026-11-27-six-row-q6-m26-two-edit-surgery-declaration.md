# 2026-11-27 (6,6) 前線 6x26 two-edit surgery — 単一オーナー宣言 (publish-then-execute)

宣言時 HEAD: `76181b40d85c1bb3e72e14292d75203f6d31b71e` (2026-11-27T09:05Z 時点の main)。

## 主題

- **(6,6) 6x26 q=6 row-deficient witness の two-edit surgery**。
  種 = K1217 の 6x25 class{2} witness（29石・rows [5,5,4,5,5,5]・
  `research/experiments/six-row-q6-m25-frontier-crunch-20261122/witness/w6x25_class2.json`
  sha256 `4ec0887057b0d60397401f99a15ec43c3c61076eddd0b4e6c1fdd88fb4b4f309`・出版正本）。
- 6x25 witness の 6x26 ボードでの未遮断セルは **T=(25,2) のみ**（一石不足構造・
  crunch kit crosscheck の not-maximal (23,2) は bbox 正規化座標系の値で、
  raw 配置では (25,2)。本宣言で機械再確認する）。
- 探索: S' = seed - R + A（|R| <= 2・|A| <= 2・最終サイズ <= 29 = 行欠損要件・
  A は空セル・T 占有または T 遮断）の完全列挙。SAT なら 6x26 witness で
  M_{6,6} lower bound 26 -> 27。全候補棄却なら局所的負（不在主張ではない）。

## 器具 (fresh 実装・出版エンジンの一般化)

- `surgery_general.py`: 出版 `seven-row-q6-m32-two-edit-surgery-20261127/scripts/surgery_m32.py`
  (sha256 `fe277e8a...`) のアルゴリズムを Q・盤面汎化した fresh 実装
  （安全 q 曲線・遮断 q-1・T-curve case split c in {q-3, q-2}・Exact Fraction・self-test・chunk 対応）。
- **較正ターゲット（出版値再現）**: 7x32 q=6・T=(31,3)・m=31 witness seed で
  出版 `surgery-m32.json` (sha256 `5867e7de...`) の
  candidates 2,224,675 / safe 0 / witnesses 0 / T-curve c4=1 c3=10 を完全再現すること。

## 対照・検証計画

1. 較正 (上記)。2. 決定性 2 走 byte 同一。3. 独立 brute-force 検証器
（S' から曲線を再構成する method-disjoint 実装）による棄却 spot-check 4000 件。
4. tamper 電池（target を遮断済みセルに変更 -> fail-closed・seed 石移動 -> fail-loud・
遮断閾値緩和 -> fail-loud）。5. m=24 witness からの rediscovery 陽性対照は
最小 sd 34/36 (>=17 手) で不成立であることを開示（K1217 非合同観察と整合）。

## 正直な開示

- 宣言出版前に、器材構築・較正・予備列挙（6x26・836,890 候補・0 witness）を
  本 sandbox で実行済み。公式記録 run（決定性 2 走・spot-check・tamper）は
  本宣言の出版後に実施し、出版された kit に記録する。
- seed・出版エンジン byte・出版 surgery-m32 出力はすべて main から fetch し sha 照合済み。
- verdict 不消費。11x11 空盤・二石 root・第三手・S2・closure class は全時点 UNKNOWN。
candidates/safe/conflicts 数は bookkeeping。
