---
id: K0535
title: λ=0標準五列盤の全Grundy公式は高さ6で厳密に安定する
kind: proposition
status: proved
topics: [variants, rectangles, grundy, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0533
  note: 任意候補集合の一般閾値8により全高さm≥8を保証
artifacts:
- path: research/experiments/quadratic-lambda-zero-strips-20261024/proof.md
  role: proof
  note: 一般定理・高さ6,7の有限基底・高さ5の明示反例を接続
- path: research/experiments/quadratic-lambda-zero-strips-20261024/verify.py
  role: verifier
  note: 高さ6,7の全安全局面で二つの独立mexと閉公式を照合
- path: research/experiments/quadratic-lambda-zero-strips-20261024/results.json
  role: data
  note: 5×6の157122局面と5×7の373938局面で両方式の公式不一致0
- path: research/experiments/quadratic-lambda-zero-strips-20261024/sharpness.json
  role: certificate
  note: 5×5の五石安全終局と全20空点への禁止三点組
scope: B_m={0,...,4}×{0,...,m−1}、四点のdet[x²,x,y,1]=0を禁止する通常プレイの全安全局面。公式が全m≥Mで成立する最小M。
evidence: m≥8の全称定理にm=6,7の全数mex二方式検査を接続する計算機支援証明。m=5の明示安全終局が最良性を証明。
---

# 標準五列λ=0版の真の公式安定化高さ6

すべてのm≥6と全安全局面Sについて、同じ一列だけの二石ならg=2、
同じ一列だけの三石ならg=0、その他は `g(S)=|S| mod2`。
特に全m≥6で空盤は後手必勝であり、全局面g≤2。

全m≥8はK0509の一般定理。残るm=6,7はそれぞれ全157,122・373,938安全局面を、
三点補完再帰と独立な列パターン列挙DPで完全照合した。
有限基底を含む計算機支援証明であり、形式証明器内の証明ではない。

m=5では `[(3,1),(3,3),(1,1),(2,1),(4,4)]` が五石の安全終局。
そのgは0だが上の公式は1を予測する。従って、全高さ以降で公式を保証する真の閾値は6。
任意の不等候補集合まで含めた最良一様閾値8とは異なる量である。
