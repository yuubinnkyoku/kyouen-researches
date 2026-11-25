# 2026-11-16：1396 baseline上の第三分岐（branch C head 1398 と branch D cost-67d head 1398'）の統合fold — head 1400（新canonical head）+ cost-67d foldのtmp再構成gap-fill

開始時main: `cd0f2b9f`（11×11レーンの最新は `dad77b79`〔本lane branch C・head 1398〕と `eee4f2713a`〔並走lane cost-67d・head 1398'〕）。**本laneがmerged 63h+63i+63j+65m foldでhead 1398/6450/509983/4720/373706をcanonical宣言した直後に、並走laneのcost-67d fold（`eee4f2713a`・merge `49d95d1d`）が同一の1396 baselineに67d bit-97 receipt 1件をfoldしてhead 1398/6450/509974/4720/373697を着地**。1396からの第三分岐が発生していた。本セッションは両枝を統合し、単一のcanonical headを確定した。

## 分岐の経緯

1. `a382ff47` 並走lane: cost-65m fold着地 **1396**/6452/510115/4722/373838。
2. `dad77b79` 本lane: merged 63h+63i+63j+65m fold着地 **1398**/6450/509983/4720/373706（63h bit-89 receiptを1396にfold）。1369/1396両head supersededを宣言。
3. `784f1499` 並走lane: cost-67d IN FLIGHT claim（child `00000000000000801202000040002000`・**1396 baseline**のまま・67 candidates・c2=1,c4=1需要）。
4. `eee4f2713a` 並走lane: cost-67d fold着地 **1398'**/6450/509974/4720/373697（1 WIN7-D10 bit-97・66 REFUTED・65,246,890 nodes・証明書46,661 rows/56 sub-roots）。**63h receiptを含まない別内容の1398**として着地（1398 baselineへのre-baseなし）。

両枝の公開head JSONは互いのreceiptを含まない（1398'側のtop-candidates CSVには63h child `00000000000000801202000040080000`が残行として存続）。

## gap-fill: `reconstruct_tmp_cost67d_20261116.py`

並走の67d fold scriptはruntime入力（`tmp-cost67d`中間体: legal-moves.json・bit97 cert-receipt/bigint/tsverify/consumed）を公開していなかった。本laneは `reconstruct_tmp_cost67d_20261116.py`（63h版と同一構成）を構築・実行し、公開成果物のみ（証明書bytes・`legal_candidates.py`独立列挙・tsverify〔Number Bareiss〕+BigInt両検証器の再実行）からtmp-cost67dを再構成した。**bit-97証明書46,661 rows / 1,685,346 bytes / md5 `2c316bb0138b82fb3c65dfcbc76e9645` が公開67d head JSON記録値と一致し、56 sub-roots全PASS・union 0/0・terminal [13,17]**。これにより67d fold scriptはfresh環境から完全再現可能になった。

## 統合fold（`recompute_frontier_merged_cost63h_63i_63j_65m_67d_20261116.py`）

1. **両枝の再現**: branch C（merged 63h+63i+63j+65m fold script）とbranch D（67d fold script）を各subprocessで再実行し、各3出力blobをmainとbyte-identicalで照合（branch C head JSON blob `a4cc8e95…`・branch D 67d head JSON blob `304c6afe…`）。単一プロセスで3鎖のrunpy namespaceを同時保持するとsandboxメモリ上限を超えるため、branchごとにsubprocess化して結果set等をdump経由で受け取る（各subprocessは公開scriptの全blob assertを含むため検証内容は不変）。
2. **分岐の集合等式**: `s_C == s_1396 ∪ cov(63h root)`・`s_D == s_1396 ∪ cov(67d root)` をassert。**枝間cover重複は0**（|cov(63h root)|=7・|cov(67d root)|=7・overlap=0）。
3. **root disjointness**: 67d bit-97 root `00000002000000801202000040002000` は705 folded roots（branch B 704 + 63h root）とraw-hex・D4ともdisjoint。branch D baseline（67d scriptのprev=704）はbranch C prevから63h rootを除いたものと一致。
4. **両childの1396 baselineでの残存確認**: 63h child `00000000000000801202000040080000` は三開親（第二候補9行/639・dual 69行/5265・class-4 77行/5548）の残行、67d child `00000000000000801202000040002000` は第二候補（9行/639）と67d parent2 `00000000000000801002000001080000`（84行/6410）の残行。需要 c1=0,c2=1,c4=1（67d）を再導出。
5. **証明書の再assert**: 67d bit-97証明書（46,661行・md5 `2c316bb…`）と63h bit-89証明書（26,070行・md5 `b721d428…`）のrows/md5・BigInt+tsverify union 0/0・terminal [13,17]を再確認。
6. **fold**: 63h bit-89 receipt（marginal 5・in-manifest 2）と67d bit-97 receipt（marginal 5・in-manifest 2）を1396 headにfold。両child orbitはそれぞれのreceiptで閉鎖。**in-manifest合計 +4 → solved 1400**。
7. **reverse-order replay**: branch D head 1398'に63h coversをfoldする逆順でも**同一のmerged setとsummary**が再現されることをassert（順序独立性）。

## 新canonical head: **1400/6448/509842/4718/373565**

- solved 1396→1400・remaining_s5_orbits 175→174・unique_remaining_s6 6452→6448・sum_remaining_cost 510115→509842・s6_needed_by_open_classes 4722→4718・cost_needed_by_open_classes 373838→373565。
- **第二候補S5 `00000000000000801202000040000000`: 9行/639 → 7行/509**（63h childと67d childの両方を喪失）。
- 63h childの開親: dual class-2+4 `00000000000000801202000000080000` 68行/5202（不変）・class-4 `00000000000000003800000001800000` 75行/5416（不変）。67d parent2 `00000000000000801002000001080000`: 84行/6410 → 82行/6269。63i第2開親 24行/1704（不変）。
- 出力: head JSON（blob `777474faf6730242b7e0080bfcdad390cca3a0ee`・7,460 B）・ranking CSV（`bd1c06140c69856764220563c3285d19251343ea`・7,535 B）・top-candidates CSV（`f9aa6e061279f3e84b830fbafe8d85403abbe7b6`・3,887 B）。**2回実行で3出力ともbyte-identical**。
- 本統合は既存の57 receipt（63i 18 + 63j 29 + 65m 8 + 63h 1 + 67d 1）の被覆集合の和に過ぎず、新たな探索結果は含まない。両方の1398 head（branch C・branch D）は**1400にsuperseded**。以後のfoldは1400 baselineへのre-base必須。

## 運用記録（実験事実）

- 本セッション中にsandbox環境リセットが発生し、未着地だったローカル作業（cost-70h sweep・証明書7件・前回統合fold実行一式）が消失した。**main着地済みの成果物には無影響**（「成果物は必ずmainに着地させてから次に進む」教訓の再確認）。70h lane（child `00000000000000801202000040000001`・第二候補S5のcost-70行・c1=0,c2=2,c4=0需要）は1回sweep完走（7 WIN7-D10・63 REFUTED・124,066,734 nodes・bits 18/24/28/59/89/112/120・証明書7件）したが**成果物が失われ未公開・未検証に戻った**。上記数値は再実行時の交叉確認材料としてのみ参照可能で、証拠としては扱わない。70hは次回以降の実行でsweepからやり直す。
- mirror再構築はcodeload zip → reconstruct script鎖（84a→83d→83c→83a→69i→62a→58c→63h→63i→63j→65m→67d〔本lane新規〕）→統合foldで完全fresh再現可能（計~10分）。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
