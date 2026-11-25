# n11 残余72行 safe8再解決 第2ラウンド（REFUTED-D10 29根除外・残余40行）の単一オーナー宣言（2026-11-20）

本レーンは K1089（代替16根 depth-10掃引・正本 SHA-256
`808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`）の結果
（WIN8-D10 candidate 3根・REFUTED-D10 fact 13根）を受け、
**REFUTED-D10 29根（K1086の16根 + K1089の13根）を除外した pool P′（120,445根）での
残余40行 greedy計画再解決** について単一オーナーとして着手する。
並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- 対象行: 残余40行（K1089 REFUTED-13根の主張被覆40行。残余49行からWIN8-3根の
  主張9行を除いた行集合）。
- 入力3正本: K1085 census（SHA-256 `5fdd342d…`）・K1086掃引（`3045e152…`）・
  K1089掃引（`808fbda1…`）をSHA-256 pinでfail-closed読み出し。
- 再導入: universe82（generation witness→canonical dedup）・safe8 pool・coverage・
  greedy23根計画完全再現はK1088機械と同じく本実験機械内で独立再導入。
  residual49行宇宙はK1085+K1086から再導入し、K1089の代替16根の主張被覆は
  canonical化・幾何検証（主張行のresidual行D4方位・C(8,6)部分集合関係・
  49行exactly-once分割）して使う。
- 再解決: pool P′ = safe8 − 29 REFUTED根での残余40行の demand・stranded行・
  greedy計画・情報論的下界・二部最大マッチング。
- 内在被覆: 累計10 WIN8-D10候補根（K1086の7根+K1089の3根）の残余40行への
  intrinsic coverage（C(8,6)=28部分集合のcanonical再導入・幾何事実のみ）。
  余剰があればwindfall供給の事実記録、無ければ需要構造確定。

## やらないこと

- 新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは一切行わない
  （証明書抽出1根の宣言ノートは並走レーンが先行出版済み:
  `research/log/2026-11-20-n11-residual72-win8-certificate-extract-single-owner-note.md`）。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。
- greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。

## 解釈規約

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。** 本計算は行を1つも閉じない。
