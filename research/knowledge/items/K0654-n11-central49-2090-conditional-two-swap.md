---
id: K0654
title: 11×11中央49の条件付き七石証明義務を二証人交換で2,091類から2,090類へ削減
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0653
  note: 独立監査済み46六石証人・2,091七石類の出発点
- type: depends_on
  target: K0644
  note: 終局証明済みLOSS7の23類と現行被覆との交差6類
- type: supersedes
  target: K0653
  note: 同じ94五石被覆を維持した条件付き計算計画を2,090類へ更新
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2090_two_swap.json
  role: certificate
  note: 二証人交換と2,983合法七石辺・2,090類・終局証明済み6類を固定
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2090_two_swap.py
  role: verifier
  note: 五終局戦略再生、4×4 Bareissと3×3差分整数幾何、改変負例8件
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2091_three_swap_neighborhood.py
  role: verifier
  note: 2,091類からの最大三証人交換の全候補を列挙し44改善候補を検出
- path: research/experiments/n11-central-19-cover-20261031/focus_s7_worker_2090.py
  role: source
  note: 現行証明書に紐付けて64子中62未検証類を四分配
- path: .github/workflows/n11-central49-2090-two-swap.yml
  role: source
  note: 独立証明書検査CI 41513037490成功
- path: .github/workflows/n11-central49-2091-three-swap-neighborhood.yml
  role: source
  note: 三証人交換全数監査CI 41512181140成功
- path: .github/workflows/n11-central49-2090-focus.yml
  role: source
  note: 現行集中配布の安全統合検査CI
- path: research/log/2026-11-03-n11-central49-2091-to-2090-two-swap.md
  role: log
  note: 探索全数計数・交換鍵・独立検証・証拠境界
scope: 標準11×11完全指摘・通常プレイ。中央49の94五石正準類を46六石LOSS候補で被覆する条件付き計画。六石LOSS・四石LOSS・二石root・空盤勝敗は対象外。
evidence: 2,091類から最大三証人交換を全数列挙。除去三つ組15,180、六頂点完全マッチング227,700、候補313,576、幾何的に有効283,303、既知WIN6除外1,431、有効281,872、改善44、最小2,090類。最良交換の共通証人を相殺し二証人交換として固定。4×4 Bareissと3×3差分幾何で46証人・94/94五石被覆・2,983合法辺・2,090七石類・終局証明済みLOSS7六類・WIN6/7衝突0を独立監査。全数CI 41512181140成功、独立証明CI 41513037490成功、改変負例8件拒否。
---

# 中央49の条件付き証明義務を2,090類へ縮小

2,091類の現行計画から最大三証人交換を全数列挙すると、既知WIN6・WIN7を除外した採用可能281,872候補のうち44候補が七石義務を改善し、最良は2,090類だった。最良の除去・追加三証人に共通する一証人を相殺すると、**厳密な二証人交換**となる。追加二証人の合法七石子を独立4×4 Bareissと3×3差分整数行列式で照合し、五つの既存終局戦略も再生した。

| 指標 | 従来 | 今回 |
| --- | ---: | ---: |
| 六石証人 | 46 | 46 |
| 五石被覆 | 94/94 | 94/94 |
| 合法七石辺 | 2,984 | **2,983** |
| 相異なる七石証明義務 | 2,091 | **2,090** |
| 終局証明済みLOSS7 | 6 | **6** |
| この証明系列で未確保 | 2,085 | **2,084** |

交換の除外・追加鍵はJSON証明書に保存し、改変負例8件を拒否した。現行集中対象の六石は交換されず、合法七石子64類のうち2類が独立終局証明済み、62類が未検証である。

**2,090類計画の局所最適性・大域最小性は未証明**。六石LOSSの新規証明もなく、二石局面{49,60}と標準11×11空盤の勝敗は**UNKNOWN**。
