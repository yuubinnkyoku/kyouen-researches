---
id: K0653
title: 11×11中央49の条件付き七石証明義務を三証人交換で2,093類から2,091類へ削減
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0652
  note: 独立監査済み46六石証人・2,093七石類の出発点
- type: depends_on
  target: K0644
  note: 終局証明済みLOSS7の23類と現行被覆との交差6類
- type: supersedes
  target: K0652
  note: 同じ94五石被覆を維持した条件付き計算計画を2,091類へ更新
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2091_three_swap.json
  role: certificate
  note: 三証人交換と2,984合法七石辺・2,091類・終局証明済み6類を固定
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2091_three_swap.py
  role: verifier
  note: 五終局戦略の再生、4×4 Bareissと3×3差分整数幾何、改変負例8件
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2093_three_swap_neighborhood.py
  role: verifier
  note: 2,093類からの最大三証人交換の全候補を列挙し唯一の改善を検出
- path: research/experiments/n11-central-19-cover-20261031/focus_s7_worker_2091.py
  role: source
  note: 2,091類の現行証明書に紐付けて64子中62未検証類を四分配
- path: .github/workflows/n11-central49-2091-three-swap.yml
  role: source
  note: 独立証明書検査CI
- path: .github/workflows/n11-central49-2093-three-swap-neighborhood.yml
  role: source
  note: 交換全数監査CI
- path: .github/workflows/n11-central49-2091-focus.yml
  role: source
  note: 現行集中配布の安全統合検査CI
- path: research/log/2026-11-03-n11-central49-2091-three-swap-reduction.md
  role: log
  note: 探索全数計数・CI・修正履歴・証拠境界
scope: 標準11×11完全指摘・通常プレイ。中央49の94五石正準類を46六石LOSS候補で被覆する条件付き計画。六石LOSS・四石LOSS・二石root・空盤勝敗は対象外。
evidence: 2,093類の証明済み現行幾何から最大三証人交換を全数列挙。除去三つ組15,180、六頂点完全マッチング227,700、候補313,610、幾何的に有効283,333、既知WIN6除外1,367、WIN7除外0、有効281,966、改善は一組だけで2,091類。CI 41508478576成功。追加三証人の4×4 Bareissと別実装3×3差分幾何を照合し、46証人・94/94五石被覆・2,984合法辺・2,091七石類・終局証明済みLOSS7六類・WIN6/7衝突0を独立監査。CI 41509060000成功。改変負例を増やした最終CIは確認待ち。
---

# 中央49の条件付き証明義務を2,091類へ縮小

2,093類の現行計画で、六石証人を最大三つ交換する全候補を列挙した。既知のWIN6・WIN7を除外しても、**ちょうど一組の交換が七石証明義務を2類減らす**。追加した三証人の合法七石子を4×4 Bareissと3×3差分整数行列式で照合した。既存の終局証明5個も再生し、六石LOSSを仮定しない。

| 指標 | 従来 | 今回 |
| --- | ---: | ---: |
| 六石証人 | 46 | 46 |
| 五石被覆 | 94/94 | 94/94 |
| 合法七石辺 | 2,986 | **2,984** |
| 相異なる七石証明義務 | 2,093 | **2,091** |
| 終局証明済みLOSS7 | 6 | **6** |
| この証明系列で未確保 | 2,087 | **2,085** |

交換の除外・追加鍵はJSON証明書に保存した。2,093類からの最大三証人交換近傍は全数検査済みだが、**新しい2,091類計画の局所最適性も、大域最小性も未証明**。実際の六石LOSSは新規に確定しておらず、二石局面 {49,60} と標準11×11空盤の勝敗は **UNKNOWN**。
