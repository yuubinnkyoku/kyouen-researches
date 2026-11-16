# 2026-11-16：cost-64h fold preregistration（独立投影）— 23 WIN7-D10 receipt を head 1452 へ fold した場合の投影 head 1472/174/6376/504672/4649/368586 を fold receipt 着地前に出版

開始時main: `3b1b0fe7`…の前の cost64h 証明書群着地時点（cost-64h claim v2 `68e48780…`・head 1452/174/6396/506144/4669/370058・fold receipt 未着地）。並走セッションがcost-64h（純粋class-2 target `00000000000000403800000008000000` の最安行 child `00000000000000403800000008100000`・64候補）のsweepを完走し（**23 WIN7-D10 / 41 REFUTED-D10 / 0 capped**・claim v2）、23枚のWIN7証明書を出版済み。claim v2は「receipt fold onto head 1452 は次の公開ステップ（別recompute script + prereg）」と明記しており、本preregは**そのfold receiptが着地する前に**独立実装で投影を固定するものである（cost-65n prereg blob `da2b2292` と同じ位置づけ）。

## 手順

1. 入力を全てblob検証: head-1450 projection tool（blob `49fcd8ae…`）が再宣言する133 basis JSON + 3 gz + 6 MS5 manifest part + cost-66c fold JSON（`8783993e…`）はtool再実行で全pin再assert。cost-76d/77e fold JSON（`8d4bc622…`）・head-1452 presweep census JSON（`0d9a94a2…`）・cost-64h claim v2（`68e48780…`）を個別blob検証。
2. basis独立再構成: 764 roots（head-1444）→ +7（66c receipts）→ 771 → +4（76d bits 19/49・77e bits 37/69）→ **775 roots / 760 distinct D4 canons**。frontier summaryが head 1452/174/6396/506144/4669/370058・demand histogram（c2=2,c4=0が797→795等）を公開値どおり再現することをassert。
3. 23 receipt rootsを claim v2 の `win7_d10_bits`（昇順）から child|1<<bit で再導出。各rootが7石であること・**D4 canonがcensus bit-tableのroot_canonと23/23一致**すること・760 folded canonsと重複0（conflict census）・23 canons pairwise distinct をassert。
4. 23 receiptsをclaim記載順（昇順bit順）で独立実装のfold semantics（covers=D4 deletion canons・marginal/marginal-in-manifest）でfoldし、投影head・histogram deltas・affected parentsを計算。**3回実行でbyte-identical**（md5 `ad874bbb…`）。

## 投影結果（foldがこのとおり着地する場合の予測値）

- **投影head: 1472/174/6376/504672/4649/368586**（solved +20・unique_remaining_s6 −20・sum_remaining_cost −1472・s6_needed_by_open_classes −20・cost_needed −1472）。
- **total marginal 111 / marginal-in-manifest 20**（manifest行20行閉鎖）。child `00000000000000403800000008100000` は**bit 4のreceipt（fold順最初）で閉鎖**。
- histogram deltas: `c2=2,c4=0` −17・`c2=2,c4=2` −2・`c2=0,c4=2` −1（他バケット不変）。
- affected parents **17親 / row incidences 42 / edge cost delta 3090**。主なところ: P `00000000000000403800000008000000`（純粋class-2 target・18行/1287）は**18→12行**（child + 5 collateral: `…00503800000008000000`・`…80801206000000000080`・`…80801206000000080000`・`…00849003000000000000`・`…00c09002000004000000`）、第2class-2親 `00000000000000003800000008001000` 45→31行（14行閉鎖と最大）。
- per-receipt marginal（昇順fold順・順序依存）: mim>0は15 receipts（bits 4,44,68,74,77,78,79,83,89,91,101,109,113,116,120）。bit 89がmim 3、bits 68/77/89/116がmim 2、他1。**totals・投影head・hist deltas・affected parents・閉鎖行集合は順序不変**（prereg JSONのfold_order_note参照）。

## fold receipt 着地時の検証プロトコル

並走のfold receipt（recompute script + fold JSON + claim v3）着地時に、本prereg（blob `5074a8a0…`）と以下を照合する: (1) 投影head 6数値・demand histogram、(2) total marginal / total mim・閉鎖manifest行20行のhex集合、(3) affected parents 17親のrows_before/after・lost rows・edge cost、(4) per-receipt marginal（fold順がpreregと異なる場合は順序不変量のみ照合し、差は実験事実として記録）、(5) conflict census 0・children-closed-by-bit。**不一致があれば実験事実として記録し、foldの前提・双方の実装を検査する。**

## 信頼境界

- 本preregは公開receiptに対するbookkeeping投影のみ。engine searchなし・verdict作成なし・行閉鎖なし。foldはmanifest被覆の帳簿であって勝敗判定ではない。
- WIN7-D10証明書は個別7石rootから深さ10以内の先手勝ちのみを証明。REFUTED-D10はLOSS証明ではない。
- solved 1452（投影1472を含む）はmanifest被覆の簿記。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/preregister_cost64h_fold_independent_20261116.py
```

出力: `output/class2-lane-cost64h-fold-preregistration-independent-20261116.json`（blob `5074a8a0…`・24,965 B）。実行時間1秒未満・3回実行byte-identical確認済み。
