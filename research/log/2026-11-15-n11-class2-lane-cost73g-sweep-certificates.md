# 2026-11-15：cost-73g sweep + WIN7証明書8枚 — 第2target S5のcost 73行を閉じるreceipts（foldは次回）

開始時状況: 前セッション継続。cost-72c receipts fold後のcanonical head **1244/6603/521339/4873/385062**（blob `42dbb92e`）をbaselineに、第2coverable class-2 target S5 `00000000000000801202000000200000`（21行/1615）の最安未sweep行 **child `00000000000000849002000000000800`（edge cost 73・需要 c1=0,c2=2,c4=0・stones [11,49,60,63,66,71]）**をclaim v1（IN FLIGHT）で確保し、73候補のdepth-10 sweepを完走していた。両開親は parent1 = 第2target S5そのもの（del66でbit-exact再現・21行/1615）と class-2 S5 `00000000000000801242000000000000`（del11でD4-canon再現・59行/4656）。残り4削除（49/60/63/71）は閉行。兄弟行 `00000000220000083800000000000200`（cost 73・第2開親67行/5182）は未着手のまま残置。

## 成果1：raw sweep 15ファイルの着地とbyte検証

前回のraw一括pushが未着地だったため、ローカル15ファイル（raw batch1-10・determinism rerun・v15 crosscheck a/b/c/refuted）の内容を実ファイルから再構成してpushし直し、公開CDN経由で**15ファイル全てmd5一致**を確認した。**8 WIN7-D10 [31,54,56,62,69,81,89,113]・65 REFUTED・0 capped・総nodes 91,357,592・pilot 3402×10**。全候補 terminal [13,17]・andclose true。

## 成果2：独立sweep audit（`audit_cost73g_raw_sweep_20261115.py`）

72c版を雛形に73g用に適応（純Python stdlib・完全整数Bareiss・repo engine不使用）。全assert PASS:

- 73 legal candidatesをzeroから再列挙（claim列挙とbit-exact一致）・child safe確認。
- 10 batchのbitsをclaim engine計画と照合・全bit一度ずつ・集計再導出（91,357,592 nodes再現）。
- determinism rerun batch 5 node-exact・v15 cross-engine 8 WIN loss=true + アンカー0/100/117 loss=false（pilot 5949×4）。
- **8 WIN rootのmobilityを独立再導出**（53/62/50/58/55/53/65/54）・root hex bit-exact・D4 orbit 8個すべて互いにdistinct、さらに**公開15 manifest・25 canonical rootと重複なし**。
- 一石削除の再導出: del66=parent1 bit-exact・del11=parent2 D4-canon・残り4削除はhead-1244 ranking CSV（175開行）に不在。parent1 (2,21,1615)・parent2 (2,59,4656)。top-candidates CSV行 `...,73,"c1=0,c2=2,c4=0"` 一致。

## 成果3：WIN8盲抽出証明書の二重独立検証と公開

`cert_driver73g.ts`（72c driverのcost名行のみ適応）でrepo-verbatim extractor（blob `52bcaf50`）を盲kill table（pref=null）で実行。**fbt_drops 0・fatalなし・総strategy rows 343,092・総extraction nodes 94,100,994**:

| bit | root | rows | nodes |
|---|---|---|---|
| 31 | 00000000000000849002000080000800 | 44,015 | 13,996,000 |
| 54 | 00000000000000849042000000000800 | 56,522 | 16,761,971 |
| 56 | 00000000000000849102000000000800 | 29,162 | 6,658,440 |
| 62 | 0000000000000084d002000000000800 | 40,108 | 6,599,704 |
| 69 | 00000000000000a49002000000000800 | 45,968 | 12,432,665 |
| 81 | 00000000000200849002000000000800 | 33,205 | 6,526,388 |
| 89 | 00000000020000849002000000000800 | 62,993 | 22,800,848 |
| 113 | 00020000000000849002000000000800 | 31,119 | 8,324,978 |

二重検証は両方独立実装で全8枚PASS: **BigInt検証器**（repo blob `62b5d941`・3x3余因子展開・union missing/extra 0/0・rows sorted-unique・terminal [13,17]）と **Bareiss検証器**（`verify_cost73g_win7_bareiss_independent.py`・全loser応手展開・戦略union閉包・consumed == 全戦略行）。

公開は72cと同様の行境界2分割（全16パートで**join md5 == whole-file md5**、part md5/blob shaをmanifestに記録）。manifest `class2-lane-cost73g-win7-certificates-20261115.json`・certificates README・per-bit verify records 16件・driver/検証器scriptを同梱pushし、**16パート+20ファイルすべて公開内容をmd5で照合**（bit89 part2のみpush競合「Reference cannot be updated」1回→再送で解決）。

## 運用メモ

- 大きなパートpushはrun_typescriptの16MiB記録制限に触れるため**1パート1呼び出し**が確実。内容はfile_system connectorのchunked read（2000行単位）で連結し、push後にremote md5照合でbyte-exact性を担保する。
- raw sweep一括pushの失敗（JSON payload破損）は、bash `cat`で実ファイル内容を確認してからtemplate literalで埋め込む方式で解消。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- 8枚のWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。child orbitの閉鎖はfold後に両開class-2親の残行を減らすが、どちらのS5親も解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- **cost-73g receipts foldは次回以降**: fold前に最新mainを再取得し、head 1244（blob `42dbb92e`）を再assert。並走の70g（8証明書）・65l（2 receipts）foldが先に着地した場合は本headへのrebase必須。fold receiptsはbits [31,54,56,62,69,81,89,113]の8枚。
- 次のsweep候補: 兄弟行 `00000000220000083800000000000200`（cost 73・第2開親67行/5182）またはthird target `00000000000000809102000000000000`の残り2行（cost 69/74・並走claimの69g/74eとの重複に注意）。

詳細: [sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-sweep-audit-20261115.json)、[certificates manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-win7-certificates-20261115.json)、[claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-inflight-20261115.json)。
