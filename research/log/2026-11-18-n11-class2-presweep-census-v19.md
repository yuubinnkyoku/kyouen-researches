# n11 class2-lane presweep census v19: 82d行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost82d sweep完了（0 WIN7-D10 / 82 REFUTED-D10 / 0 capped・127,619,232 candidate
nodes・raw 12ファイル + audit + claim v2 + logはcommit `775277b5`で出版・audit
blob `14a44c8b`・claim v2 blob `cffeda69`・batch 1-5は並走セッション出版・
batch 6-9 + det + v15 crosscheckは第二セッションの全ビット独立再実行と
field一致検証の上で出版）を受け、head-1473 presweep censusをv18からv19に
更新した。v19は22番目のverdict map（cost82d: 0 WIN / 82 REFUTED / 0 capped・
band名cost82d。cost82 / cost82b / cost82cは既に過去のbandで使用済みのため
最高位+1のdを採用）をoverlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v19_20261118.py`
  （v18スクリプト blob `99371f15` を基盤に、census v18 JSON・82d raw batch
  12ファイル / audit / claim v2の入力を追加し、22番目のverdict map `cost82d`
  を構築）。v18→v19変換で確認済みの罠（全pre-twin除外リストへの新map追加・
  pre81 twinからの82d除外・families行assertionの前バンド分のassert形式への
  変換）を踏襲。
- 82d生バッチ12ファイル（9 sweep + det1/det8 + v15 crosscheck）を独立再監査
  （9×3402 + 1×5949 pilot・82/82 per-bit REFUTED-D10・node sum 127,619,232・
  audit per_bitのroot_canon == D4 canon(child|bit) を全82 bitで検証・det1/det8は
  ms以外全field同一・v15 cross-engine 17/17一致）。
- claim v2との一致: counts {0, 82, 0}・batches_run 9・open 65/65・
  receipt_fold "not needed"・confirmation 17/17がcensus v18 overlay予測と一致
  （root_canon転移元: pre-64h harvest ×4（5/30/90/115）・cost81 ×2（15/105・
  初の81由来転移）・cost74i ×2（27/93）・cost80e ×1（32）・cost79e ×2（35/85）・
  cost75f ×2（41/79）・cost80f ×2（45/75）・cost79d ×2（46/74））。swept
  childがcensus v18のselected targetと一致し、claimのopen bitsがcensus v18の
  sweep bitsと完全一致。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。22 map構築は内部conflict 0・1,513 distinct
  canons（v18の1,444から +69: 82d childの65 open bit + harvest重複4 bit）・
  harvestとのcross-agree 57 canons（v18の53から +4: 82d childのharvest由来
  confirmation 4 bits 5/30/90/115がcanon一致、いずれもREFUTED-D10）。
- 39 family行を再計算し、v18のpublished countsを39/39で再現
  （`family_row_v18_newly_covered_counts_reproduced`・
  `family_row_open_v18_minus_82d_only_reproduced`: 差分は82d map由来のみ）。
- 二重実行byte-identical（140,936 bytes）。

## 結果

- 82d行（`00000000020000003800000080000800`）をswept扱いのexcluded行として
  記録（open 0・known 82・newly_covered_by_twenty_two_maps 78・完全反証・
  証明書なし・receipt fold不要）。8つ目の完全反証行（74i・75f・79d・79e・
  80e・80f・81に次ぐ）。fully swept childrenは22に増加。
- **残poolが8行に縮小し、全行が同一parent
  `00000000020000003800000080000000`のchildrenに**（cost 82〜87）。
  v18 rankingの非swept 8行は全てv19 rankingに残留（8/8）。82d mapは各
  sibling行の対称bit 2個をcanon被覆し、全8行のopenが2減（例: 次ターゲット
  65→63・runner-up 66→64）。
- 次ターゲット: **`00000000020000003800000090000000`（cost 82・open 63・
  confirmation 19・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:3}・legal 82）**。census v18 runner-up。confirmation 19 bits
  （5/11/15/30/32/35/41/45/46/74/75/79/85/88/90/93/105/109/115）は全て
  REFUTED-D10（pre-64h harvest ×4（5/30/90/115）・**cost82d ×2（11/109・
  初の82d由来転移）**・cost81 ×2（15/105）・cost80e ×2（32/88）・cost79e ×2
  （35/85）・cost75f ×2（41/79）・cost80f ×2（45/75）・cost79d ×2（46/74）・
  cost74i ×1（93））で、sweepでfreshに再実行する。legal_candidates.py独立列挙
  と82 bit（63 open + 19 confirmation）で一致。
- runner-up: `00000000020000003800000080000400`（cost 84・open 64）。
- cross_checks新規（82d系）: refuted bits claim/audit一致 82/82・raw batch再監査
  12ファイル（9×3402 + 1×5949 pilot・node sum 127,619,232）・confirmation 17/17
  （root_canonはcensus v18 transfer canonsと一致）・v15 cross-engine 17/17
  loss=false・det再実行field-identical・receipt fold "not needed (0 win bits)"・
  証明書 "not applicable (0 win bits)"・v18 selected target / sweep bits /
  confirmation bitsの完全一致。

## 出版

- census v19 JSON: `class2-lane-next-target-presweep-1473-v19-20261118.json`
  （git blob `a0c6abaf0df163eddc35f8b8dc0f8c0eb4268fe6`）
- スクリプト: git blob `8ba51a2d838a13ddddf671d06593db54b0947709`

## 制限

- censusはsearch-plan bookkeepingのみで、verdictを新規作成しない。
  REFUTED-D10はLOSS証明ではない。11×11空盤、二石root {49,60}/{59,60}、
  S2 {59,60}、class 1/2/4はいずれも **UNKNOWN** のまま。
