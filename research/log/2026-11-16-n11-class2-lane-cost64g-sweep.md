# 2026-11-16：cost-64g sweep完走 NOT-STERILE — 最安open行`00000000000100003800000008080000`（head 1438・59 open bits）を完走：**WIN7-D10 1件（bit 89）+ REFUTED-D10 63件（58 swept + 5 transfers）・0 capped** — 証明書1枚（BigInt+Bareiss二重検証PASS）・foldは次セッションへ繰越・11×11はUNKNOWN

開始時main: `592463e9`（自レーンのhead-1438 presweep census v3出版済み）。census v3が推奨した最安open行（shared class-2 protocol parentのcost-64行・59 open bits・5 REFUTED-D10 transfers）を、IN FLIGHT claim v1（`14bb1385`）で予約したうえでsweep完走させた。ラベル`cost64g`はmain上の未使用を検索確認（`cost64g`/対象行hexともにcommit message 0件）。並走laneの対象外（REMO/K0874・class4・76c/69a in-flightとは無競合）。

## sweepの全容

1. **事前claim（IN FLIGHT v1）**: 59 open bitsを7×8+3=59の8 batch構成で予約・5 transfers（bits 5/29/104/111/119・census bit tableのroot canonをverbatim記録・再sweepしない慣例）。
2. **v16 sweep完走**（`class4_child1_runner_v16.ts` repo-verbatim・depth 10・cap 10M/bit・pilot_d6 3402 nodes×8 batch全PASS）: **WIN7-D10 1件 = bit 89**（690,457 nodes・batch 5）・REFUTED-D10 58 swept・capped 0・**総nodes 33,505,865（~501k nodes/s）**・terminal range全bit [13,17]・andclose全適用。最重bit 43（3,672,017 nodes）。
3. **determinism rerun 2 batch**: batch 3（最重bit 43含む）とbatch 5（**WIN bit 89含む**）をscratchから再実行し、両方とも9/9行node-exact（msのみ相違）。
4. **v15 cross-engine crosscheck**: pilot 5949 nodes・anchors [1, 43, **89**, 118]全てv16判定と双方向一致。**WIN bit 89はv15でもloss=true（1,760,287 nodes）**。
5. **独立集計audit**（`audit_cost64g_raw_sweep_20261116.py`・stdlibのみ・Bareiss 4x4）：候補64をscratch列挙→claim listとbit-exact・batch bit lists恒等・**census v3のopen 59/transferred 5/family 30行2081と全照合**・transfers 5件のroot canon（D4）をd4_canon(child|1<<bit)で再導出し一致・**64候補のD4 orbitは全てdistinct（衝突0）**・childの6通りのone-stone deletion liftは両open親（shared `00000000000000003800000008002000` 30行/2081・第2親`00000000000000801202010000000000` 50行/3631）を含む。audit JSON blob `fc45acbd`。
6. **証明書1枚**（`assemble_cost64g_certificates_20261116.py`・64f版と同一protocol）: root = child|1<<89 = `00000000020100003800000008080000`（stones [19,27,59,60,61,80,89]）。盲抽出（`cert_driver65j.ts` + repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`・empty kill table）30,373 rows / 1,278,418 extraction nodes / fbt_drops 0 / fatal null。**BigInt union 0/0 + Bareiss 45/45 sub-roots全PASS**（`verify_bit7_win7_cert.ts` + `verify_win7_certificate_bigint_independent.mjs`双方exit 0・terminal range [13,17]・root mobility 45 == legal_candidates.py）。winner 44,932 / loser 14,916 / terminals 9,172。**whole cert 1,096,891 bytes（分割閾値1.2MB未満のため単一ファイル出版）**・manifest `class2-lane-cost64g-win1-certificates-20261116.json` blob `e30be681`。

## 解釈上の注意

**solved 1438はmanifest被覆の簿記で本sweepでは不変。WIN7-D10証明書はroot `00000000020100003800000008080000`という個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10 63件はLOSS証明ではなく該当rootの深さ10内的反証のみ。NOT-STERILEは行の勝敗を意味しない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両open親はいずれもUNKNOWN。**

## 成果物

- IN FLIGHT claim v1: [class2-lane-cost64g-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-inflight-20261116.json)（commit `14bb1385`・blob `895b0cfc`）
- 完了claim v2（NOT-STERILE）: 同ファイル（blob `c899b52d`・v1の全欄保存・results追記）
- raw batches 1..8: [class2-lane-cost64g-raw-batch1-20261116.jsonl](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-raw-batch1-20261116.jsonl) … batch8（blob pins claim v2 results欄に全記載）
- determinism reruns: batch3（blob `f6266ff4`）・batch5（blob `56998e7f`）
- v15 crosscheck: [class2-lane-cost64g-v15-crosscheck-20261116.jsonl](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-v15-crosscheck-20261116.jsonl)（blob `8f65eb1e`）
- sweep audit: [class2-lane-cost64g-sweep-audit-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-sweep-audit-20261116.json)（blob `fc45acbd`）+ [audit script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost64g_raw_sweep_20261116.py)
- 証明書: [bit89-root-00000000020100003800000008080000.cert](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-certificates/bit89-root-00000000020100003800000008080000.cert)（whole 1,096,891 B・blob `1d2cc167`）+ bigint-verify + bareiss-verify + 抽出summary
- manifest: [class2-lane-cost64g-win1-certificates-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-win1-certificates-20261116.json)（blob `e30be681`）+ [assembler](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/assemble_cost64g_certificates_20261116.py)

## 次の候補

- **bit 89 receiptをhead 1438 chainにfold**（64f fold scriptと同一protocol・conflict censusはauditのD4衝突0で前倒し確認済み・新head 1439予想）。
- fold後のpresweep census v4で次の最安open行を決定（見込み: `00000000000000801202010000800000` cost 65・59 open・6 transfers・第2親とshared親の双方に効く行）。
