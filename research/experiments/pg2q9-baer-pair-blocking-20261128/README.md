# pg2q9-baer-pair-blocking-20261128 — Baer部分平面対によるPG(2,q²)の2重ブロッキング

宣言: research/log/2026-11-28-pg2q9-baer-pair-blocking-declaration.md
(commit `e30035a2`, 宣言時 HEAD pin `2cad2042`・publish-then-execute・単一オーナー)。
K1371 レジューム (d)「q=9平面のBaer部分平面対による3q未満2重ブロッキング探索」
の厳密な決定。K1371 の「Baer対による3q未満候補は q≤9 で未発見」記録を
**修正する結果**を含む。

## 主結果

### PG(2,9): t=2 最小2重ブロッキング ≤ 26 < 27 = 3q（新規・全数census）
- Baer 部分平面 PG(2,3) の PGL(3,9) 軌道: **7,560 個**
  （|PGL(3,9)| = 42,456,960・安定化群 5,616 = PGL(3,3)・軌道-安定化群整合 ✓）。
- 全対 C(7,560,2) = 28,559,820 の交差census:
  {0: 3,265,920 / 1: 7,665,840 / 2: 10,614,240 / 3: 5,307,120 / 4: 393,120 / 5: 1,326,780}。
- 2重ブロッキング判定: **交差≥1 の対は全て失敗 (0/25,293,900)、
  disjoint 対は全て成功 (3,265,920/3,265,920)**。
- **最小 union = 26** (disjoint 対)。witness 26点 (out/baer_pairs.json・
  プロファイル {2:65, 5:26}・定義直接検証済み)。
- **PG(2,9) t=2 min ∈ [19, 26]** (下界19はcounting bound: 10k ≥ 2·91)。
  27 = 3q を下回る初の構成で、「min = 3n」パターンが平方位数 n=9 で
  成立しないことを示す。

### PG(2,4): Baer (Fano) 対の全census（較正・整合確認）
- 軌道 360（安定化群 168 = PSL(3,2)）。交差census
  {0: 2,880 / 1: 7,560 / 2: 30,240 / 3: 13,860 / 4: 10,080}。
  **disjoint Fano 対が 2,880 個存在**（union 14 は2重ブロッキング）。
- Baer対としての2重ブロッキング最小 union = **13** (∩=1 の 7,560 対すべて成功、
  ∩≥2 は全て失敗)。既知の PG(2,4) min = 12 < 13 と無矛盾:
  12 点の minimal DB は Baer 対の union ではない。

### PG(2,16): ≤ 42 < 48 = 3q（サンプリング・開示どおり）
- Baer 基底 PG(2,4) 検査 ✓ (プロファイル {1:252, 5:21}・2-(21,5,1))。
- seed 固定ランダムウォーク 3,000 歩: disjoint 510 個。
  **disjoint union 42 witness**（定義直接検証済み・min ∈ [33, 42]）。

### AG(2,9) 制限（負のサンプル・正直な負）
- disjoint Baer 対 3,000 個 × ℓ∞ 91 選択で AG 2重ブロッキング feasible なし。
  AG(2,9) の上界は従来どおり 26 (3q−1)。

### 一般補題（条件付き・証明つき）
Baer 部分平面 A, B ⊆ PG(2,q²) が disjoint なら A∪B は size 2(q²+q+1) の
2重ブロッキング（各直線は A・B に各≥1点を持つ・Baer 性より）。
2(q²+q+1) < 3q² ⟺ q ≥ 3。よって disjoint Baer 対の存在下では
「PG(2,n) の t=2 min = 3n」は n = q² ≥ 9 で不成立。
q=2 (n=4) では 2(7)=14 > 12 = 3n で改善なし（実際 min 12・Baer対最小 13）。

## 手法・検証（fail-closed）
- scripts/boards9.py — GF(4)/GF(9)/GF(16) 多項式環による独立構成 +
  design 検査。Baer 基底 = 部分体 GF(q) 有理点。
- scripts/baer.py — Baer 性検査 (全直線交差 ∈ {1, q+1}・内部 design)、
  PGL(3,q²) 生成元 BFS (transvection/対角/座標交換)、軌道-安定化群整合、
  全対交差census、2重ブロッキング直接判定
  (solo-line 補題: |A∩L|≥2 ∧ |B∩L|≥2 ⇒ |(A∪B)∩L| ≥ max ≥ 2)、
  witness 全直線再検査。
- scripts/ag_scan.py — AG 制限スキャン (サンプリング)。
- scripts/verify_baer.py — 盤再構成による再検証 (witness 定義直接・
  軌道再計算 (生成元順序変更)・counting lower bound)。ALL_OK。
- 再現性: 宣言後のクリーン再実行で out/ 3file とも byte-identical
  (seed 固定)。宣言前スクラッチ実行とも一致。

## Non-claims
- 「全ての q≥3 で disjoint Baer 対が存在」は一般証明しない
  (q=2,3 は全数census・q=4 はサンプリングでの機械検証のみ)。
- PG(2,9) min の SAT 下界の押し上げは実施しない (重い・長期レーン向け)。
- 26 witness の「全2重ブロッキング集合としての最小性」は主張しない
  (Baer対に限定した最小性)。
- verdict 不消費: 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・
  第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。
