---
id: K0297
title: n≥2の全最小極大配置に一重被覆点があるか
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: supersedes
  target: K0138
  note: n=1の退化反例を除外したB078の修正版
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round47-private-cover-and-global-minima.md
  role: source
  note: n=2..8の全最小極大でmin b=1を完全確認
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round50-nine-board-private-point-family.md
  role: source
  note: n=9の限定16配置でもmin b=1
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/README.md
  role: source
  note: n=9の全最小極大配置1,179件を完全列挙し全件でmin b=1を確認
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/output/maximal_sets_n9.json
  role: certificate
  note: 列挙した1,179配置（D4第一石代表、全軌道を被覆）
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/output/n9_independent_verify.json
  role: data
  note: 行列式による独立min-b検証・禁止四点29152一致・round50 16/16整合
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/scripts/verify_n9.py
  role: verifier
  note: 曲線正規化を使わない独立検証器
---

# n≥2の全最小極大配置に一重被覆点があるか

標準n×n盤、n≥2について、最小極大サイズs_nを達成する全ての安全極大配置Sに、`b_S(p)=1` となる空点pが存在するかを問う。これはn=1の空点なし反例を除いたB078の非退化版である。

n=2..8では全最小極大配置を完全列挙し、全件で `min_{p∉S} b_S(p)=1` を確認済み。n=9も research/experiments/n9-minimum-maximal-catalogue-20261016 でサイズ9極大安全集合を完全列挙（15 D4代表・13,532,044,253節点・相異なる1,179配置）し、全件で `min_p b_S(p)=1`（非極大0・不安全0）。曲線正規化を使わない独立行列式verifierでも `{1:1179}` と一致し、禁止四点総数29,152も一致、round50の既知16配置も全て列挙集合内にD4像を持つ。

したがって **n=2..9 で成立**。n≥10を含む一般全称は未証明である。
