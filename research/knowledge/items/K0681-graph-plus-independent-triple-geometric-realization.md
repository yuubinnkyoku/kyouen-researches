---
id: K0681
title: 任意グラフと独立三点辺1本はn+2e+1個の整数点で共円残局として全状態実現できる
kind: proposition
status: proved
topics: [geometry, residual-games, grundy, variants]
aliases: []
relations:
- type: depends_on
  target: K0438
  note: 有理円の逐次追加による任意グラフの別構成を三点辺1本へ拡張
- type: depends_on
  target: K0108
  note: 全包含極小残余禁止集合によるゲームDAGの一致
artifacts:
- path: research/experiments/tree-triple-broom-periodicity-20261107/geometry.md
  role: proof
  note: 全グラフ・独立三点集合についての有限除外構成と多項式時間・ビット長証明
- path: research/experiments/tree-triple-broom-periodicity-20261107/verify_geometry.py
  role: verifier
  note: 有理構成と別の整数4×4 Leibniz行列式・全安全局面の照合
- path: research/experiments/tree-triple-broom-periodicity-20261107/output/geometry_audit.json
  role: certificate
  note: 全52整数盤の座標・占有集合・禁止四点・全安全局面検査集計
- path: research/experiments/game-structure/scripts/verify_graph_realization_20261019.py
  role: source
  note: 再利用する既存有理円・有理点・構成時det3ヘルパー
- path: research/log/2026-11-07-tree-triple-broom-periodicity.md
  role: log
  note: 木の三点制約族の抽象ゲームを標準幾何ルールへ移すための拡張
scope: 任意のn>=3頂点・e辺の有限単純グラフGと独立三点集合T。標準q=4・完全指摘・通常プレイ、任意有限整数点盤と指定安全占有集合。全正方形格子盤は対象外。
evidence: 正の放物線点・三点円上の有理錨点・各辺円の有限除外構成による全称証明。52整数盤・37672四点行列式・全696安全継続局面で独立監査。
---

## 全称実現定理

任意のn≥3頂点・e辺の有限単純グラフGと、独立な三頂点の集合Tに対して、
**n+2e+1個の整数平面点**の有限盤Bと、**2e+1石の安全占有集合S**を多項式時間で構成できる。
現在の合法点はちょうどn個、その包含極小残余禁止族は **E(G)∪{T}** に一致する。

従って全ての安全継続局面で合法手・Grundy値・勝敗まで一致する。
一座標当たりの二進ビット長はO((n+e)log(n+e))以下。
標準ルールの共円・共線四点禁止で成立する。

## 構成と根拠

候補頂点を正の放物線点(i,i²)に置く。四つの正パラメータの和は0にならないので共円四点はなく、
三共線もない。Tの三点を通る有理円上に錨点a_Tを追加し、T∪{a_T}だけを禁止四点にする。
他の三点が定める一般化円との交点は有限個なので、それらを避けた有理錨点を選べる。

続いて各辺uvについて、他の既存点を含まない有理円をp_u,p_vに通し、
錨点二つを有限除外で選ぶ。新しい禁止四点は{p_u,p_v,a_uv,b_uv}だけ。
全分母を払い、全錨点を占有すると所要の残余族を得る。
独立性により三点辺Tは二点辺を含まず、包含極小化後も残る。

[構成の全称証明とビット長評価](../../experiments/tree-triple-broom-periodicity-20261107/geometry.md)を参照。

## 独立有限監査と限界

n=3,4の全グラフ・全独立三点集合33条件、n=5の固定16条件、箒木3条件の計52整数盤で、
全37672四点を別実装の4×4 Leibniz行列式で検査し、意図しない禁止四点がないことを確認。
全696安全継続局面のGrundy値も別の抽象ゲームと一致した。
全座標と占有点を[証明書](../../experiments/tree-triple-broom-periodicity-20261107/output/geometry_audit.json)に保存。

これは列挙した有限点だけを盤にする実現であり、周囲の全格子点は含めない。
複数の任意三点辺の同時実現、標準全正方形格子盤のGrundy無界性や11×11勝敗は未解決のまま。
