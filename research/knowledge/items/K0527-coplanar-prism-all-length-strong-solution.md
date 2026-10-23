---
id: K0527
title: 2×2×mの4点共面禁止版はm≥3で全局面Grundy偶奇則、極大石数3・5
kind: proposition
status: proved
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常Grundy値と終局の定義
- type: depends_on
  target: K0526
  note: m=2の境界結果。m=2では偶奇則は不成立
artifacts:
- path: research/experiments/coplanar-prism-2x2xm-20261024/proof.md
  role: proof
  note: 任意のm≥3についての全称幾何学的証明と境界盤
- path: research/experiments/coplanar-prism-2x2xm-20261024/verify.py
  role: verifier
  note: 整数外積による禁則生成と全安全局面mex
- path: research/experiments/coplanar-prism-2x2xm-20261024/independent.cpp
  role: verifier
  note: 独立した4×4行列式展開と全局面再帰
- path: research/experiments/coplanar-prism-2x2xm-20261024/results.txt
  role: data
  note: m=1〜12の二方式一致結果
scope: 3次元2×2×m整数格子頂点盤、4点共面禁止、通常・misère、全整数m≥3と境界m=1,2
solution:
  board: 2×2×m・4点共面禁止
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥3の全安全局面、m=1,2は別途境界分類
  conditions: m≥3は通常先手勝ち・misère後手勝ち、m=2はK0526参照
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 幾何学的な全称証明とm=1〜12の完全列挙
  independent_check: C++の直接4×4整数行列式とPython外積判定が一致
  note: m≥3ではK=5,s=3、全局面g=(5-|S|) mod 2、misère補助値h=1-g
---

# 2×2×mの共面4点禁止版の全長強解決

任意の整数m≥3で、4本の鉛直柱の任意の2本は同一平面にあるため、6石以上の安全配置は存在しない。一方5石安全配置は2×2×2の明示配置を埋め込める。3石の極大配置は鉛直柱の共線三石に限られ、その個数は 4*C(m,3)。4石安全配置は必ず5石まで延長できる。

このため、全安全局面について通常 g(S)=(5-|S|) mod 2、misère補助mex h(S)=1-g(S) が成立する。通常空盤は先手必勝、misère空盤は後手必勝。m=2では通常空盤も後手必勝（[K0526](K0526-cube-coplanar-four-all-safe.md)）であり、m=3が通常版の真の開始長。

[全称証明・独立検証器・m≤12の層別計算](../../experiments/coplanar-prism-2x2xm-20261024/proof.md)。有限列挙の範囲と無界証明を区別する。共球5点禁止版への転用はしない。
