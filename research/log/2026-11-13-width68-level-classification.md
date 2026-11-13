# 2026-11-13 高速レーン: w=68 キャンペーン開始（K0801 P(67)=32 の直接続編）

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
3. **chunks 1-3（本セッション）**: mask 0..501 完了
   （chunk1: 0→104〔**~23k/mask・w=67 の約2.2倍**〕・chunk2: 104→297
   〔~12.4k〕・chunk3: 297→502〔~11.7k〕・計 7.2M nodes・leaves=0・
   生残0・phase2 必要 mask 0件）。
4. **観察**: w=68 は前置帯からすでに w=67 の約2倍重い。
   heavy band 入り口（~770 前後・窓位相不变則）の加重はさらに上振れの
   可能性 → 総計 110..170M nodes・複数セッション必須。
5. resume from=502（lastDone 規約・+1 しない）。

## 意味論（P(68) は OPEN）

- 完走時（leaves=0・生残0）で **P(68) = 32 が等号付き・全称で確定**する。
  それまでは P(68) ∈ [32, 130] open。現在は部分進行（502/3,300 = 15.2%）。

## レジューム（次回の実行）

1. **w=68 キャンペーン継続**: output/width68_progress.json の chunks に追記
   （CFG.from=502・resume_from=lastDone を厳守・cap 2.4M/chunk・1実行1〜2チャンク・
   heavy band 入り口 ~770± を注視）。
2. 完走時は K0802（P(68)=32・**反映前に K 番号の空きを再確認**）に昇格・
   results/fixed-width/ 追従（pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0802**（本log時点・要再確認）。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
