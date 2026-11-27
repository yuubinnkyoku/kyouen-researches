---
id: K1359
title: "PG(2,9) s=2 の完全 Grundy スペクトル — 総 128,917,712 局面、Grundy(∅)=0、最大 Grundy 2"
kind: computation
status: computed
topics: [grundy, geometry, variants]
aliases:
- PG(2,9) s=2 complete Grundy spectrum
- projective plane order 9 cap game Grundy distribution
relations:
- type: depends_on
  target: K1353
  note: 錐+二重計数法（transitivity plus one cone DP）
- type: related
  target: K1354
  note: AG(2,9) s=2 は最大 Grundy 3（本項の PG(2,9) は 2 で対照的）
- type: related
  target: K1300
  note: s パラメータ表の PG(2,9) s=2 行（完全分布が未計算だった）
- type: related
  target: K1303
  note: 完全 6/7/8/10-アーク単一軌道数の再現アンカー
- type: related
  target: K1304
  note: 全 3-キャップ G=1・全 4-キャップ G=0 の再現アンカー
- type: related
  target: K1298
  note: パリティ特性定理（混在 ⇒ G≥2、本項は G=2 ちょうどで打ち止め）
artifacts:
- path: research/experiments/pg2q9-s2-cone-spectrum-20261127/scripts/pg2q9_cone_spectrum.py
  role: verifier
  note: 盤二重構築・錐列挙・mex DP・q<=4 素朴全 DP 較正込み本体
- path: research/experiments/pg2q9-s2-cone-spectrum-20261127/scripts/verify_pg2q9.py
  role: verifier
  note: G1..G6 ゲート + T1..T5 tamper battery（rc=0 PASS）
- path: research/experiments/pg2q9-s2-cone-spectrum-20261127/output/spectrum_q9.json
  role: data
  note: 主結果（スペクトル・極大個数・Grundy(∅)）
- path: research/experiments/pg2q9-s2-cone-spectrum-20261127/output/spectrum_q3.json
  role: data
  note: q=3 較正（錐法 ≡ 素朴 2^13 全 DP）
- path: research/experiments/pg2q9-s2-cone-spectrum-20261127/output/spectrum_q4.json
  role: data
  note: q=4 較正（素朴全 DP + 出版 PG(2,4) s=2 値一致）
- path: research/experiments/pg2q9-s2-cone-spectrum-20261127/output/audit_q9.json
  role: data
  note: ゲート/tamper レポート（gates 6/6 PASS・tamper 5/5 fail-closed）
scope: PG(2,9)（91点・91直線・各直線10点）の s=2 共演ゲーム（各直線上高々2点・1手1点追加・追加不能が終局・通常プレイ）の全安全局面（アーク）の Grundy 分布。
evidence: 錐+二重計数法（K1353）。非共線3点 F を含む全アーク 31,681 局面を visited-set DFS で完全列挙し mex DP、PGL(3,9) の非共線3点推移性より N_m(g)=N_3·T_m(g)/C(m,3)（N_3=110,565）。較正 q=3/4 で錐法≡素朴全 DP、出版アンカー 5 点（総数 128,917,712・N_3=110,560+5 全G1・N_4=1,769,040 全G0・N_5=14,859,936・完全 6/7/8/10-アーク 707,616/2,021,760/5,307,120/58,968）bit-exact 一致、異なる3つの F で T 表同一、決定性 3 走同一、子/mex 300 サンプル別実装一致、tamper 5/5 fail-closed。
---

# PG(2,9) s=2 の完全 Grundy スペクトル

| size | G=0 | G=1 | G=2 |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 0 | 91 | 0 |
| 2 | 4,095 | 0 | 0 |
| 3 | 0 | 110,565 | 0 |
| 4 | 1,769,040 | 0 | 0 |
| 5 | 0 | 14,859,936 | 0 |
| 6 | 37,857,456 | 0 | 14,152,320 |
| 7 | 2,021,760 | 49,533,120 | 0 |
| 8 | 7,960,680 | 0 | 0 |
| 9 | 0 | 589,680 | 0 |
| 10 | 58,968 | 0 | 0 |

- 総 128,917,712 局面。**Grundy(∅)=0**（先手必敗）。**最大 Grundy 2**（サイズ6限定）。
- 極大サイズはちょうど {6,7,8,10}。偶奇混在なので K1298 の定理より G≥2 が必然で、
  実測はちょうど G=2 まで（G=3 以上は q=9 projective 盤では不存在）。
- AG(2,9) s=2 の最大 Grundy 3（K1354）と対照的で、projective 化で G=3 が消える。
