# rank ≤ 4・残余禁止辺3本以下のGrundy上界（2026-10-19）

## 結論と証拠の種類

有限通常プレイで、合法点集合上の包含極小残余禁止辺が高々3本、各辺が2〜4点の場合、

\[
\boxed{g\le 3}
\]

が成立する。上界は鋭い。標準共円ゲームの任意の合法局面では、残余辺の大きさは最大4なので、**残余極小辺が3本以下ならその局面のGrundy数は3以下**となる。

これは、任意の点数の局面を有限562場合へ厳密に帰着し、**2つの独立した有限完全列挙**で確認した計算機援用証明である。解析的な全称不等式のみで導いた結果ではない。

## 全称的な有限帰着

残余禁止辺がちょうど3本のとき、辺を E1,E2,E3 とする。いずれにも属さない自由点は他のゲーム成分から独立し、その個数を f とすると

\[
g(V,\{E_1,E_2,E_3\})=g(U,\{E_1,E_2,E_3\})\oplus(f\bmod2),\quad U=E_1\cup E_2\cup E_3.
\]

したがって \(|U|\le12\)。各点を、その点が所属する辺の番号の非空ビット集合 p∈{1,...,7} で分類し、個数を c_p とする。

\[
0\le c_p\le4,\quad
2\le\sum_{p:\,i\in p}c_p\le4\quad(i=1,2,3).
\]

包含極小性は、すべての i≠j について

\[
\sum_{p:\,i\in p,\ j\notin p}c_p\ge1
\]

と同値である。各条件を満たす整数7組は**562組**（3辺のラベルを区別）に限られる。異なる配置でも同じ c は交換可能な点の置換で同型になる。

残りの辺サイズを \(e_i(c)=\sum_{p:i\in p}c_p\) とし、\(u_p\) を p 番目だけ1の単位ベクトルとする。原始的な一点追加ゲームの厳密な帰納式は

\[
G(c)=\operatorname{mex}\{G(c-u_p):c_p>0,\ e_i(c)\ge2\ \text{for all }i\in p\}.
\]

辺が1点になった場合は、その最後の点を打てない。上式はその着手を除外しており、残余辺の削除・圧縮の実装を仮定しない。

3辺未満の局面には、元の点集合と独立な2点禁止辺を \(3-h\) 個追加すればよい。追加成分のGrundyは各1なので、新ゲームのGrundyは \(g\oplus((3-h)\bmod2)\)。集合 {0,1,2,3} は xor 1 で閉じるため、3辺の場合の上界から h=1,2 も従う。h=0 は自由点のみで g=f mod2。

## 完全列挙の結果

| G | 562組中の個数 |
|---:|---:|
| 0 | 228 |
| 1 | 231 |
| 2 | 49 |
| 3 | 54 |
| 4以上 | 0 |

最大辺サイズを2に制限すると9組で分布(3,3,0,3)、3に制限すると107組で分布(44,45,9,9)。上記562組は辺サイズ4まで許した場合。

## 鋭さ（抽象残余ゲーム）

5点 a,b,c,d,e の禁止辺を \(\{a,c\},\{b,c\},\{d,e\}\) とする。最初の2辺の3点ゲームは、cへの着手で子Grundy0、a/bへの着手で子Grundy1となり、mex{0,1}=2。最後の2点辺ゲームはGrundy1で、両成分の直和は \(2\oplus1=3\)。

この鋭さは**抽象残余ゲーム**についての証人であり、標準整数格子上のある合法局面でこの残余構造を実現できるかは別問題である。

## 独立検証と再現

- `scripts/three_edge_rank4_venn.py`: 7個の所属個数を状態とするmex再帰。5^7候補から562組を選別。
- `scripts/three_edge_rank4_subset.cpp`: 同じ562組を実際の最大12個のラベル付き点へ展開し、占有ビット集合に対して直接mexを計算。所属個数による再帰は使わない。
- `output/three_edge_rank4_result.json`: 集計・最小証人・unionサイズ別分布。
- `output/three_edge_rank4_cases.csv`: 全562組の `code,grundy`。codeは \(\sum_{p=1}^7 c_p 5^{p-1}\)。

repo rootで:

```sh
python research/experiments/game-structure/scripts/three_edge_rank4_venn.py
c++ -std=c++17 -O2 -Wall -Wextra -pedantic \
  research/experiments/game-structure/scripts/three_edge_rank4_subset.cpp -o /tmp/three_edge_rank4_subset
python research/experiments/game-structure/scripts/three_edge_rank4_venn.py --cases >/tmp/venn.csv
/tmp/three_edge_rank4_subset --cases >/tmp/subset.csv
cmp /tmp/venn.csv /tmp/subset.csv
sha256sum /tmp/venn.csv
```

562組の**全ケースごと**に両実装が一致した。CSVのSHA-256:

`f5603dbc59667ce58a1ded4d2f1d6d9d8dbddab1cd0ad7e7971cb0a106b91ad7`

## 適用範囲と次の問い

- 標準q=4の任意の合法局面に適用できるが、残余極小禁止辺が3本以下であることが必要。
- 4本以上の禁止辺に対する上界は主張しない。実際、抽象4辺ではGrundy4以上の例が存在する。
- 3辺でもrank5を許すとGrundy4の例があるため、rank4の条件は本結果に本質的である。
- 11×11探索の残局で、この条件の判定が高速化になるかは未測定。
- **幾何的に実現可能な残余辺3本のGrundy値の範囲**と、**4辺・rank4での最良上界**が次の実行可能な課題。
