---
id: K0854
title: "行直線ブロック命題: safe配置では行石数≤q−1・石数q−1の行の全空点は行直線でblocked・自由列追加の停止セルは常に石数≤q−2の行にある(単一欠損witnessでは一意の欠損行)"
kind: proposition
status: proved
topics: [geometry, maximal-safe, rectangles]
aliases: []
scope: "任意の w≥1・q≥2・行 0..w−1 の有限石集合 S が safe(どの直線・円も q 石以上を含まない)なら、各水平行の石数は ≤ q−1 であり、石数ちょうど q−1 の行の全空点はその行の水平直線(ちょうど q−1 石を含む)で blocked である。よって K0853 の自由列追加の最初の非 blocked セル(停止セル)は必ず石数 ≤ q−2 の行にある。単一欠損 witness(rows が (q−2, q−1×(w−1)))では停止セルは一意の欠損行にあり、m′ > R(S) で極大性が壊れるセルも欠損行内にある。"
evidence: "全称数学的証明: (1) 行 y の水平直線は行 y の全石を含むので、safe(全曲線 ≤ q−1 石)なら行石数 ≤ q−1。(2) 行石数 = q−1 の行では、その行の水平直線は任意の空点 (x,y) を通りちょうど q−1 石を含むため、K0853 の blocked 定義(c を通る曲線が ≥ q−1 石)により全空点が blocked。(3) よって非 blocked セル(停止セルを含む)は石数 ≤ q−2 の行に限られる。独立機械監査 scripts/rowline_check.py(純Python Fraction・blocking 直線 (c,s) 族・blocking 円 三つ組族の完全列挙・K0853 checker と独立のコード)が published witness 8件で (a) 行石数 ≤ q−1・(b) q−1石行の全空点 blocked(走査窓全列)・(c) 窓内の全非blockedセルが欠損行所属・(d) 停止セル行石数 ≤ q−2 の4検査を実施し 8/8 PASS(output/rowline-audit-20261115.json): (6,4) m=46→(46,0)・(4,4) m=32→(33,2)・(4,4) m=34→(34,2)・(4,5) m=20→(20,3)・(5,5) m=26→(26,0)・(5,6) m=22→(22,0)・(5,7) m=18→(18,0)・(7,6) m=31→(31,3)。いずれも停止セルの行は行石数最小の一意の欠損行。published surgery/extension 記録の全停止セルも同一の理論予測と一致((7,5) m=33→(33,0)・(7,6) m=29/30/31→(29,3)/(30,3)/(31,3)・(5,5) m=26→(26,0)・(7,5) winC 7×38→(37,0)・(7,4) m=59 witness→(59,6)・(6,4) m=42..44 free append 停止右端 (m−1,0))。"
relations:
- type: depends_on
  target: K0853
  note: "blocked・自由列追加到達幅 R(S)・停止セルの定義を利用。K0853 に記録した『停止セルは常に欠損行』観察(当時 6/6・未証明)を一般命題として昇格し証明した。"
- type: supports
  target: K0833
  note: "witness 帯延伸 surgery の対象セル T が常に欠損行にある理由の理論化((4,4) m=35 T=(34,2)/(0,2)・(4,5) m=21 T=(20,3)/(0,3)・(5,5) m=27 (26,0)・(5,6) m=23 (22,0) はすべて石数最小行)。"
- type: supports
  target: K0827
  note: "7行族の空列延伸失敗セル((33,0)・(29,3)・(31,3)・(37,0)・(59,6))が欠損行にあることの説明。"
artifacts:
- path: research/experiments/free-column-append-criterion-20261115/scripts/rowline_check.py
  role: verifier
  note: "独立 Fraction 実装。(a) 行石数上限・(b) q−1石行の全空点 blocked・(c) 走査窓内全非blockedセルの欠損行所属・(d) 停止セル行石数の4検査。exit code は全検査 PASS のときのみ 0。"
- path: research/experiments/free-column-append-criterion-20261115/output/rowline-audit-20261115.json
  role: data
  note: "8 witness 監査結果(全 PASS)。各行 rows・欠損行・窓内非blockedセル・停止セルとその行石数を記録。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-7x6-m31-witness.json
  role: data
  note: "(7,6) m=31 surgery witness(K0827)の criterion 再現: R=31・停止 (31,3)(published『7×32 で (31,3) 未遮断』と一致)。witness_widths [30,31] — 同一34石が幅30でも safe+maximal(c3 witness と4石異なる別配置の m=30 witness)。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-5x5-m26-witness.json
  role: data
  note: "(5,5) m=26 witness(K0833/five-row-q5-m26-extend)の criterion 再現: R=26・停止 (26,0)(同レーンの埋め込み幾何『offX=0 → (26,0) の1セルのみ未遮断』と独立実装間で一致)。"
- path: research/log/2026-11-15-rowline-blocking.md
  role: log
  note: "観察→published 記録精査→証明→8 witness 機械監査の発見順の記録。"
---

## 命題(全称・証明済み)

S を行 0..w−1 に収まる有限石集合、q ≥ 2、S は safe(どの直線・円も
S の石を q 個以上含まない)とする。

1. **行石数上限**: 各水平行の石数 r_y ≤ q−1。
2. **行直線ブロック**: r_y = q−1 ならば、行 y の全空点 (x, y) は
   K0853 の意味で blocked である(遮断曲線 = 水平直線 y)。
3. **停止セルの位置**: K0853 の自由列追加の最初の非 blocked セル
   (停止セル)は必ず r_y ≤ q−2 の行にある。単一欠損 witness
   (rows = (q−2, q−1×(w−1)))では一意の欠損行にある。

**証明**:
(1) 行 y の水平直線は行 y の全 r_y 石を含む。safe なら全曲線が
≤ q−1 石なので r_y ≤ q−1。
(2) r_y = q−1 のとき、水平直線 y は行 y の任意の点(空点を含む)を
通り、ちょうど q−1 石を含む。blocked の定義(c を通る曲線が
≥ q−1 石)が満たされる。
(3) 非 blocked セルは r_y ≤ q−2 の行にしか存在できない。
停止セルは非 blocked なので主張が従う。単一欠損 witness では
r_y ≤ q−2 の行は一意。□

**系(surgery の狙い撃ち)**: witness 帯を m0 から m0+1 以上へ
延伸する surgery は、R(S) の列で遮断すべきセルが欠損行にあること
**以外の情報を一切仮定せずに**、欠損行セルを遮断する編集だけを
探索すればよい。実際に published surgery レーンの対象セル T は
全件で欠損行にあった((33,0)・(29,3)・(30,3)・(31,3)・(26,0)・
(37,0)・(59,6)・(46,0)・(34,2)・(20,3)・(22,0)…)。

## 機械監査(8 witness・独立実装)

`rowline_check.py`(K0853 checker と同じ手法・独立コード・Fraction)
が各 witness について
(a) max(rows) ≤ q−1・
(b) q−1 石行の全空点が走査窓(列 0..limit−1)で blocked・
(c) 窓内の全非 blocked セルが欠損行に所属・
(d) 停止セルの行石数 ≤ q−2
を検査:

| witness | rows | 停止セル | 欠損行 | published 記録 |
|---|---|---|---|---|
| (6,4) m=46 | [2,3,3,3,3,3] | (46,0) | {0} | (46,0) uncovered に一致 |
| (4,4) m=32 | [3,3,2,3] | (33,2) | {2} | m=33 延伸根拠に一致 |
| (4,4) m=34 | [3,3,2,3] | (34,2) | {2} | 前線 m=35 に一致 |
| (4,5) m=20 | [4,4,4,3] | (20,3) | {3} | m=21 掃引が真の前線 |
| (5,5) m=26 | [3,4,4,4,4] | (26,0) | {0} | m=27 埋め込み幾何に一致 |
| (5,6) m=22 | [4,5,5,5,5] | (22,0) | {0} | surgery (22,0) に一致 |
| (5,7) m=18 | [5,6,6,6,6] | (18,0) | {0} | witness-free 帯 19..37 と整合 |
| (7,6) m=31 | [5,5,5,4,5,5,5] | (31,3) | {3} | m=32 surgery T=(31,3) に一致 |

8/8 PASS(`output/rowline-audit-20261115.json`)。criterion 再現2件
((7,6) m=31・(5,5) m=26)は published 記録と完全一致。副産物:
(7,6) m=31 witness の同一34石は幅30でも safe+maximal
(witness_widths [30,31]・m=30 witness c3 とは4石異なる別配置)。

## 限界・言っていないこと

- 欠損行の**どの**セルがいつ非 blocked になるか(停止のタイミング
  R(S) 自体)はこの命題では決まらず、K0853 checker の走査が必要。
- 「欠損行のすべての空点が非 blocked」ではない(監査 (c) でも
  窓内の非 blocked セルは停止セル以降の欠損行セルのみ)。
- 深欠損(複数行が ≤ q−2)では停止セルの行は一意に決まらない
  (命題は「≤ q−2 の行のどこか」まで)。
- witness の不在・M の確定には一切言及しない。
