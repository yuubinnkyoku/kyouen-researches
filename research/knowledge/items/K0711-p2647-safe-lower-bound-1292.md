---
id: K0711
title: 剰余放物線Q_2647の最大安全サイズは1292以上1324以下
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線・共円四点を含まない安全集合
- type: depends_on
  target: K0706
  note: 全1323 dの修正版DRAT監査による上界A(2647)<=1324
- type: depends_on
  target: K0334
  note: 整数共円行列式が0なら四パラメータ和が0 mod pとなる必要条件
artifacts:
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/candidate.txt
  role: certificate
  note: ソート済み1292パラメータ。点は(t,t² mod 2647)
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/geometry.json
  role: data
  note: generic 4×4整数行列式で43730623候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-local-repair-20261109/verify_subset.cpp
  role: verifier
  note: 探索・CNF・edge cacheを読まない独立整数幾何検査器
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/model.json
  role: certificate
  note: 固定d=1323の元CNFで41違反の割当。最適性は未主張
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/assessment.json
  role: data
  note: 元53886節の直接評価41違反、1325点から33点除去した1292点候補
- path: research/experiments/parabola-local-repair-20261109/walk_initial.cpp
  role: solver
  note: 実際の100万flip・seed20261109の局所探索ソース
- path: research/experiments/parabola-local-repair-20261109/verify.py
  role: verifier
  note: 小規模比較回帰と明示的な証人監査の再現ドライバ
- path: research/experiments/parabola-local-repair-20261109/regression.json
  role: data
  note: 4玩具CNF、96小集合の2モード比較、7不正入力制御とhash照合
- path: research/experiments/parabola-local-repair-20261109/README.md
  role: source
  note: 構成、再現手順と信頼境界
scope: Q_2647={(t,t² mod 2647):0<=t<2647}の標準q=4安全集合。有限存在証人による下界1292とK0706の上界1324。正確値や他素数への一般化は主張しない。
evidence: 1292点証人を保存し、全115563355055選択四点を必要合同式と43730623回の直接整数4×4行列式で検査して禁止四点0件。上界はK0706の全d監査から従う。
---

## 命題と構成

**1292 <= A(2647) <= 1324**。正確な最大値は未確定。

保存CNF（p=2647,d=1323、1323変数・53886節）へ局所探索を100万flip、seed=20261109で行い、
元CNFの41節に違反する割当を得た。Pythonでも元の全節を直接評価して41違反と一致した。
対応する1325点の等号テンプレートから、違反節の支持を被覆する33点を除き、1292点を残した。
41は当該CNFの節削除距離の上界であり、最適値とは主張しない。

## 下界の独立検査

証人のパラメータの範囲・ソート・重複を検査し、座標を整数として再計算した。
探索とは別の検証器で、全115563355055選択四点を対象に必要合同式で候補を絞り、
43730623候補にgeneric 4×4 Leibniz行列式を適用して0件だった。生出力は
`2647 1292 115563355055 43730623`、終了コード0。

合同式フィルタの完全性は、行列式をmod pへ落とすとVandermonde積とパラメータ和の積になることによる。
異なる四パラメータで前者は非零だから、整数行列式0なら和は0 mod p。
各選択三点から唯一の第四パラメータを復元し、それが最大点のときだけ調べるので漏れ・重複がない。
検査器はCNF・モデル・edge cacheを使わない。したがって下界証人の安全性は、
局所探索やCNF符号化の正しさとは独立に確認される。

## 上界と限界

上界1324はK0706の全1323 dのUNSAT証明の修正版DRAT監査と等号還元から従う。
1292点集合の最大性、41違反の最小性、33点除去の最小性は未確定。
本項は有限計算の証人検査であり、Lean形式証明ではない。
小集合96例の全四点検査・合同式フィルタ・Python整数行列式の一致は回帰であり、
一般的健全性の証明と区別する。
