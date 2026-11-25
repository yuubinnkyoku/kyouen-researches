# 5行・8点版の真の満容量安定化長は16

2026-10-05（JST）。標準格子
`D(5,m)={0,...,m-1}×{0,...,4}` 上で、8点共円または共線を
禁止する通常プレイを対象とする。これは標準q=4版の結果ではない。

## 結論と証拠の種類

\[
\boxed{M_{5,8}=16},\qquad
\boxed{g(S)=(35-|S|)\bmod2\quad(m\ge16)}.
\]

下界は5×15の34石安全極大配置。上界は次の二部分を結ぶ。

- m=16..185: 各長さと鏡映を除いた対象行0,1,2の510個の有限SAT問題を
  全てUNSATと確定し、各証明トレースを別実装drat-trimで検査。
- 全m≥186: 既存の曲線充填一般定理[K0318](../../../knowledge/items/K0318-fixed-width-curve-packing-upper-bound.md)。

SATでの有限完全排除と、無界な長さへの数学的証明を区別する。
有限範囲の観測を無限区間へ外挿しない。全安全局面の巨大なGrundy表も列挙していない。

## 1. 五行内の8点円は四行の二点対だけである

一行に格子点を高々1個しか持たない円は、五行内で高々5点。
水平二点を持つ円を

\[
x^2+y^2+Bx+Cy+D=0
\]

と書くと、二根の和からBは整数。別行の点との方程式の差からCは有理数。
既約分母をvとすると、占有行は一つの剰余類mod vに限られる。
v≥2なら五行内で高々3行、従って高々6点である。

v=1ならC,Dも整数であり、占有する各行で

\[
(2x+B)^2+(2y+C)^2=N,\qquad N=B^2+C^2-4D
\]

が成り立つ。mod9の平方剰余{0,1,4,7}について81組の(C,N)を検査すると、
五つの連続行で条件を満たせるのは高々4行（既存[K0072](../../../knowledge/items/K0072-mod9-integer-row-separation.md)の同じ合同条件）。
従って五行帯の一円上の格子点は高々8個。
8個を持つならちょうど四行に二点ずつあり、残り一行は空である。

四行を0..4から選ぶと隣接する二行が必ずある。隣接行i,i+1の二点間隔をa,bとすると

\[
C=(a^2-b^2-4(2i+1))/4,\qquad N=a^2+(2i+C)^2
\]

でC,Nが決まる。各行の間隔d_yは
`d_y²=N-(2y+C)²` の正の整数平方根である。
全行の二根は同じ整数和sを持ち、`x=(s±d_y)/2`。
これで盤内の全8点円を、整数平方根だけで漏れなく生成できる。
非水平直線は五行から高々5点なので、禁止8点直線は水平行だけ。

span≤184の全円型は19個、5×185内の全8点円は2,655個である。
独立C++実装は弦差の式を使わず、同じ和の二点対の積から円係数を求める。
最大盤で4,187,104個の隣接行点対割当を検査し、全2,655円の集合が一致した。
その集合を各小盤へ制限して、m=16..185の全円集合との一致も確認する。

## 2. 不足極大を有限CNFへ正確に変換する

対象行tの石数を≤6、他の各行を≤7とする。各点の占有を変数X_pで表す。

1. 各行の石数上限をsequential-counter CNFで表す。
2. 各8点円Cに、全8点が同時に占有されない節を置く。
3. C上の対象点pごとに変数B_{C,p}を置き、B_{C,p}が真なら
   `C\{p}` の7点が全て占有されるように7節を置く。
4. 各対象点pに `X_p∨∨_{C∋p}B_{C,p}` を置く。

対象行に6石以下しかなければ、空点の追加で水平8点直線はできない。
従って空点を塞ぐものは、他の7点を既に含む8点円だけ。
上のCNFを満たす占有集合は正確に「安全で、対象行の全空点が追加不能」の集合である。
さらに外部行だけへ合法点を貪欲に追加すると、対象行のblockerは消えないため
不足極大集合へ拡張できる。逆に不足極大集合は必ずこのCNFを満たす。

行反転でt=3,4はt=1,0と同じ。m=16..185、t=0,1,2の全510問題について
CaDiCaL 2.1.2がUNSATを出し、drat-trimが各生成トレースに`s VERIFIED`を返した。
これはtimeoutやヒューリスティック探索ではない。

入力CNF・DRATトレースのhash、サイズ、検査結果は
`../output/q58_finite_certificate_manifest.json`。
境界m=16の三問題はCNFとDRATをgzipで保存した。
他の507トレースは容量節約のため保持せず、再現コードが全て再生成・再検査する。
外部SAT solverのUNSAT宣言だけに依存しないが、drat-trimとCNF変換自体は
通常のソフトウェア検証境界にあり、Lean核内検査は行っていない。

## 3. 無限末尾

K0318でw=5,q=8を代入するとr=7,a=6,N=28、Q=3,136、
d0=35,d1=20,Y=144。

\[
H=\max\{2u+v:35u+20v\le3136,\ v\le144\}=179
\]

であり、(u,v)=(89,1)が達成する。
従って全m≥r+H=186で全極大は35石。
有限排除と繋ぐと全m≥16で同じ結論になる。
残り手数35−|S|についての帰納により全局面のGrundy偶奇式が従う。

## 4. 鋭い下界

5×15で次の配置は34石、安全かつ極大である。

```text
y=0: 1,3,6,7,9,11
y=1: 1,3,4,6,8,11,13
y=2: 1,2,4,8,10,11,13
y=3: 2,3,5,7,9,10,12
y=4: 2,4,5,7,8,9,10
```

独立検査は盤内75点の全67,525三点組からprimitive整数円・直線係数を生成し、
全禁止曲線に占有点が7個以下であることを確認した。
全41空点には、それを通り既存7点を含む禁止曲線がある。
対象行は6石、残る各行は7石であり、M≥16が従う。
全空点の具体的blockerは`../output/q58_independent_audit.json`に保存。

## 再現

repoのlockfileは変更しない。python-satは外部ディレクトリへ導入する。

```sh
UV_CACHE_DIR=/workspace/onboarding-tools/uv-cache uv pip install \
  --target /workspace/research-tools/python-sat 'python-sat==1.8.dev30'
git clone https://github.com/marijnheule/drat-trim.git /workspace/research-tools/drat-trim
git -C /workspace/research-tools/drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
gcc -D_DEFAULT_SOURCE -O2 -std=c99 /workspace/research-tools/drat-trim/drat-trim.c \
  -o /workspace/research-tools/drat-trim/drat-trim
g++ -O3 -std=c++17 research/experiments/fixed-width-frontier-20261005/scripts/q58_geometry_audit.cpp \
  -o /tmp/q58_geometry_audit
/tmp/q58_geometry_audit 185 > /tmp/q58_independent_circles_185.txt
python research/experiments/fixed-width-frontier-20261005/scripts/q58_independent_check.py \
  --independent-circles /tmp/q58_independent_circles_185.txt
python research/experiments/fixed-width-frontier-20261005/scripts/q58_certify.py \
  --cadical /workspace/onboarding-tools/elan/toolchains/leanprover--lean4---v4.30.0/bin/cadical \
  --drat-trim /workspace/research-tools/drat-trim/drat-trim \
  --work-dir /tmp/q58-certify \
  --output /tmp/q58_reproduced_manifest.json
```

実行機に同じLean付属binaryがなければCaDiCaL 2.1.2を用意し`--cadical`を変える。
実行時間やプラットフォーム依存binary hashより、510個のUNSAT・DRAT VERIFIED、
円集合と証人の幾何、整数上界を照合する。

## 残った問題

本結果はm<16の全Grundy分類や、w=5,q=6,7の真の閾値を解いていない。
同じCNF方式は再利用できるが、q=7では盤外に一つだけ根を持つ8点円や
7点円もblockerになり得るため、8点が全て盤内にある円だけの生成を流用してはいけない。
