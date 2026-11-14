---
id: K0817
title: "円の連続行窓点数 P(w) の劣加法性と漸近密度上界"
kind: proposition
status: proved
topics: [geometry, rectangles]
aliases: []
scope: "標準整数格子の真円について、連続する w 本の整数水平行に含まれる格子点数の最大値 P(w)。全 a,b≥0 で P(a+b)≤P(a)+P(b)。したがって λ=lim_{w→∞}P(w)/w が存在し、K0804 の P(82)=32 から λ≤16/41。"
evidence: "全称数学的証明: 各水平行と真円の交点は高々2点なので P(w)≤2w。a+b 行の窓を a 行と b 行に分割すると各部分の点数はそれぞれ P(a),P(b) 以下であり、P は劣加法的。Fekete の補題から λ=lim P(w)/w=inf_{k≥1}P(k)/k が存在する。K0804 の全称値 P(82)=32 を代入して λ≤32/82=16/41。"
relations:
- type: depends_on
  target: K0804
  note: P(82)=32 の全称値を漸近上界に代入
- type: depends_on
  target: K0813
  note: P(w) の円格子点数定義と各水平行2点上界の枠組み
artifacts:
- path: research/experiments/circle-strip-subadditivity-20261114/report.md
  role: proof
  note: 劣加法性・Fekete の補題・P(82)=32 からの漸近上界の全称証明
- path: research/experiments/circle-strip-subadditivity-20261114/verify.py
  role: verifier
  note: P(w)表の連続性・P(82)・既知範囲の劣加法性・最小既知比率を検査
- path: research/log/2026-11-14-circle-strip-subadditivity.md
  role: log
  note: 発見経緯・有限表検査・証拠境界・次の未解決課題
---

## 命題（証明済み・全称）

P(w) を、真円が連続する w 本の整数水平行に含む格子点数の最大値とする。P(0)=0 と置くと、全ての a,b≥0 について

P(a+b) ≤ P(a)+P(b)。

したがって Fekete の補題により

λ := lim_{w→∞} P(w)/w = inf_{k≥1} P(k)/k

が存在する。さらに K0804 の全称結果 P(82)=32 から

0 ≤ λ ≤ 32/82 = 16/41。

## 証明

真円と固定した水平整数直線との交点は高々2点である。よって P(w)≤2w であり、各 P(w) は有限である。

任意の真円 C と連続する a+b 本の整数行の窓 I を取る。I を先頭 a 行 I_a と残り b 行 I_b に分ける。行集合が互いに素なので

|C∩I| = |C∩I_a| + |C∩I_b| ≤ P(a)+P(b)。

この不等式は C と I に依存しないため、最大値を取って P(a+b)≤P(a)+P(b) を得る。a=0 または b=0 は P(0)=0 から自明である。

非負で有限な劣加法列 P(w) に Fekete の補題を適用すると極限 λ が存在し、下限表示も成り立つ。K0804 は全ての真円・全ての連続82行窓について P(82)=32 を証明しているから、λ≤P(82)/82=16/41。

## 明示的な全幅上界

w=82k+r（k≥0、0≤r<82）と書く。劣加法性を繰り返すと

P(w)≤32k+P(r)≤32k+2r。

したがって

P(w)≤(16/41)w+(66/41)r≤(16/41)w+5346/41<(16/41)w+131。

これは全 w≥0 に対する明示的上界である。

## 有限表との照合

results/fixed-width/pw_circle_point_max.csv の w=2..82 の81行、P(82)=32、P(1)=2 を確認した。既知範囲 w≤82 では a+b≤82 の劣加法不等式を全3,486組について検査し、違反は0件だった。P(w)/w の既知範囲での最小値は w=82 の16/41である。これらは表の整合性検査であり、全称劣加法性の証明は上記の行分割論証による。

## 限界

- λ の正確な値は未確定であり、λ=16/41 とは主張しない。λ=0 の可能性も残る。
- P(w)=32 が w>82 でも続くとは主張しない。
- この結果は円格子点数の漸近制約であり、既存の M_{w,q} の真の安定化長を新たに確定するものではない。
