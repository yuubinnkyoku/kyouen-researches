# 2026-11-18 n11 rank-1 parent head-1476 再照合の検証側クロスチェック

## 背景

並走レーンが head-1476 での rank-1 partial-STERILE parent
`00000000000000801202000040000000` の再照合を出版した
（verifier `reconcile_rank1_parent_head1476_20261118.mjs`・result
`rank1-parent-head1476-reconciliation-20261118.json`・47/47 checks PASS・二重実行byte-identical）。
本レーンの前回契約（fold記録の交叉検証は検証側に回る）に従い、
この新規出版を独立実装でクロスチェックした。

## 実施内容

`crosscheck_rank1_head1476_reconciliation_20261118.py` は、
全入力をgit blob SHA1ピンで固定してmainの生ファイルから取得し直し、
第四実装のD4（11×11座標変換8種）で次を独立再導出した。

- K0865 census の parent entry（partial_sterile・rem 5・effRem 3・effCost 229・
  STERILE refs 71/64）・effective worklist 第1位・census totals 174/3/57/114/91/12274/12183
- 生のhead-1410 worklist 6,438行からのorbit join再計算（5行・cost計364・
  STERILE 2行/135・非STERILE 3行/229・分類はworklist categoryと一致）
- D4 canon実装の目撃検証: cost76c bit61・bit99の両派生canon rootが
  出版記録と厳密一致（座標規約の転置不変性もこの一致で裏付け）
- fold連鎖のheadセグメント算術:
  cost76d+77e 1450→1452（-153 = 76+77・rows -2）・
  cost76c bit61 1472→1473（-76・rows -1）・
  cost66i bit19 1473→1476（-207 = 3行・rows -3）
- 各receiptのcovers/marginal集合算術:
  全4 receipt（bits 19/49/37/69）で covers == canon(root − 1石) の7集合と厳密一致、
  marginal ⊆ covers・marginal_manifest ⊆ marginal・
  marginal_manifest の和 == rows_closed == {76d行, 77e行}
- 証明書のbyteレベル再ハッシュ（raw CDN・ピンコミット固定）:
  76d bit19/bit49（whole）・77e bit37/bit69（part1+part2結合）・
  76c bit61（whole）・66i bit19（part結合）の計6枚すべて
  sha256・md5・bytes・git blob sha（76d/76c）がfold/manifest記録と一致・
  行数 == rows + 2（ヘッダ+root行）
- K0863整合性のconflict scan:
  6つのfold済みWIN7-D10 root（およびその1石減算位置の全D4像）は
  どちらのSTERILE行もcoverしない（WIN/REFUTED矛盾なし）
- mjs verifierの静的チェックセット照合:
  PINS表19件 + リテラル28件 == result JSONの47 check名と完全一致・
  mjsのPINS表は再照合JSONのinputsピンと同一
- 再照合result JSONの全主要fieldを上記再導出値と照合
  （historical 29 checks・fold 3セグメント・current_parent head 1476・
  残2行 == STERILE refs == orbit join − fold閉鎖3行・bit群
  [19,37,49,61,69,99] / [19,37,49,61,69] / fallback [99]）

**結果: 84/84 checks all PASS・別プロセス2回実行でbyte-identical**
（script git blob `f23200026114fc42d2d5fc37fcb9498703abe1a7`・
result JSON 13,621 bytes・sha256 `6801393e4e9cbf0b48975607d41d94791242865c59da5ab4abf5205007673c8b`）。

## 結論

並走のhead-1476再照合は、入力ピン・orbit join・fold簿記・証明書ハッシュ・
静的検証器構造のすべての層で独立実装と一致した。
rank-1 parent `00000000000000801202000040000000` のhead-1476残行は
STERILE 2行（cost 71/64・計135）のみであり、D10 receipt体系では
閉鎖不能（K0863）。S5 parent自体は未解決のまま。

## 解釈上の制限

STERILEもREFUTED-D10もLOSS証明ではない。本クロスチェックは
簿記と証明書の検証であり、新しい探索・verdict・parent閉鎖を生成しない。
標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、
class 1/2/4はすべて**UNKNOWN**のまま。

## 公開物

- verifier: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/crosscheck_rank1_head1476_reconciliation_20261118.py`
- result: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/rank1-parent-head1476-reconciliation-crosscheck-20261118.json`
- 被検証対象: `rank1-parent-head1476-reconciliation-20261118.json`（並走・`cb7769314a`出版・本logにも記録）
