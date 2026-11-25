# 2026-11-18 N11 5-parent joint cover拡張（commit 3a04ca5b）の第三実装クロスチェック

## 成果

並走が出版した「5 cheapest parentのjoint certificate-cover共有分析の拡張」（commit `3a04ca5b`・script `joint_parent_cover_sharing_cost16_20261118.py`・output blob `40581746`・91 checks all PASS・blossom 3000グラフself-test）を、**アルゴリズムクラスが完全に独立した第三実装で全31 subsetについて検証**した。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/crosscheck_joint_cover_cost16_third_20261118.py`
- output: 同dir `output/joint-cover-cost16-third-impl-crosscheck-20261118.json`
- 19 checks all PASS・三重実行byte-identical（sha256 `2961e7dd…`）・実行2.75秒/回。

## 手法（出版blossomとの独立化）

1. **Tutte行列ランク法（代数的・blossom系と無関係）**: max matching = rank(T)/2。歪対称Tutte行列 T[a][b]=v, T[b][a]=−v を2つの素体 GF(1000000007) / GF(998244353) で独立な決定的LCG乱数評価してrankを計算（Schwartz-Zippel 誤り確率 << 1/p・2素体一致で照合）。500個の決的小グラフでbrute-force max matchingと全一致のself-testつき。
2. **2^r exact最小cover DP（組合せ的・matchingを一切使わない）**: r ≤ 18 の2 subset（11行・18行）で出版witness size・Gallai恒等式（最小cover = r − m）の両方を独立に確認。
3. **全31 subsetのfield完全比較**: rows_union・candidates・distinct_roots・span_histogram・maxspan・lower_bound・max_matching・witness_size・exact・cross_parent_roots・sum_individual_costs・sharing_benefit・witness本数の全fieldが出版outputと一致（31/31・不一致0）。
4. **全31 witnessの独立妥当性検証**: 相異・universe所属・被覆union==全行・本数==r−m。
5. universe再構成はpinned入力（worklist・census・ledger・cover表・JSONL pin `89b24065`・4-parent既出版output pin）から独立実行。cheapest-5選定・target互いに素（112行）・4-parent出版15 subset size再現も検証。

## 主要結果

- **5-way joint headline独立確認**: 112行・joint exact cost 56（個別総和58・benefit 2）・exact。cost-16単体16 exact。**joint計画のbenefit 2はcross-parent root 2本（span-2）による偶奇億却で、4-parent時代のbenefit 1から増えたが、58本中2本（3.4%）の節約にとどまる**。per-parent優先順位付けはjoint計画下でもほぼ保存されるという出版結論を第三実装も支持。
- Tutte rank法と出版blossomのmax_matchingは**全31 subsetで完全一致**（r=11〜112）。
- 出版blossomの3000グラフself-testに加え、本クロスチェックの代数的評価が全実subsetで組合せ的結果と一致したことで、**min-cover = r − max_matching（Gallai）の適用は二重に独立に確認**された。

## 解釈上の注意

joint cover costは「選ぶrootが全てcertificateとして検証される」ことを前提にした計画算術である。sharing benefitは計画数であってWIN/REFUTEDの主張ではない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
