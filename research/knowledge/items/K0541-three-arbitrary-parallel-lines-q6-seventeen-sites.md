---
id: K0541
title: 任意三平行線の6点共円共線禁止は各線17候補で全安全局面を偶奇強解決できる
kind: proposition
status: proved
topics: [rectangles, geometry, variants, maximal-safe, grundy, first-moves, verification]
aliases: []
relations:
- type: depends_on
  target: K0478
  note: 二点和energy14の剛性分類と5点二点和復元
- type: depends_on
  target: K0342
  note: 4点・5点の同和弦energy上界
- type: generalizes
  target: K0539
  note: 各線18候補の十分条件を17候補へ緩める。18候補の独立代数証明は別途有効
artifacts:
- path: research/experiments/three-parallel-q6-17-20261018/proof.md
  role: proof
  note: 四円共有点補題・E13分類・17候補十分性の旧証明案
- path: research/experiments/q6-seventeen-audit-20261024/audit.md
  role: proof
  note: 旧案の全実数帰着と枝刈り・特殊有理数範囲の論理監査、条件外の四円反例
- path: research/experiments/q6-seventeen-audit-20261024/run.py
  role: verifier
  note: 旧Pythonと独立C++の全有限部分を再実行し件数・結論を照合
- path: research/experiments/q6-seventeen-audit-20261024/audit.json
  role: data
  note: 参照旧ソースSHA256と3族各544記号候補・6173662有理候補・AP5005候補の再実行receipt
solution:
  board: 任意三平行線・各線17候補以上
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 任意の実数位置の対象有限盤の全安全局面
  conditions: q=6の共円または共線禁止、完全指摘、通常プレイ
  verification: [mathematical-proof, independent-cpp-check]
  certificate: E13以上での一点三円上界、E12以下の円予算から不足線の利用不能点を16以下へ抑える
  independent_check: 旧Pythonと独立C++の全記号候補・有理候補の再実行一致。全称帰着も別途論理監査
  note: 全終局15石、g(S)=(15−|S|) mod2。空盤先手勝ち・全初手勝ち。17の最小性は未主張
scope: 相異なる三平行線、各線に17個以上の任意の異なる実数候補点、6石共円または共線を禁止する通常プレイ。
evidence: 旧17候補案の全称帰着を2026-10-24に監査し、全有限部分をPython・独立C++で再実行。有限標本の外挿ではない。
---

# 任意三平行線の17候補十分性

各線17候補以上なら全終局は各線5石、計15石。
全安全局面で `g(S)=(15−|S|) mod 2`、空盤は先手必勝で全初手が勝ち手となる。

四円が二本の各5点以下の線外の一点を共有するには、全円対が二線上でちょうど1点を共有する必要がある。
この必要条件と二点和energyの全称分類を用い、E13,14,16の一点四円を排除する。
E13の実数族は記号的な一般点と有限個の特殊有理数へ完全帰着し、6173662候補を独立再検査した。
不足線の占有点込みの利用不能点は16以下となるため、17候補で常に延長できる。

旧案はK0350の添付に未採用で保持されていた。本項目は全称帰着の監査と独立再実行により採用する。
旧experimentの原文は当時の一次資料として保持する。

17は最小値とは主張しない。16候補の一様十分性は未解決。
またE≥13を外した一点三円上界は偽で、E6で一点四円となる明示実数配置を監査資料に含める。
