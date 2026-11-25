# n11-residual72-postfold-witness-recheck-20261120

resolve7: 残余 72 行の post-fold witness 再照合（出版済み正本のみ・単一オーナー）。
単一オーナー宣言ノート `research/log/2026-11-20-n11-resolve7-single-owner-note.md`
を先行出版した同一レーンの実行。branch/PR は作らず main に直接出版。

## 何をしたか

- **入力は 5 正本のみ**（SHA-256 pin で検証・fail-closed）:
  resolve6 正本（`e85d4bfb…`・78 行 base_state／witness_full 39 root）、
  fold9 正本（`24db2352…`・windfall4 閉鎖 4 行）、
  fold10 正本（`bed7d331…`・閉鎖 3 行・残余 72 行・retire 宣言）、
  K1069 掃引正本（39 root 分類 SHA `22953ae1…`）、
  seventeenth 38 gate 正本（`c1073bae…`・coverage claim 2 行）。
  **universe 再構築（resolve6.py のフル再実行）は行わない。候補根の新規判定も行わない。**
- 39-root live witness 計画（39 root × 2 行 = 78 行の 1 回被覆）の割当表を
  正本から再構築し、fold9/fold10 で閉じた 6 行との差分・retire 後の 38 root
  の割当・K1069 depth-10 掃引判定との交差を再照合した。

## 結果（output/residual72-postfold-witness-recheck-20261120.json が正本・27 gate 全 PASS）

1. **残余 72 行の出自が過不足なく確定**: 78 行計画から windfall4 fold の 4 行
   ＋ seventeenth fold の target 2 行を除いた集合が fold10 正本の残余 72 行と
   完全一致（78 − 4 − 2 = 72・disjoint gate PASS）。seventeenth が閉じた 3 行目
   （`00004000000000003800000100000020`・cost 86）は 78 行計画の外の target 外
   extra 行であることを gate で確認。
2. **post-retire 割当表の後継成立**: 十七 root（`00004000000000821082000000000100`）
   retire 後の 38 live root の割当は **34 root × 2 行 ＋ 4 root × 1 行 = 72 行**。
   fold9 で閉じた 4 行を割当てていた 4 root を特定
   （`…08001220`・`…8012220100000100`・`…8012080200…` 系の 4 root・正本参照）。
   各行の割当 root は 1 root のままで 1 回被覆性も維持。
3. **K1069 交差で 39-root 計画の供給枯渇を 72 行単位で確定**: 現存 38 live root
   は K1069 depth-10 全面掃引で**すべて REFUTED-D10**（WIN は十七 root のみ・
   既に retire）。よって残余 72 行の全行が「depth-10 witness として使用不能な
   REFUTED-D10 根」への割当のみとなり、**39-root 計画から残余 72 行への
   depth-10 witness 供給はゼロ**であることを正本演算で確定した。
   （K1069 README の「38 REFUTED root は depth-10 閉鎖 witness 使用不能」の
   記述を、残余 72 行の行単位・割当単位で厳密化したもの。）
4. sv17 正本の coverage claim 2 行が fold10 target 閉鎖 2 行と完全一致
   （fold 幾何再導出と triple 検証正本の独立一致・gate PASS）。

## 決定論性・再現

- stdlib のみ（hashlib/json/os/sys）。`python3 resolve7_post_fold_witness_recheck.py input <out>`。
- 2 回実行・別プロセス別 cwd（/tmp/r7b）で正本 byte-identical
  （出力 SHA-256 `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f`）。
- 27 gate（5 pin ＋ 22 structure/cross）すべて PASS・WIN/LOSS 判定は 1 つも行わない。

## 解釈規約（他の n11 項目と同一）

- REFUTED-D10 は LOSS 証明ではない。fold・被覆は行の簿記であり、閉じた行・
  残った行のゲーム理論的値には一切言及しない。本再照合は 1 行も閉じず
  1 根も判定しない。「供給ゼロ」は 39-root 計画というスコープの観察であり、
  scope 外の閉鎖機構（fresh-safe pool・add-two-stones・depth>10・他レーンの
  証明書）を否定しない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**

## 次の一手

1. 残余 72 行への候補供給の本格探索は resolve6.py の universe 再構築
   （fresh-safe pool の再照合・旧 4,417 から windfall4判定済み 4 根の取り扱いを
   含む）を要する。着手時は単一オーナー宣言ノートを先行すること。
2. add-two-stones 候補拡張・depth>10 コスト測定（K1038 stranded 構造の
   class-dependent な後続）。
