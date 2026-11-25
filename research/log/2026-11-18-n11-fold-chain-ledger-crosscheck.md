# 2026-11-18 n11 fold連鎖 head-1410→1476 全台帳クロスチェック（B親の二重計上を検出）

## 背景

head-1410（worklist 6,438行）から head-1476（`1476/174/6372/504389/4645/368303`）への
fold連鎖は、`n11-s2-5960-ms5-s7-reuse-20261113/output/` に出版された
10個のreceipt-fold記録で構成される:
cost65j (1410→1419)・cost64d (→1435)・cost64f (→1438)・cost64g (→1441)・
cost65n (→1444)・cost66c (→1450)・cost76d77e (→1452)・cost64h (→1472)・
cost76c (→1473)・cost66i bit19 (→1476)。
これまでの検証（同日のrank-1再照合・per-parent簿記の両クロスチェック）は
直近3 foldの記述的内容にとどまり、head-1452→1472を担うcost64h（23 receipt・
20行閉鎖）や、全連鎖にわたるparent単位のクロス記録整合は未検証だった。
本logは、10記録すべてを生worklistから独立検証した。

## 実施内容

`crosscheck_fold_chain_ledger_1410_1476_20261118.py` は、全11入力
（worklist・10 fold記録・head-1476再照合result）をgit blob SHA1ピンで固定し
（fold記録はcommit `376e4f44` でSHA固定取得）、次を検証した。

- 連鎖の連続性: 10記録のbasis→after が 1410→1476 で厳密に接続し、
  basis の cost/uniq が前段の frontier_after と一致。
  他に (1410, 1476] にhead区間を持つ出版記録は存在しない
- 境界: cost60c (1407→1410) の frontier_after（6,438行・509,109）が
  worklistそのものであり、60cが閉じた3行はworklistに存在しない
- 各記録の閉鎖行: 旧形式（lost_rows_per_parent）・新形式
  （parents_after.lost_rows_hexes）の両記法から抽出し、
  head差分（9+16+3+3+3+6+2+20+1+3 = 66行）と厳密一致。
  cost76c の lost 行は累積列記を含むため、先行記録の閉鎖と差し引いて
  1行（76c行）と特定し、再列記行（76d・77e行）が先行記録で閉鎖済みなことを検証
- 全66行の大域非交差性・worklist内存在・総閉鎖cost 4,720（= 509,109 − 504,389）
- 帰属性: 66行の全parent帰属（38 parent・全D4 membership検証）、
  全parentのcanon性・popcount 5
- **絶対台帳**: 各parentの join1410（5-subset canon indexで全6,438行から再構築、
  直接joinでの9親セルフテスト一致）から累積閉鎖を差し引いた
  rows_before/rows_after・edge_cost の期待値を、10記録の全parentエントリと照合
- head算術: 各記録のfrontier_after（solved・unique_remaining・sum_remaining_cost）が
  worklistの累積閉鎖から厳密に導出される（10点すべてで一致、終点 1476/6372/504389 は
  head-1476再照合resultと一致）
- cost64h: parent_row_incidences 42・parent_edge_cost_delta 3,090（incidence加重）が
  帰属表と一致（20行の閉鎖costは1,472 = head差分）
- cost66i: 5親の lost_rows/lost_edge_cost がreceiptのmarginal manifest ∩ join(p) から
  独立導出と一致

**結果: 57/57 checks all PASS・別プロセス2回実行でbyte-identical**
（result JSON sha256
`25b4422101559759304471b45f4e7d5d1e2a04ee2b62816863c49806d3a708ac`）。

## 検出した不整合（新規・検証側の所見）

**cost76c記録の parent B `00000000000000801202000000040000` エントリが
77e行を二重計上している。**

- Bの正確な閉鎖史（全記録の台帳から再構成、各点でjoin1410と厳密整合）:
  cost64d で2行（cost 153・74→72）→ cost76d77e で77e行（72→71）→
  cost64h で1行（cost 81・71→70）
- ところが cost76c の B エントリは rows_before 70（post-64h）に対して
  lost_rows_hexes = [77e行]（head-1452で既に閉鎖済み）を再度閉鎖として適用し、
  rows_after 69 / edge_cost_after 5,725 と記録。
  **正しい状態は 70行 / 5,802**
- 76c行（このfoldが実際に閉じた唯一の行）はjoin(B)に含まれない
  （D4子であるのは P と E のみ）ことを直接計算で確認
- 大域head算術（1473/6375/504596）には影響しない: foldの大域閉鎖は
  76c行の1回のみ正しく計上されている
- 修正提案: Bエントリを lost_rows 0 / lost_rows_hexes [] / lost_edge_cost 0 /
  rows_after 70 / edge_cost_after 5,802 に修正
  （または1410起点の累積形式に統一: rows_before 74・lost_rows_hexes は
  76d・77e・64d2行・64h1行の計5行）

この所見はper-parent bookkeeping上の誤記であり、fold自体の妥当性・
証明書・大域frontierには影響しない。なお、前回のper-parent簿記クロスチェック
（同日log）が検証したのは各記録の内部的算術とmembershipであり、
このBエントリも内部的には整合していた（70−1=69・77=77・77e∈join(B)）ため
検出され得なかった。連鎖横断の絶対台帳をはじめて構成したことで検出された。

## 解釈上の制限

本クロスチェックは簿記検証であり、新しい探索・verdict・parent閉鎖を生成しない。
rank-1 parent `00000000000000801202000040000000` は head-1476 でSTERILE 2行のみ
（K0863・D10 receiptでは閉鎖不能）。REFUTED-D10もSTERILEもLOSS証明ではない。
標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、
class 1/2/4はすべて**UNKNOWN**のまま。

## 公開物

- verifier: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/crosscheck_fold_chain_ledger_1410_1476_20261118.py`
- result: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json`
- 被検証対象: cost65j/64d/64f/64g/65n/66c/76d77e/64h/76c/66i の10 fold記録（並走出版）
