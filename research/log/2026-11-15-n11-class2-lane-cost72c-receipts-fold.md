# 2026-11-15：cost-72c receipt fold — head 1239→1244

開始時main: `51b766410`（cost-70f fold後のhead 1239/6608/521701/4878/385424）。cost-72cは第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-72 child `00000000000000801202000000220000`（stones [17,21,49,57,60,71]・需要 c1=0,c2=2,c4=0）のsweepで、9 WIN7-D10 roots（bits 1,7,24,39,59,64,67,72,96）の証明書9件・独立監査・claim v2が公開済みで、receipt foldだけが未着地だった。AGENTS.md、`research/knowledge/README.md`、K0783、直近のn11 log・experimentを確認した。

## 入力検証

- 9証明書の公開2 partを行境界連結・CRLF→LF正規化すると、公開manifestのwhole md5/bytesと9/9一致（合計321,781行・11,604,178 B・41,346,462 extraction nodes・sub-roots 474）。
- 9 rootの全loser初手を独立列挙（mobility 61/47/59/46/53/52/53/47/56）。
- **BigInt 3x3余因子**と**Number Bareiss 4x4**の二独立検証器で9/9 PASS（union missing/extra 0/0・terminal [13,17]・consumed union == 証明書行集合 0/0）。
- sweep auditを9 raw batchから再導出: 72候補==claim列挙・9 WIN7-D10 / 63 REFUTED-D10 / 0 capped / 61,297,942 nodes・pilots 3402×9・determinism rerun node-exact・v15 9/9 WIN + 3/3 refuted anchors（pilot 5949×3）。
- head-1239でchildはmanifest内・未解決、両開親 `00000000000000801202000000200000`（24行/1836）と `00000000000000083800000008000000`（55行/4111）がchild行を保持。一石削除D4正準化でdel 17→parent1・del 21→parent2・他4削除は閉行。需要 c1=0,c2=2,c4=0。

## fold（head 1239 → 1244）

`recompute_frontier_cost72c_receipts_20261115.py` はcost-70f fold scriptをrunpyで再実行してhead 1239をbyte-identicalに再現し、公開順 [1,7,24,39,59,64,67,72,96] で9 receiptをfoldした。

- 新canonical head: **`1244/6603/521339/4873/385062`**（solved 1239→1244、in-manifest marginal 5、raw marginal 43、zero-mim bits 39/59/64/72/96）。
- child `00000000000000801202000000220000` は**bit1**で閉鎖。
- 第2 target S5: **24行/1836 → 21行/1615**（child + `00000000000000801202000000200002` + `00000000000000881202000000200000`）。
- 第2開親 `00000000000000083800000008000000`: **55行/4111 → 52行/3898**（child + `00000000000000083800000009000000` + `00000000000000801202000000020080`）。
- set等式 `s_after == s_1239 ∪ covers(9 roots)`、503 folded rootsとのraw/D4 disjointness、sweep audit再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `2e5d7ed187b40052d62344b0fbd5a7024ffa9899`・12,264 B）、ranking CSV（`6c36559906eafc30910abd087cdbe2f044159a16`・7,580 B）、top-candidates CSV（`c7497f2f6f5e72a170c34a12d30056a0f063c9eb`・5,007 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- child orbitの閉鎖は両S5親の残り行からchildを除くが、どちらのS5も未解決のまま。第2 targetは残り21行/1615。
- 証明書木そのものの再走査は本foldの範囲外。公開manifestの二重独立検証に依拠し、foldはjoined LF bytes・root同定・sub-roots・終端範囲・親orbit・D4正準性を再検証した。

## 並走・次の一手

- cost-70g（8 WIN7証明書・fold待ち）は新head 1244へのrebaseが必須。cost70f bit84とcost70g bit29のD4重複により、70g child行は70f foldで既に被覆済み（二重計上しない）。
- cost-65l（fold in flight）・cost-69g/74eは本foldに含めない。
- 第2 target S5は残り21行/1615。次の最安未sweep行の選定が続きの一手。

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class1・class2・class4はすべて **UNKNOWN**。今回のfoldは勝敗判定を変更しない。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost72c_receipts_20261115.py
```

cost-70f baselineを再実行し、head 1239のbyte-identical再現から全制約を再検証した上でfoldする。実行時間は約1〜2分。
