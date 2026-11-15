# 2026-11-15：cost-84 sterile sweep完了 — 84 REFUTED-D10・WIN7-D10不在・frontier不変・blocker S5連続STERILE 15行目・11×11はUNKNOWN

開始時main: `3c08ca67`（本レーンのcost-84 IN FLIGHT claim直後）。前回のcost-82b STERILE sweep（K0783追記 commit `6b5b30dd`）に続き、best class-4 blocker-candidate S5 `00000000020000003800000080000000`（head 1227で18行/1460）の実際の最安未sweep行 cost-84 **`00000000020000003800000080000400`**（stones [10,31,59,60,61,89]・需要 c1=0,c2=0,c4=3）を取得した。82b完了時点で未sweepは4行（本cost-84行・cost-86行2本・cost-87行）だった。

## claim前検証（head 1227基準）

- `legal_candidates.py`（exact Bareiss・blob `8e97082c…`、cost-70e/82b claimと同一の列挙器）: 84 legal candidates、manifest edge cost 84とbit-exact一致。
- D4 demand検証（exact-integer D4正準化・8要素二面体群）: 子の6個の一石削除を照合 → 開親3個・すべてclass-4（del 10: blocker S5 `00000000020000003800000080000000` 18行/1460〔mask 4〕・del 31: `00000000020000003800000000000400` 88行/7388・del 89: `00000000000000003800000000800001` 85行/7023）・残り3削除（59/60/61）はhead-1227 ranking CSVに不在の閉行 → 需要は c1=0, c2=0, c4=3（head-1227 top-candidates CSV行14のdemand文字列と一致）。c4=3需要のためWIN7が3 class-4フロンティアに同時に効く見込みだった。
- IN FLIGHT claimを先にpush（commit `3c08ca67`）してからsweep着手。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**84/84候補・WIN7-D10 0件・84 REFUTED-D10・0 capped・総nodes 108,689,432**。STERILE（負の実験事実）: 証明書抽出対象なし。raw 13ファイル（batch 1–11・batch5 determinism rerun・v15 crosscheck）を成果物と同時push。

- terminal stone range: **全84候補 [13,17]**（深さ10境界検査合格・distinct_terminal_ranges は1種のみ）。
- 統制: batch 5（bits 44,45,46,48,49,50,53,54）determinism rerunはnode-exact一致（`class4-lane-cost84-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`・pilot 5949）で最重REFUTEDアンカー bits 66/34/86 はloss=false一致（nodes 4,040,549/9,695,280/5,532,140）（`class4-lane-cost84-v15-crosscheck-20261115.jsonl`）。

## 独立監査（全assert合格・2回実行byte-identical）

`audit_cost84_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用・geometry helpersは70d/70e/82b監査から流用）が13 rawファイルから全件再導出: 候補84はclaim列挙とbit-exact・各bit 1回ずつ・batch bits 1-11はengine計画と一致・pilot 3402×11・batch-5再現一致・v15アンカー一致・総nodes 108,689,432がcompleted claimと一致・終局石数range境界検査合格。**一石削除D4正準化6件を監査内で独立再導出**（del 10/31/89の3開親行 18/1460・88/7388・85/7023 と del 59/60/61の閉行を全件照合・head-1227 ranking CSV 175 open・top-candidates CSV需要行と一致）。監査JSON `class4-lane-cost84-sweep-audit-20261115.json`（2回実行byte-identical・md5 `ba408eefa5c70dcf732cbbfbbb0e0709`）。

## 解釈上の注意

REFUTED-D10はLOSS証明ではない。**STERILE: WIN7-D10 receiptが存在しないためfold材料なし**。child `00000000020000003800000080000400` は3開親（blocker S5〔mask 4〕・`00000000020000003800000000000400`〔mask 4〕・`00000000000000003800000000800001`〔mask 4〕）の未解決S6行のまま。この行を反証で閉じるには深さ>10の証拠が必要。**本sweepはheadを変更しない（1227/6620/522561/4890/386284不変）**。

blocker S5の連続STERILE記録は**15行目**（73f/74f/74c/75/79/79b/80/80c/81/82/86a/86b/86c/82b/84）に伸び、未sweepは3行（cost-86 `00000000020000003800100080000000` c4=3・cost-86 `00000000020000003840000080000000` c4=3・cost-87 `00000000020000003800000080000004` c4=3）。いずれもc4=3需要で、次回はcost-86行（2本のうちkanon順で先に来る方）が最安未sweep行。18行すべてがSTERILEでもblocker S5自体は解決しない（各行の反証には深さ>10の証拠が必要）が、depth-10以内に先手勝ちが無いという負の実験事実の蓄積はblocker閉鎖探索の指針となる。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l receipts foldがIN FLIGHT（head 1227基準）で本レーンの3開親と無関係・cost-70eは5 WIN rootsの証明書抽出を並走が進行中（bits 0/8のpart 1/2・2/2をpush済み）で本childと無関係。本sweep（84）はいずれの並走レーンともchild行・親が交差せず衝突していない。

## 成果物

- completed claim: [class4-lane-cost84-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost84-inflight-20261115.json)
- raw batches 1–11・determinism rerun・v15 crosscheck: 同output/ `class4-lane-cost84-raw-batch{1..11}-20261115.jsonl` ほか
- sweep audit: [class4-lane-cost84-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost84-sweep-audit-20261115.json)（再現: [audit_cost84_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost84_raw_sweep_20261115.py)）
