K0801 完走直後に着手。K0797 会計は w ≤ 84 で有効なので P(68) 決定に必要な
前提は level 17 全滅掃引のみ（下界は 2210 円 32 点・v-span 94 ≤ 134）。

## 実行記録

1. **機械**: w=67 完走機（width67_level_classify.ts・K0801 verifier）の
   verbatim 移植（REST6 2フェーズ・窓マスク 68 ビット・ワード数 ceil(w/32)
   自動・W=68）。
2. **窓マスク**: unique = maximal = **3,300**（w=66/67 と同数）。
   harness 制御: w=64→3,288・w=65→3,296・w=66→3,300・w=67→3,300 を
   本harnessで完全再現。**maximal mask 数は w≥66 で 3,300 に飽和か**
   （観察・要 w≥69 検証）。
3. **chunks 1-3（第1セッション）**: mask 0..501 完了
   （chunk1: 0→104〔**~23k/mask・w=67 の約2.2倍**〕・chunk2: 104→297
   〔~12.4k〕・chunk3: 297→502〔~11.7k〕・計 7.2M nodes・leaves=0・
   生残0・phase2 必要 mask 0件）。
4. **観察（第1セッション）**: w=68 は前置帯からすでに w=67 の約2倍重い。
   heavy band 入り口（~770 前後・窓位相不变則）の加重はさらに上振れの
   可能性 → 総計 110..170M nodes・複数セッション必須。
5. resume from=502（lastDone 規約・+1 しない）。

## 第2セッション（chunks 4-8: mask 0..821 = 24.9%・heavy band 入口通過）

1. **chunks 4-8**: mask 502..821 完了（chunk4: 502→724〔222 mask・~10.8k〕
   ・chunk5: 724→776〔52 mask・**~46k・heavy band 入り口 ~770 到達**〕・
   chunk6: 776→788〔12 mask・**~200k**〕・chunk7: 789→807〔18 mask・~133k〕
   ・chunk8: 808→822〔14 mask・~171k〕・計 9.6M nodes・leaves=0・生残0・
   phase2 必要 mask 0件）。
2. **境界 off-by-one 2件を個別証明**: chunk6→7（mask 788・314,127 nodes）
   と chunk7→8（mask 807・273,404 nodes）を classifyOne 単一mask完走機で
   証明（両方 leaves=0・生残0）→ **mask 0..821 は隣接漏れなしに完全走査済み**。
   原因: lastDone=(完了max index)+1 規約の chunk 境界で from に誤って +1
   （w=66 第1-2セッションと同一の失敗パターン・再発防止は
   「次 chunk の from は直前 chunk の lastDone を verbatim で使う」のみ）。
3. **第一 heavy band 開始確認**: 入り口 ~770（窓位相不变則どおり・w=65..67
   と同位置）・加重 ~130..200k/mask は w=67 の ~86..150k の約1.3..1.4倍
   （成長則 ~1.35 と整合）。
4. resume from=822。

## 第2セッション続き（chunks 9-11: mask 822..879・境界ギャップなし）

1. **chunks 9-11**: mask 822..879 完了（chunk9: 822→840〔18 mask・~133k〕・
   chunk10: 840→861〔21 mask・~114k〕・chunk11: 861→880〔19 mask・~126k〕・
   計 7.2M nodes・leaves=0・生残0）。今回の chunk 境界は
   「from = 直前 lastDone を verbatim」で通したため gap 証明不要。
2. **進捗**: mask 0..879 = 880/3,300 = 26.7%・累計 24M+0.6M nodes。
   第一 heavy band（~770..）は ~114..200k/mask で w=67 の ~1.3..1.4倍。
3. resume from=880。

## 第3セッション（chunks 12-13: mask 880..889・第一 heavy band 最重要部到達）

1. **chunks 12-13**: mask 880..889 完了（chunk12: 880→885〔5 mask・**~480k/mask**〕・
   chunk13: 885→890〔5 mask・~480k〕・計 4.8M nodes・leaves=0・生残0・
   phase2 必要 mask 0件）。chunk 境界は from=直前 lastDone verbatim で
   gap 証明不要。
2. **観察**: 第一 heavy band の加重は ~130..200k/mask から chunk12-13 で
   **~480k/mask に急上昇**（w=68 固有の最重要部・これまでの最高加重）。
   1 chunk あたり消化 mask 数が 19..21 から 5 に急減 → heavy band 残り
   （~999 まで）の消化は複数セッション必須。窓位相不変則（入り口 ~770）と
   整合する位置で加重のみが増幅。
3. **進捗**: mask 0..889 = 890/3,300 = 27.0%・累計 28.8M+0.6M nodes・
   resume from=890。
4. 反映: progress JSON（chunks 12-13 追記・resume_from=890）・script
   CFG.from=890 + header訂正（stale CFG.from=822 行の除去）・本log。
   全ファイル repo 読み戻し検証済み・並走なし（反映前 HEAD a586d612 再取得）。

## 意味論（P(68) は OPEN）

- 完走時（leaves=0・生残0）で **P(68) = 32 が等号付き・全称で確定**する。
  それまでは P(68) ∈ [32, 130] open。現在は部分進行（890/3,300 = 27.0%）。

## レジューム（次回の実行）

1. **w=68 キャンペーン継続**: output/width68_progress.json の chunks に追記
   （CFG.from=890・**次 chunk の from は直前 lastDone を verbatim で**・
   cap 2.4M/chunk・1実行1〜2チャンク・heavy band は ~999 まで
   （chunk12-13 で ~480k/mask の最重要部に入ったばかり・1チャンク ~5 mask の
   ペースが当面続く見込み）・
   ~1000 での沈み込みと ~1190 での第二帯再出現〔w=65..67 パターン〕を注視）。
2. 完走時は K0802（P(68)=32・**反映前に K 番号の空きを再確認**）に昇格・
   results/fixed-width/ 追従（pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0802**（本log時点・要再確認）。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
