---
id: K0683
title: rank3以下の全残余clutterは整数共円残局に普遍実現でき、rank4では5点2辺の最小障害がある
kind: proposition
status: proved
topics: [geometry, residual-games, grundy, variants]
aliases: []
relations:
- type: generalizes
  target: K0681
  note: 三点辺1本から任意個数の二点・三点辺の同時実現へ拡張
- type: depends_on
  target: K0438
  note: 有理円の有限除外による二点禁止辺の整数実現
- type: depends_on
  target: K0108
  note: 全残余禁止族による継続ゲームDAGの一致
artifacts:
- path: research/experiments/rank-three-residual-universality-20261107/proof.md
  role: proof
  note: 将来の三点円も避ける全称構成・多項式ビット長・rank4障害の最小性
- path: research/experiments/rank-three-residual-universality-20261107/verify.py
  role: verifier
  note: 全4点以下clutter125件と大きい5例の有理構成、独立整数4×4行列式と全安全mex照合
- path: research/experiments/rank-three-residual-universality-20261107/output/audit.json
  role: certificate
  note: 130整数盤の座標、占有集合、意図した禁止四点組と検査集計
- path: research/experiments/tree-triple-broom-periodicity-20261107/verify_geometry.py
  role: source
  note: 再利用した既存有理円ヘルパーと独立整数Leibniz検算器
- path: research/log/2026-11-07-rooted-core-and-rank-three-universality.md
  role: log
  note: 三点辺の同時実現で必要になった将来円除外とrank境界の発見
scope: 任意n>=1個の合法候補点と、辺サイズ2または3の任意有限clutter。標準q=4・完全指摘・通常プレイ、指定有限整数点盤と安全占有集合。rank4不可能性は任意実数座標でも成立。
evidence: 有理円の有限除外と将来円回避による全称構成。三点が定める唯一の一般化円によるrank4障害の全称証明。全130整数盤・27073四点・1295安全局面の独立監査。
---

## rank3までの普遍実現

n個の合法候補点上の包含極小禁止族Fを任意に取る。辺サイズは2または3、
各辺数をm₂,m₃とする。この残余ゲームを

\[
 \boxed{n+2m_2+m_3\text{ 個の整数点と }2m_2+m_3\text{ 石の安全局面}}
\]

で全状態実現できる。合法点はちょうどn個、残余禁止族はFそのもの。
全継続局面の合法手・Grundy値・勝敗が一致する。
構成時間は多項式、一座標のビット長はM=n+2m₂+m₃としてO(M log M)。

候補点は正の放物線上に置き、各三点辺の有理円を全て先に固定する。
各円の錨点を選ぶとき、既存三点による余分な四点だけでなく、
**将来に処理する三点円との交点も避ける**。
これで全三点円に既存の余分な錨点が載ることを防ぎ、三点辺を任意個数同時に作れる。
続いて各二点辺の円に錨点2個を置き、全錨点を占有して整数化する。

## rank4では普遍実現できない

5合法点上の目標F={0123,0124}は実現不可能である。
共有三点012が唯一の円または直線を定めるので、五点全てが同じ一般化円上に載り、
残りの四点組0134,0234,1234も強制的に禁止される。
追加の占有石を使っても、残余四点辺は既に候補四点だけで満杯なので回避できない。

この障害は**合法点数5、辺数2の双方で最小**。
4点以下で四点辺を持つclutterは四点全体を唯一の辺にするものだけで円上に実現できる。
一辺だけの族も、その辺を円上に置き、他の孤立点を有限除外で追加すれば実現できる。
したがって全clutterの無条件実現という意味で、rank3は鋭い境界となる。

## 根拠と検証境界

[全称構成・ビット長・不可能性証明](../../experiments/rank-three-residual-universality-20261107/proof.md)を保存。
4点以下の全125clutterと大きい5例について130整数盤を構成し、
全27073四点を別の整数4×4行列式で検査、全1295安全局面のGrundyも独立照合した。
将来円に既存点が入らない帰納的不変条件も各段階で検査する。

盤は指定した有限点だけからなる。周囲の全格子点を含めた標準正方形盤の実現や、
11×11の勝敗への主張は含まない。
