# 2026-11-13 高速レーン: w=66 キャンペーン開始（K0798 P(65)=32 の直接続編）

K0798 完走直後に着手。K0797 会計は w ≤ 84 で有効なので P(66) 決定に必要な
前提は level 17 全滅掃引のみ（下界は 2210 円 32 点・v-span 94 ≤ 130）。

## 実行記録

1. **機械**: w=65 完走で確立した REST6 2フェーズ機を最初から使用
   （survivors(REST6) ⊇ survivors(REST16)・phase2 は生残が出た mask のみ）。
   窓マスクは66ビット・ワード数 ceil(w/32) で自動化。
2. **窓マスク**: unique = maximal = **3,300**（w=65 の 3,296 から +4）。
3. **chunks 1-2（本セッション）**: mask 0..487 完了
   （chunk1: 0→223〔~10.8k/mask〕・chunk2: 223→488〔~9.1k/mask〕・
   計 4.8M nodes・leaves=0・生残0・フェーズ2必要 mask 0件）。軽い帯から開始
   （w=65 と同様に heavy band は後半に局在する見込み）。
   resume from=489（残り 2,812 mask）。

## 意味論（P(66) は OPEN）

- 完走時（leaves=0・生残0）で **P(66) = 32 が等号付き・全称で確定**する。
  それまでは P(66) ∈ [32, 128] open。
- ノード見込み: w=65 実績 42.6M × 成長則 ~1.35 → ~55M 前後
  （heavy band の局在性次第で大きく変わる・w=65 では外挿の1/3だった）。

## レジューム（次回の実行）

1. **w=66 キャンペーン継続**: output/width66_progress.json の chunks に追記
   （CFG.from=489・REST6 2フェーズ・cap 2.4M/chunk・1実行1..2チャンクが安定）。
2. 完走時は K0799（P(66)=32）に昇格・results/fixed-width/ 追従
   （pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0799**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。

## 第2セッション（chunks 3-8・gap mask 修正）

1. **off-by-one 発見・修正**: 機械の lastDone = (完了した最大 mask index)+1 なので
   resume_from は lastDone をそのまま使うのが正しい。第1-2セッションの
   resume_from=489 は lastDone=488 に +1 しており **mask 488 を飛ばしていた**。
   classifyOne（単一 mask 完走機）で mask 488 を個別完走（leaves=0・20,582 nodes）。
   制御: mask 200 再実行で chunk1 と整合（16,661 nodes・leaves=0）。
2. **chunks 3-8**: mask 489..888 を 6 チャンク（各 2.4M nodes cap）で完了。
   chunk3: 489→773（軽い帯 ~8.5k/mask・heavy band は ~772 から開始・w=65 とほぼ同位置）、
   chunk4: 774→794（~114k/mask）・chunk5: 795→820（~92k）・chunk6: 821→847（~89k）・
   chunk7: 847→874（~86k）・chunk8: 874→889（~150k）。
   **累計 19.6M nodes・leaves=0・生残0・フェーズ2必要 mask 0件。**
3. **chunk 境界の未走査 mask（773/794/820）も classifyOne で個別証明**
   （217,690 / 168,089 / 12,955 nodes・全て leaves=0）。
   → **mask 0..888 は隣接漏れなしに完全走査済み**（889/3,300 = 26.9%）。
4. **heavy band 開始位置は w=65（~772）とほぼ同じ**。1実行1チャンクが安定
   （2チャンクは sandbox の process safety deadline 超過・軽い帯の chunk3 は除く）。
5. 反映: progress JSON（resumeConvention・gapCertifications 追加）・script CFG.from=889
   （c2062833・3f5fd797・読み戻し検証済み・並走なし〔反映前に HEAD a50f183 を再取得〕）。

### 第2セッション続き（chunks 9-14）

- chunks 9-14 を実行し **mask 0..1233 完了（隣接漏れなし・1,234/3,300 = 37.4%）**。
  chunk9: 889→914（~92k/mask）・chunk10: 914→940（~89k）・chunk11: 940→964（~96k）・
  chunk12: 964→1000（~65k・減衰）・chunk13: 1000→1214（**~1000 で沈み込み ~11k/mask・
  214 mask/chunk**）・chunk14: 1214→1234（**~1190 から第二 heavy band 再出現 ~114k/mask**）。
- **heavy band は w=65 と同じ非単調構造**: 第一帯 ~772..999 → ~1000 の dip →
  第二帯 ~1190..。累計 34.0M nodes・leaves=0・生残0・phase2 必要 mask 0件。
- 反映: progress JSON（97d7de19・resume_from=1234）・script CFG.from=1234（b864e33f）。
  読み戻し検証済み。

## レジューム（次回の実行）

1. **w=66 キャンペーン継続**: CFG.from=1234 から（resume_from=lastDone を厳守）。
   heavy band 継続中・1実行1チャンク（2.4M cap）。
2. 完走時は K0799（P(66)=32）に昇格・results/fixed-width/ 追従。
3. 次の空き K 番号: **K0799**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
