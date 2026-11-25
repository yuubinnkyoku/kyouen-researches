---
id: K0576
title: 余補一型のq点禁止ゲームは全安全局面の通常・misère値と全勝ち初手に閉公式を持つ
kind: proposition
status: proved
topics: [variants, grundy, first-moves, residual-games, maximal-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常Grundyと終局1のmisère補助mexの定義
artifacts:
- path: research/experiments/co-singleton-forbidden-qplus1-20261031/proof.md
  role: proof
  note: 余補一型の全称mex帰納法、両ルールの全勝ち初手、極大配置と履歴の公式
- path: research/experiments/co-singleton-forbidden-qplus1-20261031/verify.py
  role: verifier
  note: N=3..10の全非空F・全安全局面を禁止集合の直接再帰で独立検査
scope: N=q+1≥3点、空でないF⊆V、禁止q点集合が正確に{V\{v}:v∈F}、通常・misère二人一点追加ゲームの全安全局面
evidence: 全称mex帰納法。N=3..10の全2032族、全1384796安全局面と18372初手を独立部分集合再帰で照合（不一致0）。整数格子への実現は主張しない。
---

# 余補一型の禁止集合族の全Grundy値

有限集合Vの大きさをN=q+1≥3、FをVの空でない部分集合とし、禁止辺をちょうどVからFの各点を1個除いたq点集合とする。合法局面Sの残点数をr、残るF点数をaとする。合法局面はr≥2、またはr=1,a=0に限る。

通常Grundy値gは、r=1なら0。r=2k（k≥1）ならa≤kのとき1、a≥k+1のとき0。r=2k+1（k≥1）ならa≤kのとき0、a=k+1のとき2、a≥k+2のとき1。**misère補助mex値hは全安全局面でgの0と1を交換し、2を保存する。**

したがって空盤の両値はNと|F|のみで決まり、全勝ち初手もF側・非F側の二種類に分けて定数時間の不等式で分類できる（詳細はproof.md）。通常・misère値はともに2以下。

終局集合は、Fの二点を残すN−2点集合がC(|F|,2)個と、非Fの一点を残すN−1点集合がN−|F|個だけ。全合法着手履歴数はC(|F|,2)(N−2)!+(N−|F|)(N−1)!。

全称性はresearch/experiments/co-singleton-forbidden-qplus1-20261031/proof.mdのmex帰納法による。独立の部分集合再帰research/experiments/co-singleton-forbidden-qplus1-20261031/verify.pyでN=3..10の全2032族・1384796安全局面・18372初手を照合し不一致0。これは[K0537](K0537-uniform-forbidden-absorbing-subset-sharp-strategies.md)の鋭さ反例に現れる族の全局面強解決だが、任意のq点禁止族や標準整数格子への一般化を主張しない。
