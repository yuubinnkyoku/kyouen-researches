# 2026-11-16：cost-65n sweep完走 NOT-STERILE — 最安open行`00000000000000801202010000800000`（head 1441・59 open bits）を完走：**WIN7-D10 2件（bits 90, 117）+ REFUTED-D10 63件（57 swept + 6 transfers）・0 capped** — 証明書2枚（BigInt+Bareiss二重検証PASS・bit 90はpart1of2/part2of2分割出版）・claim v2・独立audit・並走laneによる独立再現2件・foldは次セッションへ繰越・11×11はUNKNOWN

開始時main: `373bcdd9`（自レーンの証明書manifest・assembler・determinism/v15記録の出版コミット）。head-1441 presweep censusが推奨した最安open行（shared class-2 protocol parentのcost-65行・59 open bits・6 REFUTED-D10 transfers）を、IN FLIGHT claim v1（`7dcd9767`・blob `c16ba5c9`）で予約済み。並走laneがclaim v1の構造検証21/21 PASS（`9888e42c`）でsweep所有権を自レーンに確認済み。ラベル`cost65n`はcommit message検索で未使用を確認済み。

## sweepの全容

1. **v16 sweep完走**（`class4_child1_runner_v16.ts` repo-verbatim・depth 10・cap 10M/bit・pilot_d6 3402 nodes×8 batch全PASS）: 59 open bitsを7×8+3=59の8 batch構成で完走。**WIN7-D10 2件 = bits 90（1,562,274 nodes・batch 5）と117（388,910 nodes・batch 7）**・REFUTED-D10 57 swept + 6 pre-sweep transfers = 63・capped 0・**総nodes 92,530,349（187,251 ms・~494k nodes/s）**・terminal range全bit [13,17]・andclose全適用。最重bit 26（5,654,046 nodes）・bit 9（5,075,917）・bit 79（4,072,659）。raw batches 1-4は`60c97b93`、5-8は`e728c47e`で出版（8 blob pinsはclaim v2 results欄に全記載）。
2. **determinism rerun 2 batch**: batch 5（**WIN bit 90含む**・blob `005417e4`）とbatch 7（**WIN bit 117含む**・blob `cb450e27`）をscratchから再実行し、両方とも9/9行node-exact（msのみ相違）。
3. **v15 cross-engine crosscheck**: pilot 5949 nodes・anchors [9, **90**, 94, **117**]全てv16判定と双方向一致。**WIN bits 90（3,204,116 nodes）・117（865,824 nodes）はv15でもloss=true**（blob `158012b7`）。
4. **証明書2枚**（`assemble_cost65n_certificates_20261116.py`・64g版と同一protocol・commit `373bcdd9`）:
   - **bit 90**: root = child|1<<90 = `00000000040000801202010000800000`（stones [23,40,49,57,60,71,90]・D4 canon `00000000000100003800000048002000`）。盲抽出35,627 rows / 2,770,239 extraction nodes / fbt_drops 0 / fatal null。**BigInt union 0/0 + Bareiss 51/51 sub-roots全PASS**（terminal range [13,17]・root mobility 51 == legal_candidates.py）。**whole cert 1,285,412 bytes > 分割閾値1.2MB → part1of2（642,720 B・blob `a5d67f1d`）+ part2of2（642,692 B・blob `0b12b216`）+ byte-exact join receipt（whole sha256 `801bfdac…`・whole git blob `c2460e59…`）**で出版（commit `15c9b66b`）。
   - **bit 117**: root = child|1<<117 = `00200000000000801202010000800000`（D4 canon `00000000001020003800000008080000`）。盲抽出20,047 rows / 769,616 extraction nodes。**BigInt union 0/0 + Bareiss 49/49全PASS**。**whole cert 721,989 bytes（単一ファイル・blob `ac0ea37d`）**で出版（commit `57ab8ed5`）。
   - manifest `class2-lane-cost65n-win2-certificates-20261116.json`（blob `e2e4e3f5`）: totals 55,674 rows / 3,539,855 extraction nodes / 100 sub-roots / cert bytes 2,007,401。全10 certファイルCDN照合PASS。
5. **独立集計audit**（`audit_cost65n_raw_sweep_20261116.py`・stdlibのみ・Bareiss 4x4・64g版を65n用に機械変換）: 候補65をscratch列挙→claim listとbit-exact・batch bit lists恒等・**census v4（head 1441）のopen 59/transferred 6/family 29行2017と全照合**・transfers 6件のroot canon（D4）をd4_canon(child|1<<bit)で再導出し一致・**65候補のD4 orbitは全てdistinct（衝突0）・両WIN canon含む**・claim v2のresults欄（nodes 92,530,349・ms 187,251・heaviest top3）と全数値照合・証明書manifestの全検証フィールド再確認・childの6通りのone-stone deletion liftは両open親を含む（shared `00000000000000003800000008002000` 29行/2017・第2親`00000000000000801202010000000000` 48行/3498・第2親はcensusの2 protocol parent外のためmanifestのdirect_s5_parentsにpin）。audit JSON blob `6b7d3579`。
6. **完了claim v2**（NOT-STERILE）: v1の全欄を保存しschema/status/supersedes/resultsのみ更新（blob `257e7093`）。results欄に2 WINのcrosscheck三重記録（v16 sweep・v15・証明書）・raw 8 batch blob pins・determinism reruns・v15 anchors・k0863（NOT sterileなのでfoldをblockしない）・fold deferredを記載。
7. **並走laneによる独立再現2件**（自レーンのsweep・証明書の外部検証）: `0c237017`がrepo-verbatim runner v16で**59/59 bit独立再実行node-exact（両WIN bit含む）+ 独立raw batches 1-8**、`e01093dc`が**盲抽出4-chunk 4-parallel（3,151,841 nodes）で両証明書byte-identical再現（md5一致）+ BigInt/Bareiss再検証PASS + manifest totals全一致**。この時点でcost-65n sweepは3方向（自レーン・determinism rerun・並走lane独立再実行）で一致確認済み。

## 解釈上の注意

**solved 1441はmanifest被覆の簿記で本sweepでは不変（fold前）。WIN7-D10証明書は各7石root（`00000000040000801202010000800000`・`00200000000000801202010000800000`）単体のfirst-player win（depth 10以内）のみを証明。REFUTED-D10 63件はLOSS証明ではなく該当rootの深さ10内的反証のみ。NOT-STERILEは行の勝敗を意味しない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両open親はいずれもUNKNOWN。**

## 成果物

- 完了claim v2（NOT-STERILE）: [class2-lane-cost65n-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-inflight-20261116.json)（blob `257e7093`・v1の全欄保存・results追記）
- raw batches 1..8: [class2-lane-cost65n-raw-batch1-20261116.jsonl](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-raw-batch1-20261116.jsonl) … batch8（blob pins claim v2 results欄に全記載）
- determinism reruns: batch5（blob `005417e4`）・batch7（blob `cb450e27`）
- v15 crosscheck: [class2-lane-cost65n-v15-crosscheck-20261116.jsonl](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-v15-crosscheck-20261116.jsonl)（blob `158012b7`）
- sweep audit: [class2-lane-cost65n-sweep-audit-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-sweep-audit-20261116.json)（blob `6b7d3579`）+ [audit script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65n_raw_sweep_20261116.py)
- 証明書: [bit90 part1of2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-certificates/bit90-root-00000000040000801202010000800000.cert.part1of2) + part2of2 + join receipt、[bit117 whole](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-certificates/bit117-root-00200000000000801202010000800000.cert)（blob `ac0ea37d`）
- manifest: [class2-lane-cost65n-win2-certificates-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-win2-certificates-20261116.json)（blob `e2e4e3f5`）+ [assembler](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/assemble_cost65n_certificates_20261116.py)

## 次の候補

- **bits 90/117の2 receiptをhead 1441 chainにfold**（64g fold scriptと同一protocol・conflict censusはauditのD4衝突0で前倒し確認済み・並走laneがfold projection pre-registration `0c237017`（projected head 1441→1444/174/6404/506746/4677/370660・mim 1+2・3 affected parents）とgeneric fold-projection tool `a7ac1757`を準備済みのため、fold結果は投影と照合可能）。
- fold後のpresweep censusで次の最安open行を決定。
