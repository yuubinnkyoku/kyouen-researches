---
id: K1375
title: PG(2,5) s=4 極大safe集合・最小2重ブロッキングの PGL(3,5) 軌道分類 (全数・計13軌道)
kind: proposition
status: proved
topics: [blocking-sets, finite-geometry, orbit-classification, pg25]
aliases: [PG(2,5) s=4 orbit census, PGL(3,5) orbits maximal safe]
relations:
- type: depends_on
  target: K1370
  note: K1370 が 2^31 全列挙で確定した個数 (13:15,500 / 14:372,000 / 15:604,500 /
    16:595,975・計 1,587,975) を完全再現し、レジューム (c)「軌道分類は未実施」を決定した。
- type: depends_on
  target: K1365
  note: 補集合双対性 (極大 safe size-k ↔ 最小 DB size-(31-k)) により、size-13..16
    の軌道構造がそのまま最小 DB 15..18 族に転写される。
artifacts:
- path: research/experiments/pg25-s4-orbit-census-20261128/README.md
- path: research/experiments/pg25-s4-orbit-census-20261128/out/orbits25s4.json
---

## 主張 (有限全数計算・PG(2,5) のみ。一般 q への外挿なし)

PG(2,5) (31点・直線長6) の s=4 極大 safe 集合 1,587,975 個は、PGL(3,5) (位数 372,000)
作用下で **ちょうど 13 軌道** に分かれる:

- size 13: 1 軌道 (15,500・安定化群 24)
- size 14: 1 軌道 (372,000・安定化群 1 = regular action)
- size 15: 5 軌道 (186,000/124,000/93,000/186,000/15,500・安定化群 2/3/4/2/24)
- size 16: 6 軌道 (186,000/124,000/3,100/186,000/93,000/3,875・安定化群
  2/3/120/2/4/96)。3,100 軌道の安定化群 120 は S5 型。

補集合双対 (K1365) により最小 2 重ブロッキング size 15..18 族も同構造。

## 有限観察 (全称主張ではない)

- line-histogram (31直線との交差 0..4 点の度数) は軌道不変量だが完全不変量ではない
  (size-15 に同一 hist [0,5,6,7,13] の別軌道対)。
- size-16 に高対称 (安定化群 120・96) の小軌道 2 つが現れる一方、size-14 は regular。
- Grundy 値は未計算 (K1370 のサイズ偶奇混在 → G≥2 示唆は現状維持)。

## 証拠

3 独立実装: (1) C DFS 全列挙 (zig cc 0.13.0・枝刈り+full-line witness・fail-closed 補集合検査)、
(2) Node.js 軌道 BFS (位数 372,000 検証・安定化群は全要素固定元計数・生成元変更で分割独立性検証)、
(3) Python アフィンモデル独立検証 (異なる点ラベリング・C 直線像の直線性 fail-closed 検査・
全 1,587,975 mask の安全性/極大性/補集合最小DB性全件 PASS・PGL(3,5) 独自再構成で
軌道再分割が JS 分類と完全一致)。較正: PG(2,3) s=2・PG(2,4) s=3 で出版値完全再現。
ダンプ sha256 pin `9af9a06a3565520c278aa1b7d91e201d10fc9d67fa366b80508dfa7f8a6dbfc8`。
経緯開示: Python 検証器の初版は無限遠点正規化の取り違えで生成群が膨張し fail-closed
的に異常終了していた (修正後は位数ちょうど 372,000)。群を使わない verify mode は無影響。

## 備考

- 仮番号 K1375 (items dir は contents API 1000件 cap で衝突 check が不完全なため、統合時再採番判定)。
- 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN・verdict 不消費。

## 追記 (2026-11-28 構造addendum)

- **orbit16-2 (3,100個・stab 120) = 「conic ∪ その内部点」**: 軌道サイズ = PG(2,5) の
  conic 総数 (372,000/120・stabilizer 計数で確認)。構成例の直線プロファイル
  {1:6, 3:10, 4:15} が軌道一意の hist と一致し、stab(S) = stab(conic) (位数 120)。
- **orbit16-5 (3,875個・stab 96) = 「三角形の辺上にない点すべて (16点)」**:
  軌道サイズ = 三角形総数 (C(31,3) − 31·C(6,3) = 3,875 = 372,000/96)。
  プロファイル {0:3, 3:16, 4:12} は任意の三角形で組合せ論的に証明済み
  (辺=0-secant・頂点通過直線=4-secant 12本・その他=3-secant 16本)・極大性も同様。
- **size-13 軌道 (15,500個・stab 24) と 4-arc**: stab(S) = stab(4-arc (frame))
  ・4-arc 総数の独立計数 15,500 = 軌道サイズと一致。S = 対角三角形 + frame + 6点軌道
  の合併 (6点軌道の幾何学は未特定・frame からの明示構成は次回課題)。
- 詳細: research/experiments/pg25-s4-orbit-census-20261128/out/structure-addendum.md
