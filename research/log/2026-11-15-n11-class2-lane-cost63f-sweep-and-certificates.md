# 2026-11-15：cost-63f sweep・WIN7証明書2件出版 — 第2 class-2 target最安行・frontier不変1195・11×11はUNKNOWN

開始時main: `38b0dcda`（chain head 1195/6652/524884/4922/388607 掲載済み・78a監査追記直後）。第3target S5 `00000000000000809102000000000000` の残り3行（69/74/78）はすべて並走in flightのため、自レーンはhead-1195のtop-candidatesで大域最安の未sweep行である **cost-63 child `00000000000080809002000000000800`**（第2 coverable class-2 target S5 `00000000000000801202000000200000` のD4一石lift・stone 79追加）をcost-63fとして取得した。

## claim前検証（head 1195基準）

- `legal_candidates.py`（exact Bareiss）: 63 legal candidates、manifest edge cost 63とbit-exact一致。
- D4 demand検証: 子の6個の一石削除をD4正準化しhead-1195 ranking CSV（175 open S5）と照合 → **開いている親は2個ともclass 2**（第2target 40 orbits/2977〔stone 79削除〕・`00000000000000801202020000000000` 52 orbits/3551〔stone 11削除〕）→ c1=0, c2=2, c4=0。
- 既存cost-63帯（63/63b/63cd/63e/63a）はすべて別child → suffix 63f。兄弟cost-63行 `00000000080000801202000000200000` は未claimのまま別レーン用に残置。
- IN FLIGHT claimを先にpush（commit `30d2dd47`）してからsweep着手。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）

**63/63候補・WIN7-D10 2件（bits 85, 91）・61 REFUTED・0 capped・総nodes 44,140,211**（76aの131M nodesに対し34%）。

- bit85 root `00000000002080809002000000000800`（sweep nodes 1,950,992）
- bit91 root `00000000080080809002000000000800`（sweep nodes 604,700）

統制: batch 6（両WIN7を含む）のdeterminism rerunはloss/nodes/capped/terminal range全一致（`class2-lane-cost63f-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`）でbits 85/91はloss=true（nodes 10,145,295/3,920,892）・refutedアンカーbits 1/7/109はloss=false・pilot 5949×3（`class2-lane-cost63f-v15-crosscheck-20261115.jsonl`）。

独立監査 `audit_cost63f_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が10 rawファイルから全件再導出: 候補63はclaim列挙とbit-exact・各bit 1回ずつ・terminal range [13,17]全件・root == child|1<<bit・D4 canonical重複0（published manifest roots全部との比較込み）。監査JSON `class2-lane-cost63f-sweep-audit-20261115.json`。

## 証明書2件（二重独立検証PASS）

`cert_driver76a.ts`（repo-verbatim・blind kill table pref=null）で全loser初手をchunk抽出しsort -u merge・header 2行付与:

- **bit85**（mobility 51・chunk 3〔18+16+17手〕）: 40,154行・extraction 17,491,560 nodes・fbt_drops 0。BigInt 3×3余因子検査 **PASS**（sub-roots 51/51・union 0/0・terminal [13,17]・winner 57,352・loser 19,083）。Number Bareiss `verify_bit7_win7_cert.ts --root-check --subroots <51手> --consumed-out` **PASS**（consumed union == 証明書行・comm diff 0）。1,449,311 B・単一ファイル（分割閾値1.75 MiB未満）。
- **bit91**（mobility 49・chunk 2〔18+31手〕）: 29,305行・extraction 6,973,105 nodes・fbt_drops 0。BigInt **PASS**（sub-roots 49/49・union 0/0）。Bareiss **PASS**（consumed union一致）。1,058,527 B・単一ファイル。

root D4正準形はbit85 `00000000002080801202000000200000`・bit91 `00000000080080809002000000000800`で相互にdistinct・公開済みmanifest roots（監査スキャン）とも重複0。

最終manifest `class2-lane-cost63f-win7-certificates-20261115.json`: 2/2 WIN7 certified・計69,459行・extraction 24,464,665 nodes・sub-roots 100・terminal 20,962・edges 144,626。claimをcompletedに更新（fold pending）。

## 解釈上の注意

WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明し、63合法手のS6親は閉じない。REFUTED-D10はLOSS証明ではない。**2 receiptのfoldは未実施で、canonical chain head 1195/6652/524884/4922/388607は不変**（foldはhead 1195へのrebase必須）。解消計数はmanifest被覆の帳簿前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 成果物

- IN FLIGHT claim → completed: [class2-lane-cost63f-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63f-inflight-20261115.json)
- raw batches 1–8・determinism rerun・v15 crosscheck: 同output/ `class2-lane-cost63f-raw-batch{1..8}-20261115.jsonl` ほか
- sweep audit: [class2-lane-cost63f-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63f-sweep-audit-20261115.json)（再現: [audit_cost63f_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost63f_raw_sweep_20261115.py)）
- 証明書2本体: 同output/`class2-lane-cost63f-certificates/`（bit85・bit91）
- manifest: [class2-lane-cost63f-win7-certificates-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63f-win7-certificates-20261115.json)
