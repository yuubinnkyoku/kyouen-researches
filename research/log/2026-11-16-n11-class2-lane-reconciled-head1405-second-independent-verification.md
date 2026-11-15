# 2026-11-16：reconciled canonical head 1405の第二独立検証 — 反対方向からの全量再実装でpublished reconciliationと完全一致

開始時main: `ca0e8c42`（cost-70g fork reconciliation着地・新canonical head **1405/6443/509457/4713/373180**・fork heads 1400/1403ともsuperseded）。本レーンは着地前に同マージを独立に実装中だったため、重複pushではなく**反対方向からの第二独立実装による検証**として確定させた。

## 検証の独立性

published reconciliation（`recompute_frontier_reconcile_canonical1400_cost70g_20261116.py`）は「1403側の70g foldを再現し、1400 headをbranch D上で63h coverから再構成してから7 receiptを1400にre-base」する経路。本検証 `verify_reconciled_canonical1405_second_independent_20261116.py` は**反対方向**から同一マージを実装する:

- 共通のcost-65m 1396 baselineをin-process runpyで再現（head JSON+両CSVのblob shaをmainと照合）。
- branch M（merged 63h+63i+63j+65m+67d fold・head 1400）とbranch G（cost-70g fold・head 1403）を**各subprocessでpublished scriptごと再実行**（runby鎖・全blob assert込み）し、両headの3出力がmainとbyte-identicalであることを再確認。
- 3つのreceipt cover集合（63h bit-89・67d bit-97・70g 7 rootsのunion）を**1396 baseline上でfold**し、fork集合等式 `s_M == s_1396 | cov(63h) | cov(67d)`・`s_G == s_1396 | cov(67d) | cov(70g)`・`s_merged == s_1396 | cov(63h) | cov(67d) | cov(70g) == s_M | cov(70g) == s_G | cov(63h)` を検証。
- **逆順replayを双方向**で確認（1403 headに63h cover、1400 headに70g cover、いずれも同一set+summary）。

## 一致結果（全てassert済み）

| 項目 | 結果 |
| --- | --- |
| frontier 1405/6443/509457/4713/373180 | published head JSONとfield-by-field一致（histogram・best/next ranking込み） |
| 6 parents（第二候補 6/439・70g parent2 48/3885・dual 68/5202・class4 75/5416・67d parent2 82/6269・63i第2親 24/1704） | 全一致 |
| per-bit addition 7件（covers/marginal/mim/marginal hexes/rows/md5/sub_roots） | 全一致（mim合計5・zero-mim bits 59/89/112） |
| **ranking CSV（7,535 B）** | **byte-identical**（blob `26fa720b…`） |
| **top-candidates CSV（3,801 B）** | **byte-identical**（blob `c3433eee…`） |

cover overlapの事実も確定: `cov(63h) & cov(70g)` は**ちょうど1生の非manifest位置** `00000000020000801202000040000000`（solved計数への影響なし）・`cov(70g) & s_1400 == 10`・`cov(63h) & s_1403 == 2`。70g 7 rootsは705 branch-M roots（63h root込み）とraw+D4双方でdisjoint。8証明書（63h 26,070行・70g 350,567行/12,679,157 bytes/395 sub-roots）はlocal bytesに対してheaders/root行/行数/md5を再assert（BigInt+Number Bareiss+tsverifyの深部検証はbranch G再現とreconstruct script内でPASS済み）。

## 運用

- 検証は2回実行でbyte-identical（verification JSON 2,659 B・blob `0d4d121e…`）。所要~27秒/回（branch M/G subprocess再現込み）。
- tmp-cost70g runtime入力は `reconstruct_tmp_cost70g_20261116.py` で公開成果物から再構成（tmp-cost83c/83d/84a/83a/69i/62a/58c/63h/63i/63j/65m/67dの再構成鎖も本セッションで全再実行し、fresh mirrorから1405が完全再現可能なことを確認）。

## 解釈境界

- 本検証は公開receiptの帳簿検証であり、いかなる局面の勝敗判定でもない。solved 1405はmanifest被覆の計数。
- REFUTED-D10はLOSS証明ではない。WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## レジューム

- canonical baselineは**head 1405**（`class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json`・blob `b3ad19d7…`）。以後のfoldは1405へのrebase必須。
- 第二候補S5残6行/439のうち、cost-64（64a STERILE）とcost-71（71d STERILE）はdepth-10 receiptでは閉鎖不能。cost-75は75e（sweep完了済み・成果物未公開のin-flight memo）・cost-76一方は76cがIN FLIGHT。**未claimの残行はcost-76 `00000000040000003800080008000000` とcost-77 `00000000040000809002000000004000`**。
- 75e/76cの着地検知→1405 re-base foldの必要性評価と、監査v12（両実装+agreement v9・1405 endpoint）が次回定型候補。
