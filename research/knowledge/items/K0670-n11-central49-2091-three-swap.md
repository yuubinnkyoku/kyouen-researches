---
id: K0670
title: 11×11中央49の条件付き七石義務を2,097類から2,091類へ三証人交換で縮小（現行チェーン）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
- type: depends_on
  target: K0669
  note: 46証人・94/94被覆・2,097七石類の出発点
- type: supersedes
  target: K0669
  note: 46証人・94/94被覆・確定LOSS7 6類を保ったまま七石義務を6類削減した現行条件付き計画
- type: depends_on
  target: K0644
  note: 終局証明由来の七石LOSS23類と現行被覆との交差
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2091_descent_three_swap.json
  role: certificate
  note: 三証人交換1回、正準七石義務2,091、終局証明済みLOSS7との交差6類。2093→2091の旧チェーン（K0653）とは別計画
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2091_descent_three_swap.py
  role: verifier
  note: 2154→2098→2097→2091のチェーン全体を再生、4×4整数Bareiss、負例6件拒否
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2097_three_swap_neighborhood.py
  role: verifier
  note: 2,097出発点の三証人交換近傍の完全列挙（15,180三つ組・227,700マッチング・候補313,878組・除外修正後有効282,078・改善49・最良2,091）
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2091_descent_three_swap_neighborhood.py
  role: verifier
  note: 2,091出発点の三証人交換近傍の完全列挙（候補313,905組・有効281,978・改善0・最良2,091＝局所最適）
- path: research/experiments/n11-central-19-cover-20261031/output/three_swap_neighborhood_2091_descent.json
  role: data
  note: 上記の機械可読出力（改善0）
- path: research/experiments/n11-central-19-cover-20261031/output/three_swap_neighborhood_2097.json
  role: data
  note: 近傍全数監査の機械可読出力（改善49・最良2,091）
- path: .github/workflows/n11-central49-2091-descent-three-swap.yml
  role: source
  note: 独立幾何監査と改変負例6件を検査する専用CI。2093→2091の旧チェーンのCIとは別
- path: research/log/2026-11-04-n11-central49-2091-descent-three-swap.md
  role: log
  note: 交換経緯と検証境界・命名の重複回避
scope: 標準11×11完全指摘・通常プレイ、中央49の優先四石からの94五石局面を46六石LOSS候補で被覆する条件付き計画。三証人交換1回。六石LOSS・二石root・空盤勝敗は含まない。
evidence: K0669の2,097類計画について、全三証人交換近傍を全数列挙した。除外修正後（focus1984-certified WIN6を候補から完全除外）の有効な非自明交換は282,078組で、2,097を下回る改善は49件あった。最良を2,091正準類（2,984合法辺）へ適用し、2154→2098→2097→2091の全チェーンを独立再生し、4×4整数Bareissと3×3差分行列式で最終46証人の子を再計算。94/94五石被覆・終局証明済みLOSS7 6類・既知WIN6/WIN7非衝突（REFUTED込み）を確認。これは条件付き義務の6類縮小であり、選択六石LOSSの証明ではない。二石rootと空盤の勝敗は未証明。

さらに現在の2,091出発点について、三証人交換近傍を全数列挙したところ、除外修正後の有効な非自明交換は281,978組（候補313,905組）で、**2,091を下回る改善は0件**であった。したがって現行計画は**三証人以下の交換近傍で厳密な局所最適**である（二証人交換についてはK0646、三証人交換については本項目）。四・五証人以上の交換や大域最小性は主張しない。
---

# 2,091類への三証人交換

K0669の2,097類計画の三証人交換近傍を全数列挙した。除外修正後の有効な非自明交換は282,078組で、**2,097を下回る改善は49件**あった。最良手（2,984合法辺→2,091正準類）を適用し、46証人・94/94被覆・終局証明済みLOSS7 6類・既知WIN6/WIN7非衝突を維持した。

| 段階 | 相異なる七石類 | 合法七石辺 |
| ---: | ---: | ---: |
| K0669出発点 | 2,097 | 2,990 |
| 三証人交換 | **2,091** | **2,984** |

**条件付き計画であり、勝敗の主張ではない。** 選択六石LOSSは未証明、二石局面 {49,60} は未閉鎖、標準11×11空盤の勝敗は **UNKNOWN** のまま。2,091は二証人以下の近傍（K0646と同型）および今回の全三証人交換近傍での局所最適であり、四・五証人以上の交換や大域的最小性は主張しない。
