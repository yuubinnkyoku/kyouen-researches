---
id: K0536
title: λ=0・各列m候補の任意w列盤で実現可能な終局石数の集合を完全分類
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe, rectangles, grundy]
aliases: []
relations:
- type: depends_on
  target: K0533
  note: 四点の列分布と三点補間の禁止高さ数評価を全終局サイズへ拡張
artifacts:
- path: research/experiments/quadratic-zero-terminal-spectrum-20261024/proof.md
  role: proof
  note: 任意w,mの必要十分条件、整数点での明示構成、最小非三石終局の公式
- path: research/experiments/quadratic-zero-terminal-spectrum-20261024/construct.py
  role: verifier
  note: 明示整数構成の全安全四点と全空候補への禁止証人を独立行列式で検査
- path: research/experiments/quadratic-zero-terminal-spectrum-20261024/results.json
  role: data
  note: 幅3〜9の147構成と既存全局面検査の終局サイズ必要条件監査
scope: w≥3本の相異なる鉛直列、各列ちょうどm≥2個の任意実数候補点を持つ盤全体に対する存在分類。四点のdet[x²,x,y,1]=0を禁止する通常プレイ。
evidence: 全称的な補間数上界と、全可能サイズを整数座標で与える明示構成による数学的証明。有限147構成の検算は実装監査。
---

# 任意候補のλ=0列盤で実現できる終局サイズ

`B_r=(r−2)(r−3)(r+2)/6` とする。
各列ちょうどm点のw列盤の**どれか**で、r石の極大安全配置が存在する必要十分条件は

`r∈({3} if m≥3) ∪ {r:4≤r≤w, m≤B_r} ∪ {w+1}`。

各可能サイズは整数座標でも実現する。ただしサイズごとに盤は変わってよく、
一つの固定盤に全サイズが同時に現れるという意味ではない。

必要性は、一石列だけの場合と二石列一つの場合の両方に対する三点補間数の上界。
十分性は、既存列への追加を3+1・2+2型で塞ぎ、空列の候補を相異なる補間高さから選ぶ整数構成。
支配項を保証する明示的な大きさの整数基数で構成でき、座標探索は不要である。

`h(m)=min{r≥4:B_r≥m}` とすれば、一列三石以外の終局の、盤の選び方を含む最小石数は
厳密に `min(w+1,h(m))`。幅が十分ならΘ(m^(1/3))となる。

固定標準格子の個別サイズ集合や、その全局面の勝敗・Grundy分類は別問題。
候補が各列少なくともm点という条件では、m=2でも三点列を選べるため三石の条件が変わる。
本項の完全な集合公式は**各列ちょうどm点**に対するものとして解釈する。
