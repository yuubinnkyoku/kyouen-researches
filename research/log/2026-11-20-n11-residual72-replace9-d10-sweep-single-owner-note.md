# n11 残余72行 safe8第4ラウンド再解決9代替根の depth-10掃引の単一オーナー宣言（2026-11-20）

本レーンは K1097（残余72行 safe8 pool 第4ラウンド再解決・正本 SHA-256
`2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`）
README「次の一手」第1項である **9代替根の depth-10 verdict 掃引** について
単一オーナーとして着手する。並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- 対象: K1097正本 `scope1_refsolve_residual23.greedy_selection` の9根
  （各8石・quadruple-free・残余23行をleftover 0で完全被覆するgreedy計画根。
  gains {3: 6, 2: 2, 1: 1}）。
  各根・両AND順序（andclose 1/0）・depth 10 の **18 probes**。
- 機械: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・
  不成立時abort）。生child hex規約: child = root − 最小セットビット
  （帳記のみでverdictに影響しない）。
- verdict分類: いずれかの順序で uncapped loss=true → WIN8-D10 candidate
  （累計候補に加算し、証明書抽出は別宣言）・両順序 uncapped loss=false →
  REFUTED-D10 fact（第5ラウンド再解決のためにさらに除外する候補）・
  capped/timeoutのみ → 当該環境で未検証（コスト下界の事実としてのみ記録）。
- 独立再導入性: 残余23行宇宙（K1095 REFUTED-9根の主張23行）はK1095やK1097
  正本から直接取らず K1085+K1086+K1089+K1091+K1095 から再導入し、9根の被覆
  幾何（主張23行のexactly-once被覆・gains hist {3:6, 2:2, 1:1}・各根
  popcount 8・D4 min-canonical・quadruple-free・D4部分集合関係）を本掃引機械内で
  K1097正本とは独立に再導入しgate化する（K1097帳簿の残23行一致はcrosscheck
  gateとする）。
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
S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。** 本掃引は行を1つも閉じない:
残余72行は全行open。
