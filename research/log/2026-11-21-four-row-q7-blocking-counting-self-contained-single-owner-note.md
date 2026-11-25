# four-row q=7 自己完結ブロッキング計数証明 — 単一オーナー宣言ノート（2026-11-21 長期レーン）

## 宣言

K1182（4×m・q=7 の真の満容量安定化長 M_{4,7}=13・status proved）の
解釈規約に明示された自由課題「K0318 に依存しない自己完結的なブロッキング
計数証明（M の値を変えないが証明の独立性を高める）」を、本レーンが
単一オーナーとして着手する。宣言時 main HEAD: `497f4e176e82d979e65084900acc4ee7d3c72c0e`（2026-11-21T07:35:55Z）。

## 対象と方針

- 主定理（数学的証明）: w=4・q=7 の 4×m 盤（一般に 4 本の水平線上の点配置）
  において、行欠損を伴う極大安全配置が存在するなら m ≤ 86。
  証明骨子: 欠損行 R（石数 r ≤ q−2 = 5）の空点 m−r 個は、
  非水平直線が ≤4 格子点・水平線は 6 石不足で block できないため、
  すべて円で block される。円と水平行の交点は ≤2 なので、割当円 C_i の
  R 内割当空点数 e_i ∈ {1,2}・R 内石数 u_i は e_i + u_i ≤ 2 を満たし、
  円上石数 ≥ q−1 = 6 より R 外石数 t_i ≥ 4 + e_i。
  R 外石は 3 行 × (q−1) = 18 個以下で、同一円上の非共線 3 つ組は円を
  一意に決めるため相異なる割当円間で 3 つ組集合が非交差することから
  Σ_i C(t_i, 3) ≤ C(18, 3) = 816。一方 C(t_i,3) ≥ C(4+e_i,3) ≥ 10 e_i なので
  10 (m−r) ≤ 816、すなわち m ≤ r + 81 ≤ 86。
- 系（代替 certificate）: 機械掃引 [13,86]（K1177 原掃引 13..85 は sat2.js、
  m=86 は K1182 の genfast3 記録・2 回実行 bit-exact）と本定理の [87,∞) の
  併合により、M_{4,7} = 13 が K0318 の一般上界 U_{4,7}=81 を用いずに閉じる
  （下界 m=12 witness と capacity 存在 (m≥13) は K1177/K1182 従来どおり
  K0318 非依存）。誠実な注記として、計数上界の閾値（m ≥ 87 で def 不可能）
  は K0318 の解析上界（m ≥ 81）より 6 幅弱いが、既刊掃引 86（と支持 87, 88）
  が既に埋めているため certificate としては十分。
- 機械検証（実験 `= self-contained`）: 標準ライブラリのみの決定的・
  fail-closed 検証機を同梱し、(a) 幾何補題（円×水平行 ≤2 点・相異なる
  2 円の格子共有点 ≤2・非水平直線 ≤4 格子点）の格子全域整数演算テスト、
  (b) 計数不等式の全数値列挙（max a+2b = 81 etc.）、(c) 掃引 certificate の
  pin 照合（q7 records の射影 sha256・append 不変）、(d) m=12 不足極大
  witness 23 石の前提監査（安全性・極大性・欠損行 7 空点の割当円 e/u/t 分類
  と 10(m−r) ≤ Σ C(t,3) ≤ 816 の実データ上の成立）、(e) m=13 capacity
  witness 24 石の照合、を行う。battery 3 実行で audit byte 一致を確認する。

## 出版物（すべて本レーン所有）

1. 実験 dir `research/experiments/four-row-q7-blocking-counting-self-contained-20261121/`
   （README・scripts・output/audit.json・output/reproduction.log）
2. K 項目（番号は push 直前に 3 点確認で取得）+ 研究log
3. K1182 への relation 1 行追記（status・既存主張の変更なし・最新 main 再取得後）
4. knowledge README bullet 追記（append only・並走 bullet 温存）

## 受入条件

1. 検証機の全 gate が PASS（fail-closed: 監査は全 gate 通過時のみ書込）。
2. battery 3 実行（同一 cwd 2 回 + 隔離 cwd/HOME/TMPDIR + PYTHONHASHSEED=random
   1 回）で audit.json が byte-identical。
3. 入力 pin: frontier records.jsonl の q7 射影 sha256 および witness 2 点の
   sha256 が本文記載値と一致（不一致は fail-closed）。
4. 主定理の証明が K1182・K1177 の既存主張を変更しない（値 M_{4,7}=13 不変・
   status は新項目側で "proved (second, self-contained certificate)" 相当を記載）。
5. 知見の誠実な記載: 計数上界閾値 87 vs K0318 の 81 という相対位置、
   K0318 依存の除去が certificate 独立性向上のみを目的とすること。

## 非目標

- 既存 verdict・records・witness の変更は一切しない。
- 新たな掃引・探索は行わない（既刊掃引の再計算をしない）。
- 行は 1 行も閉じない。nodes 数・solved 数を勝敗として読まない。
  REFUTED-D10 は LOSS 証明ではない。本課題は固定幅レーンであり n11 に影響しない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**
