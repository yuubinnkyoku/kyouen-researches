# 2026-11-16：cost64h v15 REFUTED クロスチェック（`ae7e583709`）を第二実装で独立検証（41/41 + win controls node-exact）

並走セッションが13:57:39Zに出版した cost-64h **v15 REFUTED クロスエンジン検査**（shard a-e + verification record `cc410c88…`・commit `ae7e583709`）を、第二実装レーンが独立再導出して機械照合した。

## 独立検証の内容（`verify_cost64h_v15_refuted_crosscheck_independent_20261116.py`）

出力: `class2-lane-cost64h-v15-refuted-crosscheck-independent-agreement-20261116.json`（blob `77ed1808…`・2回実行でbyte-identical）。

- **C1/C2**: shard 5ファイル + verification record + claim v2 + raw batch 8本 + v15 win crosscheck の計16ファイルを git blob sha で pin 検証。
- **C3**: published v16 raw batch から REFUTED 41 bit 集合を再導出（WIN 23 bit 集合も一致）。
- **C4**: shard 内容: 41 REFUTED bit すべて loss=false・uncapped・andclose=true・terminal range 13-17・pilot_d6 は 5/5 とも 5949 nodes・bit 重複なし・bit 集合は「41 REFUTED + {4, 120}」と厳密一致。REFUTED node sum **57,767,631**、コントロール込み合計 **66,159,887**。
- **C5**: WIN コントロール bit 4/120 は出版済み v15 win crosscheck と node-exact（3,555,878 / 4,836,378）。
- **C6**: 出版 verification record の 8/8 checks が true・per-bit 41/41 の verdict+node agreement・win_control_detail も再導出値と完全一致。

## 意義

cost-64h sweep の 23 WIN + 41 REFUTED 計 64 bit 全てが v16/v15 両エンジンで verdict 一致したことになる（WIN 23 は `0d32c2a0…`、REFUTED 41 は本record、win controls は node-exact で接続）。fold receipt 着地前の状態として、sweep 全体の二重検証が完成した。

## 信頼境界

- 照合のみ。engine search なし・verdict 作成なし。REFUTED-D10 は LOSS 証明ではなく、v15/v16 の depth-10 前提の verdict 一致を意味するのみ。WIN7-D10 証明書は個別7石rootから深さ10以内の先手勝ちのみを証明する。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost64h_v15_refuted_crosscheck_independent_20261116.py
# ALL CONTROLS PASS / 出力は2回実行でbyte-identical
```
