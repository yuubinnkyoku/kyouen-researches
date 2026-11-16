# 2026-11-16 n11 class2-lane: head-1435 next-target pre-sweep census + cost-64e claim

## 概要

cost-64d fold の着地（head 1419 → 1435、commit `c7a849e0`）に続く次ターゲット選定として、
head 1435 の正確な前提で next-target pre-sweep census を実施し、
class-2 lane プロトコルの 2 親（class-2 target `00000000000000403800000008000000` 18行/1287、
共有親 `00000000000000003800000008002000` 31行/2145）の全 49 残行の
受理・転送・open 候補を D4 canonical root レベルで分類した。
その結果、最安 open 行 `0000000000000000380000000a002000`（cost 64・demand c1=0,c2=2,c4=0）を
cost-64e として claim v1 出版した（60 open bits・4 REFUTED-D10 転送済み）。

11x11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4 はいずれも **UNKNOWN**。

## 実施内容

1. **fold chain 再現**: `recompute_frontier_cost64d_receipts_20261116.py` を runpy 実行し、
   13 reconstruct scripts → head 1410 → 65j fold 1419 → 64d fold **1435/174/6413/507337/4686/371251**
   を全 published assert 付きで再現。fold receipt roots は 735+23=758 receipt（distinct 757・
   D4 canon 743 種）。
2. **lane verdict harvest**: lane output 内の sweep/audit/claim JSON 群から
   **4,122 distinct verdict canon**（WIN7-D10 426・REFUTED-D10 3,696・conflict 0）を構築。
   cost-64d raw batch 8 本と claim v4 の再 parse は 23 WIN/41 REFUTED と bit-exact 一致、
   他 sweep との D4 canon 衝突 0（published 0-conflict census と整合）。
   skip したファイル（証明書 JSON・fold claim など verdict を持たないもの）は全て JSON に記録。
3. **family census（head 1435）**:
   - class-2 target: 1,287 候補出現 → 転送済み canon 26 種（26 出現）→ open 1,261 出現 →
     **distinct open root 1,131**（全体で 156 出現削減、12.1%）。
   - 共有親: 2,145 出現 → 転送済み canon 199 種（247 出現）→ open 1,898 出現 →
     **distinct open root 1,533**（全体で 612 出現削減、28.5%）。
   - **2 行は転送のみで全確定済み**（sweep 不要）: cost-64c STERILE 行
     `00000000000000003800000008002020`（64/64 REFUTED・published verdict と一致、K0863 どおり
     receipt では閉鎖不能）と `00000000020000801202000000200000`（65/65 REFUTED）。
4. **次ターゲット決定**: open bit 数最小の行は共有親の cost-64 行 3 本（各 60 open）で、
   その先頭 `0000000000000000380000000a002000`（stones [13,25,27,59,60,61]）を **cost-64e** として
   claim v1 出版。転送済み 4 bits（70/104/115/119・root canon は census bit table に pin）は
   再実行しない（65j bit-113 と同じ転送規約）。他の in-flight claim（64a 完了済み・76c・69a）は
   全て別 child で競合なし。

## 出版

- `scripts/next_target_presweep_head1435_20261116.py`（git blob `94c89003ab13cdd7d19f87a2d641701de7ce03c2`）
- `output/class2-lane-next-target-presweep-1435-20261116.json`（git blob `5387128c15f630e8fc02a97188d1358554d6c762`）
- `output/class2-lane-next-target-rows-1435-20261116.csv`（git blob `4a0efc808302677cae265d4ae16b547ecb5edb3a`）
- `output/class2-lane-cost64e-inflight-20261116.json`（claim v1）
- 本 log

再実行で出力 JSON/CSV は byte-identical（2 回確認済み）。

## 解釈ガード

- 本 census は探索計画の簿記のみで、engine 探索は 1 bit も実行しておらず、verdict を新規に
  作成してもいない。転送 verdict は published depth-10 engine 結果の D4 canonical root 同一性による
  ものである。
- WIN7-D10 は個別 7 石 root の first-player win（depth 10 以内）のみを証明する。
  REFUTED-D10 は LOSS 証明ではない。STERILE も LOSS 証明ではない。
  solved 1435 は manifest 被覆の簿記である。
- 11x11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4 はいずれも UNKNOWN。

## 追記: cost-64e sweep 完走（同日・同一セッション）

claim v1 出版直後に v16 engine（repo-verbatim `class4_child1_runner_v16.ts`・Node 22）で
60 open bits を 8 batch で完走した。

- **結果: 60/60 REFUTED-D10・WIN7-D10 0件・capped 0件**。事前転送 4 bits（70/104/115/119）
  と合わせ **64/64 candidates REFUTED-D10 → cost-64e 行は STERILE**。
- 総 nodes **39,961,790**（pilots 8×3402 除く）・全 bit terminalStoneRange [13,17]・andclose true。
  heaviest: bit 32（3,279,693）・bit 21（3,270,894）・bit 118（2,185,077）。
- **determinism rerun**: batch2 を再実行し 9/9 行 node-exact 一致
  （`class2-lane-cost64e-v16-determinism-rerun-batch2-20261116.jsonl`・blob `7fa222a6`）。
- **v15 crosscheck**: v15 engine（pilot 5949）で anchors bits 32/0/118 が v16 と双方向一致
  （`class2-lane-cost64e-v15-crosscheck-20261116.jsonl`・blob `bce440b1`）。
- raw batch 1〜8 の git blob pin は claim v2（blob `55c51c92`）に記載。
- **K0863 帰結**: STERILE 行はいかなる WIN7-D10 receipt でも閉鎖不能（自出行・cross-cover
  とも）。よって **head 1435 は不変**（fold する receipt が存在しない）。共有親の実効
  closable demand がこの行ぶん（64 candidates）減る。REFUTED-D10 は LOSS 証明ではなく、
  STERILE 確定も行の勝敗判定ではない。
- 次回はこの 60 root の verdict が harvest に加わった状態で census を再計算すること
  （残り 2 行の cost-64 open 行 `0000000000000080120a000000800000`・
  `00000000000100003800000008080000` との orbit 共有で追加転送が見込める）。

## レジューム

- canonical head **1435**。
- cost-64e（`0000000000000000380000000a002000`）: 60 open bits を v16 engine で sweep
  （8 bits/batch・pilot 3402・cap 10M・determinism rerun・v15 crosscheck）。WIN7-D10 が出たら
  証明書抽出 → fold → census 再計算。REFUTED-D10 は LOSS ではない。
- census のbit table には cost-64e の全 bit の root canon と状態が入っているので、
  sweep 実行時に open 60 bits だけを回せばよい。
- 次の候補行（同 60 open の `0000000000000080120a000000800000`・
  `00000000000100003800000008080000`、ついで 65/61 open の 2 行）も CSV に記載済み。
- 並走の in-flight（76c・69a）の着地監視と、着手前の最新 main 確認を毎回行うこと。
