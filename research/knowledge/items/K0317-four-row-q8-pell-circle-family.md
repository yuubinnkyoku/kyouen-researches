---
id: K0317
title: 四連続整数行を2点ずつ通る8点円には無限Pell族がある
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: supports
  target: K0077
  note: 4×m・q=8では非局所円が無限に現れても早い安定化と両立する
artifacts:
- path: research/experiments/fixed-width/reports/q48-pell-circle-family.md
  role: proof
  note: Pell方程式による無限構成と最初の非局所例の証明
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/output/q48_pell_family.json
  role: data
  note: 最初の例と有限検算
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/scripts/q48_pell_family.py
  role: verifier
  note: Pell再帰・座標・円方程式・行列式の再現検査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/reports/q48-pell-foliation-two-new-families-20261015.md
  role: proof
  note: 既知の二つの新型から異なる傾きのPell無限族を構成
- path: research/experiments/fixed-width/scripts/q48_pell_foliation_20261015.py
  role: verifier
  note: 二族の正規形、Pell反復、円方程式、全四点行列式を整数検査
- path: research/experiments/fixed-width/reports/q48-circle-gap-2000000-20261015.md
  role: proof
  note: 最大弦長2000000までの11型の有限完全分類
- path: research/experiments/fixed-width/output/q48_circle_census_2000000_20261015.csv
  role: data
  note: 200万上限の完全列挙で得た弦長型
- path: research/experiments/fixed-width/scripts/q48_circle_census_increasing_ab_2000000_20261015.cpp
  role: verifier
  note: (d0,d1)から行う独立整数全列挙
- path: research/experiments/fixed-width/scripts/q48_circle_census_increasing_ac_2000000_20261015.cpp
  role: verifier
  note: (d0,d2)から行う独立整数全列挙
- path: research/experiments/fixed-width/reports/q48-mod27-chord-classification-20261015.md
  role: proof
  note: 法27の全称必要条件と最大弦長300万までの有限完全分類
- path: research/experiments/fixed-width/scripts/q48_mod27_circle_census_20261015.cpp
  role: verifier
  note: 最大弦長300万までの剰余篩付き完全列挙
- path: research/experiments/fixed-width/scripts/q48_bc_independent_20261015.cpp
  role: verifier
  note: 中央二弦長から行う独立列挙、250万まで照合
- path: research/experiments/fixed-width/output/q48-patterns-B3000000-20261015.csv
  role: data
  note: 最大弦長300万の有限列挙結果
---

# 四連続整数行を2点ずつ通る8点円には無限Pell族がある

Pell方程式
`u^2-10v^2=1`
の解から、四連続整数行を各2格子点ずつ通る円を無限に構成できる。半径と必要列数は無限に増える。

この族で最初の非局所的な8点円が盤内に全て現れるのは4×74で、8点中7点を含める最小盤は4×69。これらの「最初」は弦長の有限完全分類で確認されている。

従って4行盤では、十分長くしても局所円以外が消えるわけではない。K0077の早い安定化M_{4,8}=11は、円型そのものの消滅ではなく、少数石から塞げる点数の上界によって成立する。

## Additional exact finite circle census (2026-10-14)

The complete integer-chord enumeration through maximum horizontal span 2773 finds exactly five patterns: (1,3,3,1), (35,51,63,73), (73,63,51,35), (1331,1935,2391,2773), and (2773,2391,1935,1331). Consequently, for every 1 <= m <= 2774 the exact number of eight-point circles on four consecutive rows is max(0,m-3)+2*max(0,m-73)+2*[m=2774]. In particular, the second Pell-family circle at width 2774 is the first new type after width 74; no intermediate types occur. The total number of forbidden eight-point subsets is 4*binom(m,8) plus this circle count. This is a finite complete classification, not an unbounded classification of all circles.

Proof and two independent integer enumerators: research/experiments/fixed-width/reports/q48-circle-gap-2774-20261014.md, research/experiments/fixed-width/scripts/q48_circle_gap_2774_20261014.py, and research/experiments/fixed-width/scripts/q48_circle_gap_2774_independent_20261014.cpp. The original infinite Pell-family theorem above is unchanged.

## 1000001列までの有限完全分類（2026-10-15）

整数弦長の平方数条件を二つの異なる変数対で完全列挙した結果、`1<=m<=1000001` で4行8点円の弦長型は7種類のみである。既存の5型のほかは `(50543,73479,90795,105301)` とその上下反転であり、**105302列の次の新型は1000001列まで出現しない**。

この範囲での円数は、`[x]_+=max(0,x)` として
`C8(m)=[m-3]_+ + 2[m-73]_+ + 2[m-2773]_+ + 2[m-105301]_+`。
1000001列で `C8=6783710`。法4032と法2016の平方剰余必要条件でそれぞれ枝刈りした独立C++全探索が、最大弦長1000000まで全7型で一致した。数学的な整数弦長への還元と独立検証の詳細は `research/experiments/fixed-width/reports/q48-circle-gap-1000000-20261015.md`、再現コードは同ディレクトリの `scripts/q48_circle_census_mod4032_20261015.cpp` と `scripts/q48_circle_census_ac_mod2016_20261015.cpp`、結果は `output/q48_circle_census_1000000_20261015.json` を参照。

## 2000001列までの有限完全分類（2026-10-15）

最大弦長2000000以下では、局所型 `(1,3,3,1)` と増加5型およびその上下反転の計11型に限る。増加型の初出盤長は74、2774、105302、1067654、1893728列である。したがって

`C8(m)=[m-3]_+ + 2[m-73]_+ + 2[m-2773]_+ + 2[m-105301]_+ + 2[m-1067653]_+ + 2[m-1893727]_+`

は `1≤m≤2000001` で厳密。最大弦長2000000までの `(d0,d1)` 列挙と `(d0,d2)` 列挙が11型で一致し、別の整数座標復元検査も全770個の四点行列式を照合した。

## 3000001列までの追加有限監査（2026-10-15）

法12096の平方剰余篩を使う完全列挙では最大弦長3000000まで新型はなく、同じ11型だけだった。異なる `(d1,d2)` 列挙との照合は250万まで、100万では従来の法4032走査とも一致した。300万上限の分類は有限計算であり、3000002列以上の新型不存在を主張しない。

## 追加の無限Pell族（2026-10-15）

有限分類で得た弦長型 `(445465,715719,908883,1067653)` と `(98119,1096275,1547259,1893727)` は既存の `9/1` 傾きと異なる `47/6`、`53/12` の傾きを持ち、それぞれ別の無限Pell族を作る。具体族の正値・奇数性・単調性は整数Pell変換で全世代について示されている。任意の非局所円が無限族へ延長するという、より強い全称命題はK0431に分けて記録する。
