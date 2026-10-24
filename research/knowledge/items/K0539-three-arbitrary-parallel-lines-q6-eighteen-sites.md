---
id: K0539
title: 任意三平行線の6点共円共線禁止は各線18候補で全終局15石となる
kind: proposition
status: proved
topics: [rectangles, geometry, variants, maximal-safe, grundy, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0478
  note: 18候補不足極大のE14剛性分類と被覆等号条件を独立代数監査で排除
- type: depends_on
  target: K0002
  note: 全終局の同一石数から全安全局面のmexを帰納計算
artifacts:
- path: research/experiments/q6-eighteen-sufficiency-20261024/proof.md
  role: proof
  note: 全実数の3族と固定正規形への完全帰着および被覆不可能性
- path: research/experiments/q6-eighteen-sufficiency-20261024/symbolic-certificate.json
  role: certificate
  note: 連続3族156条件の有理式・因数分解・符号排除証拠
- path: research/experiments/q6-eighteen-sufficiency-20261024/check_symbolic.py
  role: verifier
  note: 標準ライブラリ有理多項式による独立全恒等式・完全性・符号域検査
- path: research/experiments/q6-eighteen-sufficiency-20261024/fixed_independent.cpp
  role: verifier
  note: 固定四円4823組と混合候補11628個の独立整数監査
- path: research/experiments/q6-eighteen-sufficiency-20261024/run.py
  role: verifier
  note: Python・C++の全分類件数一致と証明書改変拒否を再現
- path: research/experiments/q6-eighteen-sufficiency-20261024/audit.json
  role: data
  note: 連続156条件と固定4823条件の完全一致receipt
solution:
  board: 任意三平行線・各線18候補以上
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 任意の実数位置の対象有限盤の全安全局面
  conditions: q=6の共円または共線禁止、完全指摘、通常プレイ
  verification: [mathematical-proof, independent-cpp-check]
  certificate: K0478のE14障害の全称排除、連続156有理式および固定4823四円組
  independent_check: SymPy生成証明書を標準ライブラリで再計算、固定型はPythonと独立C++が全件一致
  note: g(S)=(15−|S|) mod2。空盤先手勝ち・全初手勝ち。18の最小性は未主張
scope: 相異なる三平行線、各線に18個以上の任意の異なる実数候補点、6石共円または共線を禁止する通常プレイ。
evidence: K0478の剛性型を全称代数帰着で排除。有限部分は全パラメータを含む恒等式・連立式検査であり、有限格子標本の外挿ではない。
---

# 任意三平行線の18候補十分性

各線18候補以上なら、すべての極大安全配置は各線5石・合計15石。
全安全局面で `g(S)=(15−|S|) mod 2`、空盤は先手必勝で全初手が勝ち手となる。

K0478に残っていたenergy14の障害を、3連続族の156有理式と固定4823四円組の完全排除で閉じる。
中線上で交換交差円が同じ空点を塞ぐ場合は、14個の相異なる空点が必要という被覆条件で排除する。
有理式証明書はSymPyに依存しない別検査器で恒等式と符号域を検査し、固定型は独立C++でも照合した。

18は十分条件であり最小値とは主張しない。K0350の旧添付にある17候補改善案の採否には依存しない。
その17候補案はその後の監査を経て[K0541](K0541-three-arbitrary-parallel-lines-q6-seventeen-sites.md)で採用された。
標準整数格子のM3,6=9とは別の任意候補配置の命題である。
