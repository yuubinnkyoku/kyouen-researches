# min-double-blocking-structure-q7-20261128 — 最小2重ブロッキングの構造分類と一般構成

宣言: research/log/2026-11-28-min-double-blocking-structure-q7-declaration.md
(commit 33dbc5ea, 宣言時 HEAD 261432360e)。K1370
(t2-blocking-duality-20261128) の計数結果を入力とする後処理中心の高速レーン作業。

## 結果（すべて有限盤、検証は定義直接 or 較正済み SAT）

### 1. 一般構成（新規・全 q で機械検証、一般証明スケッチつき）
三角形 (l1: y=0, l2: x=0, l3: x+y=1) と3つの反並行線
D1: y=1, D2: x=1, D3: x+y=0 を使う:
- **char 2**: D1∩D2∩D3 = (1,1) が一致 → C = 三角形 ∪ {R}, **|C| = 3q−2**
- **奇素域**: R12 = (1,1) ∈ D1∩D2 と R3 = (1,−1) ∈ D3 → C = 三角形 ∪ {R12, R3},
  **|C| = 3q−1**
q = 3,4,5,7,8,9 の全部で「全直線 ≥2」を定義直接検証
(out/canonical_construction.json)。既知の最小値 q=3: 8 = 3q−1, q=4: 10 = 3q−2,
q=5: 14 = 3q−1 と完全一致。新規上界: **AG(2,7) ≤ 20, AG(2,8) ≤ 22, AG(2,9) ≤ 26**。
補題（正準座標で証明可能、機械確認 q=3..7）: 三角形の反並行線3本が共有点を
持つ ⟺ char 2（全三角形は AGL(2,q) 共役・安定化群位数 6、
D1∩D2=(1,1) が D3: x+y=0 上 ⟺ 2=0）。char 偶の全三角形走査で
q=4 は 480/480 が共有点・検証済み、q=3,5,7 は 0/失敗 0（scripts/triangle_construction.py）。

### 2. AG(2,q) の t=2 最小サイズ（SAT による決定・k=19 の一部は open）
- **AG(2,3): min = 8**（k≤7 全 UNSAT, k=8 SAT。3q−1 = 構成値と一致）。
- **AG(2,7): 19 ≤ min ≤ 20**。決定的に減らした区間（自明下界は 14）:
  - k=14 case C (全直線ちょうど2) UNSAT = **AG(2,7) に 2-ovoid は存在しない**
    （全直線とちょうど2点で交わる集合の非存在。新規の否定的結果）。
  - k=15,16,17,18: case A (最大直線 ≥4), case B (最大 =3) とも UNSAT。
  - k=19: case B UNSAT, case A4 (最大 =4) UNSAT。**case A5–A8 は未決着**
    (50s/135s/280s cap で INDET、CNF は out/open_cnf/ に出版)。
  - 上界: 局所探索 seed 12 で 20 点 witness 発見（定義検証済み）。
  - 構成 (3q−1 = 20) と下界 19 の整合から **min ∈ {19, 20} で 3q−1 が本命**。
- AG(2,4): min 10, AG(2,5): min 14 は較正として完全再現。

### 3. PG(2,7): 15 ≤ min ≤ 21、3q = 21 が本命
- k=21 SAT (witness 21点・三角形型, 0.08s)。k=15..20 は素朴符号化・fix 付き・
  場合分解 A/B すべて 280–290s cap で INDET（正直言明）。
  CNF (k=20 A/B) は out/open_cnf/ に出版。
- 局所探索: k=20 best_cost 1（200k ステップ × 複数 seed）、k=19 best_cost 2。
  min = 3q = 21 を予想に留める（Baer 部分平面の対による q が平方のときの
  3q 未満候補は本実験では q≤9 で未発見）。

### 4. 構造分類（AG(2,4) 168 個、AG(2,5) 49,500 個・全数）
出版 mask リストを全件 定義再検証（blocking + minimality）の上、
line-profile で類別し AGL(2,q) 軌道展開で完全分割:
- **AG(2,4): size-10 の 48 個は単一 AGL(2,4) 軌道、size-12 の 120 個も単一軌道
  （計 2 軌道）**。size-10 の正準形は **5 本の dual arc（2本並行なし・3本共点なし）の
  10 個の対交点集合と一致**（union of full lines = C = pairwise intersections、機械検証）。
- **AG(2,5): 全 49,500 個はわずか 9 軌道**: size-14 は 2 軌道 (6000+3000)、
  size-15 は 3 軌道 (12000+12000+4000)、size-16 は 4 軌道 (6000+3000+2000+1500)。
  size-14 の 3000 軌道は 4 本 full line を含み 4q − C(4,2) = 14 = dual arc 型、
  6000 軌道は 3 本 full line（三角形 + 2 点型）。
- 補集合側との整合: minimal ↔ maximal 双方向で補集合が全件一致（K1365 の再確認）。

### 5. 较正
同一 encoder + kissat 4.0.4 (sha256 21da5d98... repo pin と同一) で
PG(2,3) 8 UNSAT / 9 SAT, PG(2,4) 11/12, PG(2,5) 14/15,
AG(2,4) 9/10, AG(2,5) 13/14 を全て再現（K1370 出版値と一致）。
場合分解符号も同値群を再現。GF(q) 盤は独立構成・2-(v,k,1) 検査済みで
出版盤 file (AG(2,4)/AG(2,5)) と行集合が完全一致。

## 方法・検証
- scripts/boards.py — GF(q) 独立構成 (q=3,4,5,7,8,9)・design 検査・出版盤照合
- scripts/sat_min.py — 素朴 SAT (at-least-2/line + sequential at-most-k + 対称性 fix)
- scripts/sat2.py — 場合分解 SAT (A/A4..A7/A8/B/C)。場合分解の妥当性は module docstring
- scripts/classify.py — 定義再検証 + AGL 軌道完全分割 (pure python)
- scripts/localsearch.py — witness 発見ヒューリスティック (seed 決定性)
- scripts/triangle_construction.py — 三角形全走査 (char 2 共有点補題の機械確認)
- scripts/canonical_construction.py — 一般構成 (char 2 / 奇素域) の全 q 検証
- out/ — 全出力 (boards.json, calibration, ag7 系列, classify JSON, canonical_construction.json,
  open_cnf/)
- 実行ログ: out/*.txt がそのまま一次記録。

## non-claims
- min = 3q (PG) / min = 3q−1 (AG, 奇素域) などの**全称主張はしない**。
  「AG(2,q) は 3q−2 (char 2) / 3q−1 (奇素域) 以下」という上界と
  「AG(2,7) ≥ 19」のような SAT による有限下界、有限盤の完全な軌道分類が本成果。
- PG(2,7) k≤20 の UNSAT は未取得。AG(2,7) k=19 case A5–A8 は未決着。
  CNF を出版して長期レーンに委ねる。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
- 途中で 1 回の実行環境リセットが発生し作業 tree が消滅した。
  宣言の方法記述から scripts 全体を再実装し、較正・全数値が
  リセット前の対話記録観測値と完全一致したことを以て出版した
  （較正値・witness・軌道 census の一致を out/*.txt で確認可能）。
