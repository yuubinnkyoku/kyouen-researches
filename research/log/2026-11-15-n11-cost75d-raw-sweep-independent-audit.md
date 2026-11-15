# 2026-11-15：cost-75d raw sweepの第二独立監査（WIN7-D10 4件〔bits 12/40/92/111〕・71 REFUTED・0 capped・候補幾何・head 1277 bookkeeping 全部PASS）

本セッションは head 1277 の全16 receipts の第二独立検証を完了した後、並走class2 laneが着地したばかりの **cost-75d raw sweep（commit `2b5482c2`）** を、並走自身のaudit・証明書がまだmainに無い段階で、published main成果物のみから独立に監査した。監査script `scripts/audit_cost75d_raw_sweep_independent_20261115.py` は純Python標準ライブラリのみで、本監査専用に書き下ろした Bareiss 4x4 整数行列式と独立な8要素D4盤面群の正準化を実装する（repo engine/solver/cache不使用・浮動小数点なし）。

## 対象

- child S6 `00000000000040801202000000200000`（stones [21,49,57,60,71,78]・第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-75行・head 1277 claim）
- raw batches 1-10（75候補・9×8+1×3）+ batch-5 v16 determinism rerun
- 監査入力はすべてmain上の成果物のみ（claim JSON・raw batch 11ファイル・head 1277 JSON・ranking CSV・top-candidates CSV）

## 結果 — 全チェックPASS（2回実行でaudit JSON byte-identical・md5 `9766a581078a45f56ad68e51d45f4219`）

幾何（すべて独立再導出）:
- child stones [21,49,57,60,71,78]（LSB bit規約）・childはD4-canonical。
- **合法候補75件の独立列挙がclaimとbit-exact一致**（6石の任意3組と退化4組を作る空マスをBareiss 4x4で全列挙除外）。edge cost 75 == 候補数。
- **6つの1石削除のD4正準形がpublished 6 orbit hexと全件一致**（独立D4群）・6 orbit相異・lift 78の直接削除がopen parent S5とbit-exact。
- head 1277 bookkeeping: parent1はbest coverable class-2 target 17/1325・ranking CSVでも2/17/1325・**残り5 orbitはopen rankingに不在（head 1277で閉鎖済み）**・top-candidates CSV行（s5=parent1, s6=child, cost 75, demand c1=0,c2=1,c4=0）一致。

raw sweep集計:
- 10バッチ各pilot 3402/loss=false/capped=false・候補はclaimの75件とexactly-once。
- **WIN7-D10 bits = [12, 40, 92, 111]**（すべてcapped=false）・71 REFUTED-D10・0 capped・全terminalStoneRange [13,17]。
- 候補nodes合計 **143,552,593**（commit messageと一致）+ pilots 34,020。
- batch-5 determinism rerunはms以外完全一致。

## 備考：node集計規約の横断差

cost-74hのcommit messageは candidates+pilots（72,720,136）を、cost-75dのcommit messageは candidatesのみ（143,552,593）を指す。両規約をaudit JSONに明示記録した（`candidate_nodes_excluding_pilots` / `total_nodes_including_pilots`）。以後のsweep logはどちらの規約かを明記するとよい。

## 信頼境界

- 本監査は**raw recordレベルの再集計・幾何再導出**であり、143,552,593 nodesの探索自体を再実行したものではない。
- **WIN7-D10 4件の証明書は未着地**（並走laneのcertificates and v15 crosscheck to follow）。本監査は証明書の正しさには一切言及しない。fold着地まではfrontier不変（head 1277）。
- 71 REFUTED-D10は深さ10以内のWIN不在のみを意味しLOSS証明ではない。solved数はmanifest被覆の簿記。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4はいずれもUNKNOWN**。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost75d_raw_sweep_independent_20261115.py   # ALL CHECKS PASS
```

mainのみから実行可能（所要数秒）。出力 `output/class2-lane-cost75d-raw-sweep-independent-audit-20261115.json`（8,950 bytes）。
