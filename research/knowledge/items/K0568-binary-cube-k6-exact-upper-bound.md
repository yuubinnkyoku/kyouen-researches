---
id: K0568
title: 二値六次元立方体の共七点禁止版の最大安全石数はK_6=9である
kind: proposition
status: scope-unclear
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
  note: C(64,7)個の7点部分集合の依存判定とCNF生成器（二算法照合つき）。こちらは依存7点組全部を禁止する正しいCNF
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/build_k6_circuits.cpp
  role: solver
  note: 包含極小依存集合（circuit）列挙とCNF生成器。d=6のcircuit削減は包含極小にならないため証明には使用不可（K0591の教訓）
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/audit_frontier9.py
  role: verifier
  note: 9点証人の極大性（64頂点すべて禁止）の独立監査
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/verify_k9_witness.py
  role: verifier
  note: exactly-9 CNFのSAT証人9点の幾何学的再検証
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/results.json
  role: data
  note: 機械可読な主張・CNF統計・検証計画
scope: 二値六次元超立方体 V_6={0,1}^6 上で、相異なる7点が一つの実アフィン超平面に載ること（退化を含む）を禁止するゲームの最大安全石数。Grundy値・misère版・d≠6は対象外。
evidence: 下界9点はK0553の証人（二検証器で完全検証済み）。上界は未確定：完全版CNF（依存7点組全部255,036,992節）のUNSAT実行はメモリ19GB環境で未完。circuit削減CNFは包含極小化の誤用のため証明に使えず、そのkissat実行も8h10mでSIGTERM終了し判定は得られていない（K0591参照）。9点証人の極大性とexactly-9 SAT制御は確定済み。
---

# 二値六次元立方体の共七点禁止版の最大安全石数は9（上界未確定）

$V_6=\{0,1\}^6$ の64頂点上で、相異なる7点が一つの実アフィン超平面に載ること
（退化を含む）を禁止するゲームの最大安全石数 $K_6$ について、
下界 $K_6\ge9$ は確定しているが、上界 $K_6\le9$ は**未確定**である。
2026-10-30現在、本項目は K_6=9 を確定した主張としては扱えない。

## 下界（確定）

9点証人は K0553 の d=6, m=9 レコード。整数Bareiss（全 $\binom{9}{7}=36$ 小行列式）と
mod $2^{61}-1$ 掃き出しの両検証器で完全検証済み。
さらに `audit_frontier9.py` により、この9点証人が64頂点すべてを禁止する
（極大配置である）ことを独立確認した。

## 上界（未確定）

10点の一般位置集合が存在しないことの証明として、以下を準備した。

1. 依存7点組の完全列挙：全 $\binom{64}{7}=621{,}216{,}192$ 個の7点部分集合を
   二つの独立算法（mod $2^{61}-1$ と mod $1000000007$）で判定し完全一致。
   依存7点組は255,036,992個。これは包含極小禁止集合の全体でもある
   （7点未満の依存はゲームでは合法なため、circuit削減は不可能）。

2. 完全版CNF：4,160変数・255,045,246節（生6.9GB）。
   19GB環境のCaDiCaLではメモリ不足で未完。**UNSAT確定には至っていない。**

3. かつて作成したcircuit削減CNF（19,484,942節）でのkissat実行は、
   8h10mでSIGTERM終了しUNSAT判定は得られていない。そもそも非circuitの
   依存7点組（依存6点を含む7点組）を禁止していないため証明として無効
   （[K0591](K0591-binary-cube-d5-strong-solution-verification.md)の教訓）。

4. 制御として、exactly-9 CNFはSATであり、kissatの解
   {11, 22, 28, 37, 42, 49, 57, 58, 63} が全36小行列式非零と
   `verify_k9_witness.py` で確認済み。

## 証拠の限界

- 上界は未証明。9点の極大性（単一証人）は上界の根拠にならない。
- $d\neq6$ の上界、Grundy値、misère版は対象外。
