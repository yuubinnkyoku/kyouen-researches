---
id: K0707
title: 旧増分DRATチェッカーは節削除後の古い代入により偽UNSAT証明を受理する
kind: proposition
status: computed
topics: [verification, certificates, provenance]
aliases: []
relations: []
artifacts:
- path: research/experiments/drat-deletion-soundness-20261109/README.md
  role: source
  note: 偽受理の機序、修正、既存監査への影響と限界
- path: research/experiments/drat-deletion-soundness-20261109/sat.cnf
  role: data
  note: 単位節1のみの充足可能な最小入力
- path: research/experiments/drat-deletion-soundness-20261109/invalid.drat
  role: data
  note: 旧版が誤受理する4行の偽UNSAT証明
- path: research/experiments/drat-deletion-soundness-20261109/regression.py
  role: verifier
  note: 旧版・修正版・素朴版のソースビルドと偽証明・正例の比較
- path: research/experiments/drat-deletion-soundness-20261109/regression.json
  role: data
  note: 13ケースの実行結果とソース・入力ハッシュ
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp
  role: verifier
  note: 削除時に代入を失効する修正版。一般健全性の証明ではない
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/audit_all_d.py
  role: verifier
  note: 検査器ソースhashごとに旧レシートとバイナリを分離する再監査ドライバ
scope: main a7bdd689 の増分DRAT実装の具体的な偽受理と、修正版の有限回帰。p=2207/2531の幾何命題の反証ではない。
evidence: ソースからビルドした旧版は充足可能な4入力の偽UNSAT証明を全て受理。修正版と素朴版は全て拒否し、正例も一致。
---

## 命題・範囲

旧 `drat_check_incremental.cpp` は、削除済み単位節から導いた level-zero 代入を
後続の RUP 検査でも使うため、充足可能な CNF に対する偽 UNSAT 証明を受理する。
`sat.cnf` と `invalid.drat` が自己完結した反例であり、ソルバを必要としない。

具体的には `{1}` から `{2}` を追加するとキャッシュに `1=true` が残る。
`{1}` を削除して `{-1}` を追加することは充足可能性を保つが、旧実装はキャッシュとの
矛盾で空節を受理する。素朴版は代入を毎回作り直し、空節を拒否する。

## 現在の根拠と限界

ソースからビルドした旧版・修正版・素朴版で13ケースを比較した。
4個の偽証明は旧版のみ受理し、修正版と素朴版は7合成ケースと6小実証明で期待通り一致した。
修正は削除時に全代入を失効させる。これは当該不具合の有限回帰であり、
修正版チェッカー全体の数学的健全性や任意の不正入力への安全性を証明するものではない。

K0693/K0702 の旧 DRAT VERIFIED 件数は独立検証済みの証拠として採用を保留する。
既存幾何命題・CNF UNSAT のソルバ主張を反証したわけではなく、両項は `needs-review` のまま。
旧レシートを新検査器の結果に混ぜず、検査器ソースhashごとの新しい監査を行う。
