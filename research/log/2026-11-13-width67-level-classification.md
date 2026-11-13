# 2026-11-13 高速レーン: w=67 キャンペーン開始（K0799 P(66)=32 の直接続編）

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
