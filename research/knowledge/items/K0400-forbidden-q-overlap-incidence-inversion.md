---
id: K0400
title: 共円・共線q点禁則の全交差分布を点次数から復元する公式
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円・共線禁則の定義を一般q点へ拡張する
artifacts:
- path: research/experiments/geometry/reports/forbidden-q-incidence-moments-20261011.md
  role: proof
  note: 二項反転と支持曲線の一意性に基づく全称証明
- path: research/experiments/geometry/scripts/forbidden_overlap_moments_20261011.cpp
  role: verifier
  note: 11×11までのq=4整数行列式完全列挙
- path: research/experiments/geometry/scripts/verify_forbidden_overlap_moments_20261011.py
  role: verifier
  note: q=4,5小盤での禁則対直接列挙と有理数円の独立照合
- path: research/experiments/geometry/output/forbidden_overlap_moments_20261011.json
  role: data
  note: 実行済み数値
---

# 共円・共線q点禁則の全交差分布を二点次数と曲線長から復元

任意の有限平面点集合とq≥4に対し、異なる禁則q点組の交差点数jの分布O_jは、禁則次数の二項モーメントM_t=Σ_{|T|=t} C(d_T,2)から二項反転で厳密に復元できる。t≥3のM_tは三点が唯一の円または直線を定めることから支持曲線の盤内点数だけで計算できる。従って全O_jは点次数・二点次数・曲線長分布のみで決まり、禁則対の全列挙を要しない。

証明と具体公式は上記proof artifact。11×11のq=4ではF=95,670、O_0..O_3=(3,994,540,561; 552,180,034; 28,906,140; 699,880)を再現。これは既存の未統合計算値と一致し、新しい11×11の勝敗を意味しない。q=5の4×4・5×5でも直接禁則対列挙と一致した。

**統合注意**: このK番号はmain未反映の仮番号。番号衝突を再確認し、AGENTS.mdの手順に従いknowledgeの検査・生成物再構築を実行するまでは正式昇格と見なさない。
