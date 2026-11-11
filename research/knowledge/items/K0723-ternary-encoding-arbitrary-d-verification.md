---
id: K0723
title: ternary 符号化の d 一般化実装は d=1323 で現行と同一の CNF・同一探索を再現し、任意 d で節生成が健全
kind: verification
status: verified
topics: [geometry, maximum-safe, search-methods, verification]
aliases: []
relations:
- type: verifies
  target: K0712
  note: 三値還元の一般 d 実装の検証
- type: generalizes
  target: K0712
  note: d=1323 固定の保存CNFから任意 d の再生成へ
- type: supports
  target: K0717
  note: 候補A/三値系の一般化が次の測定の前提になる
artifacts:
- path: research/experiments/parabola-ternary-selection-20261109/ternary_general.py
  role: solver
  note: d を引数化した三値符号化の生成器
- path: research/experiments/parabola-ternary-selection-20261109/output/generalization-check-d1323-target1322-budget100000/init.json
  role: data
  note: base 53,886 節一致の記録
- path: research/experiments/parabola-ternary-selection-20261109/output/generalization-check-d1323-target1322-budget100000/result.json
  role: data
  note: 統計完全一致・UNKNOWN
- path: research/experiments/parabola-ternary-selection-20261109/output/generalization-check-d300-target1322-budget100000/result.json
  role: data
  note: SOLVER_UNSAT 1.811 s / 1,808 conflicts
- path: research/experiments/parabola-ternary-selection-20261109/output/generalization-check-d300-target1293-budget100000/result.json
  role: data
  note: UNKNOWN 90.207 s / 142,992 節
scope: ternary_general.py の実装検証。符号化の数学的正当性は K0712 の全称証明が担い、本項は実装の一致と健全性の検査範囲に限る。
evidence: d=1323 でのバイト一致と探索統計の完全一致、p=5,7,11,13,17 の全 d・全三値割当 19,392 件の評価一致、p=17 の SAT 経路 64 件の照合（W16 ログ §4・§5・§9）。
---

## 検証内容

`ternary_general.py` は d を引数化して固定完全対 d の三値符号化を生成する。

(i) d=1323・target=1322 では、生成した base 節集合は節内を (abs,lit) 順・
節を辞書順に正規化した後で保存 CNF の 53,886 節と一致し
（base SHA `0f09fc6e…2ff0b3`）、生成 CNF（7,926 変数 / 68,404 節）は既存
`input.cnf.gz` と **gz バイト列まで一致**（`encoded_cnf_sha256 = 8cbd404a…b9f48a`）。
100k 予算の探索統計は既存実績と完全一致
（conflicts 100,001 / decisions 217,401 / propagations 50,404,659 / restarts 4,854、UNKNOWN）。

(ii) edge リストの d 非依存性は、p=5,7,11,13,17 の全 d・全三値割当 19,392 件で
`clauses_for_pair(full)` と `clauses_for_pair(kept)` の評価、および整数幾何の
禁止四点判定が全一致（不一致 0）。kept ⊆ full で、差分 874,503 はすべて
同一 pair の2点を含む台形辺。

(iii) d=300 では、target=1322 が **SOLVER_UNSAT**（1.811 秒、conflicts 1,808、
予算未満 = 打ち切りでない反駁。Glucose4 と Minisat22 で独立に UNSAT）、
target=1293 が UNKNOWN（90.207 秒、142,992 節 / 45,249 変数）。
SAT 経路は p=17 の全 d・全 target 64 件でモデル再構成と整数幾何安全性を確認。
CLI は d∈[1,1323]、target∈[3,1325] を検証し、既存出力を上書きしない。
既存 regression（19,392 割当・444 cardinality ケース）も全項目一致。

## 限界

- これは**実装の検証**であり、符号化の数学的正当性は K0712 の全称証明が担う。
- 保存 CNF は d=1323 でフィルタ済みの産物であり、別 d では再生成が必須
  （保存ファイル単体からは復元できない情報がある）。
- d=300/target=1322 の UNSAT は「±300 を含む 1322 点安全集合が存在しない」であって、
  Q_2647 全体の UNSAT ではない。かつ DRAT 監査前の `SOLVER_UNSAT`。
- 難易度の d 依存（1323 は UNKNOWN、300 は 1.8k conflicts）は実測事実で、
  機構の説明ではない。
