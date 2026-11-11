---
id: K0727
title: blocker-obligation-fill DFS: 5×m・q=7 欠損行クラスの極大安全配置を完全列挙する機械
kind: method
status: active
topics: [rectangles, variants, maximal-safe, verification]
aliases: []
relations:
- type: depends_on
  target: K0726
  note: 欠損行blockerの候補は5×19の7-8点円census（95本）に限る
- type: verifies
  target: K0302
  note: 5×18のrepo既知witnessを座標まで完全再現
- type: supports
  target: K0332
  note: M_{5,7} 厳密決定に向けたoccupancyクラス別全ケース列挙キャンペーンの中核機械
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/five_row_q7_blocker_dfs.ts
  role: source
  note: 機械本体。MODE='single' で単一S0、MODE='campaign' + START でスライス実行
- path: research/experiments/five-row-q7-m19-20261110/scripts/slice_runner_class0.ts
  role: source
  note: クラス{0} スライスrunner（双方向・global NODE_CAP）
- path: research/experiments/five-row-q7-m19-20261110/scripts/slice_runner_class1.ts
  role: source
  note: クラス{1}（行1欠損）スライスrunner（Y0=1、葉fillは行0から）
- path: research/log/2026-11-11-m57-blocker-obligation-fill.md
  role: log
  note: 機械開発・検証・キャンペーン開始の記録
---

# blocker-obligation-fill DFS（5×m・q=7 欠損行クラス完全列挙機械）

5×m・q=7 の「欠損行が ≤5 石・他行ちょうど6石」occupancy クラス
（欠損行を Y0 ∈ {0,1,2} とし、行鏡映で {0}≡{4}、{1}≡{3}）における
極大安全配置の完全列挙機械。soundness と completeness を併せ持つ:

- 前置決定: S0 ⊆ {0..m−1}（欠損行の石列）。欠損行の残点は強制空。
- 欠損行の各空点は blocker 曲線を1つ持つ必要がある。blocker は
  census（K0726）内の 7点円/8点円または行直線に限る:
  - 7点円 blocker → 円上の残り6点は強制石。
  - 8点円 blocker → 「7候補中 ≥6 石」obligation。2点既に強制空で fail、
    1点なら残り未知点は強制石、0点なら候補1点を eager 分岐（1点を空・残り石）。
- 伝播: 行cap（欠損行=5・他行=6。超過 fail、飽和で行内未確定点を強制空）、
  円石数 ≤6（超過 fail）、円飽和(=6)で円上の未確定点を強制空。
- 葉（欠損行の全空点に blocker 割当済み）で残り行をちょうど6石に fill。
- 円の重複排除キーは中心 AND 半径。(Ux,Uy,D) を gcd 正規化後、
  R2n/R2d を別々に gcd 正規化する（同時正規化はスケール不変でなく誤り）。

検証（5×18, S0={5,8,12,14,17}）: 49,162 ノードで完走し、repo の 5×18 witness
（research/experiments/fixed-width-frontier-20261005/output/q57_independent_witness.json
の行データ）を座標まで完全再現。機械の soundness・completeness を端から端まで検証。

追加の独立検証済み結果:
- 5×18 の2個目の witness（鏡映非同値）:
  rows = [[0,1,2,6,14],[4,7,9,11,13,16],[2,4,7,11,13,16],[3,5,7,10,11,15],[7,8,10,12,13,17]]。
  29石・行占有 (5,6,6,6,6)・全95 census円 ≤6石・全空点 blocked
  （行0の13空点はすべて8点円 blocker）。独立検証器 PASS。
- S0={5,8,12,14,17} は 5×18 では witness を生むが、5×19 では
  769 ノードの完全探索で witness 0（証明的不存在）。

キャンペーン運用: canonical 順（k=5→0、辞書順、鏡映代表）でケース列挙し、
スライス単位で global NODE_CAP（600k）を課す。ノード数はスライス1回の
global累積とすること（ケースごとのリセットは process safety deadline 超過の原因）。
capped ケースは次スライス先頭で再挑戦すれば成功する。
各スライスは START..nextIdx を正確に報告するため、gap・overlap は
事後に厳密に再構成でき、overlap 区間の再実行は二重検証になる。

限界: 機械は盤・occupancyクラスごとの有限列挙であり、クラス横断の全パターン
完了前に M_{5,7} の値は確定しない。クラス{0}の全ケース完了は K0728 に記録。
クラス{1}・{2}・複数行欠損クラスは進行中。
