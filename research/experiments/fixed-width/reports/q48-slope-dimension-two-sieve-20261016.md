# 4×m・q=8：実現可能な既約傾きの定量上界を対数二乗へ改善

**区分**：全称証明。既知の古典定理（一変数の大篩、算術級数の素数定理、Karamata の Tauber 型定理）を明示的に使用する。付属の計算は有限監査であり、全称証明の代用ではない。

**確認した正本**：2026-10-16 の main `db2a6b9b5291c4038b65e98fa838088881b17c0d`、AGENTS.md、knowledge README、generated/summary.md、K0432および main に反映済みの `q48-inert-prime-slope-density-20261016.md`。後者の `O(H²/log H)` を改善する。

## 定理

四つの連続整数行を各二格子点ずつ通る非局所8点円の水平弦長を、上下反転により `a<b<c<d` とする。`s=(a+d)/2`, `v=(c-b)/2` の既約比 `s/v=A/B` (`gcd(A,B)=1`, `A,B>0`) を傾きと呼ぶ。`1<=A,B<=H` の実現可能な既約傾きの種類数を `R(H)` とすると、

\[
\boxed{R(H)=O\!\left(\frac{H^2}{(\log H)^2}\right)}\quad(H\to\infty).
\]

これは実現可能性の**必要条件からの上界**である。傾きの実現数に対する下界や、すべての候補が実現可能という主張は含まない。

## 1. 素数ごとに4つの剰余類を排除する

四行の弦長平方の二階差分は `-8`。`g=gcd(A,3)`, `P=A²-B²`, `Q=(A²-9B²)/g²` とおくと、適切な正整数 `L,M` に対して

\[
QM^2-PL^2=8,\qquad A>3B.
\]

この必要条件は以下のように直接導ける。各行の左右の整数 x 座標の和は共通の整数 `2x_c` なので、4本の弦長はすべて同じ偶奇を持つ。従って `t=(d-a)/2`, `u=(b+c)/2` も整数である。共円条件より `d²-a²=3(c²-b²)`、すなわち `st=3uv`。`s=AL,v=BL` と既約化すれば `At=3Bu`。`g=gcd(A,3)` により `t=3BM/g,u=AM/g`（正整数 M）。また `a²-2b²+c²=-8` を `a=s-t,b=u-v,c=u+v` に代入すると `s²+t²-u²-v²=-8`。これが `QM²-PL²=8` である。`a>0` と `b>0`、`Q M²=P L²+8` から `A>3B`。

`p>=7`, `p≡3 (mod 4)` を素数とする。`p|P` なら、既約性により `p∤B`、また `Q≡-8B²/g² (mod p)` なので、ノルム式を `p` で割った合同式は

\[
-(BM/g)^2\equiv1\pmod p
\]

となり矛盾する（`g=1` または `3` なので `p∤g`）。同様に `p|Q` なら `P≡8B² (mod p)` から

\[
-(BL)^2\equiv1\pmod p
\]

となり矛盾する。従って `p∤PQ`。

`p∤B` を固定すると、`P=(A-B)(A+B)` および `g²Q=(A-3B)(A+3B)` から

\[
\boxed{A\not\equiv B,-B,3B,-3B\pmod p}.
\]

4つの剰余類は `p>=7` で互いに異なる。`p|B` の場合はこの篩を使用しない。

## 2. 一変数の大篩を B ごとに適用

`\mathcal P={p>=7:p≡3 (mod 4), p は素数}` とし、`z>=7` に対して

\[
G_B(z)=\sum_{\substack{q\le z\\q\ \mathrm{squarefree}\\p\mid q\Rightarrow p\in\mathcal P\\(q,B)=1}}
\prod_{p\mid q}\frac4{p-4},\qquad G(z)=G_1(z).
\]

大篩の標準的な「除外剰余類」形式：長さ `H` の整数区間で各 `p<=z` に `\omega(p)<p` 個の剰余類を避ける集合の要素数は

\[
\#\mathcal A\le\frac{H+z^2}{\displaystyle\sum_{q\le z}\mu(q)^2\prod_{p\mid q}\frac{\omega(p)}{p-\omega(p)}}
\]

で抑えられる（`q` は使用する素数だけで構成）。ここでは `p∤B` なら `\omega(p)=4`、`p|B` なら `\omega(p)=0`。よって、固定した `B` に対する候補 `A∈[1,H]` の数 `N_B(H)` は

\[
N_B(H)\le \frac{H+z^2}{G_B(z)}.
\]

## 3. B に依存する分母を一様に処理

`f` を平方自由整数上の乗法的関数で、`p∈\mathcal P` なら `f(p)=4/(p-4)`、その他の素数を含む整数では `f(n)=0` と定める。`f(1)=1`。さらに

\[
F(B)=\prod_{\substack{p\mid B\\p\in\mathcal P}}\left(1+\frac4{p-4}\right)
=\sum_{d\mid B}f(d).
\]

`q<=z` の素因数を `B` と共有する部分 `d` と共有しない部分 `m` に分けると、`G(z)=\sum_{d\mid B} f(d)G_B(z/d)`（`d` は平方自由かつ `\mathcal P` の素数のみ）である。`G_B` は単調増加だから

\[
G(z)\le F(B)G_B(z),\qquad
N_B(H)\le \frac{(H+z^2)F(B)}{G(z)}.
\]

また、非負性から

\[
\sum_{B\le H}F(B)
=\sum_{d\le H}f(d)\lfloor H/d\rfloor
\le H\sum_{d\ge1}\frac{f(d)}d
=H\prod_{p\in\mathcal P}\left(1+\frac4{p(p-4)}\right)
\le C H,
\]

ここで無限積は `\sum_p p^{-2}<\infty` により収束する。`C` は `H` に依存しない。

## 4. 篩分母の成長

`D(s)=\sum_{n\ge1}f(n)n^{-s}` (`s>0`) とおくと

\[
D(s)=\prod_{p\in\mathcal P}\left(1+\frac4{(p-4)p^s}\right)
=\zeta(1+s)^2 L(1+s,\chi_4)^{-2}\,E(s).
\]

ここで `\chi_4` は法4の非自明指標。右辺の `E(s)` は `s=0` の近傍で正則かつ `E(0)>0` である。実際、各 `p>=7,p≡3(mod4)` の Euler 因子を比べると一次項がともに `4p^{-1-s}` で、残差は一様に `O(p^{-2-2\Re s}+p^{-2-\Re s})`。`p≡1(mod4)` の因子は相殺され、`p=2,3` の有限因子は非零である。

従って `s↓0` で `D(s)∼c s^{-2}` (`c>0`)。`f(n)>=0` なので、Karamata の Tauber 型定理（離散 Laplace–Stieltjes 形式）から

\[
G(z)=\sum_{n\le z}f(n)\sim\frac c2(\log z)^2.
\]

特に `G(z)\gg(\log z)^2`。`z=\lfloor\sqrt H\rfloor` とすれば

\[
R(H)\le\sum_{B\le H}N_B(H)
\le\frac{(H+z^2)\sum_{B\le H}F(B)}{G(z)}
\ll\frac{H^2}{(\log H)^2}.
\]

これで定理が従う。

## 独立した有限監査

`research/experiments/fixed-width/scripts/q48_sieve_dimension2_20261015.py` は、剰余類による篩と4つの線形因子の素数割り算が一致すること、`G(z)<=F(B)G_B(z)`、一変数大篩の有限数値不等式を `H=80,160,320,640` で確認する。既知の傾き `9/1` も排除されない。

この検証は有限範囲に限定される。大篩・Tauber 型定理の証明を計算で代用していない。出力は `research/experiments/fixed-width/output/q48_sieve_dimension2_20261015.json`。

## 未解決

この上界の対数指数2が最良か、実現可能な傾きに対する対応する下界があるかは不明。合同篩の通過は整数8点円の存在を保証しない。


## 追加定理：篩分母の厳密な主係数と傾き数の明示的 limsup

上の f, G, F を使い、絶対収束する正の Euler 積を

\[
\mathcal E=\prod_{\substack{p\ge7\\p\equiv3\pmod4}}
\frac{p(p-1)^2}{(p-4)(p+1)^2},\qquad
\mathcal F=\prod_{\substack{p\ge7\\p\equiv3\pmod4}}
\left(1+\frac4{p(p-4)}\right)
\]

と定義する（積は素数のみ）。すると、**全称的に**

\[
\boxed{G(z)\sim \frac{\mathcal E}{2\pi^2}(\log z)^2},\qquad
\boxed{\sum_{B\le H}F(B)\sim\mathcal F H}.
\]

特に傾き数について、定数まで明示した上界

\[
\boxed{\limsup_{H\to\infty}\frac{R(H)(\log H)^2}{H^2}
\le\frac{8\pi^2\mathcal F}{\mathcal E}}
\]

が成立する。100万以下の素数による**打ち切り積**の参考値は
`E≈1.5457907108`, `F≈1.3038608642`, `E/(2π²)≈0.0783106722`, `8π²F/E≈66.5994`。
これらの小数は厳密な誤差保証付きの値ではなく、定理の定数は上の無限積そのものである。

**証明**：先の Dirichlet 級数の分解 `D(s)=ζ(1+s)²L(1+s,χ₄)^{-2}E(s)` で、
`p=2` の補正因子は `s=0` で `(1−1/2)²=1/4`、`p=3` の補正因子は
`((1−1/3)/(1+1/3))²=1/4`。`p≡3(mod4),p≥7` の補正因子は

\[
\frac{1+4/(p-4)}{((1+1/p)/(1-1/p))^2}
=\frac{p(p-1)^2}{(p-4)(p+1)^2}.
\]

よって `E(0)=\mathcal E/16`。`L(1,χ₄)=π/4` から
`D(s)~(\mathcal E/π²)s^{-2}`。非負係数に対する Karamata 定理により
`G(z)~\mathcal E (log z)²/(2π²)`。

次に `F(B)=∑_{d|B}f(d)` と `∑_{d≥1}f(d)/d=\mathcal F<∞` から

\[
\frac1H\sum_{B\le H}F(B)
=\sum_{d\ge1}\frac{f(d)}d\frac{d\lfloor H/d\rfloor}{H}
\longrightarrow\mathcal F
\]

が支配収束で従う（`d>H` の項は0）。

大篩の `z=\lfloor\sqrt H/\log H\rfloor` を選べば
`z²=o(H)`, `log z~(log H)/2` なので、先の上界から

\[
R(H)\le\frac{(H+z²)\sum_{B\le H}F(B)}{G(z)}
\le\left(\frac{8\pi²\mathcal F}{\mathcal E}+o(1)\right)
\frac{H²}{(\log H)²}.
\]

これで追加定理が従う。前節の `z=floor(sqrt H)` よりも定数を改善するため、
あえて平方根より `log H` 倍だけ小さい篩上限を使っている。

**独立検証**：`q48_sieve_constant_independent_20261016.py` は2,000までの f(n) を
「各整数の直接素因数分解」と「平方自由重みの篩」という異なるアルゴリズムで
有理数として全件照合。`q48_sieve_constant_audit_20261016.py` は100万までの
重み付き篩と有限 Euler 積を数値計算する。後者の `G(z)/(log z)²` は
`z=10³,10⁴,10⁵,10⁶` で順に `0.17159,0.14717,0.13239,0.12299`。
有限値が極限 `≈0.07831` に等しくないことは矛盾ではない。極限の証明は解析的な定理による。


## 追加改良：厳密な傾き下界を用いた定数 7.9635…

前節の定数 `8π² F/E` は全ての `1≤B≤H` を数えた上界であり、
既存 K0432 の傾き下界を捨てている。`α=√(9+6√2)` と置くと、
実現可能な傾きは `A>αB` を満たす。固定 `B` で大篩を適用する区間を

`floor(αB)+1 ≤ A ≤ H`（長さ `H−floor(αB)`）

に狭められる。したがって**さらに強い全称上界**

\[
\boxed{\limsup_{H\to\infty}\frac{R(H)(\log H)^2}{H^2}
\le\frac{4\pi^2\mathcal F}{\alpha\mathcal E}}
\]

が成立する。100万以下の素数による打ち切り積を使った**参考値**は約 `7.9635`。
無限積で表した不等式が厳密な命題であり、この小数値には厳密な誤差保証を付けていない。

**証明**：`B≤H/α` に限って、前述の大篩と `G(z)≤F(B)G_B(z)` より

\[
R(H)\le\frac{1}{G(z)}\sum_{B\le H/\alpha}
F(B)\bigl(H-\lfloor\alpha B\rfloor+z^2\bigr).
\]

前節の平均値公式 `Σ_{B≤x}F(B)~F x` と部分和の Abel 変換により

\[
\sum_{B\le H/\alpha}F(B)(H-\alpha B)
\sim\frac{\mathcal F}{2\alpha}H^2.
\]

床関数誤差は `O(ΣF(B))=O(H)`、`z²ΣF(B)=o(H²)`。
`z=floor(sqrt(H)/log H)` とすれば `G(z)~E(log H)²/(8π²)`。
従って右辺は
`(4π² F/(αE)+o(1)) H²/(log H)²`。証明終。

独立の `q48_sieve_interval_audit_20261016.py` は傾き下界を
浮動小数点でなく `A>3B` と `A⁴−18A²B²+9B⁴>0` で判定し、
各 `B` に対する**短縮区間版**大篩の有限数値不等式を `H=80,160,320,640` で照合した。
この有限照合は解析的な極限証明の代用ではない。
