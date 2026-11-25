# n11 残余72行 safe8第3ラウンド再解決12代替根の depth-10掃引の単一オーナー宣言（2026-11-20）

本レーンは K1094（safe8 pool の REFUTED-D10 41根除外後再解決・正本 SHA-256
`e19244904779d906853de603d42c07903e08ab80008aeeb621913669a249baa8`）
README「次の一手」第1項である **12代替根の depth-10 verdict 掃引** について
単一オーナーとして着手する。並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- 対象: K1094正本 `scope1_refsolve_residual30.greedy_selection` の12根
  （各8石・quadruple-free・残余30行をleftover 0で完全被覆するgreedy計画根）。
  各根・両AND順序（andclose 1/0）・depth 10 の **24 probes**。
- 機械: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・
  不成立時abort）。生child hex規約: child = root − 最小セットビット
  （帳記のみでverdictに影響しない）。
- verdict分類: いずれかの順序で uncapped loss=true → WIN8-D10 candidate
  （累計候補に加算し、証明書抽出は別宣言）・両順序 uncapped loss=false →
  REFUTED-D10 fact（第4ラウンド再解決のためにさらに除外する候補）・
  capped/timeoutのみ → 当該環境で未検証（コスト下界の事実としてのみ記録）。
- 独立再導入性: 残余30行宇宙（K1091 REFUTED-12根の主張30行）はK1091正本から
  直接取らず K1085+K1086+K1089+K1091 から再導入し、12根の被覆幾何（主張30行の
  exactly-once被覆・各根popcount 8・D4 min-canonical・quadruple-free・
  D4部分集合関係）を本掃引機械内でK1094正本とは独立に再導入しgate化する
  （K1094帳簿の残30行一致はcrosscheck gateとする）。
- resume-safe: 完走済み(root, ordering)はskip。記録はprobe-record JSONLから
  assemble gate のみで正本JSONを生成。

## やらないこと

- 行の閉鎖claim・receipt fold・証明書抽出・8石receipt被覆幾何の設計は本宣言の
  対象外（WIN8-D10 candidateが見つかった場合の証明書抽出は既存の別宣言・
  並走レーン管轄の抽出手続きに従う）。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。

## 解釈規約

REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実記録であり、
それ以前の局面のLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
