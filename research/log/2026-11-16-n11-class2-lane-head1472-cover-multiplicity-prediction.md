# 2026-11-16：head-1472 cover-multiplicity監査の事前予測（fold receipt着地前にpreregistered）— basis 775→798・covered 1452→1472・marginal 20 全assert成立

開始時main: `cfc9cf18`。cost64h fold receiptはまだmainに着地していないが、prereg（`5074a8a0…`・第二実装laneが12/12で独立同意済み・commit `0330d83d`）が投影head 1472/174/6376/504672/4649/368586を確定済みであり、23 WIN7-D10証明書rootは本日4実装で独立検証済み。よって**fold receipt着地後に実施されるhead-1472 cover-multiplicity監査の予測値を、着地前にpreregistered predictionとして出版**した（head-1441版監査 blob `fbafd1e1` と同一のsemantics）。

## 手法

- head-1441監査scriptの抽出semanticsをverbatimで再実装: base 27 WIN7証明書file群 + 103 class-frontier JSON + 6 recompute file群からreceipt roots basisを再構成。
- **basisがhead-1452状態であることをassert**: receipt roots **775**・solved（winners 498 ∪ covers）のmanifest被覆 **1452**。両方ともpreregのbasis_headと一致。
- 23 cost64h WIN root（child `00000000000000403800000008100000` | 1<<bit・全rootがbasisに非存在をassert）を追加し、**covered 1472**（prereg投影と一致）・**marginal in manifest 20**（prereg `total_marginal_in_manifest` と一致）をassert。
- multiplicity histogram・single-cover orbits・per-root exclusive contribution をhead-1441監査と同じ定義で測定。

## 予測値（fold receipt着地後の監査が再現すべき値）

- head control: basis **775→798**・covered **1452→1472**・winners 498・marginal in manifest **20**。
- multiplicity histogram（manifest orbits）: mult_1 **577**・mult_2 **215**・mult_3 **89**・mult_4 **51**・mult_5 **25**・mult_6 **18**・mult_7 **11**・mult_8 **7**・mult_9 **9**・mult_10 7・mult_11 2・mult_12 5・mult_13 1・mult_14 4・mult_15 2・mult_16 1・mult_17 3・mult_18 3・mult_19 2・mult_20 1・mult_23 2・mult_24 1・mult_29 2・mult_33 1・winner_only 433（合計1472）。
- single-cover orbits **577**（cost_sum **42,817**）・exclusive contributionを持つroot **463**。
- per-receipt: 全23 rootがchild orbitそのものをmarginal cover（root=child+1石なので自明に整合）。cost64h root由来の新規marginal manifest orbitsは child 00000000000000403800000008100000 のほか 00000000000000003800100008100000 / 00000000000000103800000008100000 / 00000000000000503800000008000000 / 00000000000000c09002000004000000 / 00000000000000801206000000000080 / 00000000000020003800000008100000 / 00000000000040003800000008100000 / 00000000000080003800000008100000 / 0000000000000080120a000000001000 / 00000000000000801206000000080000 / 00000000020000003800000008100000 / 00000000020000403800000000100000 / 00000000000080809002000000100000 / 00000000020000809002000000100000 / 00000000000000801202000000001200 / 00000000000020809002000000100000 / 00000000000000801242000000001000 / 00000000000000849003000000000000 / 00000000000000801202000000001400 の20行（preregのclosed rowsと一致）。

## 意味

- fold receiptが着地しhead 1472監査が実行されたら、この予測JSONと照合できる。**一致すればfoldと監査の双方がpreregの時点で確定していたことの確認**となり、不一致は実験事実として記録される。
- single-cover 571（head-1441）→577・exclusive roots 460→463: cost64h foldで**単一被覆のmanifest orbitが6増加**（20新規被覆のうち14は既存receipt・winnerとの重複）。被覆冗長性の監査指標としては、foldは被覆を単調に増やすが単一被覆も増やす（専属証明依存が少し増える）ことが定量的に確認された。

## 出版

- script: `scripts/cover_multiplicity_audit_head1472_prediction_20261116.py`（basis assert内蔵）。
- 予測JSON: `output/class2-lane-head1472-cover-multiplicity-audit-prediction-20261116.json`。

## 信頼境界

- 予測はprereg（blob pin `5074a8a0…`）と本日出版の23証明書4実装検証の上に成り、**fold receiptそのものはまだ検証対象になっていない**（着地後にagreement checker `check_cost64h_fold_receipt_agreement_20261116.py` が比較する）。solved はmanifest被覆の簿記であり勝敗の確定ではない。REFUTED-D10はLOSS証明ではない。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
python scripts/cover_multiplicity_audit_head1472_prediction_20261116.py
```
