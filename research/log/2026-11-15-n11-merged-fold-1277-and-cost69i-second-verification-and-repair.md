# 2026-11-15：3-way merged fold(head 1277)の第二独立検証 + cost-69i証明書4件の第二独立検証 + tmp-cost69i再現性修復

開始時の想定: 前回知識からの継続状況は「65l/74g統合head 1270 と 69i fold head 1273(1266ベース)の分岐が未解決」だった。本セッションはこのunified foldを最優先として準備した(AGENTS.md・knowledge README・最新main・69i claim/log・両branch head JSONを確認し、runpy鎖とcovers再現が独立mirrorで動くことを確認済み)。

## 並走との衝突回避(collision protocol)

unified foldの着手準備中に最新mainを再取得したところ、**並走laneがまさに同一の3-way merged foldを着地済み**だった(`dde42161`・"class2-lane 3-way merged fold: resolve the 1257 fork of the concurrent cost-65l (head 1261), cost-74g (head 1266) and cost-69i (head 1273 ...) into the unified canonical head 1277/6570/518896/4840/382619")。同じfork解決を二重にpushする意味はないため、本セッションはfoldの重複実施を取りやめ、このrepoの定型である**第二独立検証**に切り替えた。以降の並走状況: K0783は74h sterile sweepと3-way merged foldまで記録済み(`7849312f`)・次のsweep候補(cost-75d)は並走がIN FLIGHT claim済み(`ab549094`)・5x23 q=6 longcapも並走claim済み(`eddb4f66`)。重複着手なし。

## 1. 3-way merged foldの第二独立検証 — 全統制PASS・3成果物byte-identical

codeload tarballから**本セッション専用の独立mirror**を再構築し(既存の作業環境とは別)、published 3-way merge script `recompute_frontier_merged_cost65l_74g_69i_20261115.py` の3成果物だけを削除してからend-to-end再実行した。

- 全統制PASS: fork 1257のrunpy再現(byte-identical・532 folded roots)・4つのbranch head JSON blob検証(65l `0b523e70`/74g `fce4ce77`/69i `8692a7a6`/merged65l-74g `02109530`)・16 receipt rootsの相互disjointness(raw+D4・65l-vs-69iと74g-vs-69iのcross-branchペアを含む)・pairwise covers overlap(A-B 0・A-C 0・**B-C 3 hexes**〔`...809102000000001000`・`...809102000000200000`・`...809102000020000000`・すべて74g側coversで先行被覆済み〕)・chain A/B/Cのper-bit marginalsがpublishedと完全一致・chain-C marginal deltas 0・set等式 `s_merged == union(s_1261, s_1266, s_1273) == s_1257 UNION covers(16 roots)`・逆順replay(69i first)同一集合・child closure 3件(65l bit21・74g bit4・69i bit21)・第三target S5の残行0。
- **head 1277/6570/518896/4840/382619 再現**・3成果物がmainとbyte-identical(head JSON 16,208 bytes・ranking CSV 7,539 bytes・top-candidates CSV 7,933 bytes)。
- per-parent: 第二coverable class-2 target 17行/1325・class-4 lift親(65l) 75行/5519・第三target 0/0閉鎖・74g parent2 55行/4143・69i parent2 69行/5265・69i parent3(class-4) 79行/6427。

## 2. cost-69i証明書4件の第二独立検証 — BigInt・Bareiss両系統で4/4 PASS

3-way merged foldの16 receiptsのうち、**cost-69iの4枚(204,339行)はこれまで一度の検証セッションしか通っていなかった**(69i laneがBigInt+Bareissを実施)。本セッションは公開証明書bytes(bit21/bit97は単一ファイル・bit29/bit100は行境界2パートをCRLF→LF正規化join)に対し、**published独立検証器2系統を別セッションで再実行**した:

| bit | mobility | rows | BigInt union 0/0 | Bareiss union 0/0 | 終端 |
|---|---:|---:|---|---|---|
| 21 | 56 | 49,504 | PASS | PASS | [13,17] / {13,15,17} |
| 29 | 56 | 70,471 | PASS | PASS | [13,17] / {13,15,17} |
| 97 | 46 | 27,080 | PASS | PASS | [13,17] / {13,15,17} |
| 100 | 58 | 57,284 | PASS | PASS | [13,17] / {13,15,17} |

- BigInt検証器(`verify_win7_certificate_bigint_independent.mjs`・BigInt 3x3余因子展開): 4/4 "WIN7 certificate independently verified"。rows合計 **204,339**・sub-roots 56/56/46/58 = **216**・union missing/extra 0/0・terminal_range [13,17]・rows sorted-unique。md5はpublished head JSON記録と全件一致(bit21 `ef66f198`ほか)。
- Bareiss検証器(`verify_cost73h_win7_bareiss_independent.py`・純Python整数Bareiss 4x4・汎用引数で再利用): 4/4 PASS。consumed == strategy rows(union 0/0)・loser全応手展開・terminal石数 {13,15,17}([13,17]の部分集合で正しい)。
- TS検証器(`verify_bit7_win7_cert.ts`・Number-Bareiss)もsub-root分解検証で4/4 PASS(root-check stones=7/loserMobility一致・全sub-root range ⊆ [13,17]・consumed union == 証明書行集合)。

## 3. tmp-cost69i再現性修復 — published fold scriptがmainのみから再実行可能に

**発見した再現性ギャップ**: published 69i fold script `recompute_frontier_cost69i_receipts_20261115.py` は作業dir `output/tmp-cost69i/`(legal-moves.json・bit毎のcert-receipt/bigint/tsverify/consumed)を要求するが、**69i laneはこれをpushしていなかった**。ためmainのみからfold scriptをend-to-end再実行できなかった(再現確認が`sweep再導出`までで停止)。他のfold(tmp-cost70e/70f/72c/74g/78a)はすべてpush済みで、69iだけが例外だった。

**修復**: `scripts/reconstruct_tmp_cost69i_20261115.py` を新規作成し、main上の成果物のみからtmp-cost69iを再生した:

- cert-receipt.json: 公開証明書bytesから再計算(md5/rows/bytesがpublished head JSON記録と全件一致)。
- legal-moves.json: 各7石rootの合法応手を整数Bareiss 4x4で再計算。mobility 56/56/46/58がpublished `sub_roots_pass`と完全一致。
- bigint.json: published BigInt検証器の別セッションでの新たな再実行(union 0/0)。
- tsverify.json: published TS検証器の再実行(root-check行 + 全合法応手の--subroots行)。
- consumed.txt: 同TS実行の`--consumed-out`出力(集合==証明書行集合)。

**検証**: 修復後にpublished fold scriptをend-to-end再実行し、**全統制PASS・head 1273/6574/519179/4844/382902再現・3成果物がpublishedとbyte-identical**(head JSON blob `8692a7a6`・ranking CSV `7ce2e616`・top-candidates CSV `945f6556`)。completed claimのfold record再assertもPASS。

**push**: 13小ファイル + 再構成script + README(1コミット・remote blob sha照合済み: README `4ca69bca`・legal-moves `5b1cf377`・script `7bd7b3ab`ほか)。**consumed.txtのうちbit97(1,249,347 bytes・remote blob `d7023de5`・byte照合済み)のみpush**。bit21/100/29(2.24/2.58/3.34 MB)は本toolchainの1プログラム16 MiB制限によりpush不可(2.24 MBはchunked read 36 opでもbash cat 1 opでもMemoryLimitError・1.25 MBは成功)→ **再構成scriptが常に4件とも再生**するためmainからの再現性は完全。READMEにこの状況と再現コマンドを明記。

## 信頼境界

- solved 1277はmanifest被覆の簿記であり、いかなる局面の勝敗判定でもない。REFUTED-D10はLOSS証明ではない。第三target S5の閉鎖はmanifest被覆に基づく条件付き閉鎖。
- 本セッションの検証はpublished成果物に対する第二独立検証であり、新しいverdictを生成するものではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4はいずれもUNKNOWN**。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost69i_20261115.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost65l_74g_69i_20261115.py   # head 1277
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69i_receipts_20261115.py        # head 1273
```

いずれもmainのみから実行可能(実行時間: 再構成~18s・fold各~2s・BigInt/Bareiss検証 合計~90s)。

## レジューム

- canonical headは**1277/6570/518896/4840/382619**(`class-frontier-merged-cost65l-74g-69i-recompute-20261115.json`)。次のfold baselineはこのhead。
- 第二coverable class-2 target 17行/1325・audit-blocked S5 10行/698・best class-4 `00000000020000003800000080000000` 18行/1460。cost-75d(第二targetの次安行)は並走IN FLIGHT。
- 大きいテキスト(>1.5 MB)の単発pushは本toolchainでは不可。生ログ等は行境界パート分割でpushするか、再生script経由とする。
