---
id: K0318
title: 禁止曲線の三つ組・点対充填から固定幅q点版の一般安定化上界が得られる
kind: proposition
status: proved
topics: [rectangles, geometry, variants, grundy]
aliases: []
relations:
- type: supports
  target: K0071
  note: 3×m・q=5の一般上界を56から40へ改善した
- type: supports
  target: K0302
  note: 個別の厳密閾値を閉じる有限区間を短縮する一般上界
artifacts:
- path: research/experiments/fixed-width/reports/curve-packing-fixed-width.md
  role: proof
  note: 三つ組・点対予算による一般定理
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/output/curve_packing_fixed_width.json
  role: data
  note: 上界表と小盤検査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/fixed-width/scripts/curve_packing_fixed_width.py
  role: verifier
  note: 整数最適化と全小盤予算不等式の再現
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 禁止曲線の三つ組・点対充填から固定幅q点版の一般安定化上界が得られる

幅w、禁止点数q≥4、各行容量r=q−1とする。石数不足の対象行を塞ぐ禁止円・直線が使う外部三つ組と点対は、異なる曲線間で重複できない。この予算を整数最適化すると、真の安定化長M_{w,q}に明示的な一般上界U_{w,q}を与えられる。

この定理だけで3×m・q=5の一般上界は56から40へ改善される。q≥7では固定幅wに対し追加項がqとともに発散しない簡潔な上界も得られる。

これは十分条件であり、個別の真の安定化長とは区別する。K0302の厳密値は、さらに専用算術と有限完全排除を使って閉じている。
