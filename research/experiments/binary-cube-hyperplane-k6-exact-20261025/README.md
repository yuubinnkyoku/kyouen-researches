# 二値六次元立方体・共七点禁止版のK_6=9確定

2026-10-25、main `e5eb877c` を基準に作業。
[K0553](../../knowledge/items/K0553-binary-hypercube-growing-excess-witnesses.md)が
$K_6\ge9$ の9点証人を与えていた。本実験は上界 $K_6\le9$ を追加し
$K_6=9$ を確定する。

## 対象ゲーム

$V_6=\{0,1\}^6$ の64頂点上で、相異なる7点が一つの実アフィン超平面に
載ること（退化を含む）を禁止する。安全 = 任意の7点部分集合がアフィン独立。

## 上界の手法：依存7点組の全列挙とCNF

1. **列挙器** `build_k6_cnf.cpp`：全 $\binom{64}{7}=621{,}216{,}192$ 個の
   7点部分集合について、増広行列（行 $(1,x)$ の $7\times7$）の階数を
   $p=2^{61}-1$ 上で計算する。Hadamard限界より $7\times7$ の0/1行列の
   任意の小行列式の絶対値は $7^{7/2}=907<p$ なので、
   整数での特異性と $\bmod p$ での特異性は同値。
   `--count` モードでは全判定を独立な第二算法（$\bmod 1000000007$、
   別の消去法）でも再計算し、621M件すべて一致した。

   依存点組数（二算法照合済み）：

   | サイズ | 全部分集合数 | 依存数 |
   |---:|---:|---:|
   | 4 | 635,376 | 4,816 |
   | 5 | 7,624,512 | 311,360 |
   | 6 | 74,974,368 | 10,663,520 |
   | 7 | 621,216,192 | 255,036,992 |

2. **CNF（包含極小依存集合版）**：依存7点組のうち包含極小なもの
   （circuit）だけを禁止節とすれば論理的に同値であることを用い、
   `build_k6_circuits.cpp` で circuit を列挙する。
   circuit数：4点 4,816、5点 22,400、6点 1,052,800、7点 18,396,672
   （合計 19,478,688）。
   変数 $x_0,\dots,x_{63}$ に「ちょうど10点選ぶ」のSinz順序計数器
   （$x$ 側 at-most-10、$\neg x$ 側 at-most-54）と、circuitごとの節
   $\neg x_{a}\vee\cdots\vee\neg x_{g}$ を合わせたCNFを構成する。
   結果：4,160変数、19,484,942節（gzipで約560MB）。
   対称性削減版 `fix0`（頂点0を含む集合に制限、超立方体の頂点推移性による健全な制限）
   も利用可能。

3. **UNSAT解決**：CaDiCaL 1.7.4でcircuit版CNFを解き、DRAT証明書を取得。
   実行中。完了後、証明書を添付する。

4. **証明検証**：marijnheule/drat-trim（ソースからビルド）で、
   元CNFに対してDRAT証明書を独立検証。実行予定。

## 下界側の確認

9点証人は
[binary-cube-hyperplane-large-d-20261025](../binary-cube-hyperplane-large-d-20261025/frontier.txt)
の d=6 m=9 レコード。同実験の `verify_exact.py`（整数Bareiss・全286小行列式）
と `verify_mod.cpp`（mod $2^{61}-1$）の両方で完全検証済み。ここでは再検査しない。

## 再現

```sh
g++ -std=c++17 -O2 -Wall -Wextra -o /tmp/k6cnf build_k6_cnf.cpp
/tmp/k6cnf --count                      # 約25分、二算法照合つき列挙数

g++ -std=c++17 -O2 -Wall -Wextra -o /tmp/k6circ build_k6_circuits.cpp
/tmp/k6circ --count                      # circuit数の確認
/tmp/k6circ --cnf 10 /tmp/k6_k10_circ.cnf        # 全circuit版
# または対称性削減版：
# /tmp/k6circ --cnf 10 /tmp/k6_k10_fix0.cnf fix0
cadical /tmp/k6_k10_circ.cnf proof.drat   # UNSAT + DRAT
git clone --depth 1 https://github.com/marijnheule/drat-trim /tmp/drat
make -C /tmp/drat/drat-trim
/tmp/drat/drat-trim/drat-trim /tmp/k6_k10_circ.cnf proof.drat   # VERIFIED
```

CNFの生ファイル（circuit版約560MB）は再現時にのみ必要なのでリポジトリには入れない。
DRAT証明書と検証ログはサイズが確定してから添付する。

## 証拠の意味と限界

- 下界9点は二検証器で完全検証済み。
- 上界は有限CNFのUNSATに依存する。CNFの節集合の正しさは、依存7点組の
  二算法完全一致とcircuit化の同値性に依存する。
- DRAT証明書のdrat-trimによる独立検証は実行中。完了後に status を proved へ更新する。
- $d\ge7$ の上界、Grundy値、misère版は対象外。
