# 2026-11-15：cost-74h sterile sweep完全着地 — 74候補exactly-once・WIN7-D10 0件・74 REFUTED-D10・0 capped・総nodes 72,720,136・実行中sandbox環境リセット越しの決定性再検証・11×11はUNKNOWN

開始時点: cost-74h claim（`class2-lane-cost74h-inflight-20261115.json`）はIN FLIGHT、raw batchesは未完。fork 1257（cost-73h・head 6583/519287/4856/383880…と同一時点の共通fork）配下のclass2-lane sweepとして実施。

## sweep実行と着地

- **74候補をexactly-once列挙**（claim列挙とaudit scriptで二重照合）。全terminal range [13,17]・pilot 3402×10・総nodes **72,720,136**。
- 判定: **WIN7-D10 0件・74 REFUTED-D10・0 capped** — cost-74h child `00000000000000809142000000000000`（第三target S5のcost-74行・c1=0, c2=1, c4=0）は**sterile**。
- raw batches 1-10をpush、**determinism rerun**（batch5を同一分割で再実行・node-exact一致）、**v15 crosscheck**（合法アンカー [0,2,62,86,87] 全loss=false・pilot 5949×3）を実施済み。
- audit script `audit_cost74h_raw_sweep_20261115.py` 全統制PASS・**2回実行byte-identical**（audit JSON md5 `acd1b1c86daab4096bc4d079bbad26df`）。
- commit `6fac1e3e`・15ファイルremote raw CDN cmp照合OK。
- claim `class2-lane-cost74h-inflight-20261115.json` は **completed (STERILE)** へretire済み。

## bit 1の不合法とv15アンカー修正

cost-74h childのbit 1は**Bareiss-unsafe**であり、claim列挙にも含まれない。初期に74gのアンカー0/1/2と混同してv15 crosscheckのアンカーに含めた状態があったが、**合法アンカー [0,2,62,86,87] のみに修正**して実行した。audit script内でanchor合法性をassertしている（`set(anchors) ⊆ claim列挙`）。

## sandbox環境リセット越しの決定性再検証

sweep実行中に**sandbox環境リセットが発生しローカルmirrorが全消滅**した（未pushのraw 12ファイルを含む）。これに対し:

1. 10バッチ+determinism rerunを**同一分割で再生成**した。
2. 消失前の集計（nodes・terminal range・判定別件数・pilot件数）と**全件一致**を確認した。

結果として、同一コード・同一分割が**環境をまたいでbyte-identical級の再現性を持つこと**が実験事実として記録された。今後もraw成果物は生成後できるだけ早くpushする（再発対策）。

## 判定の意味

REFUTED-D10は「深さ10以内に先手WIN7証明書が存在しない」ことのみを意味し、**LOSS証明ではない**。sterile行は当該6石child配下の7石rootsの深さ10以内の先手勝ち証明が存在しないことを意味する。solved数の増減はmanifest被覆の簿記であり勝敗ではない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4はすべてUNKNOWN。**

## 成果物

- audit script: [audit_cost74h_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74h_raw_sweep_20261115.py)
- audit JSON: [audit_cost74h_raw_sweep_20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/audit_cost74h_raw_sweep_20261115.json)
- retired claim: [class2-lane-cost74h-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74h-inflight-20261115.json)
- raw batches 1-10（`output/cost74h_raw_batch_{1..10}_20261115.json`）・determinism rerun・v15 crosscheck（同dir）
