successfully downloaded text file (SHA: d7fd72bd088d280cd04bd62838c479b21ff1b25a)successfully downloaded text file (SHA: aa6ff6d4e8172aebf8fd023db1930ecbb70edef7)# 2026-11-13 高速レーン: w=65 level 17 キャンペーン開始（進行中・resume from=1302・REST6 2フェーズ採用）+ K0797 会計拡張の続き

K0797（g0 会計 w≤84 延長）の直後にレジューム(1)「w=65 標準形 DFS」に着手。

## 実行記録

0. **第2セッション追記**: chunks 9-12 実行（841→893・2.4M/36mask=67k..150k/mask・heavy band 中核で単調増加）。resume from=893。
0b. **第3セッション追記**: chunks 13-18 実行（893→975・6チャンク×1.2M=7.2M/82mask）。
    全て leaves=0・生残0。mask 893..975 の heavy band は 71k..100k nodes/mask で
    ほぼ平坦（chunk あたり 12..17 mask）。resume from=975。
0c. **第3セッション追記その2（枝刈り監査・別実験に詳細）**:
    [width65-pruning-audit](../../experiments/width65-pruning-audit-20261113/) で
    ①素数冪 121 追加は nodes -10.7% だが word-ops +96.8% で**不採用**（K0789 の
    候補掃引とは逆の結論・コストモデル依存）、②法検査順はほぼ最適（-2.6%）、
    ③heavy band の殺しは6法（19,23,7,29,43,47）に集中し他10法は一度も殺さない、
    ④**REST6 2フェーズ方式**: REST6 は survivors(REST6) ⊇ survivors(REST16) なので
    REST6 生残0の mask は REST16 でも生残0が確定（実現可能集合は全法を通過する
    ため誤殺なし・w26 L12 制御で S* がちょうど1生残で確認）。heavy −45.4% ops・
    light −40.1% ops で**実行コスト約2倍高速**。フェーズ2必要 mask は現時点 0 件。
1. **機械**: K0793/K0794 機を w=65 用に3ワード化（窓マスクが65ビットになるため
   bits を [lo,mid,hi] に拡張・それ以外は同一構造・classify 内蔵 1.2M チャンク・
   lastDone 冪等再開）。
2. **制御**: w=26 L=12 → S* ちょうど1生残（[0,1,3,4,7,10,15,18,21,22,24,25]・
   K0782..K0794 と完全一致・REST6 でも同一）。w=65 の窓マスク: unique 3,296・maximal 3,296。
3. **進捗（3セッション計18チャンク）**: mask 0..974 完了・ノード計 21.6M・
   leaves=0・生残0。重い帯は mask ~772 から開始し 58k..150k nodes/mask
   （chunk5: 772→782 の10 mask で 1.2M）。
4. **コスト観察**: K0793 の「heavy band 下端が w とともに沈む」観測と非整合 —
   w=65 の重い帯は w64 より重く始まっている。さらに第3セッションで
   heavy band が mask 975 まで沈まず 71k..100k/mask を維持することが判明した。
   残り 2,321 mask が同密度なら総ノード ~200..250M（当初 80..160M 推定を上方修正）。
   REST6 2フェーズで word-ops 観点は約半減。
0d. **第3セッション追記その3（REST6 でのキャンペーン前進）**: chunks 19-22 を
    REST6=[19,23,7,29,43,47]・cap 2.4M nodes/chunk で実行し **masks 975..1301 を完了**
    （計 9.6M nodes・leaves=0・生残0・フェーズ2必要 mask 0件・cumulative 31.2M nodes）。
    heavy band は非単調であることが判明: ~1000 で一旦沈み
    （chunk19: 215 mask/2.4M = ~11k/mask）・~1190 で再出現（chunks 20-22: ~57k..73k/mask）。
    resume from=1302・残り 1,994 mask。

## 意味論（P(65) はまだ OPEN）

- 完走時（leaves=0・生残0）+ K0797 会計（w=65: g2=8(33)・g3=12(22)・g4=5(17)・
  全形 classMax < 17）+ 2210 円下界（32点・v-span 94 ≤ 128）で
  **P(65) = 32 が等号付き・全称で確定**する。それまでは P(65) ∈ [32, 126] open。
- REST6 2フェーズの健全性: survivors(REST6) ⊇ survivors(REST16)（実現可能標準形は
  全合同証明書を通過）。REST6 フェーズ1で生残0の mask はそのまま確定。
  生残が出た mask のみ REST16 フェーズ2で再走査。

## レジューム（次回の実行）

1. **w=65 キャンペーン再開（REST6 2フェーズ機で）**: masks 1302..3295 を
   REST6=[19,23,7,29,43,47] で走査（同じ bit-set DFS・rowMask は6法分のみ・
   cap は word-ops 観点で 1.2M チャンクより実質2倍速い・lastDone 冪等再開は
   そのまま）。生残0以外の mask を見つけたら REST16 で再走査してから集計。
   output/width65_progress.json に chunk を追記（machine フィールドに
   REST6 2フェーズと明記）。
2. 完走時に K0798（P(65)=32・32プラトー w=49..65）として昇格・
   results/fixed-width/（K0795 表）の追従更新。
3. 次の空き K 番号: **K0798**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
