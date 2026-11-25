# 2026-11-17：cost66i head1473 marginal rebase auditと再現器修正

## 開始時点

mainの開始headは `c24eb5380ea847888e7c38fe89ca6bfcf38f89eb`。最新の `AGENTS.md`、`research/knowledge/README.md`、K0023/K0863/K0865/K0868、cost76c bit61 certificate/fold、cost66iの9証明書manifestとbit19 BigInt再検証記録、head1472 presweepを確認した。

cost76c bit61のreceipt foldは既に着地し、canonical headは
`1473/174/6375/504596/4648/368510`。
cost66iの9証明書は出版済みで、Bareiss検証済み。bit19は別実装BigIntでもPASSしている。ただし旧marginalはhead1452基準なので、head1473では再計算が必要だった。

## 再現器の不具合修正

既存の `rebase_cost66i_marginals_head1473_20261117.py` を実行したところ、CSVの `own_candidates_s6_s7_edge_cost` は文字列で読み込まれるのに、合計箇所で `int()` 変換をせず `sum(str...)` を実行していたため、`TypeError` で停止した。

合計式を
`sum(int(worklist[h]["own_candidates_s6_s7_edge_cost"]) ...)`
に修正した。ほかの計算規則・入力・判定条件は変更していない。

- 修正commit: `82c2bde0788b324e84d1996950c1c4c73367759a`
- 修正後blob: `83b570cda124293c055d822c4ba4bcc73cc9ea0d`
- `py_compile`: PASS
- 依存入力7件と修正後スクリプトのGit blob SHA pin: 8/8 PASS
- 新規プロセスで2回実行: stdout byte-identical
- stdout: 12,515 bytes、SHA-256 `fd742a7836054b47042ea7dfb906eaa93f3d306f65bab59c71f8f92e1667c66c`

## head1473での再計算結果

9本の既存WIN7-D10証明書のD4正準形・manifest被覆を再計算し、cost64hとcost76cで既に閉じた行を差し引いた。

| receipt順 | bit | 新規S6行 | edge cost |
|---:|---:|---:|---:|
| 1 | 19 | 3 | 207 |
| 2 | 28 | 1 | 74 |
| 3 | 29 | 0 | 0 |
| 4 | 58 | 0 | 0 |
| 5 | 88 | 1 | 83 |
| 6 | 90 | 0 | 0 |
| 7 | 99 | 1 | 77 |
| 8 | 103 | 1 | 73 |
| 9 | 112 | 0 | 0 |
| **合計** | | **7** | **514** |

bit19が最大の逐次marginalで、単独で3 manifest行・edge cost 207を閉じる候補。bit19の証明書は52合法防御、40,935戦略行、52/52 subroot、union差0/0、終端石数[13,17]で、既存Bareiss記録に加えBigInt独立再検証もPASSしている。

bit19だけをfoldした場合の**投影**は次のとおり。

- solved S6 manifest rows: 1473 → 1476
- unique remaining S6: 6375 → 6372
- sum remaining edge cost: 504596 → 504389
- S6 demand by open classes: 4648 → 4645
- open-class demand cost: 368510 → 368303

9 receiptすべてを順にfoldした場合の投影は 1480 / 6368 / 504082 / 4641 / 367996。S5 orbit数はparent-incidence閉鎖監査なしでは投影していない。

## 解釈と次の作業

今回行ったのはhead1473への集合論的marginal再基準化だけであり、**receipt foldはまだ適用していない**。新しい探索verdictも作っていない。bit19を次のfold候補として選ぶ根拠がhead1473上で再確認できた。

次はbit19の証明書・root・既存receiptとの重複・WIN/LOSS矛盾を再検査したうえで、parent-incidenceを独立再導出してfoldする。remaining S5 orbit数はその監査後にのみ更新する。

REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWNのまま。
