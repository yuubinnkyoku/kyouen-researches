# 2026-11-15：cost-73h receipts fold — canonical head 1254 → 1257（fence_noteのrebase条項発動・D4-canon wording erratum修正込み）

開始時main: HEAD `d0145e88`（自分の70g fold着地コミット）。push直前の最新mainは `f6d2ba24`（取得後も並走が進み、pushは1回fast-forward競合を挟んで着地） — いずれも本実験dirには無影響（canonical headは常に1254のまま・claimはv3のまま・73h foldは未着地であることを都度raw CDNで確認）。baseline: cost-70g chain head **1254/6593/520600/4863/384323**（`class-frontier-cost70g-receipts-recompute-20261115.json`・blob `73890fe34580ec2f869a97a00b3e6400eda30c0a`）。直前までのセッションで73hのsweep（4 WIN7-D10 [45,48,82,96]）・証明書4件（176,451 rows）・claim v3（fold IN FLIGHT fence・baseline 1249）まで完了済み。本セッションはfold実行・claim v4まで実施した。

## このfoldの特殊事情：fence_noteのrebase条項（warm hygieneではない・genuinely-remaining child）

73hのfence（claim v3 `fold_in_flight.baseline_head` = **1249/6598/520956/4868/384679**）はcost-70g foldより先にpushされていたが、fence_note自身が「並走の70g foldが先に着地したら、本foldはその時点のcanonical headにrebaseして再導出せよ」と規定していた。70g foldが着地した（head 1249→1254・commit `bc4ff54d`）ため、**本foldはhead 1254にrebaseして実施した**。rebaseが結果に与える影響はbaseline数値のみ（fold script内でassert）:

- **両開lift親は70g foldの影響を受けない**: 70g receiptsが閉じた5行はparent2側 `00000000000000801202010000000000`（73hとは別のparent）のもので、73hのparent1 `00000000000000801202000000200000`（19行/1463）とparent2 `00000000000000003800200008000000`（67行/5182）はhead 1249のaudit数値のまま不変、どちらもchild行 `00000000200000083800000000000200`（edge cost 73）を保持。
- **childはbaseline 1254でgenuinely remaining**: manifest内かつ未解決（70g foldとは対照的。70gはwarm-hygiene foldでchildが既にcross-cover済みだった）。

## fold scriptと統制

`recompute_frontier_cost73h_receipts_20261115.py`（73g/70g版を雛形・commit `a422f2d8`・blob `ce4f7d9a7ee9cc2777796a2457788e8780ac7fd8`）を書き、**3回連続実行すべてbyte-identical**を確認。統制は70g版の方式を踏襲:

- **baseline再構成**: 70g fold scriptをrunpy鎖（1227→1233→1235→1239→1244→1249→1254の全fold鎖込み）で再現し、1254 head JSON（blob `73890fe3`）・両CSV（`7397c805`・`2da64221`）ともblob-identical再生成。
- **入力検証**: 39 published cost-73h input files（sweep audit・certificates manifest・10 raw batches・determinism rerun・v15 crosschecks 2件・per-bit verify records 8件・certificates README・証明書part 8件・scripts 7件）をgit blob shaでbyte-exact検証。claimは内容検証。
- **child/両親の再検証（rebase control）**: child genuinely remaining・parent1 (19, 1463)・parent2 (67, 5182)・child行が両親のrowにcost 73で存在・openな1石削除は2親のみ・demand c1=0,c2=2,c4=0再導出。
- **sweep再導出**: 10 raw batchesから73候補一度ずつ（claim列挙とaudit batch planの両方に一致）・4 WIN7-D10 [45,48,82,96]（nodes {45: 2,947,015, 48: 880,086, 82: 1,050,117, 96: 2,098,886}）・69 REFUTED-D10・0 capped・総nodes 76,012,796・pilot 3402×10・batch5 determinism rerun node-exact・v15交差 4/4 WIN node-matched + REFUTEDアンカー 3/22/120（raw verdict一致）・pilot 5949×2・全73候補 terminal [13,17]。
- **証明書検証**: 4証明書のpart bytes検証（8 partのblob sha・md5・bytes・join md5 == whole md5・whole git blob sha == manifest・rows sorted-unique・root == child|1<<bit・sub-roots == loser mobility 56/56/59/63（audit一致）・BigInt+Bareiss verify blocks・per-bit verify records 8件再読込・union 0/0・terminal [13,17]・fbt_drops 0）・manifest totals再総和（**176,451 rows / 6,384,415 bytes / 28,144,763 extraction nodes**）。
- **root-orbit簿記**: 4新root vs **528 fold済みroot**（520 through 73g + 8 70g）raw-hex disjoint・4新D4 orbitはfold済みrootのD4 canonと**重複なし**（公開33-root scanより強い統制）・audit `d4_canonical_hex`再導出一致。

## fold結果

公開順 [45, 48, 82, 96] でfoldし、**総marginal 19・in-manifest 3**（zero-mim [82, 96]・zero-marginalなし）:

| bit | root hex | covers | marginal | in-manifest | marginal manifest hexes |
|---|---|---|---|---|---|
| 45 | `00000000200000083800200000000200` | 7 | 6 | 2 | `00000000000000083800200008000000`, `00000000200000083800000000000200` |
| 48 | `00000000200000083801000000000200` | 7 | 5 | 1 | `00000000000000403800200008000000` |
| 82 | `00000000200400083800000000000200` | 7 | 4 | 0 | — |
| 96 | `00000001200000083800000000000200` | 7 | 4 | 0 | — |

- **child orbit `00000000200000083800000000000200` はbit45（公開順最初）で閉鎖**。set等式 `s_after == s_1254 UNION covers(4 roots)` 統制PASS。
- **parent1（第2 coverable class-2 target S5 `00000000000000801202000000200000`）はchild行のみ喪失し 19行/1463 → 18行/1390**。
- **parent2（`00000000000000003800200008000000`）はchild + bit45/bit48 marginal由来の2行を喪失し 67行/5182 → 64行/4962**。
- **fold後 head: solved 1257 / unique 6590 / cost 520,380 / open 4,860 / open_cost 384,103**。両S5親ともまだ多数のrowを残し未解決。

## claim v4のerratum（prose修正）

claim v3の`demand_verification`は「stone-67 deletionがparent1を**bit-exact**に再現する」と記載していたが、これはwording erratum: 実際にはどちらのliftもraw bit-exactではなく**両方ともD4-canon**（del67 raw `00000000200000003800000000000200` → canon → parent1、del9 → canon → parent2）。fold scriptは当初raw bit-exact解釈でassertを書いて失敗し、これをきっかけに誤りを発見・訂正した（70g foldでper-bit hex対応を誤った教訓の再発防止が効いた）。親の同一性・demand・73候補列挙・sweep/証明書の結果には影響なし。claim v4 `claim_v4_erratum`に記録し、fold scriptは訂正後のD4-canon対応をassertする。

## push

5ファイル（fold script・head JSON `71f79b4b`・ranking CSV `ee4cc2ff`・top-candidates CSV `122803ea`・claim v4 `d19b630e`）を単一コミット `a422f2d8` でpush、**remote raw CDNで5ファイルすべてのgit blob shaを照合一致**。push直前にfast-forward競合1回（並走がmainを進めた）→ 最新main再取得でhead 1254・claim v3・fold未着地を確認して再pushで着地。

REFUTED-D10はLOSS証明ではなく、4証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。solved 1257はmanifest被覆の簿記であり盤全体の勝敗ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続きUNKNOWN**。次のfold baselineはhead **1257**。cost-65l（bits 21/48・fence baseline 1227でstale）のfoldは**本head 1257へのrebaseが必須**。69g/65j/74e/74g並走中。

詳細: [head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost73h-receipts-recompute-20261115.json)、[claim v4](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73h-inflight-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost73h-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost73h-receipts-20261115.csv)。
