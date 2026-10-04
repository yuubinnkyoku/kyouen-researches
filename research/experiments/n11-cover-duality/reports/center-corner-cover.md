# 中心・隅rootのs4 class coverの厳密値

**11×11空盤勝敗: UNKNOWN。** ここで求めるのは、全安全s4 classを使用可能と
仮定したcertificate skeletonの最小class数であり、各classの勝敗ではない。
base: `754cd0710d448ab397aa0cd3cb1a941e5d7f5451`。

## 問題と範囲

奇数nについて `B_n={0,…,n−1}²`、`o=(0,0)`、`c=((n−1)/2,(n−1)/2)` と置く。
標準q=4の固定二石root `{o,c}` からは、`V=B_n\{o,c}` の全点が第三手として合法。
`{o,c,a,b}` が安全な四点集合であるときだけ、第三手aとbを結ぶedgeを置く。
四点集合を**盤全体のD4 orbit**でまとめたものをclass Cとし、

```
cov(C) = {v∈V : rootを含むQ∈Cとw≠vが存在し、Q={o,c,v,w}}
```

と定義する。異なるroot配置まで同一classに入るが、coverageには固定rootを
含む像だけを使う。`OPT(n)` は `V` を覆うclass数の最小値。
WIN/LOSS未確定のclassも含めた構造的問題であり、実際に使用可能な証明済み
classだけへ制限すると最小値は増え得るし、cover自体が存在しないこともある。

**定理。奇数n≥5について**

```
OPT(n) = ceil((n²+n−8)/4).
```

n≥9では `{o,c,(1,0),(2,0)}` のclassを必須にしても同じ最適値が達成される。
したがってn=11では既存研究が使用する `{60,0,1,2}` のclassを含む31-class
skeletonが得られ、これ以外に必要なclass数の構造的最小値は30。
これはその30 classの勝敗判定を済ませたという意味ではない。

## 全称下界: 整数だけで検査できるdual

rootのstabilizerは `H={id,(x,y)↦(y,x)}`。盤上のH-orbit数は
`n+n(n−1)/2=(n²+n)/2`。このうち非隅で、root以外のorbit数は

```
T=(n²+n)/2−4=(n²+n−8)/2.
```

除いた4 orbitは、o、c、反対隅、残る隣接隅二点のorbitである。
各非隅orbitから一つの代表点を選び、その重みを1/2とする。他の点の重みは0。

一つのclassが覆う非隅H-orbit数は高々2:

1. 四点集合に隅が一つだけなら、その隅をoへ送るD4変換はHの一つのcoset。
   二つの非隅追加点はそれぞれ一つのH-orbitを覆う。
2. 隅が二つなら、残る非隅追加点は一つ。その点の像は、どちらの隅をoへ
   送るかに対応する高々二つのH-orbitに入る。
3. 隅が三つなら追加点は隅だけなので、非隅orbitを覆わない。

各classの重み和は高々1、全重みはT/2。任意のcover Fに対して、
重なりがあっても重みが非負なので

```
T/2 ≤ sum_{C∈F} sum_{v∈cov(C)} weight(v) ≤ |F|.
```

class数は整数だから `OPT(n)≥ceil(T/2)`。この証明はMILP、solverの
optimalラベル、浮動小数点、探索途中の統計に依存しない。

## 全称上界: n≥9

以下の三つのclassを先に選ぶ。点の単位は座標である。

```
S0={o,c,(1,0),(2,0)}
A ={o,c,(n−1,0),(3,0)}
B ={o,c,(n−1,n−1),(4,0)}.
```

S0とAはy=0上の三点と、その直線外のcからなり、Bは主対角線上の三点と、
その直線外の(4,0)からなる。三つの相異なる共線点を円は通れず、第四点は
直線上にないので、すべて安全。

Aは残る隣接隅二点のH-orbitを、Bは反対隅を覆う。非隅については、三つの
classが以下の**相異なる六つ**のH-orbitを覆う:

```
(1,0), (2,0), (3,0), (n−4,0), (4,0), (n−1,n−5).
```

最後の点は、Bの(4,0)を半回転してH代表へ移したもの。
六つのorbitはn≥9で相異なり、各classの非隅coverageはちょうど上記二つずつ。
S0はAともBとも異なる。これで全隅が覆われ、残る非隅orbit数は `M=T−6`。

残り各orbitから固定代表 `p=(x,y), x≥y` を取る。二代表p,qの間に
`{o,c,p,q}` が安全なときだけedgeを置いたグラフGを考える。
このedgeのclassは二orbitを覆うので、Gのedge coverはそのままs4 class cover。

固定o,c,pの三点が共線なら、その直線は主対角線で、盤点数はn以下。
共線でなければ三点の円は一意で、各水平行との交点が高々二つなので
盤点数は2n以下。よって、pと安全edgeを作れない他代表qは高々2n−3点。
Gの最小次数は

```
δ(G)≥M−1−(2n−3)=M−2n+2.
```

n≥9では `M=(n²+n−20)/2≥4n−4`、実際
`n²−7n−12=(n−9)(n+2)+6≥0`。したがって `δ(G)≥M/2`。

**matching lemma。** M点のグラフで `δ≥floor(M/2)` なら、最大matchingの
未被覆頂点は高々一つ。もし二点u,vが未被覆なら、それらは互いにも、他の
未被覆点にも隣接しない。任意のmatching edge {a,b}に対するu,vからの隣接は
高々二本で、三本あればそのedgeを二本へ交換する長さ3のaugmenting pathが
存在する。従って `deg(u)+deg(v)≤2|matching|`。
Mが偶数なら右辺≤M−2だが左辺≥M。Mが奇数なら未被覆点数も奇数なので
三点以上となり、右辺≤M−3だが左辺≥M−1。いずれも矛盾する。

Mが偶数ならmatchingをそのまま使い、Mが奇数なら一つの未被覆点をその隣点
へ結ぶedgeを追加する（上の次数下界より孤立点ではない）。これで
`ceil(M/2)` 個のedgeからなるcoverが得られる。
従って総class数は

```
3+ceil((T−6)/2)=ceil(T/2),
```

となり、下界と一致する。三つの最初のclassにS0が含まれるので、既存S0
classを再利用する制約も同時に満たす。

## n=5,7と境界の有限確認

n=5,7は上の次数下界だけでは閉じないため、具体coverと同じdualを検査した。
点idは `v=yn+x`。下記はrootを含む四点集合の代表で、行ごとに一class。

```
n=5 (c=12):
{0,12,4,1}, {0,12,24,2}, {0,12,6,7},
{0,12,8,9}, {0,12,13,18}, {0,12,19,6}.

n=7 (c=24):
{0,24,6,1}, {0,24,48,2}, {0,24,3,4}, {0,24,8,9},
{0,24,10,11}, {0,24,12,13}, {0,24,16,17}, {0,24,18,19},
{0,24,20,26}, {0,24,25,27}, {0,24,32,33}, {0,24,40,41}.
```

独立検査器は安全性、D4 classの一意性、全coverage、全classへのdual制約を
再構成して検査する。これらは存在証人＋完全有限下界検査であり、n≥9の
有限実験から全称結論を外挿したものではない。

n=3は例外: 7第三手、8class、最大coverage6なのでOPT≥2、二classの証人で
OPT=2。n≥5の式を誤ってn=3へ拡張すると1となり、成立しない。

## 独立検証と再現

生成器は共有 `kyouen_core.is_forbidden_quad` と `residual_core.d4_perms` を使い、
greedy matchingと長さ3のaugmenting pathだけで具体coverを作る。
greedy終了時の未被覆点集合は独立集合で、長さ3の交換はそこから二点を
除くだけなので、独立性は維持される。従って未被覆点が二つ以上残って
長さ3の交換が存在しない場合には、matching lemmaと同じ次数の矛盾が起きる。
生成器は一般のmaximum matching solverを実装する必要がない。
検査器は共有geometryと生成器をimportせず、原点へ平行移動した3×3整数
行列式と明示的な八つの座標変換で全safe edge、全class、coverageを再列挙する。
全dual制約を整数 `0,1,2` と分母2だけで検査し、上界と下界の一致を確認する。
削除class、偽coverage、過大dual、重複classの四変異はすべて拒否された。

```sh
python research/experiments/n11-cover-duality/scripts/generate_cover.py
python research/experiments/n11-cover-duality/scripts/verify_cover.py \
  research/experiments/n11-cover-duality/output/center-corner-cover.json \
  --mutation-checks \
  --output research/experiments/n11-cover-duality/output/verified.json
```

| n | 第三手 | 全class | dual合計 | 確定OPT |
|---:|---:|---:|---:|---:|
| 3 | 7 | 8 | 1（別に単純下界2） | 2 |
| 5 | 23 | 110 | 11/2 | 6 |
| 7 | 47 | 501 | 12 | 12 |
| 9 | 79 | 1466 | 41/2 | 21 |
| 11 | 119 | 3396 | 31 | 31 |
| 13 | 167 | 6779 | 87/2 | 44 |
| 15 | 223 | 12133 | 58 | 58 |

## n11探索への意味と残件

旧 `N11-DFPN-COVER-OPTIMUM.md` は31-class上界witnessを検査した一方、最適下界は
MILPのoptimalラベルに依存し、記録内に古い未確定記述も残っていた。今回、
その歴史資料を書き換えず、新しいproofと検査可能なdualを保存した。
標準の中心・隅rootについては、全3396classの処理を要求する必要がなく、
31classのcertificate skeletonが構造的に最良であると独立に証明できる。

ただし新しいwitnessの選択classをすべて実際のLOSS証明へ変換できる保証はない。
未知classがWINになれば除外し、coverを組み直す必要がある。class数最小化と
未知s5子の重複・計算コスト最小化も別問題。実測の速度改善は主張しない。
最新mainのK0329はs5 verdict回収とs4 manifestの独立検査を追加している。
今回の新しいcover生成器はD4 orbitを直接定義し、旧class番号を前提にしない。
安全な全classによる最小値31と、既知WINを除いた実際のcertificate候補最小化は区別する。
次の有力な一手は、既存s5 verdict cacheとs4 manifestを入力し、既知LOSSの
costを0、既知WINを禁止としたweighted coverに、この整数dualを下界として
組み込み、独立検証可能な候補skeletonを再生成すること。
