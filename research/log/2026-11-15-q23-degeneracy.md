# 2026-11-15 q∈{2,3} 完全退化（高速レーン）

## 動機

M_{w,q} 横断表（K0795・results/fixed-width/mwq_stabilization.csv）は
q ≥ 4 から始まっている。優先課題の一般化・基礎整理として
q < 4 を閉形式で決定することを試みた。

## 既存性確認

- `M_{w,3}` / `M_{w,2}` / 「任意の3点は共線または共円」の
  repo 検索 → M_{w,q} 表・K 項目に記述なし。
- K0832（t=2 fiber Grundy q=3）は多項式超曲面ファイバーゲームで
  別設定。K0825〜K0852 は全て q ≥ 4。
- mwq_stabilization.csv の最小 q_min は 4。

## 発見（→証明）

「任意の3点は一直線上または同一円上」により q=3 は完全退化:

- safe ⟺ |S| ≤ 2・極大 ⟺ |S| = 2。
- w ≥ 2: 2石配置は必ずどこかの行が ≤ 1 = q−2 石 → 全幅で
  欠損 witness → witness 帯 [1,∞) → M_{w,3} = ∞。
- w = 1: 極大 = 2石 = 行容量 → M_{1,3} = 2 = q−1。
- g(S) = (2−|S|) mod 2。q=2 も同型（M_{w,2}=∞ / M_{1,2}=1）。
- q ≥ 4 が最初の非退化 q（反例 (0,0),(1,0),(0,1),(2,2)）。

証明は2行の幾何的事実の定義展開で、有限実験に依らない。

## 機械監査

`research/experiments/q23-degeneracy-20261115/scripts/q23_degeneracy_check.py`
（全曲線 census・円は周心構成の独立 Fraction 実装）で5検査:

A census 退化（符号化健全性）・B 全部分列挙 safe/極大分類・
C 全空点 blocked・D 欠損構造・E Grundy 完全逆算。

7盤面 × q∈{2,3} = 14構成すべて PASS。
代表: 3×4・q=3 で 4096 部分集合・極大 66 = C(12,2)・
witness 66（全極大が witness）・79 安全局面 Grundy 全一致。

## 統合

- K0855 新設（status proved・全称）。
- mwq_stabilization.csv に4行追加:
  `parametric,w>=2,2,2,INF` / `parametric,w>=2,3,3,INF` /
  `exact-threshold,1,2,2,1` / `exact-threshold,1,3,3,2`。
- solver 接続: q=3 def-mode は全幅で 2石 SAT → 符号化の
  正の制御族。K0853 自由列追加の自明極限（R(S)=∞）として
  理論の整合確認にも使える。

## 意義・次へ

- 欠損 witness 探索レードの全てが q ∈ {2,3} で閉形式解決。
  非自明領域はちょうど q ≥ 4 から始まることが確定した。
- 「実験→予想→全称証明→独立検証→knowledge 昇格」の全段階を
  1セッションで完結した軽量ケース。
