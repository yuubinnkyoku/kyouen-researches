---
id: K0690
title: 任意rankの禁止集合ゲームは合法点が五個以上ならGrundyが合法点数より二以上小さい
kind: proposition
status: proved
topics: [grundy, residual-games, search-methods, variants]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常ゲームのmex定義
- type: depends_on
  target: K0108
  note: 安全局面の極小残余禁止族への帰着
- type: depends_on
  target: K0686
  note: 六点でg4、七点でg5を達成し二段差の鋭さを示す
artifacts:
- path: research/experiments/legal-count-grundy-gap-two-20261108/proof.md
  role: proof
  note: 五点以下の完全基底と合法点数についての全称帰納
- path: research/experiments/legal-count-grundy-gap-two-20261108/audit.py
  role: verifier
  note: 二方式全clutter生成、Python残余mexとC++生subsetの比較
- path: research/experiments/legal-count-grundy-gap-two-20261108/output/audit.json
  role: data
  note: 全7020族と116416安全状態の比較、五点までの全ヒストグラム
- path: research/log/2026-11-08-grundy-mobility-gap-and-hyperforests.md
  role: log
  note: 五点完全表から点数無制限の定理へ進めた経緯
scope: 固定禁止集合の完成を不合法とする任意有限集合上の一点追加通常ゲーム。現在合法点数μ>=5、rank・辺数・点数は任意。標準q4共円ゲームの全安全局面を含む。
evidence: 全rankの1..5点clutter7020族を二生成法と二Grundy計算で照合。五点最大値3を基底に、一手で合法点数が必ず減ることとmexで全点数へ帰納。
---

任意の安全局面で現在合法な点数をμとする。禁止集合のrankを制限せず、

\[
 \boxed{\mu\ge5\quad\Longrightarrow\quad g\le\mu-2.}
\]

μ=0,1,2,3,4の最適上界は順に0,1,1,2,3。
全rankの五点clutter6894族の最大値は3で、全7020小族・116416安全状態を
二つの生成法とPython/C++で照合した。
μ≥6では子の合法点数m≤μ−1。m≥5なら帰納仮定で子値≤μ−3、
m≤4でも子値≤3≤μ−3となり、mex≤μ−2。

この全称命題は有限基底を持つ計算機援用証明である。
標本から未計算の点数を推測したものではない。
六点g=4・七点g=5はK0686で達成され、μ=5..7の上界は鋭い。
一般の禁止集合ゲームでg=0..5の最少合法点数は **0,1,3,4,6,7**。

K0041の最大残手数上界h_remainingも使うなら、μ≥5で
g≤min(h_remaining,μ−2)を得る。共有solverへの実装や速度改善は未主張。
[証明・再現資料](../../experiments/legal-count-grundy-gap-two-20261108/proof.md)を参照。
大きいμでの鋭さ、標準全正方形格子盤での等号達成、世界初性は確定していない。
