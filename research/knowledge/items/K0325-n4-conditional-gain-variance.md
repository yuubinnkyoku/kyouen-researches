---
id: K0325
title: 同じ合法数・利得総和でも利得分散でP率が異なる4×4完全層
kind: computation
status: computed
topics: [statistics, grundy]
aliases: [B269]
relations:
- type: depends_on
  target: K0001
  note: 標準4×4の全安全局面
artifacts:
- path: research/experiments/original-claims/scripts/round69_scope_witness_check.py
  role: verifier
  note: 利得を新規使用不能点数として全層集計
- path: research/experiments/original-claims/output/round69_scope_witness_check.json
  role: data
  note: 固定k4・合法4・利得総和6での条件付きP率
---

# 同じ合法数・利得総和でも利得分散でP率が異なる4×4完全層

u_S(p)=|L(S)\setminus({p}∪L(S∪{p}))|とする。k=4、|L|=4、Σu=6を固定し、全ラベル付き安全局面を列挙すると、u多重集合(1,1,2,2)は24局面すべてP、(0,2,2,2)は16局面中8局面P。前者は分散1/4、後者は3/4で、低分散側のP率が高い。

同じ石数・合法数・総和の条件付き有限層の存在を示す。全盤・全層の単調関係、因果効果、一般nでの分類器ではない。無条件平均による旧B269の反証はこの存在主張を否定しない。

