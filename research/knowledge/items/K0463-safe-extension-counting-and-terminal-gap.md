---
id: K0463
title: 任意有限整数点盤の安全延長・終局計数は#P完全で極大長差は無界
kind: proposition
status: needs-review
topics:
- geometry
- variants
- maximal-safe
- maximum-safe
- residual-games
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0348
  note: 任意グラフを三共線なしの整数円禁止4点組に多項式長で符号化する構成
artifacts:
- path: research/experiments/game-structure/reports/safe-extension-complexity-20261019.md
  role: proof
  note: 独立集合多項式への全単射、終局数の#P完全性、星による極大長差の無界証明
- path: research/experiments/game-structure/scripts/verify_safe_extensions_20261019.py
  role: verifier
  note: 汎用整数4×4行列式と全延長の照合
- path: research/experiments/game-structure/scripts/independent_safe_extensions_20261019.cpp
  role: verifier
  note: 独立C++円方程式判定と全延長の照合
- path: research/experiments/game-structure/output/safe_extensions_20261019.json
  role: data
  note: 全95盤、15590四点組、2284候補集合の監査集計
scope: 二進整数座標で与える任意有限点盤と指定安全局面。全禁止4点組が同一の点を通る円で、三共線がなくても成立。標準正方形全格子盤は対象外。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 指定安全局面からの全延長と独立集合の全単射

任意の有限単純グラフGをK0348の `|V|+|E|+1` 個の整数点盤に符号化し、共通点pと各辺の固有点を先に占有すると、残る安全延長はGの独立集合と一対一に対応する。追加石数ごとの分布は独立集合多項式に等しく、極大延長は極大独立集合と一対一に対応する。

したがって安全延長の総数の計算は#P完全、少なくともk石を追加できるかはNP完全。さらに、元グラフの各頂点に葉を付けた冠グラフにより、全終局の追加石数が同じでも終局数の計数は#P完全。この特殊族のGrundy値は残り手数の偶奇だけで決まる。三共線なし・円だけ・全禁止4点組がpを共有する盤にも制限できる。星K_{1,t}を使えば、同一初期局面の極大延長は1石とt石の2通りで、長さの差は任意に大きい。

全称的な証明と適用範囲は[実験報告](../../experiments/game-structure/reports/safe-extension-complexity-20261019.md)を参照。Pythonと独立C++で95盤、15,590四点組、2,284候補延長集合を完全照合した。標準n×n全格子盤の計算量や極大長差の無界性は主張しない。
