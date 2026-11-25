---
id: K0824
title: 任意底面の高次元平行列盤は超平面跡容量ゲームへ厳密縮約される
kind: proposition
status: proved
topics: [variants, geometry, grundy]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 安全な追加だけを合法手とする通常プレイの規則
- type: generalizes
  target: K0352
  note: K0352の一般位置底面に限らず任意の有限底面で占有ベクトル縮約が成立する。K0352の閉形式分類までは一般化しない
artifacts:
- path: research/experiments/higher-dimensional-fiber-trace-reduction-20261115/report.md
  role: proof
  note: ファイバー交点数による全称縮約定理・2次元/3次元系・適用限界
- path: research/experiments/higher-dimensional-fiber-trace-reduction-20261115/verify_small_instance.py
  role: verifier
  note: 共線な底面点を持つ2例で全セル配置を直接幾何・Grundy再帰と照合
- path: research/experiments/hyperplane-trace-enumeration-20261115/report.md
  role: proof
  note: 任意有限底面の超平面跡が高々d−1点のアフィン基底から列挙でき、個数がO(w^(d−1))となる全称補題
- path: research/experiments/hyperplane-trace-enumeration-20261115/verify_trace_count.py
  role: verifier
  note: 有理数階数と有界整数法線列挙を用いた小規模全底面監査
- path: research/experiments/hyperplane-trace-enumeration-20261115/audit.json
  role: data
  note: 3次元までの776個の底面集合に対する有限監査集計
- path: research/experiments/fiber-trace-boundary-sharpness-20261115/report.md
  role: proof
  note: 全次元でq=2|B|における占有数縮約の失敗を示す標準単体底面の明示反例
- path: research/experiments/fiber-trace-boundary-sharpness-20261115/verify_boundary.py
  role: verifier
  note: 有理数階数と整数球面方程式で境界反例を検査する標準ライブラリのみの検証器
scope: d≥2、有限底面B⊂Z^(d−1)、w=|B|、m≥1、q>2w。盤B×{0,...,m−1}で、共通アフィン超平面または通常球面上のq点を禁止する標準通常プレイ
evidence: 全称数学的証明（各ファイバーと非平行超平面は高々1点、球面は高々2点）および超平面跡のアフィン基底による厳密列挙補題。非一般位置の4点/5点底面に対する有限完全な独立幾何・Grundy照合と、1〜3次元底面の776集合に対する有限跡監査。さらに標準単体底面によりq=2wで縮約が破れる全次元の明示反例を証明し、q>2wの一様境界の鋭さを確定
---

# 任意底面の高次元平行列盤は超平面跡容量ゲームへ厳密縮約される

## 命題・範囲

d≥2、有限集合B⊂Z^(d−1)、w=|B|≥1、m≥1とし、盤をB×{0,...,m−1}とする。相異なるq点が同一アフィン超平面または同一通常球面に載ることを禁止し、q>2wを仮定する。

底面の全アフィン超平面跡T=B∩Hに対し、列占有数c_bを用いると、安全性は

\[
\sum_{b\in T}c_b\le q-1
\qquad(\forall T\in\mathcal T(B))
\]

と同値である。合法手は占有ベクトルcの一成分を1増やす操作に一致し、同じcを持つ全セル配置は同じGrundy値を持つ。従ってゲームは高々(m+1)^w個の占有ベクトル状態へ厳密縮約される。

## 証明と系

長軸に平行でない超平面は各ファイバーと高々1点、通常球面は各ファイバーと高々2点で交わる。q>2wにより、禁止q点組を含めるのは長軸に平行な超平面だけである。それらはH×Rの形で、盤内の石数は対応する超平面跡T上の占有数の和になる。これで安全性と合法手の記述が従い、Grundy値の一致は同じ占有ベクトルからの子ベクトル集合が同一であることから帰納的に従う。

d=2では超平面跡は単元集合だけなので独立な行容量ゲームとなり、
g(S)=(w min(m,q−1)−|S|) mod 2、M=q−1。
d=3では底面の共線部分集合を制約集合とする平面上の列占有ゲームに落ちる。一般位置底面ではK0352の全(d−1)部分集合容量ゲームを回収するが、任意底面で同項目の閉形式Grundy分類までは主張しない。

## 超平面跡の個数と列挙

ここでの跡族の大きさ自体にも、次元だけで決まる多項式上界がある。r=d−1 と置き、

\[
\mathcal T(B)=\{B\cap H:H\text{ は }\mathbb R^r\text{ のアフィン超平面}\}
\]

とする。このとき、全ての有限 B⊂R^r（r≥1）について

\[
\boxed{
\mathcal T(B)=\{\varnothing\}\cup
\{B\cap\operatorname{aff}(A):
 A\subseteq B,\ 1\le |A|\le r\}
}
\]

が成立する。従って

\[
\boxed{
|\mathcal T(B)|\le
\sum_{i=0}^{r}\binom wi
=O_r(w^r)=O_d(w^{d-1}).
}
\]

まず T=B∩H が空でない跡なら、T のアフィン包の次元は高々 r−1 である。そのアフィン基底 A⊂T は高々 r 点からなり、aff(A)=aff(T)⊂H なので

\[
T\subseteq B\cap\operatorname{aff}(A)
\subseteq B\cap H=T.
\]

よって T=B∩aff(A) となる。

逆に 1≤|A|≤r を取る。L=aff(A) の次元は高々 r−1 である。dim L=r−1 なら L 自身が超平面である。dim L≤r−2 なら、L を含む超平面の法線ベクトル全体の中から、有限個の b∈B\L について b も含んでしまう条件を避けて選べる。各 b が除くのは法線空間の真部分空間であり、有限個の真部分空間の和は無限体上の法線空間全体を覆わない。従って L を含み B\L の点を一つも含まない超平面 H が存在し、B∩H=B∩L となる。空跡も有限 B を避ける超平面で実現できる。これで等式を得る。

したがって跡族は、サイズ高々 d−1 の部分集合 A を列挙し、B∩aff(A) を厳密な有理数階数で計算して重複を除けば全て生成できる。候補数は O_d(w^{d−1})、各候補で w 点の所属を調べるため、固定 d では O_d(w^d) 回の定数次元階数判定で制約族を構成できる。K0824の q>2w の範囲では、この跡族が占有ベクトルゲームの全制約である。これは制約表現の大きさの改善であり、状態数上界 (m+1)^w やGrundy計算全体の多項式時間化を主張しない。

## q=2w 境界の鋭さ

仮定 q>2w は、任意の有限底面に一様に適用する条件として境界まで鋭い。r=d−1≥1 とし、

\[
B=\{0,e_1,\ldots,e_r\}\subset\mathbb Z^r,
\qquad w=r+1,
\qquad m=2,
\qquad q=2w=2r+2
\]

と置く。B は r 次元のアフィン単体の頂点なので、どのアフィン超平面も B の高々 r 点しか含まない。各列を2点ずつ占有するベクトル c_b=2 は、全ての超平面跡 T について

\[
\sum_{b\in T}c_b=2|T|\le2r=q-2\le q-1
\]

を満たす。従って底面超平面跡の容量条件は、この占有ベクトルを安全と判定する。

しかし盤上の全点 B×{0,1} は、通常球面

\[
\sum_{j=1}^{r}(x_j-\tfrac12)^2
 +(z-\tfrac12)^2=\frac{r+1}{4}
\]

上にある。実際、各座標 x_j と z は0または1なので、左辺の各項は1/4である。点数は |B×{0,1}|=2(r+1)=q。従って実際の配置は共球 q 点を含み、安全ではない。

よって q=2w では、超平面跡の占有数だけによる縮約は一般には成立しない。この反例は全ての d≥2 に対して与えられ、K0824の一様な仮定 q>2w は等号境界でこれ以上弱められない。これは各個別の底面で q>2w が常に必要という意味ではない。標準整数行に追加の合同式構造を使う K0072 の q=2w 結果とも矛盾しない。

## 根拠と限界

全称性はファイバー交点数による証明。非一般位置の2例で、全4096配置および全1,048,576配置の直接階数判定と占有ベクトル判定が一致し、全安全配置のGrundy値も一致した。例2では縮約後2,935状態で、直接1,042,005状態の再帰を再現し、Grundy 2・3も出現した。有限検査は証明の代用ではない。

q≤2wでは非平行超平面や球面が禁止点数に達し得るため適用しない。任意底面の超平面跡容量ゲーム自体の閉形式分類は未解決である。

## 高さ対和が一意な場合の等号境界

高さ集合Aを、異なる2点の和が一意な有限集合へ広げると、q=2wの境界でも縮約が正確となるための必要十分条件を完全に記述できる。失敗するのは底面Bが全次元を張り、かつ共球面である場合に限る。標準連続高さではm=2,3が該当する。m=4では高さ対の和が衝突し、非共球面の底面でも縮約が破れる反例がある。詳細は[K0828](K0828-sidon-height-boundary-reduction.md)。
