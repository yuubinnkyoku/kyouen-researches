---
id: K0072
title: 標準整数行のmod9制約は高q全長分離領域を拡大する
kind: proposition
status: proved
topics:
- rectangles
- geometry
- variants
aliases:
- F-BN
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/experiments/fixed-width/reports/q2w-boundary-structure.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/fixed-width/output/q2w_boundary_structure.json
  role: data
  note: mod9全剰余とlifted determinant照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 高qの標準整数格子
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: 連続整数行、(q=2w,w≥5)または(q=2w−1,w≥6)
  verification:
  - mathematical-proof
  certificate: mod9有限剰余証明
  independent_check: 円条件の独立determinant照合
  note: M=q−1
---

# 標準整数行のmod9制約は高q全長分離領域を拡大する

整数格子の連続行で、円は5連続行の全てを二重点で通れず、6連続行のうち二重点行は高々4。平方剰余mod9の有限分類で証明する。

従ってq=2w,w≥5およびq=2w−1,w≥6では行をまたぐ禁止q集合なし。全m≥1でg(S)=(w min(m,q−1)−|S|) mod2、M=q−1。任意の平行線配置へは主張しない。

## 19行以上での半密度強化

その後の平方剰余監査により、標準整数格子の連続する \(w\ge19\) 行では、一本の円が2格子点を持つ行数 \(t\) は

\[
t\le \lceil w/2\rceil
\]

まで強化された。証明は、\(w=19,20\) を mod 11・19・23 の CRT 周期 4807 上の有限完全列挙で埋め、\(21\le w\le26\) の既存有限完全列挙と、\(w\ge27\) の mod 23・31 による周期的全称証明へ接続する。一次資料は `research/experiments/fixed-width/reports/mod11-mod19-mod23-circle-half-density.md` と `mod23-mod31-circle-half-density.md`。

従って一本の円が盤内に持てる点数 \(P\) は

\[
P\le w+\lceil w/2\rceil\qquad(w\ge19).
\]

よって \(w\ge19\) かつ \(q>w+\lceil w/2\rceil\) なら、円も非水平直線も複数行にまたがる禁止 \(q\) 点集合を作れない。各行は容量 \(q-1\) の独立成分となり、全 \(m\ge1\)・全安全局面で

\[
g(S)=\bigl(w\min(m,q-1)-|S|\bigr)\bmod2
\]

が成立する。これは上の \(q=2w\), \(2w-1\) 系とは別の、特に大きい幅でより低い \(q\) まで届く十分条件である。

境界 \(w=18\) はこの合同法では閉じていない。mod 11・19・23 の必要条件だけなら18行中10行を二重点行にできる剰余パターンが残るためであり、実際の整数格子円の反例を意味しない。
