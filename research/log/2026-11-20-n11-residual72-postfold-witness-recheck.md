# 2026-11-20 n11: resolve7 残余72行のpost-fold witness再照合（K1072）

単一オーナー宣言ノート（`2026-11-20-n11-resolve7-single-owner-note.md`）を
先行出版した上で、K1071（fold10）で残余 74→72 行・十七 root retire 後の
39-root live witness 計画の状況を、**出版済み 5 正本のみ**で再照合した。
universe 再構築・候補根の新規判定・行の閉鎖は一切行っていない。

## 入力（SHA-256 pin・fail-closed）

- resolve6 正本 `e85d4bfb…c281a`（78 行 base_state・witness_full 39 root）
- fold9 正本 `24db2352…`（windfall4 閉鎖 4 行）
- fold10 正本 `bed7d331…`（閉鎖 3 行・残余 72 行・retire 宣言）
- K1069 掃引正本 `22953ae1…`（39 root 分類 WIN 1/REFUTED 38）
- sv17 38 gate 正本 `c1073bae…`（coverage claim 2 行）

## 結果（27 gate 全 PASS・正本 SHA-256 `207f4094…`）

1. **残余 72 行の出自**: 78 行計画 − fold9 の 4 行 − fold10 の 2 行 = 72 行、
   fold10 正本の残余 72 行と完全一致・6 行は disjoint。fold10 の 3 行目の
   閉鎖（`00004000000000003800000100000020`）は 78 行計画外の target 外
   extra 行。sv17 正本の coverage claim 2 行 == fold10 target 閉鎖 2 行。
2. **retire 後割当表**: 十七 root retire 後 38 live root の割当は
   34 root × 2 行 + 4 root × 1 行 = 72 行。残余 72 行の全行がちょうど
   1 root 割当で 1 回被覆性を維持。fold9 閉鎖 4 行の割当 root 4 本を特定。
3. **K1069 交差**: 現存 38 live root はすべて REFUTED-D10。よって残余 72 行の
   全行が depth-10 witness として使用不能な根への割当のみであり、
   **39-root 計画からの残余 72 行への depth-10 witness 供給はゼロ**。
   残余 72 行の閉鎖には fresh-safe pool 再照合（resolve6.py 再実行・
   単一オーナー宣言必要）・add-two-stones・depth>10・他の証明書供給が必要。

## 決定論性

stdlib のみ。2 回実行・別プロセス別 cwd（/tmp/r7b）で byte-identical
（出力 SHA-256 `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f`）。

## 解釈規約

REFUTED-D10 は LOSS 証明ではない。本項は 1 行も閉じず 1 根も判定しない。
「供給ゼロ」は 39-root 計画スコープの観察である。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**
