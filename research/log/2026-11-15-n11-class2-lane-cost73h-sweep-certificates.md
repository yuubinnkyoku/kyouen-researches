# 2026-11-15：cost-73g兄弟行hex誤記修正 + cost-73h sweep + WIN7証明書4枚 — 第2target S5の兄弟cost-73行を閉じるreceipts（foldは次回）

開始時状況: 前セッションでcost-73g receipts fold完走（head 1249/6598/520956/4868/384679・blob `e4fb98dc`）・claim v4・fold log・K0783までpush済み。セッション中断時に検出していた兄弟行hexのprose誤記（`…220000838…` → 正しくは `…200000838…`）の修正が途中だった。

## 成果1：兄弟行hex誤記の修正push（commit `1631350a`）

claim v4の `fold.outstanding` を正しいhex `00000000200000083800000000000200` に修正し、新key `fold.erratum_sibling_hex` に誤記の全文記録を追加（claim v2以降のno_prior_sweep_noteとfold head JSONの `outstanding_not_folded.sibling_cost73_row` が誤記hexを引用・誤記hexはmanifest行自体が存在せずassert値・fold算術・証明成果物への影響なし・head JSON/scriptはblob-pinnedのためbyte-unmodified、70f baseline_mainと同じ運用）。fold log・K0783にも誤記記録を追記。修正後claim v4でfold scriptを再実行し**完全PASS**（section 9はfold recordのみ読み`outstanding`に依存しないことを確認・head 1249・3 output blob byte-identical再assert）。3ファイル（claim・log・K0783）を1コミットでpushしremote blob sha完全一致（`1c28b2a1`/`89616890`/`602300bb`）。直後のraw CDN md5差はFastlyキャッシュと判明（API側blob shaで照合解決）。

## 成果2：cost-73h claim（兄弟行のsweep確保・commit `2ede8c61`）

最新main再取得（five-row-q7並走のみで本チェーン無関係）→ repo検索23 hitsすべて列挙系で未sweep・未claimを確認 → **child `00000000200000083800000000000200`（cost 73・c1=0,c2=2,c4=0・stones [9,59,60,61,67,93]）をcost-73hとしてclaim v1（IN FLIGHT）でpush**。head 1249で両開親を再検証: del67→parent1 = 第2coverable class-2 target S5 `00000000000000801202000000200000` bit-exact（19行/1463）・del9→parent2 = class-2 S5 `00000000000000003800200008000000` D4-canon（67行/5182）・残り4削除（59/60/61/93）は閉行。`legal_candidates.py`（blob `8e97082c`）で73 legal候補。WIN7 receipt setが得られれば第2target S5の両開class-2親を同時に進める（third target残り2行は69g/74e/74g並走claimで取り合いのため兄弟行が最良の未着手行）。

## 成果3：sweep完走 — 4 WIN7-D10 [45,48,82,96]・69 REFUTED・0 capped・76,012,796 nodes

v16 runner（blob `0a4a86f6`・depth 10・cap 1e9・andclose 1・10 batch 8×9+1）で73候補を完走。**4 WIN7-D10（bits 45/48/82/96）・69 REFUTED・0 capped・総nodes 76,012,796・pilot 3402×10 PASS**。全候補 terminal [13,17]。determinism rerun（batch 5）node-exact一致・v15 cross-engine（blob `8744fc65`）4 WIN all loss=true + REFUTED anchors 3/22/120 all loss=false（pilot 5949×2）。

## 成果4：独立sweep audit全assert PASS

`audit_cost73h_raw_sweep_20261115.py`（73g版templateの73h適応・純Python stdlib・完全整数Bareiss・repo engine不使用）:

- 73 legal候補zeroから再列挙（claim列挙とbit-exact一致）・child safe確認。
- 10 batchのbits照合・全bit一度ずつ・集計再導出（76,012,796 nodes再現）。
- lift再導出: del67=parent1 bit-exact・del9=parent2 D4-canon・残り4削除はhead-1249 ranking CSV（175開行）に不在。parent1 (2,19,1463)・parent2 (2,67,5182)。top-candidates CSV行のcost 73・demand一致。
- **4 WIN rootのmobility独立再導出**（56/56/59/63）・root hex bit-exact・D4 orbit 4個すべて互いにdistinct、**公開16 manifest・33 canonical rootと重複なし**。

## 成果5：WIN4盲抽出証明書の二重独立検証と公開

`cert_driver73h.ts`（73g driverのcost名行のみ適応）でrepo-verbatim extractor（blob `52bcaf50`）を盲kill tableで実行。**fbt_drops 0・fatalなし・総strategy rows 176,451・総extraction nodes 28,144,763**:

| bit | root | rows | nodes |
|---|---|---|---|
| 45 | 00000000200000083800200000000200 | 44,989 | 11,046,694 |
| 48 | 00000000200000083801000000000200 | 34,929 | 3,638,354 |
| 82 | 00000000200400083800000000000200 | 44,836 | 4,175,255 |
| 96 | 00000001200000083800000000000200 | 51,697 | 9,284,460 |

二重検証は両方独立実装で全4枚PASS: **BigInt検証器**（repo blob `62b5d941`・union 0/0・terminal [13,17]・rows sorted-unique）と **Bareiss検証器**（`verify_cost73h_win7_bareiss_independent.py`・全loser応手展開・consumed == 全戦略行・terminal [13,15,17]内）。

公開は行境界2分割8パート（全パートで**join md5 == whole-file md5**、part md5/blob shaをmanifestに記録）。manifest `class2-lane-cost73h-win7-certificates-20261115.json`・certificates README・per-bit verify records 8件・audit script・cert driver・Bareiss検証器を同梱push（commit `495ce575` + パート8コミット）。**全36ファイルを公開CDN md5で照合一致**。さらにremoteからパートを再取得して再結合し、join md5がmanifest記載と一致することとBigInt再検証PASS（4/4）を確認（公開成果物のみによる独立再検証）。claim v2（sweep+証明書完了・fold pending）に更新。

## 運用メモ

- run_typescriptの16MiBメモリ制限はchunked readの積算でも超える: 証明書パート（~815KB）は**1パート1呼び出し**で安全にpushできる（~13 reads + 1 push で ~2MB）。
- push_filesが「Update is not a fast forward」で失敗した場合は並走pushの着地：最新mainをlist_commitsで確認し同一内容で再pushすればよい（bit82 part1で発生・再送で解決）。
- raw CDN（raw.githubusercontent.com）のFastlyキャッシュが更新前md5を返すことがある: 照合はGitHub API側のblob sha（directory listing）で行うこと。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。head 1249は本sweepでは不変（fold前）。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- 4枚のWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。child orbitの閉鎖はfold後。どちらのS5親も解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- **cost-73h receipts foldは次回**: fold前に最新mainを再取得し、その時点のcanonical headを再assert（並走の70g/65l foldが着地していたらそのheadへのrebase必須）。fold receiptsはbits [45,48,82,96]の4枚。
- K0783に73hセクション追記済み・workflowトリガー行追加済み（本コミット）。
- 並走状況: 69g/65j/74e/74g/70g/65lは他childを対象。third target残り2行は引き続き並走claim中。

詳細: [claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73h-inflight-20261115.json)、[sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73h-sweep-audit-20261115.json)、[certificates manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73h-win7-certificates-20261115.json)。
