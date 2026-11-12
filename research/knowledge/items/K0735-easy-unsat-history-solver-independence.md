---
id: K0735
title: 候補B の易 UNSAT は学習節の履歴に依存せず、ソルバ横断でも d に応じた範囲で再現する
kind: verification
status: verified
topics: [geometry, maximum-safe, verification]
aliases: []
relations:
- type: verifies
  target: K0769
  note: 候補B 分割の適用に対する独立性検証
- type: depends_on
  target: K0768
  note: 掃引記録
- type: depends_on
  target: K0772
  note: 同一符号化の基数制約
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/reverse_order_probe.py
  role: verifier
  note: 逆順と fresh-each の再解器
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w11-artifact-reverse.json
  role: data
  note: 逆順 8 点の判定
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w11-artifact-fresh.json
  role: data
  note: 履歴ゼロ 4 点の判定
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/tail_fresh_probe.py
  role: verifier
  note: 尾部 fresh-each と unit_conflict/統計の計測
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w17-tail-fresh.json
  role: data
  note: 尾部 5 点 UNSAT・境界 3 点 UNKNOWN
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/cross_solver_probe.py
  role: verifier
  note: 交差ソルバ実行器
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w14-cross-solver.json
  role: data
  note: d=1/100/300/478/851 のソルバ表（54 レコード）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w18-tail-cross-solver.json
  role: data
  note: d=1280/1300/1316/1317（47 レコード）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w19-1316-cross-rest.json
  role: data
  note: d=1316 の残り 9 種
scope: p=2647・size=1322・クラス (1,1,3) の候補B符号化、conflict 予算 100k。壁時計 cap は検証ごとに異なる（本文に明記）。同一符号化の範囲内の検証。
evidence: fresh-each 再解（W11/W17）と 14 種ソルバの交差実行（W14/W18/W19）の保存 JSON を全件実読した。
---

## 検証内容

(a) **履歴非依存**: 履歴ゼロの新規 Cadical195（fresh-each）で再解すると、
掃引で UNSAT だった 9 点（d=1,300,478,851 / 1280,1290,1300,1310,1316）はすべて UNSAT、
掃引で UNKNOWN だった 3 点（1317,1322,1200）は UNKNOWN で、conflict 予算 100k を
使い切る。別途、単一インスタンスを降順 `[1322,1000,851,500,478,300,100,1]` で回す
shared-reverse でも UNSAT は 1/300/478/851、UNKNOWN は 100/500/1000/1322 で
記録と一致する（この mode は「履歴を逆から積む」検査であり、履歴ゼロの検査ではない）。
`unit_conflict` は全点 false で、「即 UNSAT」は伝播閉包ではなく
565〜33,464 conflicts の探索による（1280-1310 は 10³ 級、1316 は 3.3×10⁴）。

(b) **ソルバ横断**: d=1/300/478 は 14 種中 13 種が UNSAT（Cadical195 を除いて 12 種、
MapleChrono のみ timeout）。d=1280/1300 は 14 種中 13 種 UNSAT（除く 1 種は MapleChrono）。
d=1316 は 14 種中 **9 種 UNSAT / 5 種 timeout**（240 秒壁時計、予算未到達）。
d=851 は試行 7 種中 4 種 UNSAT。d=1317 は 14/14 が timeout（120 秒、予算未到達）。
d=100 は 5 種すべて UNKNOWN か timeout。

## 限界

- 全モードが**同一のクラス CNF**（候補B）・同一 conflict 予算（100k）。
  壁時計 cap は d ごとに違う（W14 は 120 秒、W18 は 1280/1300/1317 が 120 秒・
  1316 が 240 秒、W19 は 1316 が 240 秒）。排除できたのは「学習節の履歴依存」と
  「Cadical195 固有性（d に応じた範囲で）」であり、**符号化の同一性は残る**。
- 「ソルバ非依存」は d について一様でない（1316 は 9/14、851 は 4/7）。
  本項は数表を伴う範囲限定の主張である。
- 交差ソルバの timeout は壁時計打ち切りで UNSAT と数えない。
  fresh-each の UNKNOWN は conflict 予算切れ。この2種を混同しない。
- 外部バイナリ（DIMACS 経由）の実行は未実施（Kissat404 は unit 節方式で、
  厳密には同一入力形式ではない）。
