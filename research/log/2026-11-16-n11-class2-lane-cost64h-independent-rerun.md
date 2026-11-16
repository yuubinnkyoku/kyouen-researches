# 2026-11-16：cost64h sweep の独立全量再実行検証 — 64/64 bit node-exact（pilot 8/8・総nodes 47,017,565・23 WIN7-D10 / 41 REFUTED-D10 / 0 capped）

開始時main: cost64h fold prereg（`c64579b4`）着地直後。並走セッションが出版したcost-64h sweep（child `00000000000000403800000008100000`・64候補・depth 10・cap 1e9・claim v2 blob `68e48780…`）を、**この環境でrepo-verbatim runner v16（blob `0a4a86f6…`）により全64 bitをバッチ分割どおり完全再実行**し、出版raw batch 1-8（claim v2のblob pin全てと照合済み）と全フィールド（wall-clock `ms` を除く）を比較した。

## 結果

- **64/64 bit node-exact一致・不一致0**（bit・loss・nodes・capped・terminalStoneRange・andclose全て）。pilot_d6 control 8/8（loss=false・nodes=3402）。
- **総nodes 47,017,565**（claim v2 `node_sum_v16` と完全一致・再実行合計も同一）。
- verdict再現: **WIN7-D10 23 bits [4,6,8,33,38,42,44,49,68,74,76,77,78,79,83,89,91,101,109,113,114,116,120] / REFUTED-D10 41 / capped 0**。WIN bit集合はclaim v2の `win7_d10_bits` とbit-exact一致（検証JSON checks C1-C9全PASS）。
- 再実行は4並列・2 wave（各バッチ1分未満）。engine起動は `--cap 1000000000` を明示（CLI default 950000のまま実行するとcapped誤判定になる既知の落とし穴）。

## 意味

- 65n（`0c237017`・59/59）・66c（`42788a0d`・59/59 + cap-raise再現）と同じ形式の**第三の全量独立再実行検証**。並走のv15 crosscheck（23 WIN bitsのみ）・determinism rerun（一部batch）・stdlib audit（出版値の再導出）を補完し、**41 REFUTED-D10 bitを含む全64 verdictが fresh environment からの独立再実行で node-exact に再現**された。
- fold receipt（head 1452への23 receipt fold・prereg `5074a8a0…` で投影済み）の入力verdictは全てこの検証で強化された。

## 出版

- 再実行raw batch 8本: `class2-lane-cost64h-independent-rerun-batch{1..8}-20261116.jsonl`（blob pinsはverification JSONに記載・batch1 `fdc379cf…` 等）。
- 検証JSON: `class2-lane-cost64h-independent-rerun-verification-20261116.json`（blob `17ab4b4b…`・35,914 B・per-bit全比較・checks C1-C9・byte-identical再実行確認済み）。
- 検証script: `verify_cost64h_independent_rerun_20261116.py`（blob `5dcbb174…`・両batch集合を読み全フィールド比較・assert内蔵）。

## 信頼境界

- 本検証はdepth-10 capped searchの再実行であって、出版verdictを超えた新規verdictは作らない。node-exact一致は「同じ決定的engine・同じ入力」の再現性の確認（engine自体の健全性はpilot control・v15/v16 cross-engine一致・証明書の独立検証が担う）。
- WIN7-D10証明書は個別7石rootから深さ10以内の先手勝ちのみを証明。REFUTED-D10はLOSS証明ではない。
- solved（head 1452・投影1472を含む）はmanifest被覆の簿記。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
for i in 1..8: node --experimental-strip-types scripts/class4_child1_runner_v16.ts \
  --child 00000000000000403800000008100000 --bits <batch i bits> \
  --depth 10 --cap 1000000000 --andclose 1
python scripts/verify_cost64h_independent_rerun_20261116.py
```
