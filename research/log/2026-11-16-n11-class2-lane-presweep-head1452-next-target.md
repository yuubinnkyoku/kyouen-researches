# 2026-11-16：head-1452 next-target presweep census — 次の純粋class-2 target 18行/1287の正確な残作業判別

開始時main: `aa5af9f33`（cost-76d/77e fold公開済み、head 1452/174/6396/506144/4669/370058）。`next_target_presweep_head1452_20261116.py`（commit公開済み）で、fold scriptをrunpy再現してhead 1452を全pin付きで再構成し（775 receipt roots / 760 distinct D4 canons）、公開済みのclass2-lane claim/sweep JSON網羅的収穫（harvest）+ 76d/77e raw batch検証の上で、3つのactionable target familyのper-bit censusを行った。出力 `class2-lane-next-target-presweep-1452-20261116.json`（blob `0d9a94a2…`・174,950 B）。

## verdict corpus harvest

- glob harvest 79ソース…77 claim/sweep JSON ファイル（per-child bit accounting + cross-source conflict assertion、**conflict 0**）。skip 87件はresults未掲載のin-flight claim（75e/76c/67d/69a等、成果物未公開が正しい）・証明書/audit/prereg類。
- 76d raw batch 10本: 72 canon新規追加、4 canonは既存harvestと一致（bit-exact、WIN [19,49] 再確認）。77e raw batch 10本: 77 canon全てsweep JSON harvestと一致（独立cross-validation）。
- 計 **3548 distinct verdict canons**（WIN7-D10 353 / REFUTED-D10 3195）。

## census結果（head 1452、receipt roots 775）

| family | rows/edge cost | occurrences | open canons | occurrences open after census |
|---|---|---:|---:|---:|
| 次の純粋class-2 target `00000000000000403800000008000000` | 18/1287 | 1287 | 1134 | 1264 |
| best coverable class-2 `00000000000000801202000040000000` | 3/211 | 211 | 126 | 127 |
| best class-4 `00000000020000003800000080000000` | 18/1460 | 1460 | 1023 | 1255 |

- **純粋class-2 targetの最安行は cost-64 `00000000000000403800000008100000`（64候補・全bit open・demand c1=0,c2=2）**。次に cost-66 3行（open 64/65/65）、cost-69 `...80000020`（open 62、7 bit harvested-refuted）。
- best coverable class-2の cost-64 行 `00000000000000801282000040000000` は 56 bit open / 8 bit既知。cost-76 行は 71 open。
- best class-4の最安行は cost-74 `00000000020000003800000088000000`（open 70）。

## 信頼境界

- censusはsearch-plan bookkeepingのみ。engine searchなし、verdict作成なし、行閉鎖なし。'open' は「公開成果物の範囲で未判定」の意味（未公開の並走lane成果を含まない保守的判定）。
- WIN7-D10は各7石rootから深さ10以内の先手勝ちのみを証明。REFUTED-D10はLOSS証明ではない。foldはmanifest被覆の帳簿。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4 は引き続き **UNKNOWN**。

## 次の一手

- 純粋class-2 targetの最安行 cost-64 `00000000000000403800000008100000`（64候補・全open・unswept unclaimed）が次のsweep lane候補。並走セッションはclaim→prereg→sweepの手順を守ること。
- 75e（並走lane、成果物公開待ち）と76c（in-flight）の着地後に本censusをrebaseすること。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1452_20261116.py
```

実行時間約1〜2分。byte-identical再現を確認済み。
