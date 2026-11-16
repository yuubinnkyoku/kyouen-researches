# 2026-11-16：cost-76d/77e 4-receipt fold（prereg → fold → field-by-field agreement）— head 1450→1452

開始時main: `40d1e16b`（cost-76d/77e fold 事前登録公開後、head 1450/174/6398/506297/4671/370211）。cost-76d レーン（claim v1 commit `99848fd3`、sweep 76/76・WIN bits [19,49]・証明書は dual-verify 済み）と cost-77e レーン（claim v1 commit `e11268da`、sweep commit `35b8ccee`、77/77・WIN bits [37,69]）の全 WIN7-D10 receipt を、事前登録の直後に fold した。

## 事前登録（fold前公開）

fold の計算前に、入力 blob pin・予測head・conflict census・children-open assertion を `class2-lane-cost76d-77e-fold-preregistration-20261116.json`（blob `d150d311…`、commit `40d1e16b`）として公開した。projection tool `fold_projection_head1450_tool_20261116.py`（commit `e97ba632`）・prereg script `preregister_cost76d_77e_fold_20261116.py`（commit `76e7bd8f`）・tool script（commit `f3379398`）も同時公開。fold実行は prereg の全フィールド（head_after 1452/174/6396/506144/4669/370058、receipts・marginals・mim・children_closed_by・parents_after・cost delta・hist delta・conflict census・cross-lane orbit）と一致した。

## fold receipts（公開順、全 WIN7-D10）

| # | lane | bit | root hex | marginal | in-manifest |
|---|---|---:|---|---:|---:|
| 1 | cost-76d | 19 | `00000000040000003800080008080000` | 5 | 1 |
| 2 | cost-76d | 49 | `00000000040000003802080008000000` | 4 | 0 |
| 3 | cost-77e | 37 | `00000000040000809002002000004000` | 6 | 1 |
| 4 | cost-77e | 69 | `00000000040000a09002000000004000` | 4 | 0 |

- 証明書: bit19 44,810行/1,618,698 B（blob `f36ac20a…`）、bit49・bit37・bit69 は sweep record に pinned。sweep規模: 76d 76/76 WIN bits [19,49]（総nodes 96,246,915）、77e 77/77 WIN bits [37,69]（総nodes 116,019,458）。
- child行 `00000000040000003800080008000000` は bit19 で、`00000000040000809002000000004000` は bit37 で閉鎖。
- raw marginal 計19行 / in-manifest 2行。影響を受けた開親は3つ（第二coverable class-2 `00000000000000801202000040000000` 5行/364→3行/211、`00000000000000003800000208000000` 65/5358→64/5282、`00000000000000801202000000040000` 72/5960→71/5883）。行incidence 4、parent edge cost delta 306、demand hist delta c2=2,c4=0 が -2。

## conflict census と cross-lane orbit

771 folded roots（756 distinct D4 canons）との153候補orbit照合で overlap 0。唯一の cross-lane 共有 orbit `00000000040000809002000000004080`（= 76d bit 86 ≡ 77e bit 7）は両sweepで REFUTED-D10、判定一致。

## 新canonical head

**`1452/174/6396/506144/4669/370058`**（solved 1450→1452、unique remaining S6 6398→6396、sum remaining cost 506297→506144、s6 needed 4671→4669、cost needed 370211→370058）。basis 1450 は公開fold JSON（blob `8783993e…` の cost-66c fold を含む764 receipt roots + 498 sweep winners）から独立再構成し、preregのbasis summary と一致。

## 出力（全blob検証済み）

- fold JSON `class-frontier-cost76d77e-receipts-recompute-20261116.json`（blob `8d4bc622…`・12,926 B）
- ranking CSV `class-frontier-s5-ranking-after-cost76d77e-receipts-20261116.csv`（`16e408d5…`・7,535 B・174行）
- top-candidates CSV `class-frontier-top-candidates-s6-after-cost76d77e-receipts-20261116.csv`（`b123801c…`・6,343 B）
- claim更新: cost-76d v1(completed) → v2 fold-complete（blob `ec598676…`）、cost-77e v1(in-flight) → v2 completed+fold（blob `36515c51…`）。v1 blob（`d2e40a3e…`/`1cfa89e5…`）は supersedes に pinned、v1 round-trip は fold script 内で byte-identical 検証済み。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- best fully-sterile class-2 `00000000000000801202000000200000`（3行/209）はreceiptでは閉じられず未解決のまま。best coverable class-2 は `00000000000000801202000040000000`（3行/211）、第二coverable `00000000000000809082000000000000`（10行/698）、次の純粋class-2 sweep target `00000000000000403800000008000000`（18行/1287）、best class-4 `00000000020000003800000080000000`（18行/1460）。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4 は引き続き **UNKNOWN**。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost76d_77e_receipts_20261116.py
```

20 raw batch JSONL（blob-pinned）・v15 crosscheck・77e determinism rerun から両sweepを再導出し、prereg と field-by-field で照合する。全CONTROL pass。
