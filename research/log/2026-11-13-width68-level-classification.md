

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


## 第4セッション（chunks 14-24: mask 890..1222 = 37.1%・第一 heavy band 通過・~1000 dip・第二帯入り口到達）

1. **chunks 14-24**（REST6 2フェーズ機・repo script verbatim・cap 2.4M/chunk・
   境界は from=直前 lastDone verbatim で gap なし）: mask 890..1222 完了
   （chunk14: 890→900〔10 mask・~240k〕・chunk15: 900→915〔15・~160k〕・
   chunk16: 915→926〔11・~218k〕・chunk17: 926→933〔7・**~343k 局所ピーク**〕・
   chunk18: 933→944〔11・~218k〕・chunk19: 944→960〔16・~150k〕・
   chunk20: 960→972〔12・~200k〕・chunk21: 972→985〔13・~185k〕・
   chunk22: 985→1127〔**142 mask・~17k**〕・chunk23: 1127→1213〔86・~28k〕・
   chunk24: 1213→1223〔10・**~240k・第二帯入り口**〕・計 26.4M nodes・leaves=0・
   生残0・phase2 必要 mask 0件）。
2. **heavy band 構造（w=68 固有の観察）**: 第一 heavy band（~770..984）の
   加重は ~114..200k が主体で・chunk12-13 の ~480k/mask は band 内でも
   きわめて局在した最重要部（chunk14 以降はすぐ ~150..240k に減衰）。
   **~1000 で沈み込み（chunk22: ~17k/mask）→ ~1190 で第二 heavy band 再出現
   （chunk24: ~240k/mask）— w=65/66/67 と同一の窓位相**。第二帯終点は
   右肩上がり則（1302→1313→1320）から ~1330..1340 見込み。
3. **進捗**: mask 0..1222 = 1,223/3,300 = 37.1%・累計 55.2M+0.6M nodes。
   残り ~2,077 mask（第二帯 ~1330..1340 まで ~110 mask が重い・
   その後は軽い帯）→ 総計 ~65..90M nodes 見込み・複数セッション必須。
4. 反映: progress JSON（chunks 14-24 追記・resume_from=1223）・script
   CFG.from=1223 + header 更新・本log。全ファイル repo 読み戻し検証済み・
   並走なし（反映前 HEAD cfec308f 再取得・本セッションコミットは
   b91dc668〔progress〕・8cf667ef〔script〕のみ）。

## レジューム（次回の実行）— 更新

1. **w=68 キャンペーン継続**: CFG.from=1223 から（**次 chunk の from は
   直前 chunk の lastDone を verbatim で**・cap 2.4M/chunk・1実行1〜2チャンク・
   第二 heavy band ~1190..~1330..1340 を通過・終点以降は軽い帯で高速消化）。
2. 完走時は K0802（P(68)=32・**反映前に K 番号の空きを再確認**）に昇格・
   results/fixed-width/ 追従（pw_circle_point_max.csv・mwq_stabilization.csv・README）。
3. 次の空き K 番号: **K0802**（本log時点・要再確認）。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。


## 第5セッション（2026-11-14・完走: chunks 25-40 + ネイティブ独立全幅再実行 → **P(68)=32 確定・K0802 昇格**）

1. **実行環境の変化**: 本セッションはネイティブ Node.js（v22）実行
   （repo script と同一アルゴリズム・依存なし）。2.4M cap チャンクが
   **0.84秒/chunk**（sandbox の約 70 倍）→ 実行コストの壁が実質的に消滅。
2. **chunks 25-40（resume_from=1223 から）**: mask 1223..3299 完了
   （37,019,331 nodes・leaves=0・生残0・phase2 必要 mask 0件・境界は
   from=直前 lastDone verbatim で gap 0件・最終 chunk40 は 97 mask・
   1,019,331 nodes・capped なし完走）。第二 heavy band は **~1308 で終了**
   （w=67 の 1320 を下回り右肩上がり則 1302→1313→1320 の反例）。
   以降は ~9..18k/mask の軽い帯。
3. **独立全幅再実行**: from=0 から単一連続 42 チャンク・96,626,896 nodes・
   28.6秒・leaves=0・生残0・gap なし（mask 788/807 も in-flow に走査）。
   **2経路の完全走査で level 17 全滅を二重確認**。
4. **交差制御（全 PASS）**: 再実行 chunks 1-6 の境界と wordOps が sandbox
   記録と完全一致・classifyOne mask 788→314,127 / 807→273,404 nodes が
   gap 証明の記録値と完全一致・w26 L12 で S* ちょうど1生残・
   harness w64/65/66/67 unique=maximal 完全再現。
5. **確定**: level 17 全滅 + K0797 会計（w≤84 有効）+ 2210 円下界
   （v-span 94 ≤ 134）⟹ **P(68) = 32（等号付き・全称）**。
   **P(w) は全幅 w=6..68 で決定済み（32 プラトー 49..68）**・
   level 17 復活点は **(68,83]**。
6. 反映: progress JSON 完走化（chunks 25-40・nativeControls・
   independentFullRerun）・native completion JSON・script 完走注記・
   K0802 item・results/fixed-width 3点（pw 68行・mwq separation-band 68行・
   README w=6..68）・本log。全ファイル repo 読み戻し検証・並走なし
   （反映前 HEAD 2da32a85 再取得・本セッションコミットは
   2ed719e1〔progress〕・1d241bcb〔native〕・5ffe046b〔script〕・
   3d5fb795〔K0802〕のみ）。

## レジューム（次回の実行）— 完走後

1. **w=69..82 掃引（新レジューム・最優先）**: ネイティブ Node 実行により
   w=68 全幅が 28.6 秒 → w=69..82 の level 17 全滅掃引は
   1幅あたり ~40秒..数分で実行可能。各幅で leaves=0・生残0 なら
   P(w)=32（K0797 会計・2210 円下界は w≥49 で有効）。
   **P(w)=32 が w=69..82 まで拡大すれば復活点は (82,83] に狭窄**。
   機械は width68_level_classify.ts の W と CFG を差し替えるのみ
   （maximalMasks は任意 w で完備・maximal=3,300 は K0803 で w=66..132 保証）。
   w=83/84 は 34 点 witness（K0785/K0791・11050 円）が既知なので
   level 17 は死なないはず → 機械の正制御（生存検出）として使える。
2. K番号: 次の空きは **K0804**（K0802・K0803 使用済み・要再確認）。
3. 11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）のまま。
