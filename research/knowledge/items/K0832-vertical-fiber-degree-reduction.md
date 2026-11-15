---
id: K0832
title: 垂直ファイバー補間による厳密占有縮約 — Σ min(c_b,t)≤q−1
kind: proposition
status: proved
topics: [variants, geometry, grundy]
aliases: []
relations:
- type: generalizes
  target: K0824
  note: K0824の超平面・球面に対するq>2|B|縮約を、各ファイバー上の次数が高々tである多項式超曲面へ一般化する。K0824のq=2|B|境界反例や超平面跡列挙補題を置き換えるものではない
- type: supports
  target: K0504
  note: 底面係数次数を制限しない全多項式族ではΣ min(c_b,t)≤q−1が厳密条件。K0504のdeg f≤kなど底面方向の次数制限付きグラフは別問題であり、補間多項式の底面次数は一般に|B|−1程度まで上がるため未解決
artifacts:
- path: research/experiments/vertical-fiber-interpolation-exact-20261115/report.md
  role: proof
  note: ファイバー根数上界とラグランジュ補間による最大共存数の厳密公式・ゲーム縮約・適用限界
- path: research/experiments/vertical-fiber-interpolation-exact-20261115/verify_interpolation.py
  role: verifier
  note: Fractionによる全4096配置×t=1,2,3の補間達成監査と退化ファイバー障害の確認
- path: research/experiments/vertical-fiber-interpolation-exact-20261115/output/audit.json
  role: data
  note: 12,288配置・768占有ベクトル出現の有限監査結果
- path: research/log/2026-11-15-vertical-fiber-interpolation-exact.md
  role: log
  note: K0832の一様閾値を局面ごとの厳密占有条件へ強化した判断・証明・限界
- path: research/experiments/vertical-fiber-degree-reduction-20261115/report.md
  role: proof
  note: ファイバーごとの根数上界から導く全称縮約定理・適用条件・鋭さの境界例
- path: research/experiments/vertical-fiber-degree-reduction-20261115/verify_boundary.py
  role: verifier
  note: r=1..8・t=1..8の整数単体境界例64件と、次数1..3の既約整数例を検査
- path: research/log/2026-11-15-vertical-fiber-degree-reduction.md
  role: log
  note: 最新main・未解決一覧との照合、定理の選定、有限検証と限界
- path: research/experiments/vertical-fiber-boundary-grundy-20261115/report.md
  role: proof
  note: 境界層が飽和ファイバーの鎖の直和となる全称証明と、底面跡制約付きの十分条件
- path: research/experiments/vertical-fiber-boundary-grundy-20261115/verify_boundary_grundy.py
  role: verifier
  note: 小パラメータの全境界占有ベクトルを再帰mexと排他的論理和公式で照合
- path: research/experiments/vertical-fiber-boundary-grundy-20261115/output/audit.json
  role: data
  note: 64パラメータ組・5,080境界状態の有限完全監査結果
- path: research/log/2026-11-15-vertical-fiber-boundary-grundy.md
  role: log
  note: K0832の境界層Grundy値を鎖分解で厳密化した判断・証明・限界
- path: research/experiments/vertical-fiber-t1-fixed-length-grundy-20261115/report.md
  role: proof
  note: t=1純ファイバーゲームで全終局石数がrmに固定されることから導く全局面Grundy公式
- path: research/experiments/vertical-fiber-t1-fixed-length-grundy-20261115/scripts/verify_t1.py
  role: verifier
  note: 小パラメータ100組・17,368安全状態の再帰mexと固定終局長公式の有限完全照合
- path: research/experiments/vertical-fiber-t1-fixed-length-grundy-20261115/output/audit.json
  role: data
  note: t=1全局面Grundy監査の集計結果
- path: research/log/2026-11-15-vertical-fiber-t1-fixed-length-grundy.md
  role: log
  note: 境界層からt=1全局面へGrundy公式を拡張した判断・証明・限界
- path: research/experiments/vertical-fiber-t2-q3-grundy-20261115/report.md
  role: proof
  note: t=2・q=3・|B|,|A|≥2の純ファイバーゲームにおける全安全局面Grundy分類の全称証明
- path: research/experiments/vertical-fiber-t2-q3-grundy-20261115/verify_t2_q3.py
  role: verifier
  note: 容量上限2の再帰列挙と再帰mexを用いたw,m=2..12の独立照合器
- path: research/experiments/vertical-fiber-t2-q3-grundy-20261115/output/audit.json
  role: data
  note: 121パラメータ組・9,196安全状態の有限監査
- path: research/log/2026-11-15-vertical-fiber-t2-q3-grundy.md
  role: log
  note: t=2・q=3の全分類を選定・証明・検証した判断と限界
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/report.md
  role: proof
  note: t=2,q=5,w≥3,m≥2の純ファイバーゲームにおける全安全局面Grundy値の閉形式分類とmex帰納証明
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/verify_t2_q5.py
  role: verifier
  note: ラベル付き占有ベクトルを直接列挙する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/verify_t2_q5_canonical.py
  role: verifier
  note: 正占有数の多重集合だけで独立に状態・遷移を生成する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/output/audit.json
  role: data
  note: 150パラメータ組・723,780ラベル状態・11,135多重集合状態の二方式監査集計
- path: research/log/2026-11-15-vertical-fiber-t2-q5-grundy.md
  role: log
  note: K0832の既存成果と最新mainを照合し、t=2,q=5分類を証明・独立監査した記録

- path: research/experiments/vertical-fiber-t2-q4-grundy-20261115/report.md
  role: proof
  note: t=2,q=4,w≥2,m≥2の純ファイバーゲームにおける全安全局面Grundy値の閉形式分類とmex帰納証明
- path: research/experiments/vertical-fiber-t2-q4-grundy-20261115/verify_t2_q4.py
  role: verifier
  note: ラベル付き占有ベクトルと正占有多重集合を独立生成する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q4-grundy-20261115/output/audit.json
  role: data
  note: 209パラメータ組・144,001ラベル状態・4,997多重集合状態の有限監査
- path: research/log/2026-11-15-vertical-fiber-t2-q4-grundy.md
  role: log
  note: K0832のq=3/q=5成果の間を埋めるq=4分類の証明・監査・限界
scope: r≥1、有限非空B⊂R^r、有限A⊂R、盤B×A。底面跡族Tの柱T×Aと、deg_z(F)≤tかつ全b∈BでF(b,.)≢0を満たす全多項式族（底面係数次数は無制限）を禁止対象とする。配置Sの多項式族との最大共存数はΣ_b min(c_b,t)と厳密に一致し、安全性は底面跡容量条件とΣ_b min(c_b,t)≤q−1の同時成立と同値。境界層Grundy公式はT=∅の純多項式ルールで全称、T≠∅では飽和ファイバー全充填後も全跡容量が保たれる場合の十分系。さらにT=∅かつt=1では全局面でG(S)=(m·min(|B|,q−1)−|S|) mod 2。さらにT=∅、t=2、q=3、|B|≥2、|A|≥2では全安全局面のGrundy値を占有ベクトルの形状とmの偶奇で完全分類する。 さらに底面跡制約なし・t=2・q=4・|B|≥2・|A|≥2では全安全局面のGrundy値を閉形式で完全分類し、|B|=2では最大1、|B|≥3ではm偶数で最大1・奇数で最大2となる。さらに底面跡制約なし・t=2・q=5・|B|≥3・|A|≥2では、全安全局面のGrundy値を占有多重集合の9型に分けて閉形式で完全分類し、m偶数で最大1、m奇数で最大3となる。
evidence: 全称数学的証明。各ファイバーの根数上界Σ min(c_b,t)と、分離線形形式に沿うラグランジュ補間による上界達成から、全多項式族に対する最大共存数を厳密決定。底面跡容量条件と合わせて安全性・合法手・Grundy値を占有ベクトルへ厳密縮約する。境界層C(c)=q−1では飽和ファイバーの鎖分解からGrundy値の排他的論理和公式を全称証明し、底面跡制約付きの十分条件も証明。2×2底面・3高さの補間監査に加え、w,m,t≤4の64組・5,080境界状態を独立再帰で有限監査。t=1の固定終局長補題から全局面Grundy公式を全称証明し、w≤5,m≤4,q≤w+2の100組・17,368安全状態を再帰mexで有限監査。t=2・q=3の全分類は容量2の三状態型への場合分けとmexによる全称証明。w,m=2..12の121組・9,196状態を専用再帰検証器で有限監査し、不一致0件。 t=2,q=5の分類は容量4の安全占有型（空・単独列・二列・(a,1,1)・四単独列）を網羅し、各型の合法子とmexを後ろ向きに解く全称証明。w=3..12,m=2..16の150組でラベル付き723,780状態と独立な多重集合11,135状態を再帰mex照合し、不一致0。有限監査は証明の代替ではない。 t=2,q=4の分類は容量3の安全占有型（空・単独列・(1,b)・三単独列）を網羅し、各遷移とmexを全称的に場合分けした。w=2..12,m=2..20の209組でラベル付き144,001状態と独立な多重集合4,997状態を再帰mex照合し、不一致0。有限監査は証明の代替ではない。
---

# 垂直ファイバー次数による一般縮約

## 一様閾値の定理（従来結果）

有限集合 B⊂R^r、|B|=w、有限高さ集合 A⊂R、|A|=m とし、盤を X=B×A とする。各 b∈B のファイバーを {b}×A と呼ぶ。

底面の指定された跡族を T とし、各 T∈T に対して柱 T×A 上の q点共存を禁止する。さらに、多項式超曲面 F(x,z)=0 上の q点共存も禁止する。ただし各 F は、全ての b∈B について一変数多項式 F(b,z) が零多項式ではなく、その z次数が高々 t であると仮定する。特に、zについてmonicな多項式はこの条件を自動的に満たす。

q>tw なら、多項式超曲面による禁止条件は一度も発生しない。したがって安全性は、底面跡容量条件だけで完全に判定できる。

配置 S⊂B×A の各ファイバー占有数を c_b=|S∩({b}×A)| と置くと、

\[
S\text{ が安全}
\iff
\sum_{b\in T}c_b\le q-1
\quad(\forall T\in\mathcal T).
\]

合法手は、ある一成分 c_b を1増やして全容量制約を保つ操作と一致する。従って同じ占有ベクトルを持つ全てのセル配置は同じ子占有ベクトル集合を持ち、Grundy値も一致する。状態数は高々 (m+1)^w である。

## 証明

固定した F と b∈B を取る。F(b,z) は零多項式ではない次数高々tの一変数多項式だから、異なる実根は高々t個である。従ってファイバー {b}×A と F=0 の交点は高々t点であり、盤全体では

\[
|(B\times A)\cap\{F=0\}|
\le\sum_{b\in B}t=tw.
\]

q>tw なので、どの配置も F=0 上に q点を含めない。多項式超曲面による禁止は消え、柱 T×A にq点を含むかどうかだけが残る。その点数は正確に Σ_{b∈T}c_b である。

また、柱の条件は占有ベクトルだけで決まる。あるファイバーに空きがあれば、そのファイバー内のどの空き高さへ石を置いても同じ子占有ベクトルになる。従って同じ c を持つ配置の子状態集合は一致し、終局からの帰納法でGrundy値も一致する。

## 既存の共円ゲームへの系

- 長軸に平行でないアフィン超平面は、各ファイバーと高々1点で交わる。したがって t=1。
- 通常の球面は、各直線ファイバーと高々2点で交わる。球面方程式は高さ z についてmonicな二次式なので t=2。
- より一般に、各ファイバー上で零多項式にならない z次数t以下の多項式超曲面を追加しても、q>tw ならゲームは変わらない。

従ってK0824の q>2w 縮約は t=2 の場合として回収される。K0824が別途示した超平面跡の個数上界や q=2w の球面反例は、本項目では置き換えない。

## 補間による正確な占有条件（q≤t|B|も含む）

従来の \(q>tw\) は全配置に対する一様十分条件だが、個々の配置ではもっと鋭い判定ができる。全ての底面係数多項式を許し、各ファイバー上では零多項式にならない全族 \(\mathcal F_t(B)\) に対し、

\[
\boxed{\max_{F\in\mathcal F_t(B)}|S\cap\{F=0\}|=\sum_{b\in B}\min(c_b,t)}
\]

が成立する。上界は各ファイバーの根数から従う。達成は、各ファイバーで選んだ石を根に含むモニック次数t多項式 \(P_b\) を作り、そのt未満の係数をB上のラグランジュ補間で一斉に実現すればよい。得られるFは全ファイバーでモニックなので、零多項式となるファイバーはない。

従って、底面跡容量条件に加えて

\[
\boxed{\sum_{b\in B}\min(c_b,t)\le q-1}
\]

を課すことが、全多項式族版の安全性の必要十分条件になる。合法手・子占有ベクトル集合・Grundy値もこの条件だけで決まる。

この等式は、係数の底面次数を制限しない全族についてのもの。固定底面次数や既約性を課した部分族では、補間による上界達成を保証しない。

## 境界層のGrundy値

底面跡制約を持たない純粋なファイバー多項式ルールでは、境界層
\[
\sum_{b\in B}\min(c_b,t)=q-1
\]
の全局面は、その層の中だけに子を持つ。Grundy値は
\[
\boxed{
G(c)=\bigoplus_{\substack{b\in B\\c_b\ge t}}
\bigl((m-c_b)\bmod 2\bigr)
}
\]
である。

実際、未飽和ファイバー \(c_b<t\) への追加は容量和を1増やして不合法になる。一方、飽和済みファイバー \(c_b\ge t\) への追加は容量和を変えず、\(c_b<m\) なら合法である。飽和済みファイバーはその後も飽和済みのままなので、境界層のゲームは長さ \(m-c_b\) の一方向の鎖の直和となる。長さ \(h\) の鎖のGrundy値は \(h\bmod2\) であり、直和の値は各成分の排他的論理和である。∎

底面跡族 \(\mathcal T\) も同時に課す場合、さらに
\[
\sum_{b\in T}c_b+
\sum_{\substack{b\in T\\c_b\ge t}}(m-c_b)
\le q-1
\quad(\forall T\in\mathcal T)
\]
が成立すれば、飽和済みファイバーを全て満杯にしても全跡容量を超えない。この場合は全ての鎖の手が最後まで合法で、同じGrundy公式が成立する。この条件を満たさない一般の跡制約付き局面には公式を適用しない。

## t=1 の全局面Grundy値

底面跡制約を持たない純ファイバー多項式ルールで t=1 とする。安全条件は非空ファイバー数が
\[
r=\min(|B|,q-1)
\]
以下であることに等しい。終局はちょうど r 本のファイバーを全て満杯にした局面であり、全終局の石数は rm で一定となる。

各着手は石数を1増やすので、任意の安全局面 S から終局までの全ての最大長着手列は rm−|S| 手である。一般に、全ての最大長着手列の長さが L で一定の有限通常プレイゲームでは、帰納法によりGrundy値は L mod 2 となる。従って
\[
\boxed{G(S)=(rm-|S|)\bmod2.}
\]
これは境界層だけでなく、t=1の全内部層を含む。底面跡制約を同時に課す場合や t≥2 の内部層には、この固定終局長の議論を適用しない。

## 境界 q=tw の鋭さ

任意の t≥1 について、一般の多項式超曲面族では q>tw の不等号を弱められない。r次元単体の頂点

\[
B=\{0,e_1,\ldots,e_r\},\qquad w=r+1
\]

を底面に取り、高さ A={1,...,t} とする。多項式

\[
F(x,z)=\prod_{j=1}^{t}(z-j)
\]

は次数tでmonic、盤 B×A の全tw点を含む。一方、Bのどのアフィン超平面跡 T も |T|≤r=w−1 なので、全ファイバーにt点ずつ置いた占有ベクトル c_b=t は

\[
\sum_{b\in T}c_b=t|T|
\le t(w-1)=tw-t\le tw-1=q-1
\]

を満たす。従って底面跡容量判定は安全と判定するのに、実際にはF上にq点がある。Fはt>1では可約だが、次数t以下の多項式超曲面を許す一般定理の境界反例として十分である。

さらに次数1〜3については、既約な整数係数の境界例もある。Bを同じ単体とし、x₁を第一底面座標とする。

- t=1: F=z−x₁。x₁=0のファイバーでは高さ0、x₁=1では高さ1を選ぶ。
- t=2: F=z(z−3)+2x₁。x₁=0では高さ {0,3}、x₁=1では {1,2} を選ぶ。
- t=3: F=z(z−4)(z−5)−12x₁。x₁=0では {0,4,5}、x₁=1では {1,2,6} を選ぶ。

いずれも各ファイバーにちょうどt点ずつ置き、全tw点が同一超曲面上に載る。各式はx₁について一次で、その係数が非零定数なので多項式環上既約である。高さは全て整数である。

## t=2・q=3 の全局面Grundy値（|B|,|A|≥2）

底面跡制約のない純ファイバー多項式ゲームで、ファイバー次数上限を \(t=2\)、禁止点数を \(q=3\) とする。K0832の厳密占有条件は

\[
\sum_{b\in B}\min(c_b,2)\le2
\]

となる。\(w=|B|\ge2\)、\(m=|A|\ge2\) のとき、安全局面は次の三種類しかない。

1. 空局面。
2. 一つのファイバーだけが非空。
3. 異なる二つのファイバーに1個ずつ石がある。

全局面のGrundy値は

\[
G(c)=
\begin{cases}
0,&\operatorname{supp}(c)=\varnothing,\\
(m-c_b)\bmod2,
 &\operatorname{supp}(c)=\{b\},\ c_b\ge2,\\
1,&\operatorname{supp}(c)=\{b\},\ c_b=1,\ m\text{ 偶数},\\
2,&\operatorname{supp}(c)=\{b\},\ c_b=1,\ m\text{ 奇数},\\
0,&\operatorname{supp}(c)=\{b_1,b_2\},\ c_{b_1}=c_{b_2}=1.
\end{cases}
\]

証明は三種類の分類に帰着する。一つのファイバーに2個以上ある局面は残り \(m-c_b\) 手の鎖。二つの単独石の局面は終局。一つの単独石の局面では、同じ列を2個にする鎖型局面と、別の列を開始する終局の二種類へ移るため、

\[
G=\operatorname{mex}\{0,(m-2)\bmod2\}
=
\begin{cases}
1&m\text{ 偶数},\\
2&m\text{ 奇数}.
\end{cases}
\]

空局面の全ての子は同じGrundy値1または2を持つので、空局面の値は0。従って全安全局面のGrundy値は0,1,2に限られる。

特に \(w=2,m=3,c=(0,1)\) では、二つの子のGrundy値が0と1となり、\(G(0,1)=2\)。これは \(t=1\) の全局面公式を \(t=2\) に単純延長できない反例である。

有限監査として、\(2\le w,m\le12\) の121組・9,196安全状態を再帰mexと照合し、不一致0件。全称性は上記の数学的証明による。

## 限界

- F(b,z)≡0を許し底面次数を制限しない場合、Bを分離する線形形式ℓに対するG(x)=∏_{b∈B}(ℓ(x)−ℓ(b))が全Bで消え、F=Gは盤全体を含む。従って非零ファイバー条件は非自明な分類に必要。底面次数制限付きで退化ファイバーを許す場合は別問題。
- 全多項式族・底面係数次数無制限・各ファイバー非零という範囲ではq≤twも上のΣ min(c_b,t)条件で完全分類した。K0504のdeg f≤kの固定次数グラフは補間次数が制限を越え得るため未解決。
- 有限検証は境界例の確認であり、全称縮約の証明は根数上界による。
- K0504の共多項式変種のうち、底面係数次数無制限の任意グラフ z=f(x) はt=1として占有ファイバー数で完全分類できる。K0504が提案するdeg f≤kの固定次数版は本項目の補間次数制限を満たすとは限らず、必要十分条件は未解決。


## t=2・q=4の純ファイバー全局面Grundy分類

底面跡制約なし、\(t=2,q=4,w=|B|\ge2,m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,2)\le3.
\]
安全占有型は空、単独列 \((a)\)、二列 \((1,b)\)、三単独列 \((1,1,1)\) に限られる。

全局面のGrundy値は次である。
\[
G(())=(m+1)\bmod2,\qquad G((a))=(m-a+1)\bmod2,
\]
\[
G((1,b))=(m-b)\bmod2\quad(b\ge2),
\]
\[
G((1,1))=
\begin{cases}
(m+1)\bmod2&w=2,\\
1&w\ge3,\ m\text{ 偶数},\\
2&w\ge3,\ m\text{ 奇数},
\end{cases}
\qquad G((1,1,1))=0.
\]
従って最大Grundy値は、\(w=2\) では常に1、\(w\ge3\) ではm偶数で1・m奇数で2。Grundy値2の最小証人は \(w=m=3,c=(1,1,0)\) であり、子の値は1と0。

証明は、\((1,b)\ (b\ge2)\) が一方向の鎖、三単独列が終局、二単独石は第三列開始の有無で分岐することを使う。単独列と空局面はその後ろ向きmexから確定する。全証明と適用限界はartifactのreport.mdに記載した。

有限監査はw=2..12,m=2..20の209組。ラベル付き144,001状態と独立な多重集合4,997状態を再帰mexで照合し、不一致0。これは有限監査であり、全称性は上記の帰納証明による。

## t=2・q=5の純ファイバー全局面Grundy分類

底面跡制約なしの純ファイバーゲームで \(t=2,q=5\)、\(w=|B|\ge3,m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,2)\le4.
\]
安全占有多重集合は \(()\)、\((a)\)、\((a,b)\)、\((a,1,1)\)、\((1,1,1,1)\) に限られる。\(p_a=(m-a)\bmod2\) と置くと、Grundy値は次で完全分類される。

| 占有型 | Grundy値 |
|---|---|
| 空 | \(1\) iff \(w=3\) かつ \(m\) 奇数、その他0 |
| \((1)\) | \(m\) 偶数なら1。奇数なら \(w=3\) で0、\(w\ge4\) で2 |
| \((a),a\ge2\) | \(p_a\) |
| \((1,1)\) | \(m\) 奇数かつ \(w=3\) のとき1、その他0 |
| \((1,b),b\ge2\) | \(m\) 偶数なら \(b\) 偶数で1・奇数で0。\(m\) 奇数なら \(b\) 偶数で3・奇数で2 |
| \((a,b),a,b\ge2\) | \(p_a\oplus p_b\) |
| \((1,1,1)\) | \(m\) 偶数なら1。奇数なら \(w=3\) で0、\(w\ge4\) で2 |
| \((a,1,1),a\ge2\) | \(p_a\) |
| \((1,1,1,1)\) | 0 |

従って
\[
\boxed{\max G=
\begin{cases}
1&m\text{ 偶数},\\
3&m\text{ 奇数}.
\end{cases}}
\]
最小のGrundy値3の証人は \(w=m=3,c=(2,1,0)\)。三つの子 \((3,1,0),(2,2,0),(2,1,1)\) の値がそれぞれ \(2,0,1\) なので、親の値は \(\operatorname{mex}\{0,1,2\}=3\)。

証明では、二飽和列は二つの鎖の直和、\((a,1,1)\) は一つの鎖、\((1,b)\) は \(x_b=\operatorname{mex}\{p_2\oplus p_b,p_b,x_{b+1}\}\)（終端では \(x_m=\operatorname{mex}\{p_2\}\)）を後ろ向きに解く。\((1,1,1)\)、\((1,1)\)、単独列、空局面を順にmexで確定する。詳細な全証明は上記report artifactに保存した。

有限監査は \(3\le w\le12,2\le m\le16\) の150組。ラベル付き占有ベクトル723,780状態と、正占有数の多重集合11,135状態を別々の再帰mexで検査し、閉形式との不一致は0。これは有限範囲の監査であり、全称性は場合分け証明による。対象は抽象ファイバー多項式ゲームで、標準二次元の3×m・q=5幾何ゲームとは別である。
