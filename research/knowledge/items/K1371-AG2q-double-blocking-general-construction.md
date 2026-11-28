---
id: K1371
title: AG(2,q) 最小2重ブロッキングの一般構成と有限決定・軌道分類
kind: proposition
status: proved
topics: [blocking-sets, finite-geometry, sat]
aliases: [AG2 double blocking general construction, q7 double blocking SAT]
relations:
- type: depends_on
  target: K1370
  note: t2-blocking-duality-20261128の計数・出版mask リストと既知最小値を入力・較正に使用
- type: depends_on
  target: K1365
  note: minimal/maximal 補集合対応の全件再確認
artifacts:
- path: research/experiments/min-double-blocking-structure-q7-20261128/README.md
  role: summary
  note: 一般構成・AG(2,7)/PG(2,7) SAT境界・AG(2,4)/(2,5) 軌道分類の全体要約
- path: research/experiments/min-double-blocking-structure-q7-20261128/scripts/boards.py
  role: verifier
  note: GF(q)盤独立構成・2-(v,q+1,1) design検査・出版盤照合
- path: research/experiments/min-double-blocking-structure-q7-20261128/scripts/sat_min.py
  role: verifier
  note: 素朴SAT encoder。PG(2,3..5)/AG(2,4..5) 既知境界の完全較正
- path: research/experiments/min-double-blocking-structure-q7-20261128/scripts/sat2.py
  role: verifier
  note: 場合分解SAT (case A4..A8/B/C)。妥当性はmodule docstring
- path: research/experiments/min-double-blocking-structure-q7-20261128/scripts/classify.py
  role: verifier
  note: 定義再検証 + AGL(2,q) 軌道完全分割
- path: research/experiments/min-double-blocking-structure-q7-20261128/scripts/canonical_construction.py
  role: proof
  note: 一般構成 (char 2: 3q-2 / 奇素域: 3q-1) の全q機械検証
- path: research/experiments/min-double-blocking-structure-q7-20261128/scripts/triangle_construction.py
  role: proof
  note: 反並行線3本共有点 ⟺ char 2 補題の正準座標証明スケッチと全三角形機械確認
- path: research/experiments/min-double-blocking-structure-q7-20261128/out/
  role: data
  note: boards.json, calibration, ag7_k*.txt, classify_*.json, canonical_construction.json, open_cnf/*.cnf (sha256先頭8桁: ag7_k19_A5 0616d483/A6 f5949a89/A7 e5d479fa/A8 75c9929b/pg7_k20_A 19abb8ba/B d901367d)
- path: research/log/2026-11-28-min-double-blocking-structure-q7.md
  role: log
  note: 実行・検証・開示・non-claims・リジューム候補
- path: research/log/2026-11-28-min-double-blocking-structure-q7-declaration.md
  role: log
  note: publish-then-execute 宣言 (commit 33dbc5ea)
scope: >-
  アフィン平面 AG(2,q) (q=3,4,5,7,8,9) における 2 重ブロッキング集合
  (全直線が C と ≥2 点で交わる) の明示的上界構成、AG(2,3)/AG(2,7)/PG(2,7) の
  SAT による有限サイズ決定、AG(2,4)/AG(2,5) の最小 2 重ブロッキング全体の
  AGL(2,q) 軌道分類。
evidence: >-
  (1) 一般構成: 三角形 (y=0, x=0, x+y=1) + 反並行線 (y=1, x=1, x+y=0)。
  char 2 では 3 反並行線が (1,1) で共有点を持ち |C|=3q-2、奇素域では
  (1,1)∈D1∩D2 と (1,-1)∈D3 の 2 点追加で |C|=3q-1。全直線 ≥2 を q=3,4,5,7,8,9
  で定義直接機械検証 (canonical_construction.py)。補題「三角形の反並行線3本の
  共有点存在 ⟺ char 2」は正準座標で示され (D1∩D2=(1,1) が x+y=0 上 ⟺ 2=0)、
  全三角形の AGL 共役性 (安定化群 6) により全三角形に波及、q=3..7 の
  全三角形走査で機械確認 (q=4: 480/480 共有点、q=3,5,7: 0)。既知最小値
  q=3:8=3q-1, q=4:10=3q-2, q=5:14=3q-1 と一致し、新規上界 AG(2,7)≤20,
  AG(2,8)≤22, AG(2,9)≤26。(2) SAT 決定 (kissat 4.0.4, repo pin 同一バイナリ、
  encoder は PG(2,3..5)/AG(2,4..5) の既知境界で較正済み): AG(2,3) min=8
  (k≤7 全 UNSAT・k=8 SAT)。AG(2,7) min∈{19,20}: k=14 case C UNSAT により
  2-ovoid 非存在、k=15..18 全 UNSAT、k=19 case B/A4 UNSAT・A5-A8 は INDET
  (open, CNF 出版)、上界 20 は局所探索 witness (定義検証済み) と一致。
  PG(2,7) min∈[15,21]: k=21 SAT、k≤20 は INDET (CNF 出版)。(3) 軌道分類
  (出版 mask 全件を blocking+minimality 定義再検証の上): AG(2,4) 168 個
  (10:48, 12:120) は 2 軌道のみ。size-10 正準形は 5 本の dual arc の
  10 個の対交点集合 (union=対交点集合=C を機械検証)。AG(2,5) 49,500 個は
  9 軌道のみ (14: 6000+3000, 15: 12000+12000+4000, 16: 6000+3000+2000+1500)。
  size-14 の 3000 軌道は dual arc 型 (full line 4 本)、6000 軌道は三角形+2点型。
  minimal↔maximal 補整合は全件一致。
---

## 命題・範囲

K1371 は有限アフィン平面 AG(2,q) の 2 重ブロッキング集合に関する 3 種の成果:
(q 任意の) 明示的上界構成とその char 2 特異補題、AG(2,3)/AG(2,7)/PG(2,7) の
最小サイズの SAT による有限決定 (AG(2,7) は区間 {19,20}・PG(2,7) は [15,21] に
厳密化、一部 open)、AG(2,4)/AG(2,5) の最小 2 重ブロッキング全体 (168 + 49,500 個)
の AGL 軌道完全分類。

## 現在の根拠と限界

一般構成の |C|=3q-2 (char 2) / 3q-1 (奇素域) は全 q で定義検証済みの明示構成で
上界としては厳密 (構成の正しさは有限検査で完結)。min が 3q-2/3q-1 に等しい
という全称主張はしない (有限盤では AG(2,3)=8, AG(2,4)=10, AG(2,5)=14 のみ確定)。
AG(2,7) k=19 case A5-A8、PG(2,7) k≤20 は open (CNF 出版済み・長期レーンへ)。
2-ovoid (全直線ちょうど2) の AG(2,7) 非存在は SAT UNSAT による有限決定。
軌道分類は AGL(2,q) 全変換による有限全数計算。PG(2,3)/(2,4) 出版リストの
PGL(3,q) 分類、AG(2,8)/(2,9) の min 決定、q 平面での Baer 対による 3q 未満
候補探索は未解決 (完了 log のリジューム節参照)。
