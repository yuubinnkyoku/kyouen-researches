---
id: K0584
title: 平面q点禁止ゲームの二担い手領域はN≤3q−7まで鋭く成立しN=2q+1の12型を強解決できる
kind: proposition
status: proved
topics: [geometry, variants, grundy, residual-games, first-moves, maximal-safe, strategy-length]
aliases: []
relations:
- type: generalizes
  target: K0582
  note: N=2qの二担い手上界をN≤3q−7へ拡張
- type: depends_on
  target: K0002
  note: 通常Grundy数とmisère補助値の定義
artifacts:
- path: research/experiments/short-board-2qplus1-20261031/proof.md
  role: proof
  note: 鋭い二担い手上界、12型分類と整数実現、全安全局面再帰
- path: research/experiments/short-board-2qplus1-20261031/verify.py
  role: verifier
  note: q=8の1510740全安全局面、極大配置数、整数幾何構成の独立照合
scope: q≥7の相異なる平面点盤N≤3q−7、特にq≥8・N=2q+1、q点共円または共線禁止の通常・misère二人ゲーム
evidence: 包除原理と三円の有理点構成による鋭い全称境界、二担い手の置換対称性による厳密mex再帰。q=8の12型1510740局面を独立照合。
---

# 二担い手領域の鋭い境界とN=2q+1

相異なる平面点からなる盤面でq≥7、N≤3q−7なら、q点以上を含む円・直線（担い手）は高々二本。この境界は鋭く、任意のq≥7についてN=3q−6で担い手がちょうど三本ある整数格子盤が存在する。

特にq≥8、N=2q+1では二担い手の場合がちょうど12型に分類され、すべて整数格子上で実現可能。二担い手の点数をq+u、q+v（u≥v≥0）、共有点数をcとすると、c≤2、u+v≤c+1であり、この整数条件が12型を尽くす。

禁止q点組数は0、C(m,q)（q≤m≤2q+1）、またはC(q+u,q)+C(q+v,q)に限られ、すべて実現可能。二担い手の全安全局面は、四群の占有数による通常・misèreの厳密再帰でO(N³)時間、N=2q+1の12型ではO(q²)時間で強解決できる。極大配置数と任意人数の完了履歴数も組合せ式で求まる。

**証拠の境界**：上界・鋭さ・分類・実現・再帰の正当性は全称的な数学的証明。q=8の12型における1,510,740安全局面の照合は有限独立検証。qに関する空盤Grundy値の無界閉公式、任意の大盤残局への無条件適用は主張しない。
