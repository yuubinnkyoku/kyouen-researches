---
id: K0382
title: 11×11既知S5 LOSS標本では決定S6証明が探索費用の主成分
kind: computation
status: observed
topics: [square-outcomes, search-methods, certificates, provenance]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 固定先手視点の交互AND/OR勝敗伝播に従う
- type: depends_on
  target: K0371
  note: 層別伝播規則を維持し、S5 LOSSはS6 LOSS子を持つ条件で評価
- type: depends_on
  target: K0372
  note: exact solver観測を独立terminal-only証明と区別
- type: depends_on
  target: K0375
  note: 既知S5 LOSS六根と歴史rawを選定・照合に使用
- type: depends_on
  target: K0378
  note: 六根の独立検証済み証明DAGからS6証人を抽出
- type: depends_on
  target: K0380
  note: 小予算比較のUNKNOWNを繰り返さず、過去完了費用から6M予算を固定
- type: supports
  target: K0380
  note: 代表3根でS5直探索の費用を先行S6 WIN確認と決定S6 LOSS証明へ分解
artifacts:
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/README.md
  role: source
  note: 条件、6根証人台帳、費用内訳、限界、再現手順
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/input/proof-witness-inventory.json
  role: data
  note: 六つの既存独立証明から抽出したS5/S6、証明閉包、共有、歴史raw
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/input/comparison-schedule.json
  role: manifest
  note: 予算、候補順、同一条件、current S4境界をsolver再実行前に固定
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/input/known-witness-order-schedule-v2.json
  role: manifest
  note: 同一v2 binary COUNT基準と、検証済み4候補のCOUNTD/KEY順比較schedule
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/input/child-profile-build.json
  role: manifest
  note: 最終計測binary・sourceのcompiler条件とSHA-256
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/stage1-v2-6m/summary.json
  role: data
  note: 同一v2 binaryでのS5直、既知S6、順位付け、共有TT比較
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/direct-s5-child-profile-6m/summary.json
  role: data
  note: 直探索の各S6子に費やした増分節点と決定証人
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/known-s6-costs-v2-6m/summary.json
  role: data
  note: v2 binaryで独立rootとして再計測した保存済みS6 LOSS証人の費用
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/known-witness-order-v2-6m/summary.json
  role: data
  note: 同一v2 binary、各6M上限でのCOUNTD・KEY順比較
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/profile-regression-v4/receipt.json
  role: verifier
  note: 既定off、profile on/off、旧binaryとの4×4完全解析回帰
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/audit.json
  role: verifier
  note: run manifest、同一binary、結果内訳、節点費用分解、既存terminal-only receiptsを横断監査
- path: research/experiments/n11-s5-loss-cost-drivers-20261012/output/final-sha256.json
  role: manifest
  note: 実験入出力・sourceのSHA-256一覧
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: source
  note: 既定offのexact replay層別・root child費用プロファイラ
scope: K0375/K0378の独立検証済み六根のうち事前固定した3根に対する、11×11 exact_prop exact replay探索費用。未知S5やsolve_rootのDFPN展開数一般には拡張しない。
evidence: 既存DAGの6つのS5 rootから各保存S6 LOSS証人を抽出した。same v2 binary、cold TT、各root 6M上限で、3つのS5直探索はすべてLOSSを再現し、総計12,778,446 nodeだった。追加profileで各rootの決定S6 LOSS直前に訪問したS6は4/5/2子で全てWIN、費用は344,344 / 2,679,846 / 1,168,545 node。決定S6 LOSS branch自身は1,990,988 / 2,736,490 / 3,858,230 nodeで、直探索全体の85.3% / 50.5% / 76.8%を占めた。保存証人を独立rootとして同じ条件で解く費用は2,006,805 / 2,691,081 / 3,837,541 nodeで、root child増分と各0.8% / 1.7% / 0.5%以内で一致した。合法子数昇順のblind prefix C1/C2はいずれもLOSS 0 / WIN 12 / UNKNOWN 6で、共有TTは総節点を2.75%減らしたが証人を解決しなかった。COUNTDとcanonical key順は各4証人に6Mを与えて全てUNKNOWN、COUNT順の完了node数を減らさなかった。S5証明費用はこの標本ではS6証人の全S7子証明に大きく集中するが、未知局面の探索改善や一般的勝敗費用は示さない。UNKNOWNはexactに昇格せず、solver出力は測定専用。証明事実はtrusted leaf 0の既存terminal-only DAGのみから採る。
---

# S5 LOSSの探索費用分解

K0375/K0378の端末まで閉じた独立証明から保存S6 LOSS証人を選び、代表3根についてS5直探索内の各S6子費用とS6単独の再探索費用を測った。S5直探索で証人の前に調べたS6は全てWINで、その確認費用は根により34万〜268万nodeだった。一方、決定S6 LOSS証明には199万〜386万nodeを要し、3根中2根では直探索費用の76.8%以上を占めた。

既知の正解証人を指定する方法Bは未知局面への証人選択手法ではない。合法子数昇順のblind順、合法子数降順、key順、root内共有TTでも、既知の正解証人を探索して解決する節点削減は確認しなかった。したがって現行S4のUNKNOWNへ方式を適用せず、既定順序も変更しない。

全runのsolver nodeは `exact_prop` のexact replay再帰展開数であり、DFPN本体の`solve_root`展開数や証明DAG節点数とは別である。current S4 `(1297036692683752448,0)` は計測時点の監査でLOSS 40 / WIN 0 / UNKNOWN 66のまま。未知S5探索、証明import、勝敗境界の変更はない。
