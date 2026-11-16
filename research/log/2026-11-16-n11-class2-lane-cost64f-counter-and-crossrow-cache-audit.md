# 2026-11-16：cost-64f verdict count correction + D4 cross-row cache reuse audit

## 発見した不整合

cost-64f completed claim v3 の `results.refuted_d10_count` が **64** になっていたが、これは64候補の総数を誤って入れた値だった。生の8 batchを再集計すると、59 sweep候補は **WIN7-D10 3件・REFUTED-D10 56件・capped 0件**。事前転送の5候補もすべてREFUTED-D10なので、64候補全体の正しい内訳は **WIN 3・REFUTED 61・capped 0**。

8 raw batchのGit blob SHAはclaimのpinと全件一致。pilotは8/8で3402 nodes、sweep bit集合はclaimの59 open bitsと完全一致、node合計54,905,391も一致した。よって探索結果ではなく、claimの集計欄だけの誤りである。

claim v4で `refuted_d10_count` を61へ修正し、56 swept / 5 transferred / 64 determinedを別欄に分けた。旧v3 blob `5159e0ac0ba9591e95ee6a9ab7a01aeb9e899f6e` は `supersedes` 履歴に残した。

## cost-64f結果のD4 cache再利用

head-1435 v2 presweepの最安8行（計515候補枠）と、cost-64fの64候補をD4正準形で突き合わせた。

| 指標 | 結果 |
|---|---:|
| cost-64f root | 64 |
| 異なるD4軌道 | 64 |
| 事前にopenだった候補枠 | 302 |
| 新たに判定できた候補枠 | 60 |
| 残るopen候補枠 | 242 |
| WIN/REFUTED矛盾 | 0 |

特に大きいのは、cost-64fの子 `0000000000000080120a000000800000`。既知REFUTED 5件を除く59 open bitすべてが今回の64 verdictで埋まり、**64/64候補が確定**した。3 WIN証明書のうちbit39がこの行を閉じ、bit107も同じ行と別の2行を覆う。manifest foldはまだ行っていない。

別のcost-65行 `00000000000000801202010000800000` にも1件のD4同値転送が見つかった。行bit51がcost-64f bit40と同じ正準rootになり、60 openから59 openへ減った。ほかの6行に新規hitはなく、矛盾は0。

## 次候補の再確認

cost-64fのreceipt-ready行を除外した後の最安open候補は、共有S5親 `00000000000000003800000008002000` の

`00000000000100003800000008080000`

で、cost 64・59 open bit。cost-64f cache hitは0。次点のcost-65行は1件転送後も59 openだが、辺費用が1高い。GitHubの現行main検索ではこの子を対象とする既存claimは見つからなかった（歴史ログ・候補表・STERILE近傍監査への言及のみ）。

この選定は **cost-64f fold後の予測**。headは依然1435であり、次候補をclaim・sweepしたわけではない。

## 保存・検証

- claim v4: [class2-lane-cost64f-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-inflight-20261116.json)
- 監査コード: [audit_cost64f_counter_and_crossrow_cache_20261116.cjs](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost64f_counter_and_crossrow_cache_20261116.cjs)
- 監査結果: [class2-lane-cost64f-counter-and-crossrow-cache-audit-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-counter-and-crossrow-cache-audit-20261116.json)

監査の同等な純JavaScript計算はV8 tool runtimeで実行した。Node版スクリプト自体のローカル実行は、Proxmox VM124がIO-ERRORとなり、pve-hp-aioのlocal-lvm thin poolが100% fullだったため未実施。ストレージ復旧・VM再起動・探索ジョブ起動は行っていない。原因をこの監査作業に帰属させる根拠はない。

## 解釈境界

- WIN7-D10は各7石rootの先手勝利のみ。REFUTED-D10はLOSS証明ではない。
- cost-64fの3 receiptsは未fold。canonical headは **1435/174/6413/507337/4686/371251** のまま。
- 予測head **1438/174/6410/507143/4683/371057** はmanifest簿記の予測で、確定headではない。
- 標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべて **UNKNOWN**。
