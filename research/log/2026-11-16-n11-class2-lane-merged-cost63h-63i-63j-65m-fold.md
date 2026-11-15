# 2026-11-16：cost-63h+63i と cost-63j+63j+65m receipts chain の再分岐統合fold — head 1396 + 63h receipt → 1398（新canonical head）

開始時main: `a382ff47`（調査中に `784f1499` まで進行）。**前回の統合fold（`c3bd5b4f`・17:37Z）がhead 1369/6479/512163/4749/375886を新canonicalと宣言し「以後のfoldはmerged headへのre-base必須」と記録した直後に、並走laneのcost-63j fold（`50e6a1b3`・17:58Z）がclaimの1367 baselineのまま29 receiptをfoldしてhead 1394を着地**（re-baseされず）、さらにcost-64a sterile（`1faa8559`・foldなし）を挟んでcost-65m fold（`a382ff47`・18:44Z）で**head 1396/6452/510115/4722/373838**まで進行。63h bit-89 receiptが正規chainから外れたまま、receipts chainが再び分岐していた。本セッションは両枝を統合し、単一のcanonical headを確定した。

## 分岐の経緯（時系列）

1. `4e3fcf00`（17:29Z）並走lane: cost-63j IN FLIGHT claim（1367 baseline）。
2. `c3bd5b4f`（17:37Z）本lane: merged 63h+63i fold着地、head **1369**をcanonical宣言・re-base必須を記録。
3. `50e6a1b3`（17:58Z）並走lane: cost-63j fold着地 **1394** — ただし1367 baselineのまま（1369へのre-baseなし）。
4. `e903c046`→`1faa8559`（18:14/18:18Z）並走lane: cost-64a sweep **STERILE**（64/64 REFUTED-D10、証明書なし、foldなし・head不変）。
5. `01df8116`（18:20Z）並走lane: cost-65m IN FLIGHT claim（1394 baseline）。`a382ff47`（18:44Z）: cost-65m fold着地 **1396**（8 receipt）。
6. `784f1499`（19:03Z）並走lane: cost-67d IN FLIGHT claim（child `00000000000000801202000040002000`・**1396 baseline**・67 candidates）。

両枝の公開head JSONは互いのreceiptを含まない（1396側のtop-candidates CSVには63h child `00000000000000801202000040080000`（cost-63・c2=2,c4=2）が第二候補S5の残行として復活している）。

## 統合fold（`recompute_frontier_merged_cost63h_63i_63j_65m_20261116.py`）

1. **両枝の再現**: 65m fold script（runpy）で1360→1367→1394→**1396**を、merged 63h+63i fold script（runpy）で1360→1367→**1369**を再現。両枝とも3出力blobをmainとbyte-identicalで照合（65m head `9798a9fc…`・merged head `c3ff5036…`）。各scriptは58c chain head 1360のbyte-identical再現まで含む。
2. **分岐の集合等式**: `s_1369 == s_1367 ∪ cov(63h root)`・`s_1396 == s_1367 ∪ cov(29×63j + 8×65m roots)`・`s_1394 == s_1367 ∪ cov(29×63j)` をassert。**枝間cover重複は0**（|cov(63h root)|=7・|cov(37×63j+65m)|=213・overlap=0）。37 coversのmarginalは1367/1369のいずれでも173、63h coversのmarginalは1367/1396のいずれでも5。
3. **root disjointness**: 63h bit-89 root `00000000020000801202000040080000` はbranch Bの704 folded roots（58cまで649 + 63i 18 + 63j 29 + 65m 8）とraw-hex・D4ともdisjoint。63jの29 root・65mの8 rootは公開head JSONのaddition記録と交叉照合。
4. **63h childの1396 headでの残存確認**: child `00000000000000801202000040080000` は三開親の残行（第二候補9行/639・dual class-2+4 69行/5265・class-4 77行/5548）で需要 c1=0,c2=2,c4=2・lift stones {19, 30, 57} を再導出。
5. **証明書の再assert**: bit-89証明書（26,070行・941,299 bytes・md5 `b721d428…`）を公開bytesと照合し、BigInt+tsverify union 0/0・terminal [13,17]・rows sorted-uniqueを再確認。
6. **fold**: bit-89 receiptを1396 headにfold。**marginal 5・in-manifest 2**（child `00000000000000801202000040080000` + bonus orbit `00000000020000801002000040080000`）・child orbitはbit 89で閉鎖。
7. **reverse-order replay**: 1369 headに37×63j+65m coversをfoldする逆順でも**同一のmerged setとsummary**が再現されることをassert（順序独立性）。

## 新canonical head: **1398/6450/509983/4720/373706**

- solved 1396→1398（in-manifest +2）・unique_remaining_s6 6452→6450・sum_remaining_cost 510115→509983・s6_needed_by_open_classes 4722→4720・cost_needed_by_open_classes 373838→373706。
- **第二候補S5 `00000000000000801202000040000000`: 9行/639 → 8行/576**（63h childのみ喪失。1369→1396の間に63j/65m foldで失われた7行と合わせ、1367当時17行/1185から計9行減）。
- dual class-2+4 S5 `00000000000000801202000000080000`: 69行/5265 → 68行/5202。class-4 S5 `00000000000000003800000001800000`: 77行/5548 → 75行/5416（bonus orbit閉鎖込み）。63i第2開親 `00000000000000403800000008000000`: 24行/1704（不変）。
- best coverable class-2は `00000000000000801202000000200000` 3行/209（全残行REFUTED-D10でdepth-10 receipt閉鎖不能・従来通り）。best class-4 blocker S5は `00000000020000003800000080000000` 18行/1460。
- 出力: head JSON（blob `a4cc8e95145a8796ff53b7686bf9cffc3d6e24cb`・7,265 B）・ranking CSV（`bf72d659261ee23a5ea49bb48dc8293482e3aff2`・7,535 B）・top-candidates CSV（`e786e6e35e0961cda6a3eeab101b7ca5d4ed4340`・3,973 B）。**2回実行で3出力ともbyte-identical**（実行時間各~23秒）。
- gap-fill: 65m fold scriptのruntime入力（tmp-cost65m中間体）は公開されていなかったため、本laneは `reconstruct_tmp_cost65m_20261116.py` を独自に構築・実行してtmp層を再構成し、65m fold scriptのfresh実行で3出力がmainとbyte-identicalになることを確認済み。並走laneも `784f1499` で同一目的・同一構成（legal_candidates再計算・split parts結合・tsverify+BigInt再実行）のreconstruct scriptを独立に公開済みであり、公開版を正とする（重複pushは行わない）。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書はbit-89 rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10（cost-64a の64/64を含む）はLOSS証明ではない。
- 統合は既存の56 receipt（63i 18 + 63j 29 + 65m 8 + 63h 1）の被覆集合の和に過ぎず、新たな探索結果は含まない。1369・1396の両branch headは1398にsuperseded。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost65m_20261116.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost63h_63i_63j_65m_20261116.py
```

(tmp-cost58c/63h/63i/63j/65m等の中間体は既存のreconstruct script群で再構成済みの前提。統合fold script自体は両枝のscriptをrunpyで再実行するため、~23秒で完了。)

## 次の一手

- **以後のfoldはmerged head 1398/6450/509983/4720/373706へのre-baseが必須**（branch head 1369・1396ともsuperseded）。
- **並走laneのcost-67d IN FLIGHT claim（`784f1499`・child `00000000000000801202000040002000`）は1396 baseline**のため、着地時は1398 baselineに更新し、67d rootsと63h bit-89 rootのdisjointnessをassertすること。本laneは着手禁止。
- 次回定型: 監査v11（両実装+agreement v8）はbranch Aの1369 endpointまでのみ。63j 29 + 65m 8 receiptと本統合foldを組み込む **v12拡張**（両実装+agreement v9、1398 endpoint）を機械的に行う。
- 第二候補S5（8行/576）の次の安い未sweep・未claim行: 67dがIN FLIGHTのため、その次のcost帯（cost-70/71/75…）をclaim前に確認。
