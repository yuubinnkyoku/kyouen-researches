# 2026-11-18 N11 cost-16 rank-33 prereadの第二独立導出検証 — 29 checks 0 failures・rank33新層 + rank32/rank31回帰の機械再導出全一致・k30→k33 era連鎖の4.rank拡張

## 位置づけ

commit `67068e077`（19:37:30Z）で出版された rank-33 cost-16 構造preread（Python exact-int script `cost16_survival_k33_preread_20261118.py` + preread JSON 31 self-checks・git blob `e4346ddd7e08799b4406dcdba930de714e4f462c`）のうちrank-33層は、この時点では当レーンのpreread実装単独であった。本検証はk=33本計算の入力基盤を独立検証可能にするため、**preread scriptを一切importしない新規実装の行多重分類器**で、pinned入力（phase-B aggregate `31bdefdb…`・k31 result `0d9f67ee…`・k32 preread `6d49ab5b…`・k33 preread `e4346ddd…`、いずれもgit blob sha1照合・jsdelivr mirror + raw fallback・fail-loud）から全構造項を機械再導出した。rank-33 prereadのrank32回帰層は「出版k=32 preread JSONに対する回帰」として書かれているため、本検証はその回帰値を**出版k32 preread JSON（`6d49ab5b…`）のrank32欄とfield-by-fieldで直接照合**する3系統構成（個別機械再導出・k33 preread回帰欄・k32 preread出版欄）とした。k=33本計算（quint b_only 2,036本・disjoint quad 146本・disjoint triple 125本）のload/assert chainの入力が確定した。

## 検証script

`research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost16_k33_preread_independent_20261118.py`（24,786B・git blob `93c130999a4eda0a7f9607fb4a16e2faea6464ae`・sha256 `f561df56000c9be93f1c17171a24651ef0258d40697acda3223ba989734825b2`）。k32版検証script（`45596e44…`）と同一様式（分類器・census・pin取得機構は新規実装）。`--local DIR` オフラインモード対応（pinned sha1照合は常時）。

## 29 checksの層構成と結果

**network mode・local modeともに 29 checks 0 failures**（local 約4.8秒・network 約6.4秒）。二重実行byte-identical、両モード間の出力一致も確認。

1. **meta層 (3)**: check_count=31・all_pass=true・schema名 `n11-cost16-k33-preread-20261118-v1`・prereadが宣言する入力pin 3件（aggregate/k31_result/k32_preread）が既知pinと一致・`unknown_status` がUNKNOWN明言+「no verdict」を含む。
2. **rank-33層 (12)**: root hex `00000000000000801302020000001000`（行7,19）・membership 120,083,817,332,086,665 のaggregate一致・**A/B split exact整数恒等式** (a_part 92,100,657,745,931,553 + b_part 27,983,159,586,155,112 = M、両部分ともaggregateのpair-root membership表と一致)・prior hits {7: [20]（単一sharer）, 19: [0,2,3,8,9,10,15,29]（8 sharer）}・4新層census pair {9 shared/23 disjoint}・triple {304/67/125}・quad {1,827/2,987/146}・quint {2,036/33,924/0} 全て機械再導出と厳密一致・3種の二重行histogram（triple 10行〔7: 8を含む〕・quad 10行〔7: 11を含む〕・quint {15: 314, 16: 66, 18: 897, 19: 759}・**行7はquint二重行に不出現**）・b_only quint のdrop-one four-subset profile 全2,036本が {3/2/0} 単一profile・**新disjoint quad 146本のunionが全てちょうど8行**（`disjoint_quad_union_sizes` {8: 146}）・**累積disjoint quad 966をC(33,4)=40,920全件再計数で直接確認、era接続もC(32,4)再計数820・C(31,4)再計数662で独立確認** (966 = 820 + 146 = 662 + 158 + 146)・full triple C(33,3)=5,456 {3,296/1,047/1,113} + 14行hist・full quint C(33,5)=237,336 {10,833/226,503/0} + hist {15: 1,930, 16: 370, 18: 6,008, 19: 2,525}・**era接続の出版k32 preread照合** (10,833 − 2,036 = 8,797 = 出版k32 preread `full_quints.b_only`、226,503 − 33,924 = 192,579 = 同zero)・sextet C(33,6)=1,107,568 all zero（I-E quint階打ち切りのrank-33版）・raw JSONの3大整数がexact整数 Serialization（double丸めなし、json int型確認）。
3. **rank32回帰層 (7)**: root `00000000000000801222000000081000`（行15,23）・membership 120,146,272,057,315,812・A/B split (92,121,445,452,103,947 / 28,024,826,605,211,865) が**k33 preread回帰欄・機械再導出・出版k32 preread JSON rank32欄の3系統で一致**・prior hits {15: [0,13,14,16,17,22], 23: [11]}・4新層census pair {7/24}・triple {275/50/140}・quad {1,878/2,459/158}・quint {2,010/29,455/0} と3種二重行histogram・disjoint_quad_count 158・cumulative 820 も出版k32 preread欄と一致・full C(32,3)=4,960 {2,992/980/988}・C(32,5)=201,376 {8,797/192,579/0}・C(32,6)=906,192 all zero・era接続 vs k31層 (8,797 − 2,010 = 6,787 = 出版k31 result `quint_census_k31.b_only`、192,579 − 29,455 = 163,124、triple 2,992 − 275 = 2,717)・`classifier_comparisons` = 31+465+4,495+31,465+4,960+201,376+906,192 = 1,148,984 の公式確認・mismatches=0。
4. **rank31回帰層 (6)**: root `00000000000040809002001000100000`（行18,26）・membership 120,181,378,067,473,629（aggregate exact値）・prior hits {18: 15 indices, 26: []（初被覆）}・4新層census {15/0/15}・{265/115/55}・{986/3,025/49}・{819/26,586/0}・3種二重行hist・full C(31,3)=4,495 {2,717/930/848}・C(31,5)=169,911 {6,787/163,124/0}（出版k31 result `quint_census_k31`・`quint_b_only_double_rows` histと一致）・C(31,6)=736,281 all zero・zero_synth 26,586 = C(30,4) − 819 ・`classifier_comparisons` = 942,617の公式確認。
5. **era連鎖 (1)**: k30→k31→k32→k33 の4.rank b_only連鎖（triple 2,452→2,717→2,992→3,296・quint 5,968→6,787→8,797→10,833）が full(n) − new(n) = full(n−1) で両層とも厳密成立。C(30,3)/C(30,5)も機械再導出で確認。

## 結論

出版済みのrank-33 prereadは**29 checks全項目で当レーンの独立実装による機械再導出と厳密一致した。不一致・新規erratumなし。** 特に (i) 新quint disjoint 0 によるI-E第5次打ち切り継続、(ii) C(33,6)=1,107,568 sextet全件all zero、(iii) disjoint quad累積966の全件再計数（820/662の中間ranks込み）、(iv) rank32/rank31回帰層が出版k32 preread・k31 result JSONと完全整合、(v) k33 prereadのrank32回帰欄とk32 preread出版欄の3系統一致、の5点はk=33本計算の入力基盤として確定した。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。** 本検証はban回避代替最小cover計画の組合せ数の構造確認であり、勝敗に関する何らのverdictも生成しない。

## レジューム

- k=32本計算の出版有無を次回実行冒頭で必ず再確認（出版済みならcrosscheck k32拡張〔quint census k32 2 + era (32,31) 1 + record layer k32 11 + preread pin/層のk32版 = +14以上、既出版124-check script `b71a3211…`へ加法的拡張〕。k33 preread層も今回のrank-33層12 checksを移植可能）。
- k=33本計算はpreread + 第二独立検証の2系統が出揃ったため着手可能（k32本計算の完了・出版後が望ましい: k33 main側のrank32回帰層はk32 result JSON出版時にそちらへ切り替え〔preread JSON `language_note` に既記載〕）。
- rank-34 root（top50 index 33）の事前機械確定が次のpreread対象。
- 実行時間はlocal 4.8s・network 6.4sで、k32版検証（3.4s/8.7s）に対しても軽量。
