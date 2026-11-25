# 2026-11-15：cost-82b sterile sweep完了 — 82 REFUTED-D10・WIN7-D10不在・frontier不変・blocker S5連続STERILE 14行目・11×11はUNKNOWN

開始時main: `5e1427b6`（本レーンのcost-82b IN FLIGHT claim直後）。**K0783 cost-70d追記の「次の未sweep行はcost-80行2本」は誤りだった**ことが判明した: best class-4 blocker-candidate S5 `00000000020000003800000080000000`（head 1227で18行/1460）のcost-80行2本（`00000000020000003800000180000000` c4=2・`00000000020000003800200080000000` c4=1）は2026-11-14に並走により既にsweep済みで、いずれもSTERILE（cost-80: 80 REFUTED・290,092,122 nodes・cost-80c: 80 REFUTED・220,291,094 nodes）。さらにcost-81（325,836,995 nodes）・cost-82（335,027,684）・cost-86a/b/c（373,903,515/344,931,733/301,085,672）の各行も同日STERILE確定済みで、18行のうち13行までsweep済みだった。本レーンは実際の最安未sweep行 cost-82行2本目 **`00000000020000003800000090000000`**（stones [28,31,59,60,61,89]・需要 c1=0,c2=0,c4=3）をcost-82bとして取得した（cost-82の名前は`...80000800`行の2026-11-14 STERILE sweepが使用済み）。

## claim前検証（head 1227基準）

- `legal_candidates.py`（exact Bareiss・blob `8e97082c…`、cost-70e claimと同一の列挙器）: 82 legal candidates、manifest edge cost 82とbit-exact一致。
- D4 demand検証（exact-integer D4正準化・8要素二面体群）: 子の6個の一石削除を照合 → 開親3個・すべてclass-4（del 28: blocker S5 `00000000020000003800000080000000` 18行/1460〔mask 4〕・del 31: `00000000000000901002000000080000` 88行/6966・del 89: `00000000000000003800000004800000` 87行/6833）・残り3削除（59/60/61）はhead-1227 ranking CSVに不在の閉行 → 需要は c1=0, c2=0, c4=3（head-1227 top-candidates CSVのdemand文字列と一致）。c4=3需要のためWIN7が3 class-4フロンティアに同時に効く見込みだった。
- IN FLIGHT claimを先にpush（commit `5e1427b6`）してからsweep着手。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・11バッチ・pilot 3402×11全PASS）

**82/82候補・WIN7-D10 0件・82 REFUTED-D10・0 capped・総nodes 68,922,913**。STERILE（負の実験事実）: 証明書抽出対象なし。raw 13ファイル（batch 1–11・batch5 determinism rerun・v15 crosscheck）を成果物と同時push。

- terminal stone range: **全82候補 [13,17]**（深さ10境界検査合格・distinct_terminal_ranges は1種のみ）。
- 統制: batch 5（bits 46,49,50,53,54,66,67,69）determinism rerunはnode-exact一致（`class4-lane-cost82b-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`・pilot 5949）で最重REFUTEDアンカー bits 118/7/2 はloss=false一致（nodes 5,796,536/11,259,120/9,262,419）（`class4-lane-cost82b-v15-crosscheck-20261115.jsonl`）。

## 独立監査（全assert合格・2回実行byte-identical）

`audit_cost82b_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用・geometry helpersは70d/70e監査から流用）が13 rawファイルから全件再導出: 候補82はclaim列挙とbit-exact・各bit 1回ずつ・batch bits 1-11はengine計画と一致・pilot 3402×11・batch-5再現一致・v15アンカー一致・総nodes 68,922,913がcompleted claimと一致・終局石数range境界検査合格。**一石削除D4正準化6件を監査内で独立再導出**（del 28/31/89の3開親行 18/1460・88/6966・87/6833 と del 59/60/61の閉行を全件照合・head-1227 ranking CSV 175 open・top-candidates CSV需要行と一致）。監査JSON `class4-lane-cost82b-sweep-audit-20261115.json`（2回実行byte-identical・md5 `e2c64baf6aed371b8c93be5f2981584a`）。

## 解釈上の注意

REFUTED-D10はLOSS証明ではない。**STERILE: WIN7-D10 receiptが存在しないためfold材料なし**。child `00000000020000003800000090000000` は3開親（blocker S5〔mask 4〕・`00000000000000901002000000080000`〔mask 4〕・`00000000000000003800000004800000`〔mask 4〕）の未解決S6行のまま。この行を反証で閉じるには深さ>10の証拠が必要。**本sweepはheadを変更しない（1227/6620/522561/4890/386284不変）**。

blocker S5の連続STERILE記録は**14行目**（73f/74f/74c/75/79/79b/80/80c/81/82/86a/86b/86c/82b）に伸び、未sweepは4行（cost-84 `00000000020000003800000080000400` c4=3・cost-86 `00000000020000003800100080000000` c4=3・cost-86 `00000000020000003840000080000000` c4=3・cost-87 `00000000020000003800000080000004` c4=3）。いずれもc4=3需要で、次回はcost-84行が最安未sweep行。18行すべてがSTERILEでもblocker S5自体は解決しない（各行の反証には深さ>10の証拠が必要）が、depth-10以内に先手勝ちが無いという負の実験事実の蓄積はblocker閉鎖探索の指針となる。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l receipts foldがIN FLIGHT（head 1227基準）で本レーンの3開親と無関係・cost-70eは5 WIN rootsの証明書抽出を並走が進行中（bit66 part 1/2・2/2をpush済み）で本childと無関係。本sweep（82b）はいずれの並走レーンともchild行・親が交差せず衝突していない。

## 成果物

- completed claim: [class4-lane-cost82b-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost82b-inflight-20261115.json)
- raw batches 1–11・determinism rerun・v15 crosscheck: 同output/ `class4-lane-cost82b-raw-batch{1..11}-20261115.jsonl` ほか
- sweep audit: [class4-lane-cost82b-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost82b-sweep-audit-20261115.json)（再現: [audit_cost82b_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost82b_raw_sweep_20261115.py)）
