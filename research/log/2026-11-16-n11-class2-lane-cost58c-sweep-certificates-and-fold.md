# 2026-11-16：cost-58c sweep・WIN7証明書34件・receipt fold — 第二候補S5が34→21行（head 1326→1360）

開始時main: `47558fdfe`（cost-62a fold後のhead 1326/6522/515251/4792/378974）。第二coverable class-2 candidate S5 `00000000000000801202000040000000` のcost-58 child `00000000000000801206000040000000`（stones [30,49,50,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二候補とclass-2 S5 `00000000000000403800000008000000`）をcost-58cとしてsweepした。

## sweep（v16 d10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）

**58/58候補・WIN7-D10 34件・24 REFUTED-D10・0 capped・総nodes 48,542,211**。terminal範囲は [11,17] を含む（密な子で早期終局あり）。batch-5 determinism rerun node-exact、v15交差エンジンで34 WIN loss=true（sum 84,716,286）・REFUTEDアンカーbits 0/2/4 loss=false・pilot 5949。

## 証明書34件（blind抽出・二重独立検証）

34 WIN rootsをblind抽出。合計**1,156,691行・41,777,346 bytes・1,607 sub-roots**。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**33/33 PASS**（union 0/0）。

**bit76のみBigInt検証器が拒否**：証明書のterminal範囲が11..17（密な子で合法手が尽きる早期終局）で、検証器の13..17ガードに掛かる。v16/v15両エンジンでWIN7-D10は確認済み。foldからは除外し、検証器の制約として記録。

## receipt fold（head 1326 → 1360）

`recompute_frontier_cost58c_receipts_20261116.py` はcost-62a fold scriptをrunpyで再実行してhead 1326/6522/515251/4792/378974をbyte-identicalに再現し、公開順で33 receipt（bit76除外）をfoldした。

- 新canonical head: **`1360/6488/512785/4758/376508`**（solved 1326→1360、in-manifest marginal 34、raw marginal 166、zero-mim 8件）。
- child `00000000000000801206000040000000` は**bit1**で閉鎖。
- **第二候補S5: 34行/2368 → 21行/1454**（child+12親orbit喪失）。
- 第2開親 `00000000000000403800000008000000`: 49行/3525 → 27行/1915（child+21親orbit喪失）。
- set等式 `s_after == s_1326 ∪ covers(33 roots)`、616 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `62a411bb…`・26,118 B）、ranking CSV（`29b901b7…`・7,537 B）、top-candidates CSV（`ba0a9311…`・5,093 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **bit76の証明書はterminal 11..17のためBigInt検証器の13..17ガードに掛かり、foldから除外**（v16/v15のWIN判定は有効）。検証器の一般化は別課題。
- 第二target S5（3行/209）は全残行REFUTED-D10でdepth-10 receipt限界のまま。第二候補S5は残り21行で未解決。best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 並走・次の一手

- 第二候補S5の次の未sweep行（cost-63 4行など）とclass-4 blocker S5の残行が候補。
- bit76型の早期終局証明書を扱えるよう、terminal範囲ガードの一般化を検討。
- 以後のfoldは新head 1360へのrebaseが必須。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost58c_receipts_20261116.py
```

cost-62a baselineを再実行し、head 1326のbyte-identical再現から33 receiptsをfoldする。実行時間は約2〜3分。
