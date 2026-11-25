# 2026-11-15：cost-70f sweep・WIN7証明書4件・receipt fold — head 1235→1239

開始時main: `d37aab5d1`（cost-70e fold後のhead 1233）。作業中にcost-71c fold（1233→1235）が着地したため、本foldは**head 1235にrebase**した。AGENTS.md、`research/knowledge/README.md`、K0783、直近のn11 log・experimentを確認した。規約どおりmainを直接更新し、branch / PRは作らない。

## 対象

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-70 child `00000000000000801202000002200000`（stones [21,25,49,57,60,71]・edge cost 70・需要 c1=0,c2=2,c4=0）。head-1235でS5は26行/1976、第2開親 `00000000000000003800000808000000` は57行/4272。両開親ともclass 2。

## sweep（v16 d10・cap 1e9・andclose 1・9バッチ・pilot 3402×9全PASS）

**70/70候補・WIN7-D10 4件（bits 9,64,72,84）・66 REFUTED-D10・0 capped・総nodes 81,480,831**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで4 WIN loss=true（nodes 4,321,887/2,103,622/2,805,890/6,901,695・sum 16,133,094）・REFUTEDアンカーbits 1/32/116 loss=false（1,809,561/4,105,852/2,797,333）・pilot 5949。

独立監査 `audit_cost70f_raw_sweep_20261115.py`（stdlibのみ・Bareiss再実装・repo engine不使用）が9 raw batchから全件再導出: 候補70==claim列挙 bit-exact・各bit 1回・pilot 3402×9・WIN/REFUTED集計・root == child|1<<bit・4 distinct D4 orbits・公開win7 manifest 64ファイル179 canonical rootsと重複0・一石削除D4正準化6件（del 25 = 第二target S5 bit-exact、del 21 = 第2開親、他4削除は閉行）・head-1233 ranking/top-candidates CSV照合。監査JSON `class2-lane-cost70f-sweep-audit-20261115.json`。

## 証明書4件（blind抽出・二重独立検証PASS）

`cert_driver78a.ts`（repo-verbatim v16抽出器・空kill table）で全loser初手をblind抽出:

| bit | root | mobility | rows | extraction nodes |
|---|---|---:|---:|---:|
| 9 | `00000000000000801202000002200200` | 57 | 48,932 | 6,242,381 |
| 64 | `00000000000000811202000002200000` | 48 | 27,831 | 3,531,058 |
| 72 | `00000000000001801202000002200000` | 55 | 32,585 | 4,767,458 |
| 84 | `00000000001000801202000002200000` | 54 | 45,807 | 12,411,367 |

全move `ok:true`・`capped:false`・`fbt_drops:0`・terminal [13,17]。4件とも1.75 MiB未満の単一ファイル。**BigInt 3x3余因子**と**Number Bareiss 4x4**の二独立検証器で4/4 PASS（sub-roots 57/48/55/54・union missing/extra 0/0・consumed union == 証明書行集合 0/0）。manifest `class2-lane-cost70f-win7-certificates-20261115.json`: **155,155行・5,601,978 bytes・26,952,264 extraction nodes・214 sub-roots・25 distinct parent-lift orbits**、child orbitは全証明書に含まれる。

## receipt fold（head 1235 → 1239）

`recompute_frontier_cost70f_receipts_20261115.py` はcost-71c fold script（pure-geometry recompute）をrunpyで再実行してhead 1235/6612/521988/4882/385711をbyte-identicalに再現し、cost-70fのclaim・sweep audit・raw 9 batch・determinism rerun・v15・証明書manifestを照合した後、公開順 [9,64,72,84] で4 receiptをfoldする。

- 新canonical head: **`1239/6608/521701/4878/385424`**（solved 1235→1239、in-manifest marginal 4、raw marginal 20、zero-mim bits 64/72）。
- child `00000000000000801202000002200000` は**bit9**で閉鎖。
- 第2 target S5: **26行/1976 → 24行/1836**（child + `00000000000100809002000000000800` を喪失）。
- 第2開親 `00000000000000003800000808000000`: **57行/4272 → 54行/4055**（child + 2親orbit喪失）。
- set等式 `s_after == s_1235 ∪ covers(4 roots)`、root disjointness（499 folded rootsとraw/D4両方で交差0）、sweep audit再導出、manifest totals再合計をassert。
- 出力: head JSON（blob `4d0f130e975b6a7bec4759387bd6d54dfe2b6a18`・9,643 B）、ranking CSV（`65a0a19b5d794ceccdc590972b1a7006b5db7c7b`・7,580 B）、top-candidates CSV（`415b50d3f34421659f36e73cea854ab89ee837f4`・5,265 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 実行環境上の注意（再現性）

- Windows + `core.autocrlf=true` のため、fold scriptは `Path.write_text` をLF固定にmonkey-patchし、証明書・manifest・公開chain入力をCRLF→LF正規化してからhashする。作業前にscripts/output配下のtext fileをLFへ正規化し、`git add --renormalize` でindex statのみ更新した（内容差分なし）。
- cost-70eのwhole証明書（5件）は公開partからローカルに連結して用意した（未追跡・公開物はpartのまま）。cost-70e/71cのclaimはv3 retire済みのため、fold chainのscriptをv2/v3両対応に保守した（70e: claim blob v3・schema v2/v3・win7_certificates.fold PENDING/COMPLETED、71c: claim blob v3・schema v2/v3・fold pending/completed）。これはchainの再実行可能性を回復する保守で、公開claimの数値・内容は変更しない。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- child orbitの閉鎖は両S5親の残り行からchildを除くが、どちらのS5も未解決のまま。第2 targetは残り24行/1836。
- 証明書木そのものの再走査は本foldの範囲外。manifest記載の二重独立検証に依拠し、foldはbytes・root同定・sub-roots・終端範囲・親orbit・D4正準性を再検証した。

## 並走・次の一手

- cost-72c（第二targetのcost-72 child・9 WIN7-D10 bits・raw着地済み・fold待ち）は本foldの新head 1239へのrebaseが必須。
- cost-70g（8 WIN7証明書・fold待ち）・cost-65l（fold in flight）・cost-69g/74eは本foldに含めない。
- 第2 target S5の残り24行のうち、次に安い未sweep行の選定が次の一手。

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class1・class2・class4はすべて **UNKNOWN**。今回のfoldは勝敗判定を変更しない。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost70f_receipts_20261115.py
```

cost-71cのpure-geometry baselineを再実行し、head 1235のbyte-identical再現から全制約を再検証した上でfoldする。実行時間は約1〜2分。
