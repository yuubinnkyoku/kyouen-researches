# 2026-11-15 n11 class2-lane cost-76b independent second audit (sweep + certificates + fold, post-landing)

第二独立検証セッション。並走sweepレーンが一括着地した cost-76b（child `00000000000000801302000000200000`, cost 76, 第二coverable class-2 target S5 `00000000000000801202000000200000` の最安未sweep行、commit 5ef0d819、head 1277→**1280/6567/518678/4837/382401**）の sweep・証明書2枚・fold簿記を、main公開成果物のみから再構築したmirrorで独立監査した。**104チェックすべてPASS、2回実行で監査JSON byte-identical（md5 29f53e3016215a5b7828fe577e4f487f）**。

## 実施内容（`audit_cost76b_sweep_fold_independent_20261115.py`、純stdlib・Bareiss 4x4・独立D4群・浮動小数点なし）

1. **sweep再導出**: 独立合法候補列挙（Bareiss 4x4）がclaimの76候補とbit-exact一致。raw batch 10件（9×8+1×4）を再集計し、全76候補が厳密に1回ずつ出現・WIN7-D10 bits [72, 96]・74 REFUTED・0 capped・候補ノード計 107,961,863・全terminal stone range 13..17・root == child XOR (1<<bit) を確認。v16 determinism rerun（batch 5）がms以外node-exact、v15交差（pilot 5949・WIN 3,999,895/7,364,097 nodes loss=true・アンカーbits 0/1/2 loss=false・6行構成）を確認。
2. **証明書2枚の再検証**: bit72（50,796 rows / mobility 60）・bit96（67,641 / 61、2-part結合でsplit manifestと全件一致）とも、receipt の bytes/md5/sha256/git blob sha が一致し、公開 Bareiss リプレイ検証器（`verify_cost73h_win7_bareiss_independent.py`）と本セッションの有理系（`verify_cost75d_win7_rational_independent.py`）の**両方を再実行してPASS**。consumed集合が両系統の再実行出力と公開fold入力dumpで一致。7石rootの合法手列挙（60/61手）も独立導出で legal-moves.json とbit-exact一致。
3. **fold簿記 1277→1280**: head 1277 JSONがcanonical blob sha 8d96b482... とbyte一致。solved +3 = in-manifest marginal 3、remaining cost −218 = 76+69+73、ranking変更が parent1 17/1325→16/1249 と `...80120200004000000` 43/2984→42/2915 と `...403800000008000000` 52/3742→51/3669 の3行のみ、と独立再計算で一致。3つの in-manifest marginal hex がそれぞれ対応S5の6石小行であることを superset 検査で確認。fold出力3件（head JSON/ranking/top-candidates）の git blob sha がclaim記録と一致。5削除軌道は両rankingに不在（1277時点で既に閉鎖）。
4. **root新規性**: 2新rootは相互に、head 1277 の16 receipt roots にも、未foldのcost-75d 4 roots にも raw/D4 とも distinct。

## 記録価値のある観察

- **consumed dump 規約差**: 76b の consumed.txt は「サブルートごとの訪問重複付きマルチセット」（bit72 69,250行 / bit96 90,622行）で、75d の sort済み一意行規約と異なる。fold scriptは `len(set(...))==len(rows)` で正しく処理しており誤りではないが、レーン横断の規約差として記録した。
- terminal stone range は [13,15,17]（bigint JSON記録の [13,17] はmin/max）。
- 本監査は pre-sweep claim 監査（`class2-lane-cost76b-claim-independent-audit-20261115.json`、sweep in flight中に実施）の補完であり、そちらはgeometry/候補/demand/head-1277簿記のみをカバーしていた。

## 解釈境界

REFUTED-D10 は WIN7-D10 不在のみを意味し LOSS 証明ではない。WIN7証明書は個々の7石rootから深さ10以内の先手勝ちのみを証明する。foldは公開receiptに対する簿記であり、solved数はmanifest被覆であって勝敗ではない。548-root disjointness と set-equality 統制はfold scriptのrunpy鎖がassertしており、その鎖の独立再実行は次回課題。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4はいずれもUNKNOWN**。

## 機械可読記録

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76b-independent-second-audit-20261115.json`（inputs欄に全入力のbytes/md5/git blob sha）
- 監査スクリプト: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76b_sweep_fold_independent_20261115.py`

## レジューム

- cost-75d fold（4 receipts）は並走で実行環境障害によりdeferred（8ca65e72、fold入力は検証済み）。着地後、baseline 1280 rebase を含む fold script 全統制の第二独立検証（runpy鎖mirror構築が必要: `recompute_frontier_merged_cost65l_74g_69i_20261115.py` の入力一式）が次の大規模タスク。同じmirrorで76b fold の 548-root disjointness・set-equality の独立再実行も行う。
- cost-77a（IN FLIGHT claim済み、child `00000000000000801202000000204000`）は並走の領域。着手しない。
