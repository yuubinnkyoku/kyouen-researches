# 2026-11-18 N11 cost-16 parent 生存曲線: rank-30 構造preread

rank-29の急増がそのまま続くとは限らない。rank-30は、同じ31行cost-16 parentのtop50 membership順位30番目のpair rootで、覆う行は **(14,19)**。rank-29の(0,16)とは異なる重なり方をする。

## 入力と再現

入力はmain上の3ファイルで、Git blob SHA-1を固定した。

- phase-B aggregate: `31bdefdb2e2cc90b706cbb8090e98eb5eece4d87`
- k=27 result: `3dc30ad6c51cc2d7678cc8777e4af2376267ddb8`
- k=28 result: `99db3a9a48d044727b3a4d83fb7fc97daa7513d2`
- rank-29の回帰基準: [2026-11-18 rank-29 preread log](2026-11-18-n11-cost16-survival-k29-preread.md)

再現スクリプトは [cost16_survival_k30_preread_20261118.mjs](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_survival_k30_preread_20261118.mjs)。repo rootから実行する。出力は同experimentの `output/cost16-survival-k30-preread-20261118.json`。

分類は独立した2方式で行った。第一は各rootの被覆行を直接数えるMap方式、第二は行ごとのroot incidenceをBigInt bitsetにして選択root集合との共通部分のbit数を数える方式。top50全体をbitset化せず、rank-30までの最初の30 rootだけを母集団にした。これによりJavaScriptの32-bit shiftによる32以上のbit位置の折り返しを避ける。

## rank-30 root

- root: `00000000080008003800000008001000`
- covered rows: `[14,19]`
- prior hits: row 14 は1本、row 19 は7本

| rank-30で新たに加わる部分集合 | B型 | zero型 | disjoint型 | 総数 |
|---|---:|---:|---:|---:|
| pair (29通り) | 8 | 0 | 21 | 29 |
| triple (406通り) | 248 | 56 | 102 | 406 |
| quad (3,654通り) | 1,302 | 2,241 | 111 | 3,654 |
| quint (23,751通り) | 1,328 | 22,423 | 0 | 23,751 |

B型quintの二重行別内訳は row 15:187、row 16:49、row 18:630、row 19:462。1,328件すべての4-subset profileは `3/2/0`（B型3・disjoint型2・zero型0）。disjoint quad 111件はすべて8行の和集合を持つ。

## 全層の再集計

- 全 `C(30,3)=4,060` triple: B型2,452 / zero型815 / disjoint型793
- 全 `C(30,5)=142,506` quint: B型5,968 / zero型136,538 / disjoint型0
- 全quintの二重行別内訳: row 15:925、row 16:221、row 18:3,536、row 19:1,286

全層からrank-30新層を引くとrank-29までの全層censusへ戻り、quintの二重行ヒストグラム差分もrank-30新層の値と一致した。rank-28の出版値とrank-29 preread logも回帰照合した。k28 JSONがk27 JSONの固定blobを入力として宣言していることも検査した。

## rank-29との比較

rank-29はdisjoint pair 24、disjoint quad 225、B型quint 2,128だった。rank-30ではそれぞれ21、111、1,328へ減少した。したがって、rank-29で観測された急増を単調な増加則として外挿してはならない。rank-30は依然としてdisjoint quadを111件持つが、rank-29の記録値は更新していない。

## 検証と実装上の注意

- 22項目すべてPASS。
- rank-28の出版census、rank-29 prereadの新層・全層censusを再現。
- rank-29/30の新層および全層でMap分類とBigInt bitset分類が一致。
- rank-30の全quint censusから新層を引いた差分がrank-29全quint censusと一致。
- もう一度別の実行でBigInt incidence方式を再計算し、rank-29/30のpair・triple・quad・quintおよびrank-30全層triple/quintが全件一致（10/10 checks）。

初回の作業用試行では、top50全体をJavaScript Numberの32-bit bitwise演算に入れてしまい、32番目以降のshiftが折り返す誤りを検出した。その出力は破棄した。確定計算はtop30に限定したBigInt bitsetで再実行し、Map方式との一致と別実行の再照合を通した。

## 解釈の境界

これは候補rootの行重複に関する有限構造censusである。Pm生存数、探索費用、WIN/LOSS、証明書、manifest閉鎖を計算していない。REFUTED-D10やSTERILEをLOSSと扱わない。標準11×11空盤、二石root、S2、class 1/2/4はすべて **UNKNOWN** のまま。
