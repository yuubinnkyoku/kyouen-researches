---
id: K0421
title: 四石以上の安全局面では子のD4同値と親安定化群の着手軌道が一致する（四石条件は鋭い）
kind: proposition
status: proved
topics: [geometry, search-methods, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円四点を含む集合は安全ではない
artifacts:
- path: research/experiments/n11-s5-s6-quotient-20261013/proof.md
  role: proof
  note: 位数2と四分回転を分ける全称証明・三石の鋭い反例
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/small_board_audit.py
  role: verifier
  note: 小盤の全安全集合と三石反例を照合
- path: research/experiments/n11-s5-s6-quotient-20261013/output/small-board-audit.json
  role: data
  note: n1..4全安全集合、n5の0..3石全集合、n11の三石反例
scope: 任意nの標準q=4安全集合Sで|S|≥4と合法追加p,q。D4不変な任意有限平面点集合のcircle-only q=4にも成立。
evidence: 全称数学的証明。非中心の四分回転軌道は共円四点ゆえ全占有できない。余分な子同値を生む回転は非中心二石以下を強制する。小盤完全照合と三石の存在反例を保存。
---

安全集合Sが四石以上なら、S∪{p}とS∪{q}のD4同値は、p,qが親の安定化群Stab_D4(S)の同じ軌道に属することと同値。
従って正準子数はBurnside公式で計算でき、親内の重複除去は安定化群の着手軌道代表だけで完全である。

全称証明はartifactのproof.mdにある。共線禁止を使わず、中心まわりのD4不変有限点集合のcircle-only q=4にも適用する。q>4やline-onlyへの適用は主張しない。

条件は一様に鋭い。11×11でS={60,69,83}の安定化群は自明、p=37とq=51は別の着手軌道だが両追加は合法で、子は90度回転で同値。113合法手が112正準子になる。

有限支持として1〜4盤の全安全集合2・15・298・5,811集合を照合し、四石以上で余分な同値はゼロ。5盤は0〜3石の全2,626集合のみを照合し、三石反例が8集合ある。有限検算を一般証明の代わりにしていない。

異なる親間の局面共有には全D4正準化が引き続き必要。勝敗・Grundy数・solver速度の改善・実装への適用はこの結果の範囲外。
