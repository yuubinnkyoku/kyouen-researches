---
id: K0097
title: 整数剰余放物線の安全最大は高々(p+3)/2、5..2000では等号
kind: proposition
status: proved
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-lemmas-2026-10-02/checks/independent_parabola.json
  role: data
  note: 29素数の証人の独立全四点検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/frontier-geometry-2026-10-05/recovered-witnesses.json
  role: certificate
  note: 131..251の23素数の保存済み安全証人
- path: research/experiments/frontier-geometry-2026-10-05/recovered-independent-audit.json
  role: data
  note: generic 4×4 Leibnizによる全94575425選択四点の独立検算
- path: research/experiments/frontier-geometry-2026-10-05/density-probe-witnesses.json
  role: certificate
  note: 509,1009の二つの追加有限存在証人
- path: research/experiments/frontier-geometry-2026-10-05/density-probe-independent-audit.json
  role: data
  note: 証明済み必要合同式と直接整数行列式で全選択四点を検査
- path: research/experiments/parabola-equality-extension-20261016/README.md
  role: source
  note: 521..2000への有限拡張の完全報告
- path: research/experiments/parabola-equality-extension-20261016/output/witnesses_521_2000.json
  role: certificate
  note: 521..1999の全206素数の等号証人（d・parameters・size=h+2）
- path: research/experiments/parabola-equality-extension-20261016/output/parabola-equality-audit.txt
  role: data
  note: generic 4×4 Leibniz独立検証（covered/checked・共円0件）の生出力
- path: research/experiments/parabola-equality-extension-20261016/scripts/probe_parabola.py
  role: solver
  note: 実装（edges厳密列挙＋d降順CNF＋cadical）
---

# 整数剰余放物線の安全最大は高々(p+3)/2、5..2000では等号

Q_p={(t,t² modp)}について奇素数pではA(p)≤(p+3)/2。対{t,p−t}を二組丸ごと取ると同高さ二弦の等脚台形になり共円、完全対は高々一組なので上界が従う。

5..127の全29素数で安全証人が達成し、全3310721四点組を別Bareiss実装で検算した。
131..251の23素数の証人も保存し、全94575425選択四点をgeneric 4×4 Leibniz展開で検算した。
さらに257..439の全31素数、443..503の全11素数の保存済み証人も、必要合同式で候補を漏れなく絞った上で直接整数共円行列式を全候補に適用し、零行列式が0件であることを有限完全検査した。

521..1999の全206素数については、509<p<1009の未記録だった穴を埋め、等号証人を構成した
（research/experiments/parabola-equality-extension-20261016）。等号集合は `{0,d,p−d}` と各対の一方
という完全対構造を取り（K0334）、各dでCNFが充足可能なら等号。206素数すべてで充足し（200素数はd=h、
1087,1091,1367,1523,1847はd=h−1、1861はd=h−66）、証人を保存した。generic 4×4 Leibniz行列式の
独立検証器で全証人を検査し（`parabola-equality-audit.txt`、出口0）、必要合同式(sum≡0)を満たす総計
2,196,275,194,090四点組のうち1,385,691,858候補に直接整数行列式を適用して共円0件。p=1009の監査値
(covered 2699163390, checked 2711706)は既存proof.mdの記録と一致した。

したがって**5..2000の全奇素数で等号が成立する**（509,1009を含む）。この連続有限範囲を超えた
全奇素数での達成は結論に含めない（K0101）。全盤K_pではなく制限集合Q_p内の値。
