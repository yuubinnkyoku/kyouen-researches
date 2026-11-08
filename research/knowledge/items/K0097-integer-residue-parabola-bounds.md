---
id: K0097
title: 整数剰余放物線の安全最大は高々(p+3)/2、5..2203では等号
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
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2143_2500.json
  role: certificate
  note: 2003..2477の64素数のうち2207を除く63素数の等号証人（2351も構成済み）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit.txt
  role: data
  note: generic 4×4 Leibnizの独立検証（covered/checked・共円0件）の生出力
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/README.md
  role: source
  note: 2003..2477への保存証人拡張の報告と再現手順
---

# 整数剰余放物線の安全最大は高々(p+3)/2、5..2203では等号

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

したがって**5..2000の全奇素数で等号が成立する**（509,1009を含む）。

## 2026-11-07 有限範囲の拡張（5..2203）

`research/experiments/parabola-equality-extension-2143-2500-20261107` で 2003..2477 の奇素数 64 個を
再走査し、63 個で等号証人を構成・保存した（2027, 2399, 2477 は d=h-1、他の 60 は d=h）。
2351 は既定設定の cadical が d=h..h-3 でタイムアウトしたが、SAT 向け設定（`--sat -L1000`）で
d=h の充足解を数秒で得て証人を構成した。2207 は d=h..h-528 の走査で未発見であり（深い d を走査中）、
等号不成立の証拠ではない。generic 4×4 Leibniz の独立検証器で全 63 証人を検査し共円 0 件
（対象四点 4,281,223,034,600 組、候補 1,886,530,224 組）。
既存の 5..2000 と合わせ、**5..2203 の全奇素数で等号が成立する**（2207 が最初の未発見素数）。

この連続有限範囲を超えた全奇素数での達成は結論に含めない（K0101）。全盤 K_p ではなく制限集合 Q_p 内の値。

## 上界の非達成と現在の監査範囲

K0706はp=2647の全1323 dのUNSAT証明を修正版検証器で監査し、`A(2647)<=1324` を有限計算で確認した。
したがって上界 `(p+3)/2` は全奇素数で鋭いわけではなく、K0101の全奇素数予想は反証済み。
K0711の独立検査済み1296点証人と合わせて `1296<=A(2647)<=1324`。
非達成素数の分布と特徴づけは未解決である。

p=2207と2531の全dのUNSAT主張はK0693/K0702に記録されているが、修正版の全数DRAT監査は未完了で、
両項目は `needs-review`。旧検査器の標本21件・途中373件の受理記録はK0707により独立証拠への採用を保留する。
現在の修正版被覆はそれぞれの正本を参照する。2207を最初の未発見候補とすることと、
最小の非達成素数を独立検証済みとすることは区別する。
