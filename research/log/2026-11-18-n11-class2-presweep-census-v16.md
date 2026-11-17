# n11 class2-lane presweep census v16: 80e行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost80e sweep完了（0 WIN7-D10 / 80 REFUTED-D10 / 0 capped・87,301,907 candidate
nodes・raw 12ファイル + audit + claim v2はcommit `72769e1e`で出版・audit blob
`53007edc`・claim v2 blob `9190341a`）を受け、head-1473 presweep censusをv15から
v16に更新した。v16は19番目のverdict map（cost80e: 0 WIN / 80 REFUTED / 0 capped）
をoverlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v16_20261118.py`
  （v15スクリプト blob `5a53528f` を基盤に、census v15 JSON・80e raw batch
  12ファイル / audit / claim v2の入力を追加し、19番目のverdict map `cost80e`
  を構築。実行環境リセット後はrepoのraw CDNから全入力を再構築して実行し、
  v15の出力が出版済みJSON（blob `dfb61db5`）とbyte-identicalに再現される
  ことを最初に確認した上でv16に進んだ）。
- 80e生バッチ12ファイル（9 sweep + det1/det8 + v15 crosscheck）を独立再監査
  （9×3402 + 1×5949 pilot・80/80 per-bit REFUTED-D10・node sum 87,301,907・
  audit per_bitのroot_canon == D4 canon(child|bit) を全80 bitで検証・det1/det8は
  ms以外全field同一・v15 cross-engine 12/12一致）。
- claim v2との一致: counts {0, 80, 0}・batches_run 9・open 68/68・
  receipt_fold "not needed"・confirmation 12/12がcensus v15 overlay予測と一致
  （root_canon転移元: pre-64h harvest ×4（bits 5/30/90/115）・cost74i ×2
  （27/93）・cost79e ×2（35/85）・cost75f ×2（41/79）・cost79d ×2（46/74））。
  さらにswept childがcensus v15のselected targetと一致し、claimのopen bitsが
  census v15のsweep bitsと完全一致することを検証。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。19 map構築は内部conflict 0・
  harvestとのcross-agree 46 canons（80e map由来 +4: 80e childのconfirmation
  4 bitsがpre-64h harvestとcanon一致し、いずれもREFUTED-D10で一致）。
- 39 family行を再計算し、v15のpublished countsを39/39で再現
  （`family_row_v15_newly_covered_counts_reproduced`・
  `family_row_open_v15_minus_80e_only_reproduced`: 差分は80e map由来のみ）。
- 二重実行byte-identical（117,673 bytes）。

## 結果

- 80e行（`00000000020000003800000180000000`）をswept扱いのexcluded行として
  記録（open 0・known 80・newly_covered_by_nineteen_maps 76・完全反証・
  証明書なし・receipt fold不要）。5つ目の完全反証行（74i・75f・79d・79eに次ぐ）。
  fully swept childrenは19に増加。
- 次ターゲット: **`00000000020000003800200080000000`（cost 80・open 67・
  confirmation 13・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:1}）**。census v15 runner-up。v15時点のopen 68のうち
  1 bit（88）が80e mapのcanon等価で新規被覆され、open 67に減少
  （次ターゲットのconfirmationにcost80e由来の転移が初めて入った）。
  confirmation 13 bits（5/27/30/35/41/46/74/79/85/88/90/93/115）は全て
  REFUTED-D10（pre-64h harvest ×4・cost74i ×2・cost79e ×2・cost75f ×2・
  cost79d ×2・cost80e ×1）で、sweepでfreshに再実行する。legal_candidates.py
  独立列挙と80 bit（67 open + 13 confirmation）で一致。
- runner-up: `00000000020000003800000080008000`（cost 81・open 68）。
  ranking top-10の10行はすべてparent
  `00000000020000003800000080000000`（cost 80〜86・open 67〜73）。
  v15 rankingの非swept 9行は全てv16 top-10に残留（9/9）。
- cross_checks新規（80e系）: refuted bits claim/audit一致 80/80・
  raw batch再監査 12ファイル（9×3402 + 1×5949 pilot・node sum 87,301,907）・
  confirmation 12/12（root_canonはcensus v15 transfer canonsと一致）・
  v15 cross-engine 12/12 loss=false・det再実行field-identical・receipt fold
  "not needed (0 win bits)"・証明書 "not applicable (0 win bits)"・
  v15 selected target / sweep bits / confirmation bitsの完全一致。

## 出版

- census v16 JSON: `class2-lane-next-target-presweep-1473-v16-20261118.json`
  （git blob `972434a4ca5df21174dc1034ac35d118fca37fc1`）
- スクリプト: git blob `871bc0d089db08d4154234d3547b3da2b7912c17`

## 制限

- censusはsearch-plan bookkeepingのみで、verdictを新規作成しない。
  REFUTED-D10はLOSS証明ではない。11×11空盤、二石root {49,60}/{59,60}、
  S2 {59,60}、class 1/2/4はいずれも **UNKNOWN** のまま。
