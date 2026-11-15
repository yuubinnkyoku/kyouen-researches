# 2026-11-15：cost-74f sterile sweep完了 — 74 REFUTED-D10・WIN7-D10不在・frontier不変1216・class-4 frontierで2行連続STERILE・11×11はUNKNOWN

開始時main: `cf32a4ea`（K0783のcost-73f追記着地直後）。head-1216のtop-candidatesで、**best class-4 blocker S5 `00000000020000003800000080000000`（18 orbits/1460・head-1045以来不変のclass-4 bottleneck）の最安未sweep行 cost-74 child `00000000020000003800000080000020`**（stones [5, 31, 59, 60, 61, 89]）をcost-74fとして取得（cost-73f〔同S5のcost-73行〕は直前実行でSTERILE閉じ・cost-74a–74eは他行で使用済み）。**class-4 frontier行の2度目のsweep着手**。

## claim前検証（head 1216基準）

- `legal_candidates.py`（exact Bareiss）: 74 legal candidates、manifest edge cost 74とbit-exact一致。
- D4 demand検証（exact-integer D4 canonicalization・8要素二面体群）: 子の6個の一石削除を照合 → 開親3個（lift 5: best blocker `00000000020000003800000080000000` 18/1460〔classes_bitmask 4〕・lift 31: `00000000000000801082000000080000` 79/6036〔**mask 5 = class-1+4混合**〕・lift 89: `00000000000000003800000000800020` 69/5346〔mask 5〕・残り3削除（lift 59/60/61）はhead-1216 ranking CSVに不在の閉行）→ maskビットごと需要 c1=2, c2=0, c4=3（head-1216 top-candidates CSVの当該行のdemand文字列と一致）。**本行は2個のmask-5開親を持ち、class-1需要も同時に運ぶ**（73fは純粋class-4需要3だったのと対照的）。
- IN FLIGHT claimを先にpush（commit `4bc32165`）してからsweep着手。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**74/74候補・WIN7-D10 0件・74 REFUTED-D10・0 capped・総nodes 59,017,987**。STERILE（負の実験事実）: 証明書抽出対象なし。raw 12ファイル（batch 1–10・determinism rerun・v15 crosscheck）は即時push済み（commit `04a781f5`）。

- terminal stone range: **全74候補 [13,17]**（深さ10境界検査〔[0]≥7・[1]≤17〕合格・`distinct_terminal_ranges` に記録。73fのbits 40/66のような早期終端行は今回はなし）。
- 統制: batch 6（bits 77–84）determinism rerunはnode-exact一致（`class2-lane-cost74f-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`）でアンカーbits 3/53/118はloss=false（nodes 4013034/4710260/1989273・pilot 5949）（`class2-lane-cost74f-v15-crosscheck-20261115.jsonl`）。

## 独立監査（全assert合格・2回実行byte-identical）

`audit_cost74f_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が12 rawファイルから全件再導出: 候補74はclaim列挙とbit-exact・各bit 1回ずつ・pilot 3402×10・batch-6再現一致・v15アンカー一致・終局石数range境界検査合格。**一石削除D4正準化6件を監査内で独立再導出**（lift 5/31/89の開親とlift 59/60/61の閉行を全件照合）。監査JSON `class2-lane-cost74f-sweep-audit-20261115.json`（再実行byte-identical・md5 `d697aa06059fb6a3a4ba84b93ccbd875`）。

## 解釈上の注意

REFUTED-D10はLOSS証明ではない。**STERILE: WIN7-D10 receiptが存在しないためfold材料なし・canonical chain head 1216/6631/523382/4901/387105は不変**。child `00000000020000003800000080000020` は3開親（best blocker〔mask 4〕と2個のmask-5行）の未解決S6行のまま（best blocker 18行/1460・mask-5親 79/6036・69/5346はすべて不変）。この行を反証で閉じるには深さ>10の証拠が必要。

**best class-4 blocker S5の最安2行（cost-73・cost-74行）が連続STERILE**となり、「class-4 frontier行では深さ10以内の先手勝ち材料が稀」という作業仮説が強化された。class-4 blocker閉鎖には、残り16行のsweep継続に加えて深さ>10探索か構造的議論が必要になる可能性が高い（観測ベースの仮説であり結論ではない）。class-4 frontierの次候補は同S5の2番目のcost-74行 `00000000020000003800000088000000`（c1=0,c2=1,c4=2）とcost-75行 `00000000020000003800020080000000`（c1=0,c2=0,c4=3）。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l（WIN7 bits 21/48・証明書・extraction summary出版済み・foldは未着地）・cost-67c（WIN7 bits 64/96・証明書manifest出版済み・foldは未着地）・cost-78a（bits 8/29/109）・cost-69g/65j/74e は並走in flightで、本sweepはこれらと衝突していない（着手前に最新mainのclaim一覧を確認済み）。それらのfoldはすべてfold時点のcanonical headへのrebase必須。

## 成果物

- completed claim: [class2-lane-cost74f-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74f-inflight-20261115.json)
- raw batches 1–10・determinism rerun・v15 crosscheck: 同output/ `class2-lane-cost74f-raw-batch{1..10}-20261115.jsonl` ほか（commit `04a781f5`）
- sweep audit: [class2-lane-cost74f-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74f-sweep-audit-20261115.json)（再現: [audit_cost74f_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74f_raw_sweep_20261115.py)）
