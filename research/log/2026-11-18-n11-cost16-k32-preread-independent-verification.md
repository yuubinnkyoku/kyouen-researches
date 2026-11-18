# 2026-11-18 N11 cost-16 rank-32 prereadの第二独立導出検証 — 25 checks 0 failures・新規3層構造 (rank32 + rank31/rank30回帰) の機械再導出全一致

## 位置づけ

並走レーンが commit `490a3e44bc`（19:27:16Z）で rank-32 cost-16 構造preread（Python exact-int script `cost16_survival_k32_preread_20261118.py` + preread JSON 31 self-checks・git blob `6d49ab5bea27c967e15b482b33e376510c62b857`）を出版したのを受け、当レーンはk31拡張（`20656084`、124-check crosscheck）の直後に**同prereadの第二独立導出検証**を実施した。preread本体の実装系統はCollection系の分類器組込みであるが、本検証は**preread scriptを一切importしない新規実装の行多重分類器**で、pinned入力（phase-B aggregate `31bdefdb…`・k31 result `0d9f67ee…`・k32 preread `6d49ab5b…`、いずれもgit blob sha1照合・jsdelivr mirror + raw fallback・fail-loud）から全構造項を機械再導出する。k32本計算（disjoint quad 158本のB型pm多次元和 + 新b_only quint 2,010本で重い）の前に入力基盤の独立検証可能性を厳密に改善する位置づけ。

## 検証script

`research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost16_k32_preread_independent_20261118.py`（18,633B・git blob `45596e44a982e79795040873a844c6fdfce4bb09`・sha256 `4ff002e64f3c723feac4537720f8460d433029532ef4ceda649713bed6afe19a`）。`--local DIR` オフラインモード対応（pinned sha1照合は常時）。

## 25 checksの層構成と結果

**network mode・local modeともに 25 checks 0 failures**（local 約3.4秒）。二重実行byte-identical、両モード間の出力一致も確認。

1. **meta層 (3)**: check_count=31・all_pass=true・schema名・prereadが宣言する入力pin 3件が既知pinと一致・`unknown_status` がUNKNOWN明言+「no verdict」を含む。
2. **rank-32層 (12)**: root hex `00000000000000801222000000081000`（行15,23）・membership 120,146,272,057,315,812 のaggregate一致・**A/B split exact整数恒等式** (a_part 92,121,445,452,103,947 + b_part 28,024,826,605,211,865 = M、両部分ともaggregateのpair-root membership表と一致)・prior hits {15: 6, 23: 1}（rank-32が行23を初被覆、indices [11]）・4新層census pair {7/24}・triple {275/50/140}・quad {1,878/2,459/158}・quint {2,010/29,455/0} 全て機械再導出と厳密一致・3種の二重行histogram（triple 12行・quad 12行・quint {15: 613, 16: 65, 18: 962, 19: 370}）・b_only quint のdrop-one four-subset profile 全2,010本が {3/2/0} 単一profile・**新disjoint quad 158本のunionが全てちょうど8行**（`disjoint_quad_union_sizes` {8: 158}）・**累積disjoint quad 820をC(32,4)=35,960全件再計数で直接確認**（era接続: 820 − 158 = 662 = C(31,4)再計数で既出版累積と一致）・full triple C(32,3)=4,960 {2,992/980/988} + 13行hist・full quint C(32,5)=201,376 {8,797/192,579/0} + hist {18: 5,111, 19: 1,766, 15: 1,616, 16: 304}・**era接続の出版k31 result照合** (8,797 − 2,010 = 6,787 = `quint_census_k31.b_only`、192,579 − 29,455 = 163,124 = 同zero)・sextet C(32,6)=906,192 all zero（I-E第6次打ち切り正当化のrank-32版・crosscheck系初）・raw JSONの3大整数がexact整数 Serialization（double丸めなし、json int型確認）。
3. **rank31回帰層 (5)**: root/membership 120,181,378,067,473,629（aggregate exact値と一致 = **k31 double丸めerratumの修正値がそのまま埋め込まれていることを確認**）・prior hits {18: 15, 26: 0}（indices含む）・4新層census {15/0/15}・{265/115/55}・{986/3,025/49}・{819/26,586/0}・3種二重行hist・full C(31,3)=4,495 {2,717/930/848}・C(31,5)=169,911 {6,787/163,124/0}・C(31,6)=736,281 all zero が**出版k31 result JSONのstructure欄と直接一致**・`classifier_comparisons` = 30+435+4,060+27,405+4,495+169,911+736,281 = 942,617 の公式確認・mismatches=0。
4. **rank30回帰層 (4) + era連鎖 (1)**: root/membership 120,210,131,097,430,568 (exact)・prior hits {14: 1, 19: 7}・4新層census {8/0/21}・{248/56/102}・{1,302/2,241/111}・{1,328/22,423/0}・二重行hist（quint {15: 187, 16: 49, 18: 630, 19: 462}）・full C(30,3)=4,060 {2,452/815/793}・C(30,5)=142,506 {5,968/136,538/0}・C(30,6)=593,775 all zero・era b_only連鎖 2,452→2,717→2,992 (triple)・5,968→6,787→8,797 (quint) の両方向連続性。

## 結論

並走出版のrank-32 prereadは**25 checks全項目で当レーンの独立実装による機械再導出と厳密一致した。不一致・新規erratumなし。** 特に (i) 新quint disjoint 0 によるI-E第5次打ち切り継続、(ii) C(32,6)=906,192 sextet全件all zero、(iii) disjoint quad累積820の全件再計数、(iv) rank31/rank30回帰層が出版k31/k30実績と完全整合していること、の4点はk32本計算の入力基盤として確定した。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。** 本検証はban回避代替最小cover計画の組合せ数の構造確認であり、勝敗に関する何らのverdictも生成しない。

## レジューム

- k32本計算は未着手（19:27時点のmain最新 `20656084` 時点で並走レーンの出版なし）。毎時並走が高確率で着手するため、当レーンが重いk32本計算を単独で開始する前に、次回実行の冒頭で**必ず最新mainを取り直してk32本計算の出版有無を確認**し、出版済みならcrosscheck拡張（quint 2 + era (32,31) 1 + record layer 11 + preread pin/層 k32版 = +14以上、既出版124-check scriptへ加法的拡張）に回ること。
- publish済み124-check crosscheck script（`b71a3211…`）の拡張時に、今回のrank-32層12 checks（meta 3除くpreread層として）をそのまま移植可能（分類器・pin機構は同一系統）。
