---
id: K0427
title: 4行8点円の弦長平方は法27で四つの型に限られる
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: depends_on
  target: K0073
  note: 円の二根和と平方弦長の二階差分条件を用いる
artifacts:
- path: research/experiments/fixed-width/reports/q48-mod27-chord-classification-20261015.md
  role: proof
  note: 全称的な法27必要条件と有限完全列挙の範囲を説明
- path: research/experiments/fixed-width/scripts/q48_mod27_chord_audit_20261015.py
  role: verifier
  note: 円係数と弦長の二つの剰余表示を独立に全列挙
- path: research/experiments/fixed-width/scripts/q48_mod27_circle_census_20261015.cpp
  role: verifier
  note: 最大弦長300万までの合同篩付き有限完全列挙
- path: research/experiments/fixed-width/scripts/q48_bc_independent_20261015.cpp
  role: verifier
  note: 中央二弦長からの独立列挙。250万までを照合
- path: research/experiments/fixed-width/output/q48-mod27-results-20261015.json
  role: data
  note: 有限列挙の型数と実行結果
- path: research/experiments/fixed-width/output/q48-patterns-B3000000-20261015.csv
  role: data
  note: 最大弦長300万までの11型
scope: 標準整数格子の4連続行に各2点を持つ全8点円。無界の合同条件と明記した有限列挙範囲。
evidence: 全円で (d0²,d1²,d2²,d3²) mod 27 は (1,9,9,1)、(10,9,0,10)、(10,0,9,10)、(19,0,0,19) のいずれか。中央二弦長は3の倍数で、両方が9の倍数なら第四型である。円の整数係数表示と法9剛性から全称証明する。最大弦長300万までの有限列挙も11型のみだが、第四型の実在・不存在や全盤長の完全分類は決めない。
---

法9の剛性と二階差分 `-8` を合わせると、法27で端の平方は等しく、中央二つの平方は9の倍数になる。平方剰余を法27で調べると上記の4組に限られる。全称結論は剰余列挙ではなく、報告に記した代数的導出による。

最大弦長300万までの11型という記述は有限完全列挙である。独立した中央二弦長走査は250万までで、300万までの結果は剰余篩付き列挙器の範囲に限る。第四型 `(19,0,0,19)` は同範囲で未出現だが、整数弦長での実現可能性は未解決。
