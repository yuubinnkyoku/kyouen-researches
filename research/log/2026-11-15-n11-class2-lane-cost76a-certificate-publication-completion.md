# cost-76a WIN7証明書6件の出版完了 — 8/8 blob照合・claim closed

cost-76a child `00000000000000809102000000000001`（S5 `00000000000000809102000000000000` + 1<<0、edge cost 76、head 1188でdemand c1=0/c2=2/c4=0）のsweepで得られた6 WIN7-D10 bits（11, 29, 66, 80, 92, 96）の証明書を、抽出から独立検証・出版・遠隔照合まで完遂した。

## 抽出 — repo-verbatim extractor + 公開driver

抽出は repo-verbatim `class4_child1_cert_extractor_exact.ts`（FBS=1<<20・drop-counting fbt cache）を、自作driver [cert_driver76a.ts](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cert_driver76a.ts)（**本sessionでscripts/に公開**、git blob sha `68336cdfe7c3eba4c0479bf79a1b309a3d32c191`、commit 86622c49）でbitごと・chunkごとにnode process実行した。kill tableは**空**（pref=null・ヒントなし・verdict cache不使用・既存判定の再利用なし。全行をextractorの自己検査つき深さ有界再帰でゼロから再証明）。各bitの全loser初手（legal_candidates.pyの独立Bareiss 4x4列挙、mobility 55〜62手）を3〜4 chunkに分割し、`sort -u` でマージ（chunk間の全行重複は深部収束として正常、**board単位の移動競合は全bitで0**を `uniq -d` で確認）、header 2行を付して証明書化した。

| bit | root_hex | rows | extraction nodes | 形式 |
|---|---|---|---|---|
| 96 | 00000001000000809102000000000001 | 34,681 | 6,642,969 | 単一 |
| 92 | 00000000100000809102000000000001 | 35,456 | 7,818,115 | 単一 |
| 11 | 00000000000000809102000000000801 | 48,653 | 13,521,724 | 単一 |
| 66 | 00000000000000849102000000000001 | 52,883 | 10,787,042 | 2分割 |
| 80 | 00000000000100809102000000000001 | 49,741 | 15,010,982 | 単一 |
| 29 | 00000000000000809102000020000001 | 57,930 | 17,130,596 | 2分割 |

計279,344行・extraction nodes 70,911,428・fbt_drops全bit 0。分割閾値は1.75 MiB = 1,835,008 bytes（境界傍証: 72b bit47 1,761,391=単一 / bit21 1,845,574=分割）。

## 二重独立検証 6/6 PASS/PASS

- **BigInt検証器** `verify_win7_certificate_bigint_independent.mjs`（3x3余因子展開・engine非依存）: 6/6 PASS。sub-roots 62/54/60/61/59/55が全てrootのloser mobilityと一致、consumed union missing/extra 0/0、終局石数 [13,17]、root安全（7石・4共円なし）
- **Number Bareiss検証器** `verify_bit7_win7_cert.ts`（--root-check、--subroots全初手、--consumed-out）: 6/6 PASS。consumed union == 証明書行集合（comm diff 0）

per-move terminalRangeのばらつき（bit66 m14 [15,17]、bit96 [13,15]など）は個別subgameの観測終局深さの範囲であり、証明書レベルでは全bit [13,17]（74d/72bと同一挙動）。

## 出版 — 8/8 remote blob照合

6ファイルを(1/6)..(6/6)の1コミット1ファイル（bit66/bit29は1コミット1part）でpushし、remote 8ファイルすべてのgit blob shaをローカル計算値と照合（**8/8 byte-exact**）。分割ファイルは行境界で分割し、連結md5がwhole md5に一致することを両bitで確認済み。

**最終マニフェスト** `class2-lane-cost76a-win7-certificates-20261115.json`（15,810 bytes、git blob sha `f3be0e0edfc4ddf5da327dc545de7009926407ef`、commit 33777bea）: 6/6 WIN7 bits certified、計279,344行・extraction nodes 70,911,428・sub-roots 351・visited 593,146・terminal 97,664・edges 528,178・v15 crosscheck nodes sum 44,074,444。sweep auditの `proof_boundary.certificate_extraction` / `independent_certificate_verification` を閉じた。claim [class2-lane-cost76a-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-inflight-20261115.json) をcompletedに更新。

v15 cross-engine anchor（[crosscheck JSONL](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-v15-crosscheck-20261115.jsonl)）: 6 WIN7 bits全てloss=true（bit96 3,556,006 / bit92 4,876,955 / bit11 7,665,696 / bit66 6,198,635 / bit80 10,820,542 / bit29 10,956,610 nodes）、REFUTED anchor bit2/30/120はloss=false、pilot d6 7/7 PASS（v15 runnerは4スペースの転写差を訂正後にrepoとbyte-exact化し、bit96再実行でnodes完全一致を確認済み — auditのhonesty note参照）。

## 運用の実録

- push_files実行**後**に16 MiB sandbox memory limitでプログラム中断が2回（bit11・bit80）あったが、いずれもremote listingのblob sha照合で着地を確認してから継続。欠損・truncationなし
- bit66の初回driver起動でchild hexの誤指定（root hexを渡した）によるfatal=2を検出し、全bit共通のchild hex `00000000000000809102000000000001` + bit番号指定に修正してやり直した（出力汚染なし・summary.jsonで即検出）

## 意味と残作業

証明書出版は76a sweepの6 WIN7 rootの証明基盤を確定させるものであり、**frontier計数は不変**（76a receiptはまだchain head 1188にfoldされていない）。次のstepは6-receipt fold（head 1188で `1188/6659/525437/4929/389160` をassertする `class-frontier-cost76a-receipts-recompute-20261115.json`）であり、72b/74d/70cwarm3/unified mergeに至るrunpy鎖（39 scripts）のbyte-identical再現に必要な材料fetchを要する大規模タスクとして次回に回す。第三class-2 targetの未claim最後の子はcost-78 `00000000000000809102000000400000`。

**証明書は各7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4はいずれも引き続きUNKNOWN。**

成果物: [最終マニフェスト](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-win7-certificates-20261115.json)、[driver](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cert_driver76a.ts)、[claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-inflight-20261115.json)、[sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-sweep-audit-20261115.json)、[v15 crosscheck](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-v15-crosscheck-20261115.jsonl)、[K0783](../knowledge/items/K0783-n11-ms5-worklist-derivation-verified-and-s7-reuse-partition.md)。証明書6本体は同output/`class2-lane-cost76a-certificates/`。
