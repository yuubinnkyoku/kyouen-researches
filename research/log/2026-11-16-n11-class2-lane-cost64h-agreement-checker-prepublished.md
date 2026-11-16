# 2026-11-16：cost64h fold receipt agreement checker を fold receipt 着地前に出版（self-test 18/18 PASS）

cost-65n時の `ace68d90` と同じ運用: 並走セッションのcost-64h fold receipt（23 WIN7-D10 receipt を head 1452 へ fold）が着地したときに備え、**着地前**に機械照合checker `check_cost64h_fold_receipt_agreement_20261116.py` を出版する。checkerは公開済みprereg `class2-lane-cost64h-fold-preregistration-independent-20261116.json`（blob `5074a8a0…`・commit `c64579b4`）の全投影値と、着地したfold record（`class-frontier-cost64h*…json`）を比較する。

## 検査項目（applicableなもの全て）

- C3 投影head 6数値（1472/174/6376/504672/4649/368586）・C4 demand histogram・C5 histogram deltas
- C6 total marginal 111・C7 total mim 20・C8 閉鎖manifest行20行のhex集合・C9 child行の閉鎖
- C13 win bit集合・C16 root hex（child|1<<bit）・C15 conflict census 0・C2b baseline head 1452
- C10/C10b/C11/C12 affected parents（17親）・row incidences 42・edge cost delta 3090
- C14 per-receipt marginal: fold順がpreregの昇順bit順と同一なら全一致を要求し、**異なる順なら per-bit の値比較に切替**（順序依存はpreregの fold_order_note に宣言済み）し、差は実験事実として記録

## self-test

- prereg自身から合成fold recordを構築してcheckerを実行: **18/18 checks PASS**（applicable全て）。
- 逆順fold（receiptsを逆転）でも order-invariant 項目は全PASS・per-bit比較経路がnote付きで動作することを確認済み。
- prereg側の入力はblob pin `5074a8a0…` をassert。

## 補足の整合性確認（本セッション）

- 出版済み23枚の証明書ファイル名（`bit{N}-root-{hex}.cert`）のroot hexがpreregの root=child|1<<bit 計算と**23/23一致**。win23 manifestはfold時のbookkeeping commitで出版される見込み（本log時点で未出版）。

## 信頼境界

- checkerは公開record間の照合のみ。engine searchなし・verdict作成なし。solved はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootから深さ10以内の先手勝ちのみを証明。REFUTED-D10はLOSS証明ではない。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/check_cost64h_fold_receipt_agreement_20261116.py --selftest
# fold receipt 着地後:
python .../check_cost64h_fold_receipt_agreement_20261116.py --fold-json <landed fold json>
```
