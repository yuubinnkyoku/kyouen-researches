successfully downloaded text file (SHA: 33e7c176f6ca46bfc37d728c9d472ae17300d8af)successfully downloaded text file (SHA: fecb68844b9760fbf369d5b96e8c4ca86b1649f5)# 2026-11-13 高速レーン: w=67 キャンペーン開始（K0799 P(66)=32 の直接続編）

K0799 完走直後に着手。K0797 会計は w ≤ 84 で有効なので P(67) 決定に必要な
前提は level 17 全滅掃引のみ（下界は 2210 円 32 点・v-span 94 ≤ 132）。

## 実行記録

1. **機械**: w=66 完走機（width66_level_classify.ts）の verbatim 移植
   （REST6 2フェーズ・窓マスク 67 ビット・ワード数 ceil(w/32) 自動・W=67）。
2. **窓マスク**: unique = maximal = **3,300**（w=66 と同数）。
   harness 制御: w=64→3,288・w=65→3,296・w=66→3,300 を本harnessで完全再現
   （既往値と一致・w=67 の 3,300 は偽でない）。
3. **chunks 1-3（本セッション）**: mask 0..769 完了
   （chunk1: 0→223〔~10.8k/mask〕・chunk2: 223→488〔~9.1k/mask〕・
   chunk3: 488→770〔~8.5k/mask〕・計 7.2M nodes・leaves=0・生残0・
   フェーズ2必要 mask 0件）。
4. **構造観察（w=66 との前置区間一致）**: chunks 1-2 の word-ops は
   w=66 の chunks 1-2 と完全一致（255673713 / 262407946）。
   → w=67 の maximal mask 列は mask 0..487 で w=66 と同一の前置区間を持ち、
   chunk 3 で初めて分岐。row 66 の追加は heavy band 前の軽い帯では
   mask 順序・DFS 挙動を保存する（窓位相 99 周期の構造と整合）。
5. resume from=770（lastDone 規約・+1 しない）。heavy band は w=66 とほぼ同位置
   （~772..）と予測。残り 2,530 mask・推定総 ~74M nodes。

## 意味論（P(67) は OPEN）

- 完走時（leaves=0・生残0）で **P(67) = 32 が等号付き・全称で確定**する。
  それまでは P(67) ∈ [32, 128] open。現在は部分進行（770/3,300 = 23.3%）。

## レジューム（次回の実行）

1. **w=67 キャンペーン継続**: output/width67_progress.json の chunks に追記
   （CFG.from=770・resume_from=lastDone を厳守・cap 2.4M/chunk・1実行1チャンク）。
2. 完走時は K0800（P(67)=32）に昇格・results/fixed-width/ 追従
   （pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0800**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。

## 第2セッション（chunks 4-8・heavy band 開始）

1. **chunks 4-8**: mask 770..839 を 5 チャンク（各 2.4M nodes cap）で完了。
   chunk4: 770→777（**~343k/mask・heavy band 開始**）・chunk5: 777→789（~200k）・
   chunk6: 789→807（~133k・減衰）・chunk7: 807→820（~185k・再上昇）・
   chunk8: 820→840（~120k）。
   **累計 21.6M nodes・leaves=0・生残0・phase2 必要 mask 0件**
   （840/3,300 = 25.5%）。resume from=840。
2. **heavy band 入り口は w=66 の約3倍重い**（~343k vs ~114k/mask）。
   総ノードは ×1.35 則の ~74M を上振れする可能性（第一帯の幅・dip 構造次第）。
   heavy band 位相自体は 99 周期窓構造で w=65/66 とほぼ同位置
   （開始 ~770..772）という観察は維持。
3. 反映: progress JSON 更新（bdf42bf・resume_from=840）。
   反映前 HEAD 6c323de4 再取得で並走なし。

## レジューム（次回の実行）

1. **w=67 キャンペーン継続**: CFG.from=840・resume_from=lastDone を厳守
   （cap 2.4M/chunk・1実行1チャンク・heavy band 継続中）。
2. 完走時は K0800（P(67)=32）に昇格・results/fixed-width/ 追従。
3. 次の空き K 番号: **K0800**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。

## 第3セッション（chunks 9-11）

1. **chunks 9-11**: mask 840..886 を 3 チャンクで完了。
   chunk9: 840→861（~114k/mask）・chunk10: 861→880（~126k）・
   chunk11: 880→887（**~343k・加重スパイク**）。
   **累計 31.2M nodes・887/3,300 = 26.9%・leaves=0・生残0・phase2 必要 mask 0件。**
2. **heavy band は ~343k/mask のスパイクと ~114..200k/mask の帯が交互**
   （w=66 の第一帯 ~86..150k より全体的に重い）。総計は ~74M を上振れ
   （~90M±）の可能性。heavy band 位相（開始 ~770..772）は w=65/66 と同一。
3. 反映: progress JSON 更新（e4ffb96e・resume_from=887・読み戻し検証済み）・
   script CFG.from=887・本log。反映前 HEAD a5229f7 再取得（並走なし）。

## レジューム（次回の実行）

1. **w=67 キャンペーン継続**: CFG.from=887・resume_from=lastDone を厳守
   （cap 2.4M/chunk・1実行1チャンク・第一 heavy band 継続中・~999 まで）。
2. 完走時は K0800（P(67)=32）に昇格・results/fixed-width/ 追従。
3. 次の空き K 番号: **K0800**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
## 第4セッション（chunks 12-17・第一 heavy band 減衰開始）

1. **chunks 12-17**: mask 887..986 を 6 チャンク（各 2.4M nodes cap）で完了。
   chunk12: 887→898（~218k/mask）・chunk13: 898→914（~150k）・
   chunk14: 914→928（~171k）・chunk15: 928→945（~141k）・
   chunk16: 945→970（**~96k・減衰**）・chunk17: 970→987（~141k・再上昇）。
   **累計 45.6M nodes・987/3,300 = 29.9%・leaves=0・生残0・phase2 必要 mask 0件。**
2. **第一 heavy band は後半で減衰し始めた**（chunk16 は 25 mask/2.4M = ~96k/mask）。
   w=65/66 の ~1000 dip 構造と整合し、第一帯終点 ~999..1310 の観測的予測を維持。
   総計推定は ~75..95M nodes（複数セッション必須）。
3. **K番号再採番**: 完走時の昇格先は **K0801**（K0800 は 2026-11-13 11:34 に
   joint g0 会計（w≤114・別レーン）が使用済み）。progress JSON の semantics を訂正済み。
4. 反映: progress JSON 更新（481c0734・resume_from=987・読み戻し検証済み）・
   script CFG.from=987（320bc4db）・本log。反映前 HEAD 8526387f 再取得（並走なし）。

## レジューム（次回の実行）

1. **w=67 キャンペーン継続**: CFG.from=987・resume_from=lastDone を厳守
   （cap 2.4M/chunk・1実行1〜2チャンク・第一 heavy band 減衰帯・dip 到達か注視）。
2. 完走時は K0801（P(67)=32）に昇格・results/fixed-width/ 追従
   （pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0801**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
