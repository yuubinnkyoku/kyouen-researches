# 2026-11-18 N11 cost-16 生存曲線 crosscheck k=31 sextet・preread層の追加拡張 — 112→124 checks・network/local両モード 0 failures・並走k31基盤拡張の独立検証とI-E第6次打ち切り正当化のcrosscheck系初導入

## 経緯（並走衝突の回避）

本レーンはk30版（98 checks・blob `58057b48…`）から独立にk31基盤拡張（PINS・quint census・era接続 (31,30)・record layer k31）を構築中だったが、push直前HEAD再取得で**並走レーンが `d994e371cf`（19:20:33Z）で同一内容の基盤拡張（112 checks）を同一script path・同一log名で出版済み**であることを検出した。repo規約（2026-11-18の並走運用手順）に従い:

1. 先行版を正本とし、**自レーンの重複する基盤拡張は廃棄して上書きしなかった**（script 42,688B・log は unpublishedのまま破棄）。
2. **先行出版版（blob `62a581fe3a691a3c6cb266f4a0f5e0e2dd03a73c`・112 checks）をlocal/network両モードで独立検証し 0 failures・両モード出力一致を確認**した（当レーン独自の検証成果。出版値 kill(31)=2,526,118,818,461,447,714・I-E 3恒等式のrecord joints再加算 52,914,484,706,624,166 / 41,353,998,417,711,129 / 11,560,486,288,913,037 は当レーンの独立実装でも全一致）。
3. 先行版に**当レーン固有の新規12 checksのみを加法的に拡張**して出版する（本コミット）。既存112 checkの出力は一切不変であることをdiffで確認（純加算・PINSにpreread pin追加のみがfetch系の変更）。

## 新規拡張1: sextet census機械再導出（3 checks・I-E第6次打ち切り正当化の第三系統検証）

k=29/30/31の6-subset census **C(29,6)=475,020・C(30,6)=593,775・C(31,6)=736,281を全件独立classifierで再分類**し、出版 `sextet_census_k{29,30,31}` のall-zero（b_only 0・disjoint 0・zero=C(n,6)）と厳密一致。第6次打ち切り正当化はそれまで各実験finalize内の自己検証（quint I-E項で止めてよい根拠）しかなく、**crosscheck系統からの独立再導出は今回が初めて**。行26がrank-31で史上初被覆しても736,281 sextet全てが構造的ゼロ。

## 新規拡張2: preread層（9 checks・k=31のみ）

rank-31 preread JSON（commit `188106bb`・blob `51d08148e0d449dbd4e93df77bbab0b00326491f`）をpin付き取得し、実験script依存なしに機械再導出:

1. **root/rows/prior hits**: (18,26)・hex照合・行18ハブ15本（indices 1,4,5,6,7,11,12,18,19,20,21,23,24,26,27）・行26 first-ever cover 0本をaggregateから再導出して一致。
2. **4種新層census**: pair {15/0/15}・triple {265/115/55}=435・quad {986/3,025/49}=4,060・quint {819/26,586/0}=27,405 が機械再導出と厳密一致（quint新b_only 819はquint census全再導出の集合とも一致）。
3. **rank30_regression埋め込みcensus**: pair {8/0/21}・triple {248/56/102}・quad {1,302/2,241/111}・quint {1,328/22,423/0} を独立に再導出して一致。
4. **full triple/quint census + 二重行hist**: triple {2,717/930/848}+hist・quint {6,787/163,124/0}+hist {15:1,003, 16:239, 18:4,149, 19:1,396}・`compared`/`mismatches`=0まで一致。
5. **新quint二重行hist {15:78, 16:18, 18:613, 19:110}** と **b_only four-subset profiles {3/2/0: 819}**: drop-one classify（5要素から1つずつ落とした4-subsetのb_only/disjoint/zero個数「3/2/0」）を独立実装で再導出し全819本が同一profile。
6. **sextet census**: preread `sextet_census` が機械再導出 {0/736,281/0} と一致。
7. **大整数3項のdouble丸め検証（erratumの独立確認）**: preread値 120,181,378,067,473,630 / 92,082,202,719,887,120 / 28,099,175,347,586,504 は exact（aggregate機械導出） 120,181,378,067,473,629 / 92,082,202,719,887,124 / 28,099,175,347,586,505 に対し **deltas (+1, −4, −1)**: すべて 0<|delta|≤8（2^56..2^57帯のhalf-ULPスケール）で等しくなく、**A+B==M恒等式が近似値側では不成立（gap −6）・exact側で厳密成立**。Node Number表示経由の丸め誤差というerratumの説明を第三系統から定量的に確認。
8. **k31出版JSON側**: `structure.preread_erratum` noteが3つのexact整数を明記・`rank31_root`の3項がexact整数・`preread_match.*` 5 check（triple_census/new_quad_census/quint_census/quint_double_rows/sextet_census）がすべて存在しpass。

## erratum（前回レジュームメモの誤記・出版前に機械検出）

k31レジュームメモにあった「quint census累積接続（6,787+819=7,606）」は誤記。正しくは **full(30) b_only 5,968 + 新層 819 = full(31) b_only 6,787**（=C(31,5)全census b_only。7,606は不存在の値・新層の二重加算）。先行版（`d994e371cf`）のlogとcheck式は正しい接続（31,30）を機械確認済みであり本誤記の影響は出版体になし。

## 実行記録

- 基盤112 checks（先行版 `d994e371cf`）: local mode 0 failures（約2秒・当レーンで検証）・network mode 0 failures・両モード出力一致。
- 拡張後124 checks: local mode（pinned入力git blob sha1照合・二重実行byte-identical）124 checks 0 failures（約3.4秒）・network mode（jsdelivr+raw fallback・全pin sha1照合）124 checks 0 failures・**先行112 checkの出力は一切不変**（diff純加算確認: 12 PASS行追加と `--- 124 checks, 0 failures` 集計行のみ）。
- 124 checks内訳: 先行98 + k31基盤14〔quint 2 + era (31,30) 1 + record layer 11〕 + **sextet 3** + **preread層 9**。拡張後script 42,522B（git blob `b71a3211917057cd36cb4e1f9b006d7298cf7fa0`・sha256 `5de62e61eb93bc3dc10f05f6f68de84a882a31773c55aa6ba086b0dab2c29e84`）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。** 生存曲線はban回避代替最小cover計画の組合せ数であり、勝敗に関する何らのverdictも生成しない。

次レジューム: (i) **k=32 prereadは並走レーンが出版済み**（commit `490a3e44bc` 19:27:16Z: rank-32 (15,23) mid-hub root・新pair 7/24・新quad disjoint 158〔累積820〕・新b_only quints 2,010〔累積8,797・全3/2/0〕・sextet C(32,6)=906,192 all zero・Node丸めerratumはJSON round-trip checkで構造的予防済み）。次回はk32本計算（重い: disjoint quad 158本のB型pm多次元和+quint 2,010本）が主対象、(ii) k32本計算出版後のcrosscheck拡張（quint 2 + era (32,31) 1 + record 11 + preread pin/層のk32版 = +14以上想定・preread層はk31同様の機械再導出で、double丸めcheckはround-trip済みなら恒等式側の検証に自動縮退の見込み）。
