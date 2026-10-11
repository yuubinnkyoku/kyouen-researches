---
id: K0402
title: 33本の非原始二重点行の初出幅 F(33) は631〜743
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/nonprimitive-33-double-rows-bounds-20261010.md
  role: proof
  note: 全称下界と幅743の構成
- path: research/experiments/fixed-width/reports/nonprimitive-33-exact-spans-561-574.md
  role: proof
  note: 561〜574幅排除
- path: research/experiments/fixed-width/reports/nonprimitive-33-exact-spans-575-594.md
  role: proof
  note: 575〜594幅排除
- path: research/experiments/fixed-width/reports/nonprimitive-33-exact-spans-595-616.md
  role: proof
  note: 595〜616幅排除
- path: research/experiments/fixed-width/reports/nonprimitive-33-exact-spans-617-624.md
  role: proof
  note: 617〜624幅排除
- path: research/experiments/fixed-width/reports/nonprimitive-33-exact-spans-625-630.md
  role: proof
  note: 625〜630幅排除
- path: research/experiments/fixed-width/scripts/verify_nonprimitive_33_rows_560.cpp
  role: verifier
  note: 560幅までの合同排除を2方式で照合
- path: research/experiments/fixed-width/scripts/check_nonprimitive_33_rows_743.py
  role: verifier
  note: 明示33行の整数点検査
- path: research/experiments/fixed-width/output/nonprimitive_33_rows_560_audit.log
  role: data
  note: 560幅監査記録
scope: 標準整数格子の非原始二重点行、k=33
evidence: 平方剰余必要条件の完全排除と明示円証人。
---

`F(33)` を、円が異なる整数格子点を2点ずつ持つ33本の水平行から、行差gcdが2以上となる選択を収める最小連続幅とする。現在確定しているのは `631<=F(33)<=743`。

下界は560幅までの完全合同排除と、幅561〜630の区間ごとの候補排除。上界は円 `x²+y²=143650` の33行証人（最小行−379、最大行363、gcd=2）による。従ってF(33)=743とは主張しない。有限化は円係数・半径に上限を置かず、平方剰余の必要条件を用いる。

631〜742幅が未排除なので結果は上下界である。二方式の合同マスク照合と整数平方根による証人検査を根拠とする。
