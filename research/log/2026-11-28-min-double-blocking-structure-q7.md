# 2026-11-28 最小2重ブロッキング: 一般構成 + AG(2,7) 下界 + 軌道分類 完了 log

宣言: research/log/2026-11-28-min-double-blocking-structure-q7-declaration.md
(commit 33dbc5ea6e6efcc3adb12c5dfded742c188a3f1c, 宣言時 HEAD
261432360e30462e9ed67977229fd421bb7af20e)。publish-then-execute。
実験: research/experiments/min-double-blocking-structure-q7-20261128/。
K 項目: K1371 (仮番号・要再採番)。

## 結果

1. **一般構成 (K1371)**: AG(2,q) の 2 重ブロッキング集合で
   char 2 なら |C| = 3q−2、奇素域なら |C| = 3q−1 を与える明示構成
   (三角形 + 反並行線の共有点/対)。q = 3,4,5,7,8,9 で全直線 ≥2 を機械検証。
   既知最小値 (q=3: 8, q=4: 10, q=5: 14) と一致、
   新規上界 AG(2,7) ≤ 20, AG(2,8) ≤ 22, AG(2,9) ≤ 26。
   補題: 反並行線3本の共有点存在 ⟺ char 2 (正準座標計算 + 三角形の
   AGL 共役性 (安定化群 6) で全三角形に波及、q=3,4,5,7 全三角形走査で確認)。
2. **AG(2,7) t=2**: min ∈ {19, 20} (3q−1 = 20 が本命)。自明下界 14 から
   場合分解 SAT で 19 まで厳密化:
   - 全直線ちょうど 2 (2-ovoid) は**存在しない** (k=14 case C UNSAT)。
   - k = 15..18: case A (最大直線 ≥4)・case B (最大 =3) 全 UNSAT。
   - k = 19: case B・case A4 UNSAT。case A5–A8 は 50/135/280s cap で INDET
     (open、CNF 出版済み: out/open_cnf/ag7_k19_A{5,6,7,8}.cnf)。
   - 上界 20: 局所探索 witness (20点, 定義検証済み) + 一般構成 20。
3. **AG(2,3) t=2**: min = 8 (= 3q−1)。k ≤ 7 全 UNSAT・k = 8 SAT。
4. **PG(2,7) t=2**: min ∈ [15, 21]。k=21 SAT (三角形型 witness)。
   k ≤ 20 は 280–290s cap で全て INDET (CNF 出版: out/open_cnf/pg7_k20_{A,B}.cnf)。
   min = 3q = 21 予想は主張しない。
5. **軌道分類 (有限・全数)**:
   - AG(2,4): 最小 t=2 ブロッキング 168 個 (10:48, 12:120) は
     **size-10 が単一 AGL(2,4) 軌道 (48)、size-12 も単一軌道 (120)**。
     size-10 正準形 = **5 本の dual arc の対交点集合** (union = 対交点集合 = C、機械検証)。
   - AG(2,5): 全 49,500 個 (14:9000, 15:28000, 16:12500) は
     **9 軌道のみ** (14: 6000+3000, 15: 12000+12000+4000, 16: 6000+3000+2000+1500)。
     size-14 の 3000 軌道は dual arc 型 (full line 4 本)、6000 軌道は
     三角形 + 2 点型 (full line 3 本)。profile 類別 7 類。
   - 補集合 (極大安全集合) との双方向全件一致を再確認。

## 検証の系統
(a) 全 mask の blocking/minimality 定義直接再検証 (49,500 + 168 全件)。
(b) SAT encoder 較正: PG(2,3) 8/9, PG(2,4) 11/12, PG(2,5) 14/15,
AG(2,4) 9/10, AG(2,5) 13/14 (K1370 出版値と境界完全一致)。
素朴版・fix 付き・場合分解版の 3 符号化すべて。
(c) GF(q) 盤の独立構成 + design 検査 + 出版盤 file との行集合完全一致 (AG(2,4)/AG(2,5))。
(d) SAT witness は抽出後に定義で再検証 (各 line ≥2, size ≤ k)。
(e) 局所探索 witness も定義検証済み。

## 開示・教訓
- 実行中に 1 回 Koyeb artifact 保存失敗で実行環境リセット・作業 tree 消滅
  (既知の file-loss モード)。宣言の方法記述から scripts を再実装し、
  較正値・witness (seed 決定性)・軌道 census がすべてリセット前観測と一致
  (byte 級でなく値一致・局所探索は seed で同一 witness を再取得)。
- sat2 の l0 固定に使う 3 点は PG の点ラベル (index = x·q + y) を
  誤ると初回の非共線 assert が即捕捉した (fail-closed 動作)。
- GF(9) の neg を恒等写像にする初版バグを q=9 構成の失敗で検出・修正
  (GF(4)/(8) の char 2 では恒等で正しい)。修正後 全 q の design 検査・
  出版盤一致を再実行して出版。

## non-claims
- 全称命題 (min = 3q 等) は予想としてのみ。有限決定結果は
  AG(2,3) = 8 のみ (他は区間または上界)。
- AG(2,7) k=19 case A5–A8、PG(2,7) k ≤ 20 は open。CNF pin:
  ag7_k19_A5 0616d483 / A6 f5949a89 / A7 e5d479fa / A8 75c9929b /
  pg7_k20_A 19abb8ba / pg7_k20_B d901367d (sha256 先頭 8 桁、全 file 同梱)。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。

## リジューム (次回の着手候補・着手前に最新 main 再取得)
- AG(2,7) k=19 case A5–A8 の重い cap (長期レーン向き) → 決着で min = 19 or 20 確定。
- PG(2,7) k=20 (A/B) 重い cap → min = 21 = 3q の検証。
- PG(2,3)/PG(2,4) 出版リストの PGL(3,q) 軌道分類 (出版盤ラベル対応付けが必要。
  PG(2,5) リストは未出版・MANIFEST sha pin のみ)。
- AG(2,8)/AG(2,9) の t=2 min 決定 (22/26 の構成値に対する SAT 境界)。
- q=9 平面での Baer 部分平面対による 3q 未満 2 重ブロッキングの探索
  (PG(2,9) 27 に対し 26 以下が可能か、理論と実験の両面)。
