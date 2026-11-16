# 2026-11-16：cost-64d sweep完了 — 64候補全走査・WIN7-D10 23・REFUTED 41・capped 0・独立監査PASS・foldは次回・11×11はUNKNOWN

開始時main: `d31f6828`（本レーンのclaim v1 IN FLIGHT + presweep prep出版直後）。本レーンはclaim `class2-lane-cost64d-inflight-20261116.json`（v1）の対象を同一セッションで完走し、claim v2（completed）へ更新した。対象は**class-2 lane最良own-closable S5 `00000000000000403800000008000000`（P・24行/1704）の最安未sweep行**である7石child `00000000000000403800000008002000`（stones [13,27,59,60,61,70]・cost 64・dual class-2需要 {c1:0,c2:2,c4:0}・共有開親 `00000000000000003800000008002000`（42行/2929）側でも未sweep）。presweep prep `prep_cost64d_presweep_20261116.ts`（第4独立実装・候補列挙+parent導出）による事前登録とbit-exact一致。

## sweep結果（8 v16 rawバッチ・全候補完走査）

- **64候補すべて判定・capped 0件**・総nodes **64,291,757**（pilots 8×3402別）。
- **WIN7-D10 23件**: bits [0,1,2,11,16,30,32,43,53,66,69,75,79,86,92,95,98,106,107,109,111,113,120]。
- **REFUTED-D10 41件**（bit 119を含む）。全候補 terminalStoneRange [13,17]・andclose true。
- **determinism rerun**（batch5 bits [80,83,85,86,87,88,89,92]・別プロセス）: node-exact一致。
- **v15交差エンジン一致**: pilot 5949・anchors [2,66,87,92,113] — 4 WIN anchors はloss=true、REFUTED anchor bit87 はloss=false、両方向一致。
- **sweep内orbit確認**: 64候補rootのD4正準形はすべてdistinct・child stabilizer order 1（sweep内重複なし）。

## 独立監査（stdlib第5実装・全control PASS）

`audit_cost64d_raw_sweep_20261116.py`（Python標準ライブラリのみ・exact Bareiss・repo engine不使用）。controls: 独立legal再列挙64候補がclaim `legal_candidates` とbit-exact一致（presweep事前登録にも一致）・batch bit lists 8/8 exact・pilots 3402×8・determinism node-exact・v15両方向一致・全receiptsがchildを被覆・no capped・parentsがhead-1419 ranking CSVとclass/rows/cost一致・child 6石safe。監査JSON `class2-lane-cost64d-raw-sweep-audit-20261116.json`。

## fold-prep marginals（head 1419基準・監査JSON内蔵）

23 WIN7-D10 receipts（一石削除D4正準化）のhead-1419 remaining set（1410 worklist − cost-65j foldで喪失の9行 = 6429行）に対する被覆: **16行閉鎖 → 投影head 1435**。per-parent投影: 共有開親 `00000000000000003800000008002000` 42→31行（cost delta −784）・target S5 `00000000000000403800000008000000` 24→18行（−417）・他11開親が各1–2行喪失（parent-row incidence計30・union 16行）。

## 解釈上の注意

**fold未適用**: 16行閉鎖はmanifest計上前進であり、chain再現（runpy chain reproduction → `recompute_frontier_cost64d_receipts_20261116.py` 新規作成 → 1419 headへのfold → root disjointness検証）を要する。fold着地まで**canonical head 1419/174/6429/508474/4702/372388 不変**（65j precedent: sweep→後日fold）。REFUTED-D10 41件はLOSS証明ではなく該当rootの深さ10内的反証のみ。23 WIN rootsの証明書は未出版（抽出・独立検証が直近の後続作業）。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親は引き続き **UNKNOWN**。

## 成果物

- claim v2: [class2-lane-cost64d-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d-inflight-20261116.json)（v1 commit `d31f6828` をsupersede・全v1欄保存）
- raw batches 1–8: 同output/ `class2-lane-cost64d-raw-batch{1..8}-20261116.jsonl`
- determinism rerun: 同output/ `class2-lane-cost64d-determinism-rerun-batch5-20261116.jsonl`
- v15 crosscheck: 同output/ `class2-lane-cost64d-v15-crosscheck-20261116.jsonl`
- sweep audit: 同output/ [class2-lane-cost64d-raw-sweep-audit-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d-raw-sweep-audit-20261116.json)（再現: [audit_cost64d_raw_sweep_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost64d_raw_sweep_20261116.py)）
