# 2026-11-16 n11: cost69aのD4 verdict-cache再利用 — 69候補中3候補を既知REFUTED-D10へ移送

## 開始状態

- 開始時の最新main: `cbfa5fc881b14b66e9a7c050b8e7e5ead0c872ca`
- 作業中の最新main: `b936f71f750b6985e09735462adbead2735bb340`
- canonical frontier head: **1410/174/6438/509109/4711/373023**（不変）
- 対象child: cost69a `00000000000000801222000000800000`
- legal S7候補: 69

## 発見

公開済みD4 verdict-cache scanの対象entryは次の通り:

- 8,964個の7石root verdict（REFUTED-D10 8,305 / WIN7-D10 659 / capped-unknown 0）
- 新規転送115件はすべてREFUTED-D10、WIN7-D10転送0
- 同一位置のcross-sweep一致1,782組、矛盾0
- 第二独立検証は入力1,279ファイルを再hashし、46比較全一致・全115転送の正準形同一性を再検証してVERIFICATION PASSED

cost69a childのentryは legal 69、engine verdict 0、D4 cache transferによるREFUTED-D10がbits **55 / 65 / 109**、未確定engine候補が**66**。bit109だけでなくbit55・bit65も既存verdictから決まる。

### bit 55

- cost69a候補root: `000000000000008012a2000000800000`
- canonical root: `000000000000008012a2000000800000`
- source: cost64c child `00000000000000003800000008002020` のbit103
- source root: `00000080000000003800000008002020`
- source sweep: 64/64 REFUTED-D10、capped 0
- source canonical rootがcost69a bit55と一致するためREFUTED-D10を転送

### bit 65

- cost69a候補root: `00000000000000821222000000800000`
- canonical root: `00000000000000809082200080000000`
- 同じsource root `00000000000000809082200080000000` が二つの独立sweepに存在:
  - cost58 child `00000000000000809082000080000000` のbit45、1,628,004 nodes、REFUTED-D10
  - cost61c child `00000000000000809082200000000000` のbit31、1,628,004 nodes、REFUTED-D10
- 同じ7石rootの両sweep判定が一致し、cost69a bit65へREFUTED-D10を転送

### bit 109

- 既存claimの記録を維持。cost69a bit109は65k bit75・74h bit97の自出行候補rootとD4同値で、K0863のSTERILE行定理と両own-row sweepからREFUTED-D10。
- このbitは二つのSTERILE行を閉じるWIN7 receipt候補ではない。

## 反映

claim `class2-lane-cost69a-inflight-20261116.json` を更新:

- `precomputed_candidate_bits = [55,65,109]`
- `engine_candidate_bits` を66件に限定
- `planned_batches` から3bitを除外（合計66件）
- bit55・bit65のsource root、canonical root、sweep出典を `canonical_cache_transfers` に記録
- 既存bit109のK0863導出は `theorem_derived_verdicts` に保持

更新commit: `b936f71f750b6985e09735462adbead2735bb340`

## 解釈境界

これは7石rootの個別REFUTED-D10判定をD4正準形で再利用したもの。**LOSS証明ではない**。WIN7 receiptは増えておらず、manifest行の閉鎖もない。canonical head 1410は不変。

cost69aの残り66候補は未探索扱いのまま。raw batchはまだ出版されていない。長時間sweepを起動した事実はない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1/class2/class4はいずれもUNKNOWN。**

## 次

1. 66候補だけをdepth-10 engineでsweep。
2. WIN7-D10が出た場合のみcertificateを再構築し、独立検証。
3. 証明書検証後に限りhead 1410とのfoldを行う。
