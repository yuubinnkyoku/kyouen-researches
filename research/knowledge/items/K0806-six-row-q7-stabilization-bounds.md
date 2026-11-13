---
id: K0806
title: 6×m・q=7の満容量安定化長は20以上402以下
kind: proposition
status: proved
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0318
  note: 曲線充填上界U_{w,q}への(6,7)代入による初の明示的上界402
- type: depends_on
  target: K0761
  note: 下界20は6×13/16/19の35石1行欠損極大安全配置の実在による
- type: depends_on
  target: K0024
  note: 従来の暗黙の一般上界T_{6,7}=10,101（402はその25分の1）
artifacts:
- path: research/experiments/six-row-q7-stabilization-upper-bound-20261113/scripts/six_row_q7_upper_bound.py
  role: verifier
  note: K0318 verbatim関数のインライン・3独立実装一致・制御再現・w=6小盤監査
- path: research/experiments/six-row-q7-stabilization-upper-bound-20261113/output/six_row_q7_upper_bound.json
  role: data
  note: 全検査結果・argmax・K0024再計算・U_{6,q}補助表
- path: research/experiments/six-row-q7-stabilization-upper-bound-20261113/report.md
  role: proof
  note: 代入の詳細・検証・限界
---

# 6×m・q=7の満容量安定化長は20以上402以下

標準六行整数格子の7点共円・共線禁止版について 20 ≤ M_{6,7} ≤ 402。
(w,q)=(6,7) は q>2w 全長定理・行分離帯（w=6 は q≥9 から）・
K0072/K0776 の既証明無限族のいずれの外側にあり、
K0761 の下界20のみが記録されていた空白である。

上界402は K0318 の曲線充填定理への代入。
r=6, N=30, Q=3960, d0=20, d1=10, Y=215 のもとで
H = max{2x+y : 20x+10y ≤ 3960, y ≤ 215} = 396（argmax x=198, y=0）、
U = 6+396 = 402。d0=2d1 のため予算効率が等しく、
q≥7 の系 M ≤ r + floor(2Q/C(r,3)) = 402 とちょうど一致する。
従来の暗黙の一般上界は K0024 の T_{6,7}=10,101。

検証は3独立実装（K0318 verbatim repo実装・期間短縪なしの全域y掃引・
閉形式の別実装）の完全一致に加え、既刊代入値 (3,5)=40・(5,6)=249・(5,7)=200
の制御再現、K0024 Tの独立再計算、6×3 全2^18 安全状態の予算不等式監査。
上界は全称証明によるもので有限SATのUNSATを根拠としない。

従って m ≥ 402 では全極大安全集合が36石で g(S)=(36−|S|) mod2。
補助として同じ代入を (6,q)・q=4..8 に実施し、
(6,5)≤658・(6,6)≤495・(6,8)≤371 の未記録だった片側上界も
results/fixed-width に反映した（(6,4) は 1,113 で旧Tと同一）。

M_{6,7} の厳密値は未解決のまま。402 は十分条件であり、
K0332 が (5,7) で 200→158 に改善したのと同様の同和弦energy等の
専用算術による縮小余地を残す。m=20..401 の各値も未解決。
