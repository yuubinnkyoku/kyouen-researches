# 2026-11-16：cost-75e 出版パイプライン完遂 — raw sweep再実行node-exact・4 WIN7-D10証明書公開（bit6はparts+receipt）・reconstruction chain再現・reconciled head 1405へのfold成功 → 新head 1407/6441/509300/4711/373023

開始時main: `71fa24c7`（S7/S8 overlap audit）。対象は本レーン（長期レーン）claimのcost-75e（child `00000000040000809002000000000002`・第二coverable class-2 candidate S5 `00000000000000801202000040000000` のcost-75行・75候補）。前回セッションは環境喪失でraw artifactsを喪失（claim memoのみ残存・publication_todo 5項目）。本セッションでtodo全項目を完遂し、claimをcompletedに引退させた。

## 実施内容

### 1. raw sweepの再実行と公開（commit `725f4b65`）
- v16 engine（blob `0a4a86f6…`検証済み）で全75候補を再実行: WIN bits [6,10,11,37]・71 REFUTED・0 capped・総nodes 108,292,517 — **outage前のmemo値と完全一致**。pilot 10×3402・terminal [13,17]・andclose全。
- 決定性再実行batch5（bits 47,48,53,54,56,57,59,61）node-exact。**v15交差**を完走（pilot 5949・WIN 4 bits全てloss=true・REFUTEDアンカー96/98/114 loss=false）。
- 10 raw batch JSONL + determinism rerun + v15 crosscheck + sweep audit（blob `ef813af4b9046e390962cfc09214d645c8f00727`・per-batch blob sha pin込み）を公開。raw CDN md5照合13/13 byte-exact。

### 2. 4 WIN7-D10証明書の完成・公開（commits `dca46d09`/`5cf7f657`/`a27d240d`/`beb6c605`/`0fd2b1f9`/`99ff9f19`）
- repo正本extractor + cert_driver75e.ts・空kill table・part1of1単一チャンクで抽出、sort -u + header/root行付与:
  - bit6 `…42`: 60,952 rows / 66 sub-roots / 21,156,914 nodes / 2,207,870B / md5 `fb4da316…`
  - bit10 `…402`: 43,842 rows / 55 sub-roots / 14,525,510 nodes / 1,585,948B / md5 `27bbc413…`
  - bit11 `…802`: 51,382 rows / 59 sub-roots / 13,290,884 nodes / 1,859,623B / md5 `b517acf9…`（**memo値とbyte-exact**）
  - bit37 `…002`: 46,987 rows / 54 sub-roots / 13,202,647 nodes / 1,698,634B / md5 `d14af659…`（outageで未完だった分を本セッションで完成）
- 全件BigInt検証器 union 0/0・terminal [13,17]、Bareiss verify全sub-roots PASS、root mobility=legal_candidates.py列挙とbit-exact。合計 rows 203,163 / extraction nodes 62,175,955 / cert bytes 7,352,075。
- **bit6（2.2MB）はpushツールの単一ファイル上限を超えるため、77e方式のpart1of2/part2of2（行境界分割）+ receiptで公開**。cat part1 part2がwhole md5 `fb4da316…`を再現（CDN取得bytesから確認・per-part git blob sha `406e072b…`/`a7dc3c6c…`照合）。manifest `class2-lane-cost75e-win7-certificates-20261116.json`（blob `a8127435…`）のbit6エントリをparts構成に修正して公開。

### 3. reconstruction chain再現（13スクリプト: 84a→83d→83c→83a→69i→62a→58c→63h→63i→63j→65m→67d→70g）
- 全tmp-cost成果物をmain出版済み成果物から再構成し、`recompute_frontier_rebase_facts_75e_76c_20261116.py` が**head 1405/6443/509457/4713/373180をend-to-end再現**・reconciliation 3出力blob（`b3ad19d7…`/`26fa720b…`/`c3433eee…`）byte-identical・rebase-facts出力（blob `8a811317…`）byte-identical・75e/76c両childのgenuinely remaining確認。

### 4. fold（`scripts/recompute_frontier_cost75e_receipts_20261116.py`・出力3点公開・全CDN md5照合OK）
- fold前確認: 76d/77e foldは未着地 → 1405基準で実施（並走のK0832高速レーンコミットはパス非競合）。
- sweep再導出（10 raw batch blob-pinned: 75候補・WIN [6,10,11,37]・71 REFUTED・0 capped・108,292,517 nodes・determinism node-exact・v15一致）、4証明書再assert（manifest blob pin・md5・sorted-unique rows・BigInt 0/0・Bareiss・bit6 parts receipt）、**root disjointness 4 vs 713 folded roots（raw + D4）**、child genuinely remaining at 1405（両open parentがchild行をedge 75で保持・demand c1=0,c2=2,c4=0）。
- fold（公開順 bits 6/10/11/37）: **total marginal 19 / in-manifest 2**。子orbitはbit6 receiptでちょうど1回閉鎖。bit10は第2のin-manifest marginal `00000000000000801202000000000201` を閉鎖（**75e parent2と70g parent2の両方の行だった**・edge 82ずつ — 事前予測の「67→66/5398」ではなく67→**65/5316**、70g parent2も48→47/3803）。bit11/37はzero-mim。逆順replay（37→6）同一集合・同一summary（子はbit37で閉鎖）。
- **新head 1407/174/6441/509300/4711/373023**（solved 1405→1407・unique_remaining 6443→6441・sum_remaining_cost 509457→509300=−75−82）。
- parents: second candidate S5 6/439→**5/364**、cost75e_parent2 67/5473→**65/5316**、cost70g_parent2 48/3885→**47/3803**、他4 parent不変。
- rankings: best class2 `…200000` 3/209不変（audit-blocked `…9082000000` 10/698不変）・best class4 18/1460不変。
- 出力: head JSON（blob `5cd93de7…`）+ ranking CSV（`2154bcb9…`）+ top-candidates CSV（`08aaf318…`）。

### 5. claim引退（`class2-lane-cost75e-inflight-20261116.json` → schema v3 completed・blob `36fc23a7…`）
- status/titleをcompletedに更新、`completion_record`（publication_todo 5項目全完了）・`fold_record`（新head・marginals・parents・逆順replay）・`rebase_note`（1400 superseded → 1405 → 1407）・`coordination_after_fold` を追加。既存キーは全保持（outage memoはhistorical recordとして明記）。

## 意義

1. **75e claim完遂**: outageで失われたraw artifactsを再実行でnode-exact復元し、bit37証明書を完成させ、4枚の証明書を全て第三環境から独立検証可能な形（byte pin + BigInt/Bareiss + legal_candidates交差）で公開した。
2. **第二coverable class-2 candidate S5の残行が5行/364に**（STERILE 64/71を除くと実質残3行: 76/76/77 — うち76cがin-flight）。
3. fold機構の追試: in-manifest marginalがchild以外に寄与する初例（bit10 marginalが2 parentの行を同時に落とす）を記録し、marginal/mimの導出が予測通り機能することを確認。
4. bit6の2.2MB制限対策として**part分割+receiptの77e方式を75eでも確立**（16MiB push制限の境界: ~1.9MB着地・2.2MBはpush前に失敗）。

## 解釈境界（重要）

- WIN7-D10証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。STERILE行は閉鎖不能の表明でLOSS証明ではない。
- solved 1407はmanifest被覆の簿記であり、いかなる局面の勝敗も確定しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 76c claim（in-flight・着手禁止）は1407へre-baseが必要。76d/77e foldが1405基準で着地した場合、1407とのreconciliation foldが必要（当該reconciliationは本4 rootとのdisjointnessをassertすること）。
- 次の候補: 第二coverable class-2 candidate S5の残5行のうち非STERILEは3行 — 76c child `00000000010000809002000001000000`（76c lane in-flight）・76d child `00000000040000003800080008000000`（76d lane・証明書bits 19/49公開済み・fold未着地）・77e child `00000000040000809002000000004000`（77e lane・証明書bits 37/69公開済み・fold未着地）。76d/77e fold着地により残る非STERILE行は76c childのみとなる見通し。
