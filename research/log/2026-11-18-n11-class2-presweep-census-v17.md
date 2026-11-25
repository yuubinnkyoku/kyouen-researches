# n11 class2-lane presweep census v17: 80f行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost80f sweep完了（0 WIN7-D10 / 80 REFUTED-D10 / 0 capped・51,125,648 candidate
nodes・raw 12ファイル + audit + claim v2はcommit `77990039`で出版・audit blob
`52abb721`・claim v2 blob `aed40c10`（confirmation_outcome fieldのみ
`e54b24a2`から修正、commit `b2c01968`））を受け、head-1473 presweep censusを
v16からv17に更新した。v17は20番目のverdict map（cost80f: 0 WIN / 80 REFUTED /
0 capped）をoverlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v17_20261118.py`
  （v16スクリプト blob `871bc0d0` を基盤に、census v16 JSON・80f raw batch
  12ファイル / audit / claim v2の入力を追加し、20番目のverdict map `cost80f`
  を構築）。
- 80f生バッチ12ファイル（9 sweep + det1/det8 + v15 crosscheck）を独立再監査
  （9×3402 + 1×5949 pilot・80/80 per-bit REFUTED-D10・node sum 51,125,648・
  audit per_bitのroot_canon == D4 canon(child|bit) を全80 bitで検証・det1/det8は
  ms以外全field同一・v15 cross-engine 13/13一致）。
- claim v2との一致: counts {0, 80, 0}・batches_run 9・open 67/67・
  receipt_fold "not needed"・confirmation 13/13がcensus v16 overlay予測と一致
  （root_canon転移元: pre-64h harvest ×4（bits 5/30/90/115）・cost74i ×2
  （27/93）・cost79e ×2（35/85）・cost75f ×2（41/79）・cost79d ×2（46/74）・
  cost80e ×1（88・初の80e由来転移））。さらにswept childがcensus v16の
  selected targetと一致し、claimのopen bitsがcensus v16のsweep bitsと完全
  一致することを検証。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。20 map構築は内部conflict 0・
  harvestとのcross-agree 50 canons（80f map由来 +4: 80f childのconfirmation
  4 bits 5/30/90/115がpre-64h harvestとcanon一致し、いずれもREFUTED-D10で一致）。
- 39 family行を再計算し、v16のpublished countsを39/39で再現
  （`family_row_v16_newly_covered_counts_reproduced`・
  `family_row_open_v16_minus_80f_only_reproduced`: 差分は80f map由来のみ）。
- 二重実行byte-identical（125,397 bytes）。

## 結果

- 80f行（`00000000020000003800200080000000`）をswept扱いのexcluded行として
  記録（open 0・known 80・newly_covered_by_twenty_maps 76・完全反証・
  証明書なし・receipt fold不要）。6つ目の完全反証行（74i・75f・79d・79e・80e
  に次ぐ）。fully swept childrenは20に増加。
- 次ターゲット: **`00000000020000003800000080008000`（cost 81・open 66・
  confirmation 15・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:3}）**。census v16 runner-up。v16時点のopen 68のうち
  2 bits（45/75）が80f mapのcanon等価で新規被覆され、open 66に減少
  （次ターゲットのconfirmationにcost80f由来の転移が初めて入った）。
  confirmation 15 bits（27/30/32/35/41/45/46/74/75/79/85/88/90/93/115）は
  全てREFUTED-D10（pre-64h harvest ×3・cost74i ×2・cost80e ×2・cost79e ×2・
  cost75f ×2・cost79d ×2・cost80f ×2）で、sweepでfreshに再実行する。
  legal_candidates.py独立列挙と81 bit（66 open + 15 confirmation）で一致。
- runner-up: `00000000020000003800000080000800`（cost 82・open 67）。
  ranking top-10の10行はすべてparent
  `00000000020000003800000080000000`（cost 81〜87・open 66〜72）。
  v16 rankingの非swept 9行は全てv17 top-10に残留（9/9）。
- cross_checks新規（80f系）: refuted bits claim/audit一致 80/80・
  raw batch再監査 12ファイル（9×3402 + 1×5949 pilot・node sum 51,125,648）・
  confirmation 13/13（root_canonはcensus v16 transfer canonsと一致）・
  v15 cross-engine 13/13 loss=false・det再実行field-identical・receipt fold
  "not needed (0 win bits)"・証明書 "not applicable (0 win bits)"・
  v16 selected target / sweep bits / confirmation bitsの完全一致。

## 出版

- census v17 JSON: `class2-lane-next-target-presweep-1473-v17-20261118.json`
  （git blob `22078142d6d616335bc1bc363065d91750b6ca14`）
- スクリプト: git blob `382c375b9754d09a29d6a242e022636fae506b43`

## 制限

- censusはsearch-plan bookkeepingのみで、verdictを新規作成しない。
  REFUTED-D10はLOSS証明ではない。11×11空盤、二石root {49,60}/{59,60}、
  S2 {59,60}、class 1/2/4はいずれも **UNKNOWN** のまま。
