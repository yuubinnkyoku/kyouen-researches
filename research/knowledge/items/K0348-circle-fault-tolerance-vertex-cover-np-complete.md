---
id: K0348
title: 任意有限整数点盤の一空点円故障耐性はVertex Coverを表現し唯一最大配置でもNP完全
kind: proposition
status: proved
topics: [geometry, maximal-safe, maximum-safe, variants, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0346
  note: 整数三次グラフの四点安全性・零和三共線・反転による円blocker実現
artifacts:
- path: research/experiments/geometry-frontier-followup-20261005/graph_cover_reduction.md
  role: proof
  note: 任意simple graphからの全称幾何構成、ρ=τ(G)、多項式座標長、NP所属の証明
- path: research/experiments/geometry-frontier-followup-20261005/verify_graph_reduction.py
  role: verifier
  note: 全小graphの零和辺列挙と別の最小横断・vertex cover完全探索、整数幾何の二重検査
- path: research/experiments/geometry-frontier-followup-20261005/graph-cover-audit.json
  role: data
  note: n≤5の全1100graph、101整数盤の全19842四点・10004三点の独立検査
scope: binary整数座標で記述する任意有限点盤B、指定元空点p、S=B\{p}。三共線なし・S安全極大かつ唯一最大・circle-only q=4に制限してもρ≤hの決定問題はNP完全。標準正方形全格子盤は含まない。
evidence: 全有限simple graphに対する多項式時間many-one reductionとNP検証の全称証明。全小graph計算は独立支持検査。
---

# 任意graphのvertex coverを一空点の円故障耐性へ移す

任意simple graphGの各vertexvに正パラメータa_v=10^v、各edge{u,v}に
固有の負パラメータb_e=−a_u−a_vを割り当てる。
base10の繰り上がりがないため、相異なる三パラメータの零和は
{a_u,a_v,b_e}というedge対応の組だけ。反対数対もない。
K0346の(t,2t³)・原点反転・整数化を使うと、
pとvertex石s_u,s_v、edge固有石s_eからなる円だけを禁止四点とする整数盤Bが得られる。
B全体に三共線はない。

edgeが一つ以上ならS=B\{p}は安全極大かつ最大。
pを合法にする削除集合Dは各三石{s_u,s_v,s_e}を横断する必要十分条件を持つ。
vertex coverはそのまま解除集合となる。
逆にDのvertex石で未被覆のedgeは固有石がDに含まれるので、
その各edgeから一endpointを選んで追加すれば同数以下のvertex coverを作れる。
従って厳密にρ_B(S)=τ(G)。

各パラメータのbit長はO(n)、共通分母Lのbit長はO(n(n+m))以下であり、
整数点盤への構成は多項式時間・出力長である。
Gへ互いに素な二つのK2を加えるとρ=τ(G)+2≥2を保証でき、Sは唯一最大となる。
よってρ≤hは、三共線なし・circle-only・唯一最大配置に制限してもNP-hard。

NP所属も成立する。入力は元空点がp一つだけなので、
全三・四点の整数行列式で幾何条件・安全性・p禁止を多項式時間で確認できる。
Sが唯一最大という条件は、全一石削除後もpが禁止されることと同値で、これも多項式検査。
削除集合D（|D|≤h）をcertificateとしてp追加後の安全性を検査すればよい。
従ってこの制限された決定問題はNP-complete。

有限監査ではn≤5の全1100simple graphで別々に最小vertex coverと零和三石横断数を完全探索し一致。
n≤4の全非空graphと選んだn5 graph、二K2追加例を含む101整数盤で、
全19842四点を共有coreとgeneric4×4Leibnizにより二重検査し、全10004三点で非共線を確認した。

このNP完全性はbinary座標の任意有限点盤に関する。
K0328の正方形全格子盤の一様ρ上界、11×11の勝敗、df-pnの速度には結論を与えない。
