---
id: K0420
title: 初手49のWIN側frontierは約1.74k証人・7.5k AND分岐で全65応手軌道が閉鎖可能
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0417
  note: LOSS側共同frontier 31,546と個別上界（49:2055）の比較基準
- type: depends_on
  target: K0371
  note: 元先手固定のAND/OR伝播（S1・S3=AND、S2・S4=OR）
- type: depends_on
  target: K0416
  note: S5 LOSSの全sixth手閉包が必要なことと未閉鎖2,992根の前例
artifacts:
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/win_side.py
  role: source
  note: 応手軌道縮約・S4分類・証人被覆のWIN側依存分析（初手49で約30分）
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/win_witness_masks.py
  role: source
  note: 証人S5マスクの限定再計算と重なり測定（約1分）
- path: research/experiments/n11-proof-cost-comparison-20261012/output/win-side-analysis.json
  role: data
  note: 65応手軌道の閉鎖性・証人数・AND幅
- path: research/experiments/n11-proof-cost-comparison-20261012/output/win-witness-masks.json
  role: data
  note: 証人1,739マスクと再計算差分
- path: research/experiments/n11-proof-cost-comparison-20261012/output/pilot-candidates.json
  role: data
  note: frontier legal手数分布・最安10件・両用16件のマスク
- path: research/experiments/n11-proof-cost-comparison-20261012/README.md
  role: source
  note: 証明戦略比較の全体記録（課題1〜5、主軸判断と実探索条件を含む）
scope: 初手49の全65応手軌道（安定化群でD4縮約）・各119 third手・全fourth手S4の既存cache分類と楽観的証人被覆。solver探索なし。
evidence: 65応手軌道すべてにviable thirdがあり（dead S4は到達133,924クラス中に0個）、無料5・証人要60。AND境界は7,503 S4分岐、楽観的証人は約1.74k相異なるS5（heuristic依存±1%）。各証人は全sixth手閉包が別途要る。LOSS側共同要求集合との重なりは16/1,739で両frontierはほぼ無共有。frontier legal手数は60〜116手、最安10件と両用16件をマスク付きで抽出した。既存cacheのLOSS 5,692件中node記録は65件のみでfrontier費用の外挿はしない。
---

初手49の先手WIN証明は、応手側に障害ゼロ（65/65閉鎖可能）でfrontier約1.74k・AND幅7.5kという有限規模に収まる。ただし証人1個あたりの全sixth手閉包費は未測定のため、frontier規模の比較は証明費用の比較ではない。

測定に基づく方針判断（証明ではなく方針）：主軸は後手WIN側共同計画を維持し、先手WIN側は初手49の証人パイロット閉包で単価実測する。両用16 S5など両戦略に資する閉包から着手し、パイロット成功なしに大量探索を開始しない。
