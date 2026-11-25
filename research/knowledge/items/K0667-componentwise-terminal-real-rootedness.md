---
id: K0667
title: グラフ星型の中心付き終局長多項式の成分別実根性判定
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0648
  note: 許容核と重みの連結成分別乗法性
- type: depends_on
  target: K0666
  note: 次数2を含まない分岐成分の非実根性
artifacts:
- path: research/experiments/componentwise-terminal-real-rootedness-20261103/proof.md
  role: proof
  note: 乗法性、実根性の成分別必要十分条件、および混合成分族の判定
- path: research/experiments/componentwise-terminal-real-rootedness-20261103/verify.py
  role: verifier
  note: 頂点数7以下の有限グラフで成分別乗法性を検査（全称証明の代用ではない）
scope: K0602/K0648の有限単純グラフ、辺を持つG、q>=4。中心点を含む極大安全配置の最短終局長差多項式。標準格子盤の全終局分布は対象外。
evidence: K0648の許容核公式からの全称証明。成分別乗法性の有限検証は補助的証拠。
---

# 成分別実根性の必要十分条件

有限単純グラフGの連結成分をG_iとする。孤立頂点の因子を1、孤立辺の因子を正の定数として、K0648の中心付き終局長差多項式をF_{G,q}(u)と書く。

**全称定理（q>=4）**：F_{G,q}(u)=∏_i F_{G_i,q}(u)。従って、F_{G,q}の全根が実数であることと、各F_{G_i,q}の全根が実数であることは同値である。定数多項式は実根的とする。

**判定可能な混合族**：各連結成分が「最大次数2以下」または「次数2の頂点を一つも持たない」のいずれかである場合、F_{G,q}が実根的である必要十分条件はGの最大次数が2以下であること。前向きは道・サイクルの既存実根性定理と乗法性、逆向きは次数3以上の成分にK0666を適用して得られる。

**証明の境界**：積の根は因子の根の多重集合であり、正の定数項を持つ非零因子同士の積で非実根は消えない。次数2を含む分岐連結成分についての一般判定は未解決。中心なしの終局配置や標準格子盤の勝敗には拡張しない。

詳しい証明は上記experimentを参照。有限検証は成分分解の整合性のみを確認しており、K0648自体の独立検証ではない。
