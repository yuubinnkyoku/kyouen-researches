---
id: K0380
title: 11×11既知S5 LOSSの分割証人探索は小予算で節点削減を示さない
kind: computation
status: observed
topics: [square-outcomes, search-methods, provenance]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の交互AND/OR勝敗伝播
- type: depends_on
  target: K0371
  note: 固定先手の層別伝播規則
- type: depends_on
  target: K0372
  note: solver exact値とterminal-only独立証明の信頼境界
- type: depends_on
  target: K0375
  note: 既知S5 LOSS六根と共有TT比較の元資料
- type: depends_on
  target: K0378
  note: 六根terminal-only独立証明DAGと監査receipt
- type: supports
  target: K0379
  note: 小予算のS5/S6分割比較でも探索節点削減が確認されない
artifacts:
- path: research/experiments/n11-s5-loss-witness-20261012/README.md
  role: source
  note: 固定比較条件、結果、制約、次の計測条件
- path: research/experiments/n11-s5-loss-witness-20261012/input/targets.json
  role: data
  note: K0375の既知S5 LOSS六根、raw provenance、独立証明source SHA
- path: research/experiments/n11-s5-loss-witness-20261012/input/s6-candidate-schedule.json
  role: data
  note: solver実行前に固定した幾何のみのS6候補と順序
- path: research/experiments/n11-s5-loss-witness-20261012/input/build.json
  role: manifest
  note: compiler・flags・solver sourceと未追跡binaryのSHA-256
- path: research/experiments/n11-s5-loss-witness-20261012/scripts/prepare_candidates.py
  role: source
  note: rawと独立証明receiptをSHA照合しS6候補を列挙
- path: research/experiments/n11-s5-loss-witness-20261012/scripts/benchmark_witness_methods.py
  role: source
  note: 5方式の同binary・同cache初期状態・同node上限比較
- path: research/experiments/n11-s5-loss-witness-20261012/scripts/check_stop_on_loss.py
  role: verifier
  note: 4×4でexact LOSS後停止、UNKNOWN継続、既定挙動を回帰検査
- path: research/experiments/n11-s5-loss-witness-20261012/tests/test_witness_schedule.py
  role: verifier
  note: 固定六根、geometry順序、共通node capの単体試験
- path: research/experiments/n11-s5-loss-witness-20261012/output/common-budget-v1/summary.json
  role: data
  note: A-E各150万nodeの勝敗・wall・最大RSS・cache測定
- path: research/experiments/n11-s5-loss-witness-20261012/output/stop-on-loss-reproduction-v1/receipt.json
  role: manifest
  note: 早期停止flagの3 assertion成功receipt
- path: research/experiments/n11-s5-loss-witness-20261012/output/regression-fixture-development.json
  role: data
  note: 不適切fixtureを含む試行のnode数・結果・raw SHA記録
- path: research/experiments/n11-s5-loss-witness-20261012/output/final-sha256.json
  role: manifest
  note: 実験入出力のSHA-256一覧
- path: research/log/2026-10-12-n11-s5-loss-witness.md
  role: source
  note: 発見順、失敗、適用判断
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: source
  note: 既定offのexact LOSS行停止flag
scope: 2026-10-12のWindows環境で、K0375/K0378の既に独立証明済みS5 LOSS六根に対して各根250,000 nodeを与えた比較。S5全域や未知S5への一般化は含まない。
evidence: 6根のdirect S5は全てUNKNOWN。各分割方式は各根で幾何順序により固定したS6子5個を各50,000 nodeまで調べ、B–Eの計30行は全てUNKNOWN、LOSS witness 0、S6 WIN 0だった。各方式の総node数は1,500,000で同じ。legal-count orderはkey orderよりnode削減を示さず、7石exact-layer cacheはhit 0 / store 0。共有TT方式DはCよりwall 7.508秒から4.813秒へ短かったがnode数は同じで、direct Aは4.927秒だった。反復初期化を減らしたwall差は探索節点削減を示さず、同一条件の一回測定で改善とは判定しない。全S6候補の残り79–89子は未測定。現行S4 unknownへの適用・solver結果の証明importは行っていない。
---

# 既知S5 LOSS根の小予算S6証人探索

K0375由来の六根を固定し、各S5につき同じ250,000 node capで直接S5 DFPNとS6個別探索を比較した。探索順は正準key順またはS6合法手数昇順で、共有TT・7石 exact cacheの条件を分離した。探索実行は同一binary、cache空の新規processから開始した。

この予算ではどの方式も六根を確定せず、S6 LOSS証人を発見しなかった。共有TT方式は複数のfresh TT初期化を避けてwallを短縮したが、節点数は直接方式と同じであり、実測node削減ではない。7石 exact cacheには保存可能なexact値が作られなかった。結果は既知LOSS根の限定標本であり、未知S5の証人順序へ一般化しない。
