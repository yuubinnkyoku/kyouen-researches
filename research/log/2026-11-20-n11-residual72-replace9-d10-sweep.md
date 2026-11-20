# 残余23行 代替9根 depth-10掃引の実行記録（2026-11-20）

単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md`
（commit `51bbb938809c36eafbf5a762f03bf729c097fe6f`・先行出版）の下で実施した。
対象は K1097（残余23行第4ラウンド再解決）の greedy 9代替根
（8根被覆判定実験で P‴ 上の候補根数最小性が確定済みの計画）の depth-10 verdict。

## 実行経緯

- 宣言前にmain最新（`ec64bfc17a`）を取り直し、K1085/K1086/K1089/K1091/K1095の
  正本を再取得してSHA-256 pin検証（6/6一致・K1097は既存検証済み正本）。
- runner v17（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）を
  K1095掃引実験から取得しSHA-1検査で一致、pilot_d6制御
  （nodes 3,402・loss=false）を単独実行でPASS確認後に宣言出版。
- 機械は出版済みreplace12掃引機械を、対象9根・入力6正本・残余23行再導入
  gate・掃引正本向けにdeterministic editor（assert付き完全置換・py_compile検証）で
  構築した。
- 18 probes（9根×両AND順序×depth 10・cap 30M・timeout 280s）を4 worker並列で
  実行、13.3秒で全完走（capped 0・error 0）。
- assembleは全20 gate PASSで正本JSONを生成。同一cwd再実行と別cwd・別HOME
  （exp-bコピー）の計3実行でbyte-identicalを確認。

## 結果の要点

- **WIN8-D10 candidate 1根**: `00000000010000809002000040002001`
  （gained 3・両順序 uncapped loss=true・nodes 608,293/691,784）。
  主張被覆行: `00000000000000801202000001000400`・
  `00000000000000801202000001080000`・`00000000010000809002000040000000`。
- **REFUTED-D10 fact 8根**（両順序 uncapped loss=false・主張被覆20行）。
- 累計: WIN8-D10 candidate 17根（主張52行）・REFUTED-D10 58根。
  第5ラウンド pool P⁗ = 120,416根・残余23行のうち20行が次の代替被覆対象。
- nodes総計 3,574,172・terminal石数union [14,18]・全18 probeがpilot_d6制御PASS。

## 再現性の確認

- probe再実行: WIN根の両順序（608,293/691,784 nodes・loss=true）と
  REFUTED根 `00000000000000083800040048100000` の両順序
  （11,664/80,912 nodes・loss=false）の再実行で、nodes/loss/capped/
  terminalStoneRangeが全て正本記録と完全一致（msは除く）。
- 独立再導入: 残余23行宇宙はK1085→K1086→K1089→K1091→K1095の連鎖から
  独立再導入し、K1097帳簿（per_row_residual23・scope1==scope2同一選定）と
  一致をcrosscheck gateで確認。9根の被覆幾何（23行exactly-once・quadruple-free・
  D4 min-canonical・gains {3:6,2:2,1:1}・child = root − 最小セットビット）を
  20 gateで全数検査。
- 正本JSON SHA-256
  `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`
  （15,403 bytes・`output/replace9-d10-sweep-20261120.json`）。

## 意味

- K1097計画の代替9根のうち8根がdepth-10で必勝を持たないことが確定し、
  候補poolは58根除外の120,416根に浸食した。第5ラウンドは残余20行の再解決になる。
- 1根がWIN8-D10 candidateとなった。これは累計17 WIN候補のうちの52行主張の
  一部であり、証明書抽出・行閉鎖は別工程・別宣言。
- REFUTED-D10 は LOSS 証明ではなく、行は1行も閉じていない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
UNKNOWN のまま。**

## 次回への引継ぎ

- 第5ラウンド再解決: pool P⁗（120,416根）上の残余20行greedy・下界・最小性の
  確認→代替根の次掃引（着手時に単一オーナー宣言）。
- 新WIN8-D10 candidateの証明書抽出は別宣言（1根単位の宣言と独立二重検証）。
- 並走レーンの証明書抽出・receipt foldの進捗反映後は、残余需要を
  再計算してから第5ラウンド計画を作ること。
