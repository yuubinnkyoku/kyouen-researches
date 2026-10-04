---
id: K0339
title: r人巡回配置ゲームで敗者が戦略に依存しない人数は極大サイズ差のgcdで完全に決まる
kind: proposition
status: proved
topics: [variants, strategy-length, maximal-safe]
aliases: []
relations:
- type: generalizes
  target: K0305
  note: 全極大サイズの偶奇構造を全rの終端プレイヤー固定へ拡張する
- type: depends_on
  target: K0024
  note: 固定幅q点版の全r系にのみ使う既存の満容量定理
- type: depends_on
  target: K0025
  note: q>2wでの全長系にのみ使う
artifacts:
- path: research/experiments/game-structure/reports/multiplayer-modulus-20261005.md
  role: proof
  note: 全rの必要十分条件、直和gcd公式、固定幅への系
- path: research/experiments/game-structure/scripts/multiplayer_modulus_20261005.py
  role: verifier
  note: 全4頂点以下の下方閉族と小盤の直接継続DAGによる独立検算
- path: research/experiments/game-structure/output/multiplayer_modulus_20261005.json
  role: data
  note: 194族・37636直和・標準1..4盤での照合
scope: 有限下方閉配置ゲーム、r≥2人巡回、最初に合法手を失う一人を敗者として終了
evidence: 全称数学的証明、有限全列挙による独立検算
---

# r人版の全称mod r定理

有限下方閉配置ゲームの極大集合Tのサイズ差のgcdをΔとする。同サイズのみならΔ=0。
最初に合法手がなくなった一人を敗者とするr人巡回対戦では、全ての合法対局で敗者が同じことと
rがΔを割ることが同値。これは空盤だけでなく全安全局面で同じ保証が成立する条件でもある。
Δ=0なら全r、Δ≥2ならr≥2の約数だけ、Δ=1ならどのrでもこの保証は成立しない。

独立部品の直和のΔは部品Δのgcdに等しい。二人Grundyのxorを多人版へ適用する主張ではない。

固定幅q点版で全極大石数がC=(q−1)wに安定した領域はΔ=0で、既存の長さ条件のまま全rへ延長できる。
安全Sからプレイヤーaが着手するなら敗者は(a+C−|S|) mod r。
q>2wの全長領域ではC=w min(m,q−1)を使う。

規則は一人の敗者を決めてそこで終了する。唯一の勝者や、敗者除外後の継続や、連合戦略の分類は主張しない。
