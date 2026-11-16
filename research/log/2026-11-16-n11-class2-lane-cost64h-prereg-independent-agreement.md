# 2026-11-16：cost64h fold pre-registration を第二実装で全項目独立再導出し完全合意（12/12 field groups）

cost-65n/66c/64g と同じ第二実装プロトコルに従い、並走セッションが出版した cost-64h fold **pre-registration**（`class2-lane-cost64h-fold-preregistration-independent-20261116.json`・blob `5074a8a0…`・commit `c64579b4`・13:43:18Z）を、**fold receipt 着地前**にこの環境で全項目独立再導出して機械照合した。本レーンは cost-64h sweep の実行・証明書抽出・prereg 作成のいずれにも関与していない（second-implementation lane）。

## 独立検証の内容（`verify_cost64h_prereg_independent_agreement_20261116.py`）

全入力をblob pin検証してから再導出した。出力: `class2-lane-cost64h-prereg-independent-agreement-20261116.json`（blob `9ab473ac…`・2回実行でbyte-identical）。

- **C1/C2**: このレーンが消費する入力17ファイル + 証明書directory 87ファイル全てを git blob sha で pin 検証（directory listing は commit `0fc0b9e2` 時点の87件と厳密一致）。
- **C3**: basis 771 roots/756 canons + 76d/77e の4 receipt から canonical head 1452（1452/174/6396/506144/4669/370058）を完全再現。fold JSON `8d4bc622…` の frontier_after とも一致。
- **C4**: raw batch 8本から sweep 集計を再導出: **23 WIN7-D10 / 41 REFUTED-D10 / 0 capped・node sum 47,017,565・pilot 8/8 (3402 nodes)**。v15 cross-engine check（pilot 5949・node sum 55,171,821・23 WIN bits loss=true）も再確認。published full re-run record（9/9 checks true）とも一致。
- **C5**: published rerun record `17ab4b4b…` の全チェックが true であることを確認。
- **C6/C7**: 23枚の WIN7 証明書を byte 検証（md5/sha256/git blob sha）し、header・root行・sorted-unique戦略行・行数・root mobility（exact-integer Bareiss enumerator による独立再計算）を検証。21 bit は出版済み BigInt record（union 0/0・subroots=mobility・rows=nRows）・Bareiss record（stones 7・loserMobility=mobility・rows=nRows・per-move stats）と、6 bit は第三検証 record `caba78da…` とも一致。
- **C10**: **bit 116/120 は main 上に BigInt/Bareiss record が未出版**（bit 120 は extraction summary も未出版。local mirror は404プレースホルダーだったため削除し記録）のため、出版済み独立 BigInt verifier `62b5d941…` を byte-faithful に取得してローカルで実行し **両方 verified**（116: 51 subroots・32,382 rows・union 0/0。120: 58 subroots・52,213 rows・union 0/0・terminal range 13-17）。証拠: `class2-lane-cost64h-bit116-120-local-bigint-verification-20261116.json`（blob `500e8ce7…`）。これは main の出版欠損ではなく本レーンの補完証拠として出版。
- **C9**: conflict census を独立実行: 64 candidate D4 orbit と fold 済み 760 canon の重複 **0**・23 WIN canon pairwise distinct・child は両 class-2 parent で open（census bit table の root_canon も64/64再導出一致）。
- **C11**: 23 receipt fold projection（昇順bit順）を head 1452 frontier verbatim セマンティクスで独立計算し、prereg と **12/12 field groups 完全合意**: receipts 23件（marginal 計111・mim 20）・projected head **1472/174/6376/504672/4649/368586**・histogram deltas・affected parents **17**（row incidences **42**・edge cost delta **3090**）・閉鎖 manifest 20行のparent map・child は **bit 4** で閉鎖。

## 意義

prereg が着地前検証済みであることにより、receipt 着地後の整合 checker（`637c2e98` で prepublished）での不一致が発生した場合、**fold application 側**に原因を切り分けられる。65n/66c で確立した prereg→receipt→agreement 二重記録の cost-64h 版が完了した。

## 転記事実

- 証明書出版順序の番号異常（「4/23」commit が存在しない・bit33 が「23/23a」・bit120 が「23/23」）は実験事実として前回記録の通り。
- `win_roots_d4_self_canonical` は bool ではなく per-root dict（10/23 root が自己標準形でない）であった点を訂正記録。

## 信頼境界

- 本検証は公開 record 間の照合と証明書の独立検証のみ。engine search なし・verdict 作成なし・行は1行も閉じていない。23-receipt fold は receipt 着地と再計算までは **projection**。solved は manifest 被覆の簿記であり勝敗ではない。WIN7-D10 証明書は個別7石rootから深さ10以内の先手勝ちのみを証明し、REFUTED-D10 は LOSS 証明ではない。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost64h_prereg_independent_agreement_20261116.py
# ALL CONTROLS PASS / 出力は2回実行でbyte-identical
```
