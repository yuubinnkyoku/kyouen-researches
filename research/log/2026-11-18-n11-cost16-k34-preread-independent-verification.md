# 2026-11-18 N11 cost-16 rank-34 prereadの第二独立導出検証 — 30 checks 0 failures・rank34新層 + rank33/rank32回帰の機械再導出全一致・k31→k34 era連鎖の4.rank拡張

## 位置づけ

commit `2a14f351` で出版された rank-34 cost-16 構造preread（Python exact-int script `cost16_survival_k34_preread_20261118.py` + preread JSON 33 self-checks・git blob `8dbb1bcbdaed9bee475f3b95932d35a9500e62cb`）は出版時点では単一実装系統の自己検査のみであった。本検証はk=34本計算の入力基盤を独立検証可能にするため、**preread scriptを一切importしない新規実装の行多重分類器**で、pinned入力（phase-B aggregate `31bdefdb…`・k31 result `0d9f67ee…`・k32 preread `6d49ab5b…`・k33 preread `e4346ddd…`・k34 preread `8dbb1bcb…`、いずれもgit blob sha1照合・jsdelivr mirror + raw fallback・fail-loud）から全構造項を機械再導出した。rank-34 prereadのrank32/rank33回帰層は「出版k=32/k=33 preread JSONに対する回帰」として書かれているため、本検証は各回帰値を**出版k=32/k=33 preread JSONの該当欄とfield-by-fieldで直接照合**する3系統構成（個別機械再導出・k34 preread回帰欄・先行出版欄）とした。

## 検証script

`research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost16_k34_preread_independent_20261118.py`（27,689B・git blob `50087af38741d0c8d6d54235ecd7d6117b0d6776`・sha256 `e06b9d5019567adeb08d8bfd6c51683a279ccffb450f45eba1b0ab714f9b72a5`）。k32/k33版検証script（`45596e44…`/`93c130999…`）と同一様式（分類器・census・pin取得機構は新規実装）。`--local DIR` オフラインモード対応（pinned sha1照合は常時）。

## 30 checksの層構成と結果

**network mode・local modeともに 30 checks 0 failures**（local 約5.8秒・network 約6.5秒）。二重実行byte-identical、両モード間の出力一致も確認。

1. **meta層 (3)**: check_count=33・all_pass=true・schema名 `n11-cost16-k34-preread-20261118-v1`・prereadが宣言する入力pin 4件（aggregate/k31_result/k32_preread/k33_preread）が既知pinと一致・`unknown_status` がUNKNOWN明言+「no verdict」を含む。
2. **rank-34層 (12)**: root hex `00000000080000003800000088001000`（行9,19）・membership 120,079,520,746,539,458 のaggregate一致・A/B split exact整数恒等式 (92,056,115,579,095,019 + 28,023,405,167,444,39)・prior hits {9: [21]（**行9初被覆・単一sharer**）, 19: [0,2,3,8,9,10,15,29,32]（9 sharer）}・4新層census pair {10 shared/23 disjoint}・triple {326/77/125}・quad {1,944/3,366/146}・quint {2,171/38,749/0} 全て機械再導出と厳密一致・3種二重行histogram（quint {15: 314, 16: 66, 18: 897, 19: 894}・**行9はquint二重行に不出現**）・drop-one profile 全2,171本 {3/2/0} 単一・**新disjoint quad 146本のunionが全てちょうど8行**・**累積disjoint quad 1,112をC(34,4)=46,376全件再計数で直接確認・era接続もC(33,4)再計数966・C(32,4)再計数820で独立確認** (1,112 = 966 + 146 = 820 + 146 + 146)・full triple C(34,3)=5,984 {3,622/1,124/1,238} + 15行hist・full quint C(34,5)=278,256 {13,004/265,252/0} + hist {15: 2,244, 16: 436, 18: 6,905, 19: 3,419}・era接続の出版k33 preread照合 (13,004 − 2,171 = 10,833 = 出版k33 preread `full_quints.b_only`、265,252 − 38,749 = 226,503)・sextet C(34,6)=1,344,904 all zero（**I-E quint階打ち切りの9連続**）・raw JSONの3大整数がexact整数 Serialization。
3. **rank33回帰層 (7)**: root `00000000000000801302020000001000`・行 [7,19]・membership 120,083,817,332,086,665・A/B split (92,100,657,745,931,553 / 27,983,159,586,155,112) が機械再導出・k34 preread回帰欄・出版k33 preread欄の3系統で一致・prior hits {7: [20], 19: [0,2,3,8,9,10,15,29]}・4新層census {9/23}・{304/67/125}・{1,827/2,987/146}・{2,036/33,924/0}・3種hist・b_only quint profile {3/2/0}: 2,036・disjoint quad 146 {8: 146}・累積966・full C(33,3)=5,456 {3,296/1,047/1,113}・C(33,5)=237,336 {10,833/226,503/0}・C(33,6)=1,107,568 all zero・era接続 vs k32層 (10,833−2,036=8,797など)・`classifier_comparisons` = 32+496+4,960+35,960+5,456+237,336+1,107,568 = 1,391,808 の公式確認・mismatches=0。
4. **rank32回帰層 (7)**: root `00000000000000801222000000081000`・行 [15,23]・membership 120,146,272,057,315,812・A/B split・prior hits {15: 6, 23: 1}・4新層census {7/24}・{275/50/140}・{1,878/2,459/158}・{2,010/29,455/0}・3種hist・disjoint quad 158 {8: 158}・累積820 が機再導出・k34 preread回帰欄・出版k32 preread欄の3系統で一致・full C(32,3)=4,960 {2,992/980/988}・C(32,5)=201,376 {8,797/192,579/0}・C(32,6)=906,192 all zero・era接続 vs 出版k31 result (`quint_census_k31` 6,787/163,124・`triple_census_k31` 2,717)・`classifier_comparisons` = 1,148,984 の公式確認。
5. **era連鎖 (1)**: k31→k32→k33→k34 の4.rank b_only連鎖（triple 2,717→2,992→3,296→3,622・quint 6,787→8,797→10,833→13,004）が full(n) − new(n) = full(n−1) で両層とも厳密成立。

## 結論

出版済みのrank-34 prereadは**30 checks全項目で当レーンの独立実装による機械再導出と厳密一致した。不一致・新規erratumなし。** 特に (i) 新quint disjoint 0 によるI-E第5次打ち切り継続・C(34,6) sextet全件all zero（9連続）、(ii) disjoint quad累積1,112の全件再計数（966/820中間ranks込み）、(iii) rank33/rank32回帰層が出版k33/k32 preread JSONと完全整合、(iv) k34 prereadの回帰欄と先行出版欄の3系統一致、の4点はk=34本計算の入力基盤として確定した。k31→k34 era連鎖の4.rank拡張も両層（triple/quint）で厳密に閉じた。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。** 本検証はban回避代替最小cover計画の組合せ数の構造確認であり、勝敗に関する何らのverdictも生成しない。

## レジューム

- k=32本計算の出版有無を次回実行冒頭で必ず再確認（出版済みならcrosscheck k32拡張〔quint census k32 2 + era (32,31) 1 + record layer k32 11 + preread pin/層のk32版 = +14以上、既出版124-check script `b71a3211…` へ加法的拡張〕。rank-32層は`45596e44…`のrank32層12 checks、rank-33層は`93c130999…`のrank33層+rank32回帰層、rank-34層は今回のrank34層+rank33/32回帰層をそれぞれ移植可能）。
- k=34本計算の入力基盤はpreread + 第二独立検証の2系統が出揃った。着手はk32/k33本計算出版後が望ましい（rank33/34回帰層の切り替えは `language_note` 記載どちらずれ）。
- rank-35 root（top50 index 34）の事前機械確定とpreread脚本変換が次の対象。
