---
id: K0688
title: 残余辺の所属被覆重みはGrundy上界を与え、固定rankでは辺数に対する線形上界が成立する
kind: proposition
status: proved
topics: [grundy, residual-games, search-methods, variants]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 有限通常ゲームのmexとGrundyの定義
- type: depends_on
  target: K0108
  note: 全残余族の継続ゲーム表現と自由点のxor分離
artifacts:
- path: research/experiments/incidence-weighted-grundy-bound-20261107/proof.md
  role: proof
  note: 安全集合の重み被覆不等式と最大残手数による全称上界、次数系と局所重み系
- path: research/experiments/incidence-weighted-grundy-bound-20261107/verify.py
  role: verifier
  note: 全7020小clutterの原始subset mex、全安全状態で残余族と有理被覆上界を再構成
- path: research/experiments/incidence-weighted-grundy-bound-20261107/output/audit.json
  role: data
  note: 非自明51244安全状態での上界・xor監査と、局所重みによる改善件数
- path: research/log/2026-11-07-pure-triple-spectra-and-incidence-bounds.md
  role: log
  note: 総辺超過量の帰納上界を考え、安全集合の重み計数で強めた経緯
scope: 任意有限点の一点追加通常ゲーム、現在合法点上のサイズ2以上の全包含極小残余辺族。rank・辺数・点数は無制限。非負被覆重みは一般実数、有限監査は有理数。
evidence: 安全集合の所属重み二重計数、Grundy<=最大残手数のmex帰納、自由点xorによる全称証明。全7020小clutterの非自明51244安全状態で完全有理数監査。
---

## 任意の所属被覆重みからの上界

非孤立な合法点の核をU、残余辺族をF、自由点数をfとする。
各辺に非負重みw_eを付け、全v∈UでΣ_{e∋v}w_e≥1を満たすとする。
C=Σ_e w_e(|e|−1)、k=⌊C⌋とすると、核のGrundy g₀と全体のgは

\[
 \boxed{g_0\le k,\qquad g=g_0\oplus(f\bmod2),\qquad
 g\le2\lfloor k/2\rfloor+1.}
\]

自由点が偶数なら全体もg≤k。
証明は、核の任意の安全追加集合Iについて
|I|≤Σ_e w_e|I∩e|≤Σ_e w_e(|e|−1)=Cであることと、
有限通常ゲームでGrundyが最大残手数以下になるmex帰納法だけによる。
重みを有理数で与えれば完全有理数で検査できる上界証拠になる。

## 次数だけから作る重みと固定rankの線形上界

T=Σ_e(|e|−1)、非孤立点の所属次数をd(v)、δ=min_v d(v)とすると、
全辺の重み1/δは被覆条件を満たす。従って

\[
 \boxed{g_0\le\lfloor T/\delta\rfloor,\quad
 g\le2\left\lfloor{\lfloor T/\delta\rfloor\over2}\right\rfloor+1.}
\]

さらに **w_e=1/min_{v∈e}d(v)** も被覆条件を満たし、その費用CはT/δ以下となる。
非一様な次数分布ではこちらの方が小さい上界を与えることがある。

最大辺サイズR、辺数hならT≤(R−1)hなので、特に

\[
 \boxed{g\le2\left\lfloor{(R-1)h\over2}\right\rfloor+1.}
\]

標準q=4の残余族ではR≤4からg≤2⌊3h/2⌋+1。
固定rankについてhに線形で、既存の辺数上界2^h−1などと小さい方を使える。
この一般評価自体の鋭さは主張しない。

## 有限監査と限界

1..5点の全rankの全7020clutterで原始占有subsetからGrundyを計算し、
各局面の合法点・残余族を再構成した。
非自明51244安全局面で、有理重みの被覆条件・核上界・自由点のxor上界が成立。
局所重みが一様次数重みを整数上界として改善した局面は10781件。

[全称証明と有限監査](../../experiments/incidence-weighted-grundy-bound-20261107/proof.md)を参照。
共有solverへの実装や速度改善、11×11勝敗はまだ主張しない。
