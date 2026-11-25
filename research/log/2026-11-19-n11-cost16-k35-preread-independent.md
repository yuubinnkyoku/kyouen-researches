# 2026-11-19 N11 cost-16 k35 preread 独立検証script出版 — rank-35全層を第二導出系列で機械検証（rank35 target・rank34/rank33回帰・meta・era鎖 計30 checks）

## 位置づけ

rank-35 preread（`90fc51c9`・JSON blob `490fa3a00b8e0b19229c94aa6b1aba4a5604ec13`）は第二導出系列（TSミラー・2回の独立導出）との全欄一致検証済みで、続けて rank-36 preread（`67985e92`・JSON blob `760aa396…`）が出版された。本出版は **k=32〜k34 と同じ独立検証script様式の k=35 版**: preread scriptを一切importせず、pinned aggregateから独立に書いた行多重分類器で全構造欄を再導出し、出版preread JSONの各欄と機械照合する第三の検査点。k34版（commit `a450e366`）からの機械変換: 対象層を rank35 に、回帰層を rank34_regression + rank33_regression に、era鎖を k32→k33→k34→k35 に組み替え。k31 result fetch・rank32_regression 層は対象prereadの範囲外のため削除。

## 出版物

1. **script**: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost16_k35_preread_independent_20261118.py`（29022B・git blob `74fdb5d1411c8a7fca9980286e20d25fa7a8f4e5`・基底k34版 blob `50087af38741d0c8d6d54235ecd7d6117b0d6776` からの機械変換）。入力pinは agg（`31bdefdb…`）+ k33 pre（`e4346ddd…`）+ k34 pre（`8dbb1bcb…`）+ k35 pre（`490fa3a0…`）の4点。

## 構成（30 checks）

- **meta (3)**: check_count=33/all_pass/schema `n11-cost16-k35-preread-20261119-v1`・宣言input pin一致（aggregate/k33 pre/k34 pre の3点）・UNKNOWN免責の存在。
- **rank35層 (12)**: root `00000000000000801202090000001000` 行[18,21]・membership 120,058,481,266,728,720 = A 92,036,253,749,417,268 + B 28,022,227,517,311,452（split恒等+aggregate一致+literal）・prior hits {18: [1,4,5,6,7,11,12,18,19,20,21,23,24,26,27,30]（16-sharer hub）, 21: []（行21初被覆）}・4新層census {16 shared/18 disjoint}・{348/133/80}・{1,612/4,289/83}・{1,595/44,781/0}（b_only quint二重行hist {15:177, 16:33, 18:1,112, 19:273}・drop-one profile 1,595本全 {3/2/0}・行21は二重行にならない）・disjoint quad 83本全union 8・**累積 1,195/1,112/966 を C(35,4)/C(34,4)/C(33,4) 全件再計数**・full C(35,3)=6,545 {3,970/1,257/1,318}・full C(35,5)=324,632 {14,599/310,033/0} で era接続 14,599−1,595=13,004（出版k34 pre rank34欄一致）・sextet C(35,6)=1,623,160 all zero・raw JSON exact整数。
- **rank34回帰層 (7)**: 出版k35 pre の rank34_regression 欄を機械再導出と、出版k34 pre rank34層（st34pre）の両方で照合。root (9,19)・membership 120,079,520,746,539,458・prior hits {9:[21], 19:[0,2,3,8,9,10,15,29,32]}・4新層 {10/23}・{326/77/125}・{1,944/3,366/146}・{2,171/38,749/0}・full C(34,3)/C(34,5)/C(34,6)・era vs 機械導出k=33層（quint 13,004−2,171=10,833・triple 3,622−326=3,296）・classifier_comparisons 1,676,081。
- **rank33回帰層 (7)**: 同様に rank33_regression 欄と出版k33 pre rank33層（st33pre）を二重照合。root (7,19)・prior hits {7:[20], 19:[0,2,3,8,9,10,15,29]}・4新層 {9/23}・{304/67/125}・{1,827/2,987/146}・{2,036/33,924/0}・full C(33,3)/C(33,5)/C(33,6)・era vs 機械k=32層（quint 10,833−2,036=8,797・zero 226,503−33,924=192,579）・classifier_comparisons 1,391,808。
- **era鎖 (1)**: k32→k33→k34→k35 の b_only 連続性（quint 8,797→10,833→13,004→14,599・triple 2,992→3,296→3,622→3,970）。

## 実行記録・正直な位置づけ

- 本scriptの照合対象30 checkの全literal値は、第二導出系列（TSミラー）の確定値と出版preread JSON実欄で突合済み（rank35 target facts は本日2回の独立導出、rank34/rank33回帰層は k36 preread 出版サイクルで再照合済み）。
- **Python実行による30 checks評価・byte-identical確認は実行環境障害（bash/Python 実行不能・約2週間継続）により未実施**。環境復旧後の最初のランで本scriptを実行し、30 checks 0 failuresとunknown_status出力を確認する（失敗した場合は直ちにerratumとして記録）。
- rank-36 preread JSONの inputs.k35_preread_independent_verification 欄の「not yet published」記述は本出版以前の状態説明であり、以後は本コミットが後続出版物。
- 本出版は **cover-plan組合せ数の構造検証のみ** であり、勝敗に関するverdictは何も生成しない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。**

## レジューム

1. **k=35本計算**（最重要・着手前に必ず最新mainで出版有無を確認〔毎時並走〕）: k34出版script（blob `de2675b…`・commit `f097e6a3`）からの機械変換。k34 result JSON pin（`d485914cf7f6198a2fbb05b09d778ecec510343f`・commit `b64d8fe1`）・k35 pre pin（`490fa3a0…`）・本script pin（`74fdb5d1411c8a7fca9980286e20d25fa7a8f4e5`）を前提に、rank-34回帰assertと rank-35事実のliteral差し替え（行21初被覆・pair 16/18・triple {348/133/80}・quad {1,612/4,289/83}・quint {1,595/44,781/0}・b_only quint累積14,599・disjoint quad累積1,195）。
2. **k36/k35 preread script・k35独立検証scriptのPython実行**（上記未実施・環境復旧後最初に実施・出版JSON sha256照合（k36 pre JSON: sha256 74254b7b 参照 log））。
3. rank-37 rootはtop50 index 36で未確定（次回preread時に機械確定）。
