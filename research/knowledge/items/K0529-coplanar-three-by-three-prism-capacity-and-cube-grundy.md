---
id: K0529
title: 3×3×m・4点共面禁止版の最大石数は3,6,8,8,9で、3立方は全局面強解決
kind: proposition
status: proved
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations: []
artifacts:
- path: research/experiments/coplanar-3x3xm-q4-20261024/proof.md
  role: proof
  note: 全mの容量上界と構成、m≤4の有限排除、3立方の強解決
- path: research/experiments/coplanar-3x3xm-q4-20261024/verify.py
  role: verifier
  note: 4×4行列式の24項展開によるm≤3全安全局面の完全生成とmex
- path: research/experiments/coplanar-3x3xm-q4-20261024/independent.cpp
  role: verifier
  note: 独立した3×3整数行列式と全合法手再帰でm≤3を検証
- path: research/experiments/coplanar-3x3xm-q4-20261024/height_audit.py
  role: verifier
  note: m=3,4の9柱高さ割当の完全列挙とm=5の明示証人検算
- path: research/experiments/coplanar-3x3xm-q4-20261024/search9.cpp
  role: verifier
  note: C++による9柱の独立枝刈り探索と最初の構成の再現
- path: research/experiments/coplanar-3x3xm-q4-20261024/results.md
  role: data
  note: 両言語の独立一致集計、9柱高さ割当の全件数と初手分類
scope: 3×3×m整数格子・4点共面のみ禁止・全m≥1のKとs、m=3の全安全局面通常・misère
solution:
  board: 3×3×3・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全72,204安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、m=3
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 全2^27部分集合を安全集合の昇順生成で網羅し72,204局面を完全再帰
  independent_check: Pythonの4×4行列式展開とC++の外積式が全局面のg/h分布まで一致
  note: g(空)=2、h(空)=1、通常は中央以外26初手勝ち、misèreは全27初手勝ち。全mのK=3,6,8,8,9（m≥5は9）、s=3
---

# 3×3×mの共面4点禁止版

全m≥1で最小極大石数は3。最大安全石数はm=1で3、m=2で6、m=3,4で8、m≥5で9である。4石以上の安全配置に3点共線はなく、二重の鉛直柱を持つ場合は少なくとも2本の柱が空になるので8石以下。9石なら9本の柱に各1石。m=3,4ではその高さの全割当を完全排除し、m=5では9石の明示配置を検算した。したがって最大安全石数9の真の開始長は5。

3×3×3では禁止4点組2918、安全局面72204、極大局面の石数別個数は3石49、5石2644、6石14616、7石752、8石16。通常空盤Grundy値は2、misère補助mexは1。通常版は中央初手だけ負け、残る26初手は勝ち。misère版は27初手すべて勝ち。最大8石配置16個は立方体対称性の下で1軌道。

[全称証明、独立した完全列挙、再現手順](../../experiments/coplanar-3x3xm-q4-20261024/proof.md)。有限盤の強解決をm≥5の全局面に拡張するものではない。[K0526](K0526-cube-coplanar-four-all-safe.md)・[K0527](K0527-coplanar-prism-all-length-strong-solution.md)の2×2断面の結果とは別の定理である。
