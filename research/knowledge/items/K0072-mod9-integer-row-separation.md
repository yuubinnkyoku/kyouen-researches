---
id: K0072
title: 標準整数行の合同条件は高q全長分離領域を拡大する
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
- path: research/experiments/fixed-width/reports/mod7-mod9-mod11-mod19-mod23-half-density-15.md
  role: proof
  note: w=15..18の二重点行半密度境界の合同完全排除とw>=15への接続
- path: research/experiments/fixed-width/scripts/mod7-mod9-mod11-mod19-mod23-half-density.py
  role: verifier
  note: 2独立方式で79651候補k行部分集合を検証し全排除
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


## 15行以上での半密度強化（2026-10-08）

既存の「19行以上での半密度強化」を厳密に改善し、**標準整数格子の連続する全 w>=15 行** について

\[
\boxed{t\le\lceil w/2\rceil,\qquad P\le w+\lceil w/2\rceil}
\]

を全称証明した。ここで t は一本の円が2整数格子点ずつ持つ行の数、P は全行から円上に取れる格子点総数である。

不足していた w=15,16,17,18 の t 上界はそれぞれ 8,8,9,9。二重点行が半数を超えると隣接する二重点行があるので、Vieta の整数 C,N に対する必要合同条件

\[
N-(2i+C)^2\in\operatorname{QR}(p)
\]

を mod 9,11,19,23 および w=16 の mod 7 で完全列挙した。9本（w=15,16）または10本（w=17,18）の候補行集合の総数は79,651で、全て排除した。**合同条件の独立した2実装は法ごとに同じ許容候補集合を返す**ことを確認済み。残る w>=19 は前節の既証明から従う。詳しい整数性の証明、合同必要条件の全件集計、再現コードは [新しい半密度証明](../../experiments/fixed-width/reports/mod7-mod9-mod11-mod19-mod23-half-density-15.md) に記録した。

従って **w>=15 かつ q>w+ceil(w/2)** では、どんな m>=1・どんな安全局面 S にも禁止 q点共円・非水平 q点共線はなく、各行の独立容量から厳密に

\[
g(S)=\bigl(w\min(m,q-1)-|S|\bigr)\bmod2,\quad
M_{w,q}=q-1
\]

となる。以前の mod9 単独の上界から追加される領域は **w=15: q=24..26、w=16: q=25..28、w=17: q=27..29、w=18: q=28..30**。従来記していた「18行が合同法では未解決」という注記は本節によって解消された。

これは標準整数格子の定理で、任意間隔の平行行や w<=14 への半密度上界までは主張しない。これより低い q で円が必ず存在するという逆向きの主張も含まない。
