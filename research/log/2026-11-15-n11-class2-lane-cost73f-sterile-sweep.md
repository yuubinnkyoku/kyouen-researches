# 2026-11-15：cost-73f sterile sweep完了 — 73 REFUTED-D10・WIN7-D10不在・frontier不変1216・11×11はUNKNOWN

開始時main: `cd652009`（並走レーンのcost-63g fold完了でchain head **1216/6631/523382/4901/387105** 掲載済み・cost-67c sweep audit 67/67直後）。head-1216のtop-candidatesで、**best class-4 blocker S5 `00000000020000003800000080000000`（18 orbits/1460・head-1045以来不変のclass-4 bottleneck）の最安未sweep行 cost-73 child `000000000200000038000000c0000000`**（stones [30, 31, 59, 60, 61, 89]）をcost-73fとして取得（cost-73a–73eはaudit-blocked class-2 S5 `00000000000000809082000000000000` の別行で使用済み）。**class-4 frontier行への初のsweep着手**（近年のレーンはすべてclass-2 target行）。

## claim前検証（head 1216基準）

- `legal_candidates.py`（exact Bareiss）: 73 legal candidates、manifest edge cost 73とbit-exact一致。
- D4 demand検証: 子の6個の一石削除をexact-integer D4 canonicalizationで照合 → 開いている親は3個ともclass 4（best blocker `00000000020000003800000080000000` 18/1460〔stone 30削除〕・`00000000020000003800000040000000` 85/6497〔stone 31削除〕・`00000000000000003800000001800000` 77/5548〔stone 89削除〕・残り3削除はhead-1216 ranking CSVに不在の閉行）→ c1=0, c2=0, c4=3（head-1216 top-candidates CSVの当該行と一致）。
- IN FLIGHT claimを先にpush（commit `f391d736`・remote blob sha `ecfc38be…` 照合済み・1回のfast-forward競合は同内容retryで解決）してからsweep着手。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**73/73候補・WIN7-D10 0件・73 REFUTED・0 capped・総nodes 51,522,112**。STERILE（負の実験事実）: 証明書抽出対象なし。

- terminal stone range: 71候補は [13,17]、bits 40/66は [11,17]（早期終端を含む正当値。監査assertは深さ10境界検査〔[0]≥7・[1]≤17〕で `distinct_terminal_ranges` に記録）。
- 統制: batch 6（bits 76,77,78,79,80,81,82,83）determinism rerunはnode-exact一致（`class2-lane-cost73f-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`）でアンカーbits 3/32/116はloss=false（nodes 7881598/1751024/1696566・pilot 5949）（`class2-lane-cost73f-v15-crosscheck-20261115.jsonl`）。

## 独立監査（全assert合格・2回実行byte-identical）

`audit_cost73f_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が12 rawファイルから全件再導出: 候補73はclaim列挙とbit-exact・各bit 1回ずつ・pilot 3402×10・batch-6再現一致・v15アンカー一致・終局石数range境界検査合格。監査JSON `class2-lane-cost73f-sweep-audit-20261115.json`（再実行byte-identical・md5 `b65cdf28f5575fa69537546c6de22ef3`）。

## 解釈上の注意

REFUTED-D10はLOSS証明ではない。**STERILE: WIN7-D10 receiptが存在しないためfold材料なし・canonical chain head 1216/6631/523382/4901/387105は不変**。child `000000000200000038000000c0000000` は3開親（すべてclass-4）の未解決S6行のまま（best blockerは18行/1460不変）。この行を反証で閉じるには深さ>10の証拠（73個の7石root各々について深さ>10の反証または不変量）が必要。代わりに同一class-4親の他の子行からのWIN7 receiptのfoldで閉じることもできる。class-4 frontierの次候補は同S5のcost-74行 `00000000020000003800000080000020`（c1=2,c2=0,c4=3）ほか。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l（WIN7 bits 21/48・証明書出版中）・cost-67c（WIN7 bits 64/96・sweep audit出版済み・証明書待ち）・cost-78a（証明書bits 8/29/109抽出中）・cost-69g/65j/74e はいずれも並走in flightで、本sweepはこれらと衝突していない（着手前に最新mainのclaim・commitを確認済み）。それらのfoldはすべてfold時点のcanonical headへのrebase必須。

## 成果物

- completed claim: [class2-lane-cost73f-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73f-inflight-20261115.json)
- raw batches 1–10・determinism rerun・v15 crosscheck: 同output/ `class2-lane-cost73f-raw-batch{1..10}-20261115.jsonl` ほか
- sweep audit: [class2-lane-cost73f-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73f-sweep-audit-20261115.json)（再現: [audit_cost73f_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost73f_raw_sweep_20261115.py)）
