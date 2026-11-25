---
id: K0669
title: 11×11中央49の条件付き七石義務を2,098類から2,097類へ三証人交換で縮小
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
- type: depends_on
  target: K0668
  note: 46証人・94/94被覆・2,098七石類の出発点
- type: supersedes
  target: K0668
  note: 46証人・94/94被覆・確定LOSS7 6類を保ったまま七石義務を1類削減した現行条件付き計画
- type: depends_on
  target: K0644
  note: 終局証明由来の七石LOSS23類と現行被覆との交差
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2097_three_swap.json
  role: certificate
  note: 三証人交換1回、正準七石義務2,097、終局証明済みLOSS7との交差6類
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2097_three_swap.py
  role: verifier
  note: 2,098計画の出典から適用・再検証、4×4整数Bareiss、負例6件拒否
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2098_three_swap_neighborhood.py
  role: verifier
  note: 2,098出発点の三証人交換近傍の完全列挙（除外修正版：15,180三つ組・227,700マッチング・候補314,219組・除外修正後有効282,451・改善2・最良2,097）
- path: research/experiments/n11-central-19-cover-20261031/output/three_swap_neighborhood_2098.json
  role: data
  note: 近傍全数監査の機械可読出力（改善2・最良2,097）
- path: research/experiments/n11-central-19-cover-20261031/output/three_swap_neighborhood_2154.json
  role: data
  note: 2154計画近傍の除外修正後の出力（改善23・最良2,098）
- path: .github/workflows/n11-central49-2097-three-swap.yml
  role: source
  note: 独立幾何監査と改変負例6件を検査する専用CI
- path: research/log/2026-11-03-n11-central49-2097-three-swap.md
  role: log
  note: 近傍除外修正の経緯と最良手の適用
scope: 標準11×11完全指摘・通常プレイ、中央49の優先四石からの94五石局面を46六石LOSS候補で被覆する条件付き計画。三証人交換1回。六石LOSS・二石root・空盤勝敗は含まない。
evidence: K0668の2,098類計画について、全三証人交換近傍を全数列挙した。当初はK0658で終局WINと確定された六石（focus_s6_win_strategy_1984.certの `00000000000000603800000000008000`）が145類のWIN7親由来WIN6除外に入っていなかったため、2098→2094の失効交換を「最良手」と誤認していた。除外修正後の真の改善は2件のみ。最良を2,097正準類（2,990合法辺）へ適用し、4×4整数Bareissと3×3差分行列式で交換後の子を再計算した。94/94五石被覆・終局証明済みLOSS7 6類・既知WIN6/WIN7非衝突（REFUTED込み）を確認。これは条件付き義務の1類縮小であり、選択六石LOSSの証明ではない。専用CI成功。二石rootと空盤の勝敗は未証明。
---

# 2,097類への三証人交換

K0668の2,098類計画の三証人交換近傍を全数列挙した。除外修正後の有効な非自明交換は282,451組で、**2,098未満へ改善する交換は2件**しかなかった。最良手（2,990合法辺→2,097正準類）を適用し、46証人・94/94被覆・終局証明済みLOSS7 6類・既知WIN6/WIN7非衝突を維持した。

| 段階 | 相異なる七石類 | 合法七石辺 |
| ---: | ---: | ---: |
| K0668出発点 | 2,098 | 2,991 |
| 三証人交換 | **2,097** | **2,990** |

**条件付き計画であり、勝敗の主張ではない。** 選択六石LOSSは未証明、二石局面 {49,60} は未閉鎖、標準11×11空盤の勝敗は **UNKNOWN** のまま。2,097は大域的最小値ではない。この計画も新たな確定WIN6/WIN7の発見で失効しうる。
