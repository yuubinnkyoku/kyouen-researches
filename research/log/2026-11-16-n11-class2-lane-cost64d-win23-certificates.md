# 2026-11-16：cost-64d WIN 23 bits全証明書抽出・出版完結 — 861,439行・BigInt+Bareiss二重検証・foldは次回・11×11等はUNKNOWN

開始時main: `f38be6d6`（本レーンのcost-64d sweep出版: 23 WIN7-D10 / 41 REFUTED / 0 capped・独立監査PASS・claim v2）。本セッションは**23 WIN rootsすべての盲抽出証明書を組み立て・二重検証・出版**し、cost-64dの証明基盤を完結させた。

## 実施内容

### 1. 盲抽出（`scripts/cert_driver65j.ts`（出版済み汎用driver）・repo-verbatim v16 engine・空kill table）

- root=child|1<<bit（child `00000000000000403800000008002000`）。driver moves == legal_candidates(root) mobility（assemble scriptがassert・23/23 PASS）。
- **23枚すべてfatal 0・fbt_drops 0・perMove capped 0**。合計抽出時間約2.5分。

| bit | rows | nodes | sub-roots | bit | rows | nodes | sub-roots |
|-----|-----|-----|-----|-----|-----|-----|-----|
| 0 | 42,975 | 4,498,457 | 54 | 79 | 24,227 | 743,990 | 47 |
| 1 | 32,089 | 1,420,348 | 48 | 86 | 56,607 | 5,156,381 | 58 |
| 2 | 57,543 | 7,847,223 | 59 | 92 | 37,920 | 2,049,472 | 52 |
| 11 | 36,442 | 2,150,116 | 53 | 95 | 28,352 | 1,672,223 | 48 |
| 16 | 40,116 | 3,797,743 | 52 | 98 | 35,070 | 2,055,858 | 51 |
| 30 | 22,054 | 669,543 | 45 | 106 | 29,469 | 2,617,647 | 50 |
| 32 | 50,624 | 5,898,585 | 55 | 107 | 29,043 | 1,826,624 | 47 |
| 43 | 39,135 | 2,280,936 | 53 | 109 | 22,855 | 905,323 | 48 |
| 53 | 43,010 | 3,254,829 | 57 | 111 | 45,982 | 4,165,675 | 54 |
| 66 | 46,953 | 6,372,576 | 56 | 113 | 48,883 | 3,811,908 | 59 |
| 69 | 26,893 | 1,048,245 | 47 | 120 | 47,694 | 5,015,192 | 56 |
| 75 | 17,503 | 510,576 | 44 | | | | |

### 2. 組立・二重検証（`scripts/assemble_cost64d_certificates_20261116.py`・65f版の23 bits変種）

- **全23枚BigInt union missing 0 / extra 0（sub-roots 1,193全PASS・terminals [13,17]）+ Bareiss全PASS**（`verify_bit7_win7_cert.ts --root-check`・stones 7）の二重検証。
- whole certは795,456〜2,084,371 bytes。**14枚が1,200,000-byte publication split閾値超過 → part1of2+part2of2+join receipt、9枚（bits 1/30/69/75/79/95/106/107/109）は閾値下→whole certのまま出版**。cat再構成のbyte-exact性はreceiptが保証。
- **assemble script再実行で全出力byte-identical確認済み**（157ファイル・複数回）。
- 23 rootのD4正準形はすべてdistinct（manifestがd4_canonical_hexを記録）。

### 3. manifest

`output/class2-lane-cost64d-win23-certificates-20261116.json`（schema `n11-class2-lane-cost64d-win23-certificates-20261116-v1`・blob `244e4b61`・42,974 bytes）。totals: **23 certs・861,439 rows・69,769,470 extraction nodes・1,193 sub-roots・winner 1,220,504・loser 362,105・terminals 310,638・31,086,866 bytes**。target.noteは「sweep監査（`f38be6d6`）のfold-prep投影: head 1419で16行閉鎖 → 投影head 1435・共有class-2親 `00000000000000003800000008002000` 42→31行・target S5 `00000000000000403800000008000000` 24→18行。fold自体はchain再現セッションに繰延・canonical head 1419不変。41 REFUTED-D10候補に証明書なし（REFUTEDはLOSS証明ではない）」を明記。

### 4. 出版（37+1 commits・各push後の照合は最終HEADで一括実施）

- whole 9枚: 各commit = whole cert + summary + bigint/bareiss verify。
- split 14枚: commit A = part1of2 + summary + verify×2 + receipt、commit B = part2of2。
- 最終commit: manifest + assemble script + log + claim v3。

## 意味

- **cost-64d sweepの23 WIN7-D10 receipts全枚に独立検証可能な証明書が対応**。証明書は「個別7石root（相手初手すべてに対するfirst-player win・depth 10以内）」のみを証明する。foldは未適用で**canonical head 1419/174/6429/508474/4702/372388 不変**（投影head 1435はmanifest被覆の簿記）。
- 次回レジューム: (1) chain再現によるfold実行（runpy chain reproduction → `recompute_frontier_cost64d_receipts_20261116.py` 新規作成 → head 1419へのfold → root disjointness vs folded roots → head 1435確定）、(2) fold後のclaim v6化（65j/65f precedent）。

## UNKNOWN guard

**solved 1419はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4・両開親はいずれもUNKNOWNのまま**。

## 成果物

- manifest: [class2-lane-cost64d-win23-certificates-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d-win23-certificates-20261116.json)（blob `244e4b61`）
- certificates: 同output/ `class2-lane-cost64d-certificates/`（whole 9枚 `bitN-root-….cert`・split 14枚 `….cert.part1of2`+`part2of2`+`….cert-receipt.json`・各 `….bigint-verify.json`/`…-bareiss-verify.json`/`….cert.part1of1.summary.json`）
- assemble: [assemble_cost64d_certificates_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/assemble_cost64d_certificates_20261116.py)
- source claim: [class2-lane-cost64d-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d-inflight-20261116.json)（v3）
