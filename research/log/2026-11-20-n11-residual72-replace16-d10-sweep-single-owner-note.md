# n11 残余72行 safe8再解決16代替根の depth-10掃引の単一オーナー宣言（2026-11-20）

本レーンは K1088（safe8 pool の REFUTED-D10 16根除外後再解決・正本 SHA-256
`16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724`）
README「次の一手」第1項である **16代替根の depth-10 verdict 掃引** について
単一オーナーとして着手する。並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- 対象: K1088正本 `scope1_refsolve_residual49.greedy_selection` の16根
  （各8石・quadruple-free・残余49行をleftover 0で完全被覆するgreedy計画根）。
  各根・両AND順序（andclose 1/0）・depth 10 の **32 probes**。
- 機械: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・
  不成立時abort）。生child hex規約: child = root − 最小セットビット
  （帳記のみでverdictに影響しない）。
- verdict分類: いずれかの順序で uncapped loss=true → WIN8-D10 candidate・
  両順序 uncapped loss=false → REFUTED-D10 fact・capped/timeoutのみ →
  当該環境で未検証（コスト下界の事実としてのみ記録）。
- 独立再導入性: 16根の被覆幾何（主張49行被覆・各根popcount 8・canonical・
  D4部分集合関係）を本掃引機械内でK1088正本とは独立に再導入しgate化する。
- resume-safe: 完走済み(root, ordering)はskip。記録はprobe-record JSONLから
  assemble gate のみで正本JSONを生成。

## やらないこと

- 行の閉鎖claim・receipt fold・証明書抽出・8石receipt被覆幾何の設計は本宣言の
  対象外（WIN8-D10 candidateが見つかった場合の証明書抽出は別の単一オーナー
  宣言を要する）。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。

## 解釈規約

REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実記録であり、
それ以前の局面のLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
