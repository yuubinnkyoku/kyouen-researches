# n11 残余72行 safe8第5ラウンド再解決の単一オーナー宣言（2026-11-20）

本レーンは K1146（残余23行代替9根depth-10掃引・正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`）
README「次の一手」第1項である **pool P⁗（safe8 120,474−58=120,416根）上の残余20行
greedy再解決（第5ラウンド）** について単一オーナーとして着手する。
並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- **計画簿記のみ**。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは
  一切行わない。
- 対象: 残余20行 = K1146 REFUTED-D10 8根の主張被覆行（canonical化）。
- 除外: REFUTED-D10 累計58根（K1086:16 + K1089:13 + K1091:12 + K1095:9 + K1146:8）。
  pool P⁗ = safe8 − 58 = **120,416根**。
- 入力6正本をSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・
  K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`・replace9正本
  `e8f5d674…`）でfail-closed読み出し。残余23行宇宙はK1097正本から取らず
  K1085→K1086→K1089→K1091→K1095の連鎖から再導入する。
- 機械は出版済みK1097機械（`research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/scripts/`）
  に第5ラウンド結合（Stage C5: replace9 verdict join・主張正準化・残余23行の
  3+20 exactly-once分割検証・Stage F: pool P⁗・残余20行・需要統計・greedy・下界・
  最大マッチング・第4ラウンドWIN候補1根のintrinsic footprint（fold独立性））
  をdeterministic editor（assert付きexact置換・py_compile検証）で加えて構築する。
- 統計pin: 残余20行の需要統計・greedy選定（根順序・周辺被覆行とも）・stranded有無・
  最大マッチング・第4ラウンドWIN候補のintrinsic footprintは、探索実行で得た
  計算事実を機械内literal pinとした上で正本実行で再検証する（pin不一致はfail-closed）。
- 決定性: stdlibのみ・乱数・時刻なし。同一cwd2回+別cwd別HOME1回の計3実行で
  正本JSON byte-identical必須。

## やらないこと

- 行の閉鎖claim・receipt fold・証明書抽出は本宣言の対象外（新WIN候補
  `00000000010000809002000040002001` の証明書抽出は既存の別宣言・並走レーン管轄の
  1根単位手続きに従う）。
- greedy/witness選定を証明書として読まない。REFUTED-D10をLOSS証明として読まない。
  node数・solved数を勝敗として読まない。

## 解釈規約

greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。** 本計算は行を1つも閉じない。
