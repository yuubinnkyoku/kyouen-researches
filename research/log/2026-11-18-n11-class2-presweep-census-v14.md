# n11 class2-lane presweep census v14: 79d行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost79d sweep完了（0 WIN7-D10 / 79 REFUTED-D10 / 0 capped・49,103,515 candidate
nodes・raw commit `1371465c`・audit blob `cfc6fbe3`・claim v2 commit `f417be0c`
・claim v2 blob `8805876f`）と、並走によるcost79c claim v2への19/19 BigInt
一般化円第三監査corpus同期（commit `8a335959`・残り16 bits監査blob
`410fb935`・同期後claim blob `ca517b73`）を受け、head-1473 presweep censusを
v13からv14に更新した。v14は17番目のverdict map（cost79d: 0 WIN / 79 REFUTED /
0 capped）をoverlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v14_20261118.py`
  （v13スクリプト blob `9976d8ce` を基盤に、79d raw batch 12ファイル / audit /
  claim v2 / 同期後79c claim / 残り16 bits第三監査の入力を追加し、17番目の
  verdict map `cost79d` を構築）。
- 79d生バッチ12ファイル（9 sweep + det1/det8 + v15 crosscheck）を独立再監査
  （9×3402 + 1×5949 pilot・79/79 per-bit REFUTED-D10・node sum 49,103,515・
  audit per_bitのroot_canon == D4 canon(child|bit) を全79bitで検証・det1/det8は
  ms以外全field同一・v15は7/7一致）。
- claim v2との一致: counts {0, 79, 0}・batches_run 9・open 72/72・
  receipt_fold "not needed"・confirmation 7/7がcensus v13 overlay予測と一致
  （root_canon転移元: pre-64h harvest ×3・cost74i ×2・cost75f ×2）。
- 同期後79c claim v2の19/19 BigInt corpusを検証
  （bigint_full_corpus_bits == 19 WIN bits − bit 110・監査blobs
  [50190347, 410fb935]・残り16監査はall_pass・union 0/0）。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。17 map構築は内部conflict 0・
  harvestとのcross-agree 40 canonsを維持。
- 39 family行を再計算し、v13のpublished countsを39/39で再現
  （`family_row_open_v13_minus_79d_only_reproduced`: 差分は79d map由来のみ）。

## 結果

- 79d行（`00000000020000003800400080000000`）をswept扱いのexcluded行として
  記録（open 0・known 79・完全反証・証明書なし・receipt fold不要）。
  3つ目の完全反証行（74i・75fに次ぐ）。
- 次ターゲット: **`00000000020000003800000880000000`（cost 79・open 72・
  confirmation 7・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:2}・石bits [31,35,59,60,61,89]）**。census v13 runner-up。
  v13時点のopen 74のうち2 bits（46/74）が79d mapのcanon等価で新規被覆され、
  open 72に減少。confirmation 7 bits（27/30/46/74/79/93/115）は全て
  REFUTED-D10（pre-64h harvest ×2・cost74i ×2・cost75f ×1・cost79d ×2）で、
  sweepでfreshに再実行する。legal_candidates.py独立列挙と79bit
  （72 open + 7 confirmation）で一致。
- runner-up: `00000000020000003800000180000000`（cost 80・open 70）。
  ranking top-10の10行はすべてparent
  `00000000020000003800000080000000`（cost 79〜86・open 70〜76）。
  v13 rankingの非swept 9行は全てv14 top-10に残留（9/9）。
- cross_checks新規（79d系）: refuted bits claim/audit一致 79/79・
  raw batch再監査 12ファイル・confirmation 7/7（root_canonはcensus v13
  transfer canonsと一致）・v15 cross-engine 7/7 loss=false・det再実行
  field-identical・receipt fold "not needed (0 win bits)"・証明書
  "not applicable (0 win bits)"。79c系ではbigint full corpus 19/19を追加。

## 制限

- censusはsearch-plan bookkeepingのみで、verdictを新規作成しない。
  REFUTED-D10はLOSS証明ではない。11×11空盤、二石root {49,60}/{59,60}、
  S2 {59,60}、class 1/2/4はいずれも **UNKNOWN** のまま。
