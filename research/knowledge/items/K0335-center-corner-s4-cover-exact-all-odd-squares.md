---
id: K0335
title: 奇数盤の中心・隅rootのs4 class cover最小数はceil((n²+n−8)/4)
kind: proposition
status: proved
topics:
- search-methods
- certificates
- geometry
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 標準q=4の安全性と全合法第三手
- type: depends_on
  target: K0092
  note: 対象となるs4 class・s5 cache研究の文脈。空盤勝敗の証明には使わない
artifacts:
- path: research/experiments/n11-cover-duality/reports/center-corner-cover.md
  role: proof
  note: H-orbit dualの全称下界、matchingによるn≥9の全称上界、n5/7の具体証人
- path: research/experiments/n11-cover-duality/scripts/generate_cover.py
  role: solver
  note: 共有整数geometryを再利用した具体cover生成。勝敗は判定しない
- path: research/experiments/n11-cover-duality/scripts/verify_cover.py
  role: verifier
  note: 別行列式・別D4実装による全safe s4 classと整数dualの独立検査
- path: research/experiments/n11-cover-duality/output/center-corner-cover.json
  role: certificate
  note: n3/5/7/9/11/13/15の上界coverと分母2の下界dual
- path: research/experiments/n11-cover-duality/output/verified.json
  role: data
  note: 全class再列挙による上下界一致と四種類の不正証人拒否
scope: 奇数n≥5、B_n上の中心cと隅oを固定。全安全{c,o,a,b}のD4 classからV=B_n\{c,o}を覆う構造的最小数。証明済みLOSS classだけへの制限や空盤勝敗ではない。
evidence: 非隅のroot-stabilizer orbitに重み1/2を置く全称dualと、次数評価によるmatching構成。n=5,7は具体証人と完全有限検査。
---

# 奇数盤の中心・隅rootのs4 class cover最小数

奇数n≥5でrootを中心cと隅oの二石に固定する。安全四点集合
`{c,o,a,b}` を盤全体のD4 orbitでclass化し、そのclassの固定rootを含む
全像からa,bのcoverageを取る。第三手 `B_n\{c,o}` 全体を覆う最小class数は

```
OPT(n)=ceil((n²+n−8)/4).
```

全安全classを候補としたcertificate skeletonの最適値であり、各classの
勝敗ラベルを確定した結果ではない。n≥9では `{c,o,(1,0),(2,0)}` のclassを
必須にしても最適値は同じ。n11では既存 `{60,0,1,2}` classを含む31-class
証人があり、これ以外の必要class数の構造的最小値は30。

rootのstabilizerは主対角線反射。非隅・非rootのorbitは
`T=(n²+n−8)/2` 個で、一つのs4 classが覆うこれらのorbitは高々二つ。
各orbitの一代表に重み1/2を置けば、各classの重み和≤1となり、
`ceil(T/2)` の全称下界を得る。

n≥9の上界では、既存classと二つの隅付きclassで全隅と六非隅orbitを覆う。
残るM=T−6 orbitを安全なs4追加pairのグラフにする。固定三点の円または
直線には盤点が高々2n個なので最小次数≥M−2n+2≥M/2。
matchingの未被覆点は高々一つで、`ceil(M/2)` edgeが残りを覆う。
n=5,7は6/12-class具体証人を完全検査して同じ下界と一致する。
詳細な全称証明・例外n=3・有限証人はproof artifactにある。

独立検査はn3/5/7/9/11/13/15の全safe edge/classを別の整数行列式とD4実装で
再列挙し、全dual制約とcoverageを確認した。n11では119第三手、6894 safe
edge、3396class、整数dual合計31、31-class上界で上下界が一致する。

実際のLOSS証明のみを許すcover、計算コストを重みとするcover、探索速度の
改善は別問題。ここから11×11空盤の勝敗は導けず、現在もUNKNOWN。
