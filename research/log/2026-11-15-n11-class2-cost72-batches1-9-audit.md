# 2026-11-15: class2-lane cost-72 raw batch 1–9の全件監査

## 対象

監査時のmain snapshot: `63a5b2d3d14cbfd8bc4e08fa19ce4fb4e01470b4`。

cost-72の対象はS5 `00000000000000803202000000000000` の六石子 `00000000000000803202000000000200`。claim上の合法七石目は72候補、9 batch、需要は `c1=0,c2=2,c4=0`。候補列は公開済みの `legal_candidates.py` Bareiss列挙とbit単位で一致するとされる。

## 9 raw batchの照合結果

全9 JSONLをclaimのbatch計画と突き合わせた。各batchの8候補bit列は完全一致し、重複・欠落・計画外bitは0。各batchのpilot controlは1件ずつ、全9件が `loss=false, nodes=3402, capped=false` で一致した。

| batch | 候補節点合計 | WIN7-D10 | REFUTED-D10 |
|---:|---:|---:|---:|
| 1 | 5,609,463 | 0 | 8 |
| 2 | 7,088,702 | 0 | 8 |
| 3 | 4,299,396 | 0 | 8 |
| 4 | 10,633,305 | 0 | 8 |
| 5 | 16,244,653 | 1（bit52） | 7 |
| 6 | 5,470,216 | 0 | 8 |
| 7 | 7,258,345 | 0 | 8 |
| 8 | 3,939,222 | 0 | 8 |
| 9 | 9,019,712 | 1（bit111） | 7 |
| **合計** | **69,563,014** | **2** | **70** |

72/72候補、72 bitすべて一意、打切り0。全候補で `andclose=true`、終局石数範囲[13,17]だった。WIN7-D10候補は次の2件。

- bit52：7,498,054節点、root `00000000000000803212000000000200`
- bit111：1,872,720節点、root `00008000000000803202000000000200`

このrunnerの記録規約では `loss=true` がWIN7-D10、`loss=false` がREFUTED-D10。ここで確認したのはraw記録とclaim計画の整合性であり、探索器の判定そのものを別実装で証明したわけではない。合法候補の再列挙も今回の監査範囲外。

## 完了扱いにしない理由

全9 raw batchは揃ったが、claim JSONの `status` は依然 `in-flight`。v15との交差検査、WIN7証明書の抽出・独立検証、完了済みsweep記録はこの監査では確認していない。cost72出力に対応する証明書もまだ確認できていない。したがってbit52/111は探索上のWIN7-D10候補に留まり、S6 manifestの解消数・frontierには **0** として扱う。

機械可読結果：[cost72 batches1–9 audit JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72-batches1-9-audit-20261115.json)。

標準11×11空盤、二石root `{49,60}`、S2 `{59,60}` は **UNKNOWN**。class2/class4も未解決。
