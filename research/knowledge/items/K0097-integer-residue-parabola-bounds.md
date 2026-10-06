---
id: K0097
title: 整数剰余放物線の安全最大は高々(p+3)/2、5..251と509,1009では等号
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
---

# 整数剰余放物線の安全最大は高々(p+3)/2、5..251と509,1009では等号

Q_p={(t,t² modp)}について奇素数pではA(p)≤(p+3)/2。対{t,p−t}を二組丸ごと取ると同高さ二弦の等脚台形になり共円、完全対は高々一組なので上界が従う。

5..127の全29素数で安全証人が達成し、全3310721四点組を別Bareiss実装で検算した。
131..251の23素数の証人も保存し、全94575425選択四点をgeneric 4×4 Leibniz展開で検算した。
さらに257..439の全31素数、443..503の全11素数の保存済み証人も、必要合同式で候補を漏れなく絞った上で直接整数共円行列式を全候補に適用し、零行列式が0件であることを有限完全検査した。
したがって5..509の全奇素数で等号が成立する。

さらに509,1009の各有限証人を保存し、K0333/K0334で証明した必要合同式で
候補を漏れなく絞り、合計3063918候補に直接整数行列式を適用した。
合同式が非零の四点は不可能性の数学的根拠で、零の全候補は整数検査で扱う。
この連続有限範囲を超えた全奇素数での達成は結論に含めない。
全盤K_pではなく制限集合Q_p内の値。
