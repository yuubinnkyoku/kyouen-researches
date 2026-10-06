---
id: K0305
title: 有限下方閉配置ゲームで全Grundy値が0/1であることと極大集合の同偶奇性は同値
kind: proposition
status: proved
topics: [grundy, variants]
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/q34-exact-threshold.md
  role: proof
  note: 例外下方閉包と偶奇尾部に使う一般補題
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 有限下方閉配置ゲームで全Grundy値が0/1であることと極大集合の同偶奇性は同値

有限の下方閉な配置ゲームでは、全局面のGrundy値が0または1だけであることと、全ての極大配置の石数が同じ偶奇を持つことが同値である。

固定幅盤の安定化後にGrundy値が残り手数の偶奇へ落ちることを、個別盤面の経験則ではなく一般原理として説明する。


## 明示式の強化

共通する極大サイズの偶奇を epsilon とする。このとき二値性だけでなく、任意の安全局面 S で g(S)=(epsilon-|S|) mod 2 が成立する。

実際、S を含む任意の極大延長 T について |T|-|S| の偶奇は epsilon-|S| に固定される。終局では g=0 なので、終局からの帰納で各手ごとに 0 と 1 が反転し、上式を得る。逆向きには、全局面で g が 0 または 1 なら mex の定義により任意の合法手で g が必ず反転する。極大局面は g=0 だから、空局面から各極大局面までの手数、すなわち極大サイズは全て同じ偶奇になる。

従って全極大配置が同じサイズである必要はなく、同じ偶奇であるだけで全安全局面の Grundy 値が明示的に決まる。
