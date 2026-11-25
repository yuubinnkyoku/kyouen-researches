# head-1472 cover-multiplicity audit (post-fold) vs preregistered prediction (2026-11-17)

## 背景

本レーンはcost64h fold receipt着地前に、head-1472 cover-multiplicity監査の**予測**を
preregistrationとして出版していた（`class2-lane-head1472-cover-multiplicity-audit-prediction-20261116.json`、
commit `d4f5044f`、log `2026-11-16-n11-class2-lane-head1472-cover-multiplicity-prediction.md`）。
cost64h fold receiptの着地（`828c595c`）とprereg agreement check 19/19 PASSを受け、
post-fold監査を実行して予測との全フィールド照合を行った。

## 実行

- basis再構成: head-1452 receipt basisを出版済みファイルからverbatim抽出
  （BASE_WIN7_ONLY 26ファイル + class-frontier chain 103ファイル（着地済みcost64h fold receiptはglobから除外）+ named frontier recompute 6ファイル）。
  **775 roots / covered 1452をassert**（predictionと同一のsemantics・同一ファイル集合）。
- 23 receipt rootsは**着地済みfold receiptから**読み取り（`root_hex == child|1<<bit`・popcount 7・basis非重複を全23件でassert）。
  予測時はsweep由来のWIN bit列から導出していた点が本実行との差分（独立経路）。
- manifest（MS5 6 part CSV）とwinners（win7-reuse-hits.csv.gz）はraw CDNから取得し、
  fold receipt blob `1633be292f...` をscript内でpin照合。
- 出力は2回実行でbyte-identical（md5 `be206d55fe62eb620f699bb050fd9660`）。

## 結果（13/13 field groups一致・mismatch 0・status PASS）

- head control: basis 775→798 roots、covered 1452→1472、winners 498、marginal_in_manifest 20。
  着地fold receiptのfrontier 6数値 `[1472, 174, 6376, 504672, 4649, 368586]` とも一致。
- multiplicity histogram: winner_only 433、mult 1が577、mult 2が215、mult 3が89（予測完全一致）。
- single-cover orbits: 577件・cost合計 42,817（予測完全一致・orbit一覧まで同一）。
- roots_with_exclusive_contribution: 463（予測一致）。
- top_exclusive_roots上位20件・per-receipt marginal詳細（23件のcovers/marginal_hexes）も完全一致。
- 予測JSON（prediction blob）の全数値がpost-fold監査で再現された。**乖離は0件**。

head-1472基盤の実効的最小検証集合は単一被覆root 577（cost 42,817）であり、
head-1441監査（`fbafd1e1`）の構造（exclusive roots 463・最大依存は単一rootの4 orbitのみ）は
64h fold後も不変であることをhead 1472で再確認した。

## 制限

- 監査はpublished receiptsに対するbookkeepingであり、engine search・新規verdictは存在しない。
- solved 1472はmanifest被覆の簿記。multiplicity 1は証明書不足を意味しない。
- WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cover_multiplicity_audit_head1472_postfold_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-head1472-cover-multiplicity-audit-20261117.json`

## 次の一手

- head-1472起点のpresweep census（次の最安open行の決定）が次ターゲット選定の入口。
- cost76c fold receiptは未着地（並走claim済み・着手禁止）。cost66i receipt foldは76c着地まで着手禁止。
