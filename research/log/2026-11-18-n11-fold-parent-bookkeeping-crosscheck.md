# 2026-11-18 n11 三fold記録のper-parent簿記クロスチェック（9 S5 parent）

## 背景

head-1410 から head-1476 へのfold連鎖
（cost76d+77e 1450→1452・cost76c bit61 1472→1473・cost66i bit19 1473→1476）は
いずれも S5 parent の remain 行を閉じてfrontierを進めた記録だが、
前回のrank-1再照合クロスチェック（同日log参照）は
fold記録のheadセグメント算術とreceiptのorbit被覆を検証したものであり、
**parent単位の簿記**（どのparentから何行・何costが閉じ、
閉鎖前行数がhead-1410の生orbit joinと整合するか）は未検証だった。
本logは、3つのfold記録 `parents_after` に現れる
9つの S5 parent 全てについて、生のhead-1410 worklist
（6,438行・git blob `2fee1d07...`ピン固定）から
第四実装のD4 orbit joinを再計算し、fold記録のparent簿記を独立検証した。

## 実施内容

`crosscheck_fold_parent_bookkeeping_20261118.py` は、全7入力
（worklist・3 fold記録・2 claim記録・head-1476再照合result）を
git blob SHA1ピンで固定し、次を検証した。

- parent universe: 3 foldの `parents_after` の和集合 == 9 parent、
  すべてpopcount 5・worklist上にchildを持つ
- fold76d77e: 76d行 ∈ join(A) ∩ join(P)、77e行 ∈ join(B) ∩ join(P)、
  非交差（76d ∉ join(B)・77e ∉ join(A)）。
  A: 65行/5358 が join1410 と厳密一致（-1行/-76）。
  B: rows_before 72 ≤ join1410 74行、差2行/153costは
  76d・77e閉鎖（fold自身）と整合。
  P: 5行/364 がjoin1410と厳密一致、-2行/-153 = 76+77
- fold76c: 4 parent全てで lost_rows_hexes ⊆ join1410(parent)、
  lost cost総和 == lost_edge_cost、
  rows_after == rows_before - lost_rows、
  edge_cost_after == edge_cost_before - lost_edge_cost。
  lost行の和集合 == {76c行, 76d行, 77e行}（worklist categoryは
  すべて非STERILE: transfer_partial / win_pending 等）。
  receiptのmarginal_manifest 5行 ⊆ canon(root61 − 1石) の7行
  （orbit被覆の目撃確認）
- fold66i: receiptのmarginal_manifest 3行は
  ①canon(root66 − 1石) の7行に含まれ、かつcanon不動点、
  ②worklist上でcost 66/75/66・総和207 == totals。
  **5 parent全てについて、閉鎖行をjoin membershipから独立に導出**し、
  記録された lost_rows / lost_edge_cost と厳密一致
  （parent-incidence 7 = H:2・I:1・E:1・F:1・G:2・unique行3）。
  basis鎖 1473→1476・frontier_after
  `1476/174/6372/504389/4645/368303` がclaim66i・head-1476再照合resultと一致
- baseline差分（join1410 − rows_before）を9 parent全てで非負検証し、
  事実表として記録: A/Pはfold76d77e時点で差0、
  Bは76d77eで-2行/-153、fold76cでは-4行/-311
  （中間fold 1452→1472の効果は再導出せず事実として記録）、
  66i側 H/Gは差0・Iは2行・Eは12行・Fは5行

**結果: 29/29 checks all PASS・別プロセス2回実行でbyte-identical**
（result JSON sha256
`c4b1b88ec1a159d49fe3a120d38d132d02074088197ce182dc14463f64b88568`）。

## 結論

3つのfold記録が触れる9 S5 parentすべてについて、
閉鎖行のparent所属（D4 orbit membership）・cost算術・
rows_before/afterの整合、およびreceiptのorbit被覆が
生worklistからの独立再導出と一致した。
特にfold66iは閉鎖行を記録からでなくjoin membershipから導出して
突き合わせており、7 parent-incidence / 3 unique行 / cost 207の
incidence構造を独立実装で確認した。
rank-1 parent `00000000000000801202000040000000` は
head-1476でSTERILE 2行のみ（K0863・D10 receiptでは閉鎖不能）、
S5 parentはいずれも未解決のまま。

## 解釈上の制限

本クロスチェックは簿記検証であり、新しい探索・verdict・parent閉鎖を
生成しない。baseline差分（中間foldによる閉鎖分）は
再導出せず観測事実として記録した。REFUTED-D10もSTERILEも
LOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、
S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。

## 公開物

- verifier: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/crosscheck_fold_parent_bookkeeping_20261118.py`
- result: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-parent-bookkeeping-crosscheck-20261118.json`
- 被検証対象: cost76d77e / cost76c / cost66i の3 fold記録（並走出版）
