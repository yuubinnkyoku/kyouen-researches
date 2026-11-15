# (5,6) 5x22 bounded-edit witness surgery — IN FLIGHT

2026-11-15 高速レーン。CSV (5,6) 行の前線 5x22（bounds 22..249）。
既存の class-split sweep（five-row-q6-m22-class-split-20261114:
19正準類中8類 INDET 250s・{0}/{1} krow 分割も INDET・SA 非発見・
encoding-symmetry 1500s budget 中断 14.7M conflicts）と探索空間が直交する
「既知 witness からの有界編集距離」を導入する。機械は
w4-w5-q5-surgery-20261115 の surgery.js（(8,9) eight-row-q9-m29-surgery
20261115 で v2 検証済み）をそのまま使用する。

## status: IN FLIGHT（実行中・結果未確定）

## 主張の対象

- 種: K0815 の 5x21 24石 witness（rows [4,5,5,5,5]、seeds_w56_21）。
  5x22 盤に offX=0/1 で埋め込む（両方。H鏡像は seed 自身を変えるため
  offX=1 は別インスタンス）。
- F = seed ∪ P \ Rm（P: seed 空セル、Rm: seed 石）、|P| ≤ 2、|Rm| ≤ 2
  （対称差 ≤ 4）、|F| ≤ 24 = 5(6−1)−1 を完全列挙し、安全（全census曲線
  ≤5石）と極大（F の全空セルがちょうど5石のcensus曲線上）を検証。
  |F| ≤ 24 → 鳩の巣で欠損行（≤4石）が従属し witness となる。
- **SAT** → 5x22 witness → M_{5,6} ≥ 23（CSV lower 境界 23..249 に前進）。
- 局所負 → 不在主張ではない（w4-w5-q5-surgery m=25 の局所負 precedent、
  K0851 対照の「局所 0 ≠ 不在」較正と同じ扱い）。

## センサスの完全性（q = w+1 境界条件）

q=6=w+1 では 6点円が単一の2点行+4つの単点行を持ち得るため、chord-pair
分解（2つの2点行ペアを要求）は一般には不完全（w=8,q=9 のとき
q9-census が必要だったのと同じ境界）。本幾何では:

- 既存較正 C2: genfast.js（chord-pair census）と sat2.js（all-triples
  完全census）が (5,22,6) --deficient で CNF バイト同一 → 5x22 盤の
  census曲線集合が一致 → 1-double-row ≥6点円は 5x22 に存在しない。
- 追加較正 C4（本実験で実施）: 独立 all-triples 列挙（C(110,3) 三点組 →
  円・直線 → ≥6点曲線集合）と surgery.js buildCensus の曲線集合の
  完全一致を機械確認してから本番を実行する。

## 較正・対照（計画）

- CTRL-1: 5x21 盤に seed から1石除去した 23石 seed → (2,2) 手術で
  元の 24石 witness を再発見できること（end-to-end 陽性対照。
  8x29 surgery の CTRL-A と同型）。
- C4: 上記 census 完全性検証。

## 計画

1. C4 census 完全性検証（chord-pair vs all-triples @ (5,6,22)）。
2. CTRL-1（5x21、seed−1石）。
3. 本番: 5x22、offX=0/1 × (|P|,|Rm|) = (2,2)、次いで (3,3) を予算内で。
4. 発見時: verify_witness.py（exact Fraction）+ verify_witness_int.py
   （純整数・第3系統）で独立検証し、witness JSON を保存。
5. 結果は records + 本README 更新 + CSV (5,6) 行 + fixed-width README に統合。
