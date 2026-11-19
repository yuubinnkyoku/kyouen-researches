---
id: K1072
title: "残余72行のpost-fold witness再照合（resolve7）: 78行計画−fold9 4行−fold10 2行=72行の過不足なし・retire後38 root割当34×2+4×1で1回被覆維持・K1069掃引交差で残36 root含む全38 live根がREFUTED-D10であり39-root計画からの残余72行へのdepth-10 witness供給ゼロを正本演算で確定"
kind: computation
status: computed
topics: [residual-coverage]
aliases:
  - resolve7 (published-records-only recheck; no universe rebuild, no new judging)
  - post-retire assignment table of the 39-root one-cover plan: 34 roots x 2 rows + 4 roots x 1 row = 72 rows, one-cover preserved
  - all 38 live assigned roots are REFUTED-D10 under the K1069 sweep; zero further depth-10 witness supply from this plan for the residual 72 rows
  - fold9-closed 4 rows' witness owners identified (4 roots degrade to 1-row assignments)
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1063
  note: resolve6正本（e85d4bfb…）のwitness_full 39 root×2行=78行の1回被覆割当表と78行base_state
- type: depends_on
  target: K1066
  note: windfall4証明書群（fold9正本24db2352…の閉鎖4行の特定）
- type: depends_on
  target: K1067
  note: windfall4 receipt fold（fold9）の閉鎖4行が78行計画内であることの正本
- type: depends_on
  target: K1069
  note: 39 live witness depth-10全面掃引正本（WIN 1/REFUTED 38・分類SHA 22953ae1…）との交差
- type: depends_on
  target: K1070
  note: 十七証明書38 gate正本（c1073bae…）のcoverage claim 2行
- type: depends_on
  target: K1071
  note: fold10正本（bed7d331…）の残余72行・閉鎖3行・retire宣言が本再照合の直接入力
artifacts:
- path: research/experiments/n11-residual72-postfold-witness-recheck-20261120/resolve7_post_fold_witness_recheck.py
  role: verifier
  note: 5正本SHA-256 pin（resolve6/fold9/fold10/K1069掃引/sv17）・27 gate・出版記録のみの再照合機械
- path: research/experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json
  role: data
  note: 再照合正本（SHA-256 207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f）・2回実行+別cwd別プロセスでbyte-identical・27 gate全PASS
- path: research/log/2026-11-20-n11-resolve7-single-owner-note.md
  role: note
  note: 単一オーナー宣言ノート（先行出版・fresh pool再照合は管轄外と明記）
scope: >-
  出版済み5正本のみから残余72行の出自・retire後割当表・K1069交差までを再照合
  する。universe再構築・候補根の新規判定・行の閉鎖・depth-saturation audit、
  二石root・空盤の勝敗確定は対象外。閉じた行・残った行のゲーム理論的値は主張しない。
evidence: >-
  （1）入力は5正本をSHA-256 pin（resolve6 e85d4bfb…・fold9 24db2352…・
  fold10 bed7d331…・K1069掃引22953ae1…・sv17 c1073bae…）で検証して
  fail-closedに読み込む。resolve6.pyのフル再実行（universe再構築）も
  候補根の新規判定も行わない。（2）構造gate: witness_full 39 root×2行の
  covered unionは78行で重複0・base_state.residual_row_hex(78)と完全一致。
  fold9閉鎖4行⊂78・fold10 target閉鎖2行⊂78・6行はdisjoint・
  78−4−2=72がfold10正本の残余72行と完全一致。fold10が閉じた3行目
  （00004000000000003800000100000020）は78行計画外のtarget外extra行。
  sv17正本のcoverage claim 2行==fold10 target閉鎖2行（幾何再導入と
  triple検証の独立一致）。（3）retire後割当: 十七root retire後の38 live
  rootの割当は34 root×2行+4 root×1行=72行で、残余72行の全行がちょうど
  1 rootに割当済み（1回被覆維持・multi-cover 0）。fold9で閉じた4行の
  割当rootを特定（…08001220・…80122201000001000・…8012020800…系4 rootが
  各1行に劣化）。（4）K1069交差: 分類正本の39 root==witness 39 root・
  WIN rootは十七rootのみ・残38 live rootはすべてREFUTED-D10。
  よって残余72行の全行が depth-10 witness として使用不能な
  REFUTED-D10 根への割当のみとなり、**39-root計画からの残余72行への
  depth-10 witness供給はゼロ**と確定（K1069 READMEの使用不能記述の
  行単位・割当単位での厳密化）。残余72行の閉鎖にはfresh-safe poolの
  再照合（resolve6.py再実行・単一オーナー宣言必要）・add-two-stones
  拡張・depth>10探索・他の証明書供給が必要。（5）決定論: stdlibのみ・
  2回実行+別cwd別プロセスでbyte-identical（正本SHA-256 207f4094…）・
  27 gate全PASS。（6）解釈規約: 本項は1行も閉じず1根も判定しない。
  REFUTED-D10はLOSS証明ではない。「供給ゼロ」は39-root計画スコープの
  観察でscope外の閉鎖機構を否定しない。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**
---

## 詳細

K1071（fold10）で残余74→72行・39-root witness計画の十七rootがretireした
直後の状況を、出版済み5正本のみを使って再照合した（単一オーナー宣言ノート
を先行出版・resolve7）。

主結果は3点: (1) 残余72行が78行計画からfold9の4行とfold10の2行を除いた
集合と過不足なく一致し、fold10の3行目の閉鎖が計画外extra行であることを
正本演算で確定。(2) retire後の38 rootの割当表は34×2+4×1=72行で1回被覆性を
維持し、fold9閉鎖4行の割当root4本を特定。(3) K1069掃引との交差で
現存38 live rootがすべてREFUTED-D10であり、**この39-root計画が残余72行に
提供できるdepth-10 witnessはゼロ**になったことを72行全行について確定。
次の一手はfresh-safe pool（resolve6.py再実行・単一オーナー宣言必要）か
候補空間の拡張（add-two-stones・depth>10）である。
詳細は[実験](../../experiments/n11-residual72-postfold-witness-recheck-20261120/README.md)・
[再照合正本](../../experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-postfold-witness-recheck.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
