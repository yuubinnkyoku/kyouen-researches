---
id: K0690
title: 任意rankの禁止集合ゲームは合法点が五個以上なら通常値とmisère補助値がともに合法点数より二以上小さい
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
- type: depends_on
  target: K0309
  note: 五合法点以下の交換則でmisèreの有限基底を得る。六点の完全分類は純三点h3の下界にも使用
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
- path: research/experiments/misere-legal-count-gap-two-20261108/proof.md
  role: proof
  note: 終局1の補助mexにも同じ帰納を適用し、任意rankと純三点のh0..7最少点数を確定
- path: research/experiments/misere-legal-count-gap-two-20261108/verify.py
  role: verifier
  note: 残余縮約h再帰と別C++生subsetの通常/補助値比較
- path: research/experiments/misere-legal-count-gap-two-20261108/output/audit.json
  role: certificate
  note: 全小型と全達成例7037根・117656安全状態で両値一致
scope: 固定禁止集合の完成を不合法とする任意有限集合上の一点追加ゲーム。現在合法点数μ>=5、rank・辺数・点数は任意。gは通常Grundy、hは終局1のmisère補助mex。標準q4共円ゲームの全安全局面を含む。
evidence: 全rankの1..5点clutter7020族を二生成法と二Grundy計算で照合。五点最大値3を基底に全点数へ帰納。hはK0309の小型交換則を基底に同様に帰納し、全小型と最少点数達成例7037根を別C++でも検査。
---

任意の安全局面で現在合法な点数をμとする。
gを通常Grundy、hを終局1のmisère補助mexとする。禁止集合のrankを制限せず、

\[
 \boxed{\mu\ge5\quad\Longrightarrow\quad g\le\mu-2,\quad h\le\mu-2.}
\]

μ=0,1,2,3,4の通常値gの最適上界は順に0,1,1,2,3。
全rankの五点clutter6894族の最大値は3で、全7020小族・116416安全状態を
二つの生成法とPython/C++で照合した。
μ≥6では子の合法点数m≤μ−1。m≥5なら帰納仮定で子値≤μ−3、
m≤4でも子値≤3≤μ−3となり、mex≤μ−2。

この全称命題は有限基底を持つ計算機援用証明である。
標本から未計算の点数を推測したものではない。
六点g=4・七点g=5はK0686で達成され、μ=5..7の上界は鋭い。
一般の禁止集合ゲームでg=0..5の最少合法点数は **0,1,3,4,6,7**。

補助値hのμ=0..5の最適上界は1,0,1,2,3,3。
K0309の交換則と上の基底から得て、μ≥6では同じ子点数帰納でh≤μ−2となる。
終局h=1は基底で扱い、非終局だけにmex帰納を適用する。
空点集合を許すと、h=0..7の最少合法点数は
**1,0,3,4,6,7,8,9**。純三点禁止族に限ると **1,0,6,7,6,7,8,9**。
全達成例のh自体を残余再帰と別C++で検査しており、通常値だけから推測していない。
[misère拡張の証明と監査](../../experiments/misere-legal-count-gap-two-20261108/proof.md)を参照。

K0041の最大残手数上界h_remainingも使うなら、μ≥5で
g≤min(h_remaining,μ−2)を得る。共有solverへの実装や速度改善は未主張。
[証明・再現資料](../../experiments/legal-count-grundy-gap-two-20261108/proof.md)を参照。
大きいμでの鋭さ、標準全正方形格子盤での等号達成、世界初性は確定していない。
hは直和のSprague–Grundy値ではなく、xor合成はしない。
