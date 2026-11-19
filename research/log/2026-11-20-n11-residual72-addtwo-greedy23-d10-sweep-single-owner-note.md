# n11 残余72行 add-two greedy 23根 depth-10掃引の単一オーナー宣言（2026-11-20）

本レーンは K1085（残余72行 fresh-unsafe 2,871本の構造分類・add-two-stones拡張census、
正本 SHA-256 `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e`）
README「次の一手」の第1項である **add-two 8石候補 greedy 23根の depth-10 掃引着手** について
単一オーナーとして着手する。並走レーンは本宣言項目に着手しないこと（K1085の44分以内の
同項目着手は 23:29Z 時点で存在しないことを確認済み）。

## 範囲（やること）

- 対象: K1085正本 `add_two_stones_census.greedy_roots` の23根（各8石・quadruple-free）。
  各根・両AND順序（andclose 1/0）・depth 10 の **46 probes**。
- 機械: runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・不成立時abort）。
  生child hex規約: child = root − 最小セットビット。node数はcap内で決定的（機種非依存）。
- 逐次実行を基本とし、CPU並列は doorway 4並列程度まで（node数には影響しない）。
- 各probeの記録: root hex・ordering・nodes・loss・capped・terminalStoneRange・wall。
  verdict分類: loss=true（uncapped）（1順序でも）→ WIN8-D10 candidate（証明書再構築対象）、
  loss=false・少なくとも片順序で未打切り完全探索 → REFUTED-D10 fact、
  capped/timeoutのみ → 当該環境で未検証（コスト下界の事実としてのみ記録）。
- 独立再導入性: greedy 23根の被覆幾何（72行の完全1回被覆・gains hist {4:7,3:13,2:2,1:1}・
  8石/6石popcount・quadruple-free・被覆関係のD4集合演算）を本実験機械内で
  K1085正本とは独立に再導入しgate化する。
- resume-safe: 完走済み(root, ordering)はskip。記録はprobe-record JSONLから
  assemble gate のみで正本JSONを生成。

## やらないこと

- 行の閉鎖claim・receipt fold・証明書抽出・8石receipt被覆幾何の設計は本宣言の対象外
  （WIN8-D10 candidateが見つかった場合の証明書抽出は別の単一オーナー宣言を要する）。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。

## 解釈規約

REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実記録であり、
それ以前の局面のLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
