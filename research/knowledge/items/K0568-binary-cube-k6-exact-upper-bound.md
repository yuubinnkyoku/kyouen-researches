---
id: K0568
title: 二値六次元立方体の共七点禁止版の最大安全石数はK_6=9である
kind: proposition
status: needs-review
topics: [variants, geometry, maximum-safe]
aliases: []
relations:
- type: depends_on
  target: K0553
  note: d=6のd+3下界（9点証人）を前提とし、本項目で上界を追加する
- type: verifies
  target: K0553
  note: d=6の9点証人を前提としてK_6=9を確定する方向の上界
artifacts:
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/README.md
  role: log
  note: 手法・再現手順・証拠の意味と限界
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/build_k6_cnf.cpp
  role: solver
  note: C(64,7)個の7点部分集合の依存判定とCNF生成器（二算法照合つき）
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/build_k6_circuits.cpp
  role: solver
  note: 包含極小依存集合（circuit）の列挙とCNF生成器。fix0対称性削減つき
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/audit_frontier9.py
  role: verifier
  note: 9点証人の極大性（64頂点すべて禁止）の独立監査
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/results.json
  role: data
  note: 機械可読な主張・CNF統計・検証計画
scope: 二値六次元超立方体 V_6={0,1}^6 上で、相異なる7点が一つの実アフィン超平面に載ること（退化を含む）を禁止するゲームの最大安全石数。Grundy値・misère版・d≠6は対象外。
evidence: 下界はK0553のd=6, m=9証人（整数Bareissとmod検証器の両方で完全検証済み）。上界は「ちょうど10点選ぶ」CNFのUNSAT（CaDiCaL、包含極小依存集合版：4,160変数・19,484,942節）による予定。CNFの節集合の正しさは、依存7点組の列挙が二つの独立算法（mod 2^61-1とmod 1000000007）で621,216,192件すべて一致したこと、およびcircuit化が包含極小性に基づく同値変換であることに依存する。CaDiCaLによるUNSAT実行およびDRAT証明書のdrat-trimによる独立検証はいずれも一時領域上で進行中であり、完了・証明書の保全後にstatusをprovedへ更新する。
---

# 二値六次元立方体の共七点禁止版の最大安全石数は9

$V_6=\{0,1\}^6$ の64頂点上で、相異なる7点が一つの実アフィン超平面に載ること
（退化を含む）を禁止するゲームの最大安全石数 $K_6$ は

$$
K_6=9
$$

である。

## 下界

9点証人は K0553 の d=6, m=9 レコード。整数Bareiss（全 $\binom{9}{7}=36$ 小行列式）と
mod $2^{61}-1$ 掃き出しの両検証器で完全検証済み。

## 上界

10点の一般位置集合が存在しないことを、以下の有限計算で示す。

1. 全 $\binom{64}{7}=621{,}216{,}192$ 個の7点部分集合について、増広行列
   $(1,x)$ の $7\times7$ 行列の階数を mod $2^{61}-1$ で計算し、依存集合を列挙する。
   Hadamard限界 $7^{7/2}=907<2^{61}-1$ により整数特異性と同値。
   独立な第二算法（mod $1000000007$、別消去法）で621M件すべて一致した。

   依存点組数：4点 4,816、5点 311,360、6点 10,663,520、7点 255,036,992。

2. 包含極小依存集合（circuit）のみを禁止節とすれば同値であることを用い、
   circuit数 4点 4,816、5点 22,400、6点 1,052,800、7点 18,396,672 を得る。

3. 変数 $x_0,\dots,x_{63}$ に「ちょうど10点選ぶ」のSinz順序計数器
   （$x$ 側 at-most-10、$\neg x$ 側 at-most-54）と、circuitごとの節
   $\neg x_{a}\vee\cdots\vee\neg x_{g}$ を合わせたCNFを構成する。
   結果：4,160変数、19,484,942節。

4. CaDiCaLでUNSATを確認し、DRAT証明書を取得する。独立検証はdrat-trimで行う。

## 証拠の意味と限界

- 下界9点は二検証器で完全検証済み。
- 上界は有限CNFのUNSATに依存する。CNFの節集合の正しさは、依存7点組の
  二算法完全一致とcircuit化の同値性に依存する。
- DRAT証明書のdrat-trimによる独立検証が完了するまで status は needs-review。
  完了後に proved へ更新し、証明書を添付する。
- $d\neq6$ の上界、Grundy値、misère版は対象外。
