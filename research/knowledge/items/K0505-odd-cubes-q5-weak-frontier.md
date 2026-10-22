---
id: K0505
title: 3次元5点禁止版の7×7×7以降の奇数辺立方盤はどちらが必勝か
kind: question
status: open
topics: [variants, first-moves, search-methods]
aliases: []
relations: []
artifacts:
- path: research/experiments/cube-q5-seven-probe-20261022/README.md
  role: log
  note: 7立方の2石根・35第三手境界・増加予算probe・未検証範囲
- path: research/experiments/cube-q5-seven-probe-20261022/probe.cpp
  role: solver
  note: 343点・6ワードmask・48対称性・遅延四点幾何のbounded exact solver
- path: research/experiments/cube-q5-seven-probe-20261022/probe-7.json
  role: data
  note: "{0,5}は76189展開・400万四点cacheでUNKNOWN"
- path: research/experiments/cube-q5-seven-probe-20261022/probe-7-20m.json
  role: data
  note: "{0,5}は100万展開・18881241四点cacheでもUNKNOWN"
- path: research/experiments/cube-q5-seven-probe-20261022/coverage-7.json
  role: data
  note: 341第三手のうち306手に4石終局応手。残る35手は全てz=6
- path: research/experiments/cube-q5-seven-probe-20261022/regression.json
  role: data
  note: 7立方上の104四点配置・35672追加候補の独立幾何比較と3立方全20二石軌道
- path: research/experiments/cube-q5-seven-probe-20261022/manifest.json
  role: manifest
  note: solver・幾何境界・回帰・実行結果のSHA-256
scope: 共平面または共球面5点禁止・通常プレイ、奇数n≥7のn×n×n整数格子
evidence: 7×7×7の2石根{0,5}を増加幾何予算でprobeしたが未確定
solution:
  board: n×n×n・3次元q=5・奇数n≥7
  level: unsolved
  outcome: unknown
  classification: [root]
  coverage: 7×7×7の{0,5}を100万展開までprobe。空盤の勝敗は未確定
  conditions: 5点共平面または共球面禁止・完全指摘・通常プレイ
  verification: [exact-search]
  certificate: 根はUNKNOWNであり勝敗証明書なし
  independent_check: 7立方の標本幾何と既知3立方全20二石軌道を確認。7立方の根の独立証明ではない
  note: 5立方のK0503および全偶数辺長のK0502から奇数n≥7の勝敗は従わない
---

全偶数辺長の構成的弱解決はK0502、5×5×5の有限証明書はK0503に記録した。
次の奇数盤7×7×7以降の空盤の勝敗と後手戦略または先手戦略を求める問題は未解決。

7立方の2石根 `{0,5}`（座標(0,0,0),(0,0,5)）について、341第三手のうち306手は
共円または共線の4石終局へ応じられる。残る35手は全てz=6面上で、4手終局では
処理できない。これだけでは2石根も空盤も判定できない。

同根を6ワードmask・48対称性・遅延幾何のexact探索器で処理した。
四点cache上限400万では76,189展開でUNKNOWNとなり、上限を2,000万に上げた
別processでは1,000,000展開、確定memo1,359,510、四点cache18,881,241でも
node上限に達してUNKNOWNだった。探索中の部分確定memoは、根の勝敗証明や
独立検査済み全局面表と混同しない。

7立方の幾何は104四点配置・35,672候補で独立行列式と照合し、探索部分は
既知3立方の全20二石軌道の独立証明書で回帰確認した。これは7立方の全幾何の
網羅検査でも空盤証明でもない。根のUNKNOWNから先手・後手どちらの勝ちも
推定しない。奇数n≥9は今回探索していない。
