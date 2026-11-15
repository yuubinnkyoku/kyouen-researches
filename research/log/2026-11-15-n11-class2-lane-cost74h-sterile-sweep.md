# 2026-11-15：cost-74h sterile sweep完全着地 — 第二coverable class-2 target S5の最安未sweep行child `00000000000000889002000000000800`（74候補exactly-once・WIN7-D10 0件・74 REFUTED-D10・0 capped・総nodes 72,720,136）・実行中sandbox環境リセット越しの決定性再検証・11×11はUNKNOWN

対象行: 2-way merged canonical head **1270**（`class-frontier-merged-cost65l-74g-recompute-20261115.json`・blob `02109530`）基準で、**第二coverable class-2 target S5 `00000000000000801202000000200000`**（17行/1325）の cost-74 行child **`00000000000000889002000000000800`**（stones [11,49,60,63,67,71]）。claim `class2-lane-cost74h-inflight-20261115.json` をpushしてからsweepした。

## demand（head 1270で再導出・検証済み）

6石それぞれの1石削除のD4正準化（8要素二面体群・最小ビットパターン）で6個のS5軌道のうち、**child行を保持する開親は2つ**: `00000000000000801222000000000000`（75行/5705・lift石11）と第二coverable class-2 target `00000000000000801202000000200000`（17行/1325・lift石67）。残り4削除軌道は閉行。per-mask-bit demand は **c1=0, c2=2, c4=0**（両開親とも純class-2需要）。このchildは第二targetの最安未sweep行（cost-65兄弟 `00000000020000801202000000200000` はcost-65kでsterile sweep済み・cost-65兄弟 `00000000220000003800000000000200` はcost-65l fold済み・cost-70兄弟 `00000000000000801282000000200000` はcost-70dでsterile sweep済み）。合法候補74個はclaim列挙と独立Bareiss 4x4列挙（`legal_candidates.py`）でbit-exact一致。

## sweep実行と着地

- **74候補をexactly-once列挙・探索**（10バッチ・pilot 3402×10・総nodes **72,720,136**・全terminal range [13,17]）。
- 判定: **WIN7-D10 0件・74 REFUTED-D10・0 capped** — child `00000000000000889002000000000800` は**sterile**。headは不変（sweep単独ではS6軌道を閉じずfrontier計数を変えない）。
- raw batches 1-10をpush、**determinism rerun**（batch5 bits [48,54,58,59,62,64,65,66] を同一v16 runnerで再実行・node-exact一致）。
- **v15 crosscheck**: 交差エンジンでWIN判定一致・refutedアンカー [0,2,62,86,87]（nodes 1,779,947/2,720,409/12,542,999/11,025,261/14,940,722・pilot 5949×3・3回のforeground実行）。**bit 1は本childでは不合法**（Bareiss-unsafe・claim列挙に不含）。当初74gのアンカー0/1/2を流用しかけたが、合法アンカーのみに修正して実行した。audit script内でanchor合法性（claim列挙への所属）をassert。
- audit script `audit_cost74h_raw_sweep_20261115.py` 全統制PASS（all_bits_exactly_once・terminal range bounds・pilot 3402×10・independent_enumeration_matches_claim・one_stone_deletion_d4_canonicalization_verified・total_nodes_match）・**2回実行byte-identical**（sweep audit JSON md5 `acd1b1c86daab4096bc4d079bbad26df`）。claim独立監査は `audit_cost74h_claim_independent_20261115.mjs` / `cost74h-claim-independent-audit-20261115.json`。
- claim `class2-lane-cost74h-inflight-20261115.json` は **completed**（sweep_results: 74候補・win7_d10_bits []・refuted 74・capped 0・nodes 72,720,136・pilots 10）へretire済み。
- commit `6fac1e3e`（15ファイル・remote raw CDN cmp照合OK）。

## sandbox環境リセット越しの決定性再検証

sweep実行中に**sandbox環境リセットが発生しローカルmirrorが全消滅**した（未pushのraw 12ファイルを含む）。これに対し:

1. 10バッチ+determinism rerunを**同一分割で再生成**した。
2. 消失前の集計（74候補・0 WIN7・74 REFUTED・0 capped・72,720,136 nodes・10 pilots at 3402）と**node-exactに全件一致**を確認した。

同一コード・同一分割が**環境をまたいで一致して再現する**ことが実験事実として記録された（auditの`post_reset_note`にも記載）。今後もraw成果物は生成後できるだけ早くpushする（再発対策）。

## 判定の意味

REFUTED-D10は「深さ10以内に先手WIN7証明書が存在しない」ことのみを意味し、**LOSS証明ではない**。sterile行は当該6石child配下の7石rootsの深さ10以内の先手勝ち証明が存在しないことを意味する。solved数の増減はmanifest被覆の簿記であり勝敗ではない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4はすべてUNKNOWN。**

## 成果物

- audit script: [audit_cost74h_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74h_raw_sweep_20261115.py)
- sweep audit JSON: [class2-lane-cost74h-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74h-sweep-audit-20261115.json)
- claim独立監査: [cost74h-claim-independent-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost74h-claim-independent-audit-20261115.json)
- retired claim: [class2-lane-cost74h-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74h-inflight-20261115.json)
- raw batches 1-10・determinism rerun・v15 crosscheck（同dir・`class2-lane-cost74h-*_20261115.jsonl`）
