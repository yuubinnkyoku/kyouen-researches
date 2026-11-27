# 2026-11-27 (6,7) 前線 6x22 two-edit surgery — 単一オーナー宣言 (publish-then-execute)

宣言時 HEAD: `8170398137fa74710e9b5fb44fb6a8c596f839b8`。

## 主題

- **(6,7) 6x22 q=7 row-deficient witness の two-edit surgery**。
  種 = K0815 第7弾の 6x21 witness（35石・rows [6,6,5,6,6,6]・
  `research/experiments/six-row-q7-m21-class-split-20261114/output/w67_21.json`
  sha256 `5f01a133ab2d51ef1a02506ef3be8f655c2cf2e46e548bc77dc08603a3203168`・出版正本）。
- 6x21 witness の 6x22 ボードでの未遮断セルは **T=(21,2) のみ**（一石不足構造・本宣言で機械再確認）。
  T-curve census c4=3・c5=1（遮断閾値 6・row-2 直線 y=2 が 5石 T-curve）。
- 探索: S' = seed - R + A（|R| <= 2・|A| <= 2・最終サイズ <= 35・A は空セル・
  T 占有または T 遮断）の完全列挙。SAT なら 6x22 witness で M_{6,7} lower 22 -> 23。
  全候補棄却なら局所的負（不在主張ではない）。class {2} kissat 280s 5,038,264
  conflicts INDET (K0815) に代わる solver-free ルート。

## 器具

- `surgery_general.py`（本日出版 `six-row-q6-m26-two-edit-surgery-20261127` kit の
  Q・盤面汎化エンジン・q=7 は閾値だけの差: 安全 7・遮断 6・T-curve c in {4,5}）。
  較正は 7x32 q=6 出版 m32 surgery の完全再現で実施済みの同一 byte
  （engine sha256 は kit MANIFEST に pin）。

## 正直な開示

- 宣言出版前に予備 probe（未遮断セル特定・予備列挙 692,655 候補）を実行済み。
  公式記録 run（決定性 2 走・独立 spot-check・tamper）は宣言出版後に実施。
- m=20 witness (w67_20.json) からの rediscovery 陽性対照は最小 sd=40（>=20 手）で
  不成立（K0815 非同型観察と整合）。

verdict 不消費。11x11 空盤・root・closure class は全時点 UNKNOWN。
