# n11 class2-lane presweep census v18: 81行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost81 sweep完了（0 WIN7-D10 / 81 REFUTED-D10 / 0 capped・86,480,711 candidate
nodes・raw 12ファイル + audit + claim v2 + logはcommit `92e6c84d`で出版・audit
blob `f90bdccd`・claim v2 blob `5dc33107`）を受け、head-1473 presweep censusを
v17からv18に更新した。v18は21番目のverdict map（cost81: 0 WIN / 81 REFUTED /
0 capped・最初のcost-81台バンド）をoverlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v18_20261118.py`
  （v17スクリプト blob `382c375b` を基盤に、census v17 JSON・81 raw batch
  12ファイル / audit / claim v2の入力を追加し、21番目のverdict map `cost81`
  を構築）。v16→v17変換で確認済みの2罠（全pre-twin除外リストへの新map追加・
  families行assertionの前バンド分のassert形式への変換）を踏襲。
- 81生バッチ12ファイル（9 sweep + det1/det8 + v15 crosscheck）を独立再監査
  （9×3402 + 1×5949 pilot・81/81 per-bit REFUTED-D10・node sum 86,480,711・
  audit per_bitのroot_canon == D4 canon(child|bit) を全81 bitで検証・det1/det8は
  ms以外全field同一・v15 cross-engine 15/15一致）。
- claim v2との一致: counts {0, 81, 0}・batches_run 9・open 66/66・
  receipt_fold "not needed"・confirmation 15/15がcensus v17 overlay予測と一致
  （root_canon転移元: pre-64h harvest ×3（30/90/115）・cost74i ×2（27/93）・
  cost80e ×2（32/88）・cost79e ×2（35/85）・cost75f ×2（41/79）・cost79d ×2
  （46/74）・cost80f ×2（45/75・初の80f由来転移））。swept childがcensus v17の
  selected targetと一致し、claimのopen bitsがcensus v17のsweep bitsと完全一致。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。21 map構築は内部conflict 0・1,444 distinct
  canons・harvestとのcross-agree 53 canons（v17の50から +3: 81 childの
  harvest由来confirmation 3 bits 30/90/115がcanon一致、いずれもREFUTED-D10）。
- 39 family行を再計算し、v17のpublished countsを39/39で再現
  （`family_row_v17_newly_covered_counts_reproduced`・
  `family_row_open_v17_minus_81_only_reproduced`: 差分は81 map由来のみ）。
- 二重実行byte-identical（133,137 bytes）。

## 結果

- 81行（`00000000020000003800000080008000`）をswept扱いのexcluded行として
  記録（open 0・known 81・newly_covered_by_twenty_one_maps 78・完全反証・
  証明書なし・receipt fold不要）。7つ目の完全反証行（74i・75f・79d・79e・
  80e・80fに次ぐ）。fully swept childrenは21に増加。
- **残poolが9行に縮小し、全行が同一parent
  `00000000020000003800000080000000`のchildrenに**（cost 82〜87）。
  presweep-1473 frontierは単一familyに収束（
  `remaining_unswept_pool_is_single_family: true`）。v17 rankingの非swept
  9行は全てv18 rankingに残留（9/9）。81 mapは各sibling行の対称bit 2個を
  canon被覆し、全行のopenが2減（例: 次ターゲット 67→65）。
- 次ターゲット: **`00000000020000003800000080000800`（cost 82・open 65・
  confirmation 17・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:2}・legal 82）**。census v17 runner-up。confirmation 17 bits
  （5/15/27/30/32/35/41/45/46/74/75/79/85/90/93/105/115）は全てREFUTED-D10
  （pre-64h harvest ×4（5/30/90/115）・**cost81 ×2（15/105・初の81由来転移）**・
  cost74i ×2（27/93）・cost80e ×1（32）・cost79e ×2（35/85）・cost75f ×2
  （41/79）・cost80f ×2（45/75）・cost79d ×2（46/74））で、sweepでfreshに
  再実行する。legal_candidates.py独立列挙と82 bit（65 open + 17
  confirmation）で一致。
- runner-up: `00000000020000003800000090000000`（cost 82・open 65）。
- cross_checks新規（81系）: refuted bits claim/audit一致 81/81・raw batch再監査
  12ファイル（9×3402 + 1×5949 pilot・node sum 86,480,711）・confirmation 15/15
  （root_canonはcensus v17 transfer canonsと一致）・v15 cross-engine 15/15
  loss=false・det再実行field-identical・receipt fold "not needed (0 win bits)"・
  証明書 "not applicable (0 win bits)"・v17 selected target / sweep bits /
  confirmation bitsの完全一致。

## 出版

- census v18 JSON: `class2-lane-next-target-presweep-1473-v18-20261118.json`
  （git blob `11306824f2363d5002559d4d1535d91a61509929`）
- スクリプト: git blob `99371f15ae240a62ce596c3728092fb717426eb6`

## 制限

- censusはsearch-plan bookkeepingのみで、verdictを新規作成しない。
  REFUTED-D10はLOSS証明ではない。11×11空盤、二石root {49,60}/{59,60}、
  S2 {59,60}、class 1/2/4はいずれも **UNKNOWN** のまま。
