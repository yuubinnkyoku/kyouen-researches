---
id: K0094
title: 二手情報を保つ一石移動で5×5のgが0から3へ変わる
kind: proposition
status: proved
topics:
- residual-games
- grundy
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/verification/structural-lemmas-2026-10-02/three-ply-equivalence.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/structural-lemmas-2026-10-02/checks/independent_lookahead.json
  role: data
  note: 旧証人と小盤の独立合法性検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/structural-lemmas-2026-10-02/checks/relocation_verified.json
  role: data
  note: 5×5全数と一石移動の検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 二手情報を保つ一石移動で5×5のgが0から3へ変わる

S=[1,3,5,6,11]、T=[1,3,5,11,17]は安全5石。L=[4,20,22,24]と二点制約が同じで、三点制約一個の差によりg0対3。全16追加集合の違いは{4,22,24}だけ。

n≤4の全6126安全局面では(L,P)が全Rを決め、二手情報不足の最小正方形盤は5。四合法点で最大差3の抽象二型を分類し、格子上では第二型を実現。旧B052の16混在群と新全数32群の差の理由は未監査。
