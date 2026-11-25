# 2026-11-18 N11 cost-16 parent rank-28 構造preread — 8番目の行18ハブroot (18,20)・行20初被覆・b_only quint 331本・disjoint quad 22本

本logはk=27本計算出版（result JSON commit `9b804a9c`・JSONL commit `d43eb059`・crosscheck commit `7f5053be`）に続き、k=28の構造prereadを独立導出・機械検証したものである。**prereadは最小cover計画のban組合せ構造のみを扱い、k=28の包含除外Pm joint計算もゲームverdictも含まない。生存曲線は被覆計画数であって探索コストでもverdictでもない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。**

script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_survival_k28_preread_20261118.py`（入力は3つのpinned JSONのみ: phase-B aggregate blob `31bdefdb…`・k26 JSON blob `1841a281…`・k27 JSON blob `3dc30ad6…`。Pm engineを呼ばない）。

## rank-28 root の確定（構造）

1. **rank-28 root = `(18,20)`**（root hex `00000000000000801202050000001000`・zero-based index 27）。**8番目の行18ハブroot**（先行27 rootのうち**14本**が行18を被覆）で、**行20はこのrootで初被覆**（行18と異なる第2ハブ行の開口）。
2. m28 = 120,361,466,461,719,625（A_part = 92,220,460,659,557,047 / B_part = 28,141,005,802,162,578・membership A+B恒等式確認済み）。※この段階ではm28はaggregateの被覆計画数であり、kill(28)は未計算。

## 新規ban組合せcensus（index 27を含む新規ban組合せ20,853本 = C(27,1)+C(27,2)+C(27,3)+C(27,4) をmap/masks両分類器で二重分類・不一致0）

| size | total (=C(27,s−1)) | b_only | zero | disjoint |
|---|---|---|---|---|
| pair | 27 | 14（shared・行18） | 0 | 13 |
| triple | 351 | 214 | 99 | 38 |
| quad | 2,925 | 626 | 2,277 | **22** |
| quint | 17,550 | **331** | 17,219 | 0 |

3. **disjoint quad 22本**、全レコード `|rows_union| = 8` を確認（disjoint quad累積は255 → 277見込み・k=28本計算で確定）。
4. **b_only quint 331本**: 二重行ヒストグラム {行15: 38 / **行18: 255** / 行19: 38}。4-subset profile分布は**331本すべて 3/2/0**（各b_only quintの5個の4-subsetのうち b_only 3・disjoint 2・zero 0）で、k27（309本すべて3/2/0）と同一のプロファイルを維持。disjoint quintは引き続き0本。
5. 全C(28,5)=98,280 census = b_only **2,512** / zero 95,768 / disjoint 0。**prev層差分解釈でk=27出版censusと厳密一致**: 2,512 − 331 = 2,181・95,768 − 17,219 = 78,549（= pinned k27 JSON b_only/zero）。全C(28,3)=3,276 census = b_only 2,009 / zero 727 / disjoint 540 も記録。
6. disjoint-partner法則の観点: rank-28も**行18ハブ型**（pair shared 14 / disjoint 13・k27と同じ「ハブ带でdisjoint殺し+sharedペアのjoint激減」の署名）。rank-28 rootのmarginal がm28の50%前後のハブ帯に留まる予測をk=28本計算で検証する。

## rank-27回帰（出版値の独立再検証・本prereadの追加価値）

k=28のcensus計算と同じ分類器をrank-27に再適用し、**k=27出版values層（26 pairs・325 triples・2,600 quads・309 b_only quintsの全レコードclass）と全点一致**を確認:

- 新26 pairs = shared 13 / disjoint 13・新325 triples = b_only 201 / zero 86 / disjoint 38・新2,600 quads = b_only 588 / zero 1,990 / disjoint 22・新309 b_only quint（zero 14,641 = 14,950 − 309）。
- 全C(27,3)=2,925 = b_only 1,795 / zero 628 / disjoint 502・全C(27,5)=80,730 = b_only 2,181 / zero 78,549 / disjoint 0。二重行ヒストグラム {15: 417, 18: 1,354, 19: 410}。
- **新規層b_only二重行ヒストグラムの出版分割独立検証**: k27出版全hist − k26出版全hist = 新層hist（{15: 38, 18: 233, 19: 38}・総和309一致）を、本scriptのrank-27新規census histが再現。
- rank-27 root (12,18)・root hex `00000000000100003820000008001000` もaggregateから再確認。

すなわちk=27出版は、本prereadの独立実装（zone: 組合せ分類のみ・joint計算なし）によっても構造面が全面的に再現された。

## 検証（21 checks all PASS・実行1.3秒）

`top50_has_50_rows`・`top50_root_keys_unique`・`every_top50_root_covers_two_distinct_valid_rows`・`rank27_new_and_full_census_match_published_k27`・`rank27_two_classifiers_agree_on_new_and_full_regressions`・`rank27_root_matches_published_anchor`・`rank28_root_and_rows_match_preread_target`・`rank28_two_classifiers_agree_on_all_20853_combinations`・`rank28_combination_totals_match_binomial_counts`（[27, 351, 2925, 17550] = C(27,1..4)）・`rank28_new_pair_census_14_shared_13_disjoint`・`rank28_new_triple_census_214_99_38`・`rank28_new_quad_census_626_2277_22`・`rank28_disjoint_quad_census_has_22_complete_eight_row_unions`・`rank28_b_only_quint_census_has_331_records`・`rank28_b_only_quint_double_row_histogram_matches`・`rank28_all_b_only_quints_have_three_b_only_two_disjoint_four_subsets`・`rank28_has_no_disjoint_quints`・`rank28_new_row_overlap_signature`（row18 prior hits 14 / row20 prior 0）・`rank28_full_quint_census_prev_layer_equals_published_k27`・`rank28_full_triple_census_recorded`・`rank28_membership_ab_split_recorded`。

census総数は全てmath.comb機械導出と一致。分類器は行リスト集計（classify_map）とbitmask演算（classify_masks）の2実装で20,853本全組合せを二重判定し不一致0（rank-27回帰の新規17,901本 + 全C(27,3)=2,925 triples + 全C(27,5)=80,730 quints = 101,556本も同様に不一致0）。

## 運用・次ステップ

- 出力JSON: `output/cost16-survival-k28-preread-20261118.json`（schema `n11-cost16-k28-preread-20261118-v1`・99,765B・21 checks）。
- k=28本計算はk27 script（60,132B）からの機械変換で着手予定。変換チェックリスト（k27 log記録の「prev欄は追加前の数・stored累積はload時実数カウント」）を適用し、load時staged assertで段取り違いを自動検出する。
- crosscheckのn=28拡張は`a4c`（anchor4 combo数）・kind期待値表・K28 pinの追加のみで対応可能（`_k{n}`接尾辞・math.comb導入済み）。
- rank-29..32 rootは(0,16)・(14,19)・(18,26)・(15,23)（既刊preread）で、本k28層はその前提を崩さない。

## 11×11空盤の現況（interpretation guard）

標準11×11空盤は**UNKNOWN**。本prereadの数値は全て「61,381標準盤の部分扭矩として同型な31行cost-16 parentの最小cover構造」であり、ban survival・kill比・membership数のいかなる値もゲームの勝敗や探索難度を意味しない。
