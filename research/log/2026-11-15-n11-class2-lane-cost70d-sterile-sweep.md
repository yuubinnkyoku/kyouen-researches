# 2026-11-15：cost-70d sterile sweep完了 — 70 REFUTED-D10・WIN7-D10不在・frontier不変・11×11はUNKNOWN

開始時main: `bb44940e` 直前の`cea4143d`（cost-69h receipts fold head 1221/6626/523035/4896/386758着地直後）。head-1221のtop-candidatesで、**第二coverable class-2 target S5 `00000000000000801202000000200000`（31行/2334）の最安未sweep行 cost-70 child `00000000000000801282000000200000`**（stones [21,49,55,57,60,71]）をcost-70dとして取得。code searchでcost-70行5本（同S5の `…02000000200004`・`…02000002200000`・`…1282000000200000`・`…841202000000200000`・`…0100809002000000000800`）すべてがcandidate CSV上のリストアップのみで未着手であることを確認済み。本行は**5本のcost-70行で唯一のclass-1需要持ち（c1=1,c2=1,c4=0）**で、WIN7が出ればclass-2（31/2334）とclass-1（75/5971）の2フロンティアに同時に効く。claim名cost-70dはcost-70/70b/70cが他childで使用済みのため。

## claim前検証（head 1221基準）

- `legal_candidates.py`（exact Bareiss）: 70 legal candidates、manifest edge cost 70とbit-exact一致。
- D4 demand検証（exact-integer D4 canonicalization・8要素二面体群）: 子の6個の一石削除を照合 → 開親2個（lift 55: 第二coverable S5 `00000000000000801202000000200000` 31/2334〔mask 2〕・lift 57: class-1 S5 `00000000000000801082000000200000` 75/5971〔mask 1〕）・残り4削除（lift 21/49/60/71）はhead-1221 ranking CSVに不在の閉行 → 需要は c1=1, c2=1, c4=0（head-1221 top-candidates CSVのdemand文字列と一致）。class-1親は69h foldの両開親（class-2）と無関係で不変。
- IN FLIGHT claimを先にpush（commit `bb44940e`）してからsweep着手。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・9バッチ・pilot 3402×9全PASS）

**70/70候補・WIN7-D10 0件・70 REFUTED-D10・0 capped・総nodes 53,890,941**。STERILE（負の実験事実）: 証明書抽出対象なし。raw 11ファイル（batch 1–9・batch5 determinism rerun・v15 crosscheck）は即時push済み（commit `eaacea59`）。

- terminal stone range: **全70候補 [13,17]**（深さ10境界検査合格・distinct_terminal_ranges は1種のみ）。
- 統制: batch 5（bits 52/54/67/72/73/74/75/76）determinism rerunはnode-exact一致（`class2-lane-cost70d-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`）でアンカーbits 4/92/114はloss=false（nodes 5,681,888/9,924,059/6,397,886・pilot 5949）（`class2-lane-cost70d-v15-crosscheck-20261115.jsonl`）。

## 独立監査（全assert合格・2回実行byte-identical）

`audit_cost70d_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が11 rawファイルから全件再導出: 候補70はclaim列挙とbit-exact・各bit 1回ずつ・pilot 3402×9・batch-5再現一致・v15アンカー一致・終局石数range境界検査合格。**一石削除D4正準化6件を監査内で独立再導出**（lift 55/57の開親とlift 21/49/60/71の閉行を全件照合）。D4重複走査は公開win7証明書manifest 56ファイル・canonical roots 138個と比較して重複0。監査JSON `class2-lane-cost70d-sweep-audit-20261115.json`（再実行byte-identical・md5 `a1739c77c0125dc7180abde83c01aa61`・commit `e306f6a1`・`24e0e552`）。

## 解釈上の注意

REFUTED-D10はLOSS証明ではない。**STERILE: WIN7-D10 receiptが存在しないためfold材料なし**。child `00000000000000801282000000200000` は2開親（第二coverable S5〔mask 2〕とclass-1 S5 `00000000000000801082000000200000`〔mask 1〕）の未解決S6行のまま。この行を反証で閉じるには深さ>10の証拠が必要。**本sweepはheadを変更しない**。

## head分岐の指摘（本sweepと無関係だが記録）

本claimのhead参照（1221/6626/523035/4896/386758・69h fold head）の時点で、並走cost-78a fold head `1225/6622/522699/4892/386422`（commit `1691d9bb`・03:07:50Z着地）が既にmainに存在していた。両foldは同一baseline head 1219から並行着地しており、**canonical chainが78a分岐（1225）と69h分岐（1221）に分かれたまま**（両head JSON・ranking CSV・top-candidates CSVがmainに併存）。本sweepはSTERILEでfold材料を持たず、どちらのchainとも交差しない（70d child行は両chainで開行・70dの2開親は78a foldの影響を受けない: 78a head 1225 rankingでは32/2403と75/5971）。**次のfold実行者は78a（1225）と69h（1221）のマージrecompute（両fold receiptsを単一chainに再適用）が必須**。上位互換の正しいheadは両fold取り込み後の値（solved 1225+2=1227から交差被覆を引いた値）となるはずで、着手前に再計算されたい。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l（fold待ち）・cost-78a（証明書5/5・fold 1225着地）・cost-69h（claim v2→v3・fold 1221着地）は並走レーン。本sweep（70d）はこれらとchild行が異なり衝突していない。claim先行push・着手前の最新main再取得・STERILE確定後の即時closure（commit `e306f6a1`）を実施。

## 成果物

- completed claim: [class2-lane-cost70d-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70d-inflight-20261115.json)
- raw batches 1–9・determinism rerun・v15 crosscheck: 同output/ `class2-lane-cost70d-raw-batch{1..9}-20261115.jsonl` ほか（commit `eaacea59`）
- sweep audit: [class2-lane-cost70d-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70d-sweep-audit-20261115.json)（再現: [audit_cost70d_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70d_raw_sweep_20261115.py)）
