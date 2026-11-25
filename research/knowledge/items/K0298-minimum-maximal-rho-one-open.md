---
id: K0298
title: n≥2の全最小極大配置で故障耐性ρが1か
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: supersedes
  target: K0206
  note: n=1でρが定義できない問題を除外したB361の修正版
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round47-private-cover-and-global-minima.md
  role: source
  note: n=2..8の全最小極大でρ=1を完全確認
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round50-nine-board-private-point-family.md
  role: source
  note: n=9の限定16配置でもρ=1
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/README.md
  role: source
  note: n=9の全最小極大配置1,179件でmin b=1、従ってρ=1
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/output/maximal_sets_n9.json
  role: certificate
  note: 列挙した1,179配置（D4第一石代表、全軌道を被覆）
- path: research/experiments/n9-minimum-maximal-catalogue-20261016/output/n9_independent_verify.json
  role: data
  note: 独立min-b検証（{1:1179})。min b=1からρ=1が従う
---

# n≥2の全最小極大配置で故障耐性ρが1か

安全極大配置Sに対し、元から空だった点を少なくとも一つ合法に戻すために除く必要がある最小石数をρ(S)とする。n≥2の最小極大配置では常にρ(S)=1かを問う。

n=2..8では全最小極大配置を完全列挙し、全件でρ=1を確認済み。一重被覆点がある場合は、その禁止三つ組の石を一つ除けばその空点が合法になるのでK0297が成立する範囲では本問も成立する。n=9は research/experiments/n9-minimum-maximal-catalogue-20261016 で全最小極大配置（1,179配置）が min b=1 を満たすことを確認したので ρ=1 も従う。

したがって **n=2..9 で成立**。n≥10を含む一般全称は未証明である。

B361のn=1を含む原文はK0206で撤回し、この非退化版を一般問題として残す。

## 2026-10-17 bounded advance

New finite evidence: exhaustive minimal maximal sets n=2..5 rho=1 (counts 4,56,176,4); full recompute of 1,179 n=9 sets rho=1; five distinct 10-stone 10x10 maximal sets rho=1. Combined with n=6..8 complete enumeration, supported for n=2..10 tested configurations.

Scope clarification: no counterexample found; does not prove general statement for n>=10. Some empty points have b>=2 but rho=1 holds (triples share common stone).

Next steps: larger-n verification. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
