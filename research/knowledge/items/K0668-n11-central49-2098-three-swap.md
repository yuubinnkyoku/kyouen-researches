---
id: K0668
title: 11×11中央49の条件付き七石義務を2,154類から2,098類へ三証人交換で縮小
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
- type: depends_on
  target: K0646
  note: 確定WIN6を除外した46証人・2,154七石義務の出発点と二証人交換局所最適
- type: supersedes
  target: K0646
  note: 同じ46証人・94/94被覆を保ったまま七石義務をさらに56類削減した現行条件付き計画
- type: depends_on
  target: K0644
  note: 終局証明由来の七石LOSS23類と現行被覆との交差
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2098_three_swap.json
  role: certificate
  note: 三証人交換1回、正準七石義務2,098、終局証明済みLOSS7との交差6類
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2098_three_swap.py
  role: verifier
  note: 4×4整数Bareissによる交換後の全員の子再計算と3×3幾何による2,154計画の再現、負例6件拒否
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2154_three_swap_neighborhood.py
  role: verifier
  note: 2,154出発点の三証人交換近傍の完全列挙（15,180三つ組・227,700マッチング・309,322候補・277,849有効・改善23・最良2,098の再現）
- path: research/experiments/n11-central-19-cover-20261031/output/three_swap_neighborhood_2154.json
  role: data
  note: 上記近傍全数監査の機械可読出力
- path: .github/workflows/n11-central49-2098-three-swap.yml
  role: source
  note: 独立幾何監査と改変負例6件を検査する専用CI
- path: research/log/2026-11-03-n11-central49-2098-three-swap.md
  role: log
  note: 交換経緯、K0658失効との区別、改善23件の最良手
scope: 標準11×11完全指摘・通常プレイ、中央49の優先四石からの94五石局面を46六石LOSS候補で被覆する条件付き計画。三証人交換1回。六石LOSS・二石root・空盤勝敗は含まない。
evidence: K0646の2,154類計画の出発点について、全三証人交換近傍を全数列挙した（15,180三つ組・227,700六端点マッチング・309,322候補組。幾何的有効279,194、WIN6除外1,345、WIN7除外0、有効277,849）。改善する交換は23あり、最良は2,098正準類（2991合法辺）に到達した。その最良手を適用した証人集合について、交換後の子を4×4整数Bareissで再計算し3×3差分行列式の計画と照合。94/94五石被覆・終局証明済みLOSS7 6類・既知WIN6 145類/WIN7 23類との非衝突を確認。これは選択六石LOSSの証明ではなく、条件付き義務の縮小である。専用CI成功。二石rootと空盤の勝敗は未証明。
---

# 2,098類への三証人交換

K0646の2,154類（二証人交換局所最適・既知WIN6除外済み）に対し、**全三証人交換近傍を全数列挙**した。15,180三つ組を227,700のマッチング通りに展開して279,194組の幾何的有効交換を得て、既知WIN6排除1,345・有効277,849のうち、**2,154を下回る改善は23組**あった。最良手は2,098正準類（2,991合法辺）で、K0650の第1回交換と一致するが、2094計画を失効させた第2回交換（WIN6証人を追加した）を含む段階は一切踏んでいない。

計画は46六石証人・94/94五石被覆・終局証明済みLOSS7 6類（K0644）・既知WIN6 145類/WIN7 23類非衝突を維持する。

| 段階 | 相異なる七石類 | 合法七石辺 |
| ---: | ---: | ---: |
| K0646出発点 | 2,154 | 2,990 |
| 三証人交換 | **2,098** | **2,991** |

**条件付き計画であり、勝敗の主張ではない。** 選択六石LOSSは未証明、二石局面 {49,60} は未閉鎖、標準11×11空盤の勝敗は **UNKNOWN** のまま。2,098は大域的最小値ではない（三・四証人以上の交換がさらに改善する可能性は残る）。2094・2093・2091・2090の各計画と同様に、この計画自身も新たな確定WIN6/WIN7の発見で失効しうる。
