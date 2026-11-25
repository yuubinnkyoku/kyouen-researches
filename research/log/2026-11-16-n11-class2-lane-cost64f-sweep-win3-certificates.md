# 2026-11-16：cost-64f sweep完走 **NOT-STERILE** — WIN7-D10 3件（bits 39/72/107）発見・証明書3枚独立検証済み出版 — head 1435不変（foldは次回chain再現session）・11×11はUNKNOWN

開始時main: `f76c9fa1`（本レーンのcensus v2+claim v1着地直後・並走の新着なし）。claim v1（child `0000000000000080120a000000800000`・59 open bits・5 REFUTED転送済み [21,35,55,64,109]）のとおりv16 engineで全59候補をsweepし、**WIN7-D10 3件**を得て証明書まで独立検証・出版した。

## sweepの全容（v16 engine・8 batch・全59 open bits）

1. **生の結果**: **WIN7-D10 bits [39, 72, 107]**・REFUTED-D10 56・capped 0・総nodes **54,905,391**（pilots 3402×8別・約495k nodes/sec・全候補andclose・terminal石数範囲 [13,17]）。batch構成: b1 [0,1,4,6,8,9,10,11] / b2 [14,18,22,26,31,32,33,39] / b3 [40,42,43,52,53,54,56,58] / b4 [61,66,67,72,75,76,77,79] / b5 [85,86,87,88,90,94,95,96] / b6 [97,98,99,102,103,105,106,107] / b7 [108,110,111,112,113,114,116,117] / b8 [118,119,120]（8×7+3=59、claim v1のbatch計画どおり）。最重候補 bit40 (2,994,208 nodes)・bit72 (2,913,001)・bit106 (2,655,747)。
2. **determinism rerun**: 最重batch（b2・9,028,952 nodes・WIN bit 39含む）を再実行し**node-exact**（bit/loss/nodes/capped/terminalStoneRange全一致・msのみ相違）。
3. **v15 crosscheck**: v15 engine（pilot_d6 5949）でanchors [0, 32, 39, 118] を実行し、**4/4 verdict両方向一致 — WIN bit 39は両engineでloss=true**。node数は実装差で当然相違。
4. **行の帰結**: 59 swept + 5 transferred = **64/64候補確定・NOT-STERILE**。K0863（STERILE行のdepth-10閉鎖不能定理）は**不適用** — 行内に3つのreceipt rootが存在し、foldで閉鎖可能。**head 1435は今回不変**（foldはprotocolどおりchain再現sessionで実施）。

## 証明書3枚（全て独立検証済み・claim v2に全pin）

- **抽出**: repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`・公開済みgeneric blind driver `cert_driver65j.ts`（kill table空）・1 chunk/bit・fbt_drops 0・fatal null。
- **bit39** root `0000000000000080120a008000800000`: 44,078 rows / 2,681,848 nodes / 50 sub-roots → split part1of2+part2of2（receipt同梱）。
- **bit72** root `0000000000000180120a000000800000`: 44,343 rows / 5,037,452 nodes / 51 sub-roots → split part1of2+part2of2。
- **bit107** root `0000080000000080120a000000800000`: 27,946 rows / 1,990,119 nodes / 41 sub-roots → whole cert（1,007,877 bytes）。
- **検証**: 全3枚で BigInt独立検証（union_missing 0 / union_extra 0・subroots 50/50, 51/51, 41/41 PASS・root mobility == `legal_candidates.py`）と exact-integer Bareiss検証（`verify_bit7_win7_cert.ts --root-check --subroots`・両verifierは失敗時非ゼロexit）が**全PASS**。totals: 116,367 rows / 9,709,419 extraction nodes / 142 sub-roots / terminal [13,17]。
- **assembler**: [assemble_cost64f_certificates_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/assemble_cost64f_certificates_20261116.py)（64d版と同一protocol・split閾値1,200,000 bytes）。
- **manifest**: [class2-lane-cost64f-win3-certificates-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-win3-certificates-20261116.json)（全git blob pin・md5・sha256込み）。

## 解釈上の注意

**WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10 56件と転送5件はLOSS証明ではない。NOT-STERILEも行の勝敗を意味しない。head 1435のまま、solved 1435はmanifest被覆の簿記。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親は引き続きUNKNOWN。**

## 成果物

- raw batches: `class2-lane-cost64f-raw-batch1..8-20261116.jsonl`（blob pinはclaim v2に記録）
- determinism rerun: [class2-lane-cost64f-v16-determinism-rerun-batch2-20261116.jsonl](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-v16-determinism-rerun-batch2-20261116.jsonl)
- v15 crosscheck: [class2-lane-cost64f-v15-crosscheck-20261116.jsonl](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-v15-crosscheck-20261116.jsonl)
- claim v2: [class2-lane-cost64f-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-inflight-20261116.json)（v1全欄保存・supersedes欄にv1 blob pin）
- 証明書16ファイル: `class2-lane-cost64f-certificates/`（parts/receipt/summary/bareiss/bigint verify）

## 次回

- **cost-64f fold**: `recompute_frontier_cost64f_receipts_20261116.py`新規作成で3 receiptsをhead 1435にfold（64d foldと同構成・conflict census・per-receipt marginals・閉鎖行数確定）→ head前進。予想閉鎖にはchild行自身（bit 39 root = child|1<<39）を含む。
- fold後のcensus再計算で次の最安open行を決定（現次点 `00000000000100003800000008080000`・59 openの可能性が高いがorbit共有で変動し得る）。
- 並走in-flight着手禁止: 76c `00000000010000809092000001000000`・69a `00000000000000801222000000800000`。
