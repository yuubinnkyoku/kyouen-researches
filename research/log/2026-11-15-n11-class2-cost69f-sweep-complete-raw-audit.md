# n11 class2-lane cost69f: 69-candidate raw sweep audit

監査対象main snapshotは `2650155ad998f52f49197ed4ec1e05714ec9f26d`。`AGENTS.md` と `research/knowledge/README.md` を確認し、K0783を現在の証拠境界に合わせて更新した。

## 対象と完全性

- S5: `00000000000000809102000000000000`
- S6 child: `00000000000000809102000000000008`
- edge cost: 69
- Bareiss 4×4列挙による合法七石目: 69件
- 9 batchの候補bit列を連結するとclaimの69 bit列と完全一致。重複・欠落なし
- 各batchにpilot controlが1件あり、9件すべて3,402節点・`loss=false`

## raw sweep結果

| 項目 | 結果 |
|---|---:|
| 候補 | 69/69 |
| WIN7-D10 | **9** |
| REFUTED-D10 | 60 |
| 打切り | 0 |
| 候補探索節点 | **112,752,229** |
| pilot control | 9/9 PASS |

WIN7-D10のbitは **2, 20, 44, 68, 69, 94, 109, 118, 119**。8通りの正方形対称変換による厳密な121-bit正準化で9 rootは9軌道に分かれた。したがって9件は同一局面の対称重複ではない。

batch別内訳:

| batch | 候補 | WIN7-D10 | REFUTED-D10 | 候補節点 |
|---:|---:|---|---:|---:|
| 1 | 8 | 2 | 7 | 15,029,170 |
| 2 | 8 | 20 | 7 | 9,522,764 |
| 3 | 8 | — | 8 | 10,668,137 |
| 4 | 8 | 44, 68 | 6 | 13,536,792 |
| 5 | 8 | 69 | 7 | 9,777,472 |
| 6 | 8 | 94 | 7 | 9,819,049 |
| 7 | 8 | — | 8 | 11,184,160 |
| 8 | 8 | 109 | 7 | 21,559,000 |
| 9 | 5 | 118, 119 | 3 | 11,655,685 |

## 証明境界

これは69候補のraw sweep完了であって、9件の勝ち証明書完成ではない。今回のmain snapshotにはcost69fの証明書抽出・独立検査の記録がまだないため、9 WIN7-D10をS6 manifestへ加算しない。S6 frontierへの寄与は **0** とする。

claimが明記するcost65j bit113との交差被覆可能性、およびcost68dの未fold証明書を再照合してから、9 rootの証明書抽出順を決める。単純に9件すべてを抽出するとは限らない。

## 現在の勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 2、class 4は引き続き **UNKNOWN**。探索節点数・WIN7-D10件数・S6 manifest被覆数から空盤勝敗を推定しない。

Machine-readable audit: [cost69f sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-sweep-audit-20261115.json)

Raw inputs: `class2-lane-cost69f-raw-batch1..9-20261115.jsonl` and `class2-lane-cost69f-inflight-20261115.json`.
